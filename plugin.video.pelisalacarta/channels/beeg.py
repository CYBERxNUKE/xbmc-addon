# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para beeg.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import sys
import urllib
from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import jsontools as json

DEBUG = config.get_setting("debug")

url_api = ""
beeg_salt = ""

def get_api_url():
  global url_api
  global beeg_salt
  data = scrapertools.downloadpage("http://beeg.com")
  version = re.compile('<script src="//static.beeg.com/cpl/([\d]+).js"').findall(data)[0]
  js_url  = "http:" + re.compile('<script src="(//static.beeg.com/cpl/[\d]+.js)"').findall(data)[0]
  url_api = "https://api2.beeg.com/api/v6/"+ version
  data = scrapertools.downloadpage(js_url)
  beeg_salt = re.compile('beeg_salt="([^"]+)"').findall(data)[0]

  
def decode(key):
  a = beeg_salt
  e = unicode(urllib.unquote(key), "utf8")
  t = len(a)
  o =""
  for n in range(len(e)):
    r= ord(e[n:n+1])
    i =  n % t
    s = ord(a[i:i+1]) % 21
    o += chr(r-s)
    
  n = []
  for x in range(len(o),0,-3):
    if x >=3:
      n.append(o[(x -3):x])
    else:
      n.append(o[0:x])
    
  return "".join(n)

get_api_url()


def mainlist(item):
    logger.info("[beeg.py] mainlist")
    get_api_url()
    itemlist = []
    itemlist.append( Item(channel=item.channel, action="videos"            , title="Útimos videos"       , url=url_api + "/index/main/0/pc", viewmode="movie"))
    itemlist.append( Item(channel=item.channel, action="listcategorias"    , title="Listado categorias"  , url=url_api + "/index/main/0/pc"))
    itemlist.append( Item(channel=item.channel, action="search"            , title="Buscar"              , url=url_api + "/index/search/0/pc?query=%s" ))
    return itemlist

def videos(item):
    logger.info("[beeg.py] videos")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    JSONData = json.load_json(data)
    
    
    for Video in JSONData["videos"]:
      thumbnail = "http://img.beeg.com/236x177/" + Video["id"].encode("utf8") +  ".jpg"
      url = url_api + "/video/" + Video["id"].encode("utf8")
      title = Video["title"].encode("utf8")
      itemlist.append( Item(channel=item.channel, action="play" , title=title , url=url, thumbnail=thumbnail, plot="", show="", folder=True))
      
    #Paginador
    Actual = int(scrapertools.get_match(item.url,url_api + '/index/[^/]+/([0-9]+)/pc'))
    if JSONData["pages"]-1 > Actual:
      scrapedurl = item.url.replace("/"+str(Actual)+"/", "/"+str(Actual+1)+"/")
      itemlist.append( Item(channel=item.channel, action="videos", title="Página Siguiente" , url=scrapedurl , thumbnail="" , folder=True, viewmode="movie") )


    
    return itemlist

def listcategorias(item):
    logger.info("[beeg.py] listcategorias")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    JSONData = json.load_json(data)
    
    
    for Tag in JSONData["tags"]["popular"]:
      url = url_api + "/index/tag/0/pc?tag=" + Tag.encode("utf8")
      title = Tag.encode("utf8")
      title = title[:1].upper() + title[1:]
      itemlist.append( Item(channel=item.channel, action="videos" , title=title , url=url, folder=True, viewmode="movie"))

    return itemlist
  
def search(item,texto):
    logger.info("[beeg.py] search")

    texto = texto.replace(" ","+")
    item.url = item.url % (texto)
    try:
        return videos(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
        
def play(item):
    logger.info("[beeg.py] findvideos")
    itemlist = []
    data = scrapertools.downloadpage(item.url)

    JSONData = json.load_json(data)
    for key in JSONData:
      videourl = re.compile("([0-9]+p)",re.DOTALL).findall(key)
      if videourl: 
        videourl= videourl[0]
        if not JSONData[videourl] == None:
          url = JSONData[videourl].encode("utf8")
          url = url.replace("{DATA_MARKERS}","data=pc.ES")
          viedokey = re.compile("key=(.*?)%2Cend=",re.DOTALL).findall(url)[0]
          
          url = url.replace(viedokey,decode(viedokey))
          if not url.startswith("https:"): url = "https:" + url
          title = videourl.encode("utf8")
          itemlist.append( Item(channel=item.channel, action="play" , fulltitle=item.title, title=title , url=url, thumbnail=item.thumbnail, server="directo", folder=False))
      
    itemlist.sort(key=lambda item: item.fulltitle.lower(), reverse=True)
    return itemlist
