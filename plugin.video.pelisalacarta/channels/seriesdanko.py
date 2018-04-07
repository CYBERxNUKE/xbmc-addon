# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import urlparse

from channels import filtertools
from core import config
from core import httptools
from core import logger
from core import scrapertools
from core import servertools
from core.item import Item

HOST = 'http://seriesdanko.com/'
IDIOMAS = {'es': 'Español', 'la': 'Latino', 'vos': 'VOS', 'vo': 'VO'}
list_idiomas = IDIOMAS.values()
CALIDADES = ['SD', 'MicroHD', 'HD/MKV']


def mainlist(item):
    logger.info()

    itemlist = list()
    itemlist.append(Item(channel=item.channel, title="Novedades", action="novedades", url=HOST))
    itemlist.append(Item(channel=item.channel, title="Más vistas", action="mas_vistas", url=HOST))
    itemlist.append(Item(channel=item.channel, title="Listado Alfabético", action="listado_alfabetico", url=HOST))
    itemlist.append(Item(channel=item.channel, title="Todas las series", action="listado_completo", url=HOST))
    itemlist.append(Item(channel=item.channel, title="Buscar...", action="search",
                         url=urlparse.urljoin(HOST, "all.php")))

    if filtertools.context:
        itemlist = filtertools.show_option(itemlist, item.channel, list_idiomas, CALIDADES)

    return itemlist


def novedades(item):
    logger.info()

    itemlist = list()

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)
    data = re.sub(r"<!--.*?-->", "", data)

    patron = '<a title="([^"]+)" href="([^"]+)".*?>'
    patron += "<img.*?src='([^']+)'"
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl, scrapedthumb in matches:
        # patron = "^(.*?)(?:Ya Disponible|Disponible|Disponbile|disponible|\(Actualizada\))$"
        # match = re.compile(patron, re.DOTALL).findall(scrapedtitle)
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        show = scrapertools.find_single_match(title, "^(.+?) \d+[x|X]\d+")

        itemlist.append(Item(channel=item.channel, title=title, url=urlparse.urljoin(HOST, scrapedurl),
                        action="episodios", thumbnail=scrapedthumb, show=show, context=filtertools.context,
                             list_idiomas=list_idiomas))

    return itemlist


def mas_vistas(item):
    logger.info()

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)
    data = re.sub(r"<!--.*?-->", "", data)

    patron = "<div class='widget HTML' id='HTML3'.+?<div class='widget-content'>(.*?)</div>"
    data = scrapertools.get_match(data, patron)

    return series_seccion(item, data)


def listado_completo(item):
    logger.info()

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)
    data = re.sub(r"<!--.*?-->", "", data)
    patron = '<div class="widget HTML" id="HTML10".+?<div class="widget-content">(.*?)</div>'
    data = scrapertools.get_match(data, patron)

    return series_seccion(item, data)


def series_seccion(item, data):
    logger.info()

    itemlist = []
    patron = "<a href='([^']+)'.*?>(.*?)</a>"
    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedtitle in matches:
        itemlist.append(Item(channel=item.channel, action="episodios", title=scrapedtitle, show=scrapedtitle,
                             url=urlparse.urljoin(HOST, scrapedurl), context=filtertools.context,
                             list_idiomas=list_idiomas))

    return itemlist


def listado_alfabetico(item):
    logger.info()

    itemlist = []

    for letra in '0ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        itemlist.append(Item(channel=item.channel, action="series_por_letra", title=letra,
                             url=urlparse.urljoin(HOST, "series.php?id={letra}".format(letra=letra))))

    return itemlist


def series_por_letra(item):
    logger.info("letra = {0}".format(item.title))
    data = httptools.downloadpage(item.url).data

    shows = re.findall("<a href='(?P<url>[^']+)' title='Capitulos de: (?P<title>.+?)'><img.+?src='(?P<img>[^']+)", data)
    itemlist = []
    for url, title, img in shows:
        itemlist.append(item.clone(title=title, url=urlparse.urljoin(HOST, url), action="episodios", thumbnail=img,
                                   show=title, context=filtertools.context, list_idiomas=list_idiomas))
    return itemlist


