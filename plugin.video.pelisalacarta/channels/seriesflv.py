# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesflv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re
import sys
import urlparse

from core import config
from core import logger
from core import scrapertools
from core import servertools
from core import httptools
from core.item import Item

CHANNEL_HOST = 'http://www.seriesflv.net/'


def mainlist(item):
    logger.info()

    itemlist = list()
    itemlist.append(Item(channel=item.channel, action="menuepisodios", title="Últimos episodios..."))
    itemlist.append(Item(channel=item.channel, action="series_listado_alfabetico", title="Listado alfabético"))
    itemlist.append(Item(channel=item.channel, action="series", title="Todas las series",
                         url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=series&order=titulo"))
    itemlist.append(Item(channel=item.channel, action="series", title="Series más vistas",
                         url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=series&order=hits"))
    itemlist.append(Item(channel=item.channel, action="series", title="Telenovelas",
                         url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=generos&order=novelas"))
    itemlist.append(Item(channel=item.channel, action="series", title="Animes",
                         url="http://www.seriesflv.net/ajax/lista.php", extra="grupo_no=0&type=generos&order=anime"))
    itemlist.append(Item(channel=item.channel, action="search", title="Buscar...",
                         url="http://www.seriesflv.net/api/search/?q="))

    return itemlist


def compara(x,y):
    return cmp(x.title,y.title)


def series_listado_alfabetico(item):
    logger.info()

    return [item.clone(action="seriesletra", title=letra, url="http://www.seriesflv.net/ajax/lista.php",
                extra="grupo_no=0&type=letra&order={0}".format(str(letra.lower())))
                for letra in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"]


def seriesletra(item):
    logger.info()

    # Descarga la pagina
    post = item.extra
    data = httptools.downloadpage(item.url, post=post, add_referer=True).data

    # Extrae las entradas (carpetas)
    '''
    <article data-item="lista" class="item lista" id="serieItems">
    	<a href="http://www.seriesflv.net/serie/fuuka.html">
        <div class="image"><img src="http://http-s.ws/ysk/img/data/4928aef967b52928cb181a19c81b158c-size-90x120-a.jpg"></div>
        <div class="info">
        <div class="title">Fuuka</div>
        <div class="sinopsis">Yuu Haruna acaba de mudarse a una nueva ciudad, lo que no evita que siga yendo como un zombi por la calle debido a su adicción a Twitter. Caminando por su nuevo entorno se topa con una chica llamada Fuuka Akitsuki, quien le rompe el teléfono enfadada pensando que lo que el muchacho intentaba era sacarle una foto de sus bragas. El encuentro entre ambos cambiará sus vidas?</div>
        <div class="otros">
        <b>Año:</b> 2017 | <b>View's:</b> 1,248 veces
        </div>
        </div>
        </a>
    </article>
    '''
    patron = "<article[^<]+<a href=['\"](?P<url>[^'\"]+)[^<]+<div[^<]+<img src=['\"](?P<img>http[^'\"]+).+[^<]+<div[^<]+<div class=['\"]title['\"]>(?P<name>[^'\"]+)</div>"
    matches = re.compile(patron).findall(data)
    itemlist = []

    for eurl, eimg, ename in matches:
    
        title = ename.strip()
        thumbnail = urlparse.urljoin(item.url, eimg)
        plot = ""
        url = urlparse.urljoin(item.url, eurl)
        itemlist.append(Item(channel=item.channel, action="episodios", title=title, url=url, thumbnail=thumbnail,
                             plot=plot, show=title))
        
        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
    
    longlist = len(itemlist)
    itemlist.sort(compara)
    # grupo_no=0&type=letra&order=a
    old_offset = scrapertools.find_single_match(item.extra, "grupo_no\=(\d+)")
    if int(old_offset) > 0:
        atras_offset = str(int(old_offset)-1)
        atrasextra = item.extra.replace("grupo_no="+old_offset, "grupo_no="+atras_offset)
        itemlist.append(Item(channel=item.channel, action="seriesletra", title="<< Anterior", extra=atrasextra,
                             url=item.url))
    if longlist >= 20:
        new_offset = str(int(old_offset)+1)
        newextra = item.extra.replace("grupo_no="+old_offset, "grupo_no="+new_offset)
        itemlist.append(Item(channel=item.channel, action="seriesletra", title=">> Siguiente", extra=newextra,
                             url=item.url))

    return itemlist


def menuepisodios(item):
    logger.info()

    itemlist = list()
    itemlist.append(Item(channel=item.channel, action="ultimos_episodios", title="Subtitulados", url="sub"))
    itemlist.append(Item(channel=item.channel, action="ultimos_episodios", title="Español", url="es"))
    itemlist.append(Item(channel=item.channel, action="ultimos_episodios", title="Latino", url="la"))
    itemlist.append(Item(channel=item.channel, action="ultimos_episodios", title="Original", url="en"))
    return itemlist


def newest(categoria):
    logger.info()

    item = Item()
    try:
        if categoria == 'series':
            item.url = "es"
            itemlist = ultimos_episodios(item)
        else:
            return []

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def ultimos_episodios(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(CHANNEL_HOST, add_referer=True).data
    # logger.info("data="+data)

    # Extrae los episodios
    '''
    <a href="http://www.seriesflv.net/ver/ciega-a-citas-1x72.html" class="item-one" lang="es"
        title="Ciega a citas 1x72 Online Sub Español Gratis">
        <div class="box-tc">1x72</div>
        <div class="box-info">
            <div class="i-title">Ciega a citas</div>
            <div class="i-time">Hace 10 minutos</div>
        </div>
    </a>
    '''
    idioma = item.url
    patron = '<a href="([^"]+)" class="item-one" lang="'+idioma+'"[^<]+'
    patron += '<div class="box-tc">([^<]+)</div[^<]+'
    patron += '<div class="box-info"[^<]+'
    patron += '<div class="i-title">([^<]+)</div[^<]+'
    patron += '<div class="i-time">([^<]+)</div>'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, episodio, serie, hace in matches:
        title = serie + " " + episodio + " (" + hace + ")"
        thumbnail = ""
        plot = ""
        url = scrapedurl
        temporada, episodio = episodio.split('x')
        itemlist.append(Item(channel=item.channel, action="findvideos", title=title, url=url, thumbnail=thumbnail,
                             plot=plot, fulltitle=title, contentTitle=serie, language=get_nombre_idioma(idioma),
                             contentSeason=int(temporada), contentEpisodeNumber=int(episodio)))

        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist


def search(item, texto):
    logger.info()

    # Evitamos hacer búsquedas en vacío
    if texto == "":
        return []

    texto = texto.replace(" ", "%20")

    if item.url == "":
        item.url = "http://www.seriesflv.net/api/search/?q="

    item.url = item.url+texto

    try:
        return buscar(item)

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def buscar(item):
    logger.info()

    # Descarga la pagina
    post = item.extra
    data = httptools.downloadpage(item.url, post=post, add_referer=True).data
    # logger.info("data="+data)

    # Extrae las entradas (carpetas)
    '''
    <ul>
        <div class="bg7 header color7">Resultados de <b>equipo a</b></div>
        <li>
            <a class="on over" href="http://www.seriesflv.net/serie/el-equipo-a.html">
                <div class="left">
                    <img src="http://http-s.ws/ysk/img/data/b5de7e0470eae36f8196d8fcbf897c17-size-90x120-a.jpg" />
                </div>
                <div class="op">
                    <span class="color1 bold tit">El equipo A</span>
                    <span class="color8 font2">6 temporadas</span>
                    <span>
                        <div class="star_rating over">
                            <ul style="float:none; left:auto;" class="star">
                                <li style="width: 100%;" class="curr"></li>
                            </ul>
                        </div>
                    </span>
                </div>
            </a>
        </li>
    </ul>
    '''
    patron = '<li><a class="on over" href="([^"]+)"[^<]+'
    patron += '<div class="left"[^<]+'
    patron += '<img src="([^"]+)"[^<]+'
    patron += '</div><div class="op"[^<]+'
    patron += '<span class="[^"]+">([^<]+)</span[^<]+'
    patron += '<span class="[^"]+">([^<]+)</span>'

    matches = re.compile(patron, re.DOTALL).findall(data)
    itemlist = []

    for scrapedurl, scrapedthumbnail, scrapedtitle, numtemporadas in matches:

        title = scrapertools.htmlclean(scrapedtitle).strip()+" ("+numtemporadas+")"
        thumbnail = urlparse.urljoin(item.url, scrapedthumbnail)
        plot = ""

        url = urlparse.urljoin(item.url, scrapedurl)
        itemlist.append(Item(channel=item.channel, action="episodios", title=title, url=url, thumbnail=thumbnail,
                             plot=plot, show=title))

        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist


def series(item):
    logger.info()

    # Descarga la pagina
    post = item.extra
    data = httptools.downloadpage(item.url, post=post, add_referer=True).data
    # logger.info("data="+data)

    # Extrae las entradas (carpetas)
    '''
    <ul>
        <li>
            <a href="http://www.seriesflv.net/serie/game-of-thrones.html" class="on over">
                <div class="left">
                    <img src="http://http-s.ws/ysk/img/data/11a1a46bca5c4cca2cac0d0711225feb-size-90x120-a.jpg"
                        width="50" height="60" />
                    Game of Thrones (Juego de tronos)
                </div>
                <div class="rigth over">
                    <div class="left op">
                        <span>4</span>
                        <p>Temporadas</p>
                    </div>
    '''
    patron = '<a.*?href="([^"]+)"[^<]+'
    patron += '<div class="left"[^<]+'
    patron += '<img.*?src="([^"]+)"[^>]*>([^<]+)</div[^<]+'
    patron += '<div class="rigth over"[^<]+'
    patron += '<div class="left op"[^<]+'
    patron += '<span>([^<]+)</span'
    matches = re.compile(patron, re.DOTALL).findall(data)
    itemlist = []

    for scrapedurl, scrapedthumbnail, scrapedtitle, numtemporadas in matches:

        title = scrapertools.htmlclean(scrapedtitle).strip()+" ("+numtemporadas+" temporadas)"
        thumbnail = urlparse.urljoin(item.url, scrapedthumbnail)
        plot = ""

        url = urlparse.urljoin(item.url, scrapedurl)
        itemlist.append(Item(channel=item.channel, action="episodios", title=title, url=url, thumbnail=thumbnail,
                             plot=plot, show=title))

        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    # grupo_no=0&type=series&order=titulo
    old_offset = scrapertools.find_single_match(item.extra, "grupo_no\=(\d+)")
    new_offset = str(int(old_offset)+1)
    newextra = item.extra.replace("grupo_no="+old_offset, "grupo_no="+new_offset)
    itemlist.append(Item(channel=item.channel, action="series", title=">> Página siguiente", extra=newextra,
                         url=item.url))

    return itemlist


def get_nombre_idioma(idioma):

    if idioma == "es":
        return "Español"
    elif idioma == "en":
        return "Inglés"
    elif idioma == "la":
        return "Latino"
    elif idioma == "sub":
        return "VOS"
    else:
        return idioma


def episodios(item):
    logger.info()
    itemlist = []

    # Descarga la pagina
    data = httptools.downloadpage(item.url, add_referer=True).data
    # logger.info("data="+data)

    # Extrae los episodios
    '''
    <tr>
        <td class="sape">
            <i class="glyphicon glyphicon-film"></i>
            <a href="http://www.seriesflv.net/ver/game-of-thrones-1x9.html" class="color4">
                Game of Thrones (Juego de tronos) 1x09
            </a>
        </td>
        <td>
            <a href="javascript:void(0);" class="loginSF" title="Marcar Visto"><span class="no visto"></span></a>
        </td>
        <td>
            <div class="star_rating">
                <ul class="star">
                    <li class="curr" style="width: 99.6%;"></li>
                </ul>
            </div>
        </td>
        <td>
            <img src="http://www.seriesflv.net/images/lang/es.png" width="20" />
            <img src="http://www.seriesflv.net/images/lang/la.png" width="20" />
            <img src="http://www.seriesflv.net/images/lang/sub.png" width="20" />
        </td>
        <td>40,583</td>
    </tr>
    '''
    patron = '<tr[^<]+<td class="sape"><i class="glyphicon glyphicon-film"></i[^<]+'
    patron += '<a href="([^"]+)"[^>]+>([^<]+)</a>.*?<img(.*?)</td'
    matches = re.compile(patron, re.DOTALL).findall(data)

    # Sólo nos interesa el título de la serie
    show = re.sub(" \([^\)]+\)$", "", item.show)

    for scrapedurl, scrapedtitle, bloqueidiomas in matches:
        title = scrapedtitle+" ("

        patronidiomas = "lang/([a-z]+).png"
        matchesidiomas = re.compile(patronidiomas, re.DOTALL).findall(bloqueidiomas)
        for idioma in matchesidiomas:
            title = title+get_nombre_idioma(idioma)+", "

        title = title[:-2]+")"

        thumbnail = ""
        plot = ""
        url = scrapedurl

        # Se a añadido el parámetro show
        itemlist.append(Item(channel=item.channel, action="findvideos", title=title, url=url, thumbnail=thumbnail,
                             plot=plot, fulltitle=title, show=show))

        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    # Opción "Añadir esta serie a la biblioteca de XBMC"
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title="Añadir esta serie a la biblioteca de XBMC", url=item.url,
                             action="add_serie_to_library", extra="episodios", show=show))

    return itemlist


def findvideos(item):
    logger.info()

    # Descarga la pagina
    data = httptools.downloadpage(item.url, add_referer=True).data
    data = scrapertools.find_single_match(data, '<div id="enlaces">(.*?)<div id="comentarios">')
    # logger.info("data="+data)

    # Extrae las entradas (carpetas)
    '''
    <tr>
        <td width="45"><img width="20" src="http://www.seriesflv.net/images/lang/es.png"></td>
        <td width="86" style="display:none">2014-12-08</td>
        <td width="134" style="text-align:left;" class="e_server"><img width="16"
            src="http://www.google.com/s2/favicons?domain=tumi.tv"> tumi</td>
        <td width="84">
            <a href="http://www.seriesflv.net/goto/?id=fzELUWsRV22s3kibihvx1sYd2jpTufOJLadefY2hRtQ%3D" rel="nofollow"
                target="_blank" title="Reproducir..." class="btn btn-primary btn-xs bg2 enlace_link">
                <i class="glyphicon glyphicon-play"></i>
                Reproducir
            </a>
        </td>
        <td width="96" class="usuario">
            <a href="http://www.seriesflv.net/usuario/anon4/" rel="nofollow" class="color1">anon4</a>
        </td>
        <td width="200" class="linkComent">Hace 4 días | </td>
        <td width="92">
        <div class="report off">
            <a href="#" class="btn btn-danger btn-xs loginSF"><i class="glyphicon glyphicon-warning-sign"></i></a>
        </div>
        <div class="views on">690</div>
        </td>
    </tr>

    <tr>
        <td width="45"><img width="20" src="http://www.seriesflv.net/images/lang/en.png"></td>
        <td width="86" style="display:none">2014-12-08</td>
        <td width="134" style="text-align:left;" class="e_server"><img width="16"
            src="http://www.google.com/s2/favicons?domain=nowdownload.ch"> nowdownload</td>
        <td width="84">
            <a href="http://www.seriesflv.net/goto/?id=xzmfISe8dDbTc6DtVjuzw9jio0X8KXGxpjH%2FpcIxaxU%3D" rel="nofollow"
                target="_blank" title="Descargar...!" class="btn btn-primary btn-xs bg2 enlace_link">
                <i class="glyphicon glyphicon-cloud-download"></i>
                Descargar
            </a>
        </td>
        <td width="96" class="usuario">
            <a href="http://www.seriesflv.net/usuario/anon33422/" rel="nofollow" class="color1">anon33422</a>
        </td>
        <td width="200" class="linkComent">Hace 4 días | 1 y 2</td>
        <td width="92">
            <div class="report off">
                <a href="#" class="btn btn-danger btn-xs loginSF"><i class="glyphicon glyphicon-warning-sign"></i></a>
            </div>
            <div class="views on">1 link</div>
        </td>
    </tr>
    '''

    patron = '<tr[^<]+'
    patron += '<td[^<]+<img width="\d+" src="([^"]+)"></td[^<]+'
    patron += '<td[^<]+</td[^<]+'
    patron += '<td[^<]+<img[^>]+>([^<]+)</td[^<]+'
    patron += '<td[^<]+<a href="([^"]+)"[^<]+<i[^<]+</i[^<]+</a></td[^<]+'
    patron += '<td[^<]+<a[^<]+</a></td[^<]+'
    patron += '<td[^>]+>([^<]+)</td>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    itemlist = []

    for url_idioma, nombre_servidor, target_url, comentario in matches:
        codigo_idioma = scrapertools.find_single_match(url_idioma, 'lang/([a-z]+).png')
        idioma = get_nombre_idioma(codigo_idioma)

        title = "Ver en "+nombre_servidor.strip()+" ("+idioma+") ("+comentario.strip()+")"
        url = target_url
        thumbnail = ""
        plot = ""

        itemlist.append(Item(channel=item.channel, action="play", title=title, url=url, thumbnail=thumbnail, plot=plot,
                             folder=False))

        logger.debug("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")

    return itemlist


def play(item):
    logger.info("pelisalacarta.channels.seriesflv play url="+item.url)

    data = httptools.downloadpage(item.url, add_referer=True).data

    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = item.channel

    return itemlist    
