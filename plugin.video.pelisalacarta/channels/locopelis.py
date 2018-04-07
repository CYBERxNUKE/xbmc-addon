# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (locopelis) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys


from core import logger
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import tmdb
from core import httptools


host='http://www.locopelis.com/'

audio = {'Latino':'[COLOR limegreen]LATINO[/COLOR]','Español':'[COLOR yellow]ESPAÑOL[/COLOR]', 'Sub Español':'[COLOR red]SUB ESPAÑOL[/COLOR]'}


def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Peliculas", action="todas", url=host, thumbnail='https://s31.postimg.org/4g4lytrqj/peliculas.png', fanart='https://s31.postimg.org/4g4lytrqj/peliculas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Generos", action="generos", url=host,thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png'))
    
    itemlist.append( Item(channel=item.channel, title="Alfabetico", action="letras", url=host, thumbnail='https://s31.postimg.org/c3bm9cnl7/a_z.png', fanart='https://s31.postimg.org/c3bm9cnl7/a_z.png', extra='letras'))
    
    itemlist.append( Item(channel=item.channel, title="Ultimas Agregadas", action="ultimas", url=host, thumbnail='https://s31.postimg.org/3ua9kwg23/ultimas.png', fanart='https://s31.postimg.org/3ua9kwg23/ultimas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Mas Vistas", action="todas", url=host+'pelicula/peliculas-mas-vistas', thumbnail='https://s32.postimg.org/466gt3ipx/vistas.png', fanart='https://s32.postimg.org/466gt3ipx/vistas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Mas Votadas", action="todas", url=host+'pelicula/peliculas-mas-votadas', thumbnail='https://s31.postimg.org/9ooh78xej/votadas.png', fanart='https://s31.postimg.org/9ooh78xej/votadas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Estrenos DVD", action="todas", url=host+'pelicula/ultimas-peliculas/estrenos-dvd', thumbnail='https://s31.postimg.org/6sksfqarf/dvd.png', fanart='https://s31.postimg.org/6sksfqarf/dvd.png'))
    
    itemlist.append( Item(channel=item.channel, title="Actualizadas", action="todas", url=host+'pelicula/ultimas-peliculas/ultimas/actualizadas', thumbnail='https://s31.postimg.org/tucv1wmgr/actualizadas.png', fanart='https://s31.postimg.org/tucv1wmgr/actualizadas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url=host+'/buscar/?q=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))
    
    return itemlist

def todas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    
    patron = '<h2 class="titpeli bold ico_b">.*?<\/h2>.*?'
    patron += '<a href="([^"]+)" title="([^"]+)">.*?'
    patron += '<img src="([^"]+)" alt=.*?><\/a>.*?'
    patron += '<p>([^<]+)<\/p>.*?'
    patron += '<div class="stars f_left pdtop10px"><strong>Genero<\/strong>:.*?, (.*?)<\/div>.*?'
    patron +='<div class=.*?>Idioma<\/strong>:.*?img src=.*?>([^<]+)<\/div>'    
       
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedtitle, scrapedthumbnail, scrapedplot, scrapedyear, scrapedidioma in matches: 
        
        year = scrapedyear
        idioma = scrapedidioma.strip()
        idioma = scrapertools.decodeHtmlentities(idioma)
        if idioma in audio:
          idioma = audio[idioma]

        url = scrapedurl
        if idioma !='':
          title = scrapedtitle+' ('+idioma+')'+' ('+year+')'
        else:
          title = scrapedtitle+' ('+year+')'
        thumbnail = scrapedthumbnail
        plot = scrapedplot
        contentTitle = scrapedtitle
        fanart = 'https://s31.postimg.org/5worjw2nv/locopelis.png'
        
        itemlist.append( Item(channel=item.channel, action="findvideos" ,title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, extra=idioma, contentTitle = contentTitle, infoLabels={'year':year}))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb=True)
#Paginacion
    siguiente=''
    title=''
    data = scrapertools.find_single_match(data,'<ul class="nav.*?\/ul>')
    actual = scrapertools.find_single_match(data,'<a href="(\?page=\d|.*?&page=\d*)"><span><b>(.*?)<\/b>')
    if actual:
      base_url = item.url+actual[0]
      while not base_url.endswith('='): base_url= base_url[:-1]
      siguiente = int(actual[1])+1
      if base_url.endswith('='):
        siguiente_url =base_url+str(siguiente)
      titlen = 'Pagina Siguiente >>> '
      fanart = 'https://s31.postimg.org/5worjw2nv/locopelis.png'
      itemlist.append(Item(channel = item.channel, action = "todas", title =titlen, url = siguiente_url, fanart = fanart))
    
    return itemlist


def generos(item):
    
    tgenero = {"comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "accion":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
               "romance":"https://s31.postimg.org/y7vai8dln/romance.png",
               "animacion e infantil":"https://s32.postimg.org/rbo1kypj9/animacion.png",
               "ciencia ficcion":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "anime":'https://s31.postimg.org/lppob54d7/anime.png',
               "documentales":"https://s32.postimg.org/7opmvc5ut/documental.png",
               "intriga":"https://s32.postimg.org/xc2ovcqfp/intriga.png",
               "musical":"https://s31.postimg.org/7i32lca7f/musical.png",
               "western":"https://s31.postimg.org/nsksyt3hn/western.png",
               "fantasia":"https://s32.postimg.org/pklrf01id/fantasia.png",
               "asiaticas":"https://s32.postimg.org/ijqp3mt85/asiatica.png",
               "bélico (guerra)":"https://s32.postimg.org/kjbko3xhx/belica.png",
               "deporte":"https://s31.postimg.org/pdc8etc0r/deporte.png",
               "adolescente":"https://s31.postimg.org/xkz086q0r/adolescente.png",
               "artes marciales":"https://s32.postimg.org/5e80taodh/artes_marciales.png",
               "cine negro":"https://s32.postimg.org/b0882kt7p/cine_negro.png",
               "eroticas +18":"https://s31.postimg.org/6kcxutv3v/erotica.png",
               "hindu":"https://s31.postimg.org/495qn1i63/hindu.png",
               "religiosas":"https://s31.postimg.org/5tgjedlwb/religiosa.png",
               "vampiros":"https://s32.postimg.org/wt6f483j9/vampiros.png",
               "zombies":"https://s32.postimg.org/atd2jfw6t/zombies.png"}

    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron ='<li><a title.*?href="http:\/\/www.locopelis.com\/categoria\/([^"]+)">([^<]+)<\/a><\/li>.*?' 
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
	url = urlparse.urljoin(item.url,'http://www.locopelis.com/categoria/'+scrapedurl)
	title = scrapedtitle.decode('cp1252')
	title = title.encode('utf-8') 
	if title.lower() in tgenero:
           thumbnail = tgenero[title.lower()]
           fanart = tgenero[title.lower()]
        else:
           thumbnail= ''
           fanart = ''
	plot = ''
	itemlist.append( Item(channel=item.channel, action="todas" , title=title.lower(), fulltitle=item.fulltitle, url=url, thumbnail=thumbnail, plot=plot, fanart = fanart))
        
    return itemlist

def ultimas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    data = data.decode('cp1252')
    realplot=''
    patron ='<a href="([^"]+)" title="([^"]+)"><img src="([^"]+)" alt=.*? style="width:105px; height:160px; border:1px solid #999"\/><\/a>'
     
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail in matches:
        url = scrapedurl
        thumbnail = scrapedthumbnail
        plot = ''
        title = scrapedtitle
        fanart = 'https://s31.postimg.org/3ua9kwg23/ultimas.png'
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart))

    return itemlist

