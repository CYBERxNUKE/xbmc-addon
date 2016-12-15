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
import dom_parser
import log_utils  # @UnusedImport
from salts_lib import scraper_utils
from salts_lib import jsunpack
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import QUALITIES
from salts_lib.constants import VIDEO_TYPES
import scraper

BASE_URL = 'http://quikrmovies.to'
DIRECT_HOSTS = ['quikr.stream', 'openload.stream', 'qvideos.stream']

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
        return 'Quikr'

    def get_sources(self, video):
        hosters = []
        source_url = self.get_url(video)
        if source_url and source_url != FORCE_NO_MATCH:
            url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(url, cache_limit=.5)
            page_quality = QUALITIES.HD720 if video.video_type == VIDEO_TYPES.MOVIE else QUALITIES.HIGH
            for fragment in dom_parser.parse_dom(html, 'div', {'class': '[^"]*embed-responsive[^"]*'}):
                iframe_url = dom_parser.parse_dom(fragment, 'iframe', ret='data-src')
                if iframe_url:
                    iframe_url = iframe_url[0]
                    iframe_host = urlparse.urlparse(iframe_url).hostname
                    if iframe_host in DIRECT_HOSTS:
                        sources = self.__parse_streams(iframe_url, url)
                    else:
                        sources = {iframe_url: {'quality': scraper_utils.get_quality(video, iframe_host, page_quality), 'direct': False}}
                
                for source in sources:
                    quality = sources[source]['quality']
                    direct = sources[source]['direct']
                    if direct:
                        host = self._get_direct_hostname(source)
                        stream_url = source + '|User-Agent=%s' % (scraper_utils.get_ua())
                    else:
                        host = urlparse.urlparse(source).hostname
                        stream_url = source
                    
                    hoster = {'multi-part': False, 'url': stream_url, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'direct': direct}
                    hosters.append(hoster)

        return hosters

    def __parse_streams(self, iframe_url, page_url):
        headers = {'Referer': page_url}
        html = self._http_get(iframe_url, headers=headers, cache_limit=.5)
        if jsunpack.detect(html):
            html = jsunpack.unpack(html)
        
        return self._parse_sources_list(html)
    
    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        if video_type == VIDEO_TYPES.TVSHOW:
            url = '/tvshows-release-year/%s/'
        else:
            url = '/release-year/%s/'

        if year:
            url = urlparse.urljoin(self.base_url, url % (year))
            html = self._http_get(url, cache_limit=48)
            norm_title = scraper_utils.normalize_title(title)
            for item in dom_parser.parse_dom(html, 'div', {'class': 'primary_movie_box'}):
                match_url = dom_parser.parse_dom(item, 'a', ret='href')
                match_title = dom_parser.parse_dom(item, 'h2', {'class': 'primary_movie_box_title'})
                match_year = dom_parser.parse_dom(item, 'div', {'class': 'primary_movie_box_year'})
                if match_url and match_title:
                    match_url = match_url[0]
                    match_title = match_title[0]
                    match_year = match_year[0] if match_year else ''
                    if norm_title in scraper_utils.normalize_title(match_title) and (not match_year or not year or year == match_year):
                        result = {'url': scraper_utils.pathify_url(match_url), 'title': scraper_utils.cleanse_title(match_title), 'year': match_year}
                        results.append(result)
        return results
    
    def _get_episode_url(self, show_url, video):
        episode_pattern = 'href="([^"]+-s0*%se0*%s(?!\d)[^"]*)' % (video.season, video.episode)
        result = self._default_get_episode_url(show_url, video, episode_pattern)
        if result: return result

        url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(url, cache_limit=2)
        fragment = dom_parser.parse_dom(html, 'ul', {'class': 'episode_list'})
        if fragment:
            ep_urls = dom_parser.parse_dom(fragment[0], 'a', ret='href')
            ep_dates = dom_parser.parse_dom(fragment[0], 'span', {'class': 'episode_air_d'})
            ep_titles = dom_parser.parse_dom(fragment[0], 'span', {'class': 'episode_name'})
            force_title = scraper_utils.force_title(video)
            if not force_title and kodi.get_setting('airdate-fallback') == 'true' and video.ep_airdate:
                for ep_url, ep_date in zip(ep_urls, ep_dates):
                    log_utils.log('Quikr Ep Airdate Matching: %s - %s - %s' % (ep_url, ep_date, video.ep_airdate), log_utils.LOGDEBUG)
                    if video.ep_airdate == scraper_utils.to_datetime(ep_date, '%Y-%m-%d').date():
                        return scraper_utils.pathify_url(ep_url)
        
            if force_title or kodi.get_setting('title-fallback') == 'true':
                norm_title = scraper_utils.normalize_title(video.ep_title)
                for ep_url, ep_title in zip(ep_urls, ep_titles):
                    ep_title = re.sub('<span>.*?</span>\s*', '', ep_title)
                    log_utils.log('Quikr Ep Title Matching: %s - %s - %s' % (ep_url, norm_title, video.ep_title), log_utils.LOGDEBUG)
                    if norm_title == scraper_utils.normalize_title(ep_title):
                        return scraper_utils.pathify_url(ep_url)
