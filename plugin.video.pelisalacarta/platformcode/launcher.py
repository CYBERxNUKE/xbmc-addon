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
# XBMC Launcher (xbmc / kodi / boxee)
# ------------------------------------------------------------

import os
import re
import sys
import urllib2

from core import channeltools
from core import config
from core import library
from core import logger
from core import scrapertools
from core.item import Item
from platformcode import platformtools


def start():
    """ Primera funcion que se ejecuta al entrar en el plugin.
    Dentro de esta funcion deberian ir todas las llamadas a las
    funciones que deseamos que se ejecuten nada mas abrir el plugin.
    """
    logger.info()

    # Test if all the required directories are created
    config.verify_directories_created()


def run():
    logger.info()

    # Extract item from sys.argv
    if sys.argv[2]:
        item = Item().fromurl(sys.argv[2])

    # If no item, this is mainlist
    else:
        item = Item(channel="channelselector", action="getmainlist", viewmode="movie")

    logger.info(item.tostring())

    try:

        # If item has no action, stops here
        if item.action == "":
            logger.info("Item sin accion")
            return

        # Action for main menu in channelselector
        if item.action == "getmainlist":
            import channelselector

            # Check for updates only on first screen
            if config.get_setting("check_for_plugin_updates") == "true":
                logger.info("Check for plugin updates enabled")
                from core import updater

                try:
                    config.set_setting("plugin_updates_available","0")
                    new_published_version_tag , number_of_updates = updater.get_available_updates()

                    config.set_setting("plugin_updates_available",str(number_of_updates))
                    itemlist = channelselector.getmainlist()

                    if new_published_version_tag!="":

                        platformtools.dialog_notification(new_published_version_tag+" disponible",
                                                "Ya puedes descargar la nueva versión del plugin\n"
                                                "desde el listado principal")

                        itemlist = channelselector.getmainlist()
                        itemlist.insert(0, Item(title="Descargar version "+new_published_version_tag, version=new_published_version_tag, channel="updater",
                                                action="update", thumbnail=channelselector.get_thumb("squares","thumb_actualizar.png")))
                except:
                    import traceback
                    logger.info(traceback.format_exc())
                    platformtools.dialog_ok("No se puede conectar", "No ha sido posible comprobar",
                                            "si hay actualizaciones")
                    logger.info("Fallo al verificar la actualización")
                    config.set_setting("plugin_updates_available","0")
                    itemlist = channelselector.getmainlist()

            else:
                logger.info("Check for plugin updates disabled")
                config.set_setting("plugin_updates_available","0")
                itemlist = channelselector.getmainlist()

            platformtools.render_items(itemlist, item)

        # Action for updating plugin
        elif item.action == "update":

            from core import updater
            updater.update(item)
            config.set_setting("plugin_updates_available","0")
            if config.get_system_platform() != "xbox":
                import xbmc
                xbmc.executebuiltin("Container.Refresh")

        # Action for channel types on channelselector: movies, series, etc.
        elif item.action == "getchanneltypes":
            import channelselector
            itemlist = channelselector.getchanneltypes()

            platformtools.render_items(itemlist, item)

        # Action for channel listing on channelselector
        elif item.action == "filterchannels":
            import channelselector
            itemlist = channelselector.filterchannels(item.channel_type)

            platformtools.render_items(itemlist, item)

        # Special action for playing a video from the library
        elif item.action == "play_from_library":
            play_from_library(item)
            return

        # Action in certain channel specified in "action" and "channel" parameters
        else:

            # Entry point for a channel is the "mainlist" action, so here we check parental control
            if item.action == "mainlist":

                # Parental control
                can_open_channel = False

                # If it is an adult channel, and user has configured pin, asks for it
                if channeltools.is_adult(item.channel) and config.get_setting("adult_pin") != "":

                    tecleado = platformtools.dialog_input("", "PIN para canales de adultos", True)
                    if tecleado is not None:
                        if tecleado == config.get_setting("adult_pin"):
                            can_open_channel = True

                # All the other cases can open the channel
                else:
                    can_open_channel = True

                if not can_open_channel:
                    return

            # Actualiza el canal individual
            if (item.action == "mainlist" and
                    item.channel != "channelselector" and
                    config.get_setting("check_for_channel_updates") == "true"):
                from core import updater
                updater.update_channel(item.channel)

            # Checks if channel exists
            channel_file = os.path.join(config.get_runtime_path(),
                                        'channels', item.channel + ".py")
            logger.info("channel_file=%s" % channel_file)

            channel = None

            if item.channel in ["personal", "personal2", "personal3", "personal4", "personal5"]:
                import channels.personal as channel

            elif os.path.exists(channel_file):
                try:
                    channel = __import__('channels.%s' % item.channel, None,
                                         None, ["channels.%s" % item.channel])
                except ImportError:
                    exec "import channels." + item.channel + " as channel"

            logger.info("Running channel %s | %s" % (channel.__name__, channel.__file__))

            # Special play action
            if item.action == "play":
                logger.info("item.action=%s" % item.action.upper())
                # logger.debug("item_toPlay: " + "\n" + item.tostring('\n'))

                # First checks if channel has a "play" function
                if hasattr(channel, 'play'):
                    logger.info("Executing channel 'play' method")
                    itemlist = channel.play(item)
                    b_favourite = item.isFavourite
                    # Play should return a list of playable URLS
                    if len(itemlist) > 0 and isinstance(itemlist[0], Item):
                        item = itemlist[0]
                        if b_favourite:
                            item.isFavourite = True
                        platformtools.play_video(item)

                    # Permitir varias calidades desde play en el canal
                    elif len(itemlist) > 0 and isinstance(itemlist[0], list):
                        item.video_urls = itemlist
                        platformtools.play_video(item)

                    # If not, shows user an error message
                    else:
                        platformtools.dialog_ok("pelisalacarta", "No hay nada para reproducir")

                # If player don't have a "play" function, not uses the standard play from platformtools
                else:
                    logger.info("Executing core 'play' method")
                    platformtools.play_video(item)

            # Special action for findvideos, where the plugin looks for known urls
            elif item.action == "findvideos":

                # First checks if channel has a "findvideos" function
                if hasattr(channel, 'findvideos'):
                    itemlist = getattr(channel, item.action)(item)

                # If not, uses the generic findvideos function
                else:
                    logger.info("No channel 'findvideos' method, "
                                "executing core method")
                    from core import servertools
                    itemlist = servertools.find_video_items(item)

                if config.get_setting('filter_servers') == 'true':
                    itemlist = filtered_servers(itemlist)

                if config.get_setting("max_links", "biblioteca") != 0:
                    itemlist = limit_itemlist(itemlist)

                from platformcode import subtitletools
                subtitletools.saveSubtitleName(item)

                platformtools.render_items(itemlist, item)

            # Special action for adding a movie to the library
            elif item.action == "add_pelicula_to_library":
                library.add_pelicula_to_library(item)

            # Special action for adding a serie to the library
            elif item.action == "add_serie_to_library":
                library.add_serie_to_library(item, channel)

            # Special action for downloading all episodes from a serie
            elif item.action == "download_all_episodes":
                from channels import descargas
                item.action = item.extra
                del item.extra
                descargas.save_download(item)

            # Special action for searching, first asks for the words then call the "search" function
            elif item.action == "search":
                logger.info("item.action=%s" % item.action.upper())

                last_search = ""
                last_search_active = config.get_setting("last_search", "buscador")
                if last_search_active:
                    try:
                        current_saved_searches_list = list(config.get_setting("saved_searches_list", "buscador"))
                        last_search = current_saved_searches_list[0]
                    except:
                        pass

                tecleado = platformtools.dialog_input(last_search)
                if tecleado is not None:
                    if last_search_active and not tecleado.startswith("http"):
                        from channels import buscador
                        buscador.save_search(tecleado)

                    # TODO revisar 'personal.py' porque no tiene función search y daría problemas
                    itemlist = channel.search(item, tecleado)
                else:
                    return

                platformtools.render_items(itemlist, item)

            # For all other actions
            else:
                logger.info("Executing channel '%s' method" % item.action)
                itemlist = getattr(channel, item.action)(item)
                platformtools.render_items(itemlist, item)

    except urllib2.URLError, e:
        import traceback
        logger.error(traceback.format_exc())

        # Grab inner and third party errors
        if hasattr(e, 'reason'):
            logger.info("Razon del error, codigo: %s | Razon: %s" %
                        (str(e.reason[0]), str(e.reason[1])))
            texto = config.get_localized_string(30050)  # "No se puede conectar con el sitio web"
            platformtools.dialog_ok("pelisalacarta", texto)

        # Grab server response errors
        elif hasattr(e, 'code'):
            logger.info("Codigo de error HTTP : %d" % e.code)
            # "El sitio web no funciona correctamente (error http %d)"
            platformtools.dialog_ok("pelisalacarta", config.get_localized_string(30051) % e.code)

    except:
        import traceback
        logger.error(traceback.format_exc())

        patron = 'File "'+os.path.join(config.get_runtime_path(), "channels", "").replace("\\", "\\\\")+'([^.]+)\.py"'
        canal = scrapertools.find_single_match(traceback.format_exc(), patron)

        try:
            import xbmc
            if config.get_platform(True)['num_version'] < 14:
                log_name = "xbmc.log"
            else:
                log_name = "kodi.log"
            log_message = "Ruta: "+xbmc.translatePath("special://logpath")+log_name
        except:
            log_message = ""

        if canal:
            platformtools.dialog_ok(
                "Error inesperado en el canal " + canal,
                "Puede deberse a un fallo de conexión, la web del canal "
                "ha cambiado su estructura, o un error interno de pelisalacarta.",
                "Para saber más detalles, consulta el log.", log_message)
        else:
            platformtools.dialog_ok(
                "Se ha producido un error en pelisalacarta",
                "Comprueba el log para ver mas detalles del error.",
                log_message)


