# -*- coding: utf-8 -*-

"""
    Covenant Add-on

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


try:
    import resolveurl

    debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()]

    if len(debrid_resolvers) == 0:
        # Support Rapidgator accounts! Unfortunately, `sources.py` assumes that rapidgator.net is only ever
        # accessed via a debrid service, so we add rapidgator as a debrid resolver and everything just works.
        # As a bonus(?), rapidgator links will be highlighted just like actual debrid links
        debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True, include_universal=False) if 'rapidgator.net' in resolver.domains]

except:
    debrid_resolvers = []


def status():
    return debrid_resolvers != []


def resolver(url, debrid, from_pack=None, return_list=False):
    try:
        debrid_resolver = [resolver for resolver in debrid_resolvers if resolver.name == debrid][0]
        debrid_resolver.login()

        if from_pack:
            _host, _media_id = debrid_resolver.get_host_and_id(url)
            url_list = debrid_resolver.get_media_url(_host, _media_id, return_all=True)
            if return_list:
                return url_list
            season, episode = from_pack.split('_')
            url = [s['link'] for s in url_list if matchEpisode(s['name'], season, episode)][0]

        _host, _media_id = debrid_resolver.get_host_and_id(url)
        stream_url = debrid_resolver.get_media_url(_host, _media_id)
        return stream_url
    except:
        from resources.lib.modules import log_utils
        log_utils.log('%s Resolve Failure' % debrid, 1)
        return None


def matchEpisode(filename, season, episode):
    import re
    filename = re.sub('[^A-Za-z0-9 ]+', ' ', filename.split('/')[-1]).lower()
    r = r"(?:[a-z\s*]|^)(?:%s|%s)\s*(?:e|x|episode)\s*(?:%s|%s)\s+" % (season.zfill(2), season, episode.zfill(2), episode)
    m = re.search(r, filename, flags=re.S)

    if m:
        return True


