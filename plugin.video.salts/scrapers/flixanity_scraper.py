"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

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
import re
import time
import urllib
import urlparse
import string
import random
import hashlib
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
from salts_lib.utils2 import i18n
import scraper


BASE_URL = 'http://flixanity.watch'
EMBED_URL = '/ajax/embeds.php'
SEARCH_URL = '/api/v1/cautare/upd'
KEY = 'MEE2cnUzNXl5aTV5bjRUSFlwSnF5MFg4MnRFOTVidFY='

class Scraper(scraper.Scraper):
    base_url = BASE_URL
    __token = None
    __t = None

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))
        self.username = kodi.get_setting('%s-username' % (self.get_name()))
        self.password = kodi.get_setting('%s-password' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Flixanity'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            if video.video_type == VIDEO_TYPES.MOVIE:
                action = 'getMovieEmb'
            else:
                action = 'getEpisodeEmb'
            match = re.search('elid\s*=\s*"([^"]+)', html)
            if self.__token is None:
                self.__get_token()
                
            if match and self.__token is not None:
                elid = urllib.quote(base64.encodestring(str(int(time.time()))).strip())
                data = {'action': action, 'idEl': match.group(1), 'token': self.__token, 'elid': elid}
                ajax_url = urlparse.urljoin(self.base_url, EMBED_URL)
                headers = {'Authorization': 'Bearer %s' % (self.__get_bearer()), 'Referer': page_url}
                headers.update(XHR)
                html = self._http_get(ajax_url, data=data, headers=headers, cache_limit=.5)
                html = html.replace('\\"', '"').replace('\\/', '/')
                 
                pattern = '<IFRAME\s+SRC="([^"]+)'
                for match in re.finditer(pattern, html, re.DOTALL | re.I):
                    url = match.group(1)
                    host = self._get_direct_hostname(url)
                    if host == 'gvideo':
                        direct = True
                        quality = scraper_utils.gv_get_quality(url)
                    else:
                        if 'vk.com' in url and url.endswith('oid='): continue  # skip bad vk.com links
                        direct = False
                        host = urlparse.urlparse(url).hostname
                        quality = scraper_utils.get_quality(video, host, QUALITIES.HD720)
    
                    source = {'multi-part': False, 'url': url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                    sources.append(source)

        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        self.__get_token()
        if self.__token is not None:
            search_url = urlparse.urljoin(self.base_url, self.__get_search_url())
            timestamp = int(time.time() * 1000)
            s = self.__get_s()
            query = {'q': title, 'limit': '100', 'timestamp': timestamp, 'verifiedCheck': self.__token, 'set': s, 'rt': self.__get_rt(self.__token + s),
                     'sl': self.__get_sl(search_url)}
            headers = {'Referer': self.base_url}
            headers.update(XHR)
            html = self._http_get(search_url, data=query, headers=headers, cache_limit=1)
            if video_type in [VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE]:
                media_type = 'TV SHOW'
            else:
                media_type = 'MOVIE'
    
            for item in scraper_utils.parse_json(html, search_url):
                if item['meta'].upper().startswith(media_type):
                    match_year = str(item['year']) if 'year' in item and item['year'] else ''
                    if not year or not match_year or year == match_year:
                        
                        result = {'title': scraper_utils.cleanse_title(item['title']), 'url': scraper_utils.pathify_url(item['permalink'].replace('/show/', '/tv-show/')), 'year': match_year}
                        results.append(result)

        return results

    def _get_episode_url(self, show_url, video):
        season_url = show_url + '/season/%s' % (video.season)
        episode_pattern = 'href="([^"]+/season/%s/episode/%s/?)"' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+/season/%s/episode/%s/?)"\s+title="(?P<title>[^"]+)'
        headers = {'Referer': urlparse.urljoin(self.base_url, show_url)}
        return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern, headers=headers)

    @classmethod
    def get_settings(cls):
        settings = super(cls, cls).get_settings()
        name = cls.get_name()
        settings.append('         <setting id="%s-username" type="text" label="     %s" default="" visible="eq(-4,true)"/>' % (name, i18n('username')))
        settings.append('         <setting id="%s-password" type="text" label="     %s" option="hidden" default="" visible="eq(-5,true)"/>' % (name, i18n('password')))
        return settings

    def _http_get(self, url, data=None, headers=None, method=None, cache_limit=8):
        # return all uncached blank pages if no user or pass
        if not self.username or not self.password:
            return ''

        html = super(self.__class__, self)._http_get(url, data=data, headers=headers, method=method, cache_limit=cache_limit)
        if '<span>Log In</span>' in html:
            log_utils.log('Logging in for url (%s)' % (url), log_utils.LOGDEBUG)
            self.__login()
            html = super(self.__class__, self)._http_get(url, data=data, headers=headers, method=method, cache_limit=0)

        self.__get_token(html)
        return html

    def __login(self):
        url = urlparse.urljoin(self.base_url, '/ajax/login.php')
        self.__get_token()
        data = {'username': self.username, 'password': self.password, 'action': 'login', 'token': self.__token, 't': ''}
        html = super(self.__class__, self)._http_get(url, data=data, headers=XHR, cache_limit=0)
        if html != '0': raise Exception('flixanity login failed')

    def __get_bearer(self):
        cj = self._set_cookies(self.base_url, {})
        for cookie in cj:
            if cookie.name == '__utmx':
                return cookie.value
    
    def __get_search_url(self):
        search_url = SEARCH_URL
        html = super(self.__class__, self)._http_get(self.base_url, cache_limit=24)
        for match in re.finditer('<script[^>]+src="([^"]+)', html):
            script = match.group(1)
            if 'flixanity' in script:
                html = super(self.__class__, self)._http_get(script, cache_limit=24)
                match = re.search('=\s*"([^"]*/cautare/[^"]*)', html)
                if match:
                    search_url = match.group(1)
                    match = re.search('u\s*=\s*"([^"]+)', html)
                    if match:
                        search_url = search_url[:search_url.rfind('/') + 1] + match.group(1)
                    break
        return search_url
        
    def __get_token(self, html=''):
        if self.username and self.password and self.__token is None:
            if not html:
                html = super(self.__class__, self)._http_get(self.base_url, cache_limit=8)
                
            match = re.search("var\s+tok\s*=\s*'([^']+)", html)
            if match:
                self.__token = match.group(1)
            else:
                log_utils.log('Unable to locate Flixanity token', log_utils.LOGWARNING)
    
    def __get_s(self):
        return ''.join([random.choice(string.ascii_letters) for _ in xrange(25)])
    
    def __get_rt(self, s, shift=13):
        s2 = ''
        for c in s:
            limit = 122 if c in string.ascii_lowercase else 90
            new_code = ord(c) + shift
            if new_code > limit:
                new_code -= 26
            s2 += chr(new_code)
        return s2

    def __get_sl(self, url):
        u = url.split('/')[-1]
        return hashlib.md5(KEY + u).hexdigest()
