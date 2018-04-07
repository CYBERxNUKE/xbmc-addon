# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (verpeliculasnuevas) por Hernan_Ar_c
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


host = 'http://verpeliculasnuevas.com'

taudio = {'latino':'[COLOR limegreen]LATINO[/COLOR]','castellano':'[COLOR yellow]ESPAÑOL[/COLOR]','sub':'[COLOR red]ORIGINAL SUBTITULADO[/COLOR]', 'castellanolatinosub':'[COLOR orange]MULTI[/COLOR]','castellanolatino':'[COLOR orange]MULTI[/COLOR]'}

thumbaudio = {'latino':'http://flags.fmcdn.net/data/flags/normal/mx.png', 'castellano':'http://flags.fmcdn.net/data/flags/normal/es.png', 'sub':'https://s32.postimg.org/nzstk8z11/sub.png'}

tcalidad = {'hq':'[COLOR limegreen]HQ[/COLOR]','hd':'[COLOR limegreen]HD[/COLOR]','hd-1080':'[COLOR limegreen]HD-1080[/COLOR]', 'dvd':'[COLOR limegreen]DVD[/COLOR]','cam':'[COLOR red]CAM[/COLOR]', }

thumbcalidad = {'hd-1080':'https://s24.postimg.org/vto15vajp/hd1080.png','dvd':'https://s31.postimg.org/6sksfqarf/dvd.png','cam':'https://s29.postimg.org/c7em44e9j/cam.png','hq':'https://s27.postimg.org/bs0jlpdsz/image.png','hd':'https://s30.postimg.org/6vxtqu9sx/image.png'}

