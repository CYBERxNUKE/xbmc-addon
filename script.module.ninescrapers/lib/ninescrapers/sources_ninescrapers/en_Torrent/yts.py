# -*- coding: UTF-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# @tantrumdev wrote this file.  As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. - Muad'Dib
# ----------------------------------------------------------------------------
#######################################################################


import re

from ninescrapers import parse_qs, urljoin, urlencode, quote, unquote_plus
from ninescrapers.modules import cleantitle, client, debrid, source_utils, log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yts.mx', 'yts.proxyninja.org']
        self.base_link = custom_base# or 'https://yts.mx'
        self.search_link = '/browse-movies/%s/all/all/0/latest/0/all'
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        if debrid.status() is False:
            return

        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:

            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = cleantitle.get_query(data['title'])
            year = data['year']
            imdb = data['imdb']

            _headers = {'User-Agent': client.agent()}

            query = ' '.join((title, year))
            query = self.search_link % quote(query)

            r, self.base_link = client.list_request(self.base_link or self.domains, query)
            try:
                results = client.parseDOM(r, 'div', attrs={'class': 'row'})[2]
            except Exception:
                return sources

            items = re.findall('class="browse-movie-bottom">(.+?)</div>\s</div>', results, re.DOTALL)
            if items is None:
                return sources

            for entry in items:
                try:
                    try:
                        link, name = re.findall('<a href="(.+?)" class="browse-movie-title">(.+?)</a>', entry, re.DOTALL)[0]
                        name = cleantitle.get_title(name)
                        y = entry[-4:]
                        name = ' '.join((name, y))
                        if not source_utils.is_match(name, title, year, self.aliases):
                            continue
                    except:
                        continue

                    response = client.request(link, headers=_headers)
                    if not imdb in response:
                        continue
                    entries = client.parseDOM(response, 'div', attrs={'class': 'modal-torrent'})

                    for torrent in entries:
                        try:
                            link = re.findall('href="magnet:(.+?)"', torrent, re.DOTALL)[0]
                            link = 'magnet:%s' % client.replaceHTMLCodes(link).split('&tr')[0]
                            name = cleantitle.get_title(link.split('dn=')[1])
                            try:
                                _type = re.findall('quality-size">(.+?)</', torrent, re.DOTALL)[0]
                                name = '.'.join((name, _type))
                            except:
                                pass
                            quality, info = source_utils.get_release_quality(name)
                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', torrent)[-1]
                                dsize, isize = source_utils._size(size)
                            except Exception:
                                dsize, isize = 0.0, ''
                            info.insert(0, isize)
                            info = ' | '.join(info)

                            sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en',
                                            'url': link, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'name': name})
                        except:
                            pass
                except:
                    log_utils.log('Ytsam - Exception', 1)
                    continue

            return sources
        except:
            log_utils.log('Ytsam - Exception', 1)
            return sources

    def resolve(self, url):
        return url
