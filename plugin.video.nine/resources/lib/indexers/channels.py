# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    ///Updated for Nine///

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
"""


from resources.lib.modules import api_keys
from resources.lib.modules import bookmarks
from resources.lib.modules import playcount
from resources.lib.modules import log_utils
from resources.lib.modules import cleangenre
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import workers
from resources.lib.modules import trakt
from resources.lib.modules import utils

import sys, re, datetime
import simplejson as json

import requests
import six
from six.moves import urllib_parse


params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')


class channels:
    def __init__(self):
        self.list = [] ; self.items = []

        self.uk_datetime = self.uk_datetime()
        self.systime = (self.uk_datetime).strftime('%Y%m%d%H%M%S%f')
        self.lang = control.apiLanguage()['tmdb']
        self.settingFanart = control.setting('fanart')
        self.hq_artwork = control.setting('hq.artwork') or 'false'
        self.trailer_source = control.setting('trailer.source') or '2'

        self.sky_now_link = 'https://epgservices.sky.com/5.1.1/api/2.0/channel/json/%s/now/nn/3'
        # self.sky_programme_link = 'http://tv.sky.com/programme/channel/%s/%s/%s.json'

        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.fanart_tv_headers = {'api-key': api_keys.fanarttv_key}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})
        self.lang = control.apiLanguage()['tmdb']

        self.tm_user = control.setting('tm.user') or api_keys.tmdb_key
        self.tmdb_api_link = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,external_ids' % ('%s', self.tm_user, self.lang)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'
        self.related_link = 'https://api.themoviedb.org/3/movie/%s/similar?api_key=%s&page=1' % ('%s', self.tm_user)
        # self.related_link = 'https://api.trakt.tv/movies/%s/related'

        self.session = requests.Session()


    def __del__(self):
        self.session.close()


    def uk_datetime(self):
        dt = datetime.datetime.utcnow() + datetime.timedelta(hours = 0)
        d = datetime.datetime(dt.year, 4, 1)
        dston = d - datetime.timedelta(days=d.weekday() + 1)
        d = datetime.datetime(dt.year, 11, 1)
        dstoff = d - datetime.timedelta(days=d.weekday() + 1)
        if dston <=  dt < dstoff:
            return dt + datetime.timedelta(hours = 1)
        else:
            return dt


    def get(self):
        channels = [
            ('ActionWomen', '1811'), ('ActionWomen HD', '4020'),
            ('Christmas 24', '4420'), ('Christmas 24+', '4421'),
            ('Film4', '1627'), ('Film4 HD', '4044'), ('Film4+', '1629'),
            ('Horror Channel', '3605'), ('Horror Channel+', '4502'),
            ('ROK', '3542'),
            ('Sky Action', '1001'), ('Sky Action HD', '4014'),
            ('Sky Christmas', '1816'), ('Sky Christmas HD', '4016'),
            ('Sky Comedy', '1002'), ('Sky Comedy HD', '4019'),
            ('Sky Family', '1808'), ('Sky Family HD', '4018'),
            ('Sky Greats', '1815'), ('Sky Greats HD', '4015'),
            ('Sky Hits', '1814'), ('Sky Hits HD', '4033'),
            ('Sky Premiere', '1409'), ('Sky Premiere HD', '4021'), ('Sky Premiere+', '1823'),
            ('Sky ScFi/Horror', '1807'), ('Sky ScFi/Horror HD', '4017'),
            ('Sky Thriller', '1818'), ('Sky Thriller HD', '4062'),
            ('Sony Action', '3708'), ('Sony Action+', '3721'),
            ('Sony Christmas', '3643'), ('Sony Christmas+', '3751'),
            ('Sony Movies', '3709'), ('Sony Movies+', '3771'),
            ('TalkingPictures', '5252'),
            ('TCM Movies', '5605'), ('TCM Movies+', '5275')
        ]

        threads = []
        for i in channels: threads.append(workers.Thread(self.sky_list, i[0], i[1]))
        [i.start() for i in threads]
        [i.join() for i in threads]
        del threads

        self_items = []
        filtered_items = set()

        for t, y, c, r in self.items:
           if not t in filtered_items:
              filtered_items.add(t)
              self_items.append((t, y, c, r))

        threads = []
        for i in range(0, len(self_items)): threads.append(workers.Thread(self.items_list, self_items[i]))
        [i.start() for i in threads]
        [i.join() for i in threads]
        del threads

        self.list = sorted(self.list, key=lambda k: k['channel'].lower())

        self.channelDirectory(self.list)
        return self.list


    def sky_list(self, channel, id):
        try:
            url = self.sky_now_link % id
            r = self.session.get(url, timeout=10)
            r.raise_for_status()
            r.encoding = 'utf-8'
            result = r.json() if six.PY3 else utils.json_loads_as_str(r.text)
            result = result['listings'][id][0]

            try:
                year = result['d']
                year = re.findall('[(](\d{4})[)]', year)[0].strip()
            except:
                year = ''

            title = result['t']
            title = title.replace('(%s)' % year, '').strip()

            try:
                rated = result['m'][4]
            except:
                rated = '0'
            if rated == 'PG': pass
            elif rated == 'U': rated = 'G'
            elif '12' in rated: rated = 'PG-13'
            elif rated == '15': rated = 'R'
            elif '18' in rated: rated = 'NC-17'
            else: rated = '0'

            self.items.append((title, year, channel, rated))
        except:
            pass


    def items_list(self, i):
        try:
            trakt_item = trakt.SearchAll(i[0], i[1], False)[0]

            content = trakt_item.get('movie')
            if not content: content = trakt_item.get('show')
            #log_utils.log('content: ' + repr(content))

            _title = content.get('title')
            _title = client.replaceHTMLCodes(_title)
            if not _title: _title = i[0]

            _year = content.get('year', 0)
            _year = re.sub('[^0-9]', '', str(_year))
            if not _year or _year == '0': _year = i[1]

            imdb = content.get('ids', {}).get('imdb')
            if imdb: imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))
            else: imdb = '0'

            tmdb = str(content.get('ids', {}).get('tmdb', 0))

            id = tmdb if not tmdb == '0' else imdb
            if id == '0': raise Exception()

            en_url = self.tmdb_api_link % (id)
            f_url = en_url + ',translations'
            url = en_url if self.lang == 'en' else f_url
            #log_utils.log('tmdb_url: ' + url)

            r = self.session.get(url, timeout=10)
            r.raise_for_status()
            r.encoding = 'utf-8'
            item = r.json() if six.PY3 else utils.json_loads_as_str(r.text)
            #log_utils.log('tmdb_item: ' + repr(item))

            if imdb == '0':
                try:
                    imdb = item['external_ids']['imdb_id']
                    if not imdb: imdb = '0'
                except:
                    pass

            original_language = item.get('original_language', '')

            if self.lang == 'en':
                en_trans_item = None
            else:
                try:
                    translations = item['translations']['translations']
                    en_trans_item = [x['data'] for x in translations if x['iso_639_1'] == 'en'][0]
                except:
                    en_trans_item = {}

            name = item.get('title', '')
            original_name = item.get('original_title', '')
            en_trans_name = en_trans_item.get('title', '') if not self.lang == 'en' else None
            #log_utils.log('self_lang: %s | original_language: %s | _title: %s | name: %s | original_name: %s | en_trans_name: %s' % (self.lang, original_language, _title, name, original_name, en_trans_name))

            if self.lang == 'en':
                title = label = name
            else:
                title = en_trans_name or original_name
                if original_language == self.lang:
                    label = name
                else:
                    label = en_trans_name or name
            if not title: title = _title
            if not label: label = _title

            plot = item.get('overview', '') or '0'

            tagline = item.get('tagline', '') or '0'

            if not self.lang == 'en':
                if plot == '0':
                    en_plot = en_trans_item.get('overview', '')
                    if en_plot: plot = en_plot

                if tagline == '0':
                    en_tagline = en_trans_item.get('tagline', '')
                    if en_tagline: tagline = en_tagline

            premiered = item.get('release_date', '') or '0'

            try: year = re.findall('(\d{4})', premiered)[0]
            except: year = ''
            if not year : year = _year

            status = item.get('status', '') or '0'

            try: studio = item['production_companies'][0]['name']
            except: studio = ''
            if not studio: studio = '0'

            try:
                genres = item['genres']
                genres = [d['name'] for d in genres]
                genre = ' / '.join(genres)
            except:
                genre = ''
            if not genre: genre = '0'

            try:
                countries = item['production_countries']
                countries = [c['name'] for c in countries]
                country = ' / '.join(countries)
            except:
                country = ''
            if not country: country = '0'

            duration = str(item.get('runtime', 0)) or '0'

            rating = str(item.get('vote_average', '')) or '0'
            votes = item.get('vote_count', '') or '0'

            castwiththumb = []
            try:
                c = item['credits']['cast'][:30]
                for person in c:
                    _icon = person['profile_path']
                    icon = self.tm_img_link % ('185', _icon) if _icon else ''
                    castwiththumb.append({'name': person['name'], 'role': person['character'], 'thumbnail': icon})
            except:
                pass
            if not castwiththumb: castwiththumb = '0'

            try:
                crew = item['credits']['crew']
                director = ', '.join([d['name'] for d in [x for x in crew if x['job'] == 'Director']])
                writer = ', '.join([w['name'] for w in [y for y in crew if y['job'] in ['Writer', 'Screenplay', 'Author', 'Novel']]])
            except:
                director = writer = '0'

            poster_path = item.get('poster_path')
            if poster_path:
                poster1 = self.tm_img_link % ('500', poster_path)
            else:
                poster1 = '0'

            fanart_path = item.get('backdrop_path')
            if fanart_path:
                fanart1 = self.tm_img_link % ('1280', fanart_path)
            else:
                fanart1 = '0'

            poster2 = fanart2 = None
            banner = clearlogo = clearart = landscape = discart = '0'
            if self.hq_artwork == 'true' and not imdb == '0':# and not self.fanart_tv_user == '':

                try:
                    #if self.fanart_tv_user == '': raise Exception()
                    r2 = self.session.get(self.fanart_tv_art_link % imdb, headers=self.fanart_tv_headers, timeout=10)
                    r2.raise_for_status()
                    r2.encoding = 'utf-8'
                    art = r2.json() if six.PY3 else utils.json_loads_as_str(r2.text)

                    try:
                        _poster2 = art['movieposter']
                        _poster2 = [x for x in _poster2 if x.get('lang') == self.lang][::-1] + [x for x in _poster2 if x.get('lang') == 'en'][::-1] + [x for x in _poster2 if x.get('lang') in ['00', '']][::-1]
                        _poster2 = _poster2[0]['url']
                        if _poster2: poster2 = _poster2
                    except:
                        pass

                    try:
                        if 'moviebackground' in art: _fanart2 = art['moviebackground']
                        else: _fanart2 = art['moviethumb']
                        _fanart2 = [x for x in _fanart2 if x.get('lang') == self.lang][::-1] + [x for x in _fanart2 if x.get('lang') == 'en'][::-1] + [x for x in _fanart2 if x.get('lang') in ['00', '']][::-1]
                        _fanart2 = _fanart2[0]['url']
                        if _fanart2: fanart2 = _fanart2
                    except:
                        pass

                    try:
                        _banner = art['moviebanner']
                        _banner = [x for x in _banner if x.get('lang') == self.lang][::-1] + [x for x in _banner if x.get('lang') == 'en'][::-1] + [x for x in _banner if x.get('lang') in ['00', '']][::-1]
                        _banner = _banner[0]['url']
                        if _banner: banner = _banner
                    except:
                        pass

                    try:
                        if 'hdmovielogo' in art: _clearlogo = art['hdmovielogo']
                        else: _clearlogo = art['clearlogo']
                        _clearlogo = [x for x in _clearlogo if x.get('lang') == self.lang][::-1] + [x for x in _clearlogo if x.get('lang') == 'en'][::-1] + [x for x in _clearlogo if x.get('lang') in ['00', '']][::-1]
                        _clearlogo = _clearlogo[0]['url']
                        if _clearlogo: clearlogo = _clearlogo
                    except:
                        pass

                    try:
                        if 'hdmovieclearart' in art: _clearart = art['hdmovieclearart']
                        else: _clearart = art['clearart']
                        _clearart = [x for x in _clearart if x.get('lang') == self.lang][::-1] + [x for x in _clearart if x.get('lang') == 'en'][::-1] + [x for x in _clearart if x.get('lang') in ['00', '']][::-1]
                        _clearart = _clearart[0]['url']
                        if _clearart: clearart = _clearart
                    except:
                        pass

                    try:
                        if 'moviethumb' in art: _landscape = art['moviethumb']
                        else: _landscape = art['moviebackground']
                        _landscape = [x for x in _landscape if x.get('lang') == self.lang][::-1] + [x for x in _landscape if x.get('lang') == 'en'][::-1] + [x for x in _landscape if x.get('lang') in ['00', '']][::-1]
                        _landscape = _landscape[0]['url']
                        if _landscape: landscape = _landscape
                    except:
                        pass

                    try:
                        if 'moviedisc' in art: _discart = art['moviedisc']
                        _discart = [x for x in _discart if x.get('lang') == self.lang][::-1] + [x for x in _discart if x.get('lang') == 'en'][::-1] + [x for x in _discart if x.get('lang') in ['00', '']][::-1]
                        _discart = _discart[0]['url']
                        if _discart: discart = _discart
                    except:
                        pass
                except:
                    #log_utils.log('fanart.tv art fail', 1)
                    pass

            poster = poster2 or poster1
            fanart = fanart2 or fanart1
            #log_utils.log('title: ' + title + ' - poster: ' + repr(poster))

            self.list.append({'title': title, 'originaltitle': title, 'label': label, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'banner': banner, 'fanart': fanart,
                    'clearlogo': clearlogo, 'clearart': clearart, 'landscape': landscape, 'discart': discart, 'premiered': premiered, 'genre': genre, 'duration': duration,
                    'director': director, 'writer': writer, 'castwiththumb': castwiththumb, 'plot': plot, 'tagline': tagline, 'status': status, 'studio': studio, 'country': country,
                    'rating': rating, 'votes': votes, 'channel': i[2], 'mpaa': i[3]})
        except:
            pass


    def channelDirectory(self, items):
        if items == None or len(items) == 0: return #control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart = control.addonFanart()

        traktCredentials = trakt.getTraktCredentialsInfo()

        kodiVersion = control.getKodiVersion()

        isPlayable = True if not 'plugin' in control.infoLabel('Container.PluginName') else False

        indicators = playcount.getMovieIndicators(refresh=True) if action == 'movies' else playcount.getMovieIndicators()

        if self.trailer_source == '0': trailerAction = 'tmdb_trailer'
        elif self.trailer_source == '1': trailerAction = 'yt_trailer'
        else: trailerAction = 'imdb_trailer'


        playbackMenu = control.lang(32063) if control.setting('hosts.mode') == '2' else control.lang(32064)

        watchedMenu = control.lang(32068) if trakt.getTraktIndicatorsInfo() == True else control.lang(32066)

        unwatchedMenu = control.lang(32069) if trakt.getTraktIndicatorsInfo() == True else control.lang(32067)

        queueMenu = control.lang(32065)

        traktManagerMenu = control.lang(32070)

        nextMenu = control.lang(32053)

        addToLibrary = control.lang(32551)

        clearProviders = control.lang(32081)

        findSimilar = control.lang(32100)

        infoMenu = control.lang(32101)

        for i in items:
            try:
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                label = i['label'] if 'label' in i and not i['label'] == '0' else title
                label = '%s (%s)' % (label, year)
                if 'channel' in i: label = '[B]%s[/B] : %s' % (i['channel'].upper(), label)

                status = i['status'] if 'status' in i else '0'

                sysname = urllib_parse.quote_plus('%s (%s)' % (title, year))
                systitle = urllib_parse.quote_plus(title)

                meta = dict((k,v) for k, v in six.iteritems(i) if not v == '0')
                meta.update({'imdbnumber': imdb, 'code': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=%s&name=%s&tmdb=%s&imdb=%s' % (sysaddon, trailerAction, systitle, tmdb, imdb)})
                if not 'duration' in i: meta.update({'duration': '120'})
                elif i['duration'] == '0': meta.update({'duration': '120'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass
                if 'castwiththumb' in i and not i['castwiththumb'] == '0': meta.pop('cast', '0')

                poster = i['poster'] if 'poster' in i and not i['poster'] == '0' else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib_parse.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib_parse.quote_plus(url)

                #path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)

                cm = []

                cm.append((findSimilar, 'Container.Update(%s?action=movies&url=%s)' % (sysaddon, urllib_parse.quote_plus(self.related_link % tmdb))))

                cm.append(('[I]Cast[/I]', 'RunPlugin(%s?action=moviecredits&tmdb=%s&status=%s)' % (sysaddon, tmdb, status)))

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if kodiVersion < 17:
                    cm.append((infoMenu, 'Action(Info)'))

                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))

                cm.append(('[I]Scrape Filterless[/I]', 'RunPlugin(%s?action=playUnfiltered&title=%s&year=%s&imdb=%s&meta=%s&t=%s)' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)))

                cm.append((clearProviders, 'RunPlugin(%s?action=clearCacheProviders)' % sysaddon))

                try: item = control.item(label=label, offscreen=True)
                except: item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                fanart = i['fanart'] if 'fanart' in i and not i['fanart'] == '0' else addonFanart

                if self.settingFanart == 'true':
                    art.update({'fanart': fanart})
                else:
                    art.update({'fanart': addonFanart})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})

                if 'landscape' in i and not i['landscape'] == '0':
                    landscape = i['landscape']
                else:
                    landscape = fanart
                art.update({'landscape': landscape})

                if 'discart' in i and not i['discart'] == '0':
                    art.update({'discart': i['discart']})

                item.setArt(art)
                item.addContextMenuItems(cm)
                if isPlayable:
                    item.setProperty('IsPlayable', 'true')

                castwiththumb = i.get('castwiththumb')
                if castwiththumb and not castwiththumb == '0':
                    if kodiVersion >= 18:
                        item.setCast(castwiththumb)
                    else:
                        cast = [(p['name'], p['role']) for p in castwiththumb]
                        meta.update({'cast': cast})

                offset = bookmarks.get('movie', imdb, '', '', True)
                if float(offset) > 120:
                    percentPlayed = int(float(offset) / float(meta['duration']) * 100)
                    item.setProperty('resumetime', str(offset))
                    item.setProperty('percentplayed', str(percentPlayed))

                item.setProperty('imdb_id', imdb)
                item.setProperty('tmdb_id', tmdb)
                try: item.setUniqueIDs({'imdb': imdb, 'tmdb': tmdb})
                except: pass

                item.setInfo(type='Video', infoLabels = control.metadataClean(meta))

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                log_utils.log('channels_dir', 1)
                pass

        control.content(syshandle, 'files')
        control.directory(syshandle, cacheToDisc=True)

