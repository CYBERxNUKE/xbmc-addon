# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------
# Gestor de descargas
# ------------------------------------------------------------
import os
import sys
import re
from core import config
from core.downloader import Downloader
from core import scrapertools
from core import logger
from core import servertools
from core import filetools
from platformcode import platformtools
from core.item import Item
import time
from core import scraper

STATUS_COLORS = {0: "orange", 1: "orange", 2: "green", 3: "red"}
STATUS_CODES = type("StatusCode",(), {"stoped" : 0, "canceled" : 1 , "completed" : 2, "error" : 3})
DOWNLOAD_LIST_PATH = config.get_setting("downloadlistpath")
DOWNLOAD_PATH = config.get_setting("downloadpath")
STATS_FILE = os.path.join(config.get_data_path(), "servers.json")
TITLE_FILE = "[COLOR %s][%i%%][/COLOR] %s"
TITLE_TVSHOW = "[COLOR %s][%i%%][/COLOR] %s [%s]"


def mainlist(item):
    logger.info()
    itemlist = []
    
    #Lista de archivos
    for file in sorted(filetools.listdir(DOWNLOAD_LIST_PATH)):
        #Saltamos todos los que no sean JSON
        if not file.endswith(".json"): continue
        
        #cargamos el item
        file = os.path.join(DOWNLOAD_LIST_PATH, file)
        i = Item(path = file).fromjson(filetools.read(file))
        i.thumbnail = i.contentThumbnail

        #Listado principal
        if not item.contentType == "tvshow":
          # Series
          if i.contentType == "episode":
              #Comprobamos que la serie no este ya en el itemlist
              if not filter(lambda x: x.contentSerieName == i.contentSerieName and x.contentChannel == i.contentChannel, itemlist):
              
                title = TITLE_TVSHOW % (STATUS_COLORS[i.downloadStatus], i.downloadProgress, i.contentSerieName, i.contentChannel)
                
                itemlist.append(Item(title = title, channel= "descargas", action= "mainlist", contentType = "tvshow", 
                                     contentSerieName = i.contentSerieName, contentChannel = i.contentChannel, 
                                     downloadStatus = i.downloadStatus, downloadProgress = [i.downloadProgress],
                                     fanart = i.fanart, thumbnail = i.thumbnail)) 
              
              else:
                s = filter(lambda x: x.contentSerieName == i.contentSerieName and x.contentChannel == i.contentChannel, itemlist)[0]
                s.downloadProgress.append(i.downloadProgress)
                downloadProgress = sum(s.downloadProgress) / len(s.downloadProgress)
                
                if not s.downloadStatus in [STATUS_CODES.error, STATUS_CODES.canceled] and not i.downloadStatus in [STATUS_CODES.completed, STATUS_CODES.stoped]:
                    s.downloadStatus = i.downloadStatus
                      
                s.title = TITLE_TVSHOW % (STATUS_COLORS[s.downloadStatus], downloadProgress, i.contentSerieName, i.contentChannel)

          # Peliculas
          elif i.contentType == "movie" or i.contentType == "video":
              i.title = TITLE_FILE % (STATUS_COLORS[i.downloadStatus], i.downloadProgress, i.contentTitle)
              itemlist.append(i)
        
        #Listado dentro de una serie      
        else:
            if i.contentType == "episode" and i.contentSerieName == item.contentSerieName and i.contentChannel == item.contentChannel:
            
                  i.title = TITLE_FILE % (STATUS_COLORS[i.downloadStatus], i.downloadProgress, 
                                          "%dx%0.2d: %s" % (i.contentSeason, i.contentEpisodeNumber,i.contentTitle))
                  itemlist.append(i)  

                    
    estados = [i.downloadStatus for i in itemlist]
    

    # Si hay alguno completado
    if 2 in estados:
        itemlist.insert(0, Item(channel=item.channel, action="clean_ready", title="Eliminar descargas completadas",
                                contentType = item.contentType, contentChannel=item.contentChannel, contentSerieName = item.contentSerieName))

    # Si hay alguno con error
    if 3 in estados:
        itemlist.insert(0, Item(channel=item.channel, action="restart_error", title="Reiniciar descargas con error",
                                contentType = item.contentType, contentChannel=item.contentChannel, contentSerieName = item.contentSerieName))

    # Si hay alguno pendiente
    if 1 in estados or 0 in estados:
        itemlist.insert(0, Item(channel=item.channel, action="download_all", title="Descargar todo",
                                contentType = item.contentType, contentChannel=item.contentChannel, contentSerieName = item.contentSerieName))

    if len(itemlist):
        itemlist.insert(0, Item(channel=item.channel, action="clean_all", title="Eliminar todo",
                                contentType = item.contentType, contentChannel=item.contentChannel, contentSerieName = item.contentSerieName))

    if not item.contentType == "tvshow" and config.get_setting("browser", "descargas") == True:
        itemlist.insert(0, Item(channel=item.channel, action="browser", title="Ver archivos descargados", url = DOWNLOAD_PATH))
    
    return itemlist


