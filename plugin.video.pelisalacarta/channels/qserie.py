# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (qserie) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys


from core import logger
from core import tmdb
from core import config
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools

host='http://www.qserie.com'

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Series", action="todas", url=host, thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png'))
    
    itemlist.append( Item(channel=item.channel, title="Generos", action="generos", url=host,thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png'))
    
    itemlist.append( Item(channel=item.channel, title="Alfabetico", action="lasmas", url=host, thumbnail='https://s31.postimg.org/c3bm9cnl7/a_z.png', fanart='https://s31.postimg.org/c3bm9cnl7/a_z.png', extra='letras'))
    
    itemlist.append( Item(channel=item.channel, title="Ultimas Agregadas", action="ultimas", url=host, thumbnail='https://s31.postimg.org/3ua9kwg23/ultimas.png', fanart='https://s31.postimg.org/3ua9kwg23/ultimas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Mas Vistas", action="lasmas", url=host, thumbnail='https://s32.postimg.org/466gt3ipx/vistas.png', fanart='https://s32.postimg.org/466gt3ipx/vistas.png', extra='Vista'))
    
    itemlist.append( Item(channel=item.channel, title="Mas Votadas", action="lasmas", url=host, thumbnail='https://s31.postimg.org/9ooh78xej/votadas.png', fanart='https://s31.postimg.org/9ooh78xej/votadas.png', extra='Votos'))
    
    return itemlist

def todas(item):
    logger.info()
    audio = {'Latino':'[COLOR limegreen]LATINO[/COLOR]','Español':'[COLOR yellow]ESPAÑOL[/COLOR]','Sub Español':'[COLOR red]ORIGINAL SUBTITULADO[/COLOR]'}
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|&nbsp;|<br>", "", data)
    
    patron = '<h2 class=.*?><a href="([^"]+)" title="([^"]+)">.*?\/h2>.*?<img src="([^"]+)".*?\/><\/a>.*?<p>([^<]+)<\/p>.*?<strong>Genero<\/strong>: .*?, (.*?)<\/div>.*?<img src=.*?>([^<]+)<\/div>'
    matches = re.compile(patron,re.DOTALL).findall(data)
     
    for scrapedurl,scrapedtitle, scrapedthumbnail, scrapedplot, scrapedyear,scrapedidioma in matches:
        idioma = scrapedidioma.strip()
        idioma = scrapertools.decodeHtmlentities(idioma) 
        url = urlparse.urljoin(item.url,scrapedurl)
        year = scrapedyear
        if idioma in audio:
           idioma=audio[idioma]
        else:
           idioma=audio['Sub Español']    
        
        title = scrapertools.decodeHtmlentities(scrapedtitle)+' ('+idioma+')'
        thumbnail = scrapedthumbnail
        plot = scrapedplot
        fanart = 'https://s31.postimg.org/dousrbu9n/qserie.png'
        itemlist.append( Item(channel=item.channel, action="temporadas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, extra=idioma, contentSerieName = scrapedtitle, infoLabels={'year':year}))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)    
#Paginacion
    siguiente=''
    title=''
    actual = scrapertools.find_single_match(data,'<li><a href=".*?"><span><b>([^<]+)<\/b><\/span><\/a><\/li>')
    ultima = scrapertools.find_single_match(data,'<li><a href=".*?page=([^"]+)">Ultima<\/a><\/li>')
    if 'page' in item.title:
        while not item.url.endswith('='): item.url= item.url[:-1]
    if actual:
       siguiente = int(actual)+1
       if item.url.endswith('='):
          siguiente_url =item.url+str(siguiente)
       else:
          siguiente_url =item.url+'?&page='+str(siguiente)  
    if actual and ultima and siguiente <= int(ultima):
       titlen = 'Pagina Siguiente >>> '+str(actual)+'/'+str(ultima)
       fanart = 'https://s32.postimg.org/4q1u1hxnp/qserie.png'
       thumbnail ='https://s32.postimg.org/4zppxf5j9/siguiente.png'
       itemlist.append(Item(channel = item.channel, action = "todas", title =titlen, url = siguiente_url, fanart = fanart, thumbnail=thumbnail))
    return itemlist

def temporadas(item):
    logger.info()
    itemlist = []
    
    data = httptools.downloadpage(item.url).data
    url_base= item.url
    patron = '<a href="javascript:.*?;" class="lccn"><b>([^<]+)<\/b><\/a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    infoLabels=item.infoLabels
    temp=1
    if matches:
        for scrapedtitle in matches:
           url = url_base
           title = scrapedtitle
           thumbnail = item.thumbnail
           plot = item.plot
           contentSeasonNumber=str(temp)

           infoLabels['season']=contentSeasonNumber
           fanart = scrapertools.find_single_match(data,'<img src="([^"]+)"/>.*?</a>')
           itemlist.append( Item(channel=item.channel, action="episodiosxtemp" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, plot=plot, fanart = fanart, contentSeasonNumber=contentSeasonNumber, contentSerieName =item.contentSerieName, infoLabels=infoLabels))
           temp = temp+1
               
        if config.get_library_support() and len(itemlist) > 0:
            itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url,
                             action="add_serie_to_library", extra="episodios", contentSerieName=item.contentSerieName ))
        tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)            
        return itemlist
    else:
        item.title =''
        item.modo = 'unico'
        return episodiosxtemp(item)

def episodios(item):
    logger.info()
    itemlist = []
    templist = temporadas(item)
    if item.modo == 'unico':
      itemlist += episodiosxtemp(item)
    else:  
      for tempitem in templist:
        itemlist += episodiosxtemp(tempitem) 

    return itemlist
 
def episodiosxtemp(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    infoLabels = item.infoLabels
    temp = item.contentSeasonNumber
    if item.title=='':
        temp = '1'
        item.contenSeasonNumber = temp
        infoLabels['season']= temp

        patron ='<li><a href="([^"]+)" class="lcc"><b>([^<]+)<\/b>.*?<\/a><\/li>'

    else: 
        patron = '<li><a href="([^"]+)" class="lcc"><b>([^<]+)<\/b> - Temp\. '+temp+'<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedurl,scrapedtitle in matches:
        
        url = urlparse.urljoin(item.url,scrapedurl)
        capitulo = re.findall(r'\d+',scrapedtitle)
        contentEpisodeNumber = str(capitulo[0])
        infoLabels['episode']=contentEpisodeNumber
        title = item.contentSerieName+' '+temp+'x'+contentEpisodeNumber
        thumbnail = item.thumbnail
        plot = item.plot
        fanart=item.fanart
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title, fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=plot, extra = item.extra, extra1 =item.extra1, extra2=item.extra2, infoLabels = infoLabels))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    if item.modo == 'unico':
        if config.get_library_support() and len(itemlist) > 0:
                itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url,
                             action="add_serie_to_library", extra="episodios", contentSerieName=item.contentSerieName, modo ='unico', contentSeasonNumber = item.contenSeasonNumber))
    
    
    return itemlist
    



