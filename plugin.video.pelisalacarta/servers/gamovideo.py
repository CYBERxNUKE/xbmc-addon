# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para gamovideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import httptools
from core import logger
from core import scrapertools
from lib import jsunpack

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url, headers=headers).data

    if ("File was deleted" or "Not Found" or "File was locked by administrator") in data:
        return False, "[Gamovideo] El archivo no existe o ha sido borrado"
    if "Video is processing now" in data:
        return False, "[Gamovideo] El video está procesándose en estos momentos. Inténtelo mas tarde."

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url, headers=headers).data

    packer = scrapertools.find_single_match(data,
                                            "<script type='text/javascript'>(eval.function.p,a,c,k,e,d..*?)</script>")
    if packer != "":
        unpacker = jsunpack.unpack(data)
    else:
        unpacker = ""
    if unpacker != "": data = unpacker

    data = re.sub(r'\n|\t|\s+', '', data)

    host = scrapertools.find_single_match(data, '\[\{image:"(http://[^/]+/)')
    mediaurl = scrapertools.find_single_match(data, ',\{file:"([^"]+)"')
    if not mediaurl.startswith(host):
        mediaurl = host + mediaurl
   
    rtmp_url = scrapertools.find_single_match(data, 'file:"(rtmp[^"]+)"')
    playpath = scrapertools.find_single_match(rtmp_url, 'vod\?h=[\w]+/(.*$)')
    rtmp_url = rtmp_url.split(playpath)[
                   0] + " playpath=" + playpath + " swfUrl=http://gamovideo.com/player61/jwplayer.flash.swf"

    video_urls = []
    video_urls.append(["RTMP [gamovideo]", rtmp_url])
    video_urls.append([scrapertools.get_filename_from_url(mediaurl)[-4:] + " [gamovideo]", mediaurl])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://gamovideo.com/auoxxtvyoy
    # http://gamovideo.com/h1gvpjarjv88
    # http://gamovideo.com/embed-sbb9ptsfqca2-588x360.html
    patronvideos = 'gamovideo.com/(?:embed-|)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gamovideo]"
        url = "http://gamovideo.com/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'gamovideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
