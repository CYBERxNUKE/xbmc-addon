# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para longurl (acortador de url)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import urllib

from core import config
from core import logger
from core import scrapertools

DEBUG = config.get_setting("debug")


def get_server_list():
    servers =[]
    data = scrapertools.downloadpage("http://longurl.org/services")
    data = scrapertools.unescape(data)
    data = scrapertools.get_match(data,'<ol>(.*?)</ol>')
    patron='<li>(.*?)</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    #añadiendo algunos manualmente que no salen en la web
    servers.append("sh.st")
    
    for server in matches:
      servers.append(server)
    return servers

servers=get_server_list()

    
def get_long_urls(data):
    logger.info("[longurl.py] get_long_urls ")  
    patron  = '<a href="http://([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for short_url in matches:
      if short_url.startswith(tuple(servers)):
        logger.info("[longurl.py] - get_long_urls: " + short_url)
        longurl_data = scrapertools.downloadpage("http://api.longurl.org/v2/expand?url="+urllib.quote_plus(short_url))
        logger.info(longurl_data)
        try:
          long_url = scrapertools.get_match(longurl_data,'<long-url><!\[CDATA\[(.*?)\]\]></long-url>')
        except:
          long_url=""
        if (long_url<> ""):data=data.replace(short_url,long_url)
    return data