def browser(item):
    logger.info()
    itemlist = []
    
    for file in filetools.listdir(item.url):
      if filetools.isdir(filetools.join(item.url, file)) and not file == "list":
        itemlist.append(Item(channel=item.channel, title=file, action=item.action, url= filetools.join(item.url, file)))
      else:
        itemlist.append(Item(channel=item.channel, title=file, action="play", url= filetools.join(item.url, file)))
    
    return itemlist


def clean_all(item):
    logger.info()
    
    for fichero in sorted(filetools.listdir(DOWNLOAD_LIST_PATH)):
        if fichero.endswith(".json"):
          download_item = Item().fromjson(filetools.read(os.path.join(DOWNLOAD_LIST_PATH, fichero)))
          if not item.contentType == "tvshow" or (item.contentSerieName == download_item.contentSerieName and item.contentChannel == download_item.contentChannel):
              filetools.remove(os.path.join(DOWNLOAD_LIST_PATH, fichero))

    platformtools.itemlist_refresh()


def clean_ready(item):
    logger.info()
    for fichero in sorted(filetools.listdir(DOWNLOAD_LIST_PATH)):
        if fichero.endswith(".json"):
            download_item = Item().fromjson(filetools.read(os.path.join(DOWNLOAD_LIST_PATH, fichero)))
            if not item.contentType == "tvshow" or (item.contentSerieName == download_item.contentSerieName and item.contentChannel == download_item.contentChannel):
              if download_item.downloadStatus == STATUS_CODES.completed:
                  filetools.remove(os.path.join(DOWNLOAD_LIST_PATH, fichero))

    platformtools.itemlist_refresh()


def restart_error(item):
    logger.info()
    for fichero in sorted(filetools.listdir(DOWNLOAD_LIST_PATH)):
        if fichero.endswith(".json"):
            download_item = Item().fromjson(filetools.read(os.path.join(DOWNLOAD_LIST_PATH, fichero)))
            
            if not item.contentType == "tvshow" or (item.contentSerieName == download_item.contentSerieName and item.contentChannel == download_item.contentChannel):
              if download_item.downloadStatus == STATUS_CODES.error:
                  if filetools.isfile(os.path.join(config.get_setting("downloadpath"), download_item.downloadFilename)):
                      filetools.remove(os.path.join(config.get_setting("downloadpath"), download_item.downloadFilename))
                      
                  update_json(item.path, {"downloadStatus" : STATUS_CODES.stoped, "downloadComplete" :  0 , "downloadProgress" : 0})


    platformtools.itemlist_refresh()


def download_all(item):
    time.sleep(0.5)
    for fichero in sorted(filetools.listdir(DOWNLOAD_LIST_PATH)):
        if fichero.endswith(".json"):
            download_item = Item(path = os.path.join(DOWNLOAD_LIST_PATH, fichero)).fromjson(filetools.read(os.path.join(DOWNLOAD_LIST_PATH, fichero)))

            if not item.contentType == "tvshow" or (item.contentSerieName == download_item.contentSerieName and item.contentChannel == download_item.contentChannel):
              if download_item.downloadStatus in [STATUS_CODES.stoped, STATUS_CODES.canceled]:
                  res = start_download(download_item)
                  platformtools.itemlist_refresh()
                  # Si se ha cancelado paramos
                  if res == STATUS_CODES.canceled: break


