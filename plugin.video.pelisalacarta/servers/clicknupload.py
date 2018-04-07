# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para clicknupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import urllib

from core import logger
from core import scrapertools

def test_video_exists( page_url ):
    logger.info("pelisalacarta.servers.clicknupload test_video_exists(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( page_url )
    if "File Not Found" in data: return False, "[Clicknupload] El archivo no existe o ha sido borrado"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("pelisalacarta.servers.clicknupload url="+page_url)
    
    data = scrapertools.cache_page( page_url )
    data = data.replace("\n","").replace("\t","")
    post = ""
    block = scrapertools.find_single_match(data, '<Form method="POST"(.*?)</Form>')
    matches = scrapertools.find_multiple_matches(block, 'input.*?name="([^"]+)".*?value="([^"]*)"')
    for inputname, inputvalue in matches:
        post += inputname + "=" + inputvalue + "&"
    #Primera solicitud post
    data = scrapertools.cache_page( page_url , post=post)
    data = data.replace("\n","").replace("\t","")
    import time
    time.sleep(5)
    post = ""
    block = scrapertools.find_single_match(data, '<Form name="F1" method="POST"(.*?)</Form>')
    matches = scrapertools.find_multiple_matches(block, '<input.*?name="([^"]+)".*?value="([^"]*)">')
    for inputname, inputvalue in matches:
        post += inputname + "=" + inputvalue + "&"
    #Segunda solicitud post tras 5 segundos de espera
    data = scrapertools.cache_page( page_url , post=post)

    video_urls = []
    media = scrapertools.find_single_match(data,"onClick=\"window.open\('([^']+)'")
    #Solo es necesario codificar la ultima parte de la url
    url_strip = urllib.quote(media.rsplit('/', 1)[1])
    media_url = media.rsplit('/', 1)[0] +"/"+url_strip
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [clicknupload]",media_url])
    for video_url in video_urls:
        logger.info("pelisalacarta.servers.clicknupload %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://clicknupload.me/jdfscsa5uoy4
    patronvideos  = "clicknupload.(?:me|com)/([a-z0-9]+)"
    logger.info("pelisalacarta.servers.clicknupload find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[clicknupload]"
        url = "http://clicknupload.me/%s" % match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'clicknupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve