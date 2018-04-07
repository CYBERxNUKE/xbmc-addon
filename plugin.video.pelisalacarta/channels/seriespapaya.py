# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriespapaya
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

from core import config
from core import logger
from core import scrapertools
from core import httptools
from core.item import Item
from core import jsontools
from core import servertools
from channels import filtertools
import urlparse
import string
import urllib
import re
from channelselector import get_thumb

HOST="http://www.seriespapaya.com"

IDIOMAS = {'es': 'Español', 'lat': 'Latino', 'in': 'Inglés', 'ca': 'Catalán', 'sub': 'VOS'}
list_idiomas = IDIOMAS.values()
CALIDADES = ['360p', '480p', '720p HD', '1080p HD']


def mainlist(item):
    logger.info()

    thumb_series    = get_thumb("squares", "thumb_canales_series.png")
    thumb_series_az = get_thumb("squares", "thumb_canales_series_az.png")
    thumb_buscar    = get_thumb("squares", "thumb_buscar.png")

    itemlist = []
    itemlist.append(Item(action = "listado_alfabetico", title = "Listado Alfabetico", channel = item.channel, thumbnail = thumb_series_az))
    itemlist.append(Item(action = "novedades", title = "Capítulos de estreno", channel = item.channel, thumbnail = thumb_series))
    itemlist.append(Item(action = "search", title = "Buscar", channel = item.channel, thumbnail = thumb_buscar))


    if filtertools.context:
        itemlist = filtertools.show_option(itemlist, item.channel, list_idiomas, CALIDADES)

    return itemlist


def listado_alfabetico(item):
    logger.info()

    itemlist = [item.clone(action = "series_por_letra", title = "0-9")]
    for letra in string.ascii_uppercase:
        itemlist.append(item.clone(action = "series_por_letra", title = letra))

    return itemlist


def series_por_letra(item):
    logger.info("letra: {0}".format(item.title))
    item.letter = item.title.lower()
    item.extra = 0
    return series_por_letra_y_grupo(item)


def series_por_letra_y_grupo(item):
    logger.info("letra: {0} - grupo: {1}".format(item.letter, item.extra))
    itemlist=[]
    url = urlparse.urljoin(HOST, "autoload_process.php")

    postRequest = {
        "group_no": item.extra,
        "letra": item.letter.lower()
    }
    data = httptools.downloadpage(url, post = urllib.urlencode(postRequest)).data

    series = re.findall('list_imagen.+?src="(?P<img>[^"]+).+?<div class="list_titulo"><a[^>]+href="(?P<url>[^"]+)[^>]+>(.*?)</a>', data, re.MULTILINE | re.DOTALL)

    for img, url, name in series:
        itemlist.append(item.clone(
                             action    = "episodios",
                             title     = name,
                             show      = name,
                             url       = urlparse.urljoin(HOST, url),
                             thumbnail = urlparse.urljoin(HOST, img),
                             list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context
                             ))

    if len(series) == 8:
        itemlist.append(item.clone(title = "Siguiente >>", action = "series_por_letra_y_grupo", extra = item.extra + 1))

    if item.extra > 0:
        itemlist.append(item.clone(title = "<< Anterior", action = "series_por_letra_y_grupo", extra = item.extra - 1))

    return itemlist

def novedades(item):
    logger.info()
    data = httptools.downloadpage(HOST).data
    shows = re.findall('sidebarestdiv[^<]+<a[^<]+title="([^"]*)[^<]+href="([^"]*)[^<]+<img[^<]+src="([^"]+)', data, re.MULTILINE | re.DOTALL)

    itemlist = []

    for title, url, img in shows:
        itemlist.append(item.clone(action = "findvideos", title = title, url=urlparse.urljoin(HOST, url), thumbnail = img))

    return itemlist


def newest(categoria):
    logger.info("categoria: {0}".format(categoria))

    if categoria != 'series':
        return []

    try:
        return novedades(Item())

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))

    return []


def episodios(item):
    logger.info("url: {0}".format(item.url))

    data = httptools.downloadpage(item.url).data

    episodes = re.findall('visco.*?href="(?P<url>[^"]+).+?nbsp; (?P<title>.*?)</a>.+?ucapaudio.?>(?P<langs>.*?)</div>', data, re.MULTILINE | re.DOTALL)

    itemlist = []
    for url, title, langs in episodes:
        languages = " ".join(["[{0}]".format(IDIOMAS.get(lang, lang)) for lang in re.findall('images/s-([^\.]+)', langs)])
        itemlist.append(item.clone(action      = "findvideos",
                                   title       = "{0} {1} {2}".format(item.title, title, languages),
                                   url         = urlparse.urljoin(HOST, url),
                                   language    = languages,
                                   list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context
                            ))

    if len(itemlist) > 0 and filtertools.context:
        itemlist = filtertools.get_links(itemlist, item.channel)

    # Opción "Añadir esta serie a la biblioteca de XBMC"
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(item.clone(title="Añadir esta serie a la biblioteca", action="add_serie_to_library", extra="episodios"))

    return itemlist


def search(item, texto):
    logger.info("texto: {0}".format(texto))
    data = httptools.downloadpage(urlparse.urljoin(HOST, "/buscar.php?term={0}".format(texto))).data
    jsonResult = jsontools.load_json(data)
    tvShows = jsonResult["myData"]

    return [item.clone(action      = "episodios",
                       title       = show["titulo"],
                       show        = show["titulo"],
                       url         = urlparse.urljoin(HOST, show["urla"]),
                       thumbnail   = urlparse.urljoin(HOST, show["img"]),
                       list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context
                ) for show in tvShows ]


def findvideos(item):
    logger.info("url: {0}".format(item.url))

    data = httptools.downloadpage(item.url).data

    expr = 'mtos'                                                 + '.+?'+ \
           '<div.+?images/(?P<lang>[^\.]+)'                       + '.+?'+ \
           '<div[^>]+>\s+(?P<date>[^\s<]+)'                       + '.+?'+ \
           '<div.+?img.+?>\s*(?P<server>.+?)</div>'               + '.+?'+ \
           '<div.+?href="(?P<url>[^"]+).+?images/(?P<type>[^\.]+)' + '.+?'+ \
           '<div[^>]+>\s*(?P<quality>.*?)</div>'                  + '.+?'+ \
           '<div.+?<a.+?>(?P<uploader>.*?)</a>'

    links = re.findall(expr, data, re.MULTILINE | re.DOTALL)

    itemlist = [item.clone(
                     action    = "play",
                     title     = "{linkType} en {server} [{lang}] [{quality}] ({uploader}: {date})".format(linkType="Ver" if linkType != "descargar" else "Descargar",
                                                                                                           lang=IDIOMAS.get(lang, lang),
                                                                                                           date=date,
                                                                                                           server=server.rstrip(),
                                                                                                           quality=quality,
                                                                                                           uploader=uploader),
                     url       = urlparse.urljoin(HOST, url),
                     language  = IDIOMAS.get(lang, lang),
                     quality   = quality,
                     list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context
                ) for lang, date, server, url, linkType, quality, uploader in links ]

    if len(itemlist) > 0 and filtertools.context:
        itemlist = filtertools.get_links(itemlist, item.channel)

    return itemlist

def play(item):
    logger.info("play: {0}".format(item.url))
    data = httptools.downloadpage(item.url).data
    videoURL = scrapertools.find_single_match(data, "location.href='([^']+)")
    logger.debug("Video URL = {0}".format(videoURL))
    itemlist = servertools.find_video_items(data=videoURL)
    return itemlist