def menu(item):
    logger.info()

    # Opciones disponibles para el menu
    op = ["Descargar", "Eliminar de la lista", "Reiniciar descarga", "Descargar desde..."]

    opciones = []

    # Opciones para el menu
    if item.downloadStatus == 0:  # Sin descargar
        opciones.append(op[0])  # Descargar
        opciones.append(op[3])  # Descargar desde...
        opciones.append(op[1])  # Eliminar de la lista

    if item.downloadStatus == 1:  # descarga parcial
        opciones.append(op[0])  # Descargar
        opciones.append(op[2])  # Reiniciar descarga
        opciones.append(op[1])  # Eliminar de la lista

    if item.downloadStatus == 2:  # descarga completada
        opciones.append(op[1])  # Eliminar de la lista
        opciones.append(op[2])  # Reiniciar descarga

    if item.downloadStatus == 3:  # descarga con error
        opciones.append(op[2])  # Reiniciar descarga
        opciones.append(op[1])  # Eliminar de la lista

    # Mostramos el dialogo
    seleccion = platformtools.dialog_select("Elige una opción", opciones)

    # -1 es cancelar
    if seleccion == -1: return

    logger.info("opcion=%s" % (opciones[seleccion]))
    # Opcion Eliminar
    if opciones[seleccion] == op[1]:
        filetools.remove(item.path)

    # Opcion inicaiar descarga
    if opciones[seleccion] == op[0]:
        start_download(item)
    
    # Opcion inicaiar descarga desde...
    if opciones[seleccion] == op[3]:
        start_download(item, ask=True)

    # Reiniciar descarga
    if opciones[seleccion] == op[2]:
        if filetools.isfile(os.path.join(config.get_setting("downloadpath"), item.downloadFilename)):
            filetools.remove(os.path.join(config.get_setting("downloadpath"), item.downloadFilename))
            
        update_json(item.path, {"downloadStatus" : STATUS_CODES.stoped, "downloadComplete" :  0 , "downloadProgress" : 0})

    platformtools.itemlist_refresh()


def move_to_libray(item):
    if not config.get_setting("library_move", "descargas") == True: 
      return
      
    try:
      from core import library
    except:
      return
      
    # Copiamos el archivo a la biblioteca
    origen = filetools.join(config.get_setting("downloadpath"), item.downloadFilename)
    destino = filetools.join(config.get_library_path(), *filetools.split(item.downloadFilename))
    
    if not filetools.isdir(filetools.dirname(destino)):
      filetools.mkdir(filetools.dirname(destino))
    
    if filetools.isfile(destino) and filetools.isfile(origen) :
      filetools.remove(destino)

    if filetools.isfile(origen):
      filetools.move(origen, destino)
      if len(filetools.listdir(filetools.dirname(origen))) == 0: 
        filetools.rmdir(filetools.dirname(origen))
      
    else:
      logger.error("No se ha encontrado el archivo: %s" % origen)
    
    if filetools.isfile(destino):
      if item.contentType == "movie" and item.infoLabels["tmdb_id"]:
        library_item = Item(title="Descargado: %s" % item.downloadFilename, channel= "descargas", action="findvideos", infoLabels=item.infoLabels, url=item.downloadFilename)
        
        library.save_library_movie(library_item)
        
      elif item.contentType == "episode" and item.infoLabels["tmdb_id"]:
        library_item = Item(title="Descargado: %s" % item.downloadFilename, channel= "descargas", action="findvideos", infoLabels=item.infoLabels, url=item.downloadFilename)
        
        tvshow = Item(channel= "descargas", contentType="tvshow", infoLabels = {"tmdb_id": item.infoLabels["tmdb_id"]})
        library.save_library_tvshow(tvshow, [library_item])



def update_json(path, params):
    item = Item().fromjson(filetools.read(path))
    item.__dict__.update(params)
    filetools.write(path, item.tojson())


