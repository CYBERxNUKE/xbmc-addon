# -*- coding: utf-8 -*-

'''
    NineScrapers module
'''

import re

from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import debrid
from ninescrapers.modules import client
from ninescrapers.modules import cleantitle
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils
#from ninescrapers import cfScraper

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['torrentdownload.info', 'torrentdownload.unblockit.ch']
        self.base_link = custom_base or 'https://www.torrentdownload.info'
        self.search_link = '/search?q=%s'
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('tdl0 - Exception', 1)
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('tdl1 - Exception', 1)
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
            log_utils.log('tdl2 - Exception', 1)
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if debrid.status() is False:
                return sources

            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((title, hdlr))
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query).lower()

            url = urljoin(self.base_link, self.search_link % quote_plus(query))
            #log_utils.log('tdl - url' + repr(url))

            r = client.r_request(url)
            #r = cfScraper.get(url, timeout=10).text
            r = r.strip()
            posts = client.parseDOM(r, 'table', attrs={'class': 'table2', 'cellspacing': '0'})[1]
            posts = client.parseDOM(posts, 'tr')[1:]
            for post in posts:
                try:
                    links = client.parseDOM(post, 'a', ret='href')[0]
                    links = client.replaceHTMLCodes(links).lstrip('/')
                    hash = links.split('/')[0]
                    name = links.split('/')[1].replace('-', '.').replace('+', '.')
                    name = cleantitle.get_title(name)

                    if not source_utils.is_match(name, title, hdlr, self.aliases):
                        continue

                    url = 'magnet:?xt=urn:btih:{}'.format(hash)

                    quality, info = source_utils.get_release_quality(name)
                    try:
                        size = client.parseDOM(post, 'td', attrs={'class': 'tdnormal'})[1]
                        dsize, isize = source_utils._size(size)
                    except:
                        dsize, isize = 0.0, ''

                    info.insert(0, isize)

                    info = ' | '.join(info)

                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                except:
                    pass

            return sources
        except:
            log_utils.log('tdl3 - Exception', 1)
            return sources

    def resolve(self, url):
        return url
