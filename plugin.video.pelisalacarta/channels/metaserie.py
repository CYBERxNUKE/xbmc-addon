# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (MetaSerie) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools



def mainlist(item):
    logger.info()

    itemlist = []
    itemlist.append( Item(channel=item.channel, title="Series", action="todas", url="http://metaserie.com/series-agregadas", thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png'))
    itemlist.append( Item(channel=item.channel, title="Anime", action="todas", url="http://metaserie.com/animes-agregados",thumbnail='https://s31.postimg.org/lppob54d7/anime.png', fanart='https://s31.postimg.org/lppob54d7/anime.png'))
    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url="http://www.metaserie.com/?s=", thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))
    return itemlist

def todas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    
    patron = '<div class="poster">[^<]'
    patron +='<a href="([^"]+)" title="([^"]+)">[^<]'
    patron +='<div class="poster_efecto"><span>([^<]+)<.*?div>[^<]'
    patron +='<img.*?src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle,scrapedplot, scrapedthumbnail in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        #title = scrapedtitle.replace("&#8217;","'")
        thumbnail = scrapedthumbnail
        plot = scrapedplot
        fanart = 'https://s32.postimg.org/7g50yo39h/metaserie.png'
        itemlist.append( Item(channel=item.channel, action="temporadas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentSerieName=title))
    
    #Paginacion

    patron  = '<li><a class="next page-numbers local-link" href="([^"]+)">&raquo;.*?li>'
    next_page_url = scrapertools.find_single_match(data,'<li><a class="next page-numbers local-link" href="([^"]+)">&raquo;.*?li>')
    if next_page_url!="":
        import inspect
        itemlist.append(
            Item(
                channel = item.channel,
                action = "todas",
                title = ">> Página siguiente",
                url = next_page_url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'
            )
        )
    return itemlist


def temporadas(item):
    logger.info()
    itemlist = []
    templist = []
    
    data = httptools.downloadpage(item.url).data
    patron = '<li class=".*?="([^"]+)".*?>([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = scrapedurl
        contentSeasonNumber = re.findall (r'.*?temporada-([^-]+)-',url)
        title = scrapedtitle
        title = title.replace("&","x");
        thumbnail = item.thumbnail
        plot = item.plot
        fanart = scrapertools.find_single_match(data,'<img src="([^"]+)"/>.*?</a>')
        itemlist.append( Item(channel=item.channel, action= 'episodiosxtemp' , title=title ,fulltitle = item.contentSerieName, url=url, thumbnail=thumbnail, plot=plot, fanart = fanart, contentSerieName=item.contentSerieName, contentSeasonNumber = contentSeasonNumber))
              
    if config.get_library_support() and len(itemlist) > 0:
       itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url,
                             action="add_serie_to_library", extra='episodios', contentSerieName=item.contentSerieName))
    
    return itemlist
    
     

def episodios(item):
    logger.info()
    itemlist = []
    templist = temporadas(item)
    for tempitem in templist:
       itemlist += episodiosxtemp(tempitem) 

    return itemlist
    
     
    

def episodiosxtemp(item):
    logger.info()
    itemlist =[]               
    data = httptools.downloadpage(item.url).data
    patron = '<td><h3 class=".*?href="([^"]+)".*?">([^<]+).*?td>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = scrapedurl
        contentEpisodeNumber = re.findall(r'.*?x([^\/]+)\/',url)
        title = scrapedtitle
        title = title.replace ("&#215;","x")
        title = title.replace ("×","x")
        thumbnail = item.thumbnail
        plot = item.plot
        fanart=item.fanart
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title, fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=plot, contentSerieName=item.contentSerieName, contentSeasonNumber = item.contentSeasonNumber, contentEpisodeNumber = contentEpisodeNumber))
    
    return itemlist

def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    itemlist = []
    if texto!='':
             try:
                 data = httptools.downloadpage(item.url).data
                 patron = '<a href="([^\"]+)" rel="bookmark" class="local-link">([^<]+)<.*?'
                 matches = re.compile(patron,re.DOTALL).findall(data)
                 scrapertools.printMatches(matches)
                 for scrapedurl,scrapedtitle in matches:
                     url = scrapedurl
                     title = scrapertools.decodeHtmlentities(scrapedtitle)
                     thumbnail = ''
                     plot = ''
                     itemlist.append( Item(channel=item.channel, action="temporadas" , title=title , fulltitle=title, url=url, thumbnail=thumbnail, plot=plot, folder =True, contentSerieName=title ))

                 return itemlist
             except:
                import sys
                for line in sys.exc_info():
                    logger.error( "%s" % line )
             return []

   

def findvideos(item):
    logger.info()
    itemlist=[]
    audio = {'la':'[COLOR limegreen]LATINO[/COLOR]','es':'[COLOR yellow]ESPAÑOL[/COLOR]','sub':'[COLOR red]ORIGINAL SUBTITULADO[/COLOR]'}
    data=httptools.downloadpage(item.url).data
    patron ='<td><img src="http:\/\/metaserie\.com\/wp-content\/themes\/mstheme\/gt\/assets\/img\/([^\.]+).png" width="20".*?<\/td>.*?<td><img src="http:\/\/www\.google\.com\/s2\/favicons\?domain=([^"]+)" \/>&nbsp;([^<]+)<\/td>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    anterior = scrapertools.find_single_match(data,'<th scope="col"><a href="([^"]+)" rel="prev" class="local-link">Anterior</a></th>')
    siguiente = scrapertools.find_single_match(data,'<th scope="col"><a href="([^"]+)" rel="next" class="local-link">Siguiente</a></th>')
    
    for scrapedid, scrapedurl, scrapedserv in matches:
        url = scrapedurl
        title = item.title+' audio '+audio[scrapedid]+' en '+scrapedserv
        extra = item.thumbnail
        thumbnail = servertools.guess_server_thumbnail(scrapedserv)
        itemlist.append( Item(channel=item.channel, action="play" , title=title, fulltitle=item.contentSerieName, url=url, thumbnail=thumbnail, extra=extra, folder= True))
    if item.extra1 != 'capitulos':
        if anterior !='':
            itemlist.append( Item(channel=item.channel, action="findvideos" , title='Capitulo Anterior' , url=anterior, thumbnail='https://s31.postimg.org/k5kpwyrgb/anterior.png', folder =True ))
        if siguiente !='':
            itemlist.append( Item(channel=item.channel, action="findvideos" , title='Capitulo Siguiente' , url=siguiente, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png', folder =True ))
    return itemlist

def play(item):
    logger.info()
    itemlist =[]
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=item.url))
    for videoitem in itemlist:
        video = item.channel
        videoitem.title = item.fulltitle
        videoitem.folder = False
        videoitem.thumbnail = item.extra
        videoitem.fulltitle = item.fulltitle
    return itemlist
   

    