def save_server_statistics(server, speed, success):
    from core import jsontools
    if os.path.isfile(STATS_FILE): servers = jsontools.load_json(open(STATS_FILE, "rb").read())
    else: servers = {}
    
    if not server in servers:
      servers[server] = {"success": [], "count": 0, "speeds": [], "last": 0}
    
    servers[server]["count"] += 1
    servers[server]["success"].append(bool(success))
    servers[server]["success"] = servers[server]["success"][-5:]
    servers[server]["last"] = time.time()
    if success:
      servers[server]["speeds"].append(speed)
      servers[server]["speeds"] = servers[server]["speeds"][-5:]

    open(STATS_FILE, "wb").write(jsontools.dump_json(servers))
    return

def get_server_position(server):
    from core import jsontools
    if os.path.isfile(STATS_FILE): servers = jsontools.load_json(open(STATS_FILE, "rb").read())
    else: servers = {}

    if server in servers:
      pos = [s for s in sorted(servers, key=lambda x: (sum(servers[x]["speeds"]) / (len(servers[x]["speeds"]) or 1), float(sum(servers[x]["success"])) / (len(servers[x]["success"]) or 1)), reverse = True)]
      return pos.index(server) +1
    else:
      return 0

def get_match_list(data, match_list, order_list= None, only_ascii = False, ignorecase = False):
    """
    Busca coincidencias en una cadena de texto, con un diccionario de "ID" / "Listado de cadenas de busqueda":
     { "ID1" : ["Cadena 1", "Cadena 2", "Cadena 3"],
       "ID2" : ["Cadena 4", "Cadena 5", "Cadena 6"]
     }
     
     El diccionario no pude contener una misma cadena de busqueda en varías IDs.
     
     La busqueda se realiza por orden de tamaño de cadena de busqueda (de mas larga a mas corta) si una cadena coincide,
     se elimina de la cadena a buscar para las siguientes, para que no se detecten dos categorias si una cadena es parte de otra:
     por ejemplo: "Idioma Español" y "Español" si la primera aparece en la cadena "Pablo sabe hablar el Idioma Español" 
     coincidira con "Idioma Español" pero no con "Español" ya que la coincidencia mas larga tiene prioridad.
     
    """
    import unicodedata
    match_dict = dict()
    matches = []
    
    #Pasamos la cadena a unicode
    data = unicode(data, "utf8")

    #Pasamos el diccionario a {"Cadena 1": "ID1", "Cadena 2", "ID1", "Cadena 4", "ID2"} y los pasamos a unicode
    for key in match_list:
      if order_list and not key in order_list:
        raise Exception("key '%s' not in match_list" % key)
      for value in match_list[key]:
        if value in match_dict:
          raise Exception("Duplicate word in list: '%s'" % value)
        match_dict[unicode(value, "utf8")] = key
    
    #Si ignorecase = True, lo pasamos todo a mayusculas    
    if ignorecase:
      data = data.upper()
      match_dict =  dict((key.upper(), match_dict[key]) for key in match_dict)
    
    #Si ascii = True, eliminamos todos los accentos y Ñ
    if only_ascii:
      data = ''.join((c for c in unicodedata.normalize('NFD',data) if unicodedata.category(c) != 'Mn'))
      match_dict =  dict((''.join((c for c in unicodedata.normalize('NFD',key) if unicodedata.category(c) != 'Mn')), match_dict[key]) for key in match_dict)

    #Ordenamos el listado de mayor tamaño a menor y buscamos.
    for match in sorted(match_dict, key = lambda x: len(x), reverse=True):
      s = data
      for a in matches:
        s = s.replace(a,"")
      if match in s:
        matches.append(match)
    if matches:
      if order_list:
        return type("Mtch_list",(),{"key": match_dict[matches[-1]], "index":order_list.index(match_dict[matches[-1]])})
      else:
        return type("Mtch_list",(),{"key": match_dict[matches[-1]], "index":None})
    else:
      if order_list:
        return type("Mtch_list",(),{"key": None, "index": len(order_list)})
      else:
        return type("Mtch_list",(),{"key": None, "index": None})


