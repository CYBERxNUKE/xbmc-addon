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
# Download and play
#------------------------------------------------------------
# Based on code from the Mega add-on (xbmchub.com)
#---------------------------------------------------------------------------

import os
import re
import socket
import sys
import threading
import time
import urllib
import urllib2

import xbmc
import xbmcgui

from core import config
from core import downloadtools
from core import logger


# Download a file and start playing while downloading
def download_and_play(url,file_name,download_path):
    # Lanza thread
    logger.info("[download_and_play.py] Active threads "+str(threading.active_count()))
    logger.info("[download_and_play.py] "+repr(threading.enumerate()))
    logger.info("[download_and_play.py] Starting download thread...")
    download_thread = DownloadThread(url,file_name,download_path)
    download_thread.start()
    logger.info("[download_and_play.py] Download thread started")
    logger.info("[download_and_play.py] Active threads "+str(threading.active_count()))
    logger.info("[download_and_play.py] "+repr(threading.enumerate()))

    # Espera
    logger.info("[download_and_play.py] Waiting...")

    while True:
        cancelled=False
        dialog = xbmcgui.DialogProgress()
        dialog.create('Descargando...', 'Cierra esta ventana para empezar la reproducción')
        dialog.update(0)

        while not cancelled and download_thread.isAlive():
            dialog.update( download_thread.get_progress() , "Cancela esta ventana para empezar la reproducción", "Velocidad: "+str(int(download_thread.get_speed()/1024))+" KB/s "+str(download_thread.get_actual_size())+"MB de "+str(download_thread.get_total_size())+"MB" , "Tiempo restante: "+str( downloadtools.sec_to_hms(download_thread.get_remaining_time())) )
            xbmc.sleep(1000)

            if dialog.iscanceled():
                cancelled=True
                break

        dialog.close()

        logger.info("[download_and_play.py] End of waiting")

        # Lanza el reproductor
        player = CustomPlayer()
        player.set_download_thread(download_thread)
        player.PlayStream( download_thread.get_file_name() )

        # Fin de reproducción
        logger.info("[download_and_play.py] Fin de reproducción")

        if player.is_stopped():
            logger.info("[download_and_play.py] Terminado por el usuario")
            break
        else:
            if not download_thread.isAlive():
                logger.info("[download_and_play.py] La descarga ha terminado")
                break
            else:
                logger.info("[download_and_play.py] Continua la descarga")

    # Cuando el reproductor acaba, si continúa descargando lo para ahora
    logger.info("[download_and_play.py] Download thread alive="+str(download_thread.isAlive()))
    if download_thread.isAlive():
        logger.info("[download_and_play.py] Killing download thread")
        download_thread.force_stop()


class CustomPlayer(xbmc.Player):
    def __init__( self, *args, **kwargs ):
        logger.info("CustomPlayer.__init__")
        self.actualtime=0
        self.totaltime=0
        self.stopped=False
        xbmc.Player.__init__( self )

    def PlayStream(self, url):  
        logger.info("CustomPlayer.PlayStream url="+url)
        self.play(url)
        self.actualtime=0
        self.url=url
        while self.isPlaying():
            self.actualtime = self.getTime()
            self.totaltime = self.getTotalTime()
            logger.info("CustomPlayer.PlayStream actualtime="+str(self.actualtime)+" totaltime="+str(self.totaltime))
            xbmc.sleep(3000)

    def set_download_thread(self,download_thread):
        logger.info("CustomPlayer.set_download_thread")
        self.download_thread = download_thread

    def force_stop_download_thread(self):
        logger.info("CustomPlayer.force_stop_download_thread")

        if self.download_thread.isAlive():
            logger.info("CustomPlayer.force_stop_download_thread Killing download thread")
            self.download_thread.force_stop()

            #while self.download_thread.isAlive():
            #    xbmc.sleep(1000)

    def onPlayBackStarted(self):
        logger.info("CustomPlayer.onPlayBackStarted PLAYBACK STARTED")

    def onPlayBackEnded(self):
        logger.info("CustomPlayer.onPlayBackEnded PLAYBACK ENDED")

    def onPlayBackStopped(self):
        logger.info("CustomPlayer.onPlayBackStopped PLAYBACK STOPPED")
        self.stopped=True
        self.force_stop_download_thread()

    def is_stopped(self):
        return self.stopped

