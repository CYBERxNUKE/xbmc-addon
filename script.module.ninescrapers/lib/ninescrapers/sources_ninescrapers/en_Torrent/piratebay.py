# -*- coding: utf-8 -*-

'''
    NineScrapers module
'''


import re

from ninescrapers import parse_qs, urljoin, urlencode, quote, unquote_plus
from ninescrapers.modules import cache
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
        self.domains = ['tpb.party', 'pirateproxy.live', 'thepiratebay10.org', 'thehiddenbay.com', 'thepiratebay.zone', 'proxybay.store', 'thepiratebay.party',
                        'piratebay.party', 'piratebay.live', 'piratebayproxy.live']
        self.base_link = custom_base# or 'piratebayproxy.live'
        # self.search_link = '/s/?q=%s&page=1&&video=on&orderby=99' #-page flip does not work
        self.search_link = '/search/%s/1/99/200' #-direct link can flip pages
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

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.get_query(title)

            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

            query = ' '.join((title, hdlr))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

            query = self.search_link % quote(query)
            r, self.base_link = client.list_request(self.base_link or self.domains, query)
            r = r.replace('&nbsp;', ' ')

            results = client.parseDOM(r, 'table', attrs={'id': 'searchResult'})

            if not 'tvshowtitle' in data:
                try:
                    url2 = urljoin(self.base_link, query.replace('/1/', '/2/'))
                    html2 = client.request(url2)
                    html2 = html2.replace('&nbsp;', ' ')
                    results += client.parseDOM(html2, 'table', attrs={'id': 'searchResult'})
                except:
                    pass

            results = ''.join(results)

            rows = re.findall('<tr(.+?)</tr>', results, re.DOTALL)

            if rows:
                for entry in rows:
                    try:
                        try:
                            url = 'magnet:%s' % (re.findall('a href="magnet:(.+?)"', entry, re.DOTALL)[0])
                            url = str(client.replaceHTMLCodes(url).split('&tr')[0])
                        except:
                            continue

                        name = client.parseDOM(entry, 'td')[1]
                        name = client.parseDOM(name, 'a')[0]
                        name = cleantitle.get_title(name)

                        if not source_utils.is_match(name, title, hdlr, self.aliases):
                            continue

                        quality, info = source_utils.get_release_quality(name, url)

                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', entry)[-1]
                            dsize, isize = source_utils._size(size)
                        except:
                            dsize, isize = 0.0, ''
                        info.insert(0, isize)

                        info = ' | '.join(info)

                        sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                        'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                    except:
                        log_utils.log('tpb_exc', 1)
                        continue

            if 'tvshowtitle' in data:
                for source in self.pack_sources(title, data['season'], data['episode']):
                    sources.append(source)

            return sources

        except:
            log_utils.log('tpb_exc', 1)
            return sources


    def pack_sources(self, title, season, episode):
        _sources = []
        try:
            query = '%s season %s' % (title, season)
            query = self.search_link % quote(query)
            r, self.base_link = client.list_request(self.base_link or self.domains, query)
            r = r.replace('&nbsp;', ' ')

            results = client.parseDOM(r, 'table', attrs={'id': 'searchResult'})
            if not results:
                return _sources
            results = ''.join(results)
            rows = re.findall('<tr(.+?)</tr>', results, re.DOTALL)

            if rows:
                for entry in rows:
                    try:
                        try:
                            url = 'magnet:%s' % (re.findall('a href="magnet:(.+?)"', entry, re.DOTALL)[0])
                            url = str(client.replaceHTMLCodes(url).split('&tr')[0])
                        except:
                            continue

                        name = client.parseDOM(entry, 'td')[1]
                        name = client.parseDOM(name, 'a')[0]
                        name = cleantitle.get_title(name)

                        if not source_utils.is_season_match(name, title, season, self.aliases):
                            continue

                        pack = '%s_%s' % (season, episode)

                        quality, info = source_utils.get_release_quality(name, url)

                        try:
                            size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', entry)[-1]
                            dsize, isize = source_utils._size(size)
                        except:
                            dsize, isize = 0.0, ''
                        info.insert(0, isize)

                        info = ' | '.join(info)

                        _sources.append({'source': 'torrent', 'quality': quality, 'language': 'en', 'url': url,
                                        'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name, 'pack': pack})
                    except:
                        log_utils.log('tpb_pack_exc', 1)
                        continue

            return _sources

        except:
            log_utils.log('tpb_pack_exc', 1)
            return _sources


    def resolve(self, url):
        return url