# -*- coding: utf-8 -*-

'''
    NineScrapers module
'''


import re

from ninescrapers import parse_qs, urljoin, urlencode, quote, quote_plus
from ninescrapers.modules import debrid
from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['torrentdownloads.pro']
        self.base_link = custom_base or 'https://www.torrentdownloads.pro'
        self.search_link = '/rss.xml?new=1&type=search&cid={0}&search={1}'
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

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            #title = cleantitle.get_query(title)
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((title, hdlr))
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            if 'tvshowtitle' in data:
                url = urljoin(self.base_link, self.search_link.format('8', quote(query)))
            else:
                url = urljoin(self.base_link, self.search_link.format('4', quote(query)))
            # log_utils.log('tdls url: ' + url)

            headers = {'User-Agent': client.agent()}
            _html = client.request(url, headers=headers)
            items = re.findall(r'<item>(.+?)</item>', _html, re.DOTALL)

            if items:
                for r in items:
                    try:
                        size = re.search(r'<size>([\d]+)</size>', r).groups()[0]
                        _hash = re.search(r'<info_hash>([a-zA-Z0-9]+)</info_hash>', r).groups()[0]
                        name = re.search(r'<title>(.+?)</title>', r).groups()[0]
                        name = cleantitle.get_title(name)
                        url = 'magnet:?xt=urn:btih:%s' % _hash.upper()

                        if not source_utils.is_match(name, title, hdlr, self.aliases):
                            continue

                        quality, info = source_utils.get_release_quality(name)

                        try:
                            dsize = float(size) / 1073741824
                            isize = '%.2f GB' % round(dsize, 2)
                        except:
                            dsize, isize = 0.0, ''
                        info.insert(0, isize)

                        info = ' | '.join(info)

                        sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                        'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                    except:
                        log_utils.log('tdls0 - Exception', 1)
                        pass

            if 'tvshowtitle' in data:
                for source in self.pack_sources(title, data['season'], data['episode']):
                    sources.append(source)

            return sources
        except:
            log_utils.log('tdls - Exception', 1)
            return sources

    def pack_sources(self, title, season, episode):
        _sources = []
        try:
            query = '%s season %s' % (title, season)
            url = urljoin(self.base_link, self.search_link.format('8', quote(query)))
            headers = {'User-Agent': client.agent()}
            _html = client.request(url, headers=headers)
            items = re.findall(r'<item>(.+?)</item>', _html, re.DOTALL)

            if items:
                for r in items:
                    try:
                        size = re.search(r'<size>([\d]+)</size>', r).groups()[0]
                        _hash = re.search(r'<info_hash>([a-zA-Z0-9]+)</info_hash>', r).groups()[0]
                        name = re.search(r'<title>(.+?)</title>', r).groups()[0]
                        name = cleantitle.get_title(name)
                        url = 'magnet:?xt=urn:btih:%s' % _hash.upper()

                        if not source_utils.is_season_match(name, title, season, self.aliases):
                            continue

                        pack = '%s_%s' % (season, episode)

                        quality, info = source_utils.get_release_quality(name)

                        try:
                            dsize = float(size) / 1073741824
                            isize = '%.2f GB' % round(dsize, 2)
                        except:
                            dsize, isize = 0.0, ''
                        info.insert(0, isize)

                        info = ' | '.join(info)

                        _sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                         'direct': False, 'debridonly': True, 'size': dsize, 'name': name, 'pack': pack})
                    except:
                        log_utils.log('tdls pack - Exception', 1)
                        pass
            return _sources

        except:
            log_utils.log('tdls pack_exc', 1)
            return _sources

    def resolve(self, url):
        return url
