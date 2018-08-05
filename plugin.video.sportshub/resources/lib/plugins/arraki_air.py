"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you can do 
    whatever you want with this stuff. Just Ask first when not released through
    the tools and parser GIT. If we meet some day, and you think this stuff is
    worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

    Changelog:
        2018.6.17
            - Initial Release


    Usage Examples:

    Text inside the tags are a formatted base64 encoded string. The format is below.
    View Mode and Sort By can both be ignored in the searches by using None in those blocks.
    Format: Base ID|Table Name|Max Results|Sort By|View Mode|API Key

    Returns the Tv Channels

    -- Base64 Unencoded String: appycq5PhSS0tygok|tv_channels|700|channel|None|keyikW1exArRfNAWj
    <dir>
        <title>TV Channels #1</title>
        <arraki_air>YXBweWNxNVBoU1MwdHlnb2t8dHZfY2hhbm5lbHN8NzAwfGNoYW5uZWx8Tm9uZXxrZXlpa1cxZXhBclJmTkFXag==</arraki_air>
    </dir>


    --------------------------------------------------------------

"""


from __future__ import absolute_import
import requests
import re
import os
import xbmc
import xbmcaddon
import json,traceback,xbmcgui
from koding import route
from ..plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from requests.exceptions import HTTPError
import posixpath
import time
from six.moves.urllib.parse import unquote
from six.moves.urllib.parse import quote

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
AddonName = xbmc.getInfoLabel('Container.PluginName')
AddonName = xbmcaddon.Addon(AddonName).getAddonInfo('id')


class ARRAKIAIR(Plugin):
    name = "arrakiair"

    def process_item(self, item_xml):
        if "<arraki_air>" in item_xml:
            item = JenItem(item_xml)
            result_item = {
                'label': item["title"],
                'icon': item.get("thumbnail", addon_icon),
                'fanart': item.get("fanart", addon_fanart),
                'mode': "ArrakiAir",
                'url': item.get("arraki_air", ""),
                'folder': True,
                'imdb': "0",
                'season': "0",
                'episode': "0",
                'info': {},
                'year': "0",
                'context': get_context_items(item),
                "summary": item.get("summary", None)
            }
            result_item["properties"] = {
                'fanart_image': result_item["fanart"]
            }
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='ArrakiAir', args=["url"])
def get_arraki_air_table(param_string):
    xml = ""
    param_string = param_string.decode('base64')
    param_string = param_string.split('|')

    view = param_string[4]
    sort = param_string[3]
    maxRecords = param_string[2]
    # App ID, Table ID, Max Results, Sort ID, View Mode, API Key

    at = Airtable(param_string[0], param_string[1], api_key=param_string[5])
    if sort.lower() == 'none' and view.lower() == 'none': match = at.get_all(maxRecords=maxRecords)
    elif sort.lower() == 'none' and view.lower() != 'none': match = at.get_all(maxRecords=maxRecords, view=[view])
    elif sort.lower() != 'none' and view.lower() == 'none': match = at.get_all(maxRecords=maxRecords, sort=[sort])
    elif sort.lower() != 'none' and view.lower() != 'none': match = at.get_all(maxRecords=maxRecords, sort=[sort], view=[view])

    for item in match:
        try:
            try:
                if item['fields']['channel']:
                    item['fields']['title'] = item['fields']['channel']
            except:
                pass

            xml_item = validate_at(item['fields'])
            if 'plugin' in item['fields']['link']:
                xml +=  "<plugin>"\
                        "   <title>%s</title>"\
                        "   <meta>"\
                        "       <summary>%s</summary>"\
                        "   </meta>"\
                        "   <link>" % (xml_item['title'],xml_item['summary'])
                xml +=  add_sublinks(xml_item)
                xml +=  "   </link>"\
                        "   <thumbnail>%s</thumbnail>"\
                        "   <fanart>%s</fanart>"\
                        "</plugin>" % (xml_item['thumbnail'],xml_item['fanart'])
            else:
                xml +=  "<item>"\
                        "   <title>%s</title>"\
                        "   <meta>"\
                        "       <summary>%s</summary>"\
                        "   </meta>"\
                        "   <link>" % (xml_item['title'],xml_item['summary'])
                xml +=  add_sublinks(xml_item)
                xml +=  "   </link>"\
                        "   <thumbnail>%s</thumbnail>"\
                        "   <fanart>%s</fanart>"\
                        "</item>" % (xml_item['thumbnail'],xml_item['fanart'])
        except:
            # continue here, so we can skip any invalid items
            continue

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


# Tag,Alternate
jen_checks = [ ['title','title'],['summary','title'],['link','link'],['thumbnail',addon_icon],['fanart',addon_fanart] ]
def validate_at(item):
    for tag in jen_checks:
        try:
            data_chk = item[tag[0]]
        except:
            if tag[0] == tag[1]:
                item[0] = ''
            else:
                try: item[0] = item[1]
                except: item[0] = ''
    return item


def add_sublinks(item_xml):
    xml = ''
    cnt = 1
    try:
        if item_xml['link'] != None and item_xml['link'] != '-':
            xml += "    <sublink>%s</sublink>" % (item_xml['link'])
    except:
        pass
    build = True
    while build == True:
        try:
            link = 'link'+str(cnt)
            cnt += 1
            if item_xml[link] != None and item_xml[link] != '-':
                xml += "    <sublink>%s</sublink>" % (item_xml[link])
        except:
            build = False
    
    return xml


class Airtable():

    VERSION = 'v0'
    API_BASE_URL = 'https://api.airtable.com/'
    API_LIMIT = 1.0 / 5  # 5 per second
    API_URL = posixpath.join(API_BASE_URL, VERSION)

    def __init__(self, base_key, table_name, api_key=None):
        """
        If api_key is not provided, :any:`AirtableAuth` will attempt
        to use ``os.environ['AIRTABLE_API_KEY']``
        """
        session = requests.Session()
        session.auth = AirtableAuth(api_key=api_key)
        self.session = session
        self.table_name = table_name
        urlsafe_table_name = quote(table_name, safe='')
        self.url_table = posixpath.join(self.API_URL, base_key,
                                        urlsafe_table_name)
        self.is_authenticated = self.validate_session(self.url_table)

    def validate_session(self, url):
        response = self.session.get(url, params={'maxRecords': 1})
        if response.ok:
            return True
        elif response.status_code == 404:
            raise ValueError('Invalid base or table name: {}'.format(url))
        else:
            raise ValueError('Authentication failed: {}'.format(response.reason))

    def _process_params(self, params):
        """
        Process params names or values as needed using filters
        """
        for param_name, param_value in params.copy().items():
            param_value = params.pop(param_name)
            ParamClass = AirtableParams._get(param_name)
            new_param = ParamClass(param_value).to_param_dict()
            params.update(new_param)
        return params

    def _process_response(self, response):
        # Removed due to IronPython Bug
        # https://github.com/IronLanguages/ironpython2/issues/242
        # if response.status_code == 422:
        #     raise HTTPError('Unprocessable Entity for url(
        #                        decoded): {}'.format(unquote(response.url)))
        response.raise_for_status()
        return response.json()

    def record_url(self, record_id):
        """ Builds URL with record id """
        return posixpath.join(self.url_table, record_id)

    def _request(self, method, url, params=None, json_data=None):
        response = self.session.request(method, url, params=params, json=json_data)
        # self._dump_request_data(response)
        return self._process_response(response)

    # def _dump_request_data(self, response):
    #     """ For Debugging """
    #     timestamp = str(time.time()).split('.')[-1]
    #     url = response.request.url
    #     method = response.request.method
    #     response_json = response.json()
    #     status = response.status_code
    #     filepath = os.path.join('tests', 'dump', '{}-{}_{}.json'.format(
    #                                                                 method,
    #                                                                 status,
    #                                                                 timestamp))
    #     dump = {
    #             'url': url,
    #             'method': method,
    #             'response_json': response_json,
    #             }
    #     with open(filepath, 'w') as fp:
    #         json.dump(dump, fp, indent=4)


    def _get(self, url, **params):
        processed_params = self._process_params(params)
        return self._request('get', url, params=processed_params)

    def _post(self, url, json_data):
        return self._request('post', url, json_data=json_data)

    def _put(self, url, json_data):
        return self._request('put', url, json_data=json_data)

    def _patch(self, url, json_data):
        return self._request('patch', url, json_data=json_data)

    def _delete(self, url):
        return self._request('delete', url)

    def get(self, record_id):
        """
        Retrieves a record by its id

        >>> record = airtable.get('recwPQIfs4wKPyc9D')

        Args:
            record_id(``str``): Airtable record id

        Returns:
            record (``dict``): Record
        """
        record_url = self.record_url(record_id)
        return self._get(record_url)

    def get_iter(self, **options):
        """
        Record Retriever Iterator

        Returns iterator with lists in batches according to pageSize.
        To get all records at once use :any:`get_all`

        >>> for page in airtable.get_iter():
        ...     for record in page:
        ...         print(record)
        [{'fields': ... }, ...]

        Keyword Args:
            maxRecords (``int``, optional): The maximum total number of records
                that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            pageSize (``int``, optional ): The number of records returned
                in each request. Must be less than or equal to 100.
                Default is 100. See :any:`PageSizeParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Airtable formula.
                See :any:`FormulaParam`.

        Returns:
            iterator (``list``): List of Records, grouped by pageSize

        """
        offset = None
        while True:
            data = self._get(self.url_table, offset=offset, **options)
            records = data.get('records', [])
            time.sleep(self.API_LIMIT)
            yield records
            offset = data.get('offset')
            if not offset:
                break

    def get_all(self, **options):
        """
        Retrieves all records repetitively and returns a single list.

        >>> airtable.get_all()
        >>> airtable.get_all(view='MyView', fields=['ColA', '-ColB'])
        >>> airtable.get_all(maxRecords=50)
        [{'fields': ... }, ...]

        Keyword Args:
            maxRecords (``int``, optional): The maximum total number of records
                that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.
            formula (``str``, optional): Airtable formula.
                See :any:`FormulaParam`.

        Returns:
            records (``list``): List of Records

        >>> records = get_all(maxRecords=3, view='All')

        """
        all_records = []
        for records in self.get_iter(**options):
            all_records.extend(records)
        return all_records

    def match(self, field_name, field_value, **options):
        """
        Returns first match found in :any:`get_all`

        >>> airtable.match('Name', 'John')
        {'fields': {'Name': 'John'} }

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.

        Keyword Args:
            maxRecords (``int``, optional): The maximum total number of records
                that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            record (``dict``): First record to match the field_value provided
        """
        formula = self.formula_from_name_and_value(field_name, field_value)
        options['formula'] = formula
        for record in self.get_all(**options):
            return record
        else:
             return {}

    def search(self, field_name, field_value, record=None, **options):
        """
        Returns all matching records found in :any:`get_all`

        >>> airtable.search('Gender', 'Male')
        [{'fields': {'Name': 'John', 'Gender': 'Male'}, ... ]

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.

        Keyword Args:
            maxRecords (``int``, optional): The maximum total number of records
                that will be returned. See :any:`MaxRecordsParam`
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            fields (``str``, ``list``, optional): Name of field or fields to
                be retrieved. Default is all fields. See :any:`FieldsParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            records (``list``): All records that matched ``field_value``

        """
        records = []
        formula = self.formula_from_name_and_value(field_name, field_value)
        options['formula'] = formula
        records = self.get_all(**options)
        return records

    def insert(self, fields):
        """
        Inserts a record

        >>> record = {'Name': 'John'}
        >>> airtable.insert(record)

        Args:
            fields(``dict``): Fields to insert.
                Must be dictionary with Column names as Key.

        Returns:
            record (``dict``): Inserted record

        """
        return self._post(self.url_table, json_data={"fields": fields})

    def _batch_request(self, func, iterable):
        """ Internal Function to limit batch calls to API limit """
        responses = []
        for item in iterable:
            responses.append(func(item))
            time.sleep(self.API_LIMIT)
        return responses

    def batch_insert(self, records):
        """
        Calls :any:`insert` repetitively, following set API Rate Limit (5/sec)
        To change the rate limit use ``airtable.API_LIMIT = 0.2``
        (5 per second)

        >>> records = [{'Name': 'John'}, {'Name': 'Marc'}]
        >>> airtable.batch_insert(records)

        Args:
            records(``list``): Records to insert

        Returns:
            records (``list``): list of added records

        """
        return self._batch_request(self.insert, records)

    def update(self, record_id, fields):
        """
        Updates a record by its record id.
        Only Fields passed are updated, the rest are left as is.

        >>> record = airtable.match('Employee Id', 'DD13332454')
        >>> fields = {'Status': 'Fired'}
        >>> airtable.update(record['id'], fields)

        Args:
            record_id(``str``): Id of Record to update
            fields(``dict``): Fields to update.
                Must be dictionary with Column names as Key

        Returns:
            record (``dict``): Updated record
        """
        record_url = self.record_url(record_id)
        return self._patch(record_url, json_data={"fields": fields})

    def update_by_field(self, field_name, field_value, fields, **options):
        """
        Updates the first record to match field name and value.
        Only Fields passed are updated, the rest are left as is.

        >>> record = {'Name': 'John', 'Tel': '540-255-5522'}
        >>> airtable.update_by_field('Name', 'John', record)

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.
            fields(``dict``): Fields to update.
                Must be dictionary with Column names as Key

        Keyword Args:
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            record (``dict``): Updated record
        """
        record = self.match(field_name, field_value, **options)
        return {} if not record else self.update(record['id'], fields)

    def replace(self, record_id, fields):
        """
        Replaces a record by its record id.
        All Fields are updated to match the new ``fields`` provided.
        If a field is not included in ``fields``, value will bet set to null.
        To update only selected fields, use :any:`update`.

        >>> record = airtable.match('Seat Number', '22A')
        >>> fields = {'PassangerName': 'Mike', 'Passport': 'YASD232-23'}
        >>> airtable.replace(record['id'], fields)

        Args:
            record_id(``str``): Id of Record to update
            fields(``dict``): Fields to replace with.
                Must be dictionary with Column names as Key.

        Returns:
            record (``dict``): New record
        """
        record_url = self.record_url(record_id)
        return self._put(record_url, json_data={"fields": fields})

    def replace_by_field(self, field_name, field_value, fields, **options):
        """
        Replaces the first record to match field name and value.
        All Fields are updated to match the new ``fields`` provided.
        If a field is not included in ``fields``, value will bet set to null.
        To update only selected fields, use :any:`update`.

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.
            fields(``dict``): Fields to replace with.
                Must be dictionary with Column names as Key.

        Keyword Args:
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            record (``dict``): New record
        """
        record = self.match(field_name, field_value, **options)
        return {} if not record else self.replace(record['id'], fields)

    def delete(self, record_id):
        """
        Deletes a record by its id

        >>> record = airtable.match('Employee Id', 'DD13332454')
        >>> airtable.delete(record['id'])

        Args:
            record_id(``str``): Airtable record id

        Returns:
            record (``dict``): Deleted Record
        """
        record_url = self.record_url(record_id)
        return self._delete(record_url)

    def delete_by_field(self, field_name, field_value, **options):
        """
        Deletes first record  to match provided ``field_name`` and
        ``field_value``.

        >>> record = airtable.delete_by_field('Employee Id', 'DD13332454')

        Args:
            field_name (``str``): Name of field to match (column name).
            field_value (``str``): Value of field to match.

        Keyword Args:
            view (``str``, optional): The name or ID of a view.
                See :any:`ViewParam`.
            sort (``list``, optional): List of fields to sort by.
                Default order is ascending. See :any:`SortParam`.

        Returns:
            record (``dict``): Deleted Record
        """
        record = self.match(field_name, field_value, **options)
        record_url = self.record_url(record['id'])
        return self._delete(record_url)


    def batch_delete(self, record_ids):
        """
        Calls :any:`delete` repetitively, following set API Rate Limit (5/sec)
        To change the rate limit use ``airtable.API_LIMIT = 0.2`` (5 per second)

        >>> record_ids = ['recwPQIfs4wKPyc9D', 'recwDxIfs3wDPyc3F']
        >>> airtable.batch_delete(records)

        Args:
            records(``list``): Record Ids to delete

        Returns:
            records (``list``): list of records deleted

        """
        return self._batch_request(self.delete, record_ids)


    def mirror(self, records, **options):
        """
        Deletes all records on table or view and replaces with records.

        >>> records = [{'Name': 'John'}, {'Name': 'Marc'}]

        >>> record = airtable.,mirror(records)

        If view options are provided, only records visible on that view will
        be deleted.

        >>> record = airtable.mirror(records, view='View')
        ([{'id': 'recwPQIfs4wKPyc9D', ... }], [{'deleted': True, ... }])

        Args:
            records(``list``): Records to insert

        Keyword Args:
            maxRecords (``int``, optional): The maximum total number of records
                that will be returned. See :any:`MaxRecordsParam`
            maxRecords (``int``, optional): Maximum number of records to retrieve

        Returns:
            records (``tuple``): (new_records, deleted_records)
        """

        all_record_ids = [r['id'] for r in self.get_all(**options)]
        deleted_records = self.batch_delete(all_record_ids)
        new_records = self.batch_insert(records)
        return (new_records, deleted_records)

    @staticmethod
    def formula_from_name_and_value(field_name, field_value):
        """ Creates a formula to match cells from from field_name and value """
        if isinstance(field_value, str):
            field_value = "'{}'".format(field_value)

        formula = "{{{name}}}={value}".format(name=field_name,
                                              value=field_value)
        return formula

    def __repr__(self):
        return '<Airtable table:{}>'.format(self.table_name)

"-------------------------------------------------------------"

class AirtableAuth(requests.auth.AuthBase):

    def __init__(self, api_key=None):
        """
        Authentication used by Airtable Class

        Args:
            api_key (``str``): Airtable API Key. Optional.
                If not set, it will look for
                enviroment variable ``AIRTABLE_API_KEY``
        """
        try:
            self.api_key = api_key or os.environ['AIRTABLE_API_KEY']
        except KeyError:
            raise KeyError('Api Key not found. Pass api_key as a kwarg \
                            or set an env var AIRTABLE_API_KEY with your key')

    def __call__(self, request):
        request.headers.update({'Authorization': 'Bearer {}'.format(self.api_key)})
        return request


"---------------------------------------------------------------"

"""
Parameter filters are instantiated internally
by using the corresponding keywords.

