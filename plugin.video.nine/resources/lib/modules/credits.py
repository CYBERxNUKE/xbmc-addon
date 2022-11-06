# -*- coding: utf-8 -*-

"""
    Nine Add-on
"""


import sys
import os
import six
from six.moves import urllib_parse

from resources.lib.modules import api_keys
from resources.lib.modules import cache
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils
from resources.lib.modules import utils


class Credits:
    def __init__(self):
        self.tm_user = control.setting('tm.user') or api_keys.tmdb_key
        self.tmdb_tv_credits = 'https://api.themoviedb.org/3/tv/%s/aggregate_credits?api_key=%s' % ('%s', self.tm_user)
        self.tmdb_movie_credits = 'https://api.themoviedb.org/3/movie/%s/credits?api_key=%s' % ('%s', self.tm_user)
        self.tmdb_tvpeople_link = 'https://api.themoviedb.org/3/person/%s/tv_credits?api_key=%s' % ('%s', self.tm_user)
        self.tmdb_moviepeople_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&sort_by=primary_release_date.desc&with_cast=%s&include_adult=false&include_video=false&page=1' % (self.tm_user, '%s')
        self.tmdb_moviedirector_link = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&sort_by=primary_release_date.desc&with_crew=%s&include_adult=false&include_video=false&page=1' % (self.tm_user, '%s')
        #self.tmdb_moviepeople_link = 'https://api.themoviedb.org/3/person/%s/movie_credits?api_key=%s' % ('%s', self.tm_user)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w185%s'
        self.fallback_img = os.path.join(control.artPath(), 'person.png')
        self.bio_link = 'https://api.themoviedb.org/3/person/%s?api_key=%s' % ('%s', self.tm_user)

    def get_tv(self, tmdb, status):
        try:
            if not tmdb or tmdb == '0':
                return control.infoDialog('No ID found')

            sysaddon = sys.argv[0]
            cache_dur = 720 if status in ['Ended', 'Canceled'] else 96

            url = self.tmdb_tv_credits % tmdb
            r = cache.get(client.request, cache_dur, url)
            r = utils.json_loads_as_str(r)

            c = r['cast'][:50]
            ids = [str(i['id']) for i in c]
            names = [i['name'] for i in c]

            items = []

            for person in c:
                role = person['roles'][0]['character']
                name = '%s [I](as %s)[/I]' % (person['name'], role) if role else person['name']

                if control.getKodiVersion() >= 17:
                    icon = self.tm_img_link % person['profile_path'] if person['profile_path'] else self.fallback_img
                    item = control.item(label=name)
                    item.setArt({'icon': icon, 'thumb': icon, 'poster': icon})
                    items.append(item)
                else:
                    items.append(name)

            select = control.selectDialog(items, heading='Actors:', useDetails=True)
            if select == -1: return
            c_id = ids[select]
            c_name = names[select]
            choose = control.selectDialog(['TV Shows appeared in', 'Movies appeared in', 'Biography'], heading=c_name)
            if choose == -1: return
            elif choose == 0:
                control.execute('Container.Update(%s?action=tvshows&url=%s)' % (sysaddon, urllib_parse.quote_plus(self.tmdb_tvpeople_link % c_id)))
            elif choose == 1:
                control.execute('Container.Update(%s?action=movies&url=%s)' % (sysaddon, urllib_parse.quote_plus(self.tmdb_moviepeople_link % c_id)))
            elif choose == 2:
                self.bio_txt(c_id)
        except:
            log_utils.log('get_tv credits', 1)
            return


    def get_movies(self, tmdb, status):
        try:
            if not tmdb or tmdb == '0':
                return control.infoDialog('No ID found')

            sysaddon = sys.argv[0]
            cache_dur = 720 if status in ['Released', 'Canceled'] else 96

            url = self.tmdb_movie_credits % tmdb
            r = cache.get(client.request, cache_dur, url)
            r = utils.json_loads_as_str(r)

            crew = r['crew']
            crew_cast = [d for d in crew if d['job'] == 'Director']
            crew_cast += r['cast'][:50]

            ids = [str(i['id']) for i in crew_cast]
            names = [' '.join((i['name'], i.get('job', ''))) for i in crew_cast]

            items = []

            for person in crew_cast:
                role = person['character'] if 'character' in person else person['job']
                name = '%s [I](as %s)[/I]' % (person['name'], role) if role else person['name']
                name = name.replace('as Director', 'Director')

                if control.getKodiVersion() >= 17:
                    icon = self.tm_img_link % person['profile_path'] if person['profile_path'] else self.fallback_img
                    item = control.item(label=name)
                    item.setArt({'icon': icon, 'thumb': icon, 'poster': icon})
                    items.append(item)
                else:
                    items.append(name)

            select = control.selectDialog(items, heading='Actors / Director(s):', useDetails=True)
            if select == -1: return
            c_id = ids[select]
            c_name = names[select]
            if 'Director' in c_name:
                choose = control.selectDialog(['Movies credited in', 'Biography'], heading=c_name.replace(' Director', ''))
                if choose == -1: return
                elif choose == 0:
                    control.execute('Container.Update(%s?action=movies&url=%s)' % (sysaddon, urllib_parse.quote_plus(self.tmdb_moviedirector_link % c_id)))
                elif choose == 1:
                    self.bio_txt(c_id)
            else:
                choose = control.selectDialog(['Movies appeared in', 'TV Shows appeared in', 'Biography'], heading=c_name)
                if choose == -1: return
                elif choose == 0:
                    control.execute('Container.Update(%s?action=movies&url=%s)' % (sysaddon, urllib_parse.quote_plus(self.tmdb_moviepeople_link % c_id)))
                elif choose == 1:
                    control.execute('Container.Update(%s?action=tvshows&url=%s)' % (sysaddon, urllib_parse.quote_plus(self.tmdb_tvpeople_link % c_id)))
                elif choose == 2:
                    self.bio_txt(c_id)
        except:
            log_utils.log('get_movies credits', 1)
            return


    def bio_txt(self, id):
        try:
            url = self.bio_link % id
            r = cache.get(client.request, 168, url)
            r = utils.json_loads_as_str(r)
            txt = '[B]Born:[/B] {0}[CR]{1}[CR]{2}'.format(r['birthday'] or 'N/A', '[B]Died:[/B] {}[CR]'.format(r['deathday']) if r['deathday'] else '', r['biography'] or '[B]Biography:[/B] N/A')
            control.textViewer(text=txt, heading=r['name'], monofont=False)
        except:
            log_utils.log('bio_txt', 1)
            return




