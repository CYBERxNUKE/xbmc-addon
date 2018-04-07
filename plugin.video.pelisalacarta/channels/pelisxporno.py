# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para Pelisxporno
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# -----------------------------------------------------------

from core import httptools
from core import logger
from core import scrapertools
    

def mainlist(item):
    logger.info()

    itemlist = []
    itemlist.append(item.clone(action="lista", title="Novedades", url="http://www.pelisxporno.com/?order=date"))
    itemlist.append(item.clone(action="categorias", title="Categorías", url="http://www.pelisxporno.com"))
    itemlist.append(item.clone(action="search", title="Buscar", url="http://www.pelisxporno.com/?s=%s"))

    return itemlist


def search(item,texto):
    logger.info()
    item.url = item.url % texto
    return lista(item) 


def lista(item):
    logger.info()
    itemlist = []

    # Descarga la pagina  
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    patron = '<div class="thumb">.*?<a href="([^"]+)" title="([^"]+)">.*?<img src="([^"]+)".*?' \
             '<div class="duration".*?>([^<]+)<'
    matches = scrapertools.find_multiple_matches(data, patron)
    for scrapedurl, scrapedtitle, scrapedthumbnail, duration in matches:
        if duration:
            scrapedtitle += "  (%s)" % duration

        itemlist.append(item.clone(action="findvideos", title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail))

    #Extrae la marca de siguiente página
    next_page = scrapertools.find_single_match(data, '<a class="page larger" href="([^"]+)">([^"]+)</a>')
    if next_page:
      scrapedurl = next_page[0]
      page = next_page[1]
      itemlist.append(item.clone(action="lista", title=">> Página Siguiente (%s)" % page, url=scrapedurl))

    return itemlist


def categorias(item):
    logger.info()
    itemlist = []

    # Descarga la pagina  
    data = httptools.downloadpage(item.url).data

    # Extrae las entradas (carpetas)
    bloque_cat = scrapertools.find_single_match(data, '<li id="categories-2"(.*?)</ul>')
    matches = scrapertools.find_multiple_matches(bloque_cat, '<a href="([^"]+)" >(.*?)</a>')
    for scrapedurl, scrapedtitle in matches:
        itemlist.append(item.clone(action="lista", title=scrapedtitle, url=scrapedurl))

    return itemlist
