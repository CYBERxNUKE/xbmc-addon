# -*- coding: utf-8 -*-

'''
    Exodus Add-on (C) 2017
    
    Rewritten for Nine
'''


import re
from six import PY3

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
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
        self.domains = ['miradetodo.co']
        self.base_link = custom_base or 'https://miradetodo.co'
        self.search_link = '/?s=%s'
        self.episode_link = '/episodio/%s-%sx%s'
        self.tvshow_link = '/series/%s/'

    def movie(self, imdb, title, localtitle, aliases, year):

        try:
            t = 'https://www.imdb.com/title/%s' % imdb
            t = cfScraper.get(t, headers={'Accept-Language': 'es-AR'}, timeout=10).text
            t = client.parseDOM(t, 'title')[0]
            t = re.sub('(?:\(|\s)\d{4}.+', '', t).strip()
            t = ' '.join((t, year))

            s = ' '.join((title, year))

            check = [cleantitle.get(t), cleantitle.get(s)]

            q = self.search_link % quote_plus(s)
            q = urljoin(self.base_link, q)

            r = cfScraper.get(q, timeout=10).text

            r = client.parseDOM(r, 'div', attrs={'class': 'item'})
            r = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'span', attrs={'class': 'tt'}), client.parseDOM(i, 'span', attrs={'class': 'year'})) for i in r]
            r = [(i[0][0], i[1][0], i[2][0]) for i in r if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            r = [i[0] for i in r if cleantitle.get(i[1]) in check and year == i[2]][0]

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url
        except:
            log_utils.log('Miradetodo - Exception', 1)
            pass

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            t = cleantitle.geturl(tvshowtitle)

            q = self.tvshow_link % t
            q = urljoin(self.base_link, q)
            r = cfScraper.get(q, timeout=10).url

            if not r:
                t = 'https://www.imdb.com/title/%s' % imdb
                t = cfScraper.get(t, headers={'Accept-Language': 'es-AR'}, timeout=10).text
                t = client.parseDOM(t, 'title')[0]
                t = re.sub('(?:\(|\s)\(TV Series.+', '', t).strip()

                q = self.search_link % quote_plus(t)
                q = urljoin(self.base_link, q)

                r = cfScraper.get(q, timeout=10).text

                r = client.parseDOM(r, 'div', attrs={'class': 'item'})
                r = zip(client.parseDOM(r, 'a', ret='href'), client.parseDOM(r, 'span', attrs={'class': 'tt'}), client.parseDOM(r, 'span', attrs={'class': 'year'}))
                r = [(i[0], re.sub('(?:\(|\s)\('+year+'.+', '', i[1]).strip(), i[2]) for i in r if len(i[0]) > 0 and '/series/' in i[0] and len(i[1]) > 0 and len(i[2]) > 0]
                r = [i[0] for i in r if year == i[2]][0]

            r = r.replace('-actualidad', '').replace('-%s' % year, '')
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'url': r}
            url = urlencode(url)
            return url
        except:
            log_utils.log('Miradetodo - Exception', 1)
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            show = data['url'].split('/')[4]
            r = urljoin(self.base_link, self.episode_link % (show, season, episode))

            url = re.findall('(?://.+?|)(/.+)', r)[0]
            url = client.replaceHTMLCodes(url)
            return url
        except:
            log_utils.log('Miradetodo - Exception', 1)
            pass

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:

            if url is None: return sources

            hostDict = hostprDict + hostDict

            url = urljoin(self.base_link, url)
            #log_utils.log('mtd_url: ' + repr(url))

            result = cfScraper.get(url, timeout=10).text

            try:
                f = client.parseDOM(result, 'div', attrs={'class': 'movieplay'})[0]
            except:
                f = client.parseDOM(result, 'div', attrs={'class': 'embed2'})[0]
                f = client.parseDOM(f, 'div')[0]

            f = client.parseDOM(f, 'iframe', ret='data-lazy-src')[0]

            try:
                if PY3: r = client.request(f, headers={'Referer': self.base_link})
                else: r = cfScraper.get(f, headers={'User-Agent': client.agent(), 'Referer': self.base_link}, timeout=10).text
                r = client.parseDOM(r, 'li')

                links = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'span')[1]) for i in r if i]

                dupes = []

                for url, hoster in links:
                    try:
                        id = re.findall(r'id=(.+?)&sub', url, re.I)[0]
                        if id in dupes: continue
                        dupes.append(id)

                        url = url.split('&sub')[0]

                        hoster = hoster.lower().replace(' ', '.').replace('mega', 'mega.nz').replace('descargar', 'cdn').replace('ver.online', 'cdn')
                        if hoster in ['amazon', 'mediafire']: continue
                        if hoster in ['gdrive', 'yandex'] or '/stream/' in url:
                            sources.append({'source': hoster, 'quality': '720p', 'language': 'en', 'url': url,
                                            'direct': True, 'debridonly': False})
                        else:
                            valid, host = source_utils.is_host_valid(hoster, hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': url,
                                                'info': 'HC-SUBS', 'direct': False, 'debridonly': False})
                    except:
                        log_utils.log('Miradetodo - Exception', 1)
                        pass


            except:
                log_utils.log('Miradetodo - Exception', 1)
                pass

            return sources
        except:
            log_utils.log('Miradetodo - Exception', 1)
            return sources

    def resolve(self, url):
        try:
            if not '/stream/' in url or '/stream/down' in url:
                r = cfScraper.get(url, headers={'User-Agent': client.agent(), 'Referer': self.base_link}, timeout=10).text
                r = client.parseDOM(r, 'body')[0]
                try: url = client.parseDOM(r, 'iframe', ret='src')[0]
                except: url = client.parseDOM(r, 'a', ret='href')[0]
                url = url.replace('\r', '')

            if '/stream/' in url:
                r2 = cfScraper.get(url, headers={'User-Agent': client.agent(), 'Referer': self.base_link}, timeout=10).text
                url = re.findall(r'[?:sources\s*:\s*\[\{]file\s*:\s*"(.+?)"', r2)[0]
                url = url.replace('http://', 'https://')
        except:
            log_utils.log('Miradetodo - Exception', 1)
            url = None
        return url


