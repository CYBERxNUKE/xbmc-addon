# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Conector para eroshare por Hernan_Ar_c
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from core import httptools


# def test_video_exists(page_url):
#     logger.info("(page_url='%s')" % page_url)
#     data = httptools.downloadpage(page_url).data

#     if "File was deleted" in data:
#         return False, "[eroshare] El archivo no existe o ha sido borrado"

#     return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[eroshare.py] url=" + page_url)
    video_urls = []
    data = httptools.downloadpage(page_url).data
    url = scrapertools.find_single_match(data,'"url_mp4":"(.*?)"')
    video_urls.append(['eroshare', url])

    #for video_url in video_urls:
    #    logger.info("pelisalacarta.servers.eroshare %s - %s" % (video_url[0],video_url[1]))
    
    return video_urls

def find_videos(page_url):
    encontrados = set()
    devuelve = []
    titulo = "[eroshare]"
    url = scrapertools.find_single_match(page_url,'(https://eroshare.com/embed/[a-zA-Z0-9]+)')
    if len(url)>0 and url not in encontrados:
        logger.info("  url=" + url)
        devuelve.append([titulo, url, 'eroshare'])
        encontrados.add(url)
        logger.info("  url duplicada=" + url)
    
    return devuelve
