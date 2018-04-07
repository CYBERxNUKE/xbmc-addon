# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nowdownload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re

from core import logger
from core import scrapertools


def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[nowdownload.py] get_video_url (page_url='%s')" % page_url)
    
    '''
    <a href="http://f02.nowdownload.co/dl/91efaa9ec507ef4de023cd62bb9a0fe2/50ab76ac/6711c9c90ebf3_family.guy.s11e02.italian.subbed.hdtv.xvid_gannico.avi" class="btn btn-danger"><i class="icon-white icon-download"></i> Download Now</a>
    '''
    data = scrapertools.cache_page( page_url )
    logger.debug("[nowdownload.py] data:" + data)
    try:
        url = scrapertools.get_match(data,'<a href="([^"]*)" class="btn btn-danger"><i class="icon-white icon-download"></i> Download Now</a>')
    except:
        #$.get("/api/token.php?token=7e1ab09df2775dbea02506e1a2651883");
    	token = scrapertools.get_match(data,'(/api/token.php\?token=[^"]*)')
    	logger.debug("[nowdownload.py] token:" + token)
    	d= scrapertools.cache_page( "http://www.nowdownload.co"+ token )
    	url = scrapertools.get_match(data,'expiryText: \'<a class="btn btn-danger" href="([^"]*)')
    	logger.debug("[nowdownload.py] url_1:" + url)
    	data = scrapertools.cache_page("http://www.nowdownload.co" + url )
    	logger.debug("[nowdownload.py] data:" + data)
    	#<a href="http://f03.nowdownload.co/dl/8ec5470153bb7a2177847ca7e1638389/50ab71b3/f92882f4d33a5_squadra.antimafia_palermo.oggi.4x01.episodio.01.ita.satrip.xvid_upz.avi" class="btn btn-success">Click here to download !</a>
    	url = scrapertools.get_match(data,'<a href="([^"]*)" class="btn btn-success">Click here to download !</a>')
    	logger.debug("[nowdownload.py] url_final:" + url)
    
    video_urls = [url]
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www.nowdownload.co/dl/9gwahc3577hj9
    #http://www.nowdownload.eu/dl/srv4g94wk6j7b
    patronvideos  = '(nowdownload.\w{2}/dl/[a-z0-9]+)'
    logger.info("[nowdownload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowdownload]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowdownload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
