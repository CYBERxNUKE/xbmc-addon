# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (seodiv) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse, urllib2, urllib, re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools

IDIOMAS = {'latino':'Latino'}
list_languages = IDIOMAS.values()

host = 'http://www.seodiv.com'


def mainlist(item):
    logger.info()

    itemlist = []

    itemlist.append(Item(channel=item.channel, title="Todos", action="todas", url=host,
                         thumbnail='https://s32.postimg.org/544rx8n51/series.png',
                         fanart='https://s32.postimg.org/544rx8n51/series.png'))

    return itemlist


def todas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    patron = '<div class=shortf><div><div class=shortf-img><a href=(.*?)><img src=(.*?) alt=.*?quality>(' \
             '.*?)<.*?series transition>(.*?) <\/span>'

    matches = re.compile(patron, re.DOTALL).findall(data)
    for scrapedurl, scrapedthumbnail, scrapedcalidad, scrapedtitle in matches:
        url = host + scrapedurl
        calidad = scrapedcalidad
        title = scrapedtitle.decode('utf-8')
        thumbnail = scrapedthumbnail
        fanart = 'https://s32.postimg.org/gh8lhbkb9/seodiv.png'

        itemlist.append(Item(channel=item.channel, action="temporadas", title=title, url=url, thumbnail=thumbnail,
                             fanart=fanart, contentSerieName=title, extra='', language=item.language,
                             quality='default'))

    return itemlist


def temporadas(item):
    logger.info()
    itemlist = []
    templist = []
    data = httptools.downloadpage(item.url).data
    url_base = item.url
    patron = '<a class="collapsed" data-toggle="collapse" data-parent="#accordion" href=.*? aria-expanded="false" ' \
             'aria-controls=.*?>([^<]+)<\/a>'
    matches = re.compile(patron, re.DOTALL).findall(data)
    temp = 1
    if 'Temporada' in str(matches):
        for scrapedtitle in matches:
            url = url_base
            tempo = re.findall(r'\d+', scrapedtitle)
            if tempo:
                title = 'Temporada' + ' ' + tempo[0]
            else:
                title = scrapedtitle.lower()
            thumbnail = item.thumbnail
            plot = item.plot
            fanart = scrapertools.find_single_match(data, '<img src="([^"]+)"/>.*?</a>')
            itemlist.append(
                Item(channel=item.channel, action="episodiosxtemp", title=title, fulltitle=item.title, url=url,
                     thumbnail=thumbnail, plot=plot, fanart=fanart, temp=str(temp),
                     contentSerieName=item.contentSerieName))
            temp = temp + 1

        if config.get_library_support() and len(itemlist) > 0:
            itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]',
                                 url=item.url, action="add_serie_to_library", extra="episodios",
                                 contentSerieName=item.contentSerieName, extra1=item.extra1, temp=str(temp)))
        return itemlist
    else:
        itemlist = episodiosxtemp(item)
        if config.get_library_support() and len(itemlist) > 0:
            itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]',
                                 url=item.url, action="add_serie_to_library", extra="episodios",
                                 contentSerieName=item.contentSerieName, extra1=item.extra1, temp=str(temp)))
        return itemlist


def episodios(item):
    logger.debug('pelisalacarta.channels.seodiv episodios')
    itemlist = []
    templist = temporadas(item)
    for tempitem in templist:
        logger.debug(tempitem)
        itemlist += episodiosxtemp(tempitem)

    return itemlist


def episodiosxtemp(item):
    logger.debug("pelisalacarta.channels.seodiv episodiosxtemp")
    itemlist = []
    data = httptools.downloadpage(item.url).data
    tempo = item.title
    if 'Temporada' in item.title:
        item.title = item.title.replace('Temporada', 'temporada')
        item.title = item.title.strip()
        item.title = item.title.replace(' ', '-')

    patron = '<li><a href="([^"]+)">.*?(Capitulo|Pelicula).*?([\d]+)'

    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtipo, scrapedtitle in matches:
        url = host + scrapedurl
        title = ''
        thumbnail = item.thumbnail
        plot = ''
        fanart = ''

        if 'temporada' in item.title and item.title in scrapedurl and scrapedtipo == 'Capitulo' and item.temp != '':
            title = item.contentSerieName + ' ' + item.temp + 'x' + scrapedtitle
            itemlist.append(
                Item(channel=item.channel, action="findvideos", title=title, fulltitle=item.fulltitle, url=url,
                     thumbnail=item.thumbnail, plot=plot))

        if 'temporada' not in item.title and item.title not in scrapedurl and scrapedtipo == 'Capitulo' and item.temp\
                == '':
            if item.temp == '': temp = '1'
            title = item.contentSerieName + ' ' + temp + 'x' + scrapedtitle
            if '#' not in scrapedurl:
                itemlist.append(
                    Item(channel=item.channel, action="findvideos", title=title, fulltitle=item.fulltitle, url=url,
                         thumbnail=item.thumbnail, plot=plot))

        if 'temporada' not in item.title and item.title not in scrapedurl and scrapedtipo == 'Pelicula':
            title = scrapedtipo + ' ' + scrapedtitle
            itemlist.append(
                Item(channel=item.channel, action="findvideos", title=title, fulltitle=item.fulltitle, url=url,
                     thumbnail=item.thumbnail, plot=plot))

    return itemlist


def findvideos(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    logger.debug(data)
    video_items = servertools.find_video_items(item)

    for videoitem in video_items:
        videoitem.thumbnail = servertools.guess_server_thumbnail(videoitem.server)
        videoitem.language = scrapertools.find_single_match(data, '<span class="f-info-title">Idioma:<\/span>\s*<span '
                                                                  'class="f-info-text">(.*?)<\/span>')
        videoitem.title = item.contentSerieName + ' (' + videoitem.server + ') (' + videoitem.language + ')'
        videoitem.quality = 'default'
        itemlist.append(videoitem)

    return itemlist
