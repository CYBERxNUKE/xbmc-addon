# -*- coding: utf-8 -*-
# Created by Tempest
# Rewritten for Nine


import re
from ninescrapers import parse_qs, urljoin, urlencode, quote_plus
from ninescrapers.modules import source_utils
from ninescrapers.modules import client
from ninescrapers.modules import log_utils


from ninescrapers import custom_base_link
custom_base = custom_base_link(__name__)

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domain = ['downloads-anymovies.com']
        self.base_link = custom_base or 'https://www.downloads-anymovies.co'
        self.search_link = '/search.php?zoom_query=%s'
        self.headers = {'User-Agent': client.agent()}
        self.aliases = []

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            data = parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']

            query = ' '.join((title, year))
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link % quote_plus(query)
            url = urljoin(self.base_link, url).replace('++', '+')

            post = client.request(url, headers=self.headers)
            items = re.compile('class="result_title"><a href="(.+?)">(.+?)</a></div>').findall(post)
            for url, data in items:
                data = data[6:] if data.lower().startswith('watch ') else data
                if not source_utils.is_match(data, title, year, self.aliases):
                    continue
                r = client.request(url, headers=self.headers)
                try:
                    links = re.findall('<span class="text"><a href="(.+?)" target="_blank">', r)
                    for link in links:
                        valid, host = source_utils.is_host_valid(link, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                except:
                    return

            return sources
        except Exception:
            log_utils.log('ANYMOVIES - Exception', 1)
            return sources

    def resolve(self, url):
        return url
