# -*- coding: utf-8 -*-

'''
    Bubbles Add-on
    Copyright (C) 2016 Bubbles

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
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 0
        self.language = ['pl']
        self.domains = ['alluc.ee']
        self.base_link = 'https://www.alluc.ee'
        self.search_link = '/api/search/%s/?apikey=%s&getmeta=0&query=%s&count=%d&from=%d'
        self.types = ['stream']
        self.streamLimit = int(control.setting('alluc.limit'))
        self.streamIncrease = 100
        self.api = control.setting('alluc.api')
        self.debrid = control.setting('alluc.download')
        if self.debrid == 'true': self.types = ['stream', 'download']
        self.extensions = ['mp4', 'mpg', 'mpeg', 'mp2', 'm4v', 'm2v', 'mkv', 'avi', 'flv', 'asf', '3gp', '3g2', 'wmv', 'mov', 'qt', 'webm', 'vob', '']

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
            if url == None: return
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
            if url == None:
                raise Exception()

            if not (self.api and not self.api == ''):
                raise Exception()

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = int(data['year']) if 'year' in data and not data['year'] == None else None
            season = int(data['season']) if 'season' in data and not data['season'] == None else None
            episode = int(data['episode']) if 'episode' in data and not data['episode'] == None else None
            query = '%s S%02dE%02d' % (title, season, episode) if 'tvshowtitle' in data else '%s %d' % (title, year)

            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            query += ' lang:%s' % self.language[0]
            query = urllib.quote_plus(query)
            url = urlparse.urljoin(self.base_link, self.search_link)

            hostDict = hostprDict + hostDict

            iterations = self.streamLimit/self.streamIncrease
            last = self.streamLimit - (iterations * self.streamIncrease)
            if not last:
                iterations = iterations - 1
                last = self.streamIncrease
            iterations = iterations + 1

            seen_urls = set()
            for type in self.types:
                searchFrom = 0
                searchCount = self.streamIncrease
                for offset in range(iterations):
                    if iterations == offset + 1: searchCount = last
                    urlNew = url % (type, self.api, query, searchCount, searchFrom)
                    searchFrom = searchFrom + self.streamIncrease

                    results = client.request(urlNew)
                    results = json.loads(results)

                    apistatus  = results['status']
                    if apistatus != 'success': break

                    results = results['result']

                    added = False
                    for result in results:
                        try:
                            jsonName = result['title']
                            jsonSize = result['sizeinternal']
                            jsonExtension = result['extension']
                            jsonLanguage = result['lang']
                            jsonHoster = result['hostername'].lower()
                            jsonLink = result['hosterurls'][0]['url']
                            
                            
                            #### Clean Unwanted Stuff ########
                            
                            if not hdlr in jsonName.upper(): raise Exception() #showing wrong episodes a lot of times
                            
                            if '3D' in jsonName: raise Exception() #who cares?
                            
                            if not 'FRENCH' in title.upper():
                                if 'FRENCH' in jsonName.upper(): raise Exception() #showing up in french
                                
                            if not 'LATINO' in title.upper():
                                if 'LATINO' in jsonName.upper(): raise Exception() #showing up in spanish
                            
                            if 'SAMPLE' in jsonName.upper():  #samples showing up
                                if not 'SAMPLE' in title.upper(): raise Exception()
                                
                            if 'EXTRA' in jsonName.upper():#extras showing up
                                if not 'EXTRA' in title.upper(): raise Exception()
                             
                            ################################

                            if jsonLink in seen_urls: continue
                            seen_urls.add(jsonLink)

                            if not jsonHoster in hostDict: continue

                            if not self.extensionValid(jsonExtension): continue

                            quality, info = source_utils.get_release_quality(jsonName)
                            info.append(self.formatSize(jsonSize))
                            info.append(jsonName)
                            info = '|'.join(info)

                            sources.append({'source' : jsonHoster, 'quality':  quality, 'language' : jsonLanguage, 'url' : jsonLink, 'info': info, 'direct' : False, 'debridonly' : False})
                            added = True
                        except:
                            pass

                    if not added:
                        break

            return sources
        except:
            return sources

    def resolve(self, url):
      return url

    def extensionValid(self, extension):
        extension = extension.replace('.', '').replace(' ', '').lower()
        return extension in self.extensions

    def formatSize(self, size):
        if size == 0 or size is None: return ''
        size = int(size) / (1024 * 1024)
        if size > 2000:
            size = size / 1024
            unit = 'GB'
        else:
            unit = 'MB'
        size = '[B][%s %s][/B]' % (size, unit)
        return size
