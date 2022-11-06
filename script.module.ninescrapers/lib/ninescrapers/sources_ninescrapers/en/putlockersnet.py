# -*- coding: UTF-8 -*-


import re
import requests

import simplejson as json
from six import ensure_text

from ninescrapers.modules import client
from ninescrapers.modules import debrid
from ninescrapers.modules import cleantitle
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils
from ninescrapers import urljoin

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['wwv.putlockers.net']
        self.base_link = custom_base or 'https://wwv.putlockers.net'
        self.search_link = '/search/?s=%s'
        self.headers = {'User-Agent': client.agent(), 'Referer': self.base_link}
        self.gomo_link = 'https://gomo.to/decoding_v3.php'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            if debrid.status() is True:
                return
            movieTitle = cleantitle.clean_search_query(title)
            link = urljoin(self.base_link, self.search_link % (movieTitle + '+' + year))
            searchPage = requests.get(link, headers=self.headers).text
            pages = client.parseDOM(searchPage, 'div', attrs={'class': 'featuredItems singleVideo'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in pages]
            result = [(i[0][0], i[1][0]) for i in results if i[0] and i[1]]
            link2 = [i[0] for i in result if cleantitle.get(title) == cleantitle.get(i[1])][0]
            moviePage = requests.get(link2, headers=self.headers).text
            videoArea = client.parseDOM(moviePage, 'div', attrs={'class': 'videoArea'})
            url = client.parseDOM(videoArea, 'a', ret='href')[0]
            return url
        except Exception:
            log_utils.log('putlockersnet Exception', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            if debrid.status() is True:
                return
            tvshowTitle = cleantitle.clean_search_query(tvshowtitle)
            link = urljoin(self.base_link, self.search_link % (tvshowTitle))
            searchPage = requests.get(link, headers=self.headers).text
            pages = client.parseDOM(searchPage, 'div', attrs={'class': 'featuredItems singleVideo'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a', ret='title')) for i in pages]
            result = [(i[0][0], i[1][0]) for i in results if i[0] and i[1]]
            link2 = [i[0] for i in result if cleantitle.get(tvshowtitle) == cleantitle.get(i[1])][0]
            url = re.findall('(?://.+?|)(/.+)', link2)[0]
            return url
        except Exception:
            log_utils.log('putlockersnet Exception', 1)
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            #log_utils.log('putlockersnet url: ' + url)
            tvshowtitle = url.rstrip('/').split('/')[-1]
            link = urljoin(self.base_link, '/episode/%s-%sx%s/' % (tvshowtitle, season, episode))
            #log_utils.log('putlockersnet link: ' + link)
            episodePage = requests.get(link, headers=self.headers).text
            videoArea = client.parseDOM(episodePage, 'div', attrs={'class': 'videoArea'})
            url = client.parseDOM(videoArea, 'a', ret='href')[0]
            return url
        except Exception:
            log_utils.log('putlockersnet Exception', 1)
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if debrid.status() is True:
                return sources
            if not url:
                return sources
            hostDict = hostDict + hostprDict
            sourcePage = requests.get(url, headers=self.headers).text
            links = client.parseDOM(sourcePage, 'iframe', ret='src')
            #log_utils.log('putlockersnet links: \n' + repr(links))
            for link in links:
                if 'gomo.to' in link:
                    for source in self.scrapeGomo(link, hostDict):
                        sources.append(source)
                else:
                    valid, host = source_utils.is_host_valid(link, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(link, link)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            log_utils.log('putlockersnet Exception', 1)
            return sources


    def scrapeGomo(self, url, hostDict):
        sources = []
        try:
            result = ensure_text(client.request(url, verify=False), errors='replace')
            tc = re.compile('tc = \'(.+?)\';').findall(result)[0]
            if (tc):
                token = re.compile('"_token": "(.+?)",').findall(result)[0]
                post = {'tokenCode': tc, '_token': token}
                def tsd(tokenCode):
                    _13x48X = tokenCode
                    _71Wxx199 = _13x48X[4:18][::-1]
                    return _71Wxx199 + "18" + "432782"
                headers = {'Host': 'gomo.to', 'Referer': url, 'User-Agent': client.agent(), 'x-token': tsd(tc)}
                result = ensure_text(client.request(self.gomo_link, XHR=True, post=post, headers=headers, verify=False), errors='replace')
                links = json.loads(result)
                for link in links:
                    link = "https:" + link if not link.startswith('http') else link
                    if 'gomo.to' in link:
                        link = ensure_text(requests.get(link, headers=self.headers, verify=False).url, errors='replace')
                        # if 'gomoplayer.com' in link: # gomoplayer added to resolveurl now
                            # from ninescrapers.modules import jsunpack
                            # sourcePage = ensure_text(requests.get(link, headers=self.headers, verify=False).content, errors='ignore')
                            # if jsunpack.detect(sourcePage):
                                # unpacked = jsunpack.unpack(sourcePage)
                                # urls = re.compile('file:"(.+?)"').findall(unpacked)
                                # for url in urls:
                                    # if '/srt/' in url: continue
                                    # info = 'MP4' if url.endswith('.mp4') else 'm3u8'
                                    # sources.append({'source': 'CDN', 'quality': 'SD', 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                        # https://database.gdriveplayer.us/player.php?imdb=tt1825683
                    # else:
                    valid, host = source_utils.is_host_valid(link, hostDict)
                    if valid:
                        quality, info = source_utils.get_release_quality(link)
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            log_utils.log('putlockersnet Exception', 1)
            return sources


    def resolve(self, url):
        return url


