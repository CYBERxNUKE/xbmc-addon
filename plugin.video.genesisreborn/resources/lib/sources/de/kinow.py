# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    Copyright (C) 2016 Exodus

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

import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['kinow.to']
        self.base_link = 'http://kinow.to'
        self.search_link = '/suche.html'

        self.year_link = '/jahr/%d.html'
        self.type_link = '/%s.html'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.__search([localtitle] + source_utils.aliases_to_array(aliases), year, 'filme')
            if not url and title != localtitle: url = self.__search([title] + source_utils.aliases_to_array(aliases), year, 'filme')
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year, 'serien')
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year, 'serien')
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            def __get_correct_link(_url, content, checkval):
                try:
                    if not _url:
                        return

                    _url = urlparse.urljoin(self.base_link, _url)
                    r = client.request(_url)

                    r = re.findall('<h4>%s[^>]*</h4>(.*?)<div' % content, r, re.DOTALL | re.IGNORECASE)[0]
                    r = re.compile('(<a.+?/a>)', re.DOTALL).findall(''.join(r))
                    r = [(dom_parser.parse_dom(i, 'a', req='href'), dom_parser.parse_dom(i, 'span')) for i in r]
                    r = [(i[0][0].attrs['href'], i[1][0].content) for i in r if i[0] and i[1]]
                    r = [(i[0], i[1] if i[1] else '0') for i in r]
                    r = [i[0] for i in r if int(i[1]) == int(checkval)][0]
                    r = re.sub('/(1080p|720p|x264|3d)', '', r, flags=re.I)

                    return source_utils.strip_domain(r)
                except:
                    return

            url = __get_correct_link(url, 'Staffel', season)
            url = __get_correct_link(url, 'Folge', episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            r = client.request(urlparse.urljoin(self.base_link, url))

            links = dom_parser.parse_dom(r, 'table')
            links = [i.content for i in links if dom_parser.parse_dom(i, 'span', attrs={'class': re.compile('linkSearch(-a)?')})]
            links = re.compile('(<a.+?/a>)', re.DOTALL).findall(''.join(links))
            links = [dom_parser.parse_dom(i, 'a', req='href') for i in links if re.findall('(.+?)\s*\(\d+\)\s*<', i)]
            links = [i[0].attrs['href'] for i in links if i]

            url = re.sub('/streams-\d+', '', url)

            for link in links:
                if '/englisch/' in link: continue
                if link != url: r = client.request(urlparse.urljoin(self.base_link, link))

                quality = 'SD'
                info = []

                detail = dom_parser.parse_dom(r, 'th', attrs={'class': 'thlink'})
                detail = [dom_parser.parse_dom(i, 'a', req='href') for i in detail]
                detail = [(i[0].attrs['href'], i[0].content.replace('&#9654;', '').strip()) for i in detail if i]

                if detail:
                    quality, info = source_utils.get_release_quality(detail[0][1])
                    r = client.request(urlparse.urljoin(self.base_link, detail[0][0]))

                r = dom_parser.parse_dom(r, 'table')
                r = [dom_parser.parse_dom(i, 'a', req=['href', 'title']) for i in r if not dom_parser.parse_dom(i, 'table')]
                r = [(l.attrs['href'], l.attrs['title']) for i in r for l in i if l.attrs['title']]

                info = ' | '.join(info)

                for stream_link, hoster in r:
                    valid, hoster = source_utils.is_host_valid(hoster, hostDict)
                    if not valid: continue

                    sources.append({'source': hoster, 'quality': quality, 'language': 'de', 'url': stream_link, 'info': info, 'direct': False, 'debridonly': False, 'checkquality': True})

            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            control.sleep(5000)

            url = urlparse.urljoin(self.base_link, url)
            url = client.request(url, output='geturl')
            if self.base_link not in url:
                return url
        except:
            return

    def __search(self, titles, year, content):
        try:
            t = [cleantitle.get(i) for i in set(titles) if i]

            c = client.request(urlparse.urljoin(self.base_link, self.year_link % int(year)), output='cookie')

            p = urllib.urlencode({'search': cleantitle.query(titles[0])})
            c = client.request(urlparse.urljoin(self.base_link, self.search_link), cookie=c, post=p, output='cookie')
            r = client.request(urlparse.urljoin(self.base_link, self.type_link % content), cookie=c, post=p)

            r = dom_parser.parse_dom(r, 'div', attrs={'id': 'content'})
            r = dom_parser.parse_dom(r, 'tr')
            r = [dom_parser.parse_dom(i, 'td') for i in r]
            r = [dom_parser.parse_dom(i, 'a', req='href') for i in r]
            r = [(i[0].attrs['href'], i[0].content, i[1].content) for i in r if i]
            r = [(i[0], i[1], re.findall('(.+?)\s<i>\((.+?)\)<', i[1]), i[2]) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '', i[3]) for i in r]
            r = [i[0] for i in r if (cleantitle.get(i[1]) in t or cleantitle.get(i[2]) in t) and i[3] == year][0]

            return source_utils.strip_domain(r)
        except:
            return