def set_server_list():
    logger.info()

    server_white_list = []
    server_black_list = []

    if len(config.get_setting('whitelist')) > 0:
        server_white_list_key = config.get_setting('whitelist').replace(', ', ',').replace(' ,', ',')
        server_white_list = re.split(',', server_white_list_key)

    if len(config.get_setting('blacklist')) > 0:
        server_black_list_key = config.get_setting('blacklist').replace(', ', ',').replace(' ,', ',')
        server_black_list = re.split(',', server_black_list_key)

    logger.info("WhiteList %s" % server_white_list)
    logger.info("BlackList %s" % server_black_list)

    return server_white_list, server_black_list


def filtered_servers(itemlist):
    logger.info()
    # logger.debug("Inlet itemlist size: %i" % len(itemlist))

    new_list = []
    white_counter = 0
    black_counter = 0

    server_white_list, server_black_list = set_server_list()

    white_list_order = config.get_setting("white_list_order", "biblioteca")

    if len(server_white_list) > 0:
        logger.info("WhiteList")
        if white_list_order:
            for server in server_white_list:
                logger.info("Servidor: " + server)
                for item in itemlist:
                    if server in unicode(item.title, "utf8").lower().encode("utf8"):
                        logger.info("Coincidencia: " + item.title)
                        new_list.append(item)
                        white_counter += 1

        else:
            for item in itemlist:
                logger.info("item.title: " + item.title)
                if any(server in unicode(item.title, "utf8").lower().encode("utf8")
                       for server in server_white_list):
                    # logger.info("found")
                    new_list.append(item)
                    white_counter += 1
                # else:
                #     logger.info("not found")

    if len(server_black_list) > 0:
        logger.info("BlackList")

        # Si existe 'new_list' se añade lo restante y se filtra
        if len(new_list) != 0:
            # Se añade al final de 'new_list' lo que no tuviera de 'itemlist'
            if len(new_list) != len(itemlist):
                for item_1 in itemlist:
                    coincidencia = False
                    for item_2 in new_list:
                        if item_2.title == item_1.title:
                            coincidencia = True
                            break
                    if not coincidencia:
                        new_list.append(item_1)

            itemlist = new_list
            new_list = []

        for item in itemlist:
            logger.info("item.title: " + item.title)
            if any(server in unicode(item.title, "utf8").lower().encode("utf8")
                   for server in server_black_list):
                # logger.info("found")
                black_counter += 1

            # Se pasa a 'new_list' si el servidor no estaba en la lista negra.
            else:
                new_list.append(item)

    logger.info("WhiteList server %s has #%d rows" %
                (server_white_list, white_counter))
    logger.info("BlackList server %s has #%d rows" %
                (server_black_list, black_counter))
    logger.info("Rest has #%d rows" % (len(new_list) - white_counter))

    if len(new_list) == 0:
        new_list = itemlist

    # logger.debug("Outlet itemlist size: %i" % len(new_list))
    return new_list


