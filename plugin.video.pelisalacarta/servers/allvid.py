# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allvid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    if ("File was deleted" or "Not Found") in data: return False, "[Allvid] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = scrapertools.cache_page(page_url)
    redirect_url = scrapertools.find_single_match(data, '<iframe src="([^"]+)')
    data = scrapertools.cache_page(redirect_url)
    matches = scrapertools.find_single_match(data,
                                             "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d.*?)</script>")
    matchjs = jsunpack.unpack(matches).replace("\\", "")

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(matchjs, '\{file:"([^"]+)",label:"([^"]+)"\}')
    for media_url, label in media_urls:
        video_urls.append([scrapertools.get_filename_from_url(media_url)[-4:] + " (" + label + ") [allvid]", media_url])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allvid.ch/jdfscsa5uoy4
    patronvideos = "allvid.ch/(?:embed-|)([a-z0-9]+)"
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allvid]"
        url = "http://allvid.ch/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'allvid'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
