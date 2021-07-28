# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.

import re, urllib, urlparse, json
from resources.lib.modules import cleantitle, client
from resources.lib.modules import dom_parser
from resources.lib.modules import source_utils
from resources.lib.sources import cfscrape


class s0urce:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['123123movies.net']
        self.base_link = 'http://www6.123123movies.net'
        self.search_link = '/watch/%s-%s-123movies.html'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (clean_title, year)))
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            aliases.append({'country': 'us', 'title': tvshowtitle})
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            clean_title = cleantitle.geturl(url['tvshowtitle']) + '-s%02d' % int(season)
            url = urlparse.urljoin(self.base_link, (self.search_link % (clean_title, url['year'])))
            r = cfscrape.get(url, headers={'User-Agent': client.agent()}).content
            r = dom_parser.parse_dom(r, 'div', {'id': 'ip_episode'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            for i in r[0]:
                if i.content == 'Episode %s' % episode:
                    url = i.attrs['href']
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            if url is None:
                return sources
            r = cfscrape.get(url, headers={'User-Agent': client.agent()}).content
            qual = re.findall(">(\w+)<\/p", r)
            for i in qual:
                quality, info = source_utils.get_release_quality(i, i)
            r = dom_parser.parse_dom(r, 'div', {'id': 'servers-list'})
            r = [dom_parser.parse_dom(i, 'a', req=['href']) for i in r if i]
            for i in r[0]:
                url = {'url': i.attrs['href'], 'data-film': i.attrs['data-film'], 'data-server': i.attrs['data-server'], 'data-name': i.attrs['data-name']}
                url = urllib.urlencode(url)
                valid, host = source_utils.is_host_valid(i.content, hostDict)
                if valid:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        try:
            urldata = urlparse.parse_qs(url)
            urldata = dict((i, urldata[i][0]) for i in urldata)
            post = {'ipplugins': 1, 'ip_film': urldata['data-film'], 'ip_server': urldata['data-server'], 'ip_name': urldata['data-name'], 'fix': "0"}
            cfscrape.headers.update({'Referer': urldata['url'], 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': client.agent()})
            p1 = cfscrape.post('http://www6.123123movies.net/ip.file/swf/plugins/ipplugins.php', data=post, headers={'User-Agent': client.agent()}).content
            p1 = json.loads(p1)
            p2 = cfscrape.get('http://www6.123123movies.net/ip.file/swf/ipplayer/ipplayer.php?u=%s&s=%s&n=0' % (p1['s'], urldata['data-server']), headers={'User-Agent': client.agent()}).content
            p2 = json.loads(p2)
            p3 = cfscrape.get('http://www6.123123movies.net/ip.file/swf/ipplayer/api.php?hash=%s' % (p2['hash']), headers={'User-Agent': client.agent()}).content
            p3 = json.loads(p3)
            n = p3['status']
            if n is False:
                p2 = cfscrape.get('http://www6.123123movies.net/ip.file/swf/ipplayer/ipplayer.php?u=%s&s=%s&n=1' % (p1['s'], urldata['data-server']), headers={'User-Agent': client.agent()}).content
                p2 = json.loads(p2)
            url = p2["data"].replace("\/","/")
            if not url.startswith('http'):
                url = "https:" + url
            return url
        except:
            return
