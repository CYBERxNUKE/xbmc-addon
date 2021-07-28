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
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2 as dom
from resources.lib.modules import cfscrape
from resources.lib.modules import jsunpack


class s0urce:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['primewire.ac', 'primewire.ink']
        self.base_link = 'https://primewire.ink/'
        self.moviesearch_link = '?keywords=%s&type=movie'
        self.tvsearch_link = '?keywords=%s&type=tv'
        self.search_link = '?search_keywords=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            query = self.search_link % urllib.quote_plus(title)
            query = urlparse.urljoin(self.base_link, query.lower())
            print query
            result = client.request(query, referer=self.base_link)
            result = client.parseDOM(result, 'div', attrs={'class': 'index_item.+?'})

            result = [(dom.parse_dom(i, 'a', req=['href', 'title'])[0]) for i in result if i]
            result = [(i.attrs['href']) for i in result if
                      cleantitle.get(title) == cleantitle.get(re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '',
                        i.attrs['title'], flags=re.I))][0]
            url = client.replaceHTMLCodes(result)
            url = url.encode('utf-8')
            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            query = self.tvsearch_link % urllib.quote_plus(
                cleantitle.query(tvshowtitle))
            query = urlparse.urljoin(self.base_link, query.lower())
            result = client.request(query, referer=self.base_link)
            result = client.parseDOM(result, 'div', attrs={'class': 'index_item.+?'})

            result = [(dom.parse_dom(i, 'a', req=['href', 'title'])[0]) for i in result if i]
            result = [
                (i.attrs['href']) for i in result if cleantitle.get(tvshowtitle) == cleantitle.get(
                    re.sub(
                        '(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)',
                        '',
                        i.attrs['title'],
                        flags=re.I))][0]

            url = client.replaceHTMLCodes(result)
            url = url.encode('utf-8')
            return url
        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = urlparse.urljoin(self.base_link, url) if url.startswith('/') else url
            url = url.split('online.html')[0]
            url = '%s%s-online.html' % (url, 'season-%01d-episode-%01d' % (int(season), int(episode)))

            url = client.replaceHTMLCodes(url)
            url = url.encode('utf-8')
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            url = urlparse.urljoin(self.base_link, url) if not url.startswith('http') else url

            result = client.request(url)
            data = re.findall(r'\s*(eval.+?)\s*</script', result, re.DOTALL)[1]
            data = jsunpack.unpack(data).replace('\\', '')

            patern = '''rtv='(.+?)';var aa='(.+?)';var ba='(.+?)';var ca='(.+?)';var da='(.+?)';var ea='(.+?)';var fa='(.+?)';var ia='(.+?)';var ja='(.+?)';var ka='(.+?)';'''
            links_url = re.findall(patern, data, re.DOTALL)[0]
            slug = 'slug={}'.format(url.split('/')[-1])
            links_url = self.base_link + [''.join(links_url)][0].replace('slug=', slug)
            links = client.request(links_url)
            links = client.parseDOM(links, 'tbody')

            for i in links:
                try: 
                    data = [
                        (client.parseDOM(i, 'a', ret='href')[0],
                         client.parseDOM(i, 'span', attrs={'class': 'version_host'})[0])][0]
                    url = urlparse.urljoin(self.base_link, data[0])
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    host = data[1]
                    valid, host = source_utils.is_host_valid(host, hostDict)
                    if not valid:
                        raise Exception()

                    quality = client.parseDOM(i, 'span', ret='class')[0]
                    quality, info = source_utils.get_release_quality(
                        quality, url)

                    sources.append({'source': host,
                                    'quality': quality,
                                    'language': 'en',
                                    'url': url,
                                    'direct': False,
                                    'debridonly': False})
                except BaseException:
                    pass

            return sources
        except Exception:
            return sources

    def resolve(self, url):
        try:

            if '/stream/' in url or '/watch/' in url:

                r = client.request(url, referer=self.base_link)
                link = client.parseDOM(r, 'a', ret='data-href', attrs={'id': 'iframe_play'})[0]
            else:
                try:

                    data = client.request(url, referer=self.base_link)
                    data = re.findall(r'\s*(eval.+?)\s*</script', data, re.DOTALL)[0]
                    link = jsunpack.unpack(data)
                    link = link.replace('\\', '')
                    if 'eval' in link:
                        link = jsunpack.unpack(link)
                    link = link.replace('\\', '')
                    host = re.findall('hosted=\'(.+?)\';var', link, re.DOTALL)[0]
                    if 'streamango' in host:
                        loc = re.findall('''loc\s*=\s*['"](.+?)['"]''', link, re.DOTALL)[0]
                        link = 'https://streamango.com/embed/{0}'.format(loc)
                    elif 'openload' in host:
                        loc = re.findall('''loc\s*=\s*['"](.+?)['"]''', link, re.DOTALL)[0]
                        link = 'https://openload.co/embed/{0}'.format(loc)
                    else:
                        link = re.findall('''loc\s*=\s*['"](.+?)['"]\;''', re.DOTALL)[0]
                except BaseException:
                    link = client.request(url, output='geturl', timeout=10)
                    print link
                    if link == url:
                        return
                    else:
                        return link

            return link
        except Exception:
            return

