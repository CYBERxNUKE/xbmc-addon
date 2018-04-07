# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para datoporn
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if 'File Not Found' in data or '404 Not Found' in data:
        return False, "[Datoporn] El archivo no existe o ha sido borrado" 

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = httptools.downloadpage(page_url).data

    media_urls = scrapertools.find_multiple_matches(data, 'file\:"([^"]+\.mp4)",label:"([^"]+)"')
    if not media_urls:
        match = scrapertools.find_single_match(data, "<script type='text/javascript'>(.*?)</script>")
        data = jsunpack.unpack(match)
        media_urls = scrapertools.find_multiple_matches(data, '\[\{file\:"([^"]+)"')

    # Extrae la URL
    calidades = []
    video_urls = []
    for media_url in sorted(media_urls, key= lambda x:int(x[1][-3:])):
        calidades.append(int(media_url[1][-3:]))
        try:
            title = ".%s %sp [datoporn]" % (media_url[0].rsplit('.',1)[1], media_url[1][-3:])
        except:
            title = ".%s %sp [datoporn]" % (media_url[-4:], media_url[1][-3:])
        video_urls.append([title, media_url[0]])

    sorted(calidades)
    m3u8 = scrapertools.find_single_match(data,'file\:"([^"]+\.m3u8)"')
    if m3u8:
        video_urls.insert(0, [".m3u8 %s [datoporn]" % calidades[-1], m3u8])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = '(?:datoporn.com|dato.porn)/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)
    for match in matches:
        titulo = "[datoporn]"
        url = "http://dato.porn/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'datoporn'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
