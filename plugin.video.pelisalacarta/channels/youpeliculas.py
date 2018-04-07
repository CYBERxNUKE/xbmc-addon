# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Canal YouPeliculas.co by EpNiebla
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import config
from core import logger
from core import httptools
from core import scrapertools
from core.item import Item
from core import servertools
from core import jsontools

host = 'http://youpeliculas.co'

def mainlist(item):
    logger.info()

    itemlist = []
    itemlist.append(item.clone(title="[Peliculas]", action="peliculas"))
    itemlist.append(item.clone(title="[Series] Novedades/Actualizadas", action="lista", extra={'post':'type=series', 'page_current':0, 'max_pages':1}))
    itemlist.append(item.clone(title="[Anime] Novedades/Actualizadas", action="lista", extra={'post':'type=anime', 'page_current':0, 'max_pages':1}))
    itemlist.append(item.clone(title="[Infantiles] Novedades/Actualizadas", action="lista", extra={'post':'type=series-animadas', 'page_current':0, 'max_pages':1}))
    itemlist.append(item.clone(title="[Dramas] Novedades/Actualizadas", action="lista", extra={'post':'type=dramas', 'page_current':0, 'max_pages':1}))
    itemlist.append(item.clone(title="Buscar", action="search" ))

    return itemlist

def peliculas(item):
    logger.info()

    itemlist = []
    itemlist.append(item.clone(title="[Peliculas] Novedades/Actualizadas", action="lista", extra={'post':'type=all-movies', 'page_current':0, 'max_pages':1}))
    itemlist.append(item.clone(title="[Peliculas] Por Categorias", action="peliculas_tipo", extra='categorias'))
    itemlist.append(item.clone(title="[Peliculas] Por Servidor", action="peliculas_tipo", extra='servidor'))
    itemlist.append(item.clone(title="[Peliculas] Por Año", action="peliculas_tipo", extra='anio'))

    return itemlist
	
def peliculas_tipo(item):
    logger.info()
    itemlist = []
	
    seccion = item.extra
    extradata = '';
    data = httptools.downloadpage(host+'/peliculas-online').data
    if seccion == 'anio':
        extradata = 'type=all-movies&filter_year='
        data = scrapertools.find_single_match(data,'<select id="filter_year">(.*?)</select>')
        patron = '<option value="([^"]+)">([^<]+)</option>'
    elif seccion == 'servidor':
        extradata = 'type=all-movies&filter_platform='
        data = scrapertools.find_single_match(data,'<select id="filter_platform">(.*?)</select>')
        patron = '<option value="([^"]+)">([^<]+)</option>'
    elif seccion == 'categorias':
        extradata = 'type=category&category='
        data = scrapertools.find_single_match(data,'<ul class="nav navbar-nav">(.*?)<div class="navbar-form navbar-left"')
        patron = '<li class=""><a href="'+host+'/peliculas-online/([^"]+)" class="">([^"]+)</a></li>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    aux=''
    for scrapedurl,extra in matches:
        if scrapedurl.strip() != aux:
            itemlist.append(Item(channel=item.channel, action='lista' , title=extra, extra={'post':extradata+scrapedurl.strip(), 'page_current':0, 'max_pages':1}))
            aux=scrapedurl.strip()

    return itemlist    
	
def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = host+'/you/load_data'
    item.extra = {'post':'type=search&category='+texto, 'page_current':0, 'max_pages':1}
    if texto!='':
        return lista(item)
    else:
        return []  
		
