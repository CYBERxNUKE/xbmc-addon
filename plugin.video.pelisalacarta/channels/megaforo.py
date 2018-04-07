# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para megaforo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item
from platformcode import platformtools


DEBUG = config.get_setting("debug")
MAIN_HEADERS = []
MAIN_HEADERS.append( ["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"] )
MAIN_HEADERS.append( ["Accept-Encoding","gzip, deflate"] )
MAIN_HEADERS.append( ["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"] )
MAIN_HEADERS.append( ["Connection","keep-alive"] )
MAIN_HEADERS.append( ["Host","mega-foro.com"] )
MAIN_HEADERS.append( ["Referer","http://mega-foro.com/"] )
MAIN_HEADERS.append( ["User-Agent","Mozilla/5.0 (Windows NT 6.2; rv:23.0) Gecko/20100101 Firefox/23.0"] )


def login():
    logger.info("[megaforo.py] login")
    # Calcula el hash del password
    LOGIN = config.get_setting("megaforouser", "megaforo")
    PASSWORD = config.get_setting("megaforopassword", "megaforo")
    logger.info("LOGIN="+LOGIN)
    logger.info("PASSWORD="+PASSWORD)
    # Hace el submit del login
    post = "user="+LOGIN+"&passwrd="+PASSWORD
    logger.info("post="+post)
    data = scrapertools.cache_page("http://mega-foro.com/login2/" , post=post, headers=MAIN_HEADERS)
    return True


def mainlist(item):
    logger.info("[megaforo.py] mainlist")
    itemlist = []
    if config.get_setting("megaforouser","megaforo") == "":
        itemlist.append( Item( channel=item.channel , title="Habilita tu cuenta en la configuración..." , action="settingCanal" , url="") )
    else:
        if login():
            itemlist.append( Item( channel=item.channel , title="Series" , action="foro" , url="http://mega-foro.com/series-de-tv/" , folder=True ) )
            itemlist.append( Item( channel=item.channel , title="Películas" , action="foro" , url="http://mega-foro.com/peliculas/" , folder=True ) )
            itemlist.append( Item( channel=item.channel , title="Infantil" , action="foro" , url="http://mega-foro.com/para-los-peques!/" , folder=True ) )
            itemlist.append( Item( channel=item.channel , title="Cortos y Documentales" , action="foro" , url="http://mega-foro.com/cortos-y-documentales/" , folder=True ) )
            itemlist.append( Item( channel=item.channel , title="Contenido Online" , action="foro" , url="http://mega-foro.com/online/" , folder=True ) )
            itemlist.append( Item( channel=item.channel , title="Anime & Manga" , action="foro" , url="http://mega-foro.com/anime-manga/" , folder=True ) )
            itemlist.append( Item( channel=item.channel , title="Música" , action="foro" , url="http://mega-foro.com/musica/" , folder=True ) )
            itemlist.append( Item(channel=item.channel, action="settingCanal"    , title="Configuración..."     , url="" ))
        else:
            itemlist.append( Item( channel=item.channel , title="Cuenta incorrecta, revisa la configuración..." , action="" , url="" , folder=False ) )
    return itemlist

def settingCanal(item):
    return platformtools.show_channel_settings()

def foro(item):
    logger.info("[megaforo.py] foro")
    itemlist=[]
    data = scrapertools.cache_page(item.url)

    if '<h3 class="catbg">Subforos</h3>' in data:
        patron = '<a class="subj(.*?)ct" href="([^"]+)" name="[^"]+">([^<]+)</a>' # HAY SUBFOROS
        action = "foro"
    else:
        patron = '<span id="([^"]+)"><a href="([^"]+)">([^<]+)</a> </span>'
        action = "findvideos"

    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedmsg, scrapedurl,scrapedtitle in matches:
            scrapedmsg = scrapedmsg.replace("msg_",";msg=")
            url = urlparse.urljoin(item.url,scrapedurl)
            scrapedtitle = scrapertools.htmlclean(scrapedtitle)
            scrapedtitle = unicode( scrapedtitle, "iso-8859-1" , errors="replace" ).encode("utf-8")
            title = scrapedtitle
            thumbnail = ""
            plot = scrapedmsg
            # Añade al listado
            if not 'Listado' in title:
               itemlist.append( Item(channel=item.channel, action=action, title=title, url=url , thumbnail=thumbnail , plot=plot , folder=True) )

    # EXTREA EL LINK DE LA SIGUIENTE PAGINA
    patron = 'div class="pagelinks floatleft.*?<strong>[^<]+</strong>\] <a class="navPages" href="(?!\#bot)([^"]+)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for match in matches:
        if len(matches) > 0:
            url = match
            title = ">> Página Siguiente"
            thumbnail = ""
            plot = ""
            # Añade al listado
            itemlist.append( Item(channel=item.channel, action="foro", title=title , url=url , thumbnail=thumbnail , plot=plot , folder=True) )
    return itemlist


def findvideos(item):
  show = item.title.replace("Añadir esta serie a la biblioteca de XBMC","")
  logger.info("[megaforo.py] findvideos show "+ show)
  itemlist=[]
  data = scrapertools.cache_page(item.url)

  if 'mega-foro' in data:
    patronimage = '<div class="inner" id="msg_\d{1,9}".*?<img src="([^"]+)".*?mega.co.nz/\#\![A-Za-z0-9\-\_]+\![A-Za-z0-9\-\_]+'
    matches = re.compile(patronimage,re.DOTALL).findall(data)
    if len(matches)>0:
      thumbnail = matches[0]
      thumbnail = scrapertools.htmlclean(thumbnail)
      thumbnail = unicode( thumbnail, "iso-8859-1" , errors="replace" ).encode("utf-8")
      item.thumbnail = thumbnail

    patronplot = '<div class="inner" id="msg_\d{1,9}".*?<img src="[^"]+"[^/]+/>(.*?)lgf_facebook_share'
    matches = re.compile(patronplot,re.DOTALL).findall(data)
    if len(matches)>0:
     plot = matches[0]
     title = item.title
     plot = re.sub('&nbsp;', '', plot)
     plot = re.sub('\s\s', '', plot)
     plot = scrapertools.htmlclean(plot)
     item.plot = ""

    from core import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
     videoitem.channel=item.channel
     videoitem.action="play"
     videoitem.folder=False
     videoitem.thumbnail=item.thumbnail
     videoitem.plot = item.plot

     videoitem.title = "["+videoitem.server+videoitem.title + " " + item.title

     videoitem.show = show
    if config.get_library_support():
       itemlist.append( Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="findvideos") )
    return itemlist

  else:
    item.thumbnail = ""
    item.plot = ""
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
     videoitem.channel=item.channel
     videoitem.action="play"
     videoitem.folder=False
     videoitem.thumbnail=item.thumbnail
     videoitem.plot = item.plot
     videoitem.title = "["+videoitem.server+videoitem.title + " " + item.title
    return itemlist  
