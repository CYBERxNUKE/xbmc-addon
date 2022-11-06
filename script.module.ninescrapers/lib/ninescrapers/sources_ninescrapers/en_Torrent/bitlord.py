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

# - Converted to py3/2 for Nine


import re

from six.moves import zip

from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import debrid
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = ['bitlordsearch.com']
        self.base_link = custom_base or 'http://www.bitlordsearch.com'
        self.search_link = '/search?q=%s'
        self.aliases = []


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
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

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((title, hdlr))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            url = self.search_link % query.replace(' ', '.')
            url = urljoin(self.base_link, url)

            try:
                r = client.request(url)
                links = zip(client.parseDOM(r, 'a', attrs={'class': 'btn btn-default magnet-button stats-action banner-button'}, ret='href'), client.parseDOM(r, 'td', attrs={'class': 'size'}))

                for link in links:
                    try:
                        url = link[0].replace('&amp;', '&')
                        url = re.sub(r'(&tr=.+)&dn=', '&dn=', url) # some links on bitlord &tr= before &dn=
                        url = url.split('&tr=')[0]
                        if 'magnet' not in url:
                            continue

                        if any(x in url.lower() for x in ['french', 'italian', 'spanish', 'truefrench', 'dublado', 'dubbed']):
                            continue

                        name = cleantitle.get_title(url.split('&dn=')[1])
                        if not source_utils.is_match(name, title, hdlr, self.aliases):
                            continue

                        quality, info = source_utils.get_release_quality(name, url)

                        try:
                            size = link[1]
                            size = str(size) + ' GB' if len(str(size)) == 1 else str(size) + ' MB'
                            dsize, isize = source_utils._size(size)
                        except:
                            dsize, isize = 0.0, ''

                        info.insert(0, isize)
                        info = ' | '.join(info)

                        sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                        'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                    except:
                        continue
            except:
                pass

            if 'tvshowtitle' in data:
                for source in self.pack_sources(title, data['season'], data['episode']):
                    sources.append(source)

            return sources

        except:
            log_utils.log('bitlord - Exception', 1)
            return sources


    def pack_sources(self, title, season, episode):
        sources = []
        try:
            query = '%s S%02d' % (title, int(season))
            url = self.search_link % query.replace(' ', '.')
            url = urljoin(self.base_link, url)

            r = client.request(url)
            links = zip(client.parseDOM(r, 'a', attrs={'class': 'btn btn-default magnet-button stats-action banner-button'}, ret='href'), client.parseDOM(r, 'td', attrs={'class': 'size'}))

            for link in links:
                try:
                    url = link[0].replace('&amp;', '&')
                    url = re.sub(r'(&tr=.+)&dn=', '&dn=', url) # some links on bitlord &tr= before &dn=
                    url = url.split('&tr=')[0]
                    if 'magnet' not in url:
                        continue

                    if any(x in url.lower() for x in ['french', 'italian', 'spanish', 'truefrench', 'dublado', 'dubbed']):
                        continue

                    name = cleantitle.get_title(url.split('&dn=')[1])
                    if not source_utils.is_season_match(name, title, season, self.aliases):
                        continue

                    pack = '%s_%s' % (season, episode)

                    quality, info = source_utils.get_release_quality(name, url)

                    try:
                        size = link[1]
                        size = str(size) + ' GB' if len(str(size)) == 1 else str(size) + ' MB'
                        dsize, isize = source_utils._size(size)
                    except:
                        dsize, isize = 0.0, ''

                    info.insert(0, isize)
                    info = ' | '.join(info)

                    sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': False, 'debridonly': True, 'size': dsize, 'name': name, 'pack': pack})
                except:
                    continue

            return sources

        except:
            log_utils.log('bitlord pack Exception', 1)
            return sources


    def resolve(self, url):
        return url
