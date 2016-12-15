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
import re
import urlparse
import random
import urllib
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://dizilab.com'
AJAX_URL = '/request/php/'
STREAM_URL = '%s%s|User-Agent=%s&Referer=%s'
ICONS = {'icon-tr': 'Turkish Subtitles', 'icon-en': 'English Subtitles', 'icon-orj': ''}
DEFAULT_SUB = 'Turkish Subtitles'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'Dizilab'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.5)
            videos = re.findall('''onclick\s*=\s*"loadVideo\('([^']+)''', html)
            subs = self.__get_subs(html)
            for v_id, icon in map(None, videos, subs):
                ajax_url = urlparse.urljoin(self.base_url, AJAX_URL)
                data = {'vid': v_id, 'tip': 1, 'type': 'loadVideo'}
                headers = {'Referer': page_url}
                headers.update(XHR)
                html = self._http_get(ajax_url, data=data, headers=headers, cache_limit=.5)
                sub = ICONS.get(icon, DEFAULT_SUB)
                hosters += self.__get_cloud_links(html, page_url, sub)
                hosters += self.__get_embedded_links(html, sub)
                hosters += self.__get_iframe_links(html, sub)
                hosters += self.__get_json_links(html, sub)
                if not kodi.get_setting('scraper_url'): break

        return hosters

    def __get_subs(self, html):
        subs = []
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'language alternative'})
        if fragment:
            subs = dom_parser.parse_dom(fragment[0], 'span', {'class': 'icon-[^"]*'}, ret='class')
        return subs
    
    def __get_json_links(self, html, sub):
        hosters = []
        js_data = scraper_utils.parse_json(html)
        if 'sources' in js_data:
            for source in js_data['sources']:
                if 'file' in source:
                    stream_url = source['file']
                    host = self._get_direct_hostname(stream_url)
                    if host == 'gvideo':
                        quality = scraper_utils.gv_get_quality(stream_url)
                    elif 'label' in source:
                        quality = scraper_utils.height_get_quality(source['label'])
                    else:
                        quality = QUALITIES.HIGH
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                    hoster['subs'] = sub
                    hosters.append(hoster)
        return hosters
    
    def __get_iframe_links(self, html, sub):
        hosters = []
        html = html.replace('\\"', '"').replace('\\/', '/')
        iframe_urls = dom_parser.parse_dom(html, 'iframe', {'id': 'episode_player'}, ret='src')
        if iframe_urls:
            stream_url = iframe_urls[0]
            host = urlparse.urlparse(stream_url).hostname
            quality = QUALITIES.HD720
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
            hoster['subs'] = sub
            hosters.append(hoster)
        return hosters
    
    def __get_embedded_links(self, html, sub):
        hosters = []
        html = html.replace('\\"', '"').replace('\\/', '/')
        sources = self._parse_sources_list(html)
        for source in sources:
            host = self._get_direct_hostname(source)
            quality = sources[source]['quality']
            direct = sources[source]['direct']
            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
            hoster['subs'] = sub
            hosters.append(hoster)
        return hosters
    
    def __get_cloud_links(self, html, page_url, sub):
        hosters = []
        html = html.replace('\\"', '"').replace('\\/', '/')
        match = re.search("dizi_kapak_getir\('([^']+)", html)
        if match:
            ep_id = match.group(1)
            for script_url in dom_parser.parse_dom(html, 'script', {'data-cfasync': 'false'}, ret='src'):
                html = self._http_get(script_url, cache_limit=24)
                match1 = re.search("var\s+kapak_url\s*=\s*'([^']+)", html)
                match2 = re.search("var\s+aCtkp\s*=\s*'([^']+)", html)
                if match1 and match2:
                    link_url = '%s?fileid=%s&access_token=%s' % (match1.group(1), ep_id, match2.group(1))
                    headers = {'Referer': page_url}
                    html = self._http_get(link_url, headers=headers, cache_limit=.5)
                    js_data = scraper_utils.parse_json(html, link_url)
                    for variant in js_data.get('variants', {}):
                        stream_host = random.choice(variant.get('hosts', []))
                        if stream_host:
                            stream_url = STREAM_URL % (stream_host, variant['path'], scraper_utils.get_ua(), urllib.quote(page_url))
                            if not stream_url.startswith('http'):
                                stream_url = 'http://' + stream_url
                            host = self._get_direct_hostname(stream_url)
                            if 'width' in variant:
                                quality = scraper_utils.width_get_quality(variant['width'])
                            elif 'height' in variant:
                                quality = scraper_utils.height_get_quality(variant['height'])
                            else:
                                quality = QUALITIES.HIGH
                            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': True}
                            hoster['subs'] = sub
                            hosters.append(hoster)
        return hosters
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'class="episode"\s+href="([^"]+/sezon-%s/bolum-%s)"' % (video.season, video.episode)
        title_pattern = 'class="episode-name"\s+href="(?P<url>[^"]+)">\s*(?P<title>[^<]+)'
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        url = urlparse.urljoin(self.base_url, AJAX_URL)
        data = {'type': 'getDizi'}
        html = self._http_get(url, data=data, headers=XHR, cache_limit=48)
        norm_title = scraper_utils.normalize_title(title)
        match_year = ''
        js_data = scraper_utils.parse_json(html, url)
        for item in js_data.get('data', []):
            match_title = item.get('adi', '')
            if 'url' in item and norm_title in scraper_utils.normalize_title(match_title):
                result = {'url': scraper_utils.pathify_url(item['url']), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                results.append(result)

        return results