Filter names (kwargs) can be either the API camelCase name (ie ``maxRecords``)
or the snake-case equivalent (``max_records``).

Refer to the :any:`Airtable` class to verify which kwargs can be
used with each method.

The purpose of these classes is to 1. improve flexibility and
ways in which parameter filter values can be passed, and 2. properly format
the parameter names and values on the request url.

For more information see the full implementation below.

"""  #


class _BaseParam():

    def __init__(self, value):
        self.value = value

    def to_param_dict(self):
        return {self.param_name: self.value}


class _BaseStringArrayParam(_BaseParam):
    """
    Api Expects Array Of Strings:
    >>> ['FieldOne', 'Field2']

    Requests Params Input:
    >>> params={'fields': ['FieldOne', 'FieldTwo']}

    Requests Url Params Encoding:
    >>> ?fields=FieldOne&fields=FieldTwo

    Expected Url Params:
    >>> ?fields[]=FieldOne&fields[]=FieldTwo
    """

    def to_param_dict(self):
        encoded_param = self.param_name + '[]'
        return {encoded_param: self.value}


class _BaseObjectArrayParam(_BaseParam):
    """
    Api Expects Array of Objects:
    >>> [{field: "UUID", direction: "desc"}, {...}]

    Requests Params Input:
    >>> params={'sort': ['FieldOne', '-FieldTwo']}
    or
    >>> params={'sort': [('FieldOne', 'asc'), ('-FieldTwo', 'desc')]}

    Requests Url Params Encoding:
    >>> ?sort=field&sort=direction&sort=field&sort=direction

    Expected Url Params:
    >>> ?sort[0][field]=FieldOne&sort[0][direction]=asc
    """

    def to_param_dict(self):
        param_dict = {}
        for index, dictionary in enumerate(self.value):
            for key, value in dictionary.items():
                param_name = '{param_name}[{index}][{key}]'.format(
                                                    param_name=self.param_name,
                                                    index=index,
                                                    key=key)
                param_dict[param_name] = value
        return param_dict


class AirtableParams():

    class MaxRecordsParam(_BaseParam):
        """
        Max Records Param

        Kwargs:
            ``max_records=`` or ``maxRecords=``

        The maximum total number of records that will be returned.

        Usage:

        >>> airtable.get_all(view='My View')

        Args:
            max_records (``int``): The maximum total number of records that
                will be returned.


        """

        # Class Input > Output
        # >>> filter = MaxRecordsParam(100)
        # >>> filter.to_param_dict()
        # {'maxRecords: 100}

        param_name = 'maxRecords'
        kwarg = 'max_records'

    class ViewParam(_BaseParam):
        """
        View Param

        Kwargs:
            ``view=``

        If set, only the records in that view will be returned.
        The records will be sorted according to the order of the view.

        Usage:

        >>> airtable.get_all(view='My View')

        Args:
            view (``str``): The name or ID of a view.

        """

        # Class Input > Output
        # >>> filter = ViewParam('Name or Id Of View')
        # >>> filter.to_param_dict()
        # {'view: 'Name or Id Of View'}

        param_name = 'view'
        kwarg = param_name

    class PageSizeParam(_BaseParam):
        """
        Page Size Param

        Kwargs:
            ``page_size=`` or ``pageSize=``

        Limits the maximum number of records returned in each request.
        Default is 100.

        Usage:

        >>> airtable.get_all(page_size=50)

        Args:
            formula (``int``): The number of records returned in each request.
                Must be less than or equal to 100. Default is 100.

        """
        # Class Input > Output
        # >>> filter = PageSizeParam(50)
        # >>> filter.to_param_dict()
        # {'pageSize: 50}

        param_name = 'pageSize'
        kwarg = 'page_size'

    class FormulaParam(_BaseParam):
        """
        Formula Param

        Kwargs:
            ``formula=`` or ``filterByFormula=``

        The formula will be evaluated for each record, and if the result
        is not 0, false, "", NaN, [], or #Error! the record will be included
        in the response.

        If combined with view, only records in that view which satisfy the
        formula will be returned. For example, to only include records where
        ``COLUMN_A`` isn't empty, pass in: ``"NOT({COLUMN_A}='')"``

        For more information see
        `Airtable Docs on formulas. <https://airtable.com/api>`_

        Usage - Text Column is not empty:

        >>> airtable.get_all(formula="NOT({COLUMN_A}='')")

        Usage - Text Column contains:

        >>> airtable.get_all(formula="FIND('SomeSubText', {COLUMN_STR})=1")

        Args:
            formula (``str``): A valid Airtable formula.

        """

        # Class Input > Output
        # >>> param = FormulaParams("FIND('DUP', {COLUMN_STR})=1")
        # >>> param.to_param_dict()
        # {'formula': "FIND('WW')=1"}

        param_name = 'filterByFormula'
        kwarg = 'formula'



    class _OffsetParam(_BaseParam):
        """
        Offset Param

        Kwargs:
            ``offset=``

        If there are more records what was in the response,
        the response body will contain an offset value.
        To fetch the next page of records,
        include offset in the next request's parameters.

        This is used internally by :any:`get_all` and :any:`get_iter`.

        Usage:

        >>> airtable.get_iter(offset='recjAle5lryYOpMKk')

        Args:
            record_id (``str``, ``list``):

        """
        # Class Input > Output
        # >>> filter = _OffsetParam('recqgqThAnETLuH58')
        # >>> filter.to_param_dict()
        # {'offset: 'recqgqThAnETLuH58'}

        param_name = 'offset'
        kwarg = param_name

    class FieldsParam(_BaseStringArrayParam):
        """
        Fields Param

        Kwargs:
            ``fields=``

        Only data for fields whose names are in this list will be included in
        the records. If you don't need every field, you can use this parameter
        to reduce the amount of data transferred.

        Usage:

        >>> airtable.get(fields='ColumnA')

        Multiple Columns:

        >>> airtable.get(fields=['ColumnA', 'ColumnB'])

        Args:
            fields (``str``, ``list``): Name of columns you want to retrieve.

        """

        # Class Input > Output
        # >>> param = FieldsParam(['FieldOne', 'FieldTwo'])
        # >>> param.to_param_dict()
        # {'fields[]': ['FieldOne', 'FieldTwo']}

        param_name = 'fields'
        kwarg = param_name

    class SortParam(_BaseObjectArrayParam):
        """
        Sort Param

        Kwargs:
            ``sort=``

        Specifies how the records will be ordered. If you set the view
        parameter, the returned records in that view will be sorted by these
        fields.

        If sorting by multiple columns, column names can be passed as a list.
        Sorting Direction is ascending by default, but can be reversed by
        prefixing the column name with a minus sign ``-``, or passing
        ``COLUMN_NAME, DIRECTION`` tuples. Direction options
        are ``asc`` and ``desc``.

        Usage:

        >>> airtable.get(sort='ColumnA')

        Multiple Columns:

        >>> airtable.get(sort=['ColumnA', '-ColumnB'])

        Explicit Directions:

        >>> airtable.get(sort=[('ColumnA', 'asc'), ('ColumnB', 'desc')])

        Args:
            fields (``str``, ``list``): Name of columns and directions.

        """

        # Class Input > Output
        # >>> filter = SortParam([{'field': 'col', 'direction': 'asc'}])
        # >>> filter.to_param_dict()
        # {'sort[0]['field']: 'col', sort[0]['direction']: 'asc'}

        param_name = 'sort'
        kwarg = param_name

        def __init__(self, value):
            # Wraps string into list to avoid string iteration
            if hasattr(value, 'startswith'):
                value = [value]

            self.value = []
            direction = 'asc'

            for item in value:
                if not hasattr(item, 'startswith'):
                    field_name, direction = item
                else:
                    if item.startswith('-'):
                        direction = 'desc'
                        field_name = item[1:]
                    else:
                        field_name = item

                sort_param = {'field': field_name, 'direction': direction}
                self.value.append(sort_param)

    @classmethod
    def _discover_params(cls):
        """
        Returns a dict where filter keyword is key, and class is value.
        To handle param alias (maxRecords or max_records), both versions are
        added.
        """

        try:
            return cls.filters
        except AttributeError:
            filters = {}
            for param_class_name in dir(cls):
                param_class = getattr(cls, param_class_name)
                if hasattr(param_class, 'kwarg'):
                    filters[param_class.kwarg] = param_class
                    filters[param_class.param_name] = param_class
            cls.filters = filters
        return cls.filters

    @classmethod
    def _get(cls, kwarg_name):
        """ Returns a Param Class Instance, by its kwarg or param name """
        param_classes = cls._discover_params()
        try:
            param_class = param_classes[kwarg_name]
        except KeyError:
            raise ValueError('invalid param keyword {}'.format(kwarg_name))
        else:
            return param_class
