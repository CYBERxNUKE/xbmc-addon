# -*- coding: utf-8 -*-
######################
#WAPITO WAPITORES
#####################



import os
import sys
import urllib
import urllib2
import shutil
import base64

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.wachtv/art', ''))
MEN = "http://www.financiate.com.ar/img/iconoLlaveAuto.png"
tv = "http://www.iconsdb.com/icons/preview/gray/tv-xxl.png"
can = "https://marketingventasparatodos.files.wordpress.com/2012/10/dinero-candado-seguridad.jpg"
estati = "http://wachtvworld.org/gallery_gen/0bf9f907238217b60f337d5d4695f7f9.jpg"
referer = 'http://www.seriesflv.com/'
thumbnail = 'http://aldocarranza.hol.es/wp-content/uploads/2014/07/iTunes-icon-150x150.png'
lista = 'http://icon-icons.com/icons2/159/PNG/256/list_tasks_22372.png'
music = "https://cdn3.iconfinder.com/data/icons/66-cds-dvds/512/Icon_60-512.png"
pel = "http://icon-icons.com/icons2/37/PNG/512/count_theapplication_themovie_3042.png"
nopor = "http://www.jshotels.com/sites/default/files/js-hotels-only-adults-18.png"
eve = "http://jvinsidercircle.com/members/images/calendar.png"
THUMBNAIL = "thumbnail"
TV_SHOWS = "tvshows"
wachusername = plugintools.get_setting("wachusername")
wachpass = plugintools.get_setting("wachpass")
morros = plugintools.get_setting("morros")
url = "http://192.99.63.186:8000/enigma2.php?username=" + wachusername + "&password=" + wachpass + "&type=get_live_categories"

