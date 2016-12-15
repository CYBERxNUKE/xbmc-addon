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
import kodi
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
import dom_parser
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://putlocker9.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE, VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'Putlocker'

    def resolve_link(self, link):
        if not link.startswith('http'):
            stream_url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(stream_url, cache_limit=0)
            iframe_url = dom_parser.parse_dom(html, 'iframe', ret='src')
            if iframe_url:
                return iframe_url[0]
        else:
            return link
        
    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            headers = {'Referer': ''}
            html = self._http_get(page_url, headers=headers, cache_limit=.5)
            page_links = []
            for fragment in dom_parser.parse_dom(html, 'script', {'type': 'text/rocketscript'}):
                for iframe_url in dom_parser.parse_dom(fragment, 'iframe', ret='src'):
                    iframe_url = iframe_url.replace('\\"', '')
                    if 'youtube' not in iframe_url:
                        host = urlparse.urlparse(iframe_url).hostname
                        page_links.append((iframe_url, 'embedded', host))
                
            page_links += re.findall('<a[^>]+href="([^"]+)[^>]+>(Version \d+)</a>([^<]+)', html)
            
            for stream_url, version, host in page_links:
                if not stream_url.startswith('http'):
                    url = source_url + stream_url
                    host = host.replace('&nbsp;', '')
                else:
                    url = stream_url
                    host = urlparse.urlparse(stream_url).hostname
                
                base_quality = QUALITIES.HD720 if version == 'embedded' else QUALITIES.HIGH
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, base_quality), 'views': None, 'rating': None, 'url': url, 'direct': False}
                hoster['version'] = '(%s)' % (version)
                hosters.append(hoster)

        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        headers = {'Referer': self.base_url}
        params = {'s': title, 'submit': 'Search Now!'}
        html = self._http_get(self.base_url, params=params, headers=headers, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'aaa_item'}):
            match_title_year = dom_parser.parse_dom(item, 'a', ret='title')
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            if match_title_year and match_url:
                match_url = match_url[0]
                match_title, match_year = scraper_utils.extra_year(match_title_year[0])
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+season-%s-episode-%s-[^"]+)' % (video.season, video.episode)
        title_pattern = 'href="(?P<url>[^"]+season-\d+-episode-\d+-[^"]+).*?\s+-\s+(?P<title>.*?)</td>'
        headers = {'Referer': urlparse.urljoin(self.base_url, show_url)}
        return self._default_get_episode_url(show_url, video, episode_pattern, title_pattern, headers=headers)
