# -*- coding: UTF-8 -*-

'''
    NineScrapers module
'''


import re

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlparse, urlencode, quote_plus
from ninescrapers.modules import cleantitle, client, debrid, log_utils, source_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['rlsbb.ru', 'rlsbb.to', 'releasebb.net', 'proxybb.com'] # cf: 'rlsbb.unblockit.ch'
        self.base_link = custom_base # or 'https://rlsbb.to'
        #self.search_base_link = 'http://search.rlsbb.ru'
        #self.search_cookie = 'serach_mode=rlsbb'
        #self.search_link = 'lib/search526049.php?phrase=%s&pindex=1&content=true'
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('RLSBB - Exception', 1)
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('RLSBB - Exception', 1)
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
            log_utils.log('RLSBB - Exception', 1)
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
            title = title.replace(' ', '-').lower()
            year = re.findall('(\d{4})', data['premiered'])[0] if 'tvshowtitle' in data else data['year']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year
            #premDate = ''

            if int(year) < 2021:
                for i, d in enumerate(self.domains):
                    self.domains[i] = 'old3.' + d
                self.base_link = None

            query = '%s-%s' % (title, hdlr)
            #query = self.search_link % quote_plus(query)
            try: r, _base_link = client.list_request(self.base_link or self.domains, query)
            except: r = None

            # if not r and 'tvshowtitle' in data:
                # query = '%s-s%02d' % (title, int(data['season']))
                # try: r, _base_link = client.list_request(self.base_link or self.domains, query)
                # except: r = None

            if not r and int(year) < 2021:
                for i, d in enumerate(self.domains):
                    self.domains[i] = d.replace('old3.', '')
                query = '%s-%s' % (title, hdlr)
                #query = self.search_link % quote_plus(query)
                r, _base_link = client.list_request(self.base_link or self.domains, query)

            entry_title = client.parseDOM(r, "h1", attrs={"class": "entry-title"})[0]
            if not source_utils.is_match(entry_title, title, hdlr, self.aliases):
                return sources

            posts = client.parseDOM(r, "div", attrs={"class": "content"})
            items = []
            for post in posts:
                try:
                    u = client.parseDOM(post, 'a', ret='href')
                    for i in u:
                        try:
                            if not i.endswith(('.rar', '.zip', '.iso', '.idx', '.sub', '.srt', '.ass', '.ssa')) \
                            and not any(x in i for x in ['.rar.', '.zip.', '.iso.', '.idx.', '.sub.', '.srt.', '.ass.', '.ssa.']):
                                items.append(i)
                            #elif len(premDate) > 0 and premDate in i.replace(".", "-"):
                                #items.append(i)
                        except:
                            pass
                except:
                    pass

            if items:

                seen_urls = set()

                for item in items:
                    try:
                        url = item.replace("\\", "").strip('"')

                        if url in seen_urls:
                            continue
                        seen_urls.add(url)

                        name = cleantitle.get_title(url.split('/')[-1]) or cleantitle.get_title(entry_title)
                        # if not cleantitle.get(title) in cleantitle.get(name):
                            # continue

                        quality, info = source_utils.get_release_quality(name)
                        info = ' | '.join(info)

                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            #log_utils.log('rlsbb name: %s | url: %s' % (repr(name), repr(url)))
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
                                            'info': info, 'direct': False, 'debridonly': True, 'name': name})
                    except:
                        #log_utils.log('RLSBB - Exception', 1)
                        pass

            return sources
        except:
            log_utils.log('RLSBB - Exception', 1)
            return sources

    def resolve(self, url):
        return url
