# -*- coding: UTF-8 -*-

'''
    NineScrapers module
'''


import re

import six

from ninescrapers import parse_qs, urlencode, quote_plus, unquote_plus, urljoin
from ninescrapers.modules import cache, cleantitle, client, debrid, log_utils, source_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['kick4ss.com', 'kickasstorrents.id', 'kickasstorrents.bz', 'kkickass.com', 'kkat.net', 'kickasst.net', 'thekat.cc', 'kickasshydra.net', 'kickass.onl', 'thekat.info', 'kickass.cm']
        self.base_link = custom_base
        self.search_link = '/usearch/%s/?field=seeders&sorder=desc'
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        if debrid.status() is False:
            return

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

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            results = []

            query = ' '.join((title, hdlr))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|<|>|\|)', ' ', query)
            query = self.search_link % quote_plus(query)
            r1, self.base_link = client.list_request(self.base_link or self.domains, query)
            if r1:
                r1 = r1.replace('&nbsp;', ' ')
                results.append(r1)

            if 'tvshowtitle' in data:
                hdlr2 = 'season %s' % data['season']
                query2 = ' '.join((title, hdlr2))
                query2 = re.sub('(\\\|/| -|:|;|\*|\?|"|<|>|\|)', ' ', query2)
                query2 = self.search_link % quote_plus(query2)
                #r2, self.base_link = client.list_request(self.base_link or self.domains, query2)
                url2 = urljoin(self.base_link, query2)
                r2 = client.request(url2)
                if r2:
                    r2 = r2.replace('&nbsp;', ' ')
                    r2 = 'pack_sources:\n' + r2
                    results.append(r2)

            for r in results:

                rows = client.parseDOM(r, 'tr', attrs={'id': 'torrent_latest_torrents'})
                if not rows:
                    continue

                for entry in rows:
                    try:
                        is_pack = '%s_%s' % (data['season'], data['episode']) if r.startswith('pack_sources') else None

                        link_name = client.parseDOM(entry, 'a', attrs={'title': 'Torrent magnet link'}, ret='href')[0]
                        link_name = link_name.split('url=')[1]
                        link_name = unquote_plus(link_name)

                        link = link_name.split('&tr=')[0]
                        name = cleantitle.get_title(link.split('&dn=')[1])

                        match = source_utils.is_match(name, title, hdlr, self.aliases) if not is_pack else source_utils.is_season_match(name, title, data['season'], self.aliases)
                        if not match:
                            continue

                        quality, info = source_utils.get_release_quality(name, link)

                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', entry)[-1]
                            dsize, isize = source_utils._size(size)
                        except:
                            dsize, isize = 0.0, ''

                        info.insert(0, isize)

                        info = ' | '.join(info)

                        sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en',
                                        'url': link, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name, 'pack': is_pack})
                    except:
                        pass

            return sources
        except:
            log_utils.log('kickass_exc', 1)
            return sources

    def resolve(self, url):
        return url
