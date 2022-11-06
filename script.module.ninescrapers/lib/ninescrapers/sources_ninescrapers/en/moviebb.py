# -*- coding: UTF-8 -*-

import re
import base64
import requests

from six import ensure_text, ensure_str
from ninescrapers import parse_qs, urljoin, urlparse, urlencode, quote_plus, unquote

from ninescrapers.modules import client
from ninescrapers.modules import cleantitle
from ninescrapers.modules import directstream
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['moviebb.net', 'fast32.com']
        self.base_link = custom_base or 'https://fast32.com'
        self.search_link = '/search-movies/%s.html'
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0', 'Referer': self.base_link})


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('moviebb Exception', 1)
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('moviebb Exception', 1)
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
            log_utils.log('moviebb Exception', 1)
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostprDict + hostDict
            sources = []
            if url is None:
                return sources
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            title = cleantitle.geturl(title)
            year = data['premiered'].split('-')[0] if 'tvshowtitle' in data else data['year']
            query = '%s-season-%s' % (title, data['season']) if 'tvshowtitle' in data else title
            search_url = self.search_link % (query.replace('-', '%20'))
            #html, self.base_link = client.list_request(self.base_link or self.domains, search_url)
            html = self.session.get(urljoin(self.base_link, search_url), headers=self.session.headers).text
            #log_utils.log('moviebb html: ' + html)
            results = client.parseDOM(html, 'div', attrs={'class': 'itemInfo'})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'a'), re.findall('(\d{4})', i)) for i in results]
            results = [(i[0][0], i[1][0], i[2][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0 and len(i[2]) > 0]
            url = [i[0] for i in results if query == cleantitle.geturl(i[1]) and year == i[2]][0]
            #
            ### Stopped here but returns proper results to play. (movies and shows)
            #
            if 'tvshowtitle' in data:
                sepi = 'season-%1d/episode-%1d.html' % (int(data['season']), int(data['episode']))
                data = self.session.get(url, headers=self.session.headers).text
                link = client.parseDOM(data, 'a', ret='href')
                url = [i for i in link if sepi in i][0]
            r = self.session.get(url, headers=self.session.headers).text
            try:
                v = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', r)[0]
                b64 = base64.b64decode(v)
                b64 = ensure_text(b64, errors='ignore')
                url = client.parseDOM(b64, 'iframe', ret='src')[0]
                host = re.findall('([\w]+[.][\w]+)$', urlparse(url.strip().lower()).netloc)[0]
                host = client.replaceHTMLCodes(host)
                host = ensure_str(host)
                valid, hoster = source_utils.is_host_valid(host, hostDict)
                if valid:
                    sources.append({'source': hoster, 'quality': 'SD', 'language': 'en', 'url': url.replace('\/', '/'), 'direct': False, 'debridonly': False})
            except:
                log_utils.log('moviebb Exception', 1)
                pass
            try:
                r = client.parseDOM(r, 'div', {'class': 'server_line'})
                r = [(client.parseDOM(i, 'a', ret='href')[0], client.parseDOM(i, 'p', attrs={'class': 'server_servername'})[0]) for i in r]
                if r:
                    for i in r:
                        host = re.sub('Server|Link\s*\d+', '', i[1]).lower()
                        url = i[0].replace('\/', '/')
                        host = client.replaceHTMLCodes(host)
                        host = ensure_str(host)
                        if 'other' in host: continue
                        valid, hoster = source_utils.is_host_valid(host, hostDict)
                        if valid:
                            sources.append({'source': hoster, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            except:
                log_utils.log('moviebb Exception', 1)
                pass
            return sources
        except:
            log_utils.log('moviebb Exception', 1)
            return sources


    def resolve(self, url):
        if any(x in url for x in self.domains):
            try:
                r = self.session.get(url, headers=self.session.headers).text
                try:
                    v = re.findall(r'document.write\(Base64.decode\("(.+?)"\)', r)[0]
                    b64 = base64.b64decode(v)
                    b64 = ensure_text(b64, errors='ignore')
                    try:
                        url = client.parseDOM(b64, 'iframe', ret='src')[0]
                    except:
                        client.parseDOM(b64, 'a', ret='href')[0]
                    url = url.replace('///', '//')
                except:
                    u = client.parseDOM(r, 'div', attrs={'class': 'player'})
                    url = client.parseDOM(u, 'a', ret='href')[0]
            except:
                log_utils.log('moviebb Exception', 1)
            return url
        else:
            return url


