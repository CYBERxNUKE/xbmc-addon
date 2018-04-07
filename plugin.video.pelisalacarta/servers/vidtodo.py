# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidtodo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core.scrapertools import *

host = "http://vidtodo.com"
id_server = "vidtodo" 

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[%s.py] get_video_url(page_url='%s')" % (id_server, page_url))

    data = cache_page(page_url).replace('"',"'")

    page_url_post = find_single_match(data, "<Form method='POST' action='([^']+)'>")
    imhuman = "&imhuman=" + find_single_match(data, "name='imhuman' value='([^']+)'").replace(" ","+")
    post = urllib.urlencode({k:v for k, v in find_multiple_matches(data, "name='([^']+)' value='([^']*)'")}) + imhuman

    time.sleep(1)
    data = cache_page(page_url_post, post=post)

    sources = get_match(data, 'sources: \[([^\]]+)\]')
    video_urls = []
    for media_url in find_multiple_matches(sources, '"([^"]+)"'):
        if media_url.endswith(".mp4"):
            video_urls.append([".mp4 [%s]" % id_server, media_url])

        if media_url.endswith(".m3u8"):
            video_urls.append(["M3U8 [%s]" % id_server, media_url])

        if media_url.endswith(".smil"):
            smil_data = cache_page(media_url)

            rtmp = get_match(smil_data , 'base="([^"]+)"')
            playpaths = find_multiple_matches(smil_data , 'src="([^"]+)" height="(\d+)"')

            mp4 = "http:" + get_match(rtmp, '(//[^:]+):') + "/%s/" + \
                  get_match(data,'"Watch video ([^"]+")').replace(' ', '.') + ".mp4"

            for playpath, inf in playpaths:
                h = get_match(playpath, 'h=([a-z0-9]+)')
                video_urls.append([".mp4 [%s] %s" % (id_server, inf), mp4 % h])
                video_urls.append(["RTMP [%s] %s" % (id_server, inf), "%s playpath=%s" % (rtmp, playpath)])

    for video_url in video_urls:
        logger.info("[%s.py] video_url: %s - %s" % (id_server, video_url[0], video_url[1]))

    return video_urls

def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://vidtodo.com/y4thgmqe5mgz
    patronvideos  = "%s.com/([a-z0-9]+)" % id_server
    logger.info("[%s.py] find_videos #" % id_server + patronvideos + "#")

    matches = find_multiple_matches(text, patronvideos)

    for match in matches:
        titulo = "[%s]" % id_server
        url = host + "/%s" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, id_server])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
