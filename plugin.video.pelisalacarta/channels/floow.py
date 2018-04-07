# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (cinefoxtv) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys, time

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools
from core import tmdb
from core import jsontools

host = 'http://floow.tv'
token = ''
key = '73894672jdjhjdddddfhd'

tgenero = {"Comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
           "Belica":"https://s32.postimg.org/kjbko3xhx/belica.png",
           "Drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
           "Accion":"https://s32.postimg.org/4hp7gwh9x/accion.png",
           "Aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
           "Latino":"https://s29.postimg.org/wmykp66ev/latino.png",
           "Animacion":"https://s32.postimg.org/rbo1kypj9/animacion.png",
           "Ciencia-Fic":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
           "Terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
           "Docu":"https://s32.postimg.org/7opmvc5ut/documental.png",
           "Musical":"https://s31.postimg.org/7i32lca7f/musical.png",
           "Western":"https://s31.postimg.org/nsksyt3hn/western.png",
           "Fantasia":"https://s32.postimg.org/pklrf01id/fantasia.png",
           "Thriller":"https://s31.postimg.org/4d7bl25y3/thriller.png",
           "Misterio":"https://s4.postimg.org/kd48bcxe5/misterio.png",
           "Crimen":"https://s14.postimg.org/5lez1j1gx/crimen.png",
           "Historia":"https://s13.postimg.org/52evvjrqf/historia.png",
           "Infantil":"https://s32.postimg.org/i53zwwgsl/infantil.png",
           "Biografia":"https://s23.postimg.org/u49p87o3f/biografia.png",
           "Noir":"https://s32.postimg.org/b0882kt7p/cine_negro.png",
           "Romantico":"https://s30.postimg.org/4i5sbj7n5/romantica.png",
           "Deporte":"https://s31.postimg.org/pdc8etc0r/deporte.png",
           "Anime":"https://s31.postimg.org/lppob54d7/anime.png",
           "Concierto":"https://s22.postimg.org/5ew6k8ls1/concierto.png"}

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Peliculas", action="menupeliculas",thumbnail='https://s31.postimg.org/4g4lytrqj/peliculas.png', fanart='https://s31.postimg.org/4g4lytrqj/peliculas.png', tipo='peliculas/'))
    
    itemlist.append( Item(channel=item.channel, title="Series", action="menuseries",thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png', tipo='peliculas/'))

    return itemlist

def menupeliculas(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Estrenos", action="lista",thumbnail='https://s12.postimg.org/4zj0rbun1/estrenos.png', fanart='https://s12.postimg.org/4zj0rbun1/estrenos.png', url = host+'/apimovies/moviepremiere/300', last_item = 0))
    
    itemlist.append( item.clone (title="Clasicos", action="lista",thumbnail='https://s8.postimg.org/8lt3x4y3p/clasicos.png', fanart='https://s8.postimg.org/8lt3x4y3p/clasicos.png', url = host+'/apimovies/moviebyscore/300', last_item = 0))

    itemlist.append( item.clone (title="Populares", action="lista",thumbnail='https://s22.postimg.org/wrx8dpa4x/popular.png', fanart='https://s22.postimg.org/wrx8dpa4x/popular.png', url = host+'/apimovies/moviebypop/300', last_item = 0))
    
    itemlist.append( item.clone (title="Por Año", action="by_year",thumbnail='https://s31.postimg.org/iyl5fvzqz/pora_o.png', fanart='https://s31.postimg.org/iyl5fvzqz/pora_o.png', last_item = 0))

    itemlist.append( item.clone (title="Generos", action="generos",thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png', url = host+'/peliculas', last_item = 0))

    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', url =host+'/apimovies/moviebyword/', fanart='https://s31.postimg.org/qose4p13f/Buscar.png',last_item = 0))

    return itemlist


def menuseries(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Estrenos", action="lista",thumbnail='https://s12.postimg.org/4zj0rbun1/estrenos.png', fanart='https://s12.postimg.org/4zj0rbun1/estrenos.png', url=host+'/apiseries/seriepremiere/300' ,tipo = 'serie', last_item = 0))
    
    itemlist.append( item.clone (title="Clasicos", action="lista",thumbnail='https://s8.postimg.org/8lt3x4y3p/clasicos.png', fanart='https://s8.postimg.org/8lt3x4y3p/clasicos.png', url = host+'/apiseries/seriebyscore/300',tipo = 'serie', last_item = 0))

    itemlist.append( item.clone (title="Populares", action="lista",thumbnail='https://s22.postimg.org/wrx8dpa4x/popular.png', fanart='https://s22.postimg.org/wrx8dpa4x/popular.png', url = host+'/apiseries/seriebypop/300',tipo = 'serie', last_item = 0))
    
    itemlist.append( item.clone (title="Por Año", action="by_year",thumbnail='https://s31.postimg.org/iyl5fvzqz/pora_o.png', fanart='https://s31.postimg.org/iyl5fvzqz/pora_o.png', tipo = 'serie', last_item = 0))

    itemlist.append( item.clone (title="Generos", action="generos",thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png', url = host+'/series', tipo='serie', last_item =0))

    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', url =host+'/apiseries/seriebyword/', fanart='https://s31.postimg.org/qose4p13f/Buscar.png', tipo='serie', last_item = 0))

    return itemlist




def lista (item):
    logger.info ()
    itemlist =[]
    
    token_url = "http://floow.tv/apibase/token"
    post = {"key": key}
    post = urllib.urlencode(post)
    data = httptools.downloadpage(token_url, post = post).data
    token_data = jsontools.load_json(data)
    token = token_data['token']

    post = {"key": key, "token":token}
    post = urllib.urlencode(post)
    data = httptools.downloadpage(item.url, post = post).data
    dict_data = jsontools.load_json(data)
    
    if item.last_item != 0 and int(item.last_item) < len(dict_data['results']):
        if int(item.last_item)+1 < len(dict_data['results']):
            first_item = int(item.last_item)+1
            if (len(dict_data['results']) - int(item.last_item+21)) > 0:
                last_item = int(item.last_item)+21
            else:
                last_item = len(dict_data['results'])
    else:
        first_item = 0
        if len(dict_data['results']) > 20:
            last_item=20
        else:
            last_item=len(dict_data['results'])

    if dict_data.get("status", "") == "success":
        
        for i in range(first_item, last_item):
            if item.tipo != 'serie':
                id_movie = dict_data['results'][i]['id']
                contentTitle = dict_data['results'][i]['title'].replace('HD','')
                itemlist.append(item.clone(action = 'findvideos',title=contentTitle, url=host+'/stream/selector/'+id_movie, thumbnail=dict_data['results'][i]['poster'], plot=dict_data['results'][i]['synopsis'],contentTitle=contentTitle , infoLabels ={'year':dict_data['results'][i]['year']}))
            else:
                contentSerieName= dict_data['results'][i]['title'].replace('HD','')
                itemlist.append(item.clone(action = 'temporadas',title=contentSerieName, url=dict_data['results'][i]['link'], thumbnail=dict_data['results'][i]['poster'], plot=dict_data['results'][i]['synopsis'],contentSerieName=contentSerieName , infoLabels ={'year':dict_data['results'][i]['year']}, token = token, tipo = item.tipo))
    
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    
    #Paginacion
    if last_item < len(dict_data['results']):
        itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = item.url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',last_item=last_item-1, tipo = item.tipo))
    return itemlist
       
def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto+'/200'

    try:
        if texto != '' and len(texto)>=3:
            return lista(item)
        else:
            return []
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def by_year(item):
    itemlist =[]
    
    if item.tipo != 'serie':
        url_base = host+'/apimovies/moviemultisearch/'
    else:
        url_base = host+'/apiseries/seriemultisearch/'

    if item.extra_year =='':
        for year in range(1900,2017,10):
            itemlist.append(Item(channel = item.channel, action = "by_year", title = str(year)+"'s", url = '', thumbnail='', extra_year=str(year), tipo = item.tipo, last_item= item.last_item))
        return itemlist
    else:
        for year in range(int(item.extra_year),int(item.extra_year)+10):
            itemlist.append(Item(channel = item.channel, action = "lista", title = str(year), url = url_base+str(year)+'/0/0', thumbnail='', last_item = item.last_item, tipo = item.tipo))
        return itemlist


def generos(item):
               
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = '<img class="genre" ng-click="gr_filter\((.*?)\)" src="\/img\/genres\/(.*?)\.png">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedfilter, scrapedtitle in matches:
    
        title = scrapedtitle
        if scrapedtitle in tgenero:
           thumbnail =tgenero[scrapedtitle]
           fanart= tgenero[scrapedtitle]
        else:
           thumbnail =''
           fanart= ''
        if item.tipo != 'serie':
            url = host+'/apimovies/moviemultisearch/1/'+scrapedfilter+'/0'
        else:
            url = host+'/apiseries/seriemultisearch/1/'+scrapedfilter+'/0'
        itemlist.append( Item(channel=item.channel, action="lista" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart, tipo = item.tipo, last_item = 0))
    return itemlist


def temporadas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    
    patron = '<div class="mini_nav_bt grey1.*?temp_filter" data-id="(.*?)">(.*?)<\/div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    infoLabels = item.infoLabels
    for scrapedid, scrapedtemp in matches:
        title = 'Temporada '+scrapedtemp
        contentSeasonNumber = scrapedtemp
        infoLabels['season'] = contentSeasonNumber
        itemlist.append( Item(channel=item.channel, action="episodiosxtemp" , title=title, url='http://floow.tv/apiseries/tempchapters/'+scrapedid, contentSeasonNumber=scrapedtemp, thumbnail=item.thumbnail, fanart = item.fanart, infoLabels = infoLabels, token = item.token, last_item = item.last_item, tipo = item.tipo))
    
    #if config.get_library_support() and len(itemlist) > 0:
    #    itemlist.append(item.clone(action = 'add_serie_to_library',title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url, contentSerieName=item.contentSerieName , tipo = item.tipo, extra = 'episodios'))

    if item.extra !='episodios':
        tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    

    return itemlist

def episodios(item):
    logger.info()
    itemlist = []
    templist = temporadas(item)
    for tempitem in templist:
       #tempitem.extra1 = 'library'
       itemlist += episodiosxtemp(tempitem)

    return itemlist


def episodiosxtemp(item):

    itemlist = []
    infoLabels = item.infoLabels
    post = {"key": key, "token":item.token}
    
    post = urllib.urlencode(post)
    data = httptools.downloadpage(item.url, post = post).data
    dict_data = jsontools.load_json(data)
    if dict_data.get("status", "") == "success":
        for i in range(len(dict_data['results'])):
            episode = dict_data['results'][i]['number']
            contentEpisodeNumber = episode
            infoLabels['episode'] = contentEpisodeNumber
            id_episode = dict_data['results'][i]['id']
            title = item.contentSeasonNumber+'x'+contentEpisodeNumber+'-'+ dict_data['results'][i]['title']
            itemlist.append(item.clone(action = 'findvideos',title=title, url=host+'/stream/selector/'+id_episode+'/2', contentSerieName=item.contentSerieName, thumbnail=item.thumbnail, plot=item.plot, contentEpisodeNumber= contentEpisodeNumber, infoLabels = infoLabels, tipo = item.tipo, token = item.token, last_item = item.last_item))
    if item.extra != 'episodios':
        tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    return itemlist


def findvideos(item):
    servers ={'pixshare':'directo','bitshare HD':'openload'}
    logger.info ()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}|', "", str(data))
    patron ='<a class=option href=(.*?) target=_self>(.*?)<\/a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for url, server in matches:
        if 'HD' in server:
            url =url
        else:
            url = host+url
        title = item.contentTitle+' ('+servers[server]+')'
        thumbnail = servertools.guess_server_thumbnail(servers[server])
        itemlist.append( Item(channel=item.channel, action="play" , title=title ,url=url, thumbnail=thumbnail, plot=item.plot, infoLabels = item.infoLabels))

    if item.tipo != 'serie' and item.tipo !='findvideos':
       if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos':
          contentTitle= item.contentTitle
          itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = contentTitle))
    return itemlist


def play(item):
    itemlist=[]
    data = httptools.downloadpage(item.url).data
    data = data.replace("'",'"')
    infoLabels = item.infoLabels
    if 'movie' in item.url or 'chapter' in item.url:
        item.url = scrapertools.find_single_match(data, '"file" : "(.*?)",')
        item.subtitle = scrapertools.find_single_match(data, '{ "file": "(.*?)", "label": "Default", "kind": "captions",  "default": true }')

        itemlist.append(item)
    else:    
        url = scrapertools.find_single_match(data, '<iframe width=".*?" height=".*?" scrolling="no" frameborder="0" src="(.*?)" allowFullScreen webkitallowfullscreen="true"><\/iframe>')
        itemlist = servertools.find_video_items(data=url)
    
    for videoitem in itemlist:
        videoitem.infoLabels = item.infoLabels
        videoitem.title = item.title
        videoitem.thumbnail = videoitem.infoLabels['thumbnail']
    

    return itemlist  
