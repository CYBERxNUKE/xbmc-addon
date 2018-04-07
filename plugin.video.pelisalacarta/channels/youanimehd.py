# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para youanimehd creado por Itsuki Minami
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item


DEBUG = config.get_setting("debug")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"


def mainlist(item):
    logger.info("pelisalacarta.channels.youanimehd mainlist")

    itemlist = []
    itemlist.append( Item(channel=item.channel, action="completo"  , title="Portada"                        , url="http://youanimehd.com/" , viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="letras"    , title="Listado Alfabetico"             , url="http://youanimehd.com/" ))
    itemlist.append( Item(channel=item.channel, action="completo"  , title="Listado Completo de Animes"     , url="http://youanimehd.com/videos" , viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo"  , title="Listado Completo de Peliculas"  , url="http://youanimehd.com/tags/pelicula" , viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo"  , title="Listado Completo de Dibujos"  , url="http://youanimehd.com/tags/cartoon" , viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo"  , title="Listado Completo de Doramas"    , url="http://youanimehd.com/tags/dorama" , viewmode="movie_with_plot"))
    #itemlist.append( Item(channel=item.channel, action="search"  , title="Buscar"                            , url="http://youanimehd.com/buscar/" ))
  
    return itemlist

def completo(item):
    logger.info("pelisalacarta.channels.youanimehd completo")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)

    '''
    <li class="mainList">
    <div class="videoThumb">
    <a href="http://youanimehd.com/video/438/Bakuman-Temporada-03" title="Mashiro al principio ansiaba convertirse en mangaka por la admiración que sentía
     por su tio Nobuhiro Mashiro, hasta que este falleció y no quiso saber..."><img src="http://youanimehd.com/thumb/1_438.jpg" alt="Mashiro al principio ansiaba convertirse en mangaka por la admiración que sentía por su tio Nobuhiro Mashiro, hasta que este falleció y no quiso saber nada del manga; hasta que un día tras olvidarse un libro en clase se encuentra con Akito Takagi que le propone crear manga con él, Mashiro al principio se niega, pero tras las constantes insistencias de Takagi acaba aceptando. El duo de Mashiro y Takagi apodado como Ashirogi Muto descubrirán lo que es el mundo del manga." id="rotate_438_latestvideo" /></a>
    </div>
    <div class="videoTitle">
    <a href="http://youanimehd.com/video/438/Bakuman-Temporada-03">Bakuman Temporada 03</a>
    </div>
    <div class="videoInfo">
    <div class="videoViews">67 Views</div>
    <div class="videoStars">
    not yet rated
    </div>
    </div>
    </li>
    '''
    patronvideos = '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" id="[^"]+" alt="[^"]+"[^<]+</a[^<]+</div[^<]+<div class="videoTitle"[^<]+<a[^>]+>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for url,plot,thumbnail,title in matches:
        scrapedtitle = title
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot

        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=item.channel, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))

    patronvideos = '<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" alt="[^"]+"[^<]+</a[^<]+</div[^<]+<div class="videoTitle"[^<]+<a[^>]+>([^<]+)</a>'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)    

    for url,plot,thumbnail,title in matches:
        scrapedtitle = title
        fulltitle = scrapedtitle
        scrapedurl = urlparse.urljoin(item.url,url)
        scrapedthumbnail = thumbnail
        scrapedplot = plot
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=item.channel, action="serie" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, fulltitle=fulltitle))

    patron = '<li><a href="([^"]+)">Next</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            scrapedurl = matches[0]
            scrapedtitle = "!Pagina Siguiente"
            scrapedthumbnail = ""
            scrapedplot = ""

        itemlist.append( Item(channel=item.channel, action="completo", title=scrapedtitle , url=scrapedurl, viewmode="movie_with_plot") )        

    return itemlist

