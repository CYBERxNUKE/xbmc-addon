# -*- coding: utf-8 -*-

'''
    Exodus Add-on
    Copyright (C) 2016 Exodus

    Re-written by JewBMX
    Adjusted for Nine
'''


import re

from ninescrapers import parse_qs, urlencode, quote_plus
from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import jsunpack
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['streamlord.com']
        self.base_link = custom_base or 'http://www.streamlord.com'
        self.search_link = 'https://www.google.com/search?q=%s+site:streamlord.com'


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
            if url == None: return

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
            if url == None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            hdlr = 's%02de%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']
            search_title = cleantitle.get_title(title, sep='+')
            check_title = '%s+%s' % (search_title, hdlr)
            query = '%s %s' % (title, hdlr)
            search_url = self.search_link % quote_plus(query)

            html = client.request(search_url)
            tag = re.findall(r'<div class="(\w+)"><a href="http:', html)[0]
            results = client.parseDOM(html, 'div', attrs={'class': tag})
            results = [(client.parseDOM(i, 'a', ret='href'), client.parseDOM(i, 'h3')) for i in results]
            results = [(i[0][0], i[1][0]) for i in results if len(i[0]) > 0 and len(i[1]) > 0]
            result = [i[0] for i in results if check_title.lower() in cleantitle.get_title(i[1], sep='+').lower()][0]
            result_html = client.request(result)

            link = None
            try: # Havent seen this used.
                f = re.findall('''["']sources['"]\s*:\s*\[(.*?)\]''', result_html)[0]
                f = re.findall('''['"]*file['"]*\s*:\s*([^\(]+)''', f)[0]
                u = re.findall('function\s+%s[^{]+{\s*([^}]+)' % f, result_html)[0]
                u = re.findall('\[([^\]]+)[^+]+\+\s*([^.]+).*?getElementById\("([^"]+)', u)[0]
                a = re.findall('var\s+%s\s*=\s*\[([^\]]+)' % u[1], result_html)[0]
                b = client.parseDOM(result_html, 'span', attrs={'id': u[2]})[0]
                link = u[0] + a + b
                link = link.replace('"', '').replace(',', '').replace('\/', '/')
            except:
                pass
            try: # this seems to be used for shows.
                link = jsunpack.unpack(result_html)
                link = link.replace('"', '')
            except:
                pass
            try: # this seems to be used for movies.
                link = re.findall(r'sources[\'"]\s*:\s*\[.*?file[\'"]\s*:\s*(\w+)\(\).*function\s+\1\(\)\s*\{\s*return\([\'"]([^\'"]+)', result_html, re.DOTALL)[0][1]
            except:
                pass

            quality = '720p' if '-movie-' in result_html else 'SD'

            if link:
                sources.append({'source': 'cdn', 'quality': quality, 'language': 'en', 'url': link, 'direct': True, 'debridonly': False})
            return sources
        except:
            log_utils.log('streamlord_exc0', 1)
            return sources


    def resolve(self, url):
        return url


