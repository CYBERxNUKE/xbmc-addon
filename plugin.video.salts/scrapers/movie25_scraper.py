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
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper


QUALITY_MAP = {'DVD': QUALITIES.HIGH, 'TS': QUALITIES.MEDIUM, 'CAM': QUALITIES.LOW}
BASE_URL = 'http://tinklepad.is'

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
        return 'movie25'

    def resolve_link(self, link):
        if self.base_url in link:
            url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=0)
            match = re.search('''href='([^']*)'\s+value="Click Here to Play"''', html, re.DOTALL | re.I)
            if match:
                return match.group(1)
            else:
                iframe_url = dom_parser.parse_dom(html, 'IFRAME', {'id': 'showvideo'}, 'src')
                if iframe_url:
                    return iframe_url[0]
                else:
                    return link
        else:
                return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            quality = None
            match = re.search('Links\s+-\s+Quality\s*([^<]*)</h1>', html, re.DOTALL | re.I)
            if match:
                quality = QUALITY_MAP.get(match.group(1).strip().upper())

            seen_links = {}
            for item in dom_parser.parse_dom(html, 'li', {'id': 'playing_button'}):
                stream_url = dom_parser.parse_dom(item, 'a', ret='href')
                if stream_url:
                    stream_url = stream_url[0]
                    match = re.search('url=([^&"]+)', stream_url)
                    if match:
                        stream_url = base64.b64decode(match.group(1))
                    else:
                        match = re.search('stream\.php\?([^"]+)', stream_url)
                        if match:
                            stream_url = base64.b64decode(match.group(1))
                            i = stream_url.rfind('&&')
                            if i > -1:
                                stream_url = stream_url[i + 2:]
                        
                    if stream_url in seen_links: continue
                    seen_links[stream_url] = True
                    host = urlparse.urlparse(stream_url).hostname
                    hoster = {'multi-part': False, 'host': host, 'class': self, 'url': stream_url, 'quality': scraper_utils.get_quality(video, host, quality), 'rating': None, 'views': None, 'direct': False}
                    hosters.append(hoster)
        return hosters

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        search_url = urlparse.urljoin(self.base_url, '/search.php')
        html = self._http_get(search_url, params={'q': title}, cache_limit=4)
        for item in dom_parser.parse_dom(html, 'div', {'class': 'movie_about'}):
            match_url = dom_parser.parse_dom(item, 'a', ret='href')
            match_title_year = dom_parser.parse_dom(item, 'a')
            if match_url and match_title_year:
                match_url = match_url[0]
                match_title, match_year = scraper_utils.extra_year(match_title_year[0])
                if not year or not match_year or year == match_year:
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                    results.append(result)
        return results
