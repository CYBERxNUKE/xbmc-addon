# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (doomtv) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core import httptools
from core.item import Item
from core import servertools
from core import tmdb

host = 'http://doomtv.net/'
headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
          ['Referer', host]]

tgenero = {"Comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "Suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "Drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "Acción":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "Aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
               "Romance":"https://s31.postimg.org/y7vai8dln/romance.png",
               "Animación":"https://s32.postimg.org/rbo1kypj9/animacion.png",
               "Ciencia Ficción":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "Terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "Documentales":"https://s32.postimg.org/7opmvc5ut/documental.png",
               "Musical":"https://s31.postimg.org/7i32lca7f/musical.png",
               "Fantasía":"https://s32.postimg.org/pklrf01id/fantasia.png",
               "Bélico Guerra":"https://s32.postimg.org/kjbko3xhx/belica.png",
               "Misterio":"https://s4.postimg.org/kd48bcxe5/misterio.png",
               "Crimen":"https://s14.postimg.org/5lez1j1gx/crimen.png",
               "Biográfia":"https://s23.postimg.org/u49p87o3f/biografia.png",
               "Familia":"https://s28.postimg.org/4wwzkt2f1/familiar.png",
               "Familiar":"https://s28.postimg.org/4wwzkt2f1/familiar.png",
               "Intriga":"https://s32.postimg.org/xc2ovcqfp/intriga.png",
               "Thriller":"https://s31.postimg.org/4d7bl25y3/thriller.png",
               "Guerra":"https://s29.postimg.org/vqgjmozzr/guerra.png",
               "Estrenos":"https://s12.postimg.org/4zj0rbun1/estrenos.png",
               "Peleas":"https://s14.postimg.org/53qrbqy5d/peleas.png",
               "Policiales":"https://s15.postimg.org/ctz76qrwb/policial.png",
               "Uncategorized":"https://s16.postimg.org/fssbi4nlh/otros.png",
               "LGBT":"https://s16.postimg.org/fssbi4nlh/otros.png"}

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Todas", action="lista",thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', url = host))

    itemlist.append( item.clone (title="Generos", action="seccion", thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png',url = host, extra ='generos'))

    itemlist.append( item.clone (title="Mas vistas", action="seccion", thumbnail='https://s32.postimg.org/466gt3ipx/vistas.png', fanart='https://s32.postimg.org/466gt3ipx/vistas.png',url = host, extra ='masvistas'))

    itemlist.append( item.clone (title="Recomendadas", action="lista",thumbnail='https://s31.postimg.org/4bsjyc4iz/recomendadas.png', fanart='https://s31.postimg.org/4bsjyc4iz/recomendadas.png', url = host, extra = 'recomendadas'))

    itemlist.append( item.clone (title="Por año", action="seccion", thumbnail='https://s31.postimg.org/iyl5fvzqz/pora_o.png', fanart='https://s31.postimg.org/iyl5fvzqz/pora_o.png',url = host, extra ='poraño'))

    itemlist.append( item.clone (title="Buscar", action="search", url='http://doomtv.net/?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))

    return itemlist


def lista(item):
    logger.info()

    itemlist = []
    max_items = 20
    next_page_url = ''

    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)

    if item.extra == 'recomendadas':
        patron = '<a href=(.*?)><div class=imgss><img src=(.*?) alt=(.*?)(?:–.*?|\(.*?|) width=120.*?icon-grade.*?' \
                 'ttps>.*?ytps>(.*?)<\/span>'
    else:
        patron = '<div class=movie>.*?img src=(.*?) alt=(.*?)(?:–.*?|\(.*?|) width=.*?<a href=(.*?)>.*?<\/h2>.*?' \
                 '(?:year.)(.*?)<\/span>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    if item.next_page != 'b':
      if len(matches) > max_items:
        next_page_url = item.url
        matches = matches [:max_items]
        next_page = 'b'
    else:
      matches = matches[max_items:]
      next_page = 'a'
      patron_next_page = '<div class=siguiente><a href=(.*?)\?'
      matches_next_page = re.compile(patron_next_page, re.DOTALL).findall(data)
      if len(matches_next_page) > 0:
        next_page_url = urlparse.urljoin(item.url, matches_next_page[0])

    for scrapedthumbnail, scrapedtitle, scrapedurl, scrapedyear in matches:
        if item.extra == 'recomendadas':
            url = scrapedthumbnail
            title = scrapedurl
            thumbnail = scrapedtitle
        else:
            url = scrapedurl
            thumbnail = scrapedthumbnail
            title = scrapedtitle
        year = scrapedyear
        fanart =''
        plot= ''
                       
        if 'serie' not in url:
            itemlist.append( Item(channel=item.channel, action='findvideos' , title=title , url=url,
                                  thumbnail=thumbnail, plot=plot, fanart=fanart, contentTitle = title,
                                  infoLabels={'year':year}))
    
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    #Paginacion
    if next_page_url !='':
      itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page_url,
                           thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',extra=item.extra,
                           next_page = next_page))
    return itemlist


def seccion(item):
    logger.info()
    
    itemlist = []
    duplicado = []
    data = httptools.downloadpage(item.url).data

    if item.extra == 'generos':
      data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    accion ='lista'
    if item.extra == 'masvistas':
        patron = '<b>\d*<\/b>\s*<a href="(.*?)">(.*?<\/a>\s*<span>.*?<\/span>\s*<i>.*?<\/i><\/li>)'
        accion = 'findvideos'
    elif item.extra == 'poraño':
        patron = '<li><a class="ito" HREF="(.*?)">(.*?)<\/a><\/li>'
    else:
        patron ='<li class="cat-item cat-item-.*?"><a href="(.*?)">(.*?)<\/i><\/li>'

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = scrapedurl
        title = scrapedtitle
        thumbnail = ''
        fanart =''
        plot= ''
        year=''
        contentTitle=''
        if item.extra == 'masvistas':
          year = re.findall(r'\b\d{4}\b',scrapedtitle)
          title = re.sub(r'<\/a>\s*<span>.*?<\/span>\s*<i>.*?<\/i><\/li>','',scrapedtitle)
          contentTitle = title
          title = title+' ('+year[0]+')'

        elif item.extra == 'generos':
          title = re.sub(r'<\/a> <i>\d+','',scrapedtitle)
          cantidad = re.findall(r'.*?<\/a> <i>(\d+)',scrapedtitle)
          logger.debug('scrapedtitle: '+scrapedtitle)
          logger.debug('cantidad: '+str(cantidad))
          th_title = title
          title = title+' ('+cantidad[0]+')'
          thumbnail = tgenero[th_title]
          fanart = thumbnail

        if url not in duplicado:
          itemlist.append( Item(channel=item.channel, action=accion , title=title , url=url, thumbnail=thumbnail,
                                plot=plot, fanart=fanart, contentTitle=contentTitle, infoLabels={'year':year}))
          duplicado.append(url)
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    return itemlist

def unpack(packed):
    p,c,k = re.search("}\('(.*)', *\d+, *(\d+), *'(.*)'\.", packed, re.DOTALL).groups()
    for c in reversed(range(int(c))):
        if k.split('|')[c]: p = re.sub(r'(\b%s\b)' % c, k.split('|')[c], p)
        p = p.replace('\\','')
        p = p.decode('string_escape')
    return p

def get_url(item):
    logger.info()
    itemlist=[]
    duplicado =[]
    patrones =["{'label':(.*?),.*?'file':'(.*?)'}","{file:'(.*?redirector.*?),label:'(.*?)'}"]
    data = httptools.downloadpage(item.url, headers=headers, cookies=False).data
    
    url = scrapertools.find_single_match(data,'class="player-content"><iframe src="(.*?)"')
    url= 'http:/'+url.replace('//','/')
    data = httptools.downloadpage(url, headers= headers, cookies=False).data
    packed = scrapertools.find_single_match(data, "<script type='text\/javascript'>(eval.*?)\s*jwplayer\(\)")

    if packed:
      unpacked=unpack(packed)
      num_patron = 0
      patron = "{'label':(.*?),.*?'file':'(.*?)'}"
      matches = re.compile(patron,re.DOTALL).findall(unpacked)
      if not matches:
       patron = "{file:'(.*?redirector.*?),label:'(.*?)'}"
       matches = re.compile(patron,re.DOTALL).findall(unpacked)
    
      for dato_a, dato_b in matches:
        if 'http' in dato_a:
          url = dato_a
          calidad = dato_b
        else:
          url = dato_b
          calidad = dato_a
        title = item.contentTitle+' ('+calidad+')'
        if url not in duplicado:
          itemlist.append( Item(channel=item.channel, action='play' , title=title , url=url, thumbnail=item.thumbnail,
                                plot=item.plot, fanart=item.fanart, contentTitle = item.contentTitle,
                                calidad = calidad))
          duplicado.append(url)

      return itemlist


def getinfo(page_url):
    info =()
    logger.info()
    data = httptools.downloadpage(page_url).data
    thumbnail = scrapertools.find_single_match(data,'<div class="cover" style="background-image: url\((.*?)\);')
    plot = scrapertools.find_single_match(data,'<h2>Synopsis<\/h2>\s*<p>(.*?)<\/p>')
    info = (plot,thumbnail)

    return info


def findvideos (item):
    logger.info()
    itemlist =[]
    itemlist = get_url(item)
    if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos' :
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]',
                             url=item.url, action="add_pelicula_to_library", extra="findvideos",
                             contentTitle = item.contentTitle))
    return itemlist

def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    if texto!='':
       return lista(item)

def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    #categoria='peliculas'
    try:
        if categoria == 'peliculas':
            item.url = host
        elif categoria == 'infantiles':
            item.url = host+'category/animacion/'
        itemlist = lista(item)
        if itemlist[-1].title == 'Siguiente >>>':
                itemlist.pop()
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist

