# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Canal (mundoflv) por Hernan_Ar_c
# ------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import tmdb
from core import scrapertools
from core.item import Item
from core import servertools
from core import httptools


host="http://mundoflv.com"
thumbmx ='http://flags.fmcdn.net/data/flags/normal/mx.png'
thumbes ='http://flags.fmcdn.net/data/flags/normal/es.png'
thumben ='http://flags.fmcdn.net/data/flags/normal/gb.png'
thumbsub ='https://s32.postimg.org/nzstk8z11/sub.png'
thumbtodos = 'https://s29.postimg.org/4p8j2pkdj/todos.png'
patrones=['<<meta property="og:image" content="([^"]+)" \/>" \/>','\/><\/a>([^*]+)<p><\/p>.*']

audio = {'la':'[COLOR limegreen]LATINO[/COLOR]','es':'[COLOR yellow]ESPAÑOL[/COLOR]','sub':'[COLOR orange]ORIGINAL SUBTITULADO[/COLOR]', 'en':'[COLOR red]Original[/COLOR]', 'vosi':'[COLOR red]ORIGINAL SUBTITULADO INGLES[/COLOR]'}

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'],
          ['Referer', host]]

def isGeneric():
    return True

def mainlist(item):
    logger.info()

    itemlist = []
    
    itemlist.append( Item(channel=item.channel, title="Series", action="todas", url=host, thumbnail='https://s32.postimg.org/544rx8n51/series.png', fanart='https://s32.postimg.org/544rx8n51/series.png'))
    
    itemlist.append( Item(channel=item.channel, title="Alfabetico", action="letras", url=host, thumbnail='https://s31.postimg.org/c3bm9cnl7/a_z.png', fanart='https://s31.postimg.org/c3bm9cnl7/a_z.png'))
    
    itemlist.append( Item(channel=item.channel, title="Mas vistas", action="masvistas", url=host, thumbnail='https://s32.postimg.org/466gt3ipx/vistas.png', fanart='https://s32.postimg.org/466gt3ipx/vistas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Recomendadas", action="recomendadas", url=host, thumbnail='https://s31.postimg.org/4bsjyc4iz/recomendadas.png', fanart='https://s31.postimg.org/4bsjyc4iz/recomendadas.png'))
    
    itemlist.append( Item(channel=item.channel, title="Ultimas Agregadas", action="ultimas", url=host, thumbnail='https://s31.postimg.org/3ua9kwg23/ultimas.png', fanart='https://s31.postimg.org/3ua9kwg23/ultimas.png'))

    itemlist.append( Item(channel=item.channel, title="Buscar", action="search", url='http://mundoflv.com/?s=', thumbnail='https://s31.postimg.org/qose4p13f/Buscar.png', fanart='https://s31.postimg.org/qose4p13f/Buscar.png'))

    return itemlist


def todas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    '''<a href="http://mundoflv.com/jessica-jones/" title="Jessica Jones (2015)">
<div class="img">
<img src="http://mundoflv.com/wp-content/uploads/2015/11/jessica-203x300.jpg" alt="Jessica Jones ()" />'''

    patron ='class="item"><a href="(.*?)" title="(.*?)(?:\|.*?|\(.*?|- )(\d{4})(?:\)|-)".*?'
    patron +='<div class="img">.*?'
    patron +='<img src="([^"]+)" alt.*?>'

    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle, scrapedyear, scrapedthumbnail in matches:
        url = scrapedurl
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        title = title.rstrip(' ')
        thumbnail = scrapedthumbnail
        year = scrapedyear
        plot = ''
        fanart = ''

        fanart = 'https://s32.postimg.org/h1ewz9hhx/mundoflv.png'
        itemlist.append( Item(channel=item.channel, action="idioma" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentSerieName=title, infoLabels={'year':year}))
        
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    itemlist = fail_tmdb(itemlist)
    #Paginacion
    patron  = '<link rel="next" href="([^"]+)" />'
    next_page_url = scrapertools.find_single_match(data,'<link rel="next" href="([^"]+)" />')
    
    if next_page_url!="":
        import inspect
        itemlist.append(Item(channel = item.channel, action = "todas", title = ">> Página siguiente", url = next_page_url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'))
    

    return itemlist


def letras(item):

    thumbletras = {'0-9':'https://s32.postimg.org/drojt686d/image.png','0 - 9':'https://s32.postimg.org/drojt686d/image.png','#':'https://s32.postimg.org/drojt686d/image.png','a':'https://s32.postimg.org/llp5ekfz9/image.png','b':'https://s32.postimg.org/y1qgm1yp1/image.png','c':'https://s32.postimg.org/vlon87gmd/image.png','d':'https://s32.postimg.org/3zlvnix9h/image.png','e':'https://s32.postimg.org/bgv32qmsl/image.png','f':'https://s32.postimg.org/y6u7vq605/image.png','g':'https://s32.postimg.org/9237ib6jp/image.png','h':'https://s32.postimg.org/812yt6pk5/image.png','i':'https://s32.postimg.org/6nbbxvqat/image.png','j':'https://s32.postimg.org/axpztgvdx/image.png','k':'https://s32.postimg.org/976yrzdut/image.png','l':'https://s32.postimg.org/fmal2e9yd/image.png','m':'https://s32.postimg.org/m19lz2go5/image.png','n':'https://s32.postimg.org/b2ycgvs2t/image.png','o':'https://s32.postimg.org/c6igsucpx/image.png','p':'https://s32.postimg.org/jnro82291/image.png','q':'https://s32.postimg.org/ve5lpfv1h/image.png','r':'https://s32.postimg.org/nmovqvqw5/image.png','s':'https://s32.postimg.org/zd2t89jol/image.png','t':'https://s32.postimg.org/wk9lo8jc5/image.png','u':'https://s32.postimg.org/w8s5bh2w5/image.png','v':'https://s32.postimg.org/e7dlrey91/image.png','w':'https://s32.postimg.org/fnp49k15x/image.png','x':'https://s32.postimg.org/dkep1w1d1/image.png','y':'https://s32.postimg.org/um7j3zg85/image.png','z':'https://s32.postimg.org/jb4vfm9d1/image.png'}

    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data

    patron = '<li><a.*?href="([^"]+)">([^<]+)<\/a><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle
        if scrapedtitle.lower() in thumbletras:
           thumbnail = thumbletras[scrapedtitle.lower()]
        else:
            thumbnail = ''
        plot = ""
        fanart = item.fanart
        itemlist.append( Item(channel=item.channel, action="todas" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart ,contentSerieName=title))

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

def masvistas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    patron = '<li><a href="(?!http:\/\/mundoflv\.com\/tag\/)(.*?)">.*?'
    patron +='div class="im">.*?'
    patron +='<img src=".*?" alt="(.*?)(?:\|.*?|\(.*?|- )(\d{4})|-" \/>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle, scrapedyear in matches:
        url = scrapedurl
        title = scrapedtitle
        fanart = item.fanart
        contentSerieName = scrapedtitle
        year = scrapedyear
        thumbnail = ''
        plot ='nada'
        itemlist.append( Item(channel=item.channel, action="idioma" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart, contentSerieName= contentSerieName, infoLabels ={'year':year}))

    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    itemlist = fail_tmdb(itemlist)
    return itemlist

def recomendadas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    realplot=''
    patron = '<li><A HREF="([^"]+)"><.*?>Ver ([^<]+)<\/A><\/li>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        data = httptools.downloadpage(scrapedurl).data
        thumbnail= scrapertools.get_match(data,'<meta property="og:image" content="([^"]+)" />')
        realplot = scrapertools.find_single_match(data, '\/><\/a>([^*]+)<p><\/p>.*')
        plot = scrapertools.remove_htmltags(realplot)
        title = scrapedtitle.replace('online','')
        title = title = scrapertools.decodeHtmlentities(title) 
        fanart = item.fanart
        itemlist.append( Item(channel=item.channel, action="idioma" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart,contentSerieName=title))

    return itemlist

def ultimas(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    realplot=''
    patron = '<li><A HREF="([^"]+)"> <.*?>Ver ([^<]+)<\/A><\/li>'
   
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        data = httptools.downloadpage(scrapedurl).data
        thumbnail= scrapertools.get_match(data,'<meta property="og:image" content="([^"]+)" />')
        realplot = scrapertools.find_single_match(data, '\/><\/a>([^*]+)<p><\/p>.*')
        plot = scrapertools.remove_htmltags(realplot)
        plot = ""
        title = scrapedtitle.replace('online','')
        title = scrapertools.decodeHtmlentities(title)
        fanart = item.fanart
        itemlist.append( Item(channel=item.channel, action="idioma" , title=title , url=url, thumbnail=thumbnail, plot=plot, fanart=fanart,contentSerieName=title))

    return itemlist

def temporadas(item):
    logger.info()
    
    itemlist = []
    templist = []
    data = httptools.downloadpage(item.url).data
    realplot = ''
    patron = "<button class='classnamer' onclick='javascript: mostrarcapitulos.*?blank'>([^<]+)</button>"
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    serieid = scrapertools.find_single_match(data,"<link rel='shortlink' href='http:\/\/mundoflv.com\/\?p=([^']+)' \/>")
    item.thumbnail = item.thumbvid
    infoLabels=item.infoLabels
    for scrapedtitle in matches:
        url = 'http://mundoflv.com/wp-content/themes/wpRafael/includes/capitulos.php?serie='+serieid+'&temporada=' + scrapedtitle
        title = 'Temporada '+ scrapertools.decodeHtmlentities(scrapedtitle)
        contentSeasonNumber = scrapedtitle
        thumbnail = item.thumbnail
        realplot = scrapertools.find_single_match(data, '\/><\/a>([^*]+)<p><\/p>.*')
        plot =''
        fanart = ''
        itemlist.append( Item(channel=item.channel, action="episodiosxtemp" , title=title , fulltitle=item.title, url=url, thumbnail=thumbnail, plot=plot, fanart = fanart, extra1=item.extra1, contentSerieName=item.contentSerieName, contentSeasonNumber = contentSeasonNumber, infoLabels = {'season':contentSeasonNumber}))
    
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)      
    if config.get_library_support() and len(itemlist) > 0:
        itemlist.append(Item(channel=item.channel, title='[COLOR yellow]Añadir esta serie a la biblioteca[/COLOR]', url=item.url,
                             action="add_serie_to_library", extra="episodios", contentSerieName=item.contentSerieName, extra1 = item.extra1))
    
    return itemlist

def episodios(item):
    logger.info()
    itemlist = []
    templist = temporadas(item)
    for tempitem in templist:
       itemlist += episodiosxtemp(tempitem)

    return itemlist

def episodiosxtemp(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    patron = "<button class='classnamer' onclick='javascript: mostrarenlaces\(([^\)]+)\).*?<"
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    for scrapedtitle in matches:
        item.url=item.url.replace("&sr","")
        item.url=item.url.replace("capitulos","enlaces")
        url = item.url+'&capitulo=' + scrapedtitle
        contentEpisodeNumber=scrapedtitle
        title=item.contentSerieName+' '+item.contentSeasonNumber+'x'+contentEpisodeNumber
        thumbnail = item.thumbnail
        plot = ''
        fanart=''
        idioma=''
        infoLabels = item.infoLabels
        infoLabels['episode']= contentEpisodeNumber
        itemlist.append( Item(channel=item.channel, action="findvideos", title=title, fulltitle=item.fulltitle, url=url, thumbnail=item.thumbnail, plot=plot, extra1=item.extra1,idioma='', contentSerieName = item.contentSerieName, contentSeasonNumber = item.contentSeasonNumber,infoLabels= infoLabels))

    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb=True)
    return itemlist
    
def idioma(item):
    logger.info()

    itemlist = []
    thumbvid =item.thumbnail
    itemlist.append( Item(channel=item.channel, title="Latino", action="temporadas", url=item.url, thumbnail=thumbmx, fanart='', extra1 = 'la', fulltitle = item.title, thumbvid = thumbvid, contentSerieName=item.contentSerieName, infoLabels=item.infoLabels))
    
    itemlist.append( Item(channel=item.channel, title="Español", action="temporadas", url=item.url, thumbnail=thumbes, fanart='', extra1 = 'es', fulltitle = item.title, thumbvid = thumbvid, contentSerieName=item.contentSerieName))
    
    itemlist.append( Item(channel=item.channel, title="Subtitulado", action="temporadas", url=item.url, thumbnail=thumbsub, fanart='', extra1 = 'sub', fulltitle = item.title, thumbvid = thumbvid, contentSerieName=item.contentSerieName))
    
    itemlist.append( Item(channel=item.channel, title="Original", action="temporadas", url=item.url, thumbnail=thumben, fanart='', extra1 = 'en', fulltitle = item.title, thumbvid = thumbvid, contentSerieName=item.contentSerieName))

    itemlist.append( Item(channel=item.channel, title="Original Subtitulado en Ingles", action="temporadas", url=item.url, thumbnail=thumben, fanart='', extra1 = 'vosi', fulltitle = item.title, thumbvid = thumbvid, contentSerieName=item.contentSerieName))

    itemlist.append( Item(channel=item.channel, title="Todo", action="temporadas", url=item.url, thumbnail=thumbtodos, fanart='', extra1 = 'all', fulltitle = item.title, thumbvid = thumbvid, contentSerieName=item.contentSerieName))


    
    return itemlist 


def busqueda(item):
    logger.info()
    itemlist = []
    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    patron = '<img class=.*?src="([^"]+)" alt="(.*?)(?:\|.*?|\(.*?|")>.*?h3><a href="(.*?)".*?class="year">(.*?)<\/span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    for scrapedthumbnail, scrapedtitle, scrapedurl, scrapedyear in matches:
        url = scrapedurl
        title = scrapertools.decodeHtmlentities(scrapedtitle)
        thumbnail = scrapedthumbnail
        plot = ''
        year = scrapedyear
        itemlist.append( Item(channel=item.channel, action="idioma" , title=title , fulltitle=title, url=url, thumbnail=thumbnail, plot=plot, contentSerieName=title, infoLabels={'year':year}))
    tmdb.set_infoLabels_itemlist(itemlist, seekTmdb = True)
    itemlist = fail_tmdb(itemlist)

   #Paginacion
    patron  = "<a rel='nofollow' class=previouspostslink' href='([^']+)'>Siguiente &rsaquo;</a>"
    next_page_url = scrapertools.find_single_match(data,"<a rel='nofollow' class=previouspostslink' href='([^']+)'>Siguiente &rsaquo;</a>")
    if next_page_url!="":
        item.url=next_page_url
        import inspect
        itemlist.append(Item(channel = item.channel,action = "busqueda",title = ">> Página siguiente", url = next_page_url, thumbnail='https://s32.postimg.org/4zppxf5j9/siguiente.png'))   
    return itemlist

def search(item,texto):
    logger.info()
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    if texto!='':
       return busqueda(item)


def findvideos(item):
    logger.info()
    itemlist = []

    data = httptools.downloadpage(item.url).data
    patron ='href="([^"]+)".*?domain=.*?>([^<]+).*?gold">([^<]+)<'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl, scrapedserver, scrapedidioma in matches:
    	url = scrapedurl
        idioma = audio[scrapedidioma]
        title = item.contentSerieName+' '+str(item.contentSeasonNumber)+'x'+str(item.contentEpisodeNumber)+' '+idioma+' ('+scrapedserver.strip(' ')+')'
        if scrapedidioma == item.extra1 or item.extra1 == 'all':
           itemlist.append(item.clone(title=title, url=url, action="play", language=idioma,
                                      server = scrapedserver.strip(), fulltitle = item.ContentSeriename))
    
    for videoitem in itemlist:
        videoitem.infoLabels = item.infoLabels
        videoitem.thumbnail = servertools.guess_server_thumbnail(videoitem.server)
        

               
        

    return itemlist


def play(item):
    logger.info('mundoflv.py play')

    special_servers = ['streamplay', 'streame', 'idowatch']

    data = httptools.downloadpage(item.url).data

    if item.server not in special_servers:
       url = scrapertools.find_single_match(data, '<(?:IFRAME|iframe).*?(?:SRC|src)=*([^ ]+) (?!style|STYLE)')
    else:
       url = scrapertools.find_single_match(data, '<meta http-equiv="refresh" content="0; url=([^"]+)">')

    itemlist = servertools.find_video_items(data=url)
    for videoitem in itemlist:
        videoitem.infoLabels = item.infoLabels
        videoitem.title = item.title
        videoitem.thumbnail = videoitem.infoLabels['thumbnail']

    return itemlist  

