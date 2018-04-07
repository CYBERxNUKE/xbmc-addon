# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (cinefoxtv) por Hernan_Ar_c
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

host = 'http://www.serieslatino.tv/'

vars = {'ef5ca18f089cf01316bbc967fa10f72950790c39ef5ca18f089cf01316bbc967fa10f72950790c39':'http://www.estadepelis.com/',
	'b48699bb49d4550f27879deeb948d4f7d9c5949a8':'embed',
	 'JzewJkLlrvcFnLelj2ikbA':'php?url=',
	 'p889c6853a117aca83ef9d6523335dc065213ae86':'player', 
	 'e20fb341325556c0fc0145ce10d08a970538987':'http://yourupload.com/embed/'}

tgenero = {"acción":"https://s32.postimg.org/4hp7gwh9x/accion.png",
           "animación":"https://s32.postimg.org/rbo1kypj9/animacion.png",
           "aventura":"https://s32.postimg.org/whwh56is5/aventura.png",
           "belico":"https://s32.postimg.org/kjbko3xhx/belica.png",
           "ciencia ficción":"https://s32.postimg.org/6hp3tsxsl/ciencia_ficcion.png",
           "comedia":"https://s32.postimg.org/q7g2qs90l/comedia.png",
           "comedia romántica":"https://s30.postimg.org/4i5sbj7n5/romantica.png",
           "cortometrajes":"https://s30.postimg.org/js6w64dvl/cortometraje.png",
           "crimen":"https://s14.postimg.org/5lez1j1gx/crimen.png",
           "cristianas":"https://s31.postimg.org/5tgjedlwb/religiosa.png",
           "deportivas":"https://s31.postimg.org/pdc8etc0r/deporte.png",
           "drama":"https://s32.postimg.org/e6z83sqzp/drama.png",
           "familiar":"https://s28.postimg.org/4wwzkt2f1/familiar.png",
           "fantasía":"https://s32.postimg.org/pklrf01id/fantasia.png",
           "guerra":"https://s29.postimg.org/vqgjmozzr/guerra.png",
           "historia":"https://s13.postimg.org/52evvjrqf/historia.png",
           "intriga":"https://s32.postimg.org/xc2ovcqfp/intriga.png",
           "misterios":"https://s4.postimg.org/kd48bcxe5/misterio.png",
           "musical":"https://s31.postimg.org/7i32lca7f/musical.png",
           "romance":"https://s31.postimg.org/y7vai8dln/romance.png",
           "suspenso":"https://s31.postimg.org/kb629gscb/suspenso.png",
           "terror":"https://s32.postimg.org/ca25xg0ed/terror.png",
           "thriller":"https://s31.postimg.org/4d7bl25y3/thriller.png"}

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( item.clone (title="Series", action="lista",thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png', extra='peliculas/', url = host+'lista-de-series/'))
    
    itemlist.append( itemlist[-1].clone (title="Doramas", action="lista", thumbnail='https://s30.postimg.org/ors2tiqht/doramas.png', fanart='https://s30.postimg.org/ors2tiqht/doramas.png',url = host+'lista-de-doramas/', extra='/genero'))

    itemlist.append( itemlist[-1].clone (title="Generos", action="generos", thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png',url = host, extra='/genero'))

    itemlist.append( itemlist[-1].clone (title="Buscar", action="search", url=host+'resultados/?q=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))

    return itemlist

def lista (item):
    logger.info ()
	
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    #logger.debug(data)
    #return
    patron = '<div id=mt-1830 class=item><a href=(.*?)><div class=image><img src=(.*?) alt=(.*?) width=.*? height=.*?class=player>.*?class=ttx>(.*?)<div class=degradado>.*?class=year>(.*?)<\/span><\/div><\/div>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedplot, scrapedyear in matches:
        url = host+scrapedurl
        thumbnail = scrapedthumbnail
        plot= scrapedplot
        scrapedtitle = scrapertools.decodeHtmlentities(scrapedtitle)
        title = scrapedtitle+' '+scrapedyear
        fanart = ''
        itemlist.append( Item(channel=item.channel, action='temporadas' , title=scrapedtitle , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentSerieName = scrapedtitle, contentYear = scrapedyear, infoLabels={'year':scrapedyear}))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb= True)   
 #Paginacion

    if itemlist !=[]:
        actual_page_url = item.url
        next_page = scrapertools.find_single_match(data,'<div class=pag_b><a href=(.*?) >Siguiente<\/a><\/div>')
        import inspect
        if next_page !='':
           itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = item.url+next_page, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'))
    return itemlist

def temporadas(item):
    logger.info()
    itemlist = []
    
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    #logger.debug(data)
    #return

    patron = '<span class=se-t.*?>(.*?)<\/span>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    infoLabels = item.infoLabels
    for scrapedtitle in matches:
    	
        contentSeasonNumber = scrapedtitle.strip('')
        title = item.contentSerieName+' Temporada '+scrapedtitle
        thumbnail = item.thumbnail
        plot = item.plot
        fanart = item.fanart
        infoLabels['season']=contentSeasonNumber

        itemlist.append( Item(channel=item.channel, action= 'episodiosxtemp' , url= item.url, title=title ,contentSerieName = item.contentSerieName, thumbnail=thumbnail, plot=plot, fanart = fanart, contentSeasonNumber = contentSeasonNumber, infoLabels=item.infoLabels))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb= True)
    
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url,
                             action="add_serie_to_library", extra="episodiosxtemp", contentSerieName = item.contentSerieName, contentYear=item.contentYear, extra1='library'))
    
    return itemlist

def episodiosxtemp(item):
    logger.info()
    itemlist =[]               
    data = httptools.downloadpage(item.url).data
    data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
    patron = 'class=numerando>(.*?)x(.*?)<\/div><div class=episodiotitle><a href=(.*?)>(.*?)<\/a><span class=date>.*?'
    matches = re.compile(patron,re.DOTALL).findall(data)
    infoLabels = item.infoLabels
    for scrapedtemp, scrapedep, scrapedurl, scrapedtitle in matches:
        url = host+scrapedurl
        contentEpisodeNumber = scrapedep.strip(' ')
        temp = scrapedtemp.strip(' ')
        title = item.contentSerieName+' '+temp+'x'+contentEpisodeNumber+' '+scrapedtitle
        thumbnail = item.thumbnail
        plot = item.plot
        fanart=item.fanart
        infoLabels['episode']=contentEpisodeNumber
        logger.debug('Nombre: '+item.contentSerieName)
    	infoLabels = item.infoLabels
        if item.extra1 == 'library':
        	itemlist.append( Item(channel=item.channel, action="findvideos" , title=title, fulltitle = item.fulltitle, url=url, thumbnail=item.thumbnail, plot=plot, contentSerieName = item.contentSerieName, contentSeasonNumber = item.contentSeasonNumber, infoLabels=infoLabels ))
        elif temp == item.contentSeasonNumber:
    		itemlist.append( Item(channel=item.channel, action="findvideos" , title=title, fulltitle = item.fulltitle, url=url, thumbnail=item.thumbnail, plot=plot, contentSerieName = item.contentSerieName, contentSeasonNumber = item.contentSeasonNumber, infoLabels=infoLabels ))

    
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb= True)
    return itemlist


def generos(item):    

	logger.info()

	itemlist = []
	norep = []
	data = httptools.downloadpage(item.url).data
	data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
	patron = '<li class=cat-item cat-item-.*?><a href=(.*?)>([^<]+)<\/a>'
	matches = re.compile(patron,re.DOTALL).findall(data)

	for scrapedurl, scrapedtitle in matches:

	    url = host+scrapedurl
	    title = scrapedtitle.lower()
	    if title in tgenero:
	       thumbnail = tgenero[title.lower()]
	    else:
	    	thumbnail =''

	    itemactual = Item(channel=item.channel, action='lista' , title=title , url=url, thumbnail=thumbnail, extra = item.extra)
	    
	    if title not in norep:
	    	itemlist.append(itemactual)
	   	norep.append (itemactual.title)
	return itemlist

def dec(encurl):

	logger.info()
	url=''
	encurl= encurl.translate(None, "',(,),;")
	encurl= encurl.split('+')

	for cod in encurl:
		if cod in vars:
			    url= url+vars[cod]
		else:
			url=url+cod
	return url


def findvideos(item):
	logger.info()
	
	itemlist =[]

	data = httptools.downloadpage(item.url).data
	patron = 'function play.*?servidores.*?attr.*?src.*?\+([^;]+);'
	matches = re.compile(patron,re.DOTALL).findall(data)
	title = item.title
	enlace = scrapertools.find_single_match(data,'var e20fb341325556c0fc0145ce10d08a970538987 =.*?"\/your\.".*?"([^"]+)"')        

	for encurl in matches:
	
		if 'e20fb34' in encurl:
		   url= dec(encurl)
		   url=url+enlace

		else:
		   url=dec(encurl)
		title =''
		server=''
		if '/opl.' in url:
			server='Openload'
		elif '/your' in url:
			server='Yourupload'
		elif '/sen.'in url:
			server='Sendvid'

		if item.extra == 'peliculas':
		    title = item.contentTitle+' ('+server+')'
		    plot = scrapertools.find_single_match(data,'<p>([^<]+)<\/p>')
		else:
			title = item.contentSerieName+' ('+server+')'
			plot = item.plot

		thumbnail = servertools.guess_server_thumbnail(title)	
		
		if 'player' not in url:
			itemlist.append(item.clone(title=title, url=url, action="play",plot=plot, thumbnail=thumbnail))


	return itemlist


def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    if texto!='':
       return lista(item)

def play(item):
     logger.info()
     itemlist = []
     data = httptools.downloadpage(item.url, add_referer=True).data
          
     itemlist = servertools.find_video_items(data=data)

     if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))

     return itemlist