thumbletras = {'0-9':'https://s32.postimg.org/drojt686d/image.png',
    '1':'https://s32.postimg.org/drojt686d/image.png',
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
    "ñ":"https://s30.postimg.org/ayy8g02xd/image.png",
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

tgenero = {    "comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
               "suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
               "drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
               "accion":"https://s32.postimg.org/4hp7gwh9x/accion.png",
               "aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
               "romance":"https://s31.postimg.org/y7vai8dln/romance.png",
               "thriller":"https://s31.postimg.org/4d7bl25y3/thriller.png",
               "ciencia-ficcion":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
               "terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
               "documental":"https://s32.postimg.org/7opmvc5ut/documental.png",
               "musical":"https://s31.postimg.org/7i32lca7f/musical.png",
               "fantastico":"https://s32.postimg.org/b6xwbui6d/fantastico.png",
               "deporte":"https://s31.postimg.org/pdc8etc0r/deporte.png",
               "infantil":"https://s32.postimg.org/i53zwwgsl/infantil.png",
               "animacion":"https://s32.postimg.org/rbo1kypj9/animacion.png"}

patrones =['','<span class="clms">Sinopsis:<\/span>([^<]+)<div class="info_movie">']

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Todas", action="lista",thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', extra='peliculas/', url = host))
    
    itemlist.append( itemlist[-1].clone (title="Generos", action="menuseccion", thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png',url = host, extra='/genero'))

    itemlist.append( itemlist[-1].clone (title="Alfabetico", action="menuseccion", thumbnail='https://s31.postimg.org/c3bm9cnl7/a_z.png', fanart='https://s31.postimg.org/c3bm9cnl7/a_z.png',url = host, extra='/tag'))

    itemlist.append( itemlist[-1].clone (title="Audio", action="menuseccion",thumbnail='https://s24.postimg.org/qmvqz4uxx/audio.png', fanart='https://s24.postimg.org/qmvqz4uxx/audio.png', url = host, extra= '/audio'))
        
    itemlist.append( itemlist[-1].clone (title="Calidad", action="menuseccion",thumbnail='https://s23.postimg.org/ui42030wb/calidad.png', fanart='https://s23.postimg.org/ui42030wb/calidad.png', extra='/calidad'))

    itemlist.append( itemlist[-1].clone (title="Año", action="menuseccion", thumbnail='https://s31.postimg.org/iyl5fvzqz/pora_o.png', fanart='https://s31.postimg.org/iyl5fvzqz/pora_o.png',url = host, extra='/fecha-estreno'))

    itemlist.append( itemlist[-1].clone (title="Buscar", action="search", url=host+'?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))

    #itemlist.append( itemlist[-1].clone (title="newest", action="newest", url=host))
    
    return itemlist

def menuseccion(item):
    logger.info()
    itemlist = []
    seccion = item.extra
    data = httptools.downloadpage(item.url).data

    if seccion == '/audio':
        patron = "<a href='\/audio([^']+)' title='lista de películas en.*?'>(?:Español|Latino|Subtitulado)<\/a>"
    elif seccion == '/calidad':
    	patron = "<a href='\/calidad([^']+)' title='lista de películas en.*?'>(?:HD-1080|HD-Real|DvD|HQ|CAM)<\/a>"
    elif seccion == '/fecha-estreno':
    	patron = "<a href='\/fecha-estreno([^']+)' title='lista de películas del.*?'>.*?<\/a>"
    elif seccion == '/genero':
    	patron = '<a href="\/genero([^"]+)">.*?<\/a><\/li>'
    else:
    	patron = "<a href='\/tag([^']+)' title='lista de películas.*?'>.*?<\/a>"

    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl in matches:
    	
    	url =host+seccion+scrapedurl
    	titulo = scrapedurl.replace('/','')
    	
    	if seccion == '/audio':
    	   title = taudio[titulo.lower()]
    	   thumbnail = thumbaudio[titulo]
    	elif seccion == '/calidad':
    	   title = tcalidad[titulo.lower()]
    	   thumbnail = thumbcalidad[titulo]
    	elif seccion == '/tag':
    	   title = titulo.upper()
    	   if titulo in thumbletras:
    	      thumbnail = thumbletras[titulo]
    	   else:
    	   	  thumbnail = ''
    	else:
    		title = titulo.upper()
    		if titulo in tgenero:
    		  thumbnail = tgenero[titulo]
    		else:
    		  thumbnail = ''

        itemlist.append( Item(channel=item.channel, action='lista' , title=title , url=url, thumbnail = thumbnail))

    return itemlist


def lista (item):
    logger.info()
	
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>', "", data)

    patron = "peli><a href=([^ ]+) title=(.*?)><img src=([^ ]+) alt=.*?><div class=([^>]+)>.*?<p>.*?<\/p>.*?flags ([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedthumbnail,  scrapedcalidad, scrapedidioma in matches:
        year = scrapertools.find_single_match(scrapedtitle,'.*?\((\d{4})\)')
        scrapedtitle = scrapertools.find_single_match(scrapedtitle,'(.*?)\(\.*?')
        url = scrapedurl
        thumbnail = scrapedthumbnail
        scrapedcalidad = scrapedcalidad.replace("'","")
        scrapedcalidad = scrapedcalidad.lower()
        
        if scrapedcalidad in tcalidad:
        	scrapedcalidad = tcalidad[scrapedcalidad]
        else:
        	scrapedcalidad = '[COLOR orange]MULTI[/COLOR]'

        if scrapedidioma in taudio:
        	scrapedidioma = taudio[scrapedidioma]
        else:
        	scrapedidioma = '[COLOR orange]MULTI[/COLOR]'        
        
        title = scrapedtitle+' | '+scrapedcalidad+' | '+scrapedidioma+ ' | '
        fanart =''

        #plot= scrapertools.find_single_match(dataplot, '<span class="clms">Sinopsis:<\/span>([^<]+)<div class="info_movie">')
        plot =''
        
        itemlist.append( Item(channel=item.channel, action='findvideos' , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentTitle = scrapedtitle, extra = item.extra, infoLabels ={'year':year}))
       
# #Paginacion
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb=True)
    itemlist = fail_tmdb(itemlist)
    if itemlist !=[]:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data,"class=previouspostslink' href='([^']+)'>Siguiente &rsaquo;<\/a>")
        import inspect
        if next_page !='':
           itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = next_page, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',extra=item.extra))
    
    return itemlist

def fail_tmdb(itemlist):
    logger.info()
    realplot=''
    for item in itemlist:
        if item.infoLabels['plot'] =='':
            data = httptools.downloadpage(item.url).data
            if item.thumbnail == '':
                item.thumbnail= scrapertools.find_single_match(data,patrones[0])
            realplot = scrapertools.find_single_match(data, patrones[1])
            item.plot = scrapertools.remove_htmltags(realplot)
    return itemlist


def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto

    if texto!='':
        return lista(item)
    else:
        return []    

def findvideos(item):
    logger.info()
    itemlist=[]
    data=httptools.downloadpage(item.url).data
    data = re.sub(r"'|\n|\r|\t|&nbsp;|<br>", "", data)

    patron = 'class="servidor" alt=""> ([^<]+)<\/span><span style="width: 40px;">([^<]+)<\/span><a class="verLink" rel="nofollow" href="([^"]+)" target="_blank"> <img title="Ver online gratis"'
    matches = matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedidioma, scrapedcalidad, scrapedurl in matches:

    	scrapedidioma = scrapertools.decodeHtmlentities(scrapedidioma)
    	
    	scrapedcalidad = scrapertools.decodeHtmlentities(scrapedcalidad)
    	if scrapedidioma.lower() == 'español':
    	   scrapedidioma = 'castellano'
    	scrapedidioma = scrapedidioma.lower()
    	idioma = taudio[scrapedidioma.lower()]
    	calidad = tcalidad[scrapedcalidad.lower()]
    	url = scrapedurl
    	itemlist.append( Item(channel=item.channel, action='play' , idioma=idioma, calidad=calidad, url=url))

    for videoitem in itemlist:
        videoitem.infoLabels=item.infoLabels
        videoitem.channel = item.channel
        videoitem.folder = False
        videoitem.thumbnail = servertools.guess_server_thumbnail(videoitem.url)
        videoitem.fulltitle = item.title
        videoitem.server = servertools.get_server_from_url(videoitem.url)
        videoitem.title = item.contentTitle+' | '+videoitem.calidad+' | '+videoitem.idioma+' ('+videoitem.server+')'

       

    if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos' :
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle)) 
    return itemlist

def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    #categoria='peliculas'
    try:
        if categoria == 'peliculas':
            item.url = host
        elif categoria == 'infantiles':
            item.url = host+'/genero/infantil/'
        itemlist = lista(item)
        if itemlist[-1].title == 'Siguiente >>>':
                itemlist.pop()
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist