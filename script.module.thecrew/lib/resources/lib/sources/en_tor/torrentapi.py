# -*- coding: utf-8 -*-

'''
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

import re,urllib,urlparse,json
from resources.lib.modules import client,debrid,source_utils
from resources.lib.modules import dom_parser2 as dom


class s0urce:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.tvsearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_string={1}&{2}'
        self.msearch = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&token={0}&mode=search&search_imdb={1}&{2}'
        self.token = 'https://torrentapi.org/pubapi_v2.php?app_id=Torapi&get_token=get_token'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return sources
            if debrid.status() == False: raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            query = '%s S%02dE%02d' % (data['tvshowtitle'], int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else '%s' % data['imdb']
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            token = client.request(self.token)
            token = json.loads(token)["token"]
            if 'tvshowtitle' in data:
                search_link = self.tvsearch.format(token, urllib.quote_plus(query), 'format=json_extended')
            else:
                search_link = self.msearch.format(token, data['imdb'], 'format=json_extended')
            rjson = client.request(search_link)
            files = json.loads(rjson)['torrent_results']
            for file in files:
                name = file["title"]
                quality, info = source_utils.get_release_quality(name, name)
                size = source_utils.convert_size(file["size"])
                info.append(size)
                info = ' | '.join(info)
                url = file["download"]
                url = url.split('&tr')[0]
                sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True})
            return sources
        except BaseException:
            return sources


    def resolve(self, url):
        return url