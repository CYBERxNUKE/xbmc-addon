# -*- coding: utf-8 -*-

'''
   Incursion Add-on
   Copyright (C) 2016 Incursion
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import requests
from ninescrapers.modules import cleantitle, source_utils, client, control, log_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['furk.net']
        self.base_link = 'https://www.furk.net'
        self.meta_search_link = "/api/plugins/metasearch?api_key=%s&q=%s&cached=yes&match=%s&moderated=%s%s&sort=relevance&type=video&offset=0&limit=%s"
        self.tfile_link = "/api/file/get?api_key=%s&t_files=1&id=%s"
        self.login_link = "/api/login/login?login=%s&pwd=%s"
        self.user_name = control.addon('plugin.video.nine').getSetting('furk.user_name')
        self.user_pass = control.addon('plugin.video.nine').getSetting('furk.user_pass')
        self.api_key = control.addon('plugin.video.nine').getSetting('furk.api')
        self.search_limit = control.addon('plugin.video.nine').getSetting('furk.limit')
        self.files = []
        self.aliases = []

    def get_api(self):

        try:

            api_key = self.api_key

            if api_key == '':
                if self.user_name == '' or self.user_pass == '':
                    return

                else:
                    s = requests.Session()
                    link = (self.base_link + self.login_link % (self.user_name, self.user_pass))
                    p = s.post(link).json()

                    if p['status'] == 'ok':
                        api_key = p['api_key']
                        control.addon('plugin.video.nine').setSetting('furk.api', api_key)
                    else:
                        pass

            return api_key

        except:
            log_utils.log('Furk API', 1)
            pass

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = {'imdb': imdb, 'title': title, 'year': year}
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            self.aliases.extend(aliases)
            url = tvshowtitle
            return url
        except:
            pass

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            url = {'tvshowtitle': url, 'season': season, 'episode': episode}
            return url
        except:
            pass

    def sources(self, url, hostDict, hostprDict):

        api_key = self.get_api()

        if not api_key:
            return

        sources = []

        try:

            content_type = 'episode' if 'tvshowtitle' in url else 'movie'
            match = 'extended'
            moderated = 'no' if content_type == 'episode' else 'yes'
            search_in = ''

            if content_type == 'movie':
                title = url['title']
                year = url['year']
                link = '@name+%s+%s+@files+%s+%s' % (title, year, title, year)

            elif content_type == 'episode':
                title = url['tvshowtitle']
                season = int(url['season'])
                episode = int(url['episode'])
                link = self.makeQuery(title, season, episode)

            s = requests.Session()
            link = self.base_link + self.meta_search_link % (api_key, link, match, moderated, search_in, self.search_limit)

            p = s.get(link).json()

            if p['status'] != 'ok':
                return

            files = p['files']

            for i in files:
                if i['is_ready'] == '1' and i['type'] == 'video':
                    try:
                        file_name = cleantitle.get_title(i['name'])
                        if not source_utils.is_match(file_name, title, aliases=self.aliases):
                            continue
                        source = 'SINGLE'
                        if int(i['files_num_video']) > 3:
                            source = 'PACK (x%02d)' % int(i['files_num_video'])
                        file_size = i['size']
                        file_id = i['id']
                        file_dl = i['url_dl']
                        if content_type == 'episode':
                            url = '%s<>%s<>%s' % (file_id, season, episode)
                        else:
                            url = '%s<>%s<>%s+%s' % (file_id, 'movie', title, year)

                        quality, info = source_utils.get_release_quality(file_name, file_dl)
                        try:
                            dsize = float(file_size) / 1073741824
                            isize = '%.2f GB' % dsize
                        except:
                            dsize, isize = 0.0, ''
                        info.insert(0, isize)
                        info = ' | '.join(info)

                        sources.append({'source': source,
                                        'quality': quality,
                                        'language': "en",
                                        'url': url,
                                        'info': info,
                                        'direct': True,
                                        'debridonly': True,
                                        'size': dsize,
                                        'name': file_name})
                    except:
                        pass

                else:
                    continue

            return sources

        except:
            log_utils.log('Furk sources', 1)
            pass

    def resolve(self, url):

        try:

            info = url.split('<>')
            file_id = info[0]

            self.content_type = 'movie' if info[1] == 'movie' else 'episode'

            if self.content_type == 'episode': self.filtering_list = self.seasEpQueryList(info[1], info[2])

            link = (self.base_link + self.tfile_link % (self.api_key, file_id))
            s = requests.Session()
            p = s.get(link).json()

            if p['status'] != 'ok' or p['found_files'] != '1':
                return

            files = p['files'][0]
            files = files['t_files']

            for i in files:
                if 'video' not in i['ct']:
                    pass
                else: self.files.append(i)

            url = self.managePack()

            return url

        except:
            log_utils.log('Furk resolve', 1)
            pass

    def managePack(self):

        for i in self.files:
            name = i['name']
            if self.content_type == 'movie':
                if 'is_largest' in i:
                    url = i['url_dl']
            else:
                if 'furk320' not in name.lower() and 'sample' not in name.lower():
                    for x in self.filtering_list:
                        if x in name.lower():
                            url = i['url_dl']
                        else:
                            pass
        return url

    def makeQuery(self, title, season, episode):
        seasEpList = self.seasEpQueryList(season, episode)
        return '@name+%s+@files+%s+|+%s+|+%s' % (title, seasEpList[0], seasEpList[1], seasEpList[2])

    def seasEpQueryList(self, season, episode):
        return ['s%02de%02d' % (int(season), int(episode)), '%dx%02d' % (int(season), int(episode)),
                '%02dx%02d' % (int(season), int(episode))]