def sort_method(item):
    """
    Puntua cada item en funcion de varios parametros:     
    @type item: item
    @param item: elemento que se va a valorar.
    @return:  puntuacion otenida
    @rtype: int
    """
    order_list_idiomas = ["ES", "LAT", "SUB", "ENG", "VOSE"]
    match_list_idimas  = {"ES"   : ["CAST", "ESP", "Castellano", "Español", "Audio Español"],
                          "LAT"  : ["LAT", "Latino"],
                          "SUB"  : ["Subtitulo Español", "Subtitulado", "SUB"],
                          "ENG"  : ["EN", "ENG", "Inglés", "Ingles", "English"],
                          "VOSE" : ["VOSE"]}
                         
    order_list_calidad = ["BLURAY", "FULLHD", "HD", "480P", "360P", "240P"]
    match_list_calidad = {"BLURAY"   : ["BR", "BLURAY"],
                          "FULLHD"  : ["FULLHD", "FULL HD", "1080", "HD1080", "HD 1080"],
                          "HD"  : ["HD", "HD REAL", "HD 720", "720", "HDTV"],
                          "480P"  : ["SD", "480P"],
                          "360P"  : ["360P"],
                          "240P" : ["240P"]}


    return get_match_list(item.title,match_list_idimas, order_list_idiomas, ignorecase=True, only_ascii=True).index, \
           get_match_list(item.title,match_list_calidad, order_list_calidad, ignorecase=True, only_ascii=True).index, \
           get_server_position(item.server)
        

def download_from_url(url, item):
    logger.info("Intentando descargar: %s" % (url))
    if url.lower().endswith(".m3u8") or url.lower().startswith("rtmp"):
      save_server_statistics(item.server, 0, False)
      return {"downloadStatus": STATUS_CODES.error}

    # Obtenemos la ruta de descarga y el nombre del archivo
    download_path = filetools.dirname(filetools.join(DOWNLOAD_PATH, item.downloadFilename))
    file_name = filetools.basename(filetools.join(DOWNLOAD_PATH, item.downloadFilename))

    # Creamos la carpeta si no existe
    if not filetools.exists(download_path):
        filetools.mkdir(download_path)

    # Mostramos el progreso
    progreso = platformtools.dialog_progress("Descargas", "Iniciando descarga...")

    # Lanzamos la descarga
    d = Downloader(url, download_path, file_name)
    d.start()

    # Monitorizamos la descarga hasta que se termine o se cancele
    while d.state == d.states.downloading and not progreso.iscanceled():
        time.sleep(0.1)
        line1 = "%s" % (d.filename)
        line2 = "%.2f%% - %.2f %s de %.2f %s a %.2f %s/s (%d/%d)" % (
        d.progress, d.downloaded[1], d.downloaded[2], d.size[1], d.size[2], d.speed[1], d.speed[2], d.connections[0],
        d.connections[1])
        line3 = "Tiempo restante: %s" % (d.remaining_time)
        progreso.update(int(d.progress), line1, line2, line3)

    # Descarga detenida. Obtenemos el estado:
    # Se ha producido un error en la descarga
    if d.state == d.states.error:
        logger.info("Error al intentar descargar %s" % (url))
        d.stop()
        progreso.close()
        status = STATUS_CODES.error

    # Aun está descargando (se ha hecho click en cancelar)
    elif d.state == d.states.downloading:
        logger.info("Descarga detenida")
        d.stop()
        progreso.close()
        status = STATUS_CODES.canceled

    # La descarga ha finalizado
    elif d.state == d.states.completed:
        logger.info("Descargado correctamente")
        progreso.close()
        status = STATUS_CODES.completed

        if item.downloadSize and item.downloadSize != d.size[0]:
            status = STATUS_CODES.error

    
    save_server_statistics(item.server, d.speed[0], d.state != d.states.error)
    
    if progreso.iscanceled():
      status = STATUS_CODES.canceled
      
    dir = os.path.dirname(item.downloadFilename)
    file = filetools.join(dir, d.filename)
    
    if status == STATUS_CODES.completed:
        move_to_libray(item.clone(downloadFilename =  file))
        
    return {"downloadUrl": d.download_url, "downloadStatus": status, "downloadSize": d.size[0],
            "downloadProgress": d.progress, "downloadCompleted": d.downloaded[0], "downloadFilename": file}