def letras(item):
    
    thumbletras = {'0-9':'https://s32.postimg.org/drojt686d/image.png',
    '0 - 9':'https://s32.postimg.org/drojt686d/image.png',
    '#':'https://s32.postimg.org/drojt686d/image.png',
    'a':'https://s32.postimg.org/llp5ekfz9/image.png',
    'b':'https://s32.postimg.org/y1qgm1yp1/image.png',
    'c':'https://s32.postimg.org/vlon87gmd/image.png',
    'd':'https://s32.postimg.org/3zlvnix9h/image.png',
    'e':'https://s32.postimg.org/bgv32qmsl/image.png',
    'f':'https://s32.postimg.org/y6u7vq605/image.png',
    'g':'https://s32.postimg.org/9237ib6jp/image.png',
    'h':'https://s32.postimg.org/812yt6pk5/image.png',
    'i':'https://s32.postimg.org/6nbbxvqat/image.png',
    'j':'https://s32.postimg.org/axpztgvdx/image.png',
    'k':'https://s32.postimg.org/976yrzdut/image.png',
    'l':'https://s32.postimg.org/fmal2e9yd/image.png',
    'm':'https://s32.postimg.org/m19lz2go5/image.png',
    'n':'https://s32.postimg.org/b2ycgvs2t/image.png',
    'o':'https://s32.postimg.org/c6igsucpx/image.png',
    'p':'https://s32.postimg.org/jnro82291/image.png',
    'q':'https://s32.postimg.org/ve5lpfv1h/image.png',
    'r':'https://s32.postimg.org/nmovqvqw5/image.png',
    's':'https://s32.postimg.org/zd2t89jol/image.png',
    't':'https://s32.postimg.org/wk9lo8jc5/image.png',
    'u':'https://s32.postimg.org/w8s5bh2w5/image.png',
    'v':'https://s32.postimg.org/e7dlrey91/image.png',
    'w':'https://s32.postimg.org/fnp49k15x/image.png',
    'x':'https://s32.postimg.org/dkep1w1d1/image.png',
    'y':'https://s32.postimg.org/um7j3zg85/image.png',
    'z':'https://s32.postimg.org/jb4vfm9d1/image.png'}

    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    data = data.decode('cp1252')
    data = scrapertools.find_single_match(data, '<\/form><\/table><\/div>.*?<\/ul>')

    patron ='<li><a href="(.*?)" title="Letra.*?">(.*?)<\/a><\/li>' 
    matches = re.compile(patron,re.DOTALL).findall(data)
    

    for scrapedurl, scrapedtitle in matches:
      url = scrapedurl
      title = scrapedtitle
      plot =''
      if scrapedtitle.lower() in thumbletras:
        thumbnail = thumbletras[scrapedtitle.lower()]
      else:
        thumbnail = ''
      itemlist.append( Item(channel=item.channel, action='todas', title=title , url=url, thumbnail=thumbnail, plot=plot))

    return itemlist
    
def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto

    if texto!='':
        return todas(item)
    else:
        return []    
                                 
    
def findvideos(item):
    logger.info()
    itemlist=[]
    data=httptools.downloadpage(item.url).data
     
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
        videoitem.channel = item.channel
        videoitem.folder = False
        videoitem.extra = item.thumbnail
        videoitem.fulltitle = item.title

    if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos' :
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle)) 
    return itemlist

def play(item):
    logger.info()
    itemlist =[]
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=item.url))
    for videoitem in itemlist:
        videoitem.channel = item.channel
        videoitem.title = item.title
        videoitem.folder = False
        videoitem.thumbnail = item.extra
        videoitem.fulltitle = item.fulltitle
        videoitem.infoLabels=item.infoLabels
    return itemlist

def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    #categoria='peliculas'
    try:
        if categoria == 'peliculas':
            item.url = host
            item.extra = 'peliculas'
        elif categoria == 'infantiles':
            item.url = host+'categoria/animacion-e-infantil/'
            item.extra = 'peliculas'
        itemlist = todas(item)
        if itemlist[-1].title == 'Siguiente >>>':
                itemlist.pop()
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist
