# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rapidvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urllib

from core import httptools
from core import logger
from core import scrapertools


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url="+page_url)
    video_urls = []

    data = get_data(page_url)
    urls = scrapertools.find_multiple_matches(data, '"file":"([^"]+)".*?"res":"([^"]+)"')
    for mediaurl, res in urls:
        ext = scrapertools.get_filename_from_url(mediaurl)[-4:]
        video_urls.append(['%s %sp [rapidvideo]' % (ext, res), mediaurl.replace("\\", "")])
    
    return video_urls


# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []
            
    #http://www.rapidvideo.com/e/YK7A0L7FU3A
    patronvideos = 'rapidvideo.(?:org|com)/(?:\?v=|e/)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "https://www.rapidvideo.com/e/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'rapidvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)


    return devuelve


def get_data(url_orig):
    try:
        response = httptools.downloadpage(url_orig)
        if not response.data or "urlopen error [Errno 1]" in str(response.code):
            raise Exception
    except:
        import random
        server_random = ['nl', 'de', 'us']
        server = server_random[random.randint(0, 2)]
        url = "https://%s.hideproxy.me/includes/process.php?action=update" % server
        post = "u=%s&proxy_formdata_server=%s&allowCookies=1&encodeURL=0&encodePage=0&stripObjects=0&stripJS=0&go=" \
               % (urllib.quote(url_orig), server)
        while True:
            response = httptools.downloadpage(url, post, follow_redirects=False)
            if response.headers.get("location"):
                url = response.headers["location"]
                post = ""
            else:
                break

    return response.data
