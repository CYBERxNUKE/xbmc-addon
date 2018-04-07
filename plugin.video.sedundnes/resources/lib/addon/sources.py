'''
    
    Copyright (C) 2016 Midraal

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

import sys,pkgutil,re,json,urllib,urlparse,random,datetime,time
import os
from threading import Event
import xbmc
import xbmcaddon
import xbmcvfs
import nanscrapers

from resources.lib.addon import dialogs
from resources.lib.addon import control
from resources.lib.addon import cleantitle
from resources.lib.addon import client
from resources.lib.addon import debrid
from resources.lib.addon import workers
from resources.lib.addon import unshorten

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

try: import urlresolver
except: pass

try: import xbmc
except: pass

debridstatus = control.setting('debridsources')

_shst_regex = ['sh.st','viid.me']

def cleantitle_get(title):
    if title == None: return
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&')
    title = re.sub(r'\<[^>]*\>','', title)
    title = re.sub('\n|([[].+?[]])|([(].+?[)])|\s(vs|v[.])\s|(:|;|-|"|,|\'|\_|\.|\?)|\(|\)|\[|\]|\{|\}|\s', '', title).lower()
    return title

class sources:
    def __init__(self):
        self.getConstants()
        self.sources = []

    def play(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None

            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)

            select = control.setting('hosts.mode') if select == None else select

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem&title=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8'))))

                    url = self.sourcesDirect(items)


            if url == None:
                return self.errorForSources()

            meta = json.loads(meta)

            from resources.lib.addon.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass

    def play_alter(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta):
        try:
            url = None
            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)
            if control.setting('hosts.mode') == '2': select = "1"
            else: select = "2"

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem&title=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8'))))

                    url = self.sourcesDirect(items)

            if url == None:
                return self.errorForSources()

            meta = json.loads(meta)

            from resources.lib.addon.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass

    def play_dialog(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None

            items = self.getSource_dialog(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)
            title = tvshowtitle if not tvshowtitle == None else title
            header = control.addonInfo('name')
            header2 = header.upper()
            try: meta = json.loads(meta)
            except: meta = ''
            progressDialog = control.progressDialog
            progressDialog.create(header, '')
            progressDialog.update(0)
            filter = []

            for i in range(len(items)):

                try:
                    try:

                        label = '[B]%s[/B] | %s | [B][I]%s [/I][/B]' % (items[i]['scraper'], items[i]['source'], items[i]['quality'])

                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), label.upper(), '')
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), label.upper())

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)

                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]

                    if self.url == None: raise Exception()

                    try: progressDialog.close()
                    except: pass

                    control.sleep(200)
                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')

                    from resources.lib.addon.player import player
                    player().run(title, year, season, episode, imdb, tvdb, self.url, meta)

                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

            self.errorForSources()
        except:
            pass

    def play_library(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select):
        try:
            url = None


            items = self.getSources(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered)

            select = control.setting('hosts.mode') if select == None else select

            title = tvshowtitle if not tvshowtitle == None else title

            if control.window.getProperty('PseudoTVRunning') == 'True':
                return control.resolve(int(sys.argv[1]), True, control.item(path=str(self.sourcesDirect(items))))

            if len(items) > 0:

                if select == '1' and 'plugin' in control.infoLabel('Container.PluginName'):
                    control.window.clearProperty(self.itemProperty)
                    control.window.setProperty(self.itemProperty, json.dumps(items))

                    control.window.clearProperty(self.metaProperty)
                    control.window.setProperty(self.metaProperty, meta)

                    control.sleep(200)

                    return control.execute('Container.Update(%s?action=addItem&title=%s)' % (sys.argv[0], urllib.quote_plus(title.encode('utf-8'))))

                elif select == '0' or select == '1':
                    url = self.sourcesDialog(items)

                else:
                    url = self.sourcesDirect(items)


            if url == None:
                return self.errorForSources()

            meta = 'play_library'

            from resources.lib.addon.player import player
            player().run(title, year, season, episode, imdb, tvdb, url, meta)
        except:
            pass


    def addItem(self, title):
        control.playlist.clear()

        items = control.window.getProperty(self.itemProperty)
        items = json.loads(items)

        if items == None or len(items) == 0: control.idle() ; sys.exit()

        meta = control.window.getProperty(self.metaProperty)
        meta = json.loads(meta)

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        downloads = True if control.setting('downloads') == 'true' and not (control.setting('movie.download.path') == '' or control.setting('tv.download.path') == '') else False


        if 'tvshowtitle' in meta and 'season' in meta and 'episode' in meta:
            name = '%s S%02dE%02d' % (title, int(meta['season']), int(meta['episode']))
        elif 'year' in meta:
            name = '%s (%s)' % (title, meta['year'])
        else:
            name = title

        systitle = urllib.quote_plus(title.encode('utf-8'))

        sysname = urllib.quote_plus(name.encode('utf-8'))


        poster = meta['poster'] if 'poster' in meta else '0'
        banner = meta['banner'] if 'banner' in meta else '0'
        thumb = meta['thumb'] if 'thumb' in meta else poster
        fanart = meta['fanart'] if 'fanart' in meta else '0'

        if poster == '0': poster = control.addonPoster()
        if banner == '0' and poster == '0': banner = control.addonBanner()
        elif banner == '0': banner = poster
        if thumb == '0' and fanart == '0': thumb = control.addonFanart()
        elif thumb == '0': thumb = fanart
        if control.setting('fanart') == 'true' and not fanart == '0': pass
        else: fanart = control.addonFanart()

        sysimage = urllib.quote_plus(poster.encode('utf-8'))

        downloadMenu = control.lang(32403).encode('utf-8')


        for i in range(len(items)):
            try:
                label = items[i]['label']

                syssource = urllib.quote_plus(json.dumps([items[i]]))

                sysurl = '%s?action=playItem&title=%s&source=%s' % (sysaddon, systitle, syssource)

                cm = []

                if downloads == True:
                    cm.append((downloadMenu, 'RunPlugin(%s?action=download&name=%s&image=%s&source=%s)' % (sysaddon, sysname, sysimage, syssource)))

                item = control.item(label=label)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': poster, 'tvshow.poster': poster, 'season.poster': poster, 'banner': banner, 'tvshow.banner': banner, 'season.banner': banner})

                if not fanart == None: item.setProperty('Fanart_Image', fanart)

                item.addContextMenuItems(cm)
                item.setInfo(type='Video', infoLabels = meta)

                control.addItem(handle=syshandle, url=sysurl, listitem=item, isFolder=False)
            except:
                pass

        control.content(syshandle, 'files')
        control.directory(syshandle, cacheToDisc=True)


    def playItem(self, title, source):
        try:
            meta = control.window.getProperty(self.metaProperty)
            meta = json.loads(meta)

            year = meta['year'] if 'year' in meta else None
            season = meta['season'] if 'season' in meta else None
            episode = meta['episode'] if 'episode' in meta else None

            imdb = meta['imdb'] if 'imdb' in meta else None
            tvdb = meta['tvdb'] if 'tvdb' in meta else None

            next = [] ; prev = [] ; total = []

            for i in range(1,1000):
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    next.append(u)
                except:
                    break
            for i in range(-1000,0)[::-1]:
                try:
                    u = control.infoLabel('ListItem(%s).FolderPath' % str(i))
                    if u in total: raise Exception()
                    total.append(u)
                    u = dict(urlparse.parse_qsl(u.replace('?','')))
                    u = json.loads(u['source'])[0]
                    prev.append(u)
                except:
                    break

            items = json.loads(source)
            items = [i for i in items+next+prev][:40]

            header = control.addonInfo('name')
            header2 = header.upper()

            progressDialog = control.progressDialog
            progressDialog.create(header, '')
            progressDialog.update(0)

            block = None

            for i in range(len(items)):
                try:
                    try:
                        if progressDialog.iscanceled(): break
                        progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
                    except:
                        progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

                    if items[i]['source'] == block: raise Exception()

                    w = workers.Thread(self.sourcesResolve, items[i])
                    w.start()

                    m = ''

                    for x in range(3600):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        k = control.condVisibility('Window.IsActive(virtualkeyboard)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        k = control.condVisibility('Window.IsActive(yesnoDialog)')
                        if k: m += '1'; m = m[-1]
                        if (w.is_alive() == False or x > 30) and not k: break
                        time.sleep(0.5)


                    for x in range(30):
                        try:
                            if xbmc.abortRequested == True: return sys.exit()
                            if progressDialog.iscanceled(): return progressDialog.close()
                        except:
                            pass

                        if m == '': break
                        if w.is_alive() == False: break
                        time.sleep(0.5)


                    if w.is_alive() == True: block = items[i]['source']

                    if self.url == None: raise Exception()

                    try: progressDialog.close()
                    except: pass

                    control.sleep(200)
                    control.execute('Dialog.Close(virtualkeyboard)')
                    control.execute('Dialog.Close(yesnoDialog)')

                    from resources.lib.addon.player import player
                    player().run(title, year, season, episode, imdb, tvdb, self.url, meta)

                    return self.url
                except:
                    pass

            try: progressDialog.close()
            except: pass

            self.errorForSources()
        except:
            pass


    def getSources(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, presetDict=[], timeout=30):
        progressDialog = control.progressDialog
        progressDialog.create(control.addonInfo('name'), '')
        progressDialog.update(0, 'Warming Up Scrapers...')

        content = 'movie' if tvshowtitle is None else 'episode'
        try:
            timeout = int(control.setting('scrapers.timeout.1'))
        except:
            pass
        allow_debrid = control.setting("allow_debrid") == "true"
        if control.setting('cachesources') == 'true':
                        control.makeFile(control.dataPath)
                        self.sourceFile = control.providercacheFile

        if content == 'movie':
            title = self.getTitle(title)
            scraper = nanscrapers.scrape_movie
            links_scraper = scraper(title,year,imdb,timeout=timeout,enable_debrid=allow_debrid)
        else:
            tvshowtitle = self.getTitle(tvshowtitle)
            scraper = nanscrapers.scrape_episode
            links_scraper = scraper(tvshowtitle,year,premiered,season,episode,imdb,tvdb,timeout=timeout,enable_debrid=allow_debrid)
        thread = workers.Thread(self.get_nan_sources, links_scraper, progressDialog)

        thread.start()
        for i in range(0, timeout * 2):
            try:
                if xbmc.abortRequested:
                    return sys.exit()
                try:
                    if progressDialog.iscanceled():
                        break
                except:
                    pass
                if not thread.is_alive(): break
                time.sleep(0.5)
            except:
                pass

        try:
            progressDialog.close()
        except:
            pass

        self.sourcesFilter()

        return self.sources

    def get_nan_sources(self, links_scraper, progressDialog):
        num_scrapers = len(nanscrapers.relevant_scrapers())
        index = 0
        string1 = control.lang(32406).encode('utf-8')
        counthd = 0
        count1080 = 0
        countSD = 0
        for scraper_links in links_scraper():
                try:
                    if xbmc.abortRequested:
                        return sys.exit()
                    if progressDialog.iscanceled():
                        break

                    index = index + 1
                    percent = int((index * 100) / num_scrapers)
                    if scraper_links is not None:
                        random.shuffle(scraper_links)
                    for scraper_link in scraper_links:
                        try:
                                q = scraper_link['quality']
                                if "1080" in q:
                                    count1080 += 1
                                elif "HD" in q:
                                    counthd += 1
                                elif "720" in q:
                                    counthd += 1
                                    scraper_link["quality"] = "HD"
                                elif "720" in q:
                                    counthd += 1
                                    scraper_link["quality"] = "HD"
                                elif "560" in q:
                                    counthd += 1
                                    scraper_link["quality"] = "HD"
                                else:
                                    countSD += 1
                        except:
                            pass

                        progressDialog.update(percent,"Links Found:" "(" + str(len(self.sources)) + ")", string1 % (num_scrapers - index))
                        self.sources.append(scraper_link)

                        try:
                            if progressDialog.iscanceled():
                                break
                        except:
                            pass
                except:
                    pass

    def prepareSources(self):
        try:
            control.makeFile(control.dataPath)

            self.sourceFile = control.providercacheFile
        except:
            pass



    def getTitle(self, title):
        title = cleantitle.normalize(title)
        return title


    def getMovieSource(self, title, year, imdb, source, call):
        source = cleantitle_get(str(source))
        type = "movie"

        try:
            url = None
            if url == None: url = call.movie(imdb, title, year)
            if url == None: raise Exception()
        except:
            pass

        try:
            sources = []
            sources = call.sources(url, self.hostDict, self.hostprDict)
            if sources == None: raise Exception()
            self.sources.extend(sources)
        except:
            pass


    def getEpisodeSource(self, title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, source, call):

        source = cleantitle_get(str(source))
        try:
            url = None
            if url == None: url = call.tvshow(imdb, tvdb, tvshowtitle, year)
            if url == None: raise Exception()
        except:
            pass
        try:
            ep_url = None
            if url == None: raise Exception()
            if ep_url == None: ep_url = call.episode(url, imdb, tvdb, title, premiered, season, episode)
            if ep_url == None: raise Exception()
        except:
            pass

        try:
            sources = []
            sources = call.sources(ep_url, self.hostDict, self.hostprDict)
            if sources == None: raise Exception()
            self.sources.extend(sources)
        except:
            pass

    def getURISource(self, url):
        try:
            sourceDict = []
            for package, name, is_pkg in pkgutil.walk_packages(__path__): sourceDict.append((name, is_pkg))
            sourceDict = [i[0] for i in sourceDict if i[1] == False]
            sourceDict = [(i, __import__(i, globals(), locals(), [], -1).source()) for i in sourceDict]

            domain = (urlparse.urlparse(url).netloc).lower()

            domains = [(i[0], i[1].domains) for i in sourceDict]
            domains = [i[0] for i in domains if any(x in domain for x in i[1])]

            if len(domains) == 0: return False

            call = [i[1] for i in sourceDict if i[0] == domains[0]][0]

            self.sources = call.sources(url, self.hostDict, self.hostprDict)

            for i in range(len(self.sources)):
                try: self.sources[i]['autoplay'] = True
                except: pass

            self.sources = self.sourcesFilter()
            return self.sources
        except:
            pass


    def clearSources(self):
        try:
            control.idle()

            yes = control.yesnoDialog(control.lang(32407).encode('utf-8'), '', '')
            if not yes: return

            control.makeFile(control.dataPath)
            dbcon = database.connect(control.providercacheFile)
            dbcur = dbcon.cursor()
            dbcur.execute("DROP TABLE IF EXISTS rel_src")
            dbcur.execute("VACUUM")
            dbcon.commit()

            control.infoDialog(control.lang(32408).encode('utf-8'), sound=True, icon='INFO')
        except:
            pass

    def sourcesFilter(self):
        provider = control.setting('hosts.sort.provider')

        quality = control.setting('hosts.quality')
        if quality == '':
            quality = '0'

        captcha = control.setting('hosts.captcha')

        random.shuffle(self.sources)

        if provider == 'true':
            self.sources = sorted(self.sources, key=lambda k: k['scraper'])

        local = [i for i in self.sources if 'local' in i and i.get('local', False) == True]
        self.sources = [i for i in self.sources if not i in local]

        filter = []

        filter += [i for i in self.sources if i['direct'] == True]
        filter += [i for i in self.sources if i['direct'] == False]
        self.sources = filter

        filter = []
        filter += [i for i in self.sources if not i['source'].lower() in self.hostBlackList]

        self.sources = filter

        filter = []
        filter += local
        if quality in ['0']: filter += [i for i in self.sources if i['quality'] == '4k' and i.get('debridonly', False) == True]
        if quality in ['0']: filter += [i for i in self.sources if i['quality'] == '4k'  and i.get('debridonly', False) == False]

        if quality in ['0', '1']: filter += [i for i in self.sources if i['quality'] == '2k' and i.get('debridonly', False) == True]
        if quality in ['0', '1']: filter += [i for i in self.sources if i['quality'] == '2k'  and i.get('debridonly', False) == False]

        if quality in ['0' ,'1', '2']: filter += [i for i in self.sources if i['quality'] == '1080p' and i.get('debridonly', False) == True]
        if quality in ['0', '1', '2']: filter += [i for i in self.sources if i['quality'] == '1080p'  and i.get('debridonly', False) == False]
        if quality in ['0', '1', '2', '3']: filter += [i for i in self.sources if i['quality'] == 'HD' and i.get('debridonly', False) == True]
        if quality in ['0', '1', '2', '3']: filter += [i for i in self.sources if i['quality'] == 'HD' and i.get('debridonly', False) == False]
        filter += [i for i in self.sources if i['quality'] == 'SD' and i.get('debridonly', False) == True]
        filter += [i for i in self.sources if i['quality'] == 'SD' and i.get('debridonly', False) == False]

        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'SCR']
        if len(filter) < 10: filter += [i for i in self.sources if i['quality'] == 'CAM']
        self.sources = filter

        if not captcha == 'true':
            filter = [i for i in self.sources if i['source'].lower() in self.hostcapDict and not 'debrid' in i]
            self.sources = [i for i in self.sources if not i in filter]
        self.sources = self.filter_zips(self.sources)

        self.sources = self.sources[:1000]

        for i in range(len(self.sources)):
            u = self.sources[i]['url']
            s = self.sources[i]['scraper'].lower()
            s = s.rsplit('.', 1)[0]
            p = self.sources[i]['source']
            d = self.sources[i].get('debridonly', False)
            d = str(d)
            p = re.sub('v\d*$', '', p)

            q = self.sources[i]['quality']
            try:
                f = (' | '.join(['[I]%s [/I]' % info.strip() for info in self.sources[i]['info'].split('|')]))
            except:
                f = ''

            if d == 'True':
                label = '%02d |[I]DEB[/I] | [B]%s[/B] | ' % (int(i+1), p)
            else:
                label = '%02d | [B]%s[/B] | ' % (int(i+1), p)

            if q in ['4K', '2k', '1080p', 'HD']:
                label += '%s | %s | [B][I]%s [/I][/B]' % (s, f, q)
            elif q == 'SD':
                label += '%s | %s | [I]%s [/I]' % (s, f, q)
            else:
                label += '%s | %s | [I]%s [/I]' % (s, f, q)
            label = label.replace('| 0 |', '|').replace(' | [I]0 [/I]', '')
            label = label.replace('[I]HEVC [/I]', 'HEVC')
            label = re.sub('\[I\]\s+\[/I\]', ' ', label)
            label = re.sub('\|\s+\|', '|', label)
            label = re.sub('\|(?:\s+|)$', '', label)

            self.sources[i]['label'] = label.upper()

        return self.sources



    def filter_zips(self, sources):
                filtered = []
                for item in sources:
                        url = item['url'].encode('utf-8')
                        if "google" in url.lower():
                                filtered.append(item)
                        else:
                                if not any(value in url.lower() for value in self.blacklist_zips):
                                        filtered.append(item)
                return filtered

    def sourcesResolve(self, item, info=False):
        try:
            self.url = None
            u = url = item['url']
            direct = item['direct']
            provider = item['scraper'].lower()
            u = url = item["url"]

            if url == None: raise Exception()
            if any(value in url for value in _shst_regex): u = unshorten._unshorten_shst(url)

            if not direct == True:

                                if not debridstatus == 'true': hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=False)
                                else: hmf = urlresolver.HostedMediaFile(url=u, include_disabled=True, include_universal=True)
                                if hmf.valid_url() == True: url = hmf.resolve()

            if url == False or url == None: raise Exception()

            ext = url.split('?')[0].split('&')[0].split('|')[0].rsplit('.')[-1].replace('/', '').lower()
            if ext == 'rar': raise Exception()

            try: headers = url.rsplit('|', 1)[1]
            except: headers = ''
            headers = urllib.quote_plus(headers).replace('%3D', '=') if ' ' in headers else headers
            headers = dict(urlparse.parse_qsl(headers))

            xbmc.log("url3:" + repr(url), xbmc.LOGNOTICE)


            if url.startswith('http') and '.m3u8' in url:
                result = client.request(url.split('|')[0], headers=headers, output='geturl', timeout='20')
                if result == None: raise Exception()

            elif url.startswith('http'):
                result = client.request(url.split('|')[0], headers=headers, output='chunk', timeout='30')
                if result == None: raise Exception()

            else:
                raise Exception()

            xbmc.log("url4:" + repr(url), xbmc.LOGNOTICE)


            self.url = url
            xbmc.log("url2:" + repr(url), xbmc.LOGNOTICE)
            return url
        except:
            if info == True: self.errorForSources()
            return

    def sourcesDirect(self, items):
        items = [i for i in items]

        if control.setting('autoplay.sd') == 'true':
                        items = [i for i in items if not i['quality'] in ['4K', '2k', '1080p', 'HD']]

        u = None

        header = control.addonInfo('name')
        header2 = header.upper()

        try:
            control.sleep(1000)

            progressDialog = control.progressDialog
            progressDialog.create(header, '')
            progressDialog.update(0)
        except:
            pass

        for i in range(len(items)):
            try:
                if progressDialog.iscanceled(): break
                progressDialog.update(int((100 / float(len(items))) * i), str(items[i]['label']), str(' '))
            except:
                progressDialog.update(int((100 / float(len(items))) * i), str(header2), str(items[i]['label']))

            try:
                if xbmc.abortRequested == True: return sys.exit()

                url = self.sourcesResolve(items[i])
                if u == None: u = url
                if not url == None: break
            except:
                pass

        try: progressDialog.close()
        except: pass

        return u


    def errorForSources(self):
        control.infoDialog(control.lang(32401).encode('utf-8'), sound=False, icon='INFO')


    def getConstants(self):
        self.itemProperty = 'plugin.video.sedundnes.container.items'

        self.metaProperty = 'plugin.video.sedundnes.container.meta'

        try:
            self.hostDict = urlresolver.relevant_resolvers(order_matters=True)
            self.hostDict = [i.domains for i in self.hostDict if not '*' in i.domains]
            self.hostDict = [i.lower() for i in reduce(lambda x, y: x+y, self.hostDict)]
            self.hostDict = [x for y,x in enumerate(self.hostDict) if x not in self.hostDict[:y]]
        except:
            self.hostDict = []

        self.hostBlackList = ['youtube.com','uploading.site',
                'uploadkadeh.ir','uploadkadeh.com','adf.ly','indishare.me','rlsbb.com','nfo.rlsbb.com','bankupload.com','katfile.com','userboard.org','multiup.org','hitfile.net','letitbit.net','pastebin.com','myvideolinks.userboard.org','arabloads.net','multiup','uppit.com','4upld.com',
                'bdupload.org', 'bdupload.info','ziifile.com','bytewhale.com','go4up.com','file.rocks', 'mylinkgen.com']

        self.hostmyDict = ['uploadrocket.net','userscloud','alfafile','.avi','.mkv','.mov','.mp4','.xvid','.divx','oboom', 'rapidgator', 'rg.to',  'uploaded', 'ul.to', 'filefactory', 'nitroflare', 'turbobit', '1fichier','uptobox', '1fich', 'uploadrocket','uploading','hugefiles', 'uploaded' , 'clicknupload']
        self.hostprDict = self.hostDict + self.hostmyDict
        self.hostcapDict = ['hugefiles.net', 'kingfiles.net', 'openload.io', 'openload.co', 'oload.tv', 'thevideo.me', 'vidup.me', 'streamin.to', 'torba.se']
        self.blacklist_zips = ['.zip', '.rar', '.jpeg', '.img', '.jpg', '.RAR', '.ZIP', '.png' , '.sub', '.srt']

        self.hostblockDict = []

        self.debridDict = debrid.debridDict()

    @staticmethod
    def sort_function(item):
        """
        transform items quality into a string that's sort-able
        Args:
            item: scraper link
        Returns:
            sortable quality string
        """
        if 'quality' in item[1][0]:
            quality = item[1][0]["quality"]
        else:
            quality = item[1][0]["path"]["quality"]
        if quality.startswith("1080"):quality = "HDa"
        elif quality.startswith("720"):quality = "HDb"
        elif quality.startswith("560"):quality = "HDc"
        elif quality == "DVD":quality = "HDd"
        elif quality == "HD":quality = "HDe"
        elif quality.startswith("480"):quality = "SDa"
        elif quality.startswith("360"):quality = "SDb"
        elif quality.startswith("SD"):quality = "SDc"
        return quality
