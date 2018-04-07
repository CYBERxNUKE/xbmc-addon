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
# --------------------------------------------------------------------------------
# Lista de vídeos favoritos
# ------------------------------------------------------------

import os
import time

from core import scrapertools
from core import config
from core import filetools
from core import logger
from core.item import Item
from platformcode import platformtools

try:
    # Fijamos la ruta a favourites.xml
    if config.is_xbmc():
        import xbmc
        FAVOURITES_PATH = xbmc.translatePath("special://profile/favourites.xml")
    else:
        FAVOURITES_PATH = os.path.join(config.get_data_path(), "favourites.xml")
except:
    import traceback
    logger.error(traceback.format_exc())


def mainlist(item):
    logger.info()
    itemlist = []

    for name, thumb, data in read_favourites():
        if "plugin://plugin.video.%s/?" % config.PLUGIN_NAME in data:
            url = scrapertools.find_single_match(data, 'plugin://plugin.video.%s/\?([^;]*)' % config.PLUGIN_NAME)\
                .replace("&quot", "")

            item = Item().fromurl(url)
            item.title = name
            item.thumbnail = thumb
            item.isFavourite = True

            item.context = [{"title": config.get_localized_string(30154),  # "Quitar de favoritos"
                             "action": "delFavourite",
                             "channel": "favoritos",
                             "from_title": item.title},
                            {"title": "Renombrar",
                             "action": "renameFavourite",
                             "channel": "favoritos",
                             "from_title": item.title}
                            ]
            # logger.debug(item.tostring('\n'))
            itemlist.append(item)

    return itemlist


def read_favourites():
    favourites_list = []
    if filetools.exists(FAVOURITES_PATH):
        data = filetools.read(FAVOURITES_PATH)

        matches = scrapertools.find_multiple_matches(data, "<favourite([^<]*)</favourite>")
        for match in matches:
            name = scrapertools.find_single_match(match, 'name="([^"]*)')
            thumb = scrapertools.find_single_match(match, 'thumb="([^"]*)')
            data = scrapertools.find_single_match(match, '[^>]*>([^<]*)')
            favourites_list.append((name, thumb, data))

    return favourites_list


def save_favourites(favourites_list):
    raw = '<favourites>' + chr(10)
    for name, thumb, data in favourites_list:
        raw += '    <favourite name="%s" thumb="%s">%s</favourite>' % (name, thumb, data) + chr(10)
    raw += '</favourites>' + chr(10)

    return filetools.write(FAVOURITES_PATH, raw)


def addFavourite(item):
    logger.info()
    # logger.debug(item.tostring('\n'))

    # Si se llega aqui mediante el menu contextual, hay que recuperar los parametros action y channel
    if item.from_action:
        item.__dict__["action"] = item.__dict__.pop("from_action")
    if item.from_channel:
        item.__dict__["channel"] = item.__dict__.pop("from_channel")

    favourites_list = read_favourites()
    data = "ActivateWindow(10025,&quot;plugin://plugin.video.%s/?" % config.PLUGIN_NAME + item.tourl() + "&quot;,return)"
    titulo = item.title.replace('"', "'")
    favourites_list.append((titulo, item.thumbnail, data))

    if save_favourites(favourites_list):
        platformtools.dialog_ok(config.get_localized_string(30102), titulo,
                                config.get_localized_string(30108))  # 'se ha añadido a favoritos'


def delFavourite(item):
    logger.info()
    # logger.debug(item.tostring('\n'))

    if item.from_title:
        item.title = item.from_title

    favourites_list = read_favourites()
    for fav in favourites_list[:]:
        if fav[0] == item.title:
            favourites_list.remove(fav)

            if save_favourites(favourites_list):
                platformtools.dialog_ok(config.get_localized_string(30102), item.title,
                                        config.get_localized_string(30105).lower())  # 'Se ha quitado de favoritos'
                platformtools.itemlist_refresh()
            break


def renameFavourite(item):
    logger.info()
    # logger.debug(item.tostring('\n'))

    # Buscar el item q queremos renombrar en favourites.xml
    favourites_list = read_favourites()
    for i, fav in enumerate(favourites_list):
        if fav[0] == item.from_title:
            # abrir el teclado
            new_title = platformtools.dialog_input(item.from_title, item.title)
            if new_title:
                favourites_list[i] = (new_title, fav[1], fav[2])
                if save_favourites(favourites_list):
                    platformtools.dialog_ok(config.get_localized_string(30102), item.from_title,
                                            "se ha renombrado como:", new_title)  # 'Se ha quitado de favoritos'
                    platformtools.itemlist_refresh()


##################################################
# Funciones para migrar favoritos antiguos (.txt)
def readbookmark(filepath):
    logger.info()
    import urllib

    bookmarkfile = filetools.open_for_reading(filepath)

    lines = bookmarkfile.readlines()

    try:
        titulo = urllib.unquote_plus(lines[0].strip())
    except:
        titulo = lines[0].strip()

    try:
        url = urllib.unquote_plus(lines[1].strip())
    except:
        url = lines[1].strip()

    try:
        thumbnail = urllib.unquote_plus(lines[2].strip())
    except:
        thumbnail = lines[2].strip()

    try:
        server = urllib.unquote_plus(lines[3].strip())
    except:
        server = lines[3].strip()

    try:
        plot = urllib.unquote_plus(lines[4].strip())
    except:
        plot = lines[4].strip()

    # Campos fulltitle y canal añadidos
    if len(lines) >= 6:
        try:
            fulltitle = urllib.unquote_plus(lines[5].strip())
        except:
            fulltitle = lines[5].strip()
    else:
        fulltitle = titulo

    if len(lines) >= 7:
        try:
            canal = urllib.unquote_plus(lines[6].strip())
        except:
            canal = lines[6].strip()
    else:
        canal = ""

    bookmarkfile.close()

    return canal, titulo, thumbnail, plot, server, url, fulltitle


def check_bookmark(readpath):
    # Crea un listado con las entradas de favoritos
    itemlist = []

    if readpath.startswith("special://") and config.is_xbmc():
        import xbmc
        readpath = xbmc.translatePath(readpath)

    for fichero in sorted(filetools.listdir(readpath)):
        # Ficheros antiguos (".txt")
        if fichero.endswith(".txt"):
            # Esperamos 0.1 segundos entre ficheros, para que no se solapen los nombres de archivo
            time.sleep(0.1)

            # Obtenemos el item desde el .txt
            canal, titulo, thumbnail, plot, server, url, fulltitle = readbookmark(filetools.join(readpath, fichero))
            if canal == "":
                canal = "favoritos"
            item = Item(channel=canal, action="play", url=url, server=server, title=fulltitle, thumbnail=thumbnail,
                        plot=plot, fanart=thumbnail, fulltitle=fulltitle, folder=False)

            filetools.rename(filetools.join(readpath, fichero), fichero[:-4] + ".old")
            itemlist.append(item)

    # Si hay Favoritos q guardar
    if itemlist:
        favourites_list = read_favourites()
        for item in itemlist:
            data = "ActivateWindow(10025,&quot;plugin://plugin.video.pelisalacarta/?" + item.tourl() + "&quot;,return)"
            favourites_list.append((item.title, item.thumbnail, data))
        if save_favourites(favourites_list):
            logger.debug("Conversion de txt a xml correcta")


# Esto solo funcionara al migrar de versiones anteriores, ya no existe "bookmarkpath"
try:
    if config.get_setting("bookmarkpath") != "":
        check_bookmark(config.get_setting("bookmarkpath"))
    else:
        logger.info("No existe la ruta a los favoritos de versiones antiguas")
except:
    pass
