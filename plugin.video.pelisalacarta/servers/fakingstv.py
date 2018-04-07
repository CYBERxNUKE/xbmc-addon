# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fakingstv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists( page_url ):
    logger.info("[fakingstv.py] test_video_exists(page_url='%s')" % page_url)
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[fakingstv.py] url="+page_url)
    data = scrapertools.cache_page( page_url )
    media_url = scrapertools.get_match(data,'\'file\': \'([^"]+)\',')
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [fakingstv]",media_url])

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos  = 'http://tv.fakings.com/embed/([a-z0-9A-Z]+)/'
    logger.info("[fakingstv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fakingstv]"
        url = "http://tv.fakings.com/embed/"+match+"/"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fakingstv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
