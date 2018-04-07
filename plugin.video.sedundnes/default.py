# -*- coding: utf-8 -*-

################################################################################
#(_)                                                                           #
# |_________________________________________                                   #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|      If your going to copy       #
# | *  *  *  *  *|==========================|         this addon just          #
# |*  *  *  *  * |##########################|         give credit!!!!          #
# |--------------|==========================|                                  #
# |#########################################|                                  #
# |=========================================|                                  #
# |#########################################|                                  #
# |=========================================|            seduNdneS             #
# |#########################################|                                  #
# |-----------------------------------------|                                  #
# |                                                                            #
# |    Not Sure Add-on                                                         #
# |    Copyright (C) 2016 Exodus                                               #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################


import urlparse,sys,re,xbmc

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

action = params.get('action')

name = params.get('name')

title = params.get('title')

year = params.get('year')

imdb = params.get('imdb')

tvdb = params.get('tvdb')

season = params.get('season')

episode = params.get('episode')

tvshowtitle = params.get('tvshowtitle')

premiered = params.get('premiered')

url = params.get('url')

image = params.get('image')

meta = params.get('meta')

select = params.get('select')

query = params.get('query')

source = params.get('source')

content = params.get('content')


if action == None:
    from resources.lib.indexers import snstreams
    snstreams.indexer().root()

elif action == 'message':
    from resources.lib.modules import notify
    notify.message(url)
elif action == 'faq':
    from resources.lib.modules import notify
    notify.faq(url)
elif action == 'private':
    from resources.lib.indexers import snstreams
    snstreams.indexer().pmode()
elif action == 'directory':
    from resources.lib.indexers import snstreams
    snstreams.indexer().get(url)

elif action == 'qdirectory':
    from resources.lib.indexers import snstreams
    snstreams.indexer().getq(url)

elif action == 'xdirectory':
    from resources.lib.indexers import snstreams
    snstreams.indexer().getx(url)

elif action == 'developer':
    from resources.lib.indexers import snstreams
    snstreams.indexer().developer()

elif action == 'tvtuner':
    from resources.lib.indexers import snstreams
    snstreams.indexer().tvtuner(url)

elif 'youtube' in str(action):
    from resources.lib.indexers import snstreams
    snstreams.indexer().youtube(url, action)

elif action == 'play1':
    from resources.lib.indexers import snstreams
    snstreams.player().play(url, content)

elif action == 'browser':
    from resources.lib.indexers import snstreams
    snstreams.resolver().browser(url)

elif action == 'search':
    from resources.lib.indexers import snstreams
    snstreams.indexer().search(url=None)

elif action == 'addSearch':
    from resources.lib.indexers import snstreams
    snstreams.indexer().addSearch(url)

elif action == 'delSearch':
    from resources.lib.indexers import snstreams
    snstreams.indexer().delSearch()

elif action == 'queueItem':
    from resources.lib.modules import control
    control.queueItem()

elif action == 'openSettings':
    from resources.lib.modules import control
    control.openSettings()


elif action == 'urlresolverSettings':
    from resources.lib.modules import control
    control.openSettings(id='script.module.urlresolver')

elif action == 'addView':
    from resources.lib.modules import views
    views.addView(content)

elif action == 'downloader':
    from resources.lib.modules import downloader
    downloader.downloader()

elif action == 'addDownload':
    from resources.lib.modules import downloader
    downloader.addDownload(name,url,image)

elif action == 'removeDownload':
    from resources.lib.modules import downloader
    downloader.removeDownload(url)

elif action == 'startDownload':
    from resources.lib.modules import downloader
    downloader.startDownload()

elif action == 'startDownloadThread':
    from resources.lib.modules import downloader
    downloader.startDownloadThread()

elif action == 'stopDownload':
    from resources.lib.modules import downloader
    downloader.stopDownload()

elif action == 'statusDownload':
    from resources.lib.modules import downloader
    downloader.statusDownload()

elif action == 'trailer':
    from resources.lib.modules import trailer
    trailer.trailer().play(name)

