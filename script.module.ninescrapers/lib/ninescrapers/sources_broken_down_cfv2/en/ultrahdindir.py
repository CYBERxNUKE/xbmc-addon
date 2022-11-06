# -*- coding: UTF-8 -*-
# Re-written for Nine

import re

from ninescrapers import cfScraper
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import cleantitle
from ninescrapers.modules import client
from ninescrapers.modules import debrid
from ninescrapers.modules import dom_parser
from ninescrapers.modules import source_utils
from ninescrapers.modules import log_utils

from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['ultrahdindir.com']
        self.base_link = custom_base or 'https://ultrahdindir.com'
        self.search_link = '/index.php?do=search&subaction=search&search_start=0&full_search=0&result_from=1&story=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            log_utils.log('ultrahd_exc3', 1)
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None:
                return sources
            if debrid.status() is False:
                return sources
            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            query = '%s %s' % (data['title'], data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)
            url = urljoin(self.base_link, self.search_link % quote_plus(query))
            #log_utils.log('ultrahd_url ' + url)
            r = cfScraper.get(url, timeout=10).text
            r = client.parseDOM(r, 'div', attrs={'class': 'box-out margin'})
            r = [(dom_parser.parse_dom(i, 'div', attrs={'class':'news-title'})) for i in r if data['imdb'] in i]
            r = [(dom_parser.parse_dom(i[0], 'a', req='href')) for i in r if i]
            r = [(i[0].attrs['href'], i[0].content) for i in r if i]
            hostDict = hostprDict + hostDict

            for item in r:
                try:
                    data = cfScraper.get(item[0], timeout=10).text
                    data = client.parseDOM(data, 'div', attrs={'id': 'r-content'})[0]
                    urls = re.findall(r'\s*<u><a href="(.+?)".+?</a></u>', data, re.S)
                    try: details = client.parseDOM(data, 'div', attrs={'class': 'text_spoiler'})[0]
                    except: details = None
                    if details:
                        _zip = zip([u for u in urls if u.startswith('https://turbobit')], re.findall(r'General : (.+?)<br', details), re.findall(r'Length : (.+?) for', details))
                    else:
                        _zip = zip([u for u in urls if u.startswith('https://turbobit')], re.findall(r'/uploads/0-0-vip-(.+?).jpg', data, re.I|re.S))

                    for z in _zip:
                        try:
                            url = client.replaceHTMLCodes(z[0])
                            name = cleantitle.get_title(z[1]).replace('dual', ' dual ')
                            if 'dublaj' in name.lower(): continue

                            quality, info = source_utils.get_release_quality(url, name)
                            if quality == 'sd' and 'remux' in name.lower(): quality = '1080p'

                            try:
                                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', z[2])[0]
                                dsize, isize = source_utils._size(size)
                            except:
                                dsize, isize = 0.0, ''
                            info.insert(0, isize)

                            info = ' | '.join(info)
                            if any(x in url for x in ['.rar', '.zip', '.iso']):
                                raise Exception()
                            # if not 'turbobit' in url:
                                # continue
                            sources.append({'source': 'turbobit', 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'size': dsize, 'name': name, 'direct': False, 'debridonly': True})
                        except:
                            log_utils.log('ultrahd_exc2', 1)
                            pass
                except:
                    log_utils.log('ultrahd_exc1', 1)
                    pass
            return sources
        except:
            log_utils.log('ultrahd_exc0', 1)
            return sources


    def resolve(self, url):
        return url