def reorder_itemlist(itemlist):
    logger.info()
    # logger.debug("Inlet itemlist size: %i" % len(itemlist))

    new_list = []
    mod_list = []
    not_mod_list = []

    modified = 0
    not_modified = 0

    to_change = [['Ver en',       '[V]'],
                 ['Descargar en', '[D]']]

    for item in itemlist:
        old_title = unicode(item.title, "utf8").lower().encode("utf8")
        for before, after in to_change:
            if before in item.title:
                item.title = item.title.replace(before, after)
                break

        new_title = unicode(item.title, "utf8").lower().encode("utf8")
        if old_title != new_title:
            mod_list.append(item)
            modified += 1
        else:
            not_mod_list.append(item)
            not_modified += 1

        # logger.debug("OLD: %s | NEW: %s" % (old_title, new_title))

    new_list.extend(mod_list)
    new_list.extend(not_mod_list)

    logger.info("Titulos modificados:%i | No modificados:%i" %
                (modified, not_modified))

    if len(new_list) == 0:
        new_list = itemlist

    # logger.debug("Outlet itemlist size: %i" % len(new_list))
    return new_list


def limit_itemlist(itemlist):
    logger.info()
    # logger.debug("Inlet itemlist size: %i" % len(itemlist))

    new_list = []

    try:
        opt = config.get_setting("max_links", "biblioteca")
        if opt == 0:
            new_list = itemlist
        else:
            i_max = 30 * opt
            new_list = itemlist[:i_max]

        # logger.debug("Outlet itemlist size: %i" % len(new_list))
        return new_list
    except:
        return itemlist