def download_from_server(item):
    unsupported_servers = ["torrent"]
    
    progreso = platformtools.dialog_progress("Descargas", "Probando con: %s" % item.server)        
    channel = __import__('channels.%s' % item.contentChannel, None, None, ["channels.%s" % item.contentChannel])
    if hasattr(channel, "play") and not item.play_menu:

        progreso.update(50, "Probando con: %s" % item.server, "Conectando con %s..." % item.contentChannel)
        try:
          itemlist = getattr(channel, "play")(item.clone(channel=item.contentChannel, action=item.contentAction))
        except:
          logger.error("Error en el canal %s" % item.contentChannel)
        else:
          if len(itemlist) and isinstance(itemlist[0], Item):
              download_item = item.clone(**itemlist[0].__dict__)
              download_item.contentAction = download_item.action
              download_item.infoLabels = item.infoLabels
              item = download_item
          elif len(itemlist) and isinstance(itemlist[0], list):
              item.video_urls = itemlist
              if not item.server: item.server = "directo"
          else:
              logger.info("No hay nada que reproducir")
              return {"downloadStatus": STATUS_CODES.error}
    
    logger.info("contentAction: %s | contentChannel: %s | server: %s | url: %s" % (item.contentAction, item.contentChannel, item.server, item.url))
    progreso.close()
    
    if not item.server or not item.url or not item.contentAction == "play" or item.server in unsupported_servers:
      logger.error("El Item no contiene los parametros necesarios.")
      return {"downloadStatus": STATUS_CODES.error}
    
    if not item.video_urls:   
      video_urls, puedes, motivo = servertools.resolve_video_urls_for_playing(item.server, item.url, item.password, True)
    else:
      video_urls, puedes, motivo = item.video_urls, True, ""

     # Si no esta disponible, salimos
    if not puedes:
        logger.info("El vídeo **NO** está disponible")
        return {"downloadStatus": STATUS_CODES.error}

    else:
        logger.info("El vídeo **SI** está disponible")

        result = {}

        # Recorre todas las opciones hasta que consiga descargar una correctamente
        for video_url in reversed(video_urls):
            
            result = download_from_url(video_url[1], item)

            if result["downloadStatus"] in [STATUS_CODES.canceled, STATUS_CODES.completed]:
                break
                
            # Error en la descarga, continuamos con la siguiente opcion
            if result["downloadStatus"] == STATUS_CODES.error:
                continue

        # Devolvemos el estado
        return result


def download_from_best_server(item, ask = False):
    logger.info("contentAction: %s | contentChannel: %s | url: %s" % (item.contentAction, item.contentChannel, item.url))
    result =  {"downloadStatus": STATUS_CODES.error}

    progreso = platformtools.dialog_progress("Descargas", "Obteniendo lista de servidores disponibles...")

    channel = __import__('channels.%s' % item.contentChannel, None, None, ["channels.%s" % item.contentChannel])
    
    progreso.update(50, "Obteniendo lista de servidores disponibles.", "Conectando con %s..." % item.contentChannel)
    if hasattr(channel, item.contentAction):
        play_items = getattr(channel, item.contentAction)(item.clone(action = item.contentAction, channel = item.contentChannel))
    else:
        play_items = servertools.find_video_items(item.clone(action = item.contentAction, channel = item.contentChannel))
   
    play_items = filter(lambda x: x.action == "play", play_items)

    progreso.update(100, "Obteniendo lista de servidores disponibles.", "Servidores disponibles: %s" % len(play_items), "Identificando servidores...")
    
    for i in play_items:
      if not i.server:
        i.server = servertools.get_server_from_url(i.url)
        if progreso.iscanceled():
          return {"downloadStatus": STATUS_CODES.canceled}
        
    play_items.sort(key=sort_method)
    
    if progreso.iscanceled():
        return {"downloadStatus": STATUS_CODES.canceled}

    progreso.close()
    
    if not ask:
    # Recorremos el listado de servers, hasta encontrar uno que funcione
      for play_item in play_items:
          play_item = item.clone(**play_item.__dict__)
          play_item.contentAction = play_item.action
          play_item.infoLabels = item.infoLabels

          result = download_from_server(play_item)
          
          if progreso.iscanceled():
            result["downloadStatus"] = STATUS_CODES.canceled

          # Tanto si se cancela la descarga como si se completa dejamos de probar mas opciones
          if result["downloadStatus"] in [STATUS_CODES.canceled, STATUS_CODES.completed]:
              break
    else:
      seleccion = platformtools.dialog_select("Selecciona el servidor", [s.title for s in play_items])
      if seleccion > -1:
        play_item = item.clone(**play_items[seleccion].__dict__)
        play_item.contentAction = play_item.action
        play_item.infoLabels = item.infoLabels
        result = download_from_server(play_item)  
      else:
        result["downloadStatus"] = STATUS_CODES.canceled

          
    return result


