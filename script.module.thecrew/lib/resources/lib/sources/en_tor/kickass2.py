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

try: from urlparse import parse_qs, urljoin
except ImportError: from urllib.parse import parse_qs, urljoin
try: from urllib import urlencode, quote_plus, unquote
except ImportError: from urllib.parse import urlencode, quote_plus, unquote

import six

from resources.lib.modules import cache, cleantitle, client, control, debrid, log_utils, source_utils, utils




class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['kickass.love', 'kkickass.com', 'kkat.net', 'kickass-kat.com', 'kickasst.net', 'kickasst.org', 'kickasstorrents.id', 'thekat.cc', 'thekat.ch']
        self._base_link = None
        self.search_link = '/usearch/%s'

    @property
    def base_link(self):
        if self._base_link is None:
            self._base_link = cache.get(self.__get_base_url, 120, 'https://%s' % self.domains[0])
        return self._base_link

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False:
            return

        try:
            if url is None:
                return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|<|>|\|)', ' ', query)
            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url)
            html = client.request(url)
            if html is None:
                return sources
            html = html.replace('&nbsp;', ' ')
            try:
                rows = client.parseDOM(html, 'tr', attrs={'id': 'torrent_latest_torrents'})
            except Exception:
                return sources
            if rows is None:
                return sources

            for entry in rows:
                try:
                    try:
                        name = re.findall('class="cellMainLink">(.+?)</a>', entry, re.DOTALL)[0]
                        name = client.replaceHTMLCodes(name)
                        # t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*|3D)(\.|\)|\]|\s|)(.+|)', '', name, flags=re.I)
                        if not cleantitle.get(title) in cleantitle.get(name):
                            continue
                    except Exception:
                        continue

                    try:
                        y = re.findall('[\.|\(|\[|\s|\_|\-](S\d+E\d+|S\d+)[\.|\)|\]|\s|\_|\-]', name, re.I)[-1].upper()
                    except Exception:
                        y = re.findall('[\.|\(|\[|\s](\d{4}|S\d*E\d*|S\d*)[\.|\)|\]|\s]', name, re.I)[-1].upper()
                    if not y == hdlr:
                        continue

                    try:
                        link = 'magnet%s' % (re.findall('url=magnet(.+?)"', entry, re.DOTALL)[0])
                        link = str(unquote(six.ensure_text(link)).split('&tr')[0])
                    except Exception:
                        continue

                    quality, info = source_utils.get_release_quality(name, link)

                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', entry)[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except Exception:
                        pass

                    info = ' | '.join(info)

                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en',
                                    'url': link, 'info': info, 'direct': False, 'debridonly': True})
                except Exception:
                    continue

            check = [i for i in sources if not i['quality'] == 'CAM']
            if check:
                sources = check

            return sources
        except Exception:
            return sources

    def __get_base_url(self, fallback):
        try:
            for domain in self.domains:
                try:
                    url = 'https://%s' % domain
                    result = client.request(url, timeout='10')
                    search_n = re.findall('<input type="txt" name="(.+?)"', result, re.DOTALL)[0]
                    if search_n and 'q1' in search_n:
                        return url
                except Exception:
                    pass
        except Exception:
            pass

        return fallback

    def resolve(self, url):
        return url
