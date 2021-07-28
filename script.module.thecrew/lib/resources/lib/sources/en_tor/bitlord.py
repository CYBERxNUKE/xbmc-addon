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

import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class s0urce:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domain = ['bitlordsearch.com']
        self.base_link = 'http://www.bitlordsearch.com'
        self.search_link = '/search?q=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            if debrid.status() is False:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s %s' % (title, hdlr)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            url = self.search_link % urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, url)

            try:
                r = client.request(url)
                links = zip(client.parseDOM(r, 'a', attrs={'class': 'btn btn-default magnet-button stats-action banner-button'}, ret='href'), client.parseDOM(r, 'td', attrs={'class': 'size'}))

                for link in links:
                    url = link[0].replace('&amp;', '&')
                    url = re.sub(r'(&tr=.+)&dn=', '&dn=', url) # some links on bitlord &tr= before &dn=
                    url = url.split('&tr=')[0]
                    if 'magnet' not in url:
                        continue

                    size = int(link[1])

                    if any(x in url.lower() for x in ['french', 'italian', 'spanish', 'truefrench', 'dublado', 'dubbed']):
                        continue

                    name = url.split('&dn=')[1]
                    t = name.split(hdlr)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and')
                    if cleantitle.get(t) != cleantitle.get(title):
                        continue

                    if hdlr not in name:
                        continue

                    quality, info = source_utils.get_release_quality(name, url)

                    try:
                        if size < 5.12: raise Exception()
                        size = float(size) / 1024
                        size = '%.2f GB' % size
                        info.append(size)
                    except:
                        pass

                    info = ' | '.join(info)

                    sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                                'info': info, 'direct': False, 'debridonly': True})

                return sources

            except:
                return sources

        except:
            return sources


    def resolve(self, url):
        return url
