# -*- coding: UTF-8 -*-
# -Cleaned and Checked on 10-16-2019 by JewBMX in Scrubs.
# -Fixed and py2/3 compat for Nine - June 2021

import re

from six import ensure_text

from ninescrapers import cfScraper
from ninescrapers.modules import client
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
        self.domains = ['telepisodes.org']
        self.base_link = custom_base or 'https://www1.telepisodes.org'
        self.tvshow_link = '/tv-series/%s/season-%s/episode-%s/'
        self.headers = {'User-Agent': client.agent(), 'Referer': self.base_link}


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = urljoin(self.base_link, self.tvshow_link % (url, season, episode))
            #log_utils.log('telepisodes_search: ' + repr(url))
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            #page = cfScraper.get(url, headers=self.headers, timeout=10).text
            r = cfScraper.get(url, headers=self.headers, timeout=10)
            if r.ok:
                page = r.text
            else:
                page = client.request(url, headers=self.headers)
            items = client.parseDOM(page, 'tr', attrs={'class': r'ext_link.*?'})
            #log_utils.log('telepisodes_items: ' + repr(items))
            for item in items:
                hoster = client.parseDOM(item, 'a', ret='title')[0]
                valid, host = source_utils.is_host_valid(hoster, hostDict)
                if valid:
                    link = client.parseDOM(item, 'a', ret='href')[0]
                    url = urljoin(self.base_link, link)
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            log_utils.log('telepisodes_exc', 1)
            return sources


    def resolve(self, url):
        try:
            r = cfScraper.get(url, headers=self.headers, timeout=10)
            if r.ok:
                page = r.text
                match2 = re.compile(r'href=(/open/site/.+?)>', re.I|re.S).findall(page)[0]
                link2 = urljoin(self.base_link, match2)
                link3 = ensure_text(cfScraper.get(link2, timeout=10).url, errors='replace')
            else:
                page = client.request(url, headers=self.headers)
                match2 = re.compile(r'href=(/open/site/.+?)>', re.I|re.S).findall(page)[0]
                link2 = urljoin(self.base_link, match2)
                link3 = client.request(link2, headers=self.headers, output='geturl')
            return link3
        except:
            log_utils.log('telepisodes_res', 1)
            return


