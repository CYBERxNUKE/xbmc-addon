# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para spruto
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url)
    if "404.txt" in data.data:
        return False, "El video ha sido borrado"
    if data.code == 503:
	    return False, "El servidor está fuera de servicio"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = httptools.downloadpage(page_url).data

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, '<source src="([^"]+)"')

    for media_url in media_urls:
        extension = scrapertools.get_filename_from_url(media_url)[-3:]
        if extension != "png" and extension != "php":
            video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " [spruto]", media_url])

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.spruto.tv/iframe_embed.php?video_id=141593
    patronvideos = 'spruto.tv/iframe_embed.php\?video_id=(\d+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[spruto]"
        url = "http://spruto.tv/iframe_embed.php?video_id=" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'spruto'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