def play_from_library(item):
    """
        Los .strm al reproducirlos desde kodi, este espera que sea un archivo "reproducible" asi que no puede contener
        más items, como mucho se puede colocar un dialogo de seleccion.
        Esto lo solucionamos "engañando a kodi" y haciendole creer que se ha reproducido algo, asi despues mediante
        "Container.Update()" cargamos el strm como si un item desde dentro de pelisalacarta se tratara, quitando todas
        las limitaciones y permitiendo reproducir mediante la funcion general sin tener que crear nuevos métodos para
        la biblioteca.
        @type item: item
        @param item: elemento con información
    """
    logger.info()
    # logger.debug("item: \n" + item.tostring('\n'))

    import xbmcgui
    import xbmcplugin
    import xbmc
    # Intentamos reproducir una imagen (esto no hace nada y ademas no da error)
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True,
                              xbmcgui.ListItem(path=os.path.join(config.get_runtime_path(), "resources", "subtitle.mp4")))

    # Por si acaso la imagen hiciera (en futuras versiones) le damos a stop para detener la reproduccion
    xbmc.Player().stop()

    # modificamos el action (actualmente la biblioteca necesita "findvideos" ya que es donde se buscan las fuentes
    item.action = "findvideos"

    window_type = config.get_setting("window_type", "biblioteca")

    # y volvemos a lanzar kodi
    if xbmc.getCondVisibility('Window.IsMedia') and not window_type == 1:
        # Ventana convencional
        xbmc.executebuiltin("Container.Update(" + sys.argv[0] + "?" + item.tourl() + ")")

    else:
        # Ventana emergente
        from channels import biblioteca
        p_dialog = platformtools.dialog_progress_bg('pelisalacarta', 'Cargando...')
        p_dialog.update(0, '')

        itemlist = biblioteca.findvideos(item)

        p_dialog.update(50, '')

        # Se filtran los enlaces segun la lista blanca y negra
        if config.get_setting('filter_servers') == 'true':
            itemlist = filtered_servers(itemlist)

        # Se limita la cantidad de enlaces a mostrar
        if config.get_setting("max_links", "biblioteca") != 0:
            itemlist = limit_itemlist(itemlist)

        # Se "limpia" ligeramente la lista de enlaces
        if config.get_setting("replace_VD", "biblioteca") == 1:
            itemlist = reorder_itemlist(itemlist)

        p_dialog.update(100, '')
        xbmc.sleep(500)
        p_dialog.close()

        if len(itemlist) > 0:
            # El usuario elige el mirror
            opciones = []
            for item in itemlist:
                opciones.append(item.title)

            # Se abre la ventana de seleccion
            if (item.contentSerieName != "" and
                    item.contentSeason != "" and
                    item.contentEpisodeNumber != ""):
                cabecera = ("%s - %sx%s -- %s" %
                            (item.contentSerieName,
                             item.contentSeason,
                             item.contentEpisodeNumber,
                             config.get_localized_string(30163)))
            else:
                cabecera = config.get_localized_string(30163)

            seleccion = platformtools.dialog_select(cabecera, opciones)

            if seleccion == -1:
                return
            else:
                item = biblioteca.play(itemlist[seleccion])[0]
                platformtools.play_video(item)