def lista (item):
    logger.info ()
    itemlist = []

    if item.extra['page_current']==0:
        data = httptools.downloadpage(host+'/you/load_data', item.extra['post']).data
    else:
        data = httptools.downloadpage(host+'/you/load_data', item.extra['post']+'&page_current='+str(item.extra['page_current'])).data
		
    matches = re.compile('<li(.*?)</li>',re.DOTALL).findall(data)
    for li in matches:
        # pelicula
        patron1 = 'data-id="([^"]+)" data-type="movie" data-imdb=[^<]+<div class="movie_image[^"]+"[^<]+<div class="[^"]+"[^<]+</div[^<]+<a href="([^"]+)" title="Ver (.*?) Película OnLine".*?<img src="([^"]+)" width=".*?<div class="movie_container">'
        match = re.compile(patron1,re.DOTALL).findall(li)
        for vidId, scrapedurl, scrapedtitle, scrapedthumbnail in match:
            itemlist.append(Item(channel=item.channel, action='findvideos', title=scrapedtitle, thumbnail=scrapedthumbnail, contentTitle = scrapedtitle, extra='vid='+vidId+'&ep='+vidId+'&type=movie' ))
        # Compilado de peliculas
        patron2 = 'data-type="movie" data-imdb=[^<]+<div class="movie_image[^"]+"[^<]+<div class="[^"]+"[^<]+</div[^<]+<a href="'+host+'/([^"]+)" title="Ver (.*?) Películas OnLine".*?<img src="([^"]+)".*?<div class="movie_container">'
        match = re.compile(patron2,re.DOTALL).findall(li)
        for scrapedurl, scrapedtitle, scrapedthumbnail in match:
            itemlist.append(Item(channel=item.channel, action='lista' , title=scrapedtitle+' (LISTADO)', thumbnail=scrapedthumbnail, contentTitle = scrapedtitle+' (LISTADO)', extra={'post':'type=seasons&category='+scrapedurl, 'page_current':0, 'max_pages':1} ))
        # series
        patron3 = 'data-id="([^"]+)" data-type="[^"]+" data-imdb=[^<]+<div class="movie_image[^"]+"[^<]+<div class="[^"]+"[^<]+</div[^<]+<a href="([^"]+)" title="Ver (.*?) Serie OnLine".*?<img src="([^"]+)".*?Temporada: <span>([^<]+)</span><br/>Episodio: <span>([^<]+)</span>'    
        match = re.compile(patron3,re.DOTALL).findall(li)
        for serieId, scrapedurl, scrapedtitle, scrapedthumbnail, tempo, cap in match:
            itemlist.append(Item(channel=item.channel, action='episodios', title=scrapedtitle+'[Temp. '+tempo+'] (Cap. '+cap+')', url=scrapedurl, contentTitle = scrapedtitle+'[Temp. '+tempo+'] (Cap. '+cap+')', thumbnail=scrapedthumbnail, extra=serieId, temporada=tempo, moreTemp=True ))
        # temporadas
        patron4 = 'data-id="([^"]+)" data-type="serie" data-imdb=[^<]+<div class="movie_image[^"]+"[^<]+<div class="[^"]+"[^<]+</div[^<]+<a href="([^"]+)" title="Ver (.*?) Serie OnLine".*?<img src="([^"]+)".*?<div class="lasted_te">Episodio: <span>([^<]+)</span>'    
        match = re.compile(patron4,re.DOTALL).findall(li)
        for serieId, scrapedurl, scrapedtitle, scrapedthumbnail, cap in match:
            itemlist.append(Item(channel=item.channel, action='episodios', title=scrapedtitle+' (Cap. '+cap+')', url=scrapedurl, contentTitle=scrapedtitle+' (Cap. '+cap+')', thumbnail=scrapedthumbnail, extra=serieId, temporada=scrapertools.find_single_match(scrapedtitle,'Temp. (.*?)]'), moreTemp=False ))	
        # otros casos
        patron5 = 'data-id="([^"]+)" data-type="movie" data-imdb=[^<]+<div class="movie_image[^"]+"[^<]+<div class="[^"]+"[^<]+</div[^<]+<a href="([^"]+)" title="Ver (.*?) Serie OnLine".*?<img src="([^"]+)".*?<div class="lasted_te">Episodio: <span>([^<]+)</span>'    
        match = re.compile(patron5,re.DOTALL).findall(li)
        for serieId, scrapedurl, scrapedtitle, scrapedthumbnail, cap in match:
            itemlist.append(Item(channel=item.channel, action='episodios', title=scrapedtitle+' (Cap. '+cap+')', url=scrapedurl, contentTitle=scrapedtitle+' (Cap. '+cap+')', thumbnail=scrapedthumbnail, extra=serieId, temporada='1', moreTemp=False ))	
        #logger.info ('peliculasalacarta.channel.verpeliculasnuevas data-total'+li)
		
    #Paginacion
    if itemlist !=[]:
        patron = '<buttom class=".*?load_more" data-total="([^"]+)" data-pages="([^"]+)"><i class="[^"]+"></i> Ver más</buttom>'
        matches = re.compile(patron, re.DOTALL).findall(data)
        if matches:
            itemlist.append(item.clone(title="Pagina Siguiente", action='lista', extra={'post':item.extra['post']+'&total='+matches[0][0], 'page_current':1, 'max_pages': int(matches[0][1]) }))
        else:
            if item.extra['page_current']+1<item.extra['max_pages']:
                itemlist.append(item.clone(title="Pagina Siguiente", action='lista', extra={'post':item.extra['post'], 'page_current':item.extra['page_current']+1, 'max_pages': item.extra['max_pages'] }))
			
    return itemlist
  