def generos(item):
    
    tgenero = {"comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "acción":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
               "aventuras":"https://s32.postimg.org/whwh56is5/aventura.png",
               "romance":"https://s31.postimg.org/y7vai8dln/romance.png",
               "infantil":"https://s32.postimg.org/i53zwwgsl/infantil.png",
               "ciencia ficción":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "anime":'https://s31.postimg.org/lppob54d7/anime.png',
               "animes":"https://s31.postimg.org/lppob54d7/anime.png",
               "dibujos":"https://s32.postimg.org/fskqyu7md/dibujos.png",
               "documental":"https://s32.postimg.org/7opmvc5ut/documental.png",
               "fantástico":"https://s32.postimg.org/b6xwbui6d/fantastico.png",
               "intriga":"https://s32.postimg.org/xc2ovcqfp/intriga.png",
               "musical":"https://s31.postimg.org/7i32lca7f/musical.png",
               "secuela":"https://s31.postimg.org/5bho037rv/secuela.png",
               "thriller (suspenso)":"https://s31.postimg.org/4d7bl25y3/thriller.png",
               "western":"https://s31.postimg.org/nsksyt3hn/western.png"}

    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron ='<li><a title="([^"]+)" href="([^"]+)" onclick=.*?' 
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
	url = urlparse.urljoin(item.url,scrapedurl)
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
    realplot=''
    patron ='<li><a title="([^"]+)" href="([^"]+)"><strong>.*?</a></li>' 
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedtitle, scrapedurl in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        data = httptools.downloadpage(scrapedurl).data
        thumbnail= scrapertools.get_match(data,'<link rel="image_src" href="([^"]+)"/>')
        realplot = scrapertools.find_single_match(data, '<p itemprop="articleBody">([^<]+)<\/p> ')
        plot = scrapertools.remove_htmltags(realplot)
        inutil = re.findall(r' Temporada \d', scrapedtitle)
        title = scrapedtitle
        title = scrapertools.decodeHtmlentities(title)
        realtitle = scrapedtitle.replace(inutil[0],'')
        fanart = 'https://s31.postimg.org/3ua9kwg23/ultimas.png'
        itemlist.append( Item(channel=item.channel, action="temporadas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentSerieName = realtitle))

    return itemlist

def lasmas(item):
    
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
    realplot=''
    if item.extra == 'letras':
         patron ='<li><a href="([^"]+)" title="Series que comienzan con.*?">([^<]+)</a></li>' 
    else:    
         patron ='<a href="([^"]+)" title="([^V]+)'+item.extra+'.*?">' 
    
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        if item.extra != 'letras':
           data = httptools.downloadpage(scrapedurl).data
           thumbnail= scrapertools.get_match(data,'<link rel="image_src" href="([^"]+)"/>')
           realplot = scrapertools.find_single_match(data, '<p itemprop="articleBody">([^<]+)<\/p> ')
           plot = scrapertools.remove_htmltags(realplot)
           action='temporadas'
        else:
           if scrapedtitle.lower() in thumbletras:
              thumbnail = thumbletras[scrapedtitle.lower()]
           else:
              thumbnail = ''
           plot=''
           action='todas'
        title = scrapedtitle.replace(': ','')
        title = scrapertools.decodeHtmlentities(title)
        if item.extra == 'letras':
           fanart = 'https://s31.postimg.org/c3bm9cnl7/a_z.png'
        elif item.extra == 'Vista':
           fanart = 'https://s32.postimg.org/466gt3ipx/vistas.png' 
        else:
           fanart = ''  
   
        itemlist.append( Item(channel=item.channel, action=action, title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentSerieName = scrapedtitle))

    return itemlist
    
def findvideos(item):
    logger.info()
    itemlist=[]
    data = httptools.downloadpage(item.url).data
    
    anterior = scrapertools.find_single_match(data,'<a class="left" href="([^"]+)" title="Cap.tulo Anterior"></a>')
    siguiente = scrapertools.find_single_match(data,'<a class="right" href="([^"]+)" title="Cap.tulo Siguiente"></a>')
    titulo = scrapertools.find_single_match(data,'<h1 class="tithd bold fs18px lnht30px ico_b pdtop10px">([^<]+)</h1> ')
    existe = scrapertools.find_single_match(data,'<center>La pel.cula que quieres ver no existe.</center>')
    
    from core import servertools
    itemlist.extend(servertools.find_video_items(data=data))
    for videoitem in itemlist:
       if 'youtube' in videoitem.url:
          itemlist.remove(videoitem)
    for videoitem in itemlist:
       videoitem.channel=item.channel
       videoitem.action="play"
       videoitem.folder=False
       videoitem.fanart =item.fanart
       videoitem.title = titulo+" "+videoitem.server
    if item.extra2 != 'todos':
       data = httptools.downloadpage(anterior).data
       existe = scrapertools.find_single_match(data,'<center>La pel.cula que quieres ver no existe.</center>')
       if not existe:
           itemlist.append( Item(channel=item.channel, action="findvideos" , title='Capitulo Anterior' , url=anterior, thumbnail='https://s31.postimg.org/k5kpwyrgb/anterior.png', folder =True ))
    
       data = httptools.downloadpage(siguiente).data
       existe = scrapertools.find_single_match(data,'<center>La pel.cula que quieres ver no existe.</center>')
       if  not existe:
           itemlist.append( Item(channel=item.channel, action="findvideos" , title='Capitulo Siguiente' , url=siguiente, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png', folder =True ))
        
    return itemlist    
    
    
    
