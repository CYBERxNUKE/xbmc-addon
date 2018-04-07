# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (playPornX) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools

host ="http://www.playpornx.net/list-movies/"

def mainlist (item):
    itemlist =[]
    itemlist.append( Item(channel=item.channel, title="Todas", action="lista", thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png'))
    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url='http://www.playpornx.net/?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))

    return itemlist

def lista (item):
    logger.info()
    
    itemlist = []
    if item.url =='': item.url=host
    data = httptools.downloadpage(item.url).data
    patron = '<a class="clip-link" title="([^"]+)"  href="([^"]+)">\s*<span class="clip">\s*<img  alt=".*?" width="190" height="266" src="([^"]+)" data-qazy="true" \/><span class="vertical-align"><\/span>\s*<\/span>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumbnail in matches:

        url = scrapedurl
        thumbnail = scrapedthumbnail
        title = scrapedtitle
                
        itemlist.append( Item(channel=item.channel, action='findvideos' , title=title , url=url, thumbnail=thumbnail))
       
# #Paginacion

    if itemlist !=[]:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data,'rel="next" href="([^"]+)"')
        import inspect
        if next_page !='':
           itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',extra=item.extra))
    return itemlist

def search (item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto

    try:
        if texto!= '':
            return lista(item)
        else:
            return []
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
