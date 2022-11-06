# -*- coding: utf-8 -*-

'''
    NineScrapers module
'''

import re

from six import ensure_str

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus

from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import dom_parser
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['el']
        self.domains = ['tenies-online']
        self.base_link = custom_base or 'https://tenies-online1.gr'
        self.search_link = '/?s=%s'
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'localtitle': localtitle, 'title': title, 'year': year}
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

            if url == None: return sources

            hostDict = hostprDict + hostDict

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            year = data['year']
            hdlr = '%s s%02de%02d' % (title.lower(), int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year
            query = '%s %s' % (title, year)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            query = quote_plus(query)

            url = urljoin(self.base_link, self.search_link % query)
            #log_utils.log('tainies_onl url: ' + repr(url))

            headers = {'User-Agent': client.agent(),
                       'Referer': self.base_link}
            #r = client.request(url, headers=headers)
            r = cfScraper.get(url, headers=headers, timeout=15).text
            posts = client.parseDOM(r, 'div', attrs={'class': 'result-item'})

            if posts:
                for post in posts:
                    try:
                        link = client.parseDOM(post, 'a', ret='href')[0]
                        name = client.parseDOM(post, 'img', ret='alt')[0]
                        name = client.replaceHTMLCodes(name)
                        name = ensure_str(name, errors='ignore')
                        t = name.split(' /')[0]
                        y = re.findall('\((\d{4})\)', name, re.I)[0]
                        name = ' '.join((t, y))
                        if not source_utils.is_match(name, title, year, self.aliases):
                            continue

                        #r2 = client.request(link)
                        r2 = cfScraper.get(link, timeout=10).text

                        if not 'tvshowtitle' in data:
                            try:
                                frames = client.parseDOM(r2, 'tr', attrs={'id': r'link-\d+'})
                                frames = [(client.parseDOM(i, 'a', ret='href', attrs={'target': '_blank'})[0],
                                           client.parseDOM(i, 'img', ret='src')[0],
                                           client.parseDOM(i, 'td')[-3]) for i in frames if frames]

                                for url, domain, _info in frames:
                                    try:
                                        host = ensure_str(domain.split('=')[-1])
                                        valid, host = source_utils.is_host_valid(host, hostDict)
                                        if not valid: continue

                                        if 'Μεταγλωτισμένο' in ensure_str(_info, errors='replace'):
                                            info = 'DUB'
                                        elif 'Ελληνικοί' in ensure_str(_info, errors='replace'):
                                            info = 'SUBS'
                                        elif 'Χωρίς' in ensure_str(_info, errors='replace'):
                                            info = ''
                                        else:
                                            info = ''

                                        sources.append({'source': host, 'quality': 'sd', 'language': 'el', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                                    except:
                                        pass
                            except:
                                #log_utils.log('tainies_onl_exc4', 1)
                                pass

                        else:
                            try:
                                old_seasons = client.parseDOM(r2, 'div', attrs={'class': r'wp-content'})[0]
                                seasons = [client.parseDOM(old_seasons, 'div', attrs={'class': r'easySpoilerGroupWrapperFirst'}) +
                                           client.parseDOM(old_seasons, 'div', attrs={'class': r'easySpoilerGroupWrapper'})][0]
                                           # client.parseDOM(seasons, 'div', attrs={'class': r'easySpoilerGroupWrapperLast'})]
                                episodes = dom_parser.parse_dom(seasons, 'a', req='href')
                                patterns = ['s%02de%02d' % (int(data['season']), int(data['episode'])), 's%02d e%02d' % (int(data['season']), int(data['episode']))]
                                episode = [(i.attrs['href'], i.content.lower()) for i in episodes if any(x in i.content.lower() for x in patterns) and i.attrs['href'].startswith('http')]
                                if not episode:
                                    seasons2 = client.parseDOM(old_seasons, 'h3')
                                    patterns2 = ['>Σεζόν %s<' % data['season'], '>σεζόν %s<' % data['season'], '>Season %s<' % data['season']]
                                    season = [s for s in seasons2 if any(x in s for x in patterns2)][0]
                                    episodes = dom_parser.parse_dom(season, 'a', req='href')
                                    episode = [(i.attrs['href'], i.content) for i in episodes if '%02d' % int(data['episode']) in i.content and i.attrs['href'].startswith('http')]

                                for url, name in episode:
                                    try:
                                        valid, host = source_utils.is_host_valid(url, hostDict)
                                        if not valid: continue
                                        quality, info = source_utils.get_release_quality(name, url)
                                        #info.append(name)
                                        info = ' | '.join(info)

                                        sources.append({'source': host, 'quality': quality, 'language': 'el', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                                    except:
                                        pass
                            except:
                                #log_utils.log('tainies_onl_exc3', 1)
                                pass

                            try:
                                seasons = client.parseDOM(r2, 'div', attrs={'class': r'se-c'})
                                cur_season = [s for s in seasons if client.parseDOM(s, 'span', attrs={'class': r'se-t.*?'})[0] == data['season']][0]
                                cur_season = client.parseDOM(cur_season, 'ul', attrs={'class': r'episodios'})[0]
                                episode = client.parseDOM(cur_season, 'li', attrs={'class': r'mark-%s' % data['episode']})[0]
                                hdlr2 = '%s - %s' % (data['season'], data['episode'])
                                if not client.parseDOM(episode, 'div', attrs={'class': r'numerando'})[0] == hdlr2: raise Exception()
                                link2 = client.parseDOM(episode, 'a', ret='href')[0]
                                r3 = cfScraper.get(link2, timeout=10).text
                                frames = client.parseDOM(r3, 'tr', attrs={'id': r'link-\d+'})
                                frames = [(client.parseDOM(i, 'a', ret='href', attrs={'target': '_blank'})[0],
                                           client.parseDOM(i, 'img', ret='src')[0],
                                           client.parseDOM(i, 'td')[-3]) for i in frames if frames]

                                for frame in frames:
                                    try:
                                        url = frame[0]

                                        host = ensure_str(frame[1].split('=')[-1])
                                        valid, host = source_utils.is_host_valid(host, hostDict)
                                        if not valid: continue

                                        _info = frame[2]
                                        if 'Μεταγλωτισμένο' in ensure_str(_info, errors='replace'):
                                            info = 'DUB'
                                        elif 'Ελληνικοί' in ensure_str(_info, errors='replace'):
                                            info = 'SUBS'
                                        elif 'Χωρίς' in ensure_str(_info, errors='replace'):
                                            info = ''
                                        else:
                                            info = ''

                                        sources.append({'source': host, 'quality': 'sd', 'language': 'el', 'url': url, 'info': info, 'direct': False, 'debridonly': False})
                                    except:
                                        pass
                            except:
                                #log_utils.log('tainies_onl_exc2', 1)
                                pass

                    except:
                        log_utils.log('tainies_onl_exc1', 1)
                        pass

            return sources
        except:
            log_utils.log('tainies_onl_exc', 1)
            return sources

    def resolve(self, url):
        if '/links/' in url:
            r = cfScraper.get(url, timeout=15).text
            url = client.parseDOM(r, 'a', attrs={'id': 'link'}, ret='href')[0]
        #log_utils.log('tainies_onl_url: ' + str(url))
        return url