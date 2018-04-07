# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pornoactricesx
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")


def mainlist(item):
    logger.info("[pornoactricesx.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="videos"          , title="Útimos videos"     , url="http://www.pornoactricesx.com/"))
    itemlist.append( Item(channel=item.channel, action="listactrices"    , title="Listado Actrices"  , url="http://www.pornoactricesx.com/todas-las-actrices"))
    itemlist.append( Item(channel=item.channel, action="search"          , title="Buscar"            , url="http://www.pornoactricesx.com/search/content/"))

    return itemlist

def search(item,texto):
    logger.info("[pornoactricesx.py] search")
    texto = texto.replace( " ", "+" )
    item.url = item.url + texto
    try:
        return videos(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
def videos(item):
    logger.info("[pornoactricesx.py] videos")
    itemlist = []
    mas= True
    data = ""
    url= item.url
    while len(itemlist) < 25 and mas== True:
      data = scrapertools.cachePage(url)
      data = scrapertools.unescape(data)
      patron = '<div class="field field-name-title field-type-ds field-label-hidden view-mode-teaser"><div class="field-items"><div class="field-item even"><h1><a href="([^"]+)">([^"]+)</a></h1></div></div></div>  </div>'
      patron +='[^<]{4}<div class="group-left">[^<]{5}<div class="field field-name-field-imagen-del-video field-type-image field-label-hidden view-mode-teaser"><div class="field-items">'
      patron +='<figure class="clearfix field-item even"><a href="([^"]+)"><img class="image-style-medium" src="([^"]+)"'
      matches = re.compile(patron,re.DOTALL).findall(data)
      for url,title,url2,thumbnail in matches:

          scrapedtitle = title.replace(" Vídeo porno completo.","")
          scrapedurl = urlparse.urljoin( "http://www.pornoactricesx.com" , url )
          scrapedthumbnail = thumbnail
          scrapedplot = ""
          # Depuracion
          if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
          itemlist.append( Item(channel=item.channel, action='play', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )
          
      #Patron 2 para busquedas
      patron='<div class="field field-name-title field-type-ds field-label-hidden view-mode-search_result">'
      patron +='<div class="field-items"><div class="field-item even"><h1><a href="([^"]+)">([^"]+)</a></h1></div></div></div>  </div>'
      patron +='[^<]{4}<div class="group-left">[^<]{5}<div class="field field-name-field-imagen-del-video field-type-image field-label-hidden view-mode-search_result"><div class="field-items"><figure class="clearfix field-item even"><a href="([^"]+)"><img class="image-style-medium" src="([^"]+)" width='
      matches = re.compile(patron,re.DOTALL).findall(data)
      for url,title, url2, thumbnail in matches:

          scrapedtitle = title.replace(" Vídeo porno completo.","")
          scrapedurl = urlparse.urljoin( "http://www.pornoactricesx.com" , url )
          scrapedthumbnail = thumbnail
          scrapedplot = ""
          # Depuracion
          if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
          itemlist.append( Item(channel=item.channel, action='play', title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot) )
      patron = '<a title="Ir a la página siguiente" href="([^<]+)">siguiente ›</a>'
      matches = re.compile(patron,re.DOTALL).findall(data)
      if len(matches) >0:
        url="http://www.pornoactricesx.com"+matches[0]
        mas=True
      else:
        mas=False
        
    #Paginador
    patron = '<a title="Ir a la página siguiente" href="([^<]+)">siguiente ›</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)  
    if len(matches) >0:
      scrapedurl = "http://www.pornoactricesx.com"+matches[0]
      itemlist.append( Item(channel=item.channel, action="videos", title="Página Siguiente" , url=scrapedurl , thumbnail="" , folder=True) )
      
    return itemlist

def play(item):
    logger.info("[pornoactricesx.py] findvideos")
    itemlist=[]
    # Descarga la página
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    logger.info(data)
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.thumbnail = item.thumbnail
        videoitem.channel=item.channel
        videoitem.action="play"
        videoitem.folder=False
        videoitem.title = item.title

    return itemlist

def listactrices(item):
    logger.info("[pornoactricesx.py] listcategorias")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.unescape(data)
    patron =  '<span class="field-content"><a href="([^"]+)">([^"]+)</a></span>  </span>'
    patron += '[^<]+<div class="views-field views-field-field-imagen-del-video">        <div class="field-content"><img class="image-style-thumbnail" src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url, actriz, thumbnail in matches:
      url="http://www.pornoactricesx.com"+url
      itemlist.append( Item(channel=item.channel, action="videos" , title=actriz, url=url, thumbnail=thumbnail))
    
    #Paginador
    patron = '<a title="Ir a la página siguiente" href="([^"]+)">siguiente ›'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches) >0:
      url="http://www.pornoactricesx.com"+matches[0]
      itemlist.append( Item(channel=item.channel, action="listactrices" , title="Página Siguiente", url=url))

    return itemlist
