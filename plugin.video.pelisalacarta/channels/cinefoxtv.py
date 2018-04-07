# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (cinefoxtv) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re, time
import os, sys, threading

from core import logger
from core import config
from core import scrapertools
from core import httptools
from core.item import Item
from core import servertools
from core import tmdb



host = 'http://cinefoxtv.net/'
headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
          ['Referer', host]]

global duplicado
global itemlist
global temp_list
canal = 'cinefoxtv'

tgenero = {"Comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "Suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "Drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "Acción":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "Aventuras":"https://s32.postimg.org/whwh56is5/aventura.png",
               "Animacion":"https://s32.postimg.org/rbo1kypj9/animacion.png",
               "Ciencia Ficcion":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "Terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "Documentales":"https://s32.postimg.org/7opmvc5ut/documental.png",
               "Musical":"https://s31.postimg.org/7i32lca7f/musical.png",
               "Western":"https://s31.postimg.org/nsksyt3hn/western.png",
               "Belico":"https://s32.postimg.org/kjbko3xhx/belica.png",
               "Crimen":"https://s14.postimg.org/5lez1j1gx/crimen.png",
               "Biográfica":"https://s23.postimg.org/u49p87o3f/biografia.png",
               "Deporte":"https://s31.postimg.org/pdc8etc0r/deporte.png",
               "Fantástico":"https://s32.postimg.org/b6xwbui6d/fantastico.png",
               "Estrenos":"https://s12.postimg.org/4zj0rbun1/estrenos.png",
               "Película 18+":"https://s31.postimg.org/6kcxutv3v/erotica.png",
               "Thriller":"https://s31.postimg.org/4d7bl25y3/thriller.png",
               "Familiar":"https://s28.postimg.org/4wwzkt2f1/familiar.png",
               "Romanticas":"https://s30.postimg.org/4i5sbj7n5/romantica.png",
               "Intriga":"https://s32.postimg.org/xc2ovcqfp/intriga.png",
               "Infantil":"https://s32.postimg.org/i53zwwgsl/infantil.png"}

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Todas", action="lista",thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', extra='peliculas/', url = host+'page/1.html'))
    
    itemlist.append( itemlist[-1].clone (title="Generos", action="generos", thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png',url = host))

    itemlist.append( itemlist[-1].clone (title="Mas Vistas", action="lista", thumbnail='https://s32.postimg.org/466gt3ipx/vistas.png', fanart='https://s32.postimg.org/466gt3ipx/vistas.png',url = host+'top-peliculas-online/1.html'))

    itemlist.append( itemlist[-1].clone (title="Buscar", action="search", thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png',url = host+'tag/'))

    return itemlist


def lista (item):
    logger.info ()
    itemlist =[]
    duplicado = []
    max_items = 24
    next_page_url = ''

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    if item.title == 'Todas':
      data = scrapertools.find_single_match(data,'<h3>Ver Últimas Peliculas Completa Online Gratis Agregadas.*?clearall')
    data = scrapertools.decodeHtmlentities(data)
    patron = '"box_image_b"><a href="([^"]+)" title=".*?><img src="([^"]+)" alt="(.*?)(\d{4}).*?"'
    matches = re.compile(patron,re.DOTALL).findall(data)

    if item.next_page != 'b':
      if len(matches) > max_items:
        next_page_url = item.url
        matches = matches [:max_items]
        next_page = 'b'
    else:
      matches = matches[max_items:]
      next_page = 'a'
      patron_next_page = '<a class="page dark gradient" href="([^"]+)">PROXIMO'
      matches_next_page = re.compile(patron_next_page, re.DOTALL).findall(data)
      if len(matches_next_page) > 0:
        next_page_url = urlparse.urljoin(item.url, matches_next_page[0])
      
    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedyear in matches:
        
      url = scrapedurl
      thumbnail = scrapedthumbnail
      contentTitle = re.sub(r"\(.*?\)|\/.*?|\(|\)|.*?\/|&excl;","",scrapedtitle)
      title = scrapertools.decodeHtmlentities(contentTitle)+'('+scrapedyear+')'
      fanart =''
      plot= ''

      if url not in duplicado:
        itemlist.append( Item(channel=item.channel, action='findvideos' , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentTitle = contentTitle, infoLabels ={'year':scrapedyear}))
        duplicado.append(url)

    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    if next_page_url !='':
      itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page_url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',extra=item.extra, next_page = next_page))
    return itemlist

def generos (item):
    logger.info ()
    
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron = '<li><a href="([^"]+)"><i class="fa fa-caret-right"><\/i> <strong>Películas de (.*?)<\/strong><\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = scrapedurl
        if scrapedtitle in tgenero:
            thumbnail = tgenero[scrapedtitle]
        else:
            thumbnail = ''
        title = scrapedtitle
        fanart =''
        plot= ''
                
        if title != 'Series':
            itemlist.append( Item(channel=item.channel, action='lista' , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart))
    return itemlist

def getinfo(page_url):
    
    logger.info ()
    data = httptools.downloadpage(page_url).data
    plot = scrapertools.find_single_match(data,'<\/em>\.(?:\s*|.)(.*?)\s*<\/p>')
    info = plot

    return info

def findvideos(item):
    logger.info ()
    itemlist =[]
    info = getinfo(item.url)
    data = httptools.downloadpage(item.url, headers = headers).data
    patron = 'src="(.*?)" style="border:none;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl in matches:
        itemlist.extend(servertools.find_video_items(data=scrapedurl))


    for videoitem in itemlist:
       videoitem.title = item.contentTitle+' ('+videoitem.server+')'
       videoitem.channel=item.channel
       videoitem.plot = info
       videoitem.action="play"
       videoitem.folder=False

    if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos' :
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))

    return itemlist

def search(item,texto):
    logger.info()
    texto = texto.replace(" ","-")
    item.url = item.url+texto+'/'
    if texto!='':
       return lista(item)

def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    #categoria='peliculas'
    try:
        if categoria == 'peliculas':
            item.url = host+'page/1.html'
        elif categoria == 'infantiles':
            item.url = host+'peliculas-de-genero/infantil/1.html'
        itemlist = lista(item)
        if itemlist[-1].title == 'Siguiente >>>':
                itemlist.pop()
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist
       
