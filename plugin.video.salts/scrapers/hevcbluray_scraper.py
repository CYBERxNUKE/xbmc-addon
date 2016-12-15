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
import scraper
import urlparse
import re
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES

BASE_URL = 'https://hevcbluray.com'
QUALITY_MAP = {'HD 720P': QUALITIES.HD720, 'HD 1080P': QUALITIES.HD1080, '1080P BLURAY': QUALITIES.HD1080}

class Scraper(scraper.Scraper):
    base_url = BASE_URL

    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE])

    @classmethod
    def get_name(cls):
        return 'HEVCBluRay'

    def get_sources(self, video):
        source_url = self.get_url(video)
        sources = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            is_3d = False
            page_quality = QUALITIES.HD720
            title = dom_parser.parse_dom(html, 'title')
            if title:
                title = title[0]
                match = re.search('(\d{3,})p', title)
                if match:
                    page_quality = scraper_utils.height_get_quality(match.group(1))
                
                is_3d = True if re.search('\s+3D\s+', title) else False
            
            fragments = dom_parser.parse_dom(html, 'div', {'class': 'txt-block'}) + dom_parser.parse_dom(html, 'li', {'class': 'elemento'})
            for fragment in fragments:
                for match in re.finditer('href="([^"]+)', fragment):
                    stream_url = match.group(1)
                    host = urlparse.urlparse(stream_url).hostname
                    q_str = dom_parser.parse_dom(fragment, 'span', {'class': 'd'})
                    q_str = q_str[0].upper() if q_str else ''
                    base_quality = QUALITY_MAP.get(q_str, page_quality)
                    quality = scraper_utils.get_quality(video, host, base_quality)
                    source = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': False}
                    source['format'] = 'x265'
                    source['3D'] = is_3d
                    sources.append(source)
                    
        return sources

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        html = self._http_get(self.base_url, params={'s': title}, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'item'}):
            match = re.search('href="([^"]+)', item)
            match_title = dom_parser.parse_dom(item, 'span', {'class': 'tt'})
            year_frag = dom_parser.parse_dom(item, 'span', {'class': 'year'})
            if match and match_title:
                url = match.group(1)
                match_title = match_title[0]
                if re.search('\d+\s*x\s*\d+', match_title): continue  # exclude episodes
                match_title, match_year = scraper_utils.extra_year(match_title)
                if not match_year and year_frag:
                    match_year = year_frag[0]

                match = re.search('(.*?)\s+\d{3,}p', match_title)
                if match:
                    match_title = match.group(1)
                
                extra = dom_parser.parse_dom(item, 'span', {'class': 'calidad2'})
                if extra:
                    match_title += ' [%s]' % (extra[0])
                    
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(url)}
                    results.append(result)

        return results
