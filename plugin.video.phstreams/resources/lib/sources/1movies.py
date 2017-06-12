# -*- coding: utf-8 -*-

'''
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
'''


import re,urllib,urlparse,json,base64

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import cache

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['1movies.tv']
        self.base_link = 'https://1movies.tv'
        self.search_link = '/movies/search?s=%s'

    def matchAlias(self, title, aliases):
        try:
            for alias in aliases:
                if cleantitle.get(title) == cleantitle.get(alias['title']):
                    return True
        except:
            return False

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': title})
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except:
            return

    def searchShow(self, title, season, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            t = cleantitle.get(title)
            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query('%s Season %01d' % (title.replace('\'', '-'), int(season)))))
            r = client.request(url, timeout='10')
            r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
            if r:
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(i[0], re.findall('(.+?)\s+-\s+Season\s+(\d+)', i[1])) for i in r]
                r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
                r = [i[0] for i in r if t == cleantitle.get(i[1]) and int(season) == int(i[2])][0]
            else:
                url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.query('%s %01d' % (title.replace('\'', '-'), int(year)))))
                r = client.request(url, timeout='10')
                r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
                r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
                r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
                r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
                r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
                r = [i[0] for i in r if t == cleantitle.get(i[1]) and year == i[2]][0]
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url.encode('utf-8')
        except:
            return

    def searchMovie(self, title, year, aliases, headers):
        try:
            title = cleantitle.normalize(title)
            url = urlparse.urljoin(self.base_link, self.search_link % (cleantitle.geturl(title.replace('\'', '-'))))
            r = client.request(url, timeout='10', headers=headers)
            r = client.parseDOM(r, 'h2', attrs={'class': 'tit'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in r]
            r = [(i[0][0], i[1][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0]
            r = [(i[0], re.findall('(.+?) \((\d{4})', i[1])) for i in r]
            r = [(i[0], i[1][0][0], i[1][0][1]) for i in r if len(i[1]) > 0]
            r = [i[0] for i in r if self.matchAlias(i[1], aliases) and year == i[2]][0]
            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url.encode('utf-8')
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            headers = {}

            if 'tvshowtitle' in data:
                episode = int(data['episode'])
                url = self.searchShow(data['tvshowtitle'], data['season'], data['year'], aliases, headers)
            else:
                episode = 0
                url = self.searchMovie(data['title'], data['year'], aliases, headers)

            if url == None: return sources

            url = urlparse.urljoin(self.base_link, url)
            p = client.request(url, timeout='10')

            if episode > 0:
                r = client.parseDOM(p, 'div', attrs={'class': 'ep_link.+?'})[0]
                r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'a'))
                r = [(i[0], re.findall('Episode\s+(\d+)', i[1])) for i in r]
                r = [(i[0], i[1][0]) for i in r]
                r = [i[0] for i in r if int(i[1]) == episode][0]
                p = client.request(r, timeout='10')

            p = re.findall('load_player\((\d+)\)', p)
            p = urllib.urlencode({'id': p[0]})
            headers = {'Referer': url}
            r = urlparse.urljoin(self.base_link, '/ajax/movie/load_player_v3')
            r = client.request(r, post=p, headers=headers, XHR=True, timeout='10')
            url = json.loads(r)['value']
            if (url.startswith('//')):
                url = 'https:' + url
            url = client.request(url, headers=headers, XHR=True, output='geturl', timeout='10')

            if 'openload.io' in url or 'openload.co' in url or 'oload.tv' in url:
                sources.append({'source': 'openload.co', 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,'debridonly': False})
                raise Exception()

            r = client.request(url, headers=headers, XHR=True, timeout='10')
            try:
                src = json.loads(r)['playlist'][0]['sources']
                links = [i['file'] for i in src if 'file' in i]
                for i in links:
                    try:
                        sources.append(
                            {'source': 'gvideo', 'quality': directstream.googletag(i)[0]['quality'], 'language': 'en',
                             'url': i, 'direct': True, 'debridonly': False})
                    except:
                        pass
            except:
                pass

            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            for i in range(3):
                u = directstream.googlepass(url)
                if not u == None: break
            return u
        except:
            return