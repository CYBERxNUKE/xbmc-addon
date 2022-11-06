# -*- coding: utf-8 -*-
# - Converted to py3/2 for Nine

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

import re, time

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import cleantitle
from ninescrapers.modules import dom_parser
from ninescrapers.modules import client
from ninescrapers.modules import debrid
from ninescrapers.modules import source_utils
from ninescrapers.modules import workers
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['rapidmoviez.cr', 'rmz.cr']
        self.base_link = custom_base or 'https://rmz.cr'
        self.search_link = '/search/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('RMZ - Exception', 1)
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('RMZ - Exception', 1)
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None: return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            log_utils.log('RMZ - Exception', 1)
            return

    # def search(self, title, year):
        # try:
            # url = urljoin(self.base_link, self.search_link % (quote_plus(title)))
            # headers = {'User-Agent': client.agent()}
            # r = cfScraper.get(url, headers=headers, timeout=10).text
            # r = dom_parser.parse_dom(r, 'div', {'class': 'list_items'})[0]
            # r = dom_parser.parse_dom(r.content, 'li')
            # r = [(dom_parser.parse_dom(i, 'a', {'class': 'title'})) for i in r]
            # r = [(i[0].attrs['href'], i[0].content) for i in r]
            # r = [(urljoin(self.base_link, i[0])) for i in r if cleantitle.get(title) in cleantitle.get(i[1]) and year in i[1]]
            # if r: return r[0]
            # else: return
        # except:
            # log_utils.log('RMZ - Exception', 1)
            # return

    def search(self, title, hdlr2, imdb):
        try:
            imdb = re.sub(r'[^0-9]', '', imdb)
            url = urljoin(self.base_link, self.search_link % (quote_plus(title)))
            headers = {'User-Agent': client.agent()}
            r = cfScraper.get(url, headers=headers, timeout=10).text
            r1 = client.parseDOM(r, 'div', attrs={'class': 'list_items'})[0]
            r1 = client.parseDOM(r1, 'li')
            try:
                r1 = [i for i in r1 if imdb in i][0]
                r1 = client.parseDOM(r1, 'a', ret='href')[0]
                return urljoin(self.base_link, r1)
            except:
                r2 = client.parseDOM(r, 'div', attrs={'class': 'list'})
                r2 = [i for i in r2 if '<h3>Releases' in i][0]
                r2 = client.parseDOM(r2, 'div', attrs={'class': 'list_items'})[0]
                r2 = client.parseDOM(r2, 'li')
                r2 = [i for i in r2 if imdb in i]
                if hdlr2:
                    r2 = [i for i in r2 if hdlr2 in i]
                r2 = [client.parseDOM(u, 'a', ret='href')[0] for u in r2]
                r2 = [urljoin(self.base_link, u) for u in r2]
                return r2
        except:
            log_utils.log('RMZ - Exception', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        self.sources = []

        try:
            if url is None:
                return self.sources

            if debrid.status() is False:
                return self.sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)

            hdlr = data['year']
            hdlr2 = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else ''
            imdb = data['imdb']

            url = self.search(title, hdlr2, imdb)
            #log_utils.log('rmz url: ' + repr(url))

            urls = []

            if not isinstance(url, list):
                headers = {'User-Agent': client.agent()}
                r = cfScraper.get(url, headers=headers, timeout=10).text

                if hdlr2 == '':
                    r = dom_parser.parse_dom(r, 'ul', {'id': 'releases'})[0]
                else:
                    r = dom_parser.parse_dom(r, 'ul', {'id': 'episodes'})[0]
                r = dom_parser.parse_dom(r.content, 'a', req=['href'])
                urls.extend([(i.content, urljoin(self.base_link, i.attrs['href'])) for i in r if i and i.content != 'Watch'])
                if hdlr2 != '':
                    urls = [(i[0], i[1]) for i in urls if hdlr2.lower() in i[0].lower()]
            else:
                urls.extend([('', u) for u in url])

            self.hostDict = hostDict + hostprDict
            threads = []

            for i in urls:
                threads.append(workers.Thread(self._get_sources, i[0], i[1]))
            [i.start() for i in threads]

            alive = [x for x in threads if x.is_alive() is True]
            while alive:
                alive = [x for x in threads if x.is_alive() is True]
                time.sleep(0.1)
            return self.sources
        except:
            log_utils.log('RMZ - Exception', 1)
            return self.sources

    def _get_sources(self, name, url):
        try:
            headers = {'User-Agent': client.agent()}
            r = cfScraper.get(url, headers=headers, timeout=10).text
            urls = []

            if not name:
                name_size = client.parseDOM(r, 'div', attrs={'class': 'blog-details clear'})[0]
                name_size = client.parseDOM(name_size, 'h2')[0]
                name = name_size.split('<br')[0]
            else:
                name_size = client.replaceHTMLCodes(name)
                name = re.sub(r'\[.*?\]', '', name_size)
            name = cleantitle.get_title(name)


            links = zip(client.parseDOM(r, 'h4', attrs={'class': 'links'}), client.parseDOM(r, 'pre', attrs={'class': 'links'}))
            for l in links:
                if 'rapidrar' in l[0].lower():
                    continue
                _urls = re.findall(r'''((?:http|ftp|https)://[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])''', l[1], flags=re.MULTILINE|re.DOTALL)
                if 'clicknupload' in l[0].lower():
                    urls.append(_urls[0])
                else:
                    urls.extend(_urls)
            urls = [i for i in urls if not i.endswith(('.rar', '.rar.html', '.zip', '.iso', '.idx', '.sub', '.srt', '.ass', '.ssa'))]

            for url in urls:
                if url in str(self.sources):
                    continue

                quality, info = source_utils.get_release_quality(name, url)
                try:
                    size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', name_size)[0]
                    dsize, isize = source_utils._size(size)
                except:
                    dsize, isize = 0.0, ''
                info.insert(0, isize)
                info = ' | '.join(info)

                valid, host = source_utils.is_host_valid(url, self.hostDict)
                if not valid:
                    continue
                self.sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
        except:
            #log_utils.log('RMZ - Exception', 1)
            pass

    def resolve(self, url):
        return url