def search(item, texto):
    logger.info("texto={0}".format(texto))

    itemlist = []

    try:
        data = httptools.downloadpage(item.url).data
        shows = re.findall("<a href='(?P<url>/serie.php\?serie=[0-9]+)'[^>]*>(?P<title>[^<]*{0}[^<]*)".format(texto),
                           data, re.IGNORECASE)
        for url, title in shows:
            itemlist.append(item.clone(title=title, url=urlparse.urljoin(HOST, url), action="episodios", show=title,
                                       context=filtertools.context, list_idiomas=list_idiomas))

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)

    return itemlist


def episodios(item):
    logger.info()

    itemlist = []

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)
    data = re.sub(r"<!--.*?-->", "", data)

    data = re.sub(r"a> <img src=/assets/img/banderas/", "a><idioma>", data)
    data = re.sub(r"<img src=/assets/img/banderas/", "|", data)
    data = re.sub(r"\.png border='\d+' height='\d+' width='\d+'[^>]+>\s+<", "</idioma><", data)
    data = re.sub(r"\.png border='\d+' height='\d+' width='\d+'[^>]+>", "", data)

    patron = '<div id="T1".*?'
    patron += "<img src='([^']+)'"
    matches = re.compile(patron, re.DOTALL).findall(data)
    if len(matches) > 0:
        thumbnail = matches[0]
    else:
        thumbnail = item.thumbnail

    patron = "<a href='([^']+)'>(.*?)</a><idioma>(.*?)</idioma>"
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedidioma in matches:
        idioma = ""
        for i in scrapedidioma.split("|"):
            idioma += " [" + IDIOMAS.get(i, "OVOS") + "]"
        title = scrapedtitle + idioma

        itemlist.append(Item(channel=item.channel, title=title, url=urlparse.urljoin(HOST, scrapedurl),
                             action="findvideos", show=item.show, thumbnail=thumbnail, plot="", language=idioma,
                             list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context))

    if len(itemlist) > 0 and filtertools.context:
            itemlist = filtertools.get_links(itemlist, item.channel)

    # Opción "Añadir esta serie a la biblioteca de XBMC"
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(item.clone(title="Añadir esta serie a la biblioteca", action="add_serie_to_library",
                                   extra="episodios"))

    return itemlist


def findvideos(item):
    logger.info()

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)
    data = re.sub(r"<!--.*?-->", "", data)

    online = re.findall('<table class=.+? cellpadding=.+? cellspacing=.+?>(.+?)</table>', data,
                        re.MULTILINE | re.DOTALL)

    return parse_videos(item, "Ver", online[0]) + parse_videos(item, "Descargar", online[1])


def parse_videos(item, tipo, data):
    logger.info()

    itemlist = []

    pattern = "<td.+?<img src='/assets/img/banderas/([^\.]+).+?</td><td.+?>(.*?)</td><td.+?" \
              "<img src='/assets/img/servidores/([^\.]+).+?</td><td.+?href='([^']+)'.+?>.*?</a></td>" \
              "<td.+?>(.*?)</td>"

    links = re.findall(pattern, data, re.MULTILINE | re.DOTALL)

    for language, date, server, link, quality in links:
        if quality == "":
            quality = "SD"
        title = "{tipo} en {server} [{idioma}] [{quality}] ({fecha})".\
            format(tipo=tipo, server=server, idioma=IDIOMAS.get(language, "OVOS"), quality=quality, fecha=date)

        itemlist.append(Item(channel=item.channel, title=title, url=urlparse.urljoin(HOST, link), action="play",
                             show=item.show, language=IDIOMAS.get(language, "OVOS"), quality=quality,
                             list_idiomas=list_idiomas, list_calidad=CALIDADES, fulltitle=item.title,
                             context=filtertools.context))
        # context=CONTEXT+"|guardar_filtro"))

    if len(itemlist) > 0 and filtertools.context:
        itemlist = filtertools.get_links(itemlist, item.channel)

    return itemlist


def play(item):
    logger.info("play url={0}".format(item.url))

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;|<Br>|<BR>|<br>|<br/>|<br />|-\s", "", data)

    patron = '<div id="url2".*?><a href="([^"]+)">.+?</a></div>'
    url = scrapertools.find_single_match(data, patron)

    itemlist = servertools.find_video_items(data=url)
    titulo = scrapertools.find_single_match(item.fulltitle, "^(.*?)\s\[.+?$")
    if titulo:
        titulo += " [{language}]".format(language=item.language)

    for videoitem in itemlist:
        if titulo:
            videoitem.title = titulo
        else:
            videoitem.title = item.title
        videoitem.channel = item.channel

    return itemlist
