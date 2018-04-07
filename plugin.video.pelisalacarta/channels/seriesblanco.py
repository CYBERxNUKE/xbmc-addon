# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re
import sys
import urlparse

from channelselector import get_thumb
from core import channeltools
from core import config
from core import logger
from core import scrapertools
from core import servertools
from core import httptools
from core.item import Item

from channels import filtertools


channel_xml = channeltools.get_channel_parameters("seriesblanco")
HOST = "http://seriesblanco.com/"
IDIOMAS = {'es': 'Español', 'en': 'Inglés', 'la': 'Latino', 'vo': 'VO', 'vos': 'VOS', 'vosi': 'VOSI', 'otro': 'OVOS'}
list_idiomas = IDIOMAS.values()
CALIDADES = ['SD', 'HDiTunes', 'Micro-HD-720p', 'Micro-HD-1080p', '1080p', '720p']

CAPITULOS_DE_ESTRENO_STR = "Capítulos de Estreno"

def mainlist(item):
    logger.info()

    thumb_series    = get_thumb("squares", "thumb_canales_series.png")
    thumb_series_az = get_thumb("squares", "thumb_canales_series_az.png")
    thumb_buscar    = get_thumb("squares", "thumb_buscar.png")

    itemlist = []
    itemlist.append(Item(channel=item.channel, title="Listado alfabético", action="series_listado_alfabetico",
                         thumbnail=thumb_series_az))
    itemlist.append(Item(channel=item.channel, title="Todas las series", action="series",
                         url=urlparse.urljoin(HOST, "listado/"), thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Capítulos de estreno", action="homeSection", extra=CAPITULOS_DE_ESTRENO_STR,
                         url=HOST , thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Último actualizado", action="homeSection", extra="Último Actualizado",
                         url=HOST , thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Series más vistas", action="series", extra="Series Más vistas",
                         url=urlparse.urljoin(HOST, "listado-visto/") , thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Series menos vistas", action="homeSection", extra="Series Menos vistas",
                         url=HOST , thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Últimas fichas creadas", action="series",
                         url=urlparse.urljoin(HOST, "fichas_creadas/"), thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Series por género", action="generos",
                         url=HOST , thumbnail=thumb_series))
    itemlist.append(Item(channel=item.channel, title="Buscar...", action="search", url=HOST, thumbnail=thumb_buscar))

    if filtertools.context:
        itemlist = filtertools.show_option(itemlist, item.channel, list_idiomas, CALIDADES)

    return itemlist

def homeSection(item):
    logger.info("section = {0}".format(item.extra))

    pattern = "['\"]panel-title['\"]>[^/]*{0}(.*?)(?:panel-title|\Z)".format(item.extra)
    logger.debug("pattern = {0}".format(pattern))

    data = httptools.downloadpage(item.url).data
    result = re.search(pattern, data, re.MULTILINE | re.DOTALL)

    if result:
        # logger.debug("found section: {0}".format(result.group(1)))
        item.extra = 1
        return extractSeriesFromData(item, result.group(1))
    
    logger.debug("No match")
    return []

def extractSeriesFromData(item, data):
    itemlist = []
    episodePattern = re.compile('/capitulo-([0-9]+)/')
    shows = re.findall("<a.+?href=['\"](?P<url>[^'\"]+)[^<]*<img[^>]*src=['\"](?P<img>http[^'\"]+).*?(?:alt|title)=['\"](?P<name>[^'\"]+)", data)
    for url, img, name in shows:
        try:
            name.decode('utf-8')
        except UnicodeError:
            name = unicode(name, "iso-8859-1", errors="replace").encode("utf-8")

        logger.debug("Show found: {name} -> {url} ({img})".format(name = name, url = url, img = img))
        itemlist.append(item.clone(title=name, url=urlparse.urljoin(HOST, url),
                                   action="episodios" if not episodePattern.search(url) else "findvideos", show=name, thumbnail=img,
                                   list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context))

    morePages = re.search('pagina=([0-9]+)">>>', data)
    if morePages:
        logger.debug("Adding next page item")
        itemlist.append(item.clone(title = "Siguiente >>", extra = item.extra + 1))

    if item.extra > 1:
        logger.debug("Adding previous page item")
        itemlist.append(item.clone(title = "<< Anterior", extra = item.extra - 1))

    return itemlist

