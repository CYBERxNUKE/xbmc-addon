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
import base64
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import QUALITIES
import scraper

BASE_URL = 'http://www.santaseries.com'

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
        return 'SantaSeries'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, cache_limit=.25)
            for link in dom_parser.parse_dom(html, 'li', {'class': 'elemento'}):
                stream_url = ''
                match = re.search('href="[^"]*/load-episode/#([^"]+)', link)
                if match:
                    stream_url = base64.decodestring(match.group(1))
                else:
                    match = re.search('href="([^"]+)', link)
                    if match:
                        stream_url = match.group(1)
                        
                if stream_url.startswith('http'):
                    label = dom_parser.parse_dom(link, 'span', {'class': 'd'})
                    host = urlparse.urlparse(stream_url).hostname
                    quality = scraper_utils.get_quality(video, host, QUALITIES.HIGH)
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': stream_url, 'direct': False}
                    if label: hoster['extra'] = label[0]
                    hosters.append(hoster)
        return hosters

    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]*-season-%s-episode-%s(?!\d)[^"]*)' % (video.season, video.episode)
        return self._default_get_episode_url(show_url, video, episode_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=1)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item'}):
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'tt'})
            match_year = dom_parser.parse_dom(item, 'span', {'class': 'year'})
            if match_url and match_title:
                match_url = match_url[0]
                match_title = match_title[0]
                match_year = match_year[0] if match_year else ''
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)

        return results
