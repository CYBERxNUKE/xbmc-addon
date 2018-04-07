# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tremendaseries
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------
import re
import sys


from core import logger
from core import config
from core import scrapertools
from core import channeltools
from core import tmdb
from core.item import Item
from core import servertools

__channel__ = "tremendaseries"

# Configuracion del canal
try:
    __modo_grafico__ = config.get_setting('modo_grafico',__channel__)
    __perfil__= int(config.get_setting('perfil',__channel__))
except:
    __modo_grafico__ = True 
    __perfil__= 1

host ="http://tremendaseries.com/"

# Fijar perfil de color            
perfil = [['0xFFFFE6CC','0xFF994D00','0xFFFFCE9C'],
          ['0xFFBDBDBD','0xFF01DFD7','0xFF848484'],
          ['0xFFF5BCA9','0xFF61210B','0xFFFE642E']]     
color1, color2, color3 = perfil[__perfil__]

parameters= channeltools.get_channel_parameters(__channel__)
fanart= parameters['fanart']
thumbnail_host= parameters['thumbnail']


def mainlist(item):
    logger.info("pelisalacarta.channels.tremendaseries mainlist")
    
    itemlist = []
    itemlist.append(Item(channel=__channel__, action="listadoSeries", title="Novedades", extra= '0',
                         text_color= color2, fanart= fanart, url= "http://tremendaseries.com/series/pagina-1",
                         thumbnail = "https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/TV%20Series.png"))
    itemlist.append(Item(channel=__channel__, action="search", title="Buscar...", text_color= color3, fanart= fanart, thumbnail = "https://raw.githubusercontent.com/master-1970/resources/master/images/genres/0/Search.png"))
   
    return itemlist
   
   
