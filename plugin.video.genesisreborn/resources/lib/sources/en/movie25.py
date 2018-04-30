# -*- coding: utf-8 -*-

'''
    Flixnet Add-on

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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 0
        self.language = ['en']
        self.domains = ['movie25.ph', 'movie25.hk', 'tinklepad.is', 'tinklepad.ag', 'movie25.ag','5movies.to','movie25.unblocked.vc']
        self.base_link = 'https://movie25.unblocked.vc'
        self.search_link = '/search.php?q='
        self.search_link_2 = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAwODQ5Mjc2ODA5NjE4MzM5MDAwMzowdWd1c2phYm5scSZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='
        self.video_link = '/getlink.php?Action=get&lk=%s'

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

    def _search(self, title, year, aliases, headers):
        try:
            q = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(cleantitle.getsearch(title)))
            r = client.request(q)
            r = client.parseDOM(r, 'div', attrs={'class':'ml-img'})
            r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'img', ret='alt'))
            url = [i for i in r if cleantitle.get(title) == cleantitle.get(i[1]) and year in i[1]][0][0]

            return url
        except:
            pass



    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url == None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            aliases = eval(data['aliases'])
            headers = {}
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']

            if 'tvshowtitle' in data:    
                episode = data['episode']
                season = data['season']
                url = self._search(data['tvshowtitle'], data['year'], aliases, headers)
                url = url.replace('online-free','season-%s-episode-%s-online-free'%(season,episode))

            else:
                episode = None
                year = data['year']
                url = self._search(data['title'], data['year'], aliases, headers)

            
            url = url if 'http' in url else urlparse.urljoin(self.base_link, url)
            result = client.request(url);

            result = client.parseDOM(result, 'li', attrs={'class':'link-button'})
            links = client.parseDOM(result, 'a', ret='href')
            i = 0
            for l in links:
                if i == 10: break
                try:
                    l = l.split('=')[1]
                    l = urlparse.urljoin(self.base_link, self.video_link%l)
                    result = client.request(l, post={}, headers={'Referer':url})
                    u = result if 'http' in result else 'http:'+result 
                    if 'google' in u:
                        valid, hoster = source_utils.is_host_valid(u, hostDict)
                        urls, host, direct = source_utils.check_directstreams(u, hoster)
                        for x in urls: sources.append({'source': host, 'quality': x['quality'], 'language': 'en', 'url': x['url'], 'direct': direct, 'debridonly': False})
             
                    else:
                        valid, hoster = source_utils.is_host_valid(u, hostDict)
                        if not valid: continue
                        try:
                            u.decode('utf-8')
                            sources.append({'source': hoster, 'quality': 'SD', 'language': 'en', 'url': u, 'direct': False, 'debridonly': False})
                            i+=1
                        except:
                            pass
                    
                except:
                    pass       

            return sources
        except:
            return sources


    def resolve(self, url):
        if 'google' in url:
            return directstream.googlepass(url)
        else:
            return url