def start_download(item, ask = False):
    logger.info("contentAction: %s | contentChannel: %s | url: %s" % (item.contentAction, item.contentChannel, item.url))

    # Ya tenemnos server, solo falta descargar
    if item.contentAction == "play":
        ret = download_from_server(item)
        update_json(item.path, ret)
        return ret["downloadStatus"]

    # No tenemos server, necesitamos buscar el mejor
    else:
        ret = download_from_best_server(item, ask)
        update_json(item.path, ret)
        return ret["downloadStatus"]


def get_episodes(item):
    logger.info("contentAction: %s | contentChannel: %s | contentType: %s" % (item.contentAction, item.contentChannel, item.contentType))
    
    #El item que pretendemos descargar YA es un episodio
    if item.contentType == "episode":
      episodes = [item.clone()]
      
    #El item es uma serie o temporada
    elif item.contentType in ["tvshow", "season"]:
      # importamos el canal
      channel = __import__('channels.%s' % item.contentChannel, None, None, ["channels.%s" % item.contentChannel])
      # Obtenemos el listado de episodios
      episodes = getattr(channel, item.contentAction)(item)
      
    
    itemlist = []
    
    #Tenemos las lista, ahora vamos a comprobar
    for episode in episodes:
      
      #Si partiamos de un item que ya era episodio estos datos ya están bien, no hay que modificarlos
      if item.contentType != "episode":
        episode.contentAction = episode.action
        episode.contentChannel = episode.channel
      
      #Si el resultado es una temporada, no nos vale, tenemos que descargar los episodios de cada temporada
      if episode.contentType == "season":
        itemlist.extend(get_episodes(episode))
      
      #Si el resultado es un episodio ya es lo que necesitamos, lo preparamos para añadirlo a la descarga 
      if episode.contentType == "episode":
        
        #Pasamos el id al episodio
        if not episode.infoLabels["tmdb_id"]:
          episode.infoLabels["tmdb_id"] = item.infoLabels["tmdb_id"]
        
        #Episodio, Temporada y Titulo
        if not episode.contentSeason or not episode.contentEpisodeNumber:
          season_and_episode = scrapertools.get_season_and_episode(episode.title)
          if season_and_episode:
            episode.contentSeason = season_and_episode.split("x")[0]
            episode.contentEpisodeNumber = season_and_episode.split("x")[1]
          
        #Buscamos en tmdb
        if item.infoLabels["tmdb_id"]:
          scraper.find_and_set_infoLabels(episode)
                
        #Episodio, Temporada y Titulo
        if not episode.contentTitle:
          episode.contentTitle = re.sub("\[[^\]]+\]|\([^\)]+\)|\d*x\d*\s*-","",episode.title).strip()
          
        episode.downloadFilename = filetools.validate_path(os.path.join(item.downloadFilename,"%dx%0.2d - %s" % (episode.contentSeason, episode.contentEpisodeNumber, episode.contentTitle.strip())))
        
        itemlist.append(episode)
      #Cualquier otro resultado no nos vale, lo ignoramos
      else:
        logger.info("Omitiendo item no válido: %s" % episode.tostring())
        
    return itemlist 
    
    

      