def letras(item):
    logger.info("pelisalacarta.channels.youanimehd letras")
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="completo" , title="0-9", url="http://youanimehd.com/tags/0-9", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="A"  , url="http://youanimehd.com/tags/a", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="B"  , url="http://youanimehd.com/tags/b", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="C"  , url="http://youanimehd.com/tags/c", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="D"  , url="http://youanimehd.com/tags/d", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="E"  , url="http://youanimehd.com/tags/e", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="F"  , url="http://youanimehd.com/tags/f", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="G"  , url="http://youanimehd.com/tags/g", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="H"  , url="http://youanimehd.com/tags/h", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="I"  , url="http://youanimehd.com/tags/i", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="J"  , url="http://youanimehd.com/tags/j", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="K"  , url="http://youanimehd.com/tags/k", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="L"  , url="http://youanimehd.com/tags/l", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="M"  , url="http://youanimehd.com/tags/m", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="N"  , url="http://youanimehd.com/tags/n", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="O"  , url="http://youanimehd.com/tags/o", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="P"  , url="http://youanimehd.com/tags/p", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="Q"  , url="http://youanimehd.com/tags/q", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="R"  , url="http://youanimehd.com/tags/r", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="S"  , url="http://youanimehd.com/tags/s", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="T"  , url="http://youanimehd.com/tags/t", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="U"  , url="http://youanimehd.com/tags/u", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="V"  , url="http://youanimehd.com/tags/v", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="W"  , url="http://youanimehd.com/tags/w", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="X"  , url="http://youanimehd.com/tags/x", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="Y"  , url="http://youanimehd.com/tags/y", viewmode="movie_with_plot"))
    itemlist.append( Item(channel=item.channel, action="completo" , title="Z"  , url="http://youanimehd.com/tags/z", viewmode="movie_with_plot"))

    return itemlist


def serie(item):
    logger.info("pelisalacarta.channels.youanimehd serie")
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = data.replace('\n',"")
    data = scrapertools.get_match(data,'<div class="sc_menu"[^<]+<ul class="sc_menu">(.*?)</ul[^<]+</div[^<]+</li>')

    # Saca el argumento
    """patronplot  = 'Descripción</strong><br /><br />([^"]+)<br />'
    matches = re.compile(patronplot,re.DOTALL).findall(data)
    
    if len(matches)>0:"""
    scrapedplot = ""
    
    # Saca enlaces a los episodios
    #<li><a target="vides" href="http://www.youanimehd.com/videoss/?video=196994058_165265436&c=1086387723">
    #<img  src="http://cs525400.vk.me/u196994058/video/l_ab9b6a65.jpg","date":1366157450,"views":0,"comments":0,"player":"http://vk.com/video_ext.php?oid=196994058&id=165265436&hash=79452ec7c92c0c6f" width="100" height="75" alt="1" border="0" align="top"/><span style="color:red">Capitulo 1</span>
    #</a> </li>
    patronvideos = ' <li><a target="vides" href="([^"]+)"[^<]+<img\s+src="([^"]+)"[^<]+<span style="color:red">([^"]+)</span>'
    itemlist = []        
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
        
    for match in matches:
        #chapnum += 1
        #if chapnum == "0"
           #initnum = 0
        #chapnum = str(chapnum+1)
        #scrapedtitle = matches[2] + chapnum
        scrapedtitle = match[2]
        scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
        scrapedtitle = scrapertools.entityunescape( scrapedtitle )        
        try:
            episodio = scrapertools.get_match(scrapedtitle,"(\d+)")
            if len(episodio)==1:
                scrapedtitle = "1x0"+episodio
            else:
                scrapedtitle = "1x"+episodio
        except:
            pass
        
        scrapedurl = urlparse.urljoin(item.url,match[0])
        scrapedthumbnail = match[1]
        #if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")

        itemlist.append( Item(channel=item.channel, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=item.show, fulltitle="a", folder=False))
    
    if config.get_library_support():
        itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="serie", show=item.show) )

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.youanimehd play url="+item.url)

    itemlist=[]
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    from core import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel=item.channel
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = "["+videoitem.server+"]"

    return itemlist
