# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fastplay
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data

    if "Object not found" in data:
        return False, "[Fastplay] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    video_urls = []
    videos = scrapertools.find_multiple_matches(data, 'file\s*:\s*"([^"]+)"')
    calidad = scrapertools.find_single_match(data, 'height\s*:\s*"([^"]+)"')
    for video_url in videos:
        extension = scrapertools.get_filename_from_url(video_url)[-4:]
        video_urls.append(["%s %s [fastplay]" % (extension, calidad+"p"), video_url])

    for video_url in video_urls:
        logger.info(" %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # https://fastplay.cc/flash-ZapZwMMA
    # https://fastplay.cc/ZupZwMMA
    patronvideos = 'fastplay.(?:cc|sx)/(?:flash-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fastplay]"
        url = "http://fastplay.cc/flash-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'fastplay'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)
           
    return devuelve