def series(item):
    if not hasattr(item, 'extra') or not isinstance(item.extra, int):
        item.extra = 1

    pageURL = "{url}{merger}pagina={pageNo}".format(url = item.url, pageNo = item.extra, merger = '&' if '?' in item.url else '?')
    logger.info("url = {0}".format(pageURL))

    data = httptools.downloadpage(pageURL).data
    return extractSeriesFromData(item, data)



def series_listado_alfabetico(item):
    logger.info()

    return [item.clone(action="series", title=letra, url=urlparse.urljoin(HOST, "listado-{0}/".format(letra)))
                for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]


def generos(item):
    logger.info()
    data = httptools.downloadpage(item.url).data

    result = re.findall("href=['\"](?P<url>/listado/[^'\"]+)['\"][^/]+/i>\s*(?P<genero>[^<]+)", data)
    return [item.clone(action="series", title=genero, url = urlparse.urljoin(item.url, url)) for url, genero in result]


def newest(categoria):
    logger.info("categoria: {0}".format(categoria))
    itemlist = []
    try:
        if categoria == 'series':
            itemlist = homeSection(Item(extra = CAPITULOS_DE_ESTRENO_STR, url = HOST))

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def search(item, texto):
    logger.info("{0}".format(texto))
    texto = texto.replace(" ", "+")

    if texto == "":
        return []

    try:
        item.url = urlparse.urljoin(HOST, "/search.php?q1={0}&q2={1}".format(texto, texto.lower()))
        return series(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []

def episodios(item):
    logger.info("{0} - {1}".format(item.title, item.url))

    itemlist = []

    # Descarga la página
    data = httptools.downloadpage(item.url).data

    fanart = scrapertools.find_single_match(data, "background-image[^'\"]+['\"]([^'\"]+)")
    plot = scrapertools.find_single_match(data, "id=['\"]profile2['\"]>\s*(.*?)\s*</div>")

    logger.debug("fanart: {0}".format(fanart))
    logger.debug("plot: {0}".format(plot))

    ajaxSeasons = re.findall("['\"]loadSeason\((\d+),(\d+)\)", data)
    ajaxData = ""
    for showID, seasonNo in ajaxSeasons:
        logger.debug("Ajax seasson request: Show = {0} - Season = {1}".format(showID, seasonNo))
        ajaxData += httptools.downloadpage(HOST + '/ajax/load_season.php?season_id=' + showID + '&season_number=' + seasonNo).data

    if ajaxData:
        data = ajaxData

    episodes = re.findall("<tr.*?href=['\"](?P<url>[^'\"]+).+?>(?P<title>.+?)</a>.*?<td>(?P<flags>.*?)</td>", data, re.MULTILINE | re.DOTALL)
    for url, title, flags in episodes:
        idiomas = " ".join(["[{0}]".format(IDIOMAS.get(language, "OVOS")) for language in re.findall("banderas/([^\.]+)", flags, re.MULTILINE)])
        displayTitle = "{show} - {title} {languages}".format(show = item.show, title = title, languages = idiomas)
        logger.debug("Episode found {0}: {1}".format(displayTitle, urlparse.urljoin(HOST, url)))
        itemlist.append(item.clone(title=displayTitle, url=urlparse.urljoin(HOST, url),
                                   action="findvideos", plot=plot, fanart=fanart, language=idiomas,
                                   list_idiomas=list_idiomas, list_calidad=CALIDADES, context=filtertools.context))

    if len(itemlist) > 0 and filtertools.context:
        itemlist = filtertools.get_links(itemlist, item.channel)

    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(item.clone(title="Añadir esta serie a la biblioteca", action="add_serie_to_library", extra="episodios"))

    return itemlist


def parseVideos(item, typeStr, data):
    videoPatternsStr = [
        '<tr.+?<span>(?P<date>.+?)</span>.*?banderas/(?P<language>[^\.]+).+?href="(?P<link>[^"]+).+?servidores/'
        '(?P<server>[^\.]+).*?</td>.*?<td>.*?<span>(?P<uploader>.+?)</span>.*?<span>(?P<quality>.*?)</span>',
        '<tr.+?banderas/(?P<language>[^\.]+).+?<td[^>]*>(?P<date>.+?)</td>.+?href=[\'"](?P<link>[^\'"]+)'
        '.+?servidores/(?P<server>[^\.]+).*?</td>.*?<td[^>]*>.*?<a[^>]+>(?P<uploader>.+?)</a>.*?</td>.*?<td[^>]*>'
        '(?P<quality>.*?)</td>.*?</tr>'
    ]

    for vPatStr in videoPatternsStr:
        vPattIter = re.compile(vPatStr, re.MULTILINE | re.DOTALL).finditer(data)

        itemlist = []

        for vMatch in vPattIter:
            vFields = vMatch.groupdict()
            quality = vFields.get("quality")
            if not quality:
                quality = "SD"

            title = "{0} en {1} [{2}] [{3}] ({4}: {5})"\
                .format(typeStr, vFields.get("server"), IDIOMAS.get(vFields.get("language"), "OVOS"), quality,
                        vFields.get("uploader"), vFields.get("date"))
            itemlist.append(item.clone(title=title, fulltitle=item.title, url=urlparse.urljoin(HOST, vFields.get("link")),
                                       action="play", language=IDIOMAS.get(vFields.get("language"), "OVOS"),
                                       quality=quality, list_idiomas=list_idiomas, list_calidad=CALIDADES,
                                       context=filtertools.context))

        if len(itemlist) > 0 and filtertools.context:
            itemlist = filtertools.get_links(itemlist, item.channel)

        if len(itemlist) > 0:
            return itemlist

    return []


def extractVideosSection(data):
    return re.findall("panel-title(.+?)</div>[^<]*</div>[^<]*</div>", data, re.MULTILINE | re.DOTALL)


def findvideos(item):
    logger.info("{0} = {1}".format(item.show, item.url))

    # Descarga la página
    data = httptools.downloadpage(item.url).data
    # logger.info(data)

    online = extractVideosSection(data)


    try:
        filtro_enlaces = config.get_setting("filterlinks", item.channel)
    except:
        filtro_enlaces = 2

    list_links = []

    if filtro_enlaces != 0:
        list_links.extend(parseVideos(item, "Ver", online[0]))

    if filtro_enlaces != 1:
        list_links.extend(parseVideos(item, "Descargar", online[1]))

    return list_links


def play(item):
    logger.info("{0} - {1} = {2}".format(item.show, item.title, item.url))

    if item.url.startswith(HOST):
        data = httptools.downloadpage(item.url).data

        ajaxLink = re.findall("loadEnlace\((\d+),(\d+),(\d+),(\d+)\)", data)
        ajaxData = ""
        for serie, temp, cap, linkID in ajaxLink:
            logger.debug("Ajax link request: Sherie = {0} - Temp = {1} - Cap = {2} - Link = {3}".format(serie, temp, cap, linkID))
            ajaxData += httptools.downloadpage(HOST + '/ajax/load_enlace.php?serie=' + serie + '&temp=' + temp + '&cap=' + cap + '&id=' + linkID).data

        if ajaxData:
            data = ajaxData

        patron = "onclick='window.open\(\"([^\"]+)\"\);'/>"
        url = scrapertools.find_single_match(data, patron)
    else:
        url = item.url

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