# Download in background
class DownloadThread(threading.Thread):
    
    def __init__(self, url, file_name, download_path):
        logger.info("DownloadThread.__init__ "+repr(file))
        self.url = url
        self.download_path = download_path
        self.file_name = os.path.join( download_path , file_name )
        self.progress = 0
        self.force_stop_file_name = os.path.join( self.download_path , "force_stop.tmp" )
        self.velocidad=0
        self.tiempofalta=0
        self.actual_size=0
        self.total_size=0

        if os.path.exists(self.force_stop_file_name):
            os.remove(self.force_stop_file_name)

        threading.Thread.__init__(self)

    def run(self):
        logger.info("DownloadThread.run Download starts...")

        if "megacrypter.com" in self.url:
            self.download_file_megacrypter()
        else:
            self.download_file()
        logger.info("DownloadThread.run Download ends")

    def force_stop(self):
        logger.info("DownloadThread.force_stop...")
        force_stop_file = open( self.force_stop_file_name , "w" )
        force_stop_file.write("0")
        force_stop_file.close()

    def get_progress(self):
        return self.progress;

    def get_file_name(self):
        return self.file_name

    def get_speed(self):
        return self.velocidad

    def get_remaining_time(self):
        return self.tiempofalta

    def get_actual_size(self):
        return self.actual_size

    def get_total_size(self):
        return self.total_size

    def download_file_megacrypter(self):
        logger.info("DownloadThread.download_file Megacrypter downloader")

        comando = "./megacrypter.sh"
        logger.info("DownloadThread.download_file comando="+comando)

        oldcwd = os.getcwd()
        logger.info("DownloadThread.download_file oldcwd="+oldcwd)

        cwd = os.path.join( config.get_runtime_path() , "tools")
        logger.info("DownloadThread.download_file cwd="+cwd)
        os.chdir(cwd)
        logger.info("DownloadThread.download_file directory changed to="+os.getcwd())

        logger.info("DownloadThread.download_file destino="+self.download_path)

        os.system( comando+" '"+self.url+ "' \"" + self.download_path+"\"" )
        #p = subprocess.Popen([comando , self.url , self.download_path], cwd=cwd, stdout=subprocess.PIPE , stderr=subprocess.PIPE )
        #out, err = p.communicate()
        #logger.info("DownloadThread.download_file out="+out)

        os.chdir(oldcwd)

    def download_file(self):
        logger.info("DownloadThread.download_file Direct download")

        headers=[]

        # Se asegura de que el fichero se podrá crear
        logger.info("DownloadThread.download_file nombrefichero="+self.file_name)
        self.file_name = xbmc.makeLegalFilename(self.file_name)
        logger.info("DownloadThread.download_file nombrefichero="+self.file_name)
        logger.info("DownloadThread.download_file url="+self.url)
    
        # Crea el fichero
        existSize = 0
        f = open(self.file_name, 'wb')
        grabado = 0

        # Interpreta las cabeceras en una URL como en XBMC
        if "|" in self.url:
            additional_headers = self.url.split("|")[1]
            if "&" in additional_headers:
                additional_headers = additional_headers.split("&")
            else:
                additional_headers = [ additional_headers ]
    
            for additional_header in additional_headers:
                logger.info("DownloadThread.download_file additional_header: "+additional_header)
                name = re.findall( "(.*?)=.*?" , additional_header )[0]
                value = urllib.unquote_plus(re.findall( ".*?=(.*?)$" , additional_header )[0])
                headers.append( [ name,value ] )
    
            self.url = self.url.split("|")[0]
            logger.info("DownloadThread.download_file url="+self.url)
    
        # Timeout del socket a 60 segundos
        socket.setdefaulttimeout(60)

        # Crea la petición y añade las cabeceras
        h=urllib2.HTTPHandler(debuglevel=0)
        request = urllib2.Request(self.url)
        for header in headers:
            logger.info("DownloadThread.download_file Header="+header[0]+": "+header[1])
            request.add_header(header[0],header[1])

        # Lanza la petición
        opener = urllib2.build_opener(h)
        urllib2.install_opener(opener)
        try:
            connexion = opener.open(request)
        except urllib2.HTTPError,e:
            logger.info("DownloadThread.download_file error %d (%s) al abrir la url %s" % (e.code,e.msg,self.url))
            #print e.code
            #print e.msg
            #print e.hdrs
            #print e.fp
            f.close()

            # El error 416 es que el rango pedido es mayor que el fichero => es que ya está completo
            if e.code==416:
                return 0
            else:
                return -2
    
        try:
            totalfichero = int(connexion.headers["Content-Length"])
        except:
            totalfichero = 1

        self.total_size = int(float(totalfichero) / float(1024*1024))
                
        logger.info("Content-Length=%s" % totalfichero)        
        blocksize = 100*1024
    
        bloqueleido = connexion.read(blocksize)
        logger.info("DownloadThread.download_file Iniciando descarga del fichero, bloqueleido=%s" % len(bloqueleido))
    
        maxreintentos = 10

        while len(bloqueleido)>0:
            try:
                if os.path.exists(self.force_stop_file_name):
                    logger.info("DownloadThread.download_file Detectado fichero force_stop, se interrumpe la descarga")
                    f.close()

                    xbmc.executebuiltin((u'XBMC.Notification("Cancelado", "Descarga en segundo plano cancelada", 300)'))

                    return

                # Escribe el bloque leido
                #try:
                #    import xbmcvfs
                #    f.write( bloqueleido )
                #except:
                f.write(bloqueleido)
                grabado = grabado + len(bloqueleido)
                logger.info("DownloadThread.download_file grabado=%d de %d" % (grabado,totalfichero) )
                percent = int(float(grabado)*100/float(totalfichero))
                self.progress=percent;
                totalmb = float(float(totalfichero)/(1024*1024))
                descargadosmb = float(float(grabado)/(1024*1024))
                self.actual_size = int(descargadosmb)
    
                # Lee el siguiente bloque, reintentando para no parar todo al primer timeout
                reintentos = 0
                while reintentos <= maxreintentos:
                    try:

                        before = time.time()
                        bloqueleido = connexion.read(blocksize)
                        after = time.time()
                        if (after - before) > 0:
                            self.velocidad=len(bloqueleido)/((after - before))
                            falta=totalfichero-grabado
                            if self.velocidad>0:
                                self.tiempofalta=falta/self.velocidad
                            else:
                                self.tiempofalta=0
                        break
                    except:
                        reintentos = reintentos + 1
                        logger.info("DownloadThread.download_file ERROR en la descarga del bloque, reintento %d" % reintentos)
                        for line in sys.exc_info():
                            logger.error( "%s" % line )
                
                # Ha habido un error en la descarga
                if reintentos > maxreintentos:
                    logger.info("DownloadThread.download_file ERROR en la descarga del fichero")
                    f.close()
    
                    return -2
    
            except:
                import traceback,sys
                from pprint import pprint
                exc_type, exc_value, exc_tb = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_tb)
                for line in lines:
                    line_splits = line.split("\n")
                    for line_split in line_splits:
                        logger.error(line_split)

                f.close()
                return -2

        return