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

import base64
import json
import re
import urllib
import urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import directstream
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.domains = ['seriesever.net']
        self.base_link = 'http://seriesever.net'
        self.search_link = 'service/search?q=%s'
        self.part_link = 'service/get_video_part'

        self.login_link = 'service/login'
        self.user = control.setting('seriesever.user')
        self.password = control.setting('seriesever.pass')


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.__search([localtvshowtitle] + source_utils.aliases_to_array(aliases), year)
            if not url and tvshowtitle != localtvshowtitle: url = self.__search([tvshowtitle] + source_utils.aliases_to_array(aliases), year)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            url = re.sub('\.\w+$', '', url)
            return url + '/staffel-%s-episode-%s.html' % (season, episode)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if url == None:
                return sources

            url = urlparse.urljoin(self.base_link, url)

            cookie = self.__get_premium_cookie()

            r = client.request(url, mobile=True, cookie=cookie)

            query = urlparse.urljoin(self.base_link, self.part_link)
            id = re.compile('var\s*video_id\s*=\s*"(\d+)"').findall(r)[0]

            p = dom_parser.parse_dom(r, 'a', attrs={'class': 'changePart', 'data-part': re.compile('\d+p')}, req='data-part')

            for i in p:
                i = i.attrs['data-part']

                p = urllib.urlencode({'video_id': id, 'part_name': i, 'page': '0'})
                p = client.request(query, cookie=cookie, mobile=True, XHR=True, post=p, referer=url)

                p = json.loads(p)
                p = p.get('part_count', 0)

                for part_count in range(0, p):
                    try:
                        r = urllib.urlencode({'video_id': id, 'part_name': i, 'page': part_count})
                        r = client.request(query, cookie=cookie, mobile=True, XHR=True, post=r, referer=url)

                        r = json.loads(r)
                        r = r.get('part', {})

                        s = r.get('source', '')
                        url = r.get('code', '')

                        if s == 'url' and 'http' not in url:
                            url = self.__decode_hash(url)
                        elif s == 'other':
                            url = dom_parser.parse_dom(url, 'iframe', req='src')
                            if len(url) < 1: continue
                            url = url[0].attrs['src']
                            if '/old/seframer.php' in url: url = self.__get_old_url(url)

                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if not valid: continue

                        if i in ['720p', 'HD']: quali = 'HD'
                        elif i in ['1080p', '1440p']: quali = i
                        elif i in ['2160p']: quali = '4K'
                        else: quali = 'SD'

                        if 'google' in url: host = 'gvideo'; direct = True; urls = directstream.google(url)
                        elif 'ok.ru' in url: host = 'vk'; direct = True; urls = directstream.odnoklassniki(url)
                        elif 'vk.com' in url: host = 'vk'; direct = True; urls = directstream.vk(url)
                        else: direct = False; urls = [{'quality': quali, 'url': url}]

                        for i in urls: sources.append({'source': host, 'quality': i['quality'], 'language': 'de', 'url': i['url'], 'direct': direct, 'debridonly': False})
                    except:
                        pass

            return sources
        except:
            return sources

    def resolve(self, url):
        if url.startswith('/'): url = 'http:%s' % url
        return url

    def __search(self, titles, year):
        try:
            query = self.search_link % (urllib.quote_plus(titles[0]))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) for i in set(titles) if i]
            y = ['%s' % str(year), '%s' % str(int(year) + 1), '%s' % str(int(year) - 1), '0']

            r = client.request(query, XHR=True)

            if r and r.startswith('{'): r = '[%s]' % r

            r = json.loads(r)
            r = [(i['url'], i['name']) for i in r if 'name' in i and 'url' in i]
            r = [(i[0], i[1], re.findall('(.+?) \(*(\d{4})?\)*$', i[1])) for i in r]
            r = [(i[0], i[2][0][0] if len(i[2]) > 0 else i[1], i[2][0][1] if len(i[2]) > 0 else '0') for i in r]
            r = sorted(r, key=lambda i: int(i[2]), reverse=True)  # with year > no year
            r = [i[0] for i in r if cleantitle.get(i[1]) in t and i[2] in y][0]

            url = source_utils.strip_domain(r)
            url = url.replace('serien/', '')
            return url
        except:
            return

    def __decode_hash(self, hash):
        hash = hash.replace("!BeF", "R")
        hash = hash.replace("@jkp", "Ax")
        hash += '=' * (-len(hash) % 4)
        try: return base64.b64decode(hash)
        except: return

    def __get_old_url(self, url):
        try:
            r = client.request(url, mobile=True)
            url = re.findall('url="(.*?)"', r)

            if len(url) == 0:
                url = dom_parser.parse_dom(r, 'iframe', req='src')[0].attrs['src']
                if "play/se.php" in url:
                    r = client.request(url, mobile=True)
                    return self.__decode_hash(re.findall('link:"(.*?)"', r)[0])
            else:
                return url[0]
        except:
            return

    def __get_premium_cookie(self):
        try:
            if (self.user == '' or self.password == ''): raise Exception()
            login = urlparse.urljoin(self.base_link, self.login_link)
            post = urllib.urlencode({'username': self.user, 'password': self.password})
            cookie = client.request(login, mobile=True, post=post, XHR=True, output='cookie')
            r = client.request(urlparse.urljoin(self.base_link, 'api'), mobile=True, cookie=cookie)
            return cookie if r == '1' else ''
        except:
            return ''