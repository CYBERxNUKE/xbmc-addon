# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para userscloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    response = httptools.downloadpage(page_url)

    if not response.sucess or "Not Found" in response.data or "File was deleted" in response.data:
        return False, "[Userscloud] El fichero no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    video_urls = []
    data = httptools.downloadpage(page_url)
    media_url = scrapertools.find_single_match(data, '<source src="([^"]+)"')
    if not media_url:
        id_ = page_url.rsplit("/", 1)[1]
        rand = scrapertools.find_single_match(data, 'name="rand" value="([^"]+)"')
        post = "op=download2&id=%s&rand=%s&referer=%s&method_free=&method_premium=" % (id_, rand, page_url)
        data = httptools.downloadpage(page_url, post).data

        media_url = scrapertools.find_single_match(data, '<a href="([^"]+)" class="btn btn-success"')

    ext = scrapertools.get_filename_from_url(media_url)[-4:]
    video_urls.append(["%s [userscloud]" % ext, media_url])
        
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):

    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    #http://userscloud.com/z3nnqbspjyne
    #http://userscloud.com/embed-z3nnqbspjyne.html
    patronvideos = 'userscloud.com/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[userscloud]"
        url = "https://userscloud.com/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'userscloud'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
