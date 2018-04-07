# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Real_Debrid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re
import time
import urllib

from core import channeltools
from core import config
from core import jsontools
from core import logger
from core import scrapertools
from platformcode import platformtools

DEBUG = config.get_setting("debug")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'}


# Returns an array of possible video url's from the page_url
def get_video_url(page_url, premium=False, video_password=""):
    logger.info("pelisalacarta.servers.realdebrid get_video_url( page_url='%s' , video_password=%s)"
                % (page_url, video_password))
    
    # Se comprueba si existe un token guardado y sino se ejecuta el proceso de autentificación
    token_auth = channeltools.get_channel_setting("realdebrid_token", "realdebrid")
    if token_auth is None or token_auth == "":
        if config.is_xbmc():
            token_auth = authentication()
            if token_auth == "":
                return [["REAL-DEBRID: No se ha completado el proceso de autentificación", ""]]
        else:
            return [["Es necesario activar la cuenta. Accede al menú de ayuda", ""]]

    post_link = urllib.urlencode([("link", page_url), ("password", video_password)])
    headers["Authorization"] = "Bearer %s" % token_auth
    url = "https://api.real-debrid.com/rest/1.0/unrestrict/link"
    data = scrapertools.downloadpage(url, post=post_link, headers=headers.items())
    data = jsontools.load_json(data)
    
    # Si el token es erróneo o ha caducado, se solicita uno nuevo
    if "error" in data and data["error"] == "bad_token":
        debrid_id = channeltools.get_channel_setting("realdebrid_id", "realdebrid")
        secret = channeltools.get_channel_setting("realdebrid_secret", "realdebrid")
        refresh = channeltools.get_channel_setting("realdebrid_refresh", "realdebrid")

        post_token = urllib.urlencode({"client_id": debrid_id, "client_secret": secret, "code": refresh,
                                       "grant_type": "http://oauth.net/grant_type/device/1.0"})
        renew_token = scrapertools.downloadpage("https://api.real-debrid.com/oauth/v2/token", post=post_token,
                                                headers=headers.items())
        renew_token = jsontools.load_json(renew_token)
        if not "error" in renew_token:
            token_auth = renew_token["access_token"]
            channeltools.set_channel_setting("realdebrid_token", token_auth, "realdebrid")
            headers["Authorization"] = "Bearer %s" % token_auth
            data = scrapertools.downloadpage(url, post=post_link, headers=headers.items())
            data = jsontools.load_json(data)

    if "download" in data:
        return get_enlaces(data)
    else:
        if "error" in data:
            msg = data["error"].decode("utf-8","ignore")
            msg = msg.replace("hoster_unavailable", "Servidor no disponible") \
                     .replace("unavailable_file", "Archivo no disponible") \
                     .replace("hoster_not_free", "Servidor no gratuito") \
                     .replace("bad_token", "Error en el token")
            return [["REAL-DEBRID: " + msg, ""]]
        else:
            return [["REAL-DEBRID: No se ha generado ningún enlace", ""]]


def get_enlaces(data):
    itemlist = []
    if "alternative" in data:
        for link in data["alternative"]:
            video_url = link["download"].encode("utf-8")
            title = video_url.rsplit(".", 1)[1]
            if "quality" in link:
                title += " (" + link["quality"] + ") [realdebrid]"
            itemlist.append([title, video_url])
    else:
        video_url = data["download"].encode("utf-8")
        title = video_url.rsplit(".", 1)[1] + " [realdebrid]"
        itemlist.append([title, video_url])

    return itemlist


def authentication():
    logger.info("pelisalacarta.servers.realdebrid authentication")
    try:
        client_id = "YTWNFBIJEEBP6"
        
        # Se solicita url y código de verificación para conceder permiso a la app
        url = "http://api.real-debrid.com/oauth/v2/device/code?client_id=%s&new_credentials=yes" % (client_id)
        data = scrapertools.downloadpage(url, headers=headers.items())
        data = jsontools.load_json(data)
        verify_url = data["verification_url"]
        user_code = data["user_code"]
        device_code = data["device_code"]
        intervalo = data["interval"]
        
        
        dialog_auth = platformtools.dialog_progress("Autentificación. No cierres esta ventana!!",
                                                    "1. Entra en la siguiente url: %s" % verify_url,
                                                    "2. Ingresa este código en la página y presiona Allow:  %s" % user_code,
                                                    "3. Espera a que se cierre esta ventana")
        
        # Generalmente cada 5 segundos se intenta comprobar si el usuario ha introducido el código
        while True:
            time.sleep(intervalo)
            try:
                if dialog_auth.iscanceled():
                    return ""

                url = "https://api.real-debrid.com/oauth/v2/device/credentials?client_id=%s&code=%s" \
                      % (client_id, device_code)
                data = scrapertools.downloadpage(url, headers=headers.items())
                data = jsontools.load_json(data)
                if "client_secret" in data:
                    # Código introducido, salimos del bucle
                    break
            except:
                pass

        try:
            dialog_auth.close()
        except:
            pass
        
        debrid_id = data["client_id"]
        secret = data["client_secret"] 

        # Se solicita el token de acceso y el de actualización para cuando el primero caduque
        post = urllib.urlencode({"client_id": debrid_id, "client_secret": secret, "code": device_code,
                                 "grant_type": "http://oauth.net/grant_type/device/1.0"})
        data = scrapertools.downloadpage("https://api.real-debrid.com/oauth/v2/token", post=post,
                                         headers=headers.items())
        data = jsontools.load_json(data)

        token = data["access_token"]
        refresh = data["refresh_token"]

        channeltools.set_channel_setting("realdebrid_id", debrid_id, "realdebrid")
        channeltools.set_channel_setting("realdebrid_secret", secret, "realdebrid")
        channeltools.set_channel_setting("realdebrid_token", token, "realdebrid")
        channeltools.set_channel_setting("realdebrid_refresh", refresh, "realdebrid")
        
        return token
    except:
        import traceback
        logger.error(traceback.format_exc())
        return ""
