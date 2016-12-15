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
import urlparse
import re
import scraper
import urllib
import base64
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'http://www.pelispedia.tv'
PK_URL = '/Pe_Player_Html5/pk/pk_2/plugins/protected.php'
GK_URL = '/gkphp_flv/plugins/gkpluginsphp.php'
DEL_LIST = ['sub', 'id']
XHR = {'X-Requested-With': 'XMLHttpRequest'}
MOVIE_SEARCH_URL = 'aHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vY3VzdG9tc2VhcmNoL3YxZWxlbWVudD9rZXk9QUl6YVN5Q1ZBWGlVelJZc01MMVB2NlJ3U0cxZ3VubU1pa1R6UXFZJnJzej1maWx0ZXJlZF9jc2UmbnVtPTEwJmhsPWVuJmN4PTAxMzA0MzU4NDUzMDg1NzU4NzM4MTpkcGR2Y3FlbGt3dyZnb29nbGVob3N0PXd3dy5nb29nbGUuY29tJnE9JXM='

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'PelisPedia'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'div', {'class': 'repro'})
            if fragment:
                iframe_url = dom_parser.parse_dom(fragment[0], 'iframe', ret='src')
                if iframe_url:
                    html = self._http_get(iframe_url[0], cache_limit=.5)
                    fragment = dom_parser.parse_dom(html, 'div', {'id': 'botones'})
                    if fragment:
                        for media_url in dom_parser.parse_dom(fragment[0], 'a', ret='href'):
                            media_url = media_url.replace(' ', '')
                            if any([media_url for u in (self.base_url, 'pelispedia.biz', 'pelispedia.vip') if u in media_url]):
                                headers = {'Referer': iframe_url[0]}
                                html = self._http_get(media_url, headers=headers, cache_limit=.5)
                                hosters += self.__get_page_links(html)
                                hosters += self.__get_pk_links(html)
                                hosters += self.__get_gk_links(html, url)
                            else:
                                host = urlparse.urlparse(media_url).hostname
                                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': QUALITIES.HD720, 'views': None, 'rating': None, 'url': media_url, 'direct': False}
                                hosters.append(hoster)
            
        return hosters

    def __get_page_links(self, html):
        hosters = []
        sources = self._parse_sources_list(html)
        for source in sources:
            quality = sources[source]['quality']
            hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': quality, 'host': self._get_direct_hostname(source), 'rating': None, 'views': None, 'direct': True}
            hosters.append(hoster)
        return hosters

    def __get_pk_links(self, html):
        hosters = []
        match = re.search('var\s+parametros\s*=\s*"([^"]+)', html)
        if match:
            params = urlparse.parse_qs(urlparse.urlparse(match.group(1)).query)
            if 'pic' in params:
                data = {'sou': 'pic', 'fv': '11', 'url': params['pic'][0]}
                url = urlparse.urljoin(self.base_url, PK_URL)
                html = self._http_get(url, headers=XHR, data=data, cache_limit=.5)
                js_data = scraper_utils.parse_json(html, url)
                for item in js_data:
                    if 'url' in item and item['url']:
                        if 'width' in item and item['width']:
                            quality = scraper_utils.width_get_quality(item['width'])
                        elif 'height' in item and item['height']:
                            quality = scraper_utils.height_get_quality(item['height'])
                        else:
                            quality = QUALITIES.HD720
                        stream_url = item['url'] + '|User-Agent=%s' % (scraper_utils.get_ua())
                        hoster = {'multi-part': False, 'url': stream_url, 'class': self, 'quality': quality, 'host': self._get_direct_hostname(item['url']), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
        return hosters
    
    def __get_gk_links(self, html, url):
        hosters = []
        for match in re.finditer('gkpluginsphp.*?link\s*:\s*"([^"]+)', html):
            data = {'link': match.group(1)}
            headers = XHR
            headers['Referer'] = url
            gk_url = urlparse.urljoin(self.base_url, GK_URL)
            html = self._http_get(gk_url, data=data, headers=headers, cache_limit=.5)
            js_result = scraper_utils.parse_json(html, gk_url)
            if 'link' in js_result and 'func' not in js_result:
                if isinstance(js_result['link'], list):
                    sources = dict((link['link'], scraper_utils.height_get_quality(link.get('label', 700))) for link in js_result['link'])
                else:
                    sources = {js_result['link']: QUALITIES.HD720}
                
                for source in sources:
                    if source:
                        hoster = {'multi-part': False, 'url': source, 'class': self, 'quality': sources[source], 'host': self._get_direct_hostname(source), 'rating': None, 'views': None, 'direct': True}
                        hosters.append(hoster)
        return hosters
        
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-season-%s-episode-%s[^\d"]*)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+-season-\d+-episode-\d+[^"]*).*?<span[^>]*class="[^"]*ml5[^"]*">(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        if video_type == VIDEO_TYPES.TVSHOW:
            results = self.__tv_search(title, year)
        else:
            results = self.__movie_search(title, year)
        return results

    def __tv_search(self, title, year):
        results = []
        if title:
            url = '/series/letra/%s/' % (title[0])
            results = self.__proc_results(url, title, year)
                        
        return results

    def __movie_search(self, title, year):
        results = []
        search_url = base64.decodestring(MOVIE_SEARCH_URL) % (urllib.quote_plus(title))
        html = self._http_get(search_url, cache_limit=1)
        js_data = scraper_utils.parse_json(html)
        if 'results' in js_data:
            norm_title = scraper_utils.normalize_title(title)
            for item in js_data['results']:
                match_url = urllib.unquote(item['url'])
                if '/pelicula/' not in match_url: continue
                match_title_year = item['titleNoFormatting']
                match_title_year = re.sub('^Ver\s+', '', match_title_year)
                match = re.search('(.*?)(?:\s+\(?(\d{4})\)?)', match_title_year)
                if match:
                    match_title, match_year = match.groups()
                else:
                    match_title = match_title_year
                    match_year = ''
                
                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
        
        if not results and title and year:
            url = '/movies/all/?year=%s&gender=&letra=%s' % (year, title[0])
            results = self.__proc_results(url, title, year)
            
        return results

    def __proc_results(self, url, title, year):
        results = []
        url = urlparse.urljoin(self.base_url, url)
        html = self._http_get(url, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        for item in dom_parser.parse_dom(html, 'li', {'class': '[^"]*bpM12[^"]*'}):
            title_frag = dom_parser.parse_dom(item, 'h2')
            year_frag = dom_parser.parse_dom(item, 'div', {'class': '[^"]*sectionDetail[^"]*'})
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            if title_frag and match_url:
                match_url = match_url[0]
                match = re.search('(.*?)<br>', title_frag[0])
                if match:
                    match_title = match.group(1)
                else:
                    match_title = title_frag[0]
                    
                match_year = ''
                if year_frag:
                    match = re.search('(\d{4})', year_frag[0])
                    if match:
                        match_year = match.group(1)

                if norm_title in scraper_utils.normalize_title(match_title) and (not year or not match_year or year == match_year):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        
        return results
