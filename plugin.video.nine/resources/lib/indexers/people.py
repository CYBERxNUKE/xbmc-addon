# -*- coding: utf-8 -*-

"""
    Nine Add-on
"""


from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import log_utils
from resources.lib.indexers import navigator

import os, sys, re

try: from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

import six
from six.moves import urllib_parse


params = dict(urllib_parse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')


class People:
    def __init__(self):
        self.list = []

        self.items_per_page = str(control.setting('items.per.page')) or '20'

        self.personlist_link = 'https://www.imdb.com/search/name?gender=male,female&count=50&start=1'
        self.person_search_link = 'https://www.imdb.com/search/name?count=50&name='
        self.person_movie_link = 'https://www.imdb.com/search/title?title_type=movie,short,tvMovie&production_status=released&role=%s&sort=year,desc&count=%s&start=1' % ('%s', self.items_per_page)
        self.person_tv_link = 'https://www.imdb.com/search/title?title_type=tvSeries,tvMiniSeries&release_date=,date[0]&role=%s&sort=year,desc&count=%s&start=1' % ('%s', self.items_per_page)
        self.bio_link = 'https://www.imdb.com/name/%s/bio'


    def persons(self, url=None, content=''):
        if not url:
            url = self.personlist_link
        self.list = cache.get(self.imdb_person_list, 24, url)
        self.addDirectory(self.list, content)
        return self.list


    def search(self, content=''):
        navigator.navigator().addDirectoryItem(32603, 'peopleSearchnew&content=%s' % content, 'people-search.png', 'DefaultMovies.png')

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()

        try:
            dbcur.executescript("CREATE TABLE IF NOT EXISTS people (ID Integer PRIMARY KEY AUTOINCREMENT, term);")
        except:
            pass

        dbcur.execute("SELECT * FROM people ORDER BY ID DESC")
        lst = []

        delete_option = False
        for (id, term) in dbcur.fetchall():
            if term not in str(lst):
                delete_option = True
                navigator.navigator().addDirectoryItem(term.title(), 'peopleSearchterm&name=%s&content=%s' % (term, content), 'people-search.png', 'DefaultMovies.png')
                lst += [(term)]
        dbcur.close()

        if delete_option:
            navigator.navigator().addDirectoryItem(32605, 'clearCacheSearch&select=people', 'tools.png', 'DefaultAddonProgram.png')

        navigator.navigator().endDirectory(False)


    def search_new(self, content):
        control.idle()

        t = control.lang(32010)
        k = control.keyboard('', t)
        k.doModal()
        q = k.getText() if k.isConfirmed() else None

        if not q: return
        q = q.lower()

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM people WHERE term = ?", (q,))
        dbcur.execute("INSERT INTO people VALUES (?,?)", (None,q))
        dbcon.commit()
        dbcur.close()
        url = self.person_search_link + urllib_parse.quote_plus(q)
        self.persons(url, content=content)


    def search_term(self, q, content):
        control.idle()
        q = q.lower()

        dbcon = database.connect(control.searchFile)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM people WHERE term = ?", (q,))
        dbcur.execute("INSERT INTO people VALUES (?,?)", (None, q))
        dbcon.commit()
        dbcur.close()
        url = self.person_search_link + urllib_parse.quote_plus(q)
        self.persons(url, content=content)


    def bio_txt(self, url, name):
        url = self.bio_link % url
        r = cache.get(client.request, 168, url)

        try: born = client.parseDOM(r, 'time', ret='datetime')[0]
        except: born = ''
        try: died = client.parseDOM(r, 'time', ret='datetime')[1]
        except: died = ''

        try:
            bio = client.parseDOM(r, 'div', attrs={'class': r'soda odd'})[0]
            bio = client.parseDOM(bio, 'p')[0]
            bio = client.replaceHTMLCodes(bio)
            bio = six.ensure_str(bio, errors='ignore')
            bio = bio.replace('<br />', '[CR]')
            bio = re.sub(r'<.*?>', '', bio)
        except:
            bio = ''

        txt = '[B]Born:[/B] {0}[CR]{1}[CR]{2}'.format(born or 'N/A', '[B]Died:[/B] {}[CR]'.format(died) if died else '', bio or '[B]Biography:[/B] N/A')
        control.textViewer(text=txt, heading=name, monofont=False)


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs={'class': '.+?etail'})
        except:
            return

        try:
            result = result.replace(r'"class=".*?ister-page-nex', '" class="lister-page-nex')
            next = client.parseDOM(result, 'a', ret='href', attrs={'class': r'.*?ister-page-nex.*?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs={'class': u'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urllib_parse.urlparse(url).query, urllib_parse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = six.ensure_str(next, errors='ignore')
        except:
            next = ''

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = six.ensure_str(name, errors='ignore')

                id = client.parseDOM(item, 'a', ret='href')[0]
                id = re.findall(r'(nm\d*)', id, re.I)[0]
                id = client.replaceHTMLCodes(id)
                id = six.ensure_str(id, errors='replace')

                try:
                    image = client.parseDOM(item, 'img', ret='src')[0]
                    image = re.sub(r'(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                    image = client.replaceHTMLCodes(image)
                    image = six.ensure_str(image, errors='replace')
                    if '/sash/' in image or '/nopicture/' in image: raise Exception()
                except:
                    image = 'person.png'

                try:
                    info = client.parseDOM(item, 'p')
                    info = '[I]%s[/I][CR]%s' % (info[0].split('<')[0].strip(), info[1])
                    info = client.replaceHTMLCodes(info)
                    info = six.ensure_str(info, errors='ignore')
                    info = re.sub(r'<.*?>', '', info)
                except:
                    info = ''

                self.list.append({'name': name, 'id': id, 'image': image, 'plot': info, 'next': next})
            except:
                pass

        return self.list


    def getPeople(self, name, url):
        try:
            select = control.selectDialog(['Movies', 'TV Shows', 'Biography'], heading=name)
            if select == -1: return
            elif select == 0:
                from resources.lib.indexers import movies
                movies.movies().get(self.person_movie_link % url)
            elif select == 1:
                from resources.lib.indexers import tvshows
                tvshows.tvshows().get(self.person_tv_link % url)
            elif select == 2:
                self.bio_txt(url, name)
        except:
            log_utils.log('getPeople', 1)
            pass


    def addDirectory(self, items, content):
        if items == None or len(items) == 0: return #control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        playRandom = control.lang(32535)

        nextMenu = control.lang(32053)

        for i in items:
            try:
                name = i['name']

                plot = i['plot'] or '[CR]'

                if i['image'].startswith('http'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                try: item = control.item(label=name, offscreen=True)
                except: item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb, 'poster': thumb, 'fanart': addonFanart})
                item.setInfo(type='video', infoLabels={'plot': plot})

                cm = []

                if content == 'movies':
                    link = urllib_parse.quote_plus(self.person_movie_link % i['id'])
                    cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, link)))
                    url = '%s?action=movies&url=%s' % (sysaddon, link)
                elif content == 'tvshows':
                    link = urllib_parse.quote_plus(self.person_tv_link % i['id'])
                    cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=show&url=%s)' % (sysaddon, link)))
                    url = '%s?action=tvshows&url=%s' % (sysaddon, link)
                else:
                    url = '%s?action=personsSelect&name=%s&url=%s' % (sysaddon, urllib_parse.quote_plus(name), urllib_parse.quote_plus(i['id']))

                if cm:
                    item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                log_utils.log('people_dir', 1)
                pass

        try:
            next = items[0]['next']
            if next == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=persons&url=%s&content=%s' % (sysaddon, urllib_parse.quote_plus(next), content)

            try: item = control.item(label=nextMenu, offscreen=True)
            except: item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon, 'fanart': addonFanart})
            item.setProperty('SpecialSort', 'bottom')

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, '')
        control.directory(syshandle, cacheToDisc=True)

