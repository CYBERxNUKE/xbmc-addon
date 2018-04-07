# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (EstaDePelis) por Hernan_Ar_c
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

host = 'http://www.estadepelis.com/'
headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
          ['Referer', host]]

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

	itemlist.append( item.clone (title="Peliculas", action="menupeliculas",thumbnail='https://s31.postimg.org/4g4lytrqj/peliculas.png', fanart='https://s31.postimg.org/4g4lytrqj/peliculas.png'))

	itemlist.append( item.clone (title="Series", action="lista",thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png',url = host+'lista-de-series/', extra = 'series' ))

	itemlist.append( item.clone (title="Doramas", action="lista",thumbnail='https://s30.postimg.org/ors2tiqht/doramas.png', fanart='https://s30.postimg.org/ors2tiqht/doramas.png',url = host+'lista-de-doramas/', extra = 'series'))

	itemlist.append( item.clone (title="Documentales", action="lista",thumbnail='https://s21.postimg.org/i9clk3u6v/documental.png', fanart='https://s21.postimg.org/i9clk3u6v/documental.png', url = host+'lista-de-documentales/', extra = 'peliculas'))

	itemlist.append( itemlist[-1].clone (title="Buscar", action="search", url=host+'search?q=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))

	return itemlist


def menupeliculas(item):
	logger.info()

	itemlist = []

	itemlist.append( item.clone (title="Todas", action="lista",thumbnail='https://s12.postimg.org/iygbg8ip9/todas.png', fanart='https://s12.postimg.org/iygbg8ip9/todas.png', url = host+'lista-de-peliculas/', extra = 'peliculas'))

	itemlist.append( item.clone (title="Ultimas", action="lista",thumbnail='https://s31.postimg.org/3ua9kwg23/ultimas.png', fanart='https://s31.postimg.org/3ua9kwg23/ultimas.png', url = host, extra = 'peliculas'))

	itemlist.append( item.clone (title="Generos", action="generos",thumbnail='https://s31.postimg.org/szbr0gmkb/generos.png', fanart='https://s31.postimg.org/szbr0gmkb/generos.png', url = host, extra = 'peliculas'))

	return itemlist


def lista(item):    

	logger.info()

	itemlist = []
	data = httptools.downloadpage(item.url).data
	data = re.sub(r'"|\n|\r|\t|&nbsp;|<br>|\s{2,}', "", data)
	contentSerieName = ''

	patron = '<div class=movie><div class=imagen><img src=(.*?) alt=(.*?) width=.*? height=.*?\/><a href=(.*?)><span class=player>.*?class=year>(.*?)<\/span>'
	matches = re.compile(patron,re.DOTALL).findall(data)

	if item.extra=='peliculas':
		accion = 'findvideos'
	else:
		accion = 'temporadas'


	for scrapedthumbnail, scrapedtitle, scrapedurl, scrapedyear in matches:

	    scrapedurl = scrapedurl.translate(None,'"')
	    scrapedurl = scrapedurl.translate(None,"'")
	    url = host+scrapedurl
	    thumbnail = scrapedthumbnail
	    title = scrapedtitle
	    year = scrapedyear
	    if item.extra == 'series':
	    	contentSerieName = scrapedtitle

	    
	    itemlist.append( Item(channel=item.channel, action=accion , title=title , url=url, thumbnail=thumbnail, contentTitle = scrapedtitle, extra = item.extra, contentSerieName=contentSerieName, infoLabels={'year':year}))
	tmdb.set_infoLabels_itemlist(itemlist, seekTmdb= True)     
	# #Paginacion

	if itemlist !=[]:
	    actual_page_url = item.url
	    next_page = scrapertools.find_single_match(data,'<div class=siguiente><a href=(.*?)>')
	    url = host+next_page
	    import inspect
	    if next_page !='':
	       itemlist.append(Item(channel = item.channel, action = "lista", title = 'Siguiente >>>', url = url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png',extra=item.extra))
	return itemlist

def generos(item):    

	logger.info()

	itemlist = []
	norep = []
	data = httptools.downloadpage(item.url).data

	patron = '<li class="cat-item cat-item-.*?"><a href="([^"]+)">([^<]+)<\/a>'
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

def temporadas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = '<li class="has-sub"><a href="([^"]+)"><span><b class="icon-bars"><\/b> ([^<]+)<\/span><\/a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    temp = 1
    infoLabels = item.infoLabels
    for scrapedurl, scrapedtitle in matches:
        url = scrapedurl
        title = scrapedtitle.strip('')
        contentSeasonNumber = temp
        infoLabels['season']=contentSeasonNumber
        thumbnail = item.thumbnail
        plot = scrapertools.find_single_match(data,'<p>([^<]+)<\/p>')
        itemlist.append( Item(channel=item.channel, action="episodiosxtemp" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, contentSerieName=item.contentSerieName, contentSeasonNumber = contentSeasonNumber, plot = plot, infoLabels=infoLabels))
        temp = temp +1
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb= True)     
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url, action="add_serie_to_library", extra="episodios", contentSerieName=item.contentSerieName, extra1 = item.extra1, temp=str(temp)))
    
    return itemlist

def episodios(item):
    
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    temp = 'temporada-'+str(item.contentSeasonNumber)
    patron = '<li>.\s*<a href="(.*?)">.\s*<span.*?datex">([^<]+)<'
        
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl, scrapedepisode in matches:
        url = host+scrapedurl
        title = item.contentSerieName+' '+scrapedepisode
        thumbnail = item.thumbnail
        fanart=''
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title, fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=item.plot, extra = item.extra, contentSerieName=item.contentSerieName))
	            
    return itemlist            


def episodiosxtemp(item):
    
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    temp = 'temporada-'+str(item.contentSeasonNumber)
    patron = '<li>.\s*<a href="(.*?-'+temp+'.*?)">.\s*<span.*?datex">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)
    infoLabels=item.infoLabels
    for scrapedurl, scrapedepisode in matches:
        url = host+scrapedurl
        title = item.contentSerieName+' '+scrapedepisode
        scrapedepisode=re.sub(r'.*?x','',scrapedepisode)
        infoLabels['episode']=scrapedepisode
        thumbnail = item.thumbnail
        fanart=''
        itemlist.append( Item(channel=item.channel, action="findvideos" , title=title, fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=item.plot, extra = item.extra, contentSerieName=item.contentSerieName, infoLabels=infoLabels))
        
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb= True) 
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

	if config.get_library_support() and len(itemlist) > 0 and item.extra !='findvideos':
		itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url, 
			action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))

	
			

	return itemlist


def play(item):
     logger.info()
     itemlist = []
     #data = scrapertools.anti_cloudflare(item.url, host=host, headers=headers)
     data = httptools.downloadpage(item.url, add_referer=True).data
          
     itemlist = servertools.find_video_items(data=data)

     if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta pelicula a la biblioteca[/COLOR]', url=item.url,
                             action="add_pelicula_to_library", extra="findvideos", contentTitle = item.contentTitle))

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
            item.extra = 'peliculas'
        elif categoria == 'infantiles':
            item.url = host+'search?q=animación'
            item.extra = 'peliculas'
        itemlist = lista(item)
        if itemlist[-1].title == 'Siguiente >>>':
                itemlist.pop()
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist






	
