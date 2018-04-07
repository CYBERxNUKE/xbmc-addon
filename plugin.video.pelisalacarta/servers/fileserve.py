# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fileserve
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists( page_url ):
    logger.info("[fileserve.py] test_video_exists(page_url='%s')" % page_url)
    
    # Existe: http://www.fileserve.com/file/E5Y5R5E
    # No existe: 
    data = scrapertools.cache_page(page_url)
    patron  = '<div class="panel file_download">[^<]+<img src="/images/down_arrow.gif"[^<]+<h1>([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        return True,""
    else:
        patron  = '<li class="title"><h1>(File not available)</h1>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            return False,"El archivo ya no está disponible<br/>en fileserve o ha sido borrado"
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[fileserve.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    if premium:
        # Accede a la home para precargar la cookie
        data = scrapertools.cache_page("http://fileserve.com/index.php")
    
        # Hace el login
        url = "http://fileserve.com/login.php"
        post = "loginUserName=%s&loginUserPassword=%s&autoLogin=on&ppp=102&loginFormSubmit=Login" % (user,password)
        data = scrapertools.cache_page(url, post=post)
    
        location = scrapertools.get_header_from_response(page_url,header_to_get="location")
        logger.info("location="+location)
    
        if location.startswith("http"):
            extension = location[-4:]
            video_urls.append( [ "%s (Premium) [fileserve]" % extension, location ] )

    for video_url in video_urls:
        logger.info("[fileserve.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = 'http://www.fileserve.com/file/([A-Z0-9a-z]{7})'
    logger.info("[fileserve.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Fileserve]"
        url = "http://www.fileserve.com/file/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fileserve' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
