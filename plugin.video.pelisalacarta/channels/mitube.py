# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - WIIMC Plugin
# Canal para mitube (por GASMURO)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import jsontools as json
import os
import re
import sys
import time
import urllib2

from lib import pafy

if sys.version_info[:2] >= (3, 0):
    # pylint: disable=E0611,F0401
    uni, byt, xinput = str, bytes, input
    from urllib.parse import urlencode
else:
    uni, byt, xinput = unicode, str, raw_input
    uni = unicode
    from urllib import urlencode

    


from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")


ANIMEFLV_REQUEST_HEADERS = []
ANIMEFLV_REQUEST_HEADERS.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept-Encoding","gzip, deflate"])
ANIMEFLV_REQUEST_HEADERS.append(["Cache-Control","max-age=0"])
ANIMEFLV_REQUEST_HEADERS.append(["Connection","keep-alive"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept","text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"])
ANIMEFLV_REQUEST_HEADERS.append(["Accept-Language","es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3"])


def mainlist(item):
    logger.info("[mitube.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=item.channel, action="search"        , title="Buscar"              , url="https://www.googleapis.com/youtube/v3/search" ))
  
    return itemlist




def utf8_encode(x):
    """ Encode Unicode. """
    return x.encode("utf8") if type(x) == uni else x

def generate_search_qs(term, page, result_count=None):
    """ Return query string. """
   
    aliases = dict(views='viewCount')
    term = utf8_encode(term)
    qs = {
        'q': term,
        'maxResults': 50,
        'safeSearch': "none",
        'order': 'relevance',
        'part': 'id,snippet',
        'type': 'video',
        'key': "AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo"
    }


    return qs


def search(item,texto):
    logger.info("[mitube.py] search")
    term=texto

    original_term = term
    print ("search for %s", original_term)
    url = "https://www.googleapis.com/youtube/v3/search"
    query = generate_search_qs(urllib2.unquote(term), 1)
    ##have_results = _search(url, original_term, query)
    if query:
      item.url = url + "?" + urlencode(query) 
    else:
      item.url = url
    # use cached value if exists

    try:
    	return series(item)
   # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            print line        
            logger.error( "%s" % line )
        return []


def get_tracks_from_json(jsons):
    """ Get search results from web page. """
    try:
        items = jsons['data']['items']
       
    except KeyError:
        items = []

    songs = []

    for item in items:
        ytid = item['id']
        cursong = Video(ytid=ytid, title=item['title'].strip(),
                        length=int(item['duration']))

        likes = item.get('likeCount', "0")
        likes = int(re.sub(r"\D", "", likes))
        total = item.get('ratingCount', 0)
        dislikes = total - likes
        g.meta[ytid] = dict(
            rating=uni(item.get('rating', "0."))
            [:4].ljust(4, "0"),
            uploader=item['uploader'],
            category=item['category'],
            aspect=item.get('aspectRatio', "custom"),
            uploaded=yt_datetime(item['uploaded'])[1],
            likes=uni(num_repr(likes)),
            dislikes=uni(num_repr(dislikes)),
            commentCount=uni(num_repr(item.get('commentCount', 0))),
            viewCount=uni(num_repr(item.get("viewCount", 0))),
            title=item['title'],
            length=uni(fmt_time(cursong.length)))

        songs.append(cursong)

    if not items:
        dbg("got unexpected data or no search results")
        return False

    return songs


def fmt_time(seconds):
    """ Format number of seconds to %H:%M:%S. """
    hms = time.strftime('%H:%M:%S', time.gmtime(int(seconds)))
    H, M, S = hms.split(":")

    if H == "00":
        hms = M + ":" + S

    elif H == "01" and int(M) < 40:
        hms = uni(int(M) + 60) + ":" + S

    elif H.startswith("0"):
        hms = ":".join([H[1], M, S])

    return hms




def series(item):
    logger.info("[mitube.py] series")
      
    # Descarga la pagina
   # print item.url
    data = scrapertools.cache_page(item.url)
 #, headers = ANIMEFLV_REQUEST_HEADERS)
   # print data
    wdata = json.load_json(data)
  #  songs = get_tracks_from_json(wdata)
    try:
        items = wdata['items']
  
    except KeyError:
        items = []

    itemlist = []
    ##print items

    for item in items:
        ytid = item['id']['videoId']
        title= item['snippet']['title'].encode('ascii','ignore')
        url="https://www.youtube.com/watch?v="+ytid
        thumbnail=item['snippet']['thumbnails']['default']['url'].replace('https','http')
        show=""
        #plot=fmt_time(item['duration'])
        plot=""
       ## print "title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"], plot[="+plot+"]"
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"], plot[="+plot+"]")
        ##itemlist.append( Item(channel=item.channel, action="play", server="youtube",title=title, url=url , thumbnail=thumbnail , fanart=thumbnail,  folder=False) )
        itemlist.append( Item(channel=item.channel, action="ver",title=title+" "+plot, url=url , thumbnail=thumbnail ,plot=plot, viewmode="movie_with_plot") )
     
    return itemlist




def descargabg(item):
    logger.info("[mitube.py] get_video_url(page_url='%s')" % item.url)
    os.system('echo 2|mpsyt dlurl '+item.url+' &')
    itemlist = []
    itemlist.append( Item(title='Bajando'))
    itemlist.append( Item(title='Para ver el video ve a la carpeta youtube y busca el archivo'))
    
    return itemlist

def ver(item):
    logger.info("[mitube.py] get_video_url(page_url='%s')" % item.url)
   # os.system('echo 2|mpsyt dlurl '+item.url+' &')
    video = pafy.new(item.url)
    
    itemlist = []
    streams = video.streams
    for s in streams:
	    itemlist.append( Item(channel=item.channel, action="play", server="directo", title=s.resolution+" "+s.extension, url=s.url , thumbnail=item.thumbnail , fanart=item.thumbnail,  folder=False))
	   # para wiimc itemlist.append( Item(channel=item.channel, action="play_video", server="directo", title=s.resolution+" "+s.extension, url=s.url , thumbnail=item.thumbnail , fanart=item.thumbnail,  folder=False))
    itemlist.append( Item(channel=item.channel, action="descargabg",title="descargar", url=item.url , thumbnail=item.thumbnail ,plot=item.plot) )

    return itemlist