def episodios (item):
    logger.info ()
    itemlist = []
	
    data = httptools.downloadpage(host+'/you/load-options-episodes','type=episodes&vid='+item.extra).data
    data = scrapertools.find_single_match(data,'<table class="table">(.*?)</table>')
    patron = '<tr id="([^"]+)" class="[^"]+"[^<]+<td[^<]+<div[^<]+<strong>([^<]+)</strong[^<]+</div[^<]+</td[^<]+<td[^<]+<div[^>]+>([^<]+)<span.*?</tr>'

    if int(item.temporada)>1 and item.moreTemp!=False:
        match = re.compile('.co/(.*?)-temp-'+item.temporada, re.DOTALL).findall(item.url)
        if match:
            itemlist.append(Item(channel=item.channel, action='lista', title='Temporadas Anteriores', contentTitle = 'Temporadas Anteriores', extra={'post':'type=seasons&category='+match[0], 'page_current':0, 'max_pages':1}  ))
	
    matches = re.compile(patron,re.DOTALL).findall(data)
    for capId, cap, nameCap in matches:
        itemlist.append(Item(channel=item.channel, action='findvideos', title='[Temp. '+item.temporada+'] Cap. '+cap+'.- '+nameCap, thumbnail=item.thumbnail, contentTitle = '[Temp.]'+item.temporada+'Cap. '+cap+'.- '+nameCap, extra='vid='+item.extra+'&ep='+capId+'&type=episodes' ))

    return itemlist    
	
def findvideos(item):
    logger.info ()
    itemlist=[]
    data = httptools.downloadpage(host+'/you/load-options',item.extra).data
    #data = re.sub(r"'|\n|\r|\t|&nbsp;|<br>", "", data)
	
    listado = scrapertools.find_single_match(data,'var sources = {(.*?)}, sel_source =')
    json_videos = jsontools.load_json('{'+listado+'}');
    lenguaje = scrapertools.find_single_match(data,'var labeli = {(.*?)};')	
    json_lang = jsontools.load_json('{'+lenguaje+'}');
    #calidad = scrapertools.find_single_match(data,'var label = {(.*?)}.*?var labeli')
    #json_qual = jsontools.load_json('{'+calidad+'}');
	
    for lang, cali in json_videos.items():
        for qual, links in cali.items():
            for link in links:
                vidId=link.split('_', 1 )
                #logger.info ('peliculasalacarta.channel.youpeliculas json= '+vidId[0].upper()+'['+json_lang[lang]+']['+qual+']')
                itemlist.append(Item(channel=item.channel, action='play', url=host+'/you/load-player', extra='type=movie&link='+vidId[1], title='Ver en '+vidId[0].upper()+' ['+json_lang[lang]+']['+qual+']', thumbnail=item.thumbnail))
    for videoitem in itemlist:
        videoitem.fulltitle = item.title
        videoitem.folder = False
        
    return itemlist

def play(item):
    logger.info()
    itemlist=[]

    player = httptools.downloadpage(item.url,item.extra).data
    video = scrapertools.find_single_match(player,'<iframe class="embed-responsive-item" src="([^"]+)"')
    #logger.info("video="+video)
    enlaces = servertools.findvideos(video)
    if enlaces:    	
    	thumbnail = servertools.guess_server_thumbnail(video)
    	# Añade al listado de XBMC
    	itemlist.append( Item(channel=item.channel, action="play", title=item.title , fulltitle=item.fulltitle, url=enlaces[0][1] , server=enlaces[0][2], thumbnail=thumbnail, folder=False) )
    
    return itemlist	