# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nosvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("pelisalacarta.servers.nosvideo.py test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    if "404 Page no found" in data:
        return False, "[nosvideo] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("pelisalacarta.servers.nosvideo.py get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Lee la URL
    data = scrapertools.cache_page(page_url)
    urls = scrapertools.find_multiple_matches(data, ":'(http:\/\/.+?(?:v.mp4|.smil))")
    urls = set(urls)

    for media_url in urls:
        if ".smil" in media_url:
            data = scrapertools.downloadpage(media_url)
            rtmp = scrapertools.find_single_match(data, '<meta base="([^"]+)"')
            playpath = scrapertools.find_single_match(data, '<video src="([^"]+)"')
            media_url = rtmp + " playpath=" + playpath
            filename = "rtmp"
        else:
            filename = scrapertools.get_filename_from_url(media_url)[-4:]
        video_urls.append([ filename + " [nosvideo]", media_url])

    for video_url in video_urls:
        logger.info("pelisalacarta.servers.nosvideo.py %s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://nosvideo.com/?v=iij5rw25kh4c
    # http://nosvideo.com/vj/video.php?u=27cafd27ce64900d&w=640&h=380
    patronvideos = 'nosvideo.com/(?:\?v=|vj/video.php\?u=|)([a-z0-9]+)'
    logger.info("pelisalacarta.servers.nosvideo.py find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nosvideo]"
        url = "http://nosvideo.com/vj/videomain.php?u=%s&w=&h=530" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'nosvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    # http://nosupload.com/?v=iij5rw25kh4c
    patronvideos = 'nosupload.com(/\?v\=[a-z0-9]+)'
    logger.info("pelisalacarta.servers.nosvideo.py find_videos #" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nosvideo]"
        url = "http://nosvideo.com" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'nosvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
