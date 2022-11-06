# -*- coding: utf-8 -*-

'''
    NineScrapers module
'''


import re, base64

from six import ensure_text

#from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode
from ninescrapers.modules import client
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['fsapi.xyz']
        self.base_link = custom_base or 'https://fsapi.xyz'
        self.search_link = '/movie/%s'
        self.search_link2 = '/tv-imdb/%s-%s-%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
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

            hostDict = hostprDict + hostDict
            direct_stream = tuple(source_utils.supported_video_extensions())

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            if not data['imdb'] or data['imdb'] == '0':
                return sources

            if 'tvshowtitle' in data:
                query = self.search_link2 % (data['imdb'], data['season'], data['episode'])
            else:
                query = self.search_link % data['imdb']

            url = urljoin(self.base_link, query)
            posts = client.r_request(url)
            #log_utils.log('fsapi_posts: ' + posts)
            r = re.findall('<a href="(.+?)" rel', posts)
            r = client.parseDOM(posts, 'a', ret='href', attrs={'target': 'iframe_a'})
            urls = [u.split('url=')[1] for u in r]
            urls = [ensure_text(base64.b64decode(url), errors='ignore') for url in urls]
            urls = ['https:' + url if url.startswith('//') else url for url in urls]
            urls = list(set(urls))
            #log_utils.log('fsapi_all_urls: ' + repr(urls))

            for url in urls:

                try:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

                    elif '/hls/' in url or url.endswith(direct_stream):
                        sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})

                    # elif 'vidsrc' in url: # vidsrc turned on a scraper of its own
                        # try:
                            # r = client.request(url, headers={'User-Agent': client.agent(), 'Referer': 'https://v2.vidsrc.me'})
                            # r = re.findall('data-hash="(.+?)"', r)[0]
                            # log_utils.log('fsapi_vidsrc_r: ' + repr(r))
                            # r = 'https://v2.vidsrc.me/src/%s' % r
                            # r2 = client.request(r, headers={'User-Agent': client.agent(), 'Referer': 'https://v2.vidsrc.me'})
                            # links = re.findall("'player' src='(.+?)'", r2) + re.findall('"file": "(.+?)"', r2)
                            # log_utils.log('fsapi_vidsrc_links: ' + repr(links))
                            # links = [link + '|Referer=https://vidsrc.me' for link in links]
                            # for url in links:
                                # url = url if url.startswith('http') else 'https:{0}'.format(url)
                                # sources.append({'source': 'CDN', 'quality': '720p', 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
                        # except:
                            # pass
                except:
                    log_utils.log('FSAPI Exception', 1)
                    pass

            return sources
        except:
            log_utils.log('FSAPI Exception', 1)
            return sources

    def resolve(self, url):
        #log_utils.log('FSAPI url: ' + repr(url))
        return url
