# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (ultrapeliculashd) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools
from core import tmdb

host = 'http://www.ultrapeliculashd.com'

tgenero = {"Comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "Suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "Drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "Acción":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "Aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
               "Romance":"https://s31.postimg.org/y7vai8dln/romance.png",
               "Animación":"https://s32.postimg.org/rbo1kypj9/animacion.png",
               "Ciencia Ficción":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "Terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "Fantasía":"https://s32.postimg.org/pklrf01id/fantasia.png",
               "Crimen":"https://s14.postimg.org/5lez1j1gx/crimen.png",
               "Biográfia":"https://s23.postimg.org/u49p87o3f/biografia.png",
               "Estrenos":"https://s12.postimg.org/4zj0rbun1/estrenos.png",
               "Familiar":"https://s28.postimg.org/4wwzkt2f1/familiar.png",
               "Infantil":"https://s32.postimg.org/i53zwwgsl/infantil.png",
               "Religión":"https://s31.postimg.org/5tgjedlwb/religiosa.png",
               "Thriller":"https://s31.postimg.org/4d7bl25y3/thriller.png",
               "Series":"https://s32.postimg.org/544rx8n51/series.png",
               "Varios":"https://s16.postimg.org/fssbi4nlh/otros.png",
               "Sagas":"https://s12.postimg.org/tza2z0e3h/sagas.png"}

tcalidad = {'1080P':'https://s24.postimg.org/vto15vajp/hd1080.png','720P':'https://s28.postimg.org/wllbt2kgd/hd720.png',"HD":"https://s30.postimg.org/6vxtqu9sx/image.png"}

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Todas", action="lista",thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', url = host))

    itemlist.append( item.clone (title="Sagas", action="lista",thumbnail='https://s12.postimg.org/tza2z0e3h/sagas.png', fanart='https://s12.postimg.org/tza2z0e3h/sagas.png', url = host+'/category/sagas/'))

    itemlist.append( Item(channel=item.channel, title="Generos", action="generos", url=host, thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png'))
    
    itemlist.append( Item(channel=item.channel, title="Calidad", action="seccion", url=host, thumbnail='https://s23.postimg.org/ui42030wb/calidad.png', fanart='https://s23.postimg.org/ui42030wb/calidad.png', extra = 'calidad'))

    itemlist.append( item.clone (title="Por Año", action="seccion",thumbnail='https://s31.postimg.org/iyl5fvzqz/pora_o.png', fanart='https://s31.postimg.org/iyl5fvzqz/pora_o.png', url = host, extra = 'year'))

    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url=host+'/?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))
    

    return itemlist

def lista (item):
    logger.info ()
	
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    patron = '<div id=mt-.*? class=item><a href=(.*?)\/><div class=image><img src=(.*?) alt=(.*?)\[.*?\].*?<span class=player><\/span><span class=imdb><b>.*?'
    patron += '<span class=ttx>(.*?)<div class=degradado>.*?class=year>(.*?)<\/span>.*?class=calidad2>(.*?)<\/span>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot,scrapedyear, calidad  in matches:
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot= scrapedplot
        contentTitle = scrapedtitle
        contentTitle = contentTitle.replace('|','')
        contentTitle = contentTitle.strip(' ')
        title = contentTitle+' ('+calidad+')'
        year = scrapedyear
        fanart =''
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart, contentTitle=contentTitle, infoLabels={'year':year}))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb =True)       
    #Paginacion

    if itemlist !=[]:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data,'<div class=pag_b><a href=(.*?) >Siguiente<\/a>')
        import inspect
        if next_page !='':
           itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'))
    return itemlist

def generos(item):
    
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    
    patron = '<li class=cat-item cat-item-.*?><a href=(.*?) >(.*?)<\/a> <span>(.*?)<\/span>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, cantidad in matches:
        thumbnail =''
        fanart= ''
        if scrapedtitle in tgenero:
            thumbnail = tgenero[scrapedtitle]
        title = scrapedtitle+' ('+cantidad+')'
        url = scrapedurl

        itemlist.append( Item(channel=item.channel, action="lista" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart))
    return itemlist

def seccion(item):
    
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    if item.extra == 'year':
        patron = '<li><a href=(.*?\/fecha-estreno.*?)>(.*?)<\/a>'
    else:
        patron = '<li><a href=(http:\/\/www\.ultrapeliculashd\.com\/calidad.*?)>(.*?)<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        thumbnail =''
        if item.extra == 'calidad':
            thumbnail = tcalidad[scrapedtitle]
        fanart= ''
        title = scrapedtitle
        url = scrapedurl

        itemlist.append( Item(channel=item.channel, action="lista" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart))
    return itemlist

def findvideos(item):
    logger.info()
    itemlist=[]
    data = httptools.downloadpage(item.url).data
    
    patron = '<a href="(.*?)" rel="nofollow"'
    matches = matches = re.compile(patron,re.DOTALL).findall(data)
    for videoitem in matches:
        itemlist.extend(servertools.find_video_items(data=videoitem))

    for videoitem in itemlist:
        videoitem.channel = item.channel
        videoitem.action ='play'
        videoitem.thumbnail = servertools.guess_server_thumbnail(videoitem.server)
        videoitem.infoLabels = item.infoLabels
        videoitem.title = item.contentTitle+' ('+videoitem.server+')'
        if 'youtube' in videoitem.url:
            videoitem.title = '[COLOR orange]Trailer en Youtube[/COLOR]'

    if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos':
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))
    return itemlist

def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        if texto != '':
            return lista(item)
        else:
            return []
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []


def newest(categoria):
  logger.info()
  itemlist = []
  item = Item()
  item.extra = 'estrenos/'
  try:
      if categoria == 'peliculas':
          item.url = host+'/category/estrenos/'
          
      elif categoria == 'infantiles':
          item.url = host+'/category/infantil/'

      itemlist = lista(item)
      if itemlist[-1].title == 'Siguiente >>>':
              itemlist.pop()
  except:
      import sys
      for line in sys.exc_info():
          logger.error("{0}".format(line))
      return []

  return itemlist


