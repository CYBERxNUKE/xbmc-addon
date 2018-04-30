# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    Copyright (C) 2016 Exodus

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
import urllib
import urlparse
import json

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import tvmaze
from resources.lib.modules import anilist
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['de']
        self.genre_filter = ['animation', 'anime']
        self.domains = ['pure-anime.tv']
        self.base_link = 'http://pure-anime.tv'
        self.search_link = '/wp-json/wp/v2/posts?search=%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'localtvshowtitle': localtvshowtitle, 'aliases': aliases, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            data.update({'season': season, 'episode': episode})
            return urllib.urlencode(data)
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []

        try:
            if not url:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            tvshowtitle = data.get('tvshowtitle')
            localtvshowtitle = data.get('localtvshowtitle')
            aliases = source_utils.aliases_to_array(eval(data['aliases']))
            episode = tvmaze.tvMaze().episodeAbsoluteNumber(data.get('tvdb'), int(data.get('season')), int(data.get('episode')))

            alt_title = anilist.getAlternativTitle(tvshowtitle)
            links = self.__search([alt_title] + aliases, episode)
            if not links and localtvshowtitle != alt_title: links = self.__search([localtvshowtitle] + aliases, episode)
            if not links and tvshowtitle != localtvshowtitle: links = self.__search([tvshowtitle] + aliases, episode)

            for link in links:
                valid, host = source_utils.is_host_valid(link, hostDict)
                if not valid: continue

                sources.append({'source': host, 'quality': 'SD', 'language': 'de', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources

    def resolve(self, url):
        return url

    def __search(self, titles, episode):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.query(titles[0]) + ' ' + str(episode))
            query = urlparse.urljoin(self.base_link, query)

            t = [cleantitle.get(i) + str(episode) for i in set(titles) if i]

            r = client.request(query)
            r = r.split('</style>')[-1].strip()
            r = json.loads(r)

            r = [(i.get('title', {}).get('rendered'), i.get('content', {}).get('rendered')) for i in r]
            r = [(re.sub('ger (?:sub|dub)', '', i[0], flags=re.I).strip(), i[1]) for i in r if i[0] and i[1]]
            r = [(i[0], re.findall('(.+?) (\d*)$', i[0]), i[1]) for i in r]
            r = [(i[0] if not i[1] else i[1][0][0] + ' ' + str(int(i[1][0][1])), i[2]) for i in r]
            r = [dom_parser.parse_dom(i[1], 'div') for i in r if cleantitle.get(i[0]) in t]
            r = [[x.attrs['href'] for x in dom_parser.parse_dom(i, 'a', req='href')] + [x.attrs['src'] for x in dom_parser.parse_dom(i, 'iframe', req='src')] for i in r]
            return r[0]
        except:
            return
