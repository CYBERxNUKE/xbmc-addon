# -*- coding: utf-8 -*-

'''
    Genesis Add-on
    Copyright (C) 2015 lambda

    -Mofidied by The Crew
    -Copyright (C) 2019 The Crew


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
'''
from resources.lib.modules import control, log_utils

try:
    import resolveurl

    debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True) if resolver.isUniversal()]

    if len(debrid_resolvers) == 0:
        # Support Rapidgator accounts! Unfortunately, `sources.py` assumes that rapidgator.net is only ever
        # accessed via a debrid service, so we add rapidgator as a debrid resolver and everything just works.
        # As a bonus(?), rapidgator links will be highlighted just like actual debrid links
        debrid_resolvers = [resolver() for resolver in resolveurl.relevant_resolvers(order_matters=True,include_universal=False) if 'rapidgator.net' in resolver.domains]

except:
    debrid_resolvers = []


def status(torrent=False):
    debrid_check = debrid_resolvers != []
    if debrid_check is True:
        if torrent:
            enabled = control.setting('torrent.enabled')
            if enabled == '' or enabled.lower() == 'true':
                return True
            else:
                return False
    return debrid_check


def resolver(url, debrid):
    try:
        debrid_resolver = [resolver for resolver in debrid_resolvers if resolver.name == debrid][0]

        debrid_resolver.login()
        _host, _media_id = debrid_resolver.get_host_and_id(url)
        stream_url = debrid_resolver.get_media_url(_host, _media_id)

        return stream_url
    except Exception as e:
        log_utils.log('%s Resolve Failure: %s' % (debrid, e), log_utils.LOGWARNING)
        return None
