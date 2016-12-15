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
import log_utils
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://projectfreetv.at'

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
        return 'pftv'

    def resolve_link(self, link):
        if not link.startswith('http'):
            url = urlparse.urljoin(self.base_url, link)
            html = self._http_get(url, cache_limit=.5)
            match = re.search('href="([^"]+).*?value="Continue to video"', html)
            if match:
                url = urlparse.urljoin(self.base_url, match.group(1))
                html = self._http_get(url, cache_limit=.5)
                redirect = dom_parser.parse_dom(html, 'meta', {'http-equiv': 'refresh'}, ret='content')
                if redirect:
                    match = re.search('url=([^"]+)', redirect[0])
                    if match: return match.group(1)

        return link

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)

            for match in re.finditer('<td>\s*<a\s+href="([^"]+)(?:[^>]+>){2}\s*(?:&nbsp;)*\s*([^<]+)', html):
                url, host = match.groups()
                hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': scraper_utils.get_quality(video, host, QUALITIES.HIGH), 'views': None, 'rating': None, 'url': scraper_utils.pathify_url(url), 'direct': False}
                hosters.append(hoster)

        return hosters

    def _get_episode_url(self, show_url, video):
        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=8)
        season_pattern = 'href="([^"]+season-%s/)' % (video.season)
        match = re.search(season_pattern, html)
        if match:
            season_url = match.group(1)
            episode_pattern = 'href="([^"]+season-%s-episode-%s/)' % (video.season, video.episode)
            airdate_pattern = '{day} {short_month} {year}\s*<a\s+href="([^"]+)'
            return self._default_get_episode_url(season_url, video, episode_pattern, airdate_pattern=airdate_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        norm_title = scraper_utils.normalize_title(title)
        url = urlparse.urljoin(self.base_url, '/watch-series/')
        headers = {'Referer': self.base_url}
        html = self._http_get(url, headers=headers, cache_limit=8)
        for item in dom_parser.parse_dom(html, 'li'):
            for match in re.finditer('title="([^"]+)[^>]+href="([^"]+)', item):
                match_title, match_url = match.groups()
                if norm_title in scraper_utils.normalize_title(match_title):
                    result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': ''}
                    results.append(result)

        return results
