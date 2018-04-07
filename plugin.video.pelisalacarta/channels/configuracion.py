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
# Configuracion
# ------------------------------------------------------------

import os

from core import config
from core.item import Item
from core import logger
from core import filetools

from platformcode import platformtools

DEBUG = True
CHANNELNAME = "configuracion"


def mainlist(item):
    logger.info()

    itemlist = list()
    itemlist.append(Item(channel=CHANNELNAME, title="Preferencias", action="settings", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    if config.get_setting("plugin_updates_available") == "0":
        nuevas = ""
    elif config.get_setting("plugin_updates_available") == "1":
        nuevas = " (1 nueva)"
    else:
        nuevas = " (" + config.get_setting("plugin_updates_available") + " nuevas)"

    thumb_configuracion = "thumb_configuracion_" + config.get_setting("plugin_updates_available") + ".png"

    itemlist.append(Item(channel=CHANNELNAME, title="Descargar e instalar otras versiones" + nuevas,
                         action="get_all_versions", folder=True,
                         thumbnail=get_thumbnail_path(thumb_configuracion)))

    itemlist.append(Item(channel=CHANNELNAME, title="", action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes especiales", action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    itemlist.append(Item(channel="novedades", title="   Ajustes de la sección 'Novedades'", action="menu_opciones",
                         folder=True, thumbnail=get_thumbnail_path("thumb_novedades.png")))
    itemlist.append(Item(channel="buscador", title="   Ajustes del buscador global", action="opciones", folder=True,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Ajustes de descargas", action="channel_config", config="descargas", folder=True,
                         thumbnail=get_thumbnail_path("thumb_descargas.png")))
                         
    if config.get_library_support():
        itemlist.append(Item(channel="biblioteca", title="   Ajustes de la biblioteca",
                             action="channel_config", folder=True,
                             thumbnail=get_thumbnail_path("thumb_biblioteca.png")))
        itemlist.append(Item(channel="biblioteca", action="update_biblio", folder=False,
                             thumbnail=get_thumbnail_path("thumb_biblioteca.png"),
                             title="   Buscar nuevos episodios y actualizar biblioteca"))

    itemlist.append(Item(channel=CHANNELNAME, title="   Añadir o Actualizar canal/conector desde una URL",
                         action="menu_addchannels"))
    itemlist.append(Item(channel=CHANNELNAME, action="", title="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    itemlist.append(Item(channel=CHANNELNAME, title="Activar/desactivar canales",
                         action="conf_tools", folder=False, extra="channels_onoff",
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="Ajustes por canales",
                         action="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    # Inicio - Canales configurables
    import channelselector
    from core import channeltools
    channel_list = channelselector.filterchannels("all")

    for channel in channel_list:
        channel_parameters = channeltools.get_channel_parameters(channel.channel)

        if channel_parameters["has_settings"]:
            itemlist.append(Item(channel=CHANNELNAME, title="   Configuración del canal '%s'" % channel.title,
                                 action="channel_config", config=channel.channel, folder=False,
                                 thumbnail=channel.thumbnail))
    # Fin - Canales configurables

    itemlist.append(Item(channel=CHANNELNAME, action="", title="", folder=False,
                         thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="Otras herramientas", action="submenu_tools",
                         folder=True, thumbnail=get_thumbnail_path("thumb_configuracion_0.png")))

    return itemlist


def channel_config(item):
    return platformtools.show_channel_settings(channelpath=filetools.join(config.get_runtime_path(), "channels",
                                                                          item.config))


def get_all_versions(item):
    logger.info()

    itemlist = []

    # Lee la versión local
    from core import updater
    from core import versiontools

    # Descarga la lista de versiones
    from core import api
    api_response = api.plugins_get_all_packages()

    if api_response["error"]:
        platformtools.dialog_ok("Error", "Se ha producido un error al descargar la lista de versiones")
        return

    for entry in api_response["body"]:

        if entry["package"]=="plugin":
            title = "pelisalacarta "+entry["tag"]+" (Publicada "+entry["date"]+")"
            local_version_number = versiontools.get_current_plugin_version()
        elif entry["package"]=="channels":
            title = "Canales (Publicada "+entry["date"]+")"
            local_version_number = versiontools.get_current_channels_version()
        elif entry["package"]=="servers":
            title = "Servidores (Publicada "+entry["date"]+")"
            local_version_number = versiontools.get_current_servers_version()
        else:
            title = entry["package"]+" (Publicada "+entry["date"]+")"
            local_version_number = None

        title_color = ""

        if local_version_number is None:
            title = title

        elif entry["version"] == local_version_number:
            title = title + " ACTUAL"

        elif entry["version"] > local_version_number:
            title_color = "yellow"

        else:
            title_color = "0xFF666666"

        itemlist.append(Item(channel=CHANNELNAME, title=title, url=entry["url"],
                             filename=entry["filename"], package=entry["package"],
                             version=str(entry["version"]), text_color=title_color,
                             action="download_and_install_package", folder=False))

    return itemlist


def download_and_install_package(item):
    logger.info()

    from core import updater
    from core import versiontools

    if item.package=="plugin":
        if int(item.version)<versiontools.get_current_plugin_version():
            if not platformtools.dialog_yesno("Instalando versión anterior","¿Seguro que quieres instalar una versión anterior?"):
                return
        elif int(item.version)==versiontools.get_current_plugin_version():
            if not platformtools.dialog_yesno("Reinstalando versión actual","¿Seguro que quieres reinstalar la misma versión que ya tienes?"):
                return
        elif int(item.version)>versiontools.get_current_plugin_version():
            if not platformtools.dialog_yesno("Instalando nueva versión","¿Seguro que quieres instalar esta nueva versión?"):
                return
    else:
        if not platformtools.dialog_yesno("Instalando paquete","¿Seguro que quieres instalar este paquete?"):
            return

    local_file_name = os.path.join( config.get_data_path() , item.filename)
    updater.download_and_install(item.url,local_file_name)

    if config.is_xbmc() and config.get_system_platform() != "xbox":
        import xbmc
        xbmc.executebuiltin("Container.Refresh")


def settings(item):
    config.open_settings()


def menu_addchannels(item):
    logger.info()
    itemlist = list()
    itemlist.append(Item(channel=CHANNELNAME, title="# Copia de seguridad automática en caso de sobrescritura",
                         action="", text_color="green"))
    itemlist.append(Item(channel=CHANNELNAME, title="Añadir o actualizar canal", action="addchannel", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Añadir o actualizar conector", action="addchannel", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Mostrar ruta de carpeta para copias de seguridad",
                         action="backups", folder=False))
    itemlist.append(Item(channel=CHANNELNAME, title="Eliminar copias de seguridad guardadas", action="backups",
                         folder=False))

    return itemlist


def addchannel(item):
    import os
    import time
    logger.info()

    tecleado = platformtools.dialog_input("", "Introduzca la URL")
    if not tecleado:
        return
    logger.info("url=%s" % tecleado)

    local_folder = config.get_runtime_path()
    if "canal" in item.title:
        local_folder = filetools.join(local_folder, 'channels')
        folder_to_extract = "channels"
        info_accion = "canal"
    else:
        local_folder = filetools.join(local_folder, 'servers')
        folder_to_extract = "servers"
        info_accion = "conector"

    # Detecta si es un enlace a un .py o .xml (pensado sobre todo para enlaces de github)
    try:
        extension = tecleado.rsplit(".", 1)[1]
    except:
        extension = ""

    files = []
    zip = False
    if extension == "py" or extension == "xml":
        filename = tecleado.rsplit("/", 1)[1]
        localfilename = filetools.join(local_folder, filename)
        files.append([tecleado, localfilename, filename])
    else:
        import re
        from core import scrapertools
        # Comprueba si la url apunta a una carpeta completa (channels o servers) de github
        if re.search(r'https://github.com/[^\s]+/'+folder_to_extract, tecleado):
            try:
                data = scrapertools.downloadpage(tecleado)
                matches = scrapertools.find_multiple_matches(data,
                                                             '<td class="content">.*?href="([^"]+)".*?title="([^"]+)"')
                for url, filename in matches:
                    url = "https://raw.githubusercontent.com" + url.replace("/blob/", "/")
                    localfilename = filetools.join(local_folder, filename)
                    files.append([url, localfilename, filename])
            except:
                import traceback
                logger.info("Detalle del error: %s" % traceback.format_exc())
                platformtools.dialog_ok("Error", "La url no es correcta o no está disponible")
                return
        else:
            filename = 'new%s.zip' % info_accion
            localfilename = filetools.join(config.get_data_path(), filename)
            files.append([tecleado, localfilename, filename])
            zip = True

    logger.info("localfilename=%s" % localfilename)
    logger.info("descarga fichero...")

    try:
        if len(files) > 1:
            lista_opciones = ["No", "Sí", "Sí (Sobrescribir todos)"]
            overwrite_all = False
        from core import downloadtools
        for url, localfilename, filename in files:
            result = downloadtools.downloadfile(url, localfilename, continuar=False, resumir=False)
            if result == -3:
                if len(files) == 1:
                    dyesno = platformtools.dialog_yesno("El archivo ya existe", "Ya existe el %s %s. "
                                                                                "¿Desea sobrescribirlo?" %
                                                        (info_accion, filename))
                else:
                    if not overwrite_all:
                        dyesno = platformtools.dialog_select("El archivo %s ya existe, ¿desea sobrescribirlo?"
                                                             % filename, lista_opciones)
                    else:
                        dyesno = 1
                # Diálogo cancelado
                if dyesno == -1:
                    return
                # Caso de carpeta github, opción sobrescribir todos
                elif dyesno == 2:
                    overwrite_all = True
                elif dyesno:
                    hora_folder = "Copia seguridad [%s]" % time.strftime("%d-%m_%H-%M", time.localtime())
                    backup = filetools.join(config.get_data_path(), 'backups', hora_folder, folder_to_extract)
                    if not filetools.exists(backup):
                        os.makedirs(backup)
                    import shutil
                    shutil.copy2(localfilename, filetools.join(backup, filename))
                    downloadtools.downloadfile(url, localfilename, continuar=True, resumir=False)
                else:
                    if len(files) == 1:
                        return
                    else:
                        continue
    except:
        import traceback
        logger.info("Detalle del error: %s" % traceback.format_exc())
        return

    if zip:
        try:
            # Lo descomprime
            logger.info("descomprime fichero...")
            from core import ziptools
            unzipper = ziptools.ziptools()
            logger.info("destpathname=%s" % local_folder)
            unzipper.extract(localfilename, local_folder, folder_to_extract, True, True)
        except:
            import traceback
            logger.error("Detalle del error: %s" % traceback.format_exc())
            # Borra el zip descargado
            filetools.remove(localfilename)
            platformtools.dialog_ok("Error", "Se ha producido un error extrayendo el archivo")
            return

        # Borra el zip descargado
        logger.info("borra fichero...")
        filetools.remove(localfilename)
        logger.info("...fichero borrado")

    platformtools.dialog_ok("Éxito", "Actualización/Instalación realizada correctamente")


def backups(item):
    logger.info()

    ruta = filetools.join(config.get_data_path(), 'backups')
    ruta_split = ""
    if "ruta" in item.title:
        heading = "Ruta de copias de seguridad"
        if not filetools.exists(ruta):
            folders = "Carpeta no creada"
        else:
            folders = str(len(filetools.listdir(ruta))) + " copia/s de seguridad guardadas"
        if len(ruta) > 55:
            ruta_split = ruta[55:]
            ruta = ruta[:55]
        platformtools.dialog_ok(heading, ruta, ruta_split, folders)
    else:
        if not filetools.exists(ruta):
            platformtools.dialog_ok("La carpeta no existe", "No hay copias de seguridad guardadas")
        else:
            dyesno = platformtools.dialog_yesno("Las copias de seguridad se eliminarán", "¿Está seguro?")
            if dyesno:
                import shutil
                shutil.rmtree(ruta, ignore_errors=True)


def get_thumbnail_path(thumb_name):
    import urlparse
    web_path = "http://media.tvalacarta.info/pelisalacarta/squares/"
    return urlparse.urljoin(web_path, thumb_name)


def submenu_tools(item):
    logger.info()
    itemlist = []

    itemlist.append(Item(channel=CHANNELNAME, title="Herramientas de canales", action="",
                         folder=False, thumbnail=get_thumbnail_path("thumb_canales.png")))
    itemlist.append(Item(channel=CHANNELNAME, title="   Comprobar archivos *_data.json",
                         action="conf_tools", folder=True, extra="lib_check_datajson",
                         thumbnail=get_thumbnail_path("thumb_canales.png")))

    if config.get_library_support():
        itemlist.append(Item(channel=CHANNELNAME, title="Herramientas de biblioteca", action="",
                             folder=False, thumbnail=get_thumbnail_path("thumb_biblioteca.png")))
        itemlist.append(Item(channel=CHANNELNAME, action="overwrite_tools", folder=False,
                             thumbnail=get_thumbnail_path("thumb_biblioteca.png"),
                             title="   Sobreescribir toda la biblioteca (strm, nfo y json)"))

    return itemlist


def conf_tools(item):
    logger.info()

    # Activar o desactivar canales
    if item.extra == "channels_onoff":
        import channelselector
        from core import channeltools

        channel_list = channelselector.filterchannels("allchannelstatus")

        channel_language = config.get_setting("channel_language")
        if channel_language == "":
            channel_language = "all"

        excluded_channels = ['tengourl',
                             'buscador',
                             'libreria',
                             'configuracion',
                             'novedades',
                             'personal',
                             'ayuda',
                             'descargas']

        list_controls = []
        try:
            list_controls.append({'id': "all_channels",
                                  'type': "list",
                                  'label': "Todos los canales",
                                  'default': 0,
                                  'enabled': True,
                                  'visible': True,
                                  'lvalues': ['',
                                              'Activar todos',
                                              'Desactivar todos',
                                              'Establecer estado por defecto']})

            for channel in channel_list:
                # Si el canal esta en la lista de exclusiones lo saltamos
                if channel.channel not in excluded_channels:
                    # Se cargan los ajustes del archivo json del canal
                    jsonchannel = channeltools.get_channel_json(channel.channel)
                    if jsonchannel.get("settings") or jsonchannel.get("active"):
                        channel_parameters = channeltools.get_channel_parameters(channel.channel)

                        # No incluir si es un canal para adultos, y el modo adulto está desactivado
                        if (channel_parameters["adult"] == "true" and
                                config.get_setting("adult_mode") == "false"):
                            continue

                        # No incluir si el canal es en un idioma filtrado
                        if (channel_language != "all" and
                                channel_parameters["language"] != channel_language):
                            continue

                        status = None
                        xml_status = channel_parameters["active"].replace("t", "T").replace("f", "F")
                        xml_status = eval(xml_status)

                        if config.get_setting("enabled", channel.channel):
                            status = config.get_setting("enabled", channel.channel)
                            status = status.replace("t", "T").replace("f", "F")
                            status = eval(status)
                            # logger.info(channel.channel + " | Status: " + str(status))
                        else:
                            status = xml_status
                            # logger.info(channel.channel + " | Status (XML): " + str(status))

                        status_control = ""
                        if not xml_status:
                            status_control = " [COLOR grey](Desactivado por defecto)[/COLOR]"

                        if status is not None:
                            control = {'id': channel.channel,
                                       'type': "bool",
                                       'label': channel_parameters["title"] + status_control,
                                       'default': status,
                                       'enabled': True,
                                       'visible': True}
                            list_controls.append(control)

                    else:
                        logger.info("Algo va mal con el canal " + channel.channel)
                else:
                    continue

            return platformtools.show_channel_settings(list_controls=list_controls,
                                                       caption="Canales",
                                                       callback="channel_status",
                                                       custom_button={"visible": False})
        except:
            import traceback
            logger.info(channel.title + " | Detalle del error: %s" % traceback.format_exc())
            platformtools.dialog_notification("Error",
                                              "Se ha producido un error con el canal %s" %
                                              channel.title)

    # Comprobacion de archivos channel_data.json
    elif item.extra == "lib_check_datajson":
        itemlist = []
        import channelselector
        from core import channeltools
        channel_list = channelselector.filterchannels("allchannelstatus")

        # Tener una lista de exclusion no tiene mucho sentido por que se comprueba si
        # el xml tiene "settings", pero por si acaso se deja
        excluded_channels = ['tengourl',
                             'configuracion',
                             'personal',
                             'ayuda']

        try:
            import os
            from core import jsontools
            for channel in channel_list:

                needsfix = None
                list_status = None
                list_controls = None
                default_settings = None
                channeljson_exists = None

                # Se convierte el "channel.channel" del canal biblioteca para que no de error
                if channel.channel == "libreria":
                    channel.channel = "biblioteca"

                # Se comprueba si el canal esta en la lista de exclusiones
                if channel.channel not in excluded_channels:
                    # Se comprueba que tenga "settings", sino se salta
                    jsonchannel = channeltools.get_channel_json(channel.channel)
                    if not jsonchannel.get("settings"):
                        itemlist.append(Item(channel=CHANNELNAME,
                                             title=channel.title + " - No tiene ajustes por defecto",
                                             action="", folder=False,
                                             thumbnail=channel.thumbnail))
                        continue
                        # logger.info(channel.channel + " SALTADO!")

                    # Se cargan los ajustes del archivo json del canal
                    file_settings = os.path.join(config.get_data_path(), "settings_channels",
                                                 channel.channel + "_data.json")
                    dict_settings = {}
                    dict_file = {}
                    if filetools.exists(file_settings):
                        # logger.info(channel.channel + " Tiene archivo _data.json")
                        channeljson_exists = "true"
                        # Obtenemos configuracion guardada de ../settings/channel_data.json
                        try:
                            dict_file = jsontools.load_json(open(file_settings, "rb").read())
                            if isinstance(dict_file, dict) and 'settings' in dict_file:
                                dict_settings = dict_file['settings']
                        except EnvironmentError:
                            logger.info("ERROR al leer el archivo: %s" % file_settings)
                    else:
                        # logger.info(channel.channel + " No tiene archivo _data.json")
                        channeljson_exists = "false"

                    if channeljson_exists == "true":
                        try:
                            datajson_size = filetools.getsize(file_settings)
                        except:
                            import traceback
                            logger.info(channel.title +
                                        " | Detalle del error: %s" % traceback.format_exc())
                    else:
                        datajson_size = None

                    # Si el _data.json esta vacio o no existe...
                    if (len(dict_settings) and datajson_size) == 0 or channeljson_exists == "false":
                        # Obtenemos controles del archivo ../channels/channel.xml
                        needsfix = "true"
                        try:
                            # Se cargan los ajustes por defecto
                            list_controls, default_settings = channeltools.get_channel_controls_settings(channel.channel)
                            # logger.info(channel.title + " | Default: %s" % default_settings)
                        except:
                            import traceback
                            logger.info(channel.title + " | Detalle del error: %s" % traceback.format_exc())
                            # default_settings = {}

                        # Si _data.json necesita ser reparado o no existe...
                        if needsfix == "true" or channeljson_exists == "false":
                            if default_settings is not None:
                                # Creamos el channel_data.json
                                default_settings.update(dict_settings)
                                dict_settings = default_settings
                                dict_file['settings'] = dict_settings
                                # Creamos el archivo ../settings/channel_data.json
                                json_data = jsontools.dump_json(dict_file)
                                try:
                                    open(file_settings, "wb").write(json_data)
                                    # logger.info(channel.channel + " - Archivo _data.json GUARDADO!")
                                    # El channel_data.json se ha creado/modificado
                                    list_status = " - [COLOR red] CORREGIDO!![/COLOR]"
                                except EnvironmentError:
                                    logger.info("ERROR al salvar el archivo: %s" % file_settings)
                            else:
                                if default_settings is None:
                                    list_status = " - [COLOR red] Imposible cargar los ajustes por defecto![/COLOR]"

                    else:
                        # logger.info(channel.channel + " - NO necesita correccion!")
                        needsfix = "false"

                    # Si se ha establecido el estado del canal se añade a la lista
                    if needsfix is not None:
                        if needsfix == "true":
                            if channeljson_exists == "false":
                                list_status = " - Ajustes creados"
                                list_colour = "red"
                            else:
                                list_status = " - No necesita correccion"
                                list_colour = "green"
                        else:
                            # Si "needsfix" es "false" y "datjson_size" es None habra
                            # ocurrido algun error
                            if datajson_size is None:
                                list_status = " - Ha ocurrido algun error"
                                list_colour = "red"
                            else:
                                list_status = " - No necesita correccion"
                                list_colour = "green"

                    if list_status is not None:
                        itemlist.append(Item(channel=CHANNELNAME,
                                             title=channel.title + list_status,
                                             action="", folder=False,
                                             thumbnail=channel.thumbnail,
                                             text_color=list_colour))
                    else:
                        logger.info("Algo va mal con el canal %s" % channel.channel)

                # Si el canal esta en la lista de exclusiones lo saltamos
                else:
                    continue
        except:
            import traceback
            logger.info(channel.title + " | Detalle del error: %s" % traceback.format_exc())
            platformtools.dialog_notification("Error",
                                              "Se ha producido un error con el canal %s" %
                                              channel.title)
        return itemlist

    else:
        platformtools.dialog_notification("pelisalacarta", "Error!")
        platformtools.itemlist_update(Item(channel=CHANNELNAME, action="submenu_tools"))


def channel_status(item, dict_values):
    try:
        for v in dict_values:

            if v == "all_channels":
                import channelselector
                from core import channeltools
                logger.info("Todos los canales | Estado seleccionado: %s" %
                            str(dict_values[v]).lower())
                if str(dict_values[v]) != "0":
                    channel_list = channelselector.filterchannels("allchannelstatus")
                    excluded_channels = ['tengourl', 'buscador',
                                         'libreria', 'configuracion',
                                         'novedades', 'personal',
                                         'ayuda', 'descargas']
                    for channel in channel_list:
                        if channel.channel not in excluded_channels:
                            channel_parameters = channeltools.get_channel_parameters(channel.channel)
                            new_status_all_default = None
                            new_status_all = None
                            new_status_all_default = channel_parameters["active"]

                            # Opcion Activar todos
                            if str(dict_values[v]) == "1":
                                new_status_all = "true"

                            # Opcion Desactivar todos
                            if str(dict_values[v]) == "2":
                                new_status_all = "false"

                            # Opcion Recuperar estado por defecto
                            if str(dict_values[v]) == "3":
                                # Si tiene "enabled" en el json es porque el estado no es el del xml
                                if config.get_setting("enabled", channel.channel):
                                    new_status_all = new_status_all_default

                                # Si el canal no tiene "enabled" en el json no se guarda, se pasa al siguiente
                                else:
                                    continue

                            # Se guarda el estado del canal
                            if new_status_all is not None:
                                config.set_setting("enabled", new_status_all, channel.channel)
                    break
                else:
                    continue

            else:
                logger.info("Canal: %s | Estado: %s" %
                            (v, str(dict_values[v]).lower()))
                config.set_setting("enabled", str(dict_values[v]).lower(), v)

        platformtools.itemlist_update(Item(channel=CHANNELNAME, action="mainlist"))

    except:
        import traceback
        logger.info("Detalle del error: %s" % traceback.format_exc())
        platformtools.dialog_notification("Error",
                                          "Se ha producido un error al guardar")


def overwrite_tools(item):
    import library_service
    from core import library


    seleccion = platformtools.dialog_yesno("Sobrescribir toda la biblioteca",
                                           "Esto puede llevar algun tiempo.",
                                           "¿Desea continuar?")
    if seleccion == 1:
        heading = 'Sobrescribiendo biblioteca....'
        p_dialog = platformtools.dialog_progress_bg('pelisalacarta', heading)
        p_dialog.update(0, '')
        show_list = []

        for path, folders, files in filetools.walk(library.TVSHOWS_PATH):
            show_list.extend([filetools.join(path, f) for f in files if f == "tvshow.nfo"])

        if show_list:
            t = float(100) / len(show_list)


        for i, tvshow_file in enumerate(show_list):
            head_nfo, serie = library.read_nfo(tvshow_file)
            path = filetools.dirname(tvshow_file)

            if not serie.active:
                # si la serie no esta activa descartar
                continue

            # Eliminamos la carpeta con la serie ...
            filetools.rmdirtree(path)

            # ... y la volvemos a añadir
            library_service.update(path, p_dialog, i, t, serie, 3)


        p_dialog.close()
