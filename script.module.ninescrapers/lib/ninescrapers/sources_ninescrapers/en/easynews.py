# -*- coding: utf-8 -*-

'''
    OpenScrapers Project
    Updated for Nine
'''

import re
import base64
import requests
import six

from ninescrapers import parse_qs, urljoin, urlencode, quote
from ninescrapers.modules import cleantitle, control, log_utils, source_utils, utils


SORT = {'s1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-'}
SEARCH_PARAMS = {'st': 'adv', 'sb': 1, 'fex': 'm4v,3gp,mov,divx,xvid,wmv,avi,mpg,mpeg,mp4,mkv,avc,flv,webm', 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3}
SEARCH_PARAMS.update(SORT)


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['easynews.com']
        self.base_link = 'https://members.easynews.com'
        self.search_link = '/2.0/search/solr-search/advanced'
        self.aliases = []


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urlencode(url)
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urlencode(url)
            return url
        except:
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
            return


    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if not url:
                return sources

            auth = self._get_auth()
            if not auth:
                return sources

            try:
                title_chk = control.setting('easynews.title.chk') == 'true'
                data = parse_qs(url)
                data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

                title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
                year = data['year']
                years = '%s,%s,%s' % (str(int(year) - 1), year, str(int(year) + 1))
                hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else year
                query = '%s %s' % (title, hdlr if 'tvshowtitle' in data else years)

                url, params = self._translate_search(query)
                headers = {'Authorization': auth}
                r = requests.get(url, params=params, headers=headers, timeout=15)
                r.raise_for_status()
                r.encoding = 'utf-8'
                results = r.json() if six.PY3 else utils.json_loads_as_str(r.text)
                down_url = results.get('downURL')
                dl_farm = results.get('dlFarm')
                dl_port = results.get('dlPort')
                files = results.get('data', [])
            except:
                log_utils.log('EASYNEWS exc', 1)
                return sources

            for item in files:
                try:
                    post_hash, post_title, ext, duration, size = item['0'], item['10'], item['11'], item['14'], item['4']
                    checks = [False] * 5
                    if 'alangs' in item and item['alangs'] and 'eng' not in item['alangs']: checks[1] = True
                    if re.match('^\d+s', duration) or re.match('^[0-5]m', duration): checks[2] = True
                    if 'passwd' in item and item['passwd']: checks[3] = True
                    if 'virus' in item and item['virus']: checks[4] = True
                    if 'type' in item and item['type'].upper() != 'VIDEO': checks[5] = True
                    if any(checks):
                        continue

                    stream_url = down_url + quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
                    name_chk = post_title + ext
                    if 'tvshowtitle' in data:
                        name_chk = re.sub(r'S\d+([.-])E\d+', hdlr, name_chk, 1, re.I)
                        name_chk = re.sub(r'^tvp[.-]', '', name_chk, 1, re.I)
                    name_chk = re.sub(r'disney[.-]gallery[.-]star[.-]wars[.-]', '', name_chk, 0, re.I)
                    name_chk = re.sub(r'marvels[.-]', '', name_chk, 0, re.I)
                    name_chk = cleantitle.get_title(name_chk)
                    if title_chk:
                        if not source_utils.is_match(name_chk, title, hdlr, self.aliases):
                            continue

                    file_dl = stream_url + '|Authorization=%s' % (quote(auth))

                    quality, info = source_utils.get_release_quality(name_chk, stream_url)
                    try:
                        dsize, isize = source_utils._size(size)
                    except:
                        dsize, isize = 0.0, ''
                    info.insert(0, isize)
                    info = ' | '.join(info)

                    sources.append({'source': 'direct', 'quality': quality, 'language': 'en', 'url': file_dl,
                                    'info': info, 'direct': True, 'debridonly': True, 'size': dsize, 'name': name_chk})
                except:
                    log_utils.log('EASYNEWS exc', 1)
                    pass
            return sources
        except:
            log_utils.log('EASYNEWS exc', 1)
            return sources


    def _get_auth(self):
        auth = None
        try:
            username = control.setting('easynews.user')
            password = control.setting('easynews.pass')
            if not username or not password:
                return auth
            user_info = '%s:%s' % (username, password)
            user_info = six.ensure_text(base64.b64encode(six.ensure_binary(user_info)))
            auth = 'Basic ' + user_info
        except:
            log_utils.log('EASYNEWS exc', 1)
            pass
        return auth


    def _translate_search(self, query):
        params = SEARCH_PARAMS
        params['pby'] = 350
        params['safeO'] = 1
        params['gps'] = query
        url = urljoin(self.base_link, self.search_link)
        return url, params


    def resolve(self, url):
        return url