def search(item, texto):
    logger.info("pelisalacarta.channels.tremendaseries search")

    item.url = "http://tremendaseries.com/resultados/"
    texto = texto.replace(" ", "-")
    item.url = item.url+texto
    item.extra= '0'
    try:
        return listadoSeries(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%{0}".format(line))
        return []   
   

def listadoSeries(item):
    logger.info("pelisalacarta.channels.tremendaseries listadoSeries")
    itemlist = []
    if __modo_grafico__:
      nItemxPage = 28 
    else:
      nItemxPage = 100 # o los que haya en la pagina
    
    data0 = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    patron = '<div class="nuevos_caps"(.*?)</div></div>'
    data = scrapertools.find_single_match(data0,patron)   

    patron  = '<div class="portadas_home">.*?href="([^"]+).*?' #url
    patron += 'title="([^"]+).*?' #titulo 
    patron += 'src=series([^&]+).*?' #thumbnail 
    matches = scrapertools.find_multiple_matches(data,patron)
    
    item_inicial= int(item.extra)
    items_total = len(matches)
    if (item_inicial + nItemxPage) < items_total:
      item_final = item_inicial + nItemxPage  
    else:
      item_final = items_total
    matches = matches[item_inicial:item_final]
    #logger.debug(" %i - %i - %i" %(item_inicial, item_final, items_total))

    for scrapedurl,scrapedtitle,scrapedthumbnail in matches:
        thumbnail = 'http://tremendaseries.com/screen' + scrapedthumbnail
        newItem = Item(channel=__channel__,action="listadoTemporadas", title=scrapedtitle.strip(),url=scrapedurl, thumbnail=thumbnail,
                      text_color= color1, folder=True, fanart=fanart, show= scrapedtitle)
        itemlist.append (newItem)
    logger.debug(str(len(itemlist)))
    # Obtenemos los datos basicos de todas las series mediante multihilos
    tmdb.set_infoLabels(itemlist, __modo_grafico__)
 
    if itemlist:
        #Paginacion solo cuando hay resultados:
        #   Se pagina en subpaginas cuando el resultado es mayor q nItemxPage
        #   Se pagina normal cuando ya no hay mas resultados por mostrar en la url
        if item_final < items_total:
            # Siguiente sub pagina
            itemlist.append(Item(channel=__channel__, action="listadoSeries", title=">> Página siguiente", url=item.url,
                                 text_color= color2, fanart=fanart, thumbnail= thumbnail_host, extra= str(nItemxPage)))
        else:
            # Siguiente pagina en web
            patron = '<span class="current">.*?<a href="([^"]+)'
            url = scrapertools.find_single_match(data0,patron)
            if url:
                itemlist.append(Item(channel=__channel__, action="listadoSeries", title=">> Página siguiente", url=url,
                                 text_color= color2, fanart=fanart, thumbnail= thumbnail_host, extra= '0'))
    
    return itemlist

def listadoTemporadas(item):
    logger.info("pelisalacarta.channels.tremendaseries listadoTemporadas")
    itemlist = []
    
    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    patron = '<div class="tit_enlaces"><ul>(.*?)<div class="addthis_sharing_toolbox"'
    data = scrapertools.find_single_match(data,patron)
    #logger.debug(data)
    patron  = '<a href="javascript:void\(\);">([^<]+)<br>'
    matches = scrapertools.find_multiple_matches(data,patron)

    for scrapedtitle in matches:
        temporada = scrapertools.find_single_match(scrapedtitle, '(\d+)')
        newItem= item.clone(title= scrapedtitle, text_color= color1, action="listadoCapitulos", extra=temporada)
        newItem.infoLabels['season'] = temporada
        itemlist.append(newItem)
        
    # Obtenemos los datos de todas las temporadas de la serie mediante multihilos
    tmdb.set_infoLabels(itemlist, __modo_grafico__)
    for i in itemlist:
        i.title = "%s. %s" %(i.infoLabels['season'],i.infoLabels['tvshowtitle'])
        if i.infoLabels['title']: 
            # Si la temporada tiene nombre propio añadirselo al titulo del item
            i.title += " - %s" %(i.infoLabels['title'])
        if i.infoLabels.has_key('poster_path'):
            # Si la temporada tiene poster propio remplazar al de la serie
            i.thumbnail = i.infoLabels['poster_path']
    
    '''
    if config.get_library_support():
        logger.debug(item.url)
        itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca", 
                              url=item.url, action="add_serie_to_library", extra="episodios###serie_add", 
                              show= item.show, thumbnail = thumbnail_host, fanart= fanart, text_color= color3))'''
    
    return itemlist
     
    
def listadoCapitulos(item):
    logger.info("pelisalacarta.channels.tremendaseries capitulos")
    itemlist = []
    conEnlaces= False
    
    data = re.sub(r"\n|\r|\t|\s{2}|(<!--.*?-->)","",scrapertools.cache_page(item.url))
    patron = '<div class="tit_enlaces"><ul>(.*?)<div class="addthis_sharing_toolbox"'
    
    data = scrapertools.find_single_match(data,patron)
    patron  = '<a href="([^"]+).*?' #url
    patron += '<div class="enlaces" style="([^"]+).*?' #enlaces? if background-color in style: no hay enlaces
    patron += '<span class="icon-forward3">.*?</span>([^<]+).*?' #TemporadaxEpisodio
    patron += '<div class="text_en_boton" [^>]+>(.*?)</div><div class="text_en_boton2"' #title
    
    matches = scrapertools.find_multiple_matches(data,patron)
    for scrapedurl, scrapedtenlaces, scrapedcapitulo, scrapedtitle in matches:
        temporada, episodio = scrapedcapitulo.split('x')
        if item.extra !="serie_add" and temporada != item.infoLabels['season']: # solo nos interesan los enlaces de esta temporada
            continue
            
        if '</span>' in scrapedtitle:
                data = '<' + scrapertools.find_single_match(scrapedtitle,'<([^>]+)') + '>'
                scrapedtitle = scrapedtitle.replace(data,'')
                scrapedtitle = scrapedtitle.replace('</span>','')

        scrapedtitle = re.sub(r'(S\d*E\d*)', scrapedcapitulo, scrapedtitle, re.I) #Sustituir S01E01 por 1x01
        newItem= item.clone(title= scrapedtitle, url= scrapedurl, text_color= color1, action="findvideos")
        newItem.infoLabels['season'] = temporada
        newItem.infoLabels['episode'] = episodio
        
        if not 'background-color' in scrapedtenlaces:
            conEnlaces = True
        elif item.extra !="serie_add": 
            # No hay enlaces para este capitulos. Añadirlo como una etiqueta (TAG) ...
            # ...excepto si estamos añadiendolo a la biblioteca.
            newItem.action = ''
            newItem.text_color = color3
            newItem.thumbnail = thumbnail_host            
        
        itemlist.append(newItem)   
    
    if item.extra !="serie_add": 
        # Obtenemos los datos de todos los capitulos de la temporada mediante multihilos
        tmdb.set_infoLabels(itemlist, __modo_grafico__)
        for i in itemlist:
            if i.infoLabels['title']: 
                # Si el capitulo tiene nombre propio añadirselo al titulo del item
                i.title = "%sx%s %s" %(i.infoLabels['season'],i.infoLabels['episode'],i.infoLabels['title'])
            if i.infoLabels.has_key('poster_path'):
                # Si el capitulo tiene imagen propia remplazar al poster
                i.thumbnail = i.infoLabels['poster_path']
        
        '''
        if config.get_library_support() and conEnlaces:
            itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca", 
                                  url=item.url, action="add_serie_to_library", extra="episodios###serie_add", 
                                  show= item.show, thumbnail = thumbnail_host, fanart= fanart, text_color= color3))'''
    
    return itemlist

    
def findvideos(item):
    logger.info("pelisalacarta.channels.tremendaseries findvideos")
    itemlist = []
    list =[]
    
    def finvideos_by_Category(item, data_0):
        list_0 =[]
        patron_0  = '<a target="_blank" rel="nofollow" href="([^"]+).*?' #url
        patron_0 += '<span id="serv1" title="([^"]+).*?' #titulo
        patron_0 += 'class=[^>]+>([^<]+).*?' #servidor
        patron_0 += '<span id="idioma[^>]+>([^<]+).*?' #idioma
        patron_0 += '<span id="cal[^>]+>([^<]+)' #calidad
        matches2 = re.compile(patron_0, re.DOTALL).findall(data_0)
        
        for url, titulo, servidor, idioma, calidad in matches2:
            servidor = servidor.replace('www.','')
            if '.' in servidor:
              servidor =  servidor.split('.')[0]
            titulo += ' (' + idioma + ') [' + calidad + ']'
            
            newItem = item.clone(action="play", title=titulo, url=url, folder=True, text_color= color1, server= servidor)
            list_0.append(newItem)
        return list_0
              
              
    data = scrapertools.cache_page(item.url)
    patron = '>Enlaces para ver online(.*?)<div class="tit_enlaces">'
    list = finvideos_by_Category(item,scrapertools.find_single_match(data,patron))
    if len(list) > 0:
        list.insert(0,Item(channel=__channel__, title="Ver online", text_color= color2, fanart= fanart, folder= False
                                ,thumbnail= thumbnail_host, text_blod=True))           
        itemlist.extend(list)
    
    patron = '>Enlaces para descargar(.*?)<div class="addthis_sharing_toolbox"'
    list = finvideos_by_Category(item,scrapertools.find_single_match(data,patron))
    if len(list) > 0:
        list.insert(0,Item(channel=__channel__, title="Descargar", text_color= color2, fanart= fanart, folder= False
                                ,thumbnail= thumbnail_host, text_blod=True))
        itemlist.extend(list)
    
    return itemlist
 
 
def play(item):
    logger.info("pelisalacarta.channels.tremendaseries play")
    print item.url
    
    data= scrapertools.cache_page(item.url)
    url_base = 'http://tremendaseries.com/saliendo'
    patron = url_base + '(.*?)">'
    data2 = url_base + scrapertools.find_single_match(data,patron)
    data2 = scrapertools.getLocationHeaderFromResponse(data2)
    logger.info("pelisalacarta.channels.tremendaseries data2="+data2)

    itemlist = servertools.find_video_items(data=data2)
    
    return itemlist    
   
'''   
def episodios(item):
    # Necesario para las actualizaciones automaticas
    newItem = Item(channel=__channel__,url=item.url, show=item.show, extra= "serie_add")
    newItem.infoLabels['season'] = 'all'
    return listadoCapitulos(newItem)'''
    

    

   
            
    
    
    
    