def run():
    plugintools.log("wachtv.run")
    params = plugintools.get_params()
    if params.get("action") is None:
        xtv(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    plugintools.close_item_list()
	
	
def xtv(params):
  xtvmaster = plugintools.get_setting("xtvmaster")
  

  if xtvmaster == 'false':
   plugintools.message("WACHTV","ACCEDE PRIMERO AL PORTAL")
   plugintools.open_settings_dialog()
  else:
        data = plugintools.read(url + "0")
        if "<items>" in data:
           main_list(params)
        elif "" in data:
           xbmc.executebuiltin("Notification(%s,%s,%s,%s)" % ('WACHTV', "USUARIO O CONTRASEÑA INCORRECTA......", 10 , art+'b.png')) 
           plugintools.open_settings_dialog()

def main_list(params):
    plugintools.log("wachtv.main_list "+repr(params))
    plugintools.set_view(THUMBNAIL)
    plugintools.add_item( 
        action = "cuenta", 
        title = "MI CUENTA",
        thumbnail = MEN,
        fanart = can,
        folder = False )
    plugintools.add_item( 
        action = "perro2", 
        title = "TV ONLINE",
        thumbnail = tv,
        fanart = estati,
        url = url,
        folder = True )
    plugintools.add_item( 
        action = "perro", 
        title = "PELICULAS",
        thumbnail = pel,
        fanart = estati,
        url = "http://192.99.63.186:8000/enigma2.php?username=" + wachusername + "&password=" + wachpass + "&type=get_vod_streams&cat_id=0",
        folder = True )
    plugintools.add_item( 
        action = "parse2", 
        title = "MUSICA",
        thumbnail = music,
        fanart = estati,
        folder = True )
    plugintools.add_item( 
        action = "perro", 
        title = "ZONA DE EVENTOS",
        thumbnail = eve,
        fanart = estati,
        url = "http://192.99.63.186:8000/enigma2.php?username=" + wachusername + "&password=" + wachpass + "&type=get_vod_streams&cat_id=14",
        folder = True )
    if morros == "true" :
	plugintools.add_item( 
        action = "perro", 
        title = "SOLO ADULTOS ",
        url = "http://192.99.63.186:8000/enigma2.php?username=" + wachusername + "&password=" + wachpass + "&type=get_live_streams&cat_id=" + "13",
        thumbnail = nopor,
        fanart = estati,
        folder = True )
    

	

		
def parse2(params):
    plugintools.log("parse "+repr(params))
    plugintools.set_view(THUMBNAIL)
    plugintools.add_item( 
        action = "perro", 
        title = "MUSICA VIDEOS",
        url = url + "19",
        thumbnail = music,
        folder = True )
    plugintools.add_item(
        action = "search5",
        title = "MUSICA AL GUSTO",
        thumbnail = music,
        folder = True )
		
	
		
def perro(params):
    plugintools.set_view(TV_SHOWS)
    url = params.get("url")
    data = plugintools.read(url)
    
    SongLists = plugintools.find_multiple_matches(data, '<channel>(.*?)</channel>')
    for entry in SongLists:
            ima = plugintools.find_single_match(entry, '<desc_image>([^"]+)</desc_image>')
            ima = ima.replace("<![CDATA[", "")
            ima = ima.replace("]]>", "")
            titulo = plugintools.find_single_match(entry, '<title>([^"]+)</title>')
            titulo = base64.b64decode(titulo)
            titulo = titulo.upper()
            titulo = titulo.replace("PARENT-CODE=\"6666\",","")
            description = plugintools.find_single_match(entry, '<description>([^"]+)</description>')
            description = base64.b64decode(description)
            playstation = plugintools.find_single_match(entry, '<stream_url>([^"]+)</stream_url>')
            playstation = playstation.replace("<![CDATA[", "")
            playstation = playstation.replace("]]>", "")
            playstation = playstation.replace(".ts", ".m3u8")
            plugintools.add_item(action="play", title = titulo , plot = description , url = playstation , thumbnail = ima , fanart = ima , info_labels = None , folder = False, isPlayable = True)



def perro2(params):
    plugintools.set_view(THUMBNAIL)
    url = params.get("url")
    data = plugintools.read(url)
    
    SongLists = plugintools.find_multiple_matches(data, '<channel>(.*?)</channel>')
    for entry in SongLists:
     ima = plugintools.find_single_match(entry, '<desc_image>([^"]+)</desc_image>')
     ima = ima.replace("<![CDATA[", "")
     ima = ima.replace("]]>", "")
     playstation = plugintools.find_single_match(entry, '<playlist_url>([^"]+)</playlist_url>')
     playstation = playstation.replace("<![CDATA[", "")
     playstation = playstation.replace("]]>", "")
     titulo = plugintools.find_single_match(entry, '<title>([^"]+)</title>')
     titulo = base64.b64decode(titulo)
     titulo = titulo.upper()
     if titulo.find("LATINOS") >= 0:
        plugintools.add_item(action="perro", title = titulo , url = playstation , thumbnail = tv , fanart = estati  , folder = True)
     if titulo.find("DEPORTES") >= 0:
	    plugintools.add_item(action="perro", title = titulo , url = playstation , thumbnail = tv , fanart = estati  , folder = True)		
     if titulo.find("AMERICANOS") >= 0:		
        plugintools.add_item(action="perro", title = titulo , url = playstation , thumbnail = tv , fanart = estati  , folder = True)	
     if titulo.find("INTERNACIONALES") >= 0:
        plugintools.add_item(action="perro", title = titulo , url = playstation , thumbnail = tv , fanart = estati , folder = True)		 
     if titulo.find("ALL") >= 0:
        plugintools.add_item(action="perro", title = titulo , url = playstation , thumbnail = tv , fanart = estati  , folder = True)		 	 
	 
def cuenta(params):
    url_getlink = 'http://192.99.63.186:8000/panel_api.php?username=' + wachusername + "&password=" + wachpass
    request_headers=[]
    request_headers.append(["User-Agent","Kodi plugin by MikkM"])
    body,response_headers = plugintools.read_body_and_headers(url_getlink, headers=request_headers)
    datos = plugintools.find_multiple_matches(body, '"user_info":(.*?)"server_info"')
    for entry in datos:
     ima = plugintools.find_single_match(entry, '"username":"([^"]+)"')
     ma = plugintools.find_single_match(entry, '"password":"([^"]+)"')
     esta = plugintools.find_single_match(entry, '"status":"([^"]+)"')
     ven = plugintools.find_single_match(entry, '"exp_date":"([^"]+)"')
     dialog = xbmcgui.Dialog()
     selector = dialog.select('WACHTV', ['# VER USERNAME Y PASSWORD' , '# VERIFICAR STATUS Y FECHA DE VENCIMIENTO' ])
    if selector == 0:
        plugintools.message("WACHTV INFORMA" , "USERNAME:" + ima , "PASSWORD:" + ma  )
    if selector == 1:
        plugintools.message("WACHTV INFORMA" , "STATUS:" + esta , "FECHA DE VENCIMIENTO:" + ven )

	
def play2(params):
    plugintools.set_view(THUMBNAIL)
    url = params.get("url")
    plugintools.play_resolved_url(url)


def play(params):
    plugintools.set_view(TV_SHOWS)
    url = params.get("url")
    plugintools.play_resolved_url(url)
	
def search5(params):
    dialog = xbmcgui.Dialog()
    selector = dialog.select('WACHTV', ['BUSQUEDA POR CANCION', 'BUSQUEDA POR ARTISTA'])
    if selector == 0:
        texto = plugintools.keyboard_input()
        plugintools.set_setting("last_search",texto)
        busqueda = 'http://www.goear.com/apps/android/search_songs_json.php?q='+ texto
        busqueda  = busqueda.replace(' ', "+")
        data = gethttp_referer_headers(busqueda,referer)
        if "id" in data:
           plugintools.log("busqueda= "+busqueda)
           songs = plugintools.find_multiple_matches(data, '{(.*?)}')
           for entry in songs:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()
            plugintools.log("title_song= "+title_song)
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.log("songtime= "+songtime)
            url='http://www.goear.com/action/sound/get/'+id_song
            plugintools.log("url= "+url)
            plugintools.add_item(action="play2", title = title_song + " " +'[COLOR orange] ('+songtime+')[/COLOR]', url=url, thumbnail = thumbnail , fanart = "" , folder = False, isPlayable = True)
        elif "0" in data:
             errormsg = plugintools.message("WACHTV","SIN RESULTADOS")
             search5(params)
    if selector == 1:
        texto = plugintools.keyboard_input()
        plugintools.set_setting("last_search",texto)
        url = 'http://www.goear.com/apps/android/search_playlist_json.php?q='+texto
        plugintools.log("url= "+url)
        url2  = url.replace(' ', "+")
        data = gethttp_referer_headers(url2,referer)
        if "id" in data:
           songs = plugintools.find_multiple_matches(data, '{(.*?)}')
           i = 1
           for entry in songs:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            url = 'http://www.goear.com/apps/android/playlist_songs_json.php?v='+id_song 
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()			
            plugintools.log("title_song= "+title_song)
            plsongs = plugintools.find_single_match(entry, '"plsongs":"([^"]+)"')
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.add_item(action="songs2", title = title_song + " " + '[COLOR red]('+ plsongs +')[/COLOR]' + 'ITEMS' + '[COLOR orange] ('+songtime+')[/COLOR]' +  'DURACION'  , url = url , thumbnail = lista , fanart = ""  , folder = True, isPlayable = False)
            i = i + 1			
        elif "0" in data:
             errormsg = plugintools.message("WACHTV","SIN RESULTADOS")
             search5(params)		
           

		   
		   
def songs2(params):
        url = params.get("url")
        data = gethttp_referer_headers(url,referer)
        songs2 = plugintools.find_multiple_matches(data, '{(.*?)}')
        i = 1
        for entry in songs2:
            plugintools.log("entry= "+entry)
            id_song = plugintools.find_single_match(entry, '"id":"([^"]+)')
            plugintools.log("id_song= "+id_song)
            title_song = plugintools.find_single_match(entry, '"title":"([^"]+)')
            title_song = title_song.upper()
            plugintools.log("title_song= "+title_song)
            songtime = plugintools.find_single_match(entry, '"songtime":"([^"]+)')
            plugintools.log("songtime= "+songtime)
            url='http://www.goear.com/action/sound/get/'+id_song
            plugintools.log("url= "+url)
            plugintools.add_item(action="play2", title = title_song + " " +'[COLOR orange] ('+songtime+')[/COLOR]', url=url, thumbnail = thumbnail , fanart = "" , folder = False, isPlayable = True)
            i = i + 1








def gethttp_referer_headers(url,referer):    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body

		
		
run()