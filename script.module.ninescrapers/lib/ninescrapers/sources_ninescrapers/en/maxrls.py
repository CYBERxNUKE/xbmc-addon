# -*- coding: utf-8 -*-
"""
    **Created by Tempest**
    --updated for Nine 14/7/2020--
"""

import re

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import log_utils
from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import debrid
from ninescrapers.modules import source_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['max-rls.com']
        self.base_link = custom_base or 'https://max-rls.com'
        self.search_link = '/?s=%s&submit=Find'
        self.headers = {'User-Agent': client.agent()}
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:

            if url is None:
                return sources

            if debrid.status() is False:
                return sources

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((title, hdlr))

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('%3A+', '+')
            #log_utils.log('maxrls url: ' + url)

            #r = client.request(url)
            r = cfScraper.get(url, timeout=10).text

            posts = client.parseDOM(r, 'div', attrs={'class': 'post'})

            for post in posts:
                items = []
                try:
                    postTitle = client.parseDOM(post, 'h2', attrs={'class': 'postTitle'})[0]
                    postTitle = client.parseDOM(postTitle, 'a')[0]
                    if not source_utils.is_match(postTitle, title, hdlr, self.aliases):
                        continue

                    stuff = client.parseDOM(post, 'div', attrs={'class': 'postContent'})[0]
                    stuff = client.parseDOM(stuff, 'p', attrs={'dir': 'ltr'})
                    for s in stuff:
                        try: items.append((client.parseDOM(s, 'strong')[0], client.parseDOM(s, 'strong')[1], client.parseDOM(s, 'strong')[2]))
                        except: continue
                except:
                    pass

                for item in items:
                    try:
                        name = item[0]
                        name = client.replaceHTMLCodes(name)
                        name = re.sub(r'<.*?>', '', name)
                        name = cleantitle.get_title(name)
                        size = item[1]
                        links = client.parseDOM(item[2], 'a', ret='href')
                        for url in links:
                            if any(x in url for x in ['.rar', '.zip', '.iso']): continue
                            quality, info = source_utils.get_release_quality(name, url)
                            try:
                                size = re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB|gb|mb))', size, re.DOTALL)[0]
                                dsize, isize = source_utils._size(size)
                            except:
                                dsize, isize = 0.0, ''
                            info.insert(0, isize)
                            info = ' | '.join(info)
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                                'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                    except:
                        pass
            return sources
        except:
            log_utils.log('max_rls Exception', 1)
            return sources

    def resolve(self, url):
        return url