def write_json(item):
    logger.info("pelisalacarta.channels.descargas write_json")
  
    item.action = "menu"
    item.channel = "descargas"
    item.downloadStatus = STATUS_CODES.stoped
    item.downloadProgress = 0
    item.downloadSize = 0
    item.downloadCompleted = 0
    if not item.contentThumbnail:
      item.contentThumbnail = item.thumbnail
    
    for name in ["text_bold", "text_color", "text_italic", "context", "totalItems", "viewmode", "title", "fulltitle", "thumbnail"]:
      if item.__dict__.has_key(name):
        item.__dict__.pop(name)

    path = os.path.join(config.get_setting("downloadlistpath"), str(time.time()) + ".json")
    filetools.write(path, item.tojson())
    item.path = path
    time.sleep(0.1)

    
def save_download(item):
    logger.info()
    
    # Menu contextual
    if item.from_action and item.from_channel:
        item.channel = item.from_channel
        item.action = item.from_action
        del item.from_action
        del item.from_channel

    item.contentChannel = item.channel
    item.contentAction = item.action

    if item.contentType in ["tvshow", "episode", "season"]:
        save_download_tvshow(item)
                
    elif item.contentType == "movie":
        save_download_movie(item)
    
    else:
        save_download_video(item)


def save_download_video(item):
    logger.info("contentAction: %s | contentChannel: %s | contentTitle: %s" % (item.contentAction, item.contentChannel, item.contentTitle))

    set_movie_title(item)
      
    item.downloadFilename = filetools.validate_path("%s [%s]" % (item.contentTitle.strip(), item.contentChannel))

    write_json(item)
    
    if not platformtools.dialog_yesno(config.get_localized_string(30101), "¿Iniciar la descarga ahora?"):
        platformtools.dialog_ok(config.get_localized_string(30101), item.contentTitle,
                                config.get_localized_string(30109))
    else:
        start_download(item)


def save_download_movie(item):
    logger.info("contentAction: %s | contentChannel: %s | contentTitle: %s" % (item.contentAction, item.contentChannel, item.contentTitle))
    
    progreso = platformtools.dialog_progress("Descargas", "Obteniendo datos de la pelicula")
    
    set_movie_title(item)
      
    result = scraper.find_and_set_infoLabels(item)
    if not result:
      progreso.close()
      return save_download_video(item)
    
    progreso.update(0, "Añadiendo pelicula...")

    item.downloadFilename = filetools.validate_path("%s [%s]" % (item.contentTitle.strip(), item.contentChannel))

    write_json(item)

    progreso.close()
    
    if not platformtools.dialog_yesno(config.get_localized_string(30101), "¿Iniciar la descarga ahora?"):
        platformtools.dialog_ok(config.get_localized_string(30101), item.contentTitle,
                                config.get_localized_string(30109))
    else:
        start_download(item)


def save_download_tvshow(item):
    logger.info("contentAction: %s | contentChannel: %s | contentType: %s | contentSerieName: %s" % (item.contentAction, item.contentChannel, item.contentType, item.contentSerieName))
    
    progreso = platformtools.dialog_progress("Descargas", "Obteniendo datos de la serie")
    
    scraper.find_and_set_infoLabels(item)
    
    item.downloadFilename = filetools.validate_path("%s [%s]" % (item.contentSerieName, item.contentChannel))
    
    progreso.update(0, "Obteniendo episodios...", "conectando con %s..." % item.contentChannel)

    episodes = get_episodes(item)

    progreso.update(0, "Añadiendo capitulos...", " ")

    for x, i in enumerate(episodes):
        progreso.update(x * 100 / len(episodes), "%dx%0.2d: %s" % (i.contentSeason, i.contentEpisodeNumber, i.contentTitle))
        write_json(i)
    progreso.close()

    if not platformtools.dialog_yesno(config.get_localized_string(30101), "¿Iniciar la descarga ahora?"):
        platformtools.dialog_ok(config.get_localized_string(30101),
                                str(len(episodes)) + " capitulos de: " + item.contentSerieName,
                                config.get_localized_string(30109))
    else:
        for i in episodes:
            res = start_download(i)
            if res == STATUS_CODES.canceled:
                break


def set_movie_title(item):
    if not item.contentTitle:
      item.contentTitle = re.sub("\[[^\]]+\]|\([^\)]+\)","",item.fulltitle).strip()
      
    if not item.contentTitle:
      item.contentTitle = re.sub("\[[^\]]+\]|\([^\)]+\)","",item.title).strip()