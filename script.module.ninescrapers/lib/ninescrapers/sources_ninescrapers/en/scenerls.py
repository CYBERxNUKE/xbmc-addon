# -*- coding: utf-8 -*-
"""
**Created by Tempest**
"""
# - rewritten for Nine

import re

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import debrid
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['scene-rls.com', 'scene-rls.net']
        self.base_link = custom_base or 'http://scene-rls.net'
        self.search_link = '/?s=%s&submit=Find'
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
            if url is None: return

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
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url)
            #log_utils.log('scenerls url: ' + url)

            r = cfScraper.get(url, timeout=10).text

            posts = client.parseDOM(r, 'div', attrs={'class': 'post'})

            for post in posts:
                try:
                    postTitle = client.parseDOM(post, 'h2', attrs={'class': 'postTitle'})[0]
                    postTitle = client.parseDOM(postTitle, 'a')[0]
                    #log_utils.log('scnrls postTitle: ' + repr(postTitle))
                    if not source_utils.is_match(postTitle, title, hdlr, self.aliases):
                        continue

                    stuff = client.parseDOM(post, 'div', attrs={'class': 'postContent'})[0]
                    items = zip(re.findall('((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', stuff), client.parseDOM(stuff, 'h2', attrs={'style': 'text.*?'}))
                except:
                    pass

                for item in items:
                    try:
                        size = item[0]
                        links = client.parseDOM(item[1], 'a', ret='href')
                    except:
                        pass

                    for url in links:
                        try:
                            if any(x in url for x in ['.rar', '.zip', '.iso']):
                                continue

                            name = url.strip('/').split('/')[-1].replace('.html', '')
                            name = cleantitle.get_title(name)
                            quality, info = source_utils.get_release_quality(name, url)

                            try:
                                dsize, isize = source_utils._size(size)
                            except:
                                dsize, isize = 0.0, ''
                            info.insert(0, isize)

                            info = ' | '.join(info)

                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                        except:
                            pass

            return sources
        except:
            log_utils.log('scenerls exc', 1)
            return sources

    def resolve(self, url):
        return url


