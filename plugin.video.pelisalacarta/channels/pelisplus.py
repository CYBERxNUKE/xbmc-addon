# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (pelisplus) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import tmdb
from core import config
from core import scrapertools
from core import httptools
from core.item import Item
from core import servertools


host ="http://www.pelisplus.tv/"

headers = [['User-Agent', 'Mozilla/50.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
          ['Referer', host]]

patrones = ['<img src="([^"]+)" alt=".*?" class="picture-movie">','<span>Sinopsis:<\/span>.([^<]+)<span class="text-detail-hide"><\/span>.<\/p>']



def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Peliculas", action="menupeliculas",thumbnail='https://s31.postimg.org/4g4lytrqj/peliculas.png', fanart='https://s31.postimg.org/4g4lytrqj/peliculas.png', extra='peliculas/'))
    
    itemlist.append( Item(channel=item.channel, title="Series", action="menuseries",thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png', extra='peliculas/'))
    
    itemlist.append( Item(channel=item.channel, title="Documentales", action="lista", url=host+'documentales/pag-1', thumbnail='https://s21.postimg.org/i9clk3u6v/documental.png', fanart='https://s21.postimg.org/i9clk3u6v/documental.png', extra='documentales/'))

    return itemlist

def menupeliculas(item):

    logger.info()
    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Ultimas", action="lista", url=host+'estrenos/pag-1', thumbnail='https://s31.postimg.org/3ua9kwg23/ultimas.png', fanart='https://s31.postimg.org/3ua9kwg23/ultimas.png', extra='estrenos/'))
    
    itemlist.append( Item(channel=item.channel, title="Todas", action="lista", url=host+'peliculas/pag-1', thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', extra='peliculas/'))
    
    itemlist.append( Item(channel=item.channel, title="Generos", action="generos", url=host+'peliculas/pag-1', thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png', extra='documentales/'))
    
    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url=host+'busqueda/?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png', extra='peliculas/'))
    
    return itemlist

def menuseries(item):

    logger.info()
    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Todas", action="lista", url=host+"series/pag-1",thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', extra='series/'))
        
    itemlist.append( Item(channel=item.channel, title="Generos", action="generos", url=host+'series/pag-1', thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png', extra='series/'))

    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url=host+'busqueda/?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png', extra='series/'))
    
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


def lista(item):
    logger.info()
    
    itemlist = []

    if 'series/' in item.extra:
        accion = 'temporadas'
        tipo = 'tvshow'
    else:
        accion = 'findvideos'
        tipo = 'movie'

    data = httptools.downloadpage(item.url).data
    
    if item.title != 'Buscar':
        patron ='<img.*?width="147" heigh="197".*?src="([^"]+)".*?>.*?.<i class="icon online-play"><\/i>.*?.<h2 class="title title-.*?">.*?.<a href="([^"]+)" title="([^"]+)">.*?>'
        actual = scrapertools.find_single_match(data,'<a href="http:\/\/www.pelisplus.tv\/.*?\/pag-([^p]+)pag-2" class="page bicon last"><<\/a>')
    else:
        patron = '<img data-original="([^"]+)".*?width="147" heigh="197".*?src=.*?>.*?\n<i class="icon online-play"><\/i>.*?\n<h2 class="title title-.*?">.*?\n<a href="([^"]+)" title="([^"]+)">.*?>'
        actual = ''
    
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedthumbnail, scrapedurl, scrapedtitle in matches:
        url = scrapedurl
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        thumbnail = scrapedthumbnail
        
        filtro_thumb = scrapedthumbnail.replace("https://image.tmdb.org/t/p/w154", "")
        filtro_list = {"poster_path": filtro_thumb} #Nombre del campo a filtrar y valor en los resultados de la api de tmdb
        filtro_list = filtro_list.items()

        if item.title != 'Buscar':
          itemlist.append(Item(channel=item.channel,contentType=tipo, action=accion, title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,
                              fulltitle=scrapedtitle, infoLabels={'filtro': filtro_list},
                               contentTitle =scrapedtitle, contentSerieName= scrapedtitle, extra = item.extra))
        else:
          item.extra = item.extra.rstrip('s/')
          if item.extra in url:
            itemlist.append(Item(channel=item.channel,contentType=tipo, action=accion, title=scrapedtitle, url=scrapedurl, thumbnail=scrapedthumbnail,
            fulltitle=scrapedtitle, infoLabels={'filtro': filtro_list}, 
            contentTitle =scrapedtitle, contentSerieName= scrapedtitle, extra = item.extra))
        
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)

    # Encuentra los elementos que no tienen plot y carga las paginas correspondientes para obtenerlo#
    for item in itemlist:
      if item.infoLabels['plot']=='':
        data = httptools.downloadpage(item.url).data
        item.fanart = scrapertools.find_single_match(data,'meta property="og:image" content="([^"]+)" \/>')
        item.plot =scrapertools.find_single_match(data,'<span>Sinopsis:<\/span>.([^<]+)<span class="text-detail-hide"><\/span>.<\/p>')

#Paginacion
    if item.title != 'Buscar' and actual !='':
       if itemlist !=[]:
           next_page = str(int(actual)+1)
           next_page_url = host+item.extra+'pag-'+next_page
           import inspect
           itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page_url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',extra=item.extra))
    return itemlist
    
def temporadas(item):
    logger.info()
    itemlist = []
    templist =[]
    data = httptools.downloadpage(item.url).data
    
    patron = '<span class="ico accordion_down"><\/span>Temporada([^<]+)'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedtitle in matches:
        infoLabels=item.infoLabels
        url = item.url
        title = 'Temporada '+scrapedtitle.strip(' \r\n')
        thumbnail = scrapertools.find_single_match(data,'<img src="([^"]+)" alt="" class="picture-movie">')
        plot = scrapertools.find_single_match(data,'<span>Sinopsis:<\/span>.([^<]+).<span class="text-detail-hide"><\/span>')
        fanart = scrapertools.find_single_match(data,'<img src="([^"]+)"/>.*?</a>')
        contentSeasonNumber = scrapedtitle.strip(' \r\n')
        itemlist.append( Item(channel=item.channel, action="episodios" , title=title, fulltitle=item.title, url=url, thumbnail=thumbnail, plot=plot, fanart = fanart, extra=scrapedtitle.rstrip('\n'), contentSerieName =item.contentSerieName, contentSeasonNumber = contentSeasonNumber, infoLabels={'season':contentSeasonNumber}))
    
    if item.extra == 'temporadas':
        for tempitem in itemlist:
            templist += episodios(tempitem)
    else:
    	tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url,
                             action="add_serie_to_library", extra="temporadas", contentSerieName=item.contentSerieName, contentSeasonNumber=contentSeasonNumber))
    if item.extra == 'temporadas':
        return templist
    else:
        return itemlist
    
def episodios(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = '<span class="ico season_play"><\/span>([^<]+)<\/a>.<a href="([^"]+)" class="season-online enabled">'
    temporada = 'temporada/'+item.extra.strip(' ')
    matches = re.compile(patron,re.DOTALL).findall(data)
    infoLabels=item.infoLabels

    for scrapedtitle, scrapedurl in matches:      

        if temporada in scrapedurl:
           url = scrapedurl
           contentSeasonNumber = re.findall(r'temporada.*?(\d+)',url)
           capitulo = re.findall(r'Capitulo \d+', scrapedtitle)
           contentEpisodeNumber = re.findall(r'\d+', capitulo[0])
           contentEpisodeNumber = contentEpisodeNumber[0]
           infoLabels['episode']=contentEpisodeNumber
           title = contentSeasonNumber[0]+'x'+contentEpisodeNumber+' - '+scrapedtitle
           
           thumbnail = scrapertools.find_single_match(data,'<img src="([^"]+)" alt="" class="picture-movie">')
           plot = ''
           fanart = ''
           itemlist.append( Item(channel=item.channel, action="findvideos" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, plot=plot, fanart = fanart, extra=scrapedtitle, contentSeasonNumber = item.contentSeasonNumber, infoLabels = infoLabels))
    if item.extra != 'temporadas':
    	tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    	itemlist = fail_tmdb(itemlist)
    return itemlist       

def fail_tmdb(itemlist):
    logger.info()
    realplot=''
    for item in itemlist:
        if item.infoLabels['plot'] =='':
            data = httptools.downloadpage(item.url).data
            if item.fanart == '':
                item.fanart= scrapertools.find_single_match(data,patrones[0])
            realplot = scrapertools.find_single_match(data, patrones[1])
            item.plot = scrapertools.remove_htmltags(realplot)
    return itemlist

def generos(item):
    
    tgenero = {"Comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "Suspense":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "Drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "Accion":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "Aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
               "Romance":"https://s31.postimg.org/y7vai8dln/romance.png",
               "Animacion":"https://s32.postimg.org/rbo1kypj9/animacion.png",
               "Ciencia Ficcion":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "Terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "Documental":"https://s32.postimg.org/7opmvc5ut/documental.png",
               "Musica":"https://s31.postimg.org/7i32lca7f/musical.png",
               "Western":"https://s31.postimg.org/nsksyt3hn/western.png",
               "Fantasia":"https://s32.postimg.org/pklrf01id/fantasia.png",
               "Guerra":"https://s32.postimg.org/kjbko3xhx/belica.png",
               "Misterio":"https://s4.postimg.org/kd48bcxe5/misterio.png",
               "Crimen":"https://s14.postimg.org/5lez1j1gx/crimen.png",
               "Historia":"https://s13.postimg.org/52evvjrqf/historia.png",
               "Pelicula De La Television":"https://s14.postimg.org/jtzrcpmoh/delatv.png",
               "Foreign":"https://s14.postimg.org/6gun6dxkx/extranjera.png"}
               
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = '<i class="s-upper" id="([^"]+)"><\/i>.<span>([^<]+)<\/span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl, scrapedtitle in matches:
    
        url = scrapedurl+'pag-1'
        title = scrapedtitle
        if scrapedtitle in tgenero:
           thumbnail =tgenero[scrapedtitle]
           fanart= tgenero[scrapedtitle]
        else:
           thumbnail =''
           fanart= ''
        extra = scrapedurl.replace('http://www.pelisplus.tv/','')
        itemlist.append( Item(channel=item.channel, action="lista" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, fanart = fanart, extra=extra))
    return itemlist
    

def findvideos(item):
    logger.info ()
    itemlist=[]
    duplicados=[]
    datas=httptools.downloadpage(item.url).data
    patron ="<iframe.*?src='(.*?)' frameborder.*?"
    matches = re.compile(patron,re.DOTALL).findall(datas)
    
    for scrapedurl in matches:
       
       
       if 'elreyxhd' in scrapedurl or 'pelisplus.biz'in scrapedurl:
            data = httptools.downloadpage(scrapedurl, headers=headers).data
            
            quote = scrapertools.find_single_match(data,'sources.*?file.*?http')
            if quote and "'" in quote:
               patronr ="file:'([^']+)',label:'([^.*?]+)',type:.*?'.*?}"
            elif '"' in quote:
               patronr ='{file:"(.*?)",label:"(.*?)"}'
            matchesr = re.compile(patronr,re.DOTALL).findall(data)
            
            for scrapedurl, scrapedcalidad in matchesr:
               url = scrapedurl 
               
               title = item.contentTitle+' ('+str(scrapedcalidad)+')'
               thumbnail = item.thumbnail
               fanart=item.fanart
               if url not in duplicados:
               	itemlist.append( Item(channel=item.channel, action="play" , title=title , url=url, thumbnail=thumbnail,fanart =fanart, extra='directo'))
               	duplicados.append(url)

    url = scrapedurl
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=datas))
    
    for videoitem in itemlist:
        videoitem.infoLabels = item.infoLabels
        videoitem.channel = item.channel
        if videoitem.server != '':
           videoitem.thumbnail = servertools.guess_server_thumbnail (videoitem.server)
        else:
          videoitem.thumbnail = item.thumbnail
        videoitem.action = 'play'
        videoitem.fulltitle = item.title
        
        if videoitem.extra !='directo' and 'youtube' not in videoitem.url:
           videoitem.title = item.contentTitle+' ('+videoitem.server+')'
        
    n=0   
    for videoitem in itemlist:
       if 'youtube' in videoitem.url:
          videoitem.title='[COLOR orange]Trailer en'+' ('+videoitem.server+')[/COLOR]'
          itemlist[n], itemlist[-1] = itemlist[-1], itemlist[n]
       n=n+1

    if item.extra =='findvideos'and 'youtube' in itemlist[-1]:
      itemlist.pop(1)

    if 'serie' not in item.url:
       if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos':
          itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))
          
    return itemlist

def newest(categoria):
  logger.info()
  itemlist = []
  item = Item()
  item.extra = 'estrenos/'
  try:
      if categoria == 'peliculas':
          item.url = host+'estrenos/pag-1'
          
      elif categoria == 'infantiles':
          item.url = host+'peliculas/animacion/pag-1'

      elif categoria == 'documentales':
          item.url = host+'documentales/pag-1'
          item.extra = 'documentales/'
      
      itemlist = lista(item)
      if itemlist[-1].title == 'Siguiente >>>':
              itemlist.pop()
  except:
      import sys
      for line in sys.exc_info():
          logger.error("{0}".format(line))
      return []

  return itemlist