elif action == 'clearCache1':
    from resources.lib.modules import cache
    cache.clear()

elif action == 'radios':
    from resources.lib.indexers import snradios
    snradios.radios()

elif action == 'radioResolve':
    from resources.lib.indexers import snradios
    snradios.radioResolve(url)

elif action == 'radio1fm':
    from resources.lib.indexers import snradios
    snradios.radio1fm()

elif action == 'radio181fm':
    from resources.lib.indexers import snradios
    snradios.radio181fm()

elif action == 'radiocast':
    from resources.lib.indexers import snradios
    snradios.kickinradio()

elif action == 'kickinradiocats':
    from resources.lib.indexers import snradios
    snradios.kickinradiocats(url)

elif action == 'sntoons.root' or action == 'cartoon':
    from resources.lib.indexers import sntoons
    sntoons.indexer().root()

elif action == 'sntoons.cartoons':
    from resources.lib.indexers import sntoons
    sntoons.indexer().cartoons(url)

elif action == 'sntoons.cartoongenres':
    from resources.lib.indexers import sntoons
    sntoons.indexer().cartoongenres()

elif action == 'sntoons.cartoonstreams':
    from resources.lib.indexers import sntoons
    sntoons.indexer().cartoonstreams(url, image, fanart)

elif action == 'sntoons.cartoonplay':
    from resources.lib.indexers import sntoons
    sntoons.indexer().cartoonplay(url)

elif action == 'sntoons.anime':
    from resources.lib.indexers import sntoons
    sntoons.indexer().anime(url)

elif action == 'sntoons.animegenres':
    from resources.lib.indexers import sntoons
    sntoons.indexer().animegenres()

elif action == 'sntoons.animestreams':
    from resources.lib.indexers import sntoons
    sntoons.indexer().animestreams(url, image, fanart)

elif action == 'sntoons.animeplay':
    from resources.lib.indexers import sntoons
    sntoons.indexer().animeplay(url)
	
elif action == 'traktManager':
    from resources.lib.modules import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.modules import trakt
    trakt.authTrakt()
	
elif action == 'ScraperSettings':
    from resources.lib.modules import control
    control.openSettings(id='script.module.nanscrapers')
elif action == 'ResolverSettings':
    from resources.lib.modules import control
    control.openSettings(id='script.mrknow.urlresolver')
elif action == "realdebridauth":
    from resources.lib.addon import debrid
    debrid.rdAuthorize()

######################IMDB SCRAPER#################################


if action == None:
    from resources.lib.indexers import navigator
    navigator.navigator().root()

elif action == 'movieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies()

elif action == 'movieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().movies(lite=True)

elif action == 'mymovieNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies()

elif action == 'mymovieliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mymovies(lite=True)

elif action == 'tvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows()

elif action == 'tvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tvshows(lite=True)

elif action == 'mytvNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows()

elif action == 'mytvliteNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().mytvshows(lite=True)

elif action == 'downloadNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().downloads()

elif action == 'toolNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().tools()

elif action == 'searchNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().search()

elif action == 'viewsNavigator':
    from resources.lib.indexers import navigator
    navigator.navigator().views()

elif action == 'clearCache':
    from resources.lib.indexers import navigator
    navigator.navigator().clearCache()

elif action == 'infoCheck':
    from resources.lib.indexers import navigator
    navigator.navigator().infoCheck('')

elif action == 'movies':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'moviePage':
    from resources.lib.indexers import movies
    movies.movies().get(url)

elif action == 'movieWidget':
    from resources.lib.indexers import movies
    movies.movies().widget()

elif action == 'movieSearch':
    from resources.lib.indexers import movies
    movies.movies().search()

elif action == 'moviePerson':
    from resources.lib.indexers import movies
    movies.movies().person()

elif action == 'movieGenres':
    from resources.lib.indexers import movies
    movies.movies().genres()

elif action == 'movieLanguages':
    from resources.lib.indexers import movies
    movies.movies().languages()

elif action == 'movieCertificates':
    from resources.lib.indexers import movies
    movies.movies().certifications()

elif action == 'movieYears':
    from resources.lib.indexers import movies
    movies.movies().years()

elif action == 'moviePersons':
    from resources.lib.indexers import movies
    movies.movies().persons(url)

elif action == 'movieUserlists':
    from resources.lib.indexers import movies
    movies.movies().userlists()

elif action == 'tvshows':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

################################################################################
#(_)                                                                           #
# |_________________________________________                                   #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|      If your going to copy       #
# | *  *  *  *  *|==========================|         this addon just          #
# |*  *  *  *  * |##########################|         give credit!!!!          #
# |--------------|==========================|                                  #
# |#########################################|                                  #
# |=========================================|                                  #
# |#########################################|                                  #
# |=========================================|            seduNdneS             #
# |#########################################|                                  #
# |-----------------------------------------|                                  #
# |                                                                            #
# |    Not Sure Add-on                                                         #
# |    Copyright (C) 2016 Exodus                                               #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################

elif action == 'tvshowPage':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().get(url)

elif action == 'tvSearch':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().search()

elif action == 'tvPerson':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().person()

elif action == 'tvGenres':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().genres()

elif action == 'tvNetworks':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().networks()

elif action == 'tvLanguages':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().languages()

elif action == 'tvCertificates':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().certifications()

elif action == 'tvPersons':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().persons(url)

elif action == 'tvUserlists':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().userlists()

elif action == 'seasons':
    from resources.lib.indexers import episodes
    episodes.seasons().get(tvshowtitle, year, imdb, tvdb)

elif action == 'episodes':
    from resources.lib.indexers import episodes
    episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, episode)

elif action == 'calendar':
    from resources.lib.indexers import episodes
    episodes.episodes().calendar(url)

elif action == 'tvWidget':
    from resources.lib.indexers import episodes
    episodes.episodes().widget()

elif action == 'calendars':
    from resources.lib.indexers import episodes
    episodes.episodes().calendars()

elif action == 'episodeUserlists':
    from resources.lib.indexers import episodes
    episodes.episodes().userlists()

elif action == 'refresh':
    from resources.lib.addon import control
    control.refresh()

elif action == 'queueItem':
    from resources.lib.addon import control
    control.queueItem()

#elif action == 'openSettings':
#    from resources.lib.addon import control
#   control.openSettings(query)

elif action == 'artwork':
    from resources.lib.addon import control
    control.artwork()

elif action == 'addView':
    from resources.lib.addon import views
    views.addView(content)

elif action == 'moviePlaycount':
    from resources.lib.addon import playcount
    playcount.movies(imdb, query)

elif action == 'episodePlaycount':
    from resources.lib.addon import playcount
    playcount.episodes(imdb, tvdb, season, episode, query)

elif action == 'tvPlaycount':
    from resources.lib.addon import playcount
    playcount.tvshows(name, imdb, tvdb, season, query)

elif action == 'Mkeywords':
    from resources.lib.indexers import movies
    movies.movies().keywords()

elif action == 'TVkeywords':
    from resources.lib.indexers import tvshows
    tvshows.tvshows().keywords()

elif action == 'sortby':
    from resources.lib.indexers import navigator
    navigator.navigator().sortby()

elif action == 'useramount':
    from resources.lib.indexers import navigator
    navigator.navigator().listamount()

elif action == 'trailer':
    from resources.lib.addon import trailer
    trailer.trailer().play(name, url)

elif action == 'traktManager':
    from resources.lib.addon import trakt
    trakt.manager(name, imdb, tvdb, content)

elif action == 'authTrakt':
    from resources.lib.addon import trakt
    trakt.authTrakt()

elif action == 'smuSettings':
    try: import urlresolver
    except: pass
    urlresolver.display_settings()

elif action == 'download':
    import json
    from resources.lib.addon import sources
    from resources.lib.addon import downloader
    try: downloader.download(name, image, sources.sources().sourcesResolve(json.loads(source)[0], True))
    except: pass

elif action == 'play':
    from resources.lib.addon import sources
    sources.sources().play(title, year, imdb, tvdb, season, episode, tvshowtitle, premiered, meta, select)

elif action == 'addItem':
    from resources.lib.addon import sources
    sources.sources().addItem(title)

elif action == 'playItem':
    from resources.lib.addon import sources
    sources.sources().playItem(title, source)

elif action == 'alterSources':
    from resources.lib.addon import sources
    sources.sources().alterSources(url, meta)

elif action == 'clearSources':
    from resources.lib.addon import sources
    sources.sources().clearSources()

elif action == 'random':
    rtype = params.get('rtype')
    if rtype == 'movie':
        from resources.lib.indexers import movies
        rlist = movies.movies().get(url, create_directory=False)
        r = sys.argv[0]+"?action=play1"
    elif rtype == 'episode':
        from resources.lib.indexers import episodes
        rlist = episodes.episodes().get(tvshowtitle, year, imdb, tvdb, season, create_directory=False)
        r = sys.argv[0]+"?action=play1"
    elif rtype == 'season':
        from resources.lib.indexers import episodes
        rlist = episodes.seasons().get(tvshowtitle, year, imdb, tvdb, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=episode"
    elif rtype == 'show':
        from resources.lib.indexers import tvshows
        rlist = tvshows.tvshows().get(url, create_directory=False)
        r = sys.argv[0]+"?action=random&rtype=season"
    from resources.lib.addon import control
    from random import randint
    import json
    try:
        rand = randint(1,len(rlist))-1
        for p in ['title','year','imdb','tvdb','season','episode','tvshowtitle','premiered','select']:
            if rtype == "show" and p == "tvshowtitle":
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand]['title'])
                except: pass
            else:
                try: r += '&'+p+'='+urllib.quote_plus(rlist[rand][p])
                except: pass
        try: r += '&meta='+urllib.quote_plus(json.dumps(rlist[rand]))
        except: r += '&meta='+urllib.quote_plus("{}")
        if rtype == "movie":
            try: control.infoDialog(rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        elif rtype == "episode":
            try: control.infoDialog(rlist[rand]['tvshowtitle']+" - Season "+rlist[rand]['season']+" - "+rlist[rand]['title'], control.lang(32536).encode('utf-8'), time=30000)
            except: pass
        control.execute('RunPlugin(%s)' % r)
    except:
        control.infoDialog(control.lang(32537).encode('utf-8'), time=8000)
		
elif action == 'movieToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().add(name, title, year, imdb, tmdb)

elif action == 'moviesToLibrary':
    from resources.lib.modules import libtools
    libtools.libmovies().range(url)

elif action == 'tvshowToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().add(tvshowtitle, year, imdb, tvdb)

elif action == 'tvshowsToLibrary':
    from resources.lib.modules import libtools
    libtools.libtvshows().range(url)

elif action == 'updateLibrary':
    from resources.lib.modules import libtools
    libtools.libepisodes().update(query)

elif action == 'service':
    from resources.lib.modules import libtools
    libtools.libepisodes().service()
		
else:
    if 'search' in action:
        url = action.split('search=')[1]
        url = url + '|SECTION|'
        from resources.lib.indexers import snstreams
        snstreams.indexer().search(url)
    else: quit()
################################################################################
#(_)                                                                           #
# |_________________________________________                                   #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|      If your going to copy       #
# | *  *  *  *  *|==========================|         this addon just          #
# |*  *  *  *  * |##########################|         give credit!!!!          #
# |--------------|==========================|                                  #
# |#########################################|                                  #
# |=========================================|                                  #
# |#########################################|                                  #
# |=========================================|            seduNdneS             #
# |#########################################|                                  #
# |-----------------------------------------|                                  #
# |                                                                            #
# |    Not Sure Add-on                                                         #
# |    Copyright (C) 2017 FTG                                                  #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################