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
# channeltools - Herramientas para trabajar con canales
# ------------------------------------------------------------

import os

import config
import jsontools
import logger
import scrapertools

DEFAULT_UPDATE_URL = "https://raw.githubusercontent.com/tvalacarta/pelisalacarta/develop/python/main-classic/channels/"


def is_adult(channel_name):
    logger.info("channel_name="+channel_name)

    channel_parameters = get_channel_parameters(channel_name)

    return channel_parameters["adult"] == "true"


def get_channel_parameters(channel_name):
    # logger.info("pelisalacarta.core.channeltools get_channel_parameters channel_name="+channel_name)
    channel_xml = os.path.join(config.get_runtime_path(), 'channels', channel_name+".xml")

    if os.path.exists(channel_xml):
        # logger.info("channel_name+".xml found")

        infile = open(channel_xml, "rb")
        data = infile.read()
        infile.close()

        channel_parameters = dict()
        channel_parameters["title"] = scrapertools.find_single_match(data, "<name>([^<]*)</name>")
        channel_parameters["channel"] = scrapertools.find_single_match(data, "<id>([^<]*)</id>")
        channel_parameters["active"] = scrapertools.find_single_match(data, "<active>([^<]*)</active>")
        channel_parameters["adult"] = scrapertools.find_single_match(data, "<adult>([^<]*)</adult>")
        channel_parameters["language"] = scrapertools.find_single_match(data, "<language>([^<]*)</language>")
        # Imagenes: se admiten url y archivos locales dentro de "resources/images"
        channel_parameters["thumbnail"] = scrapertools.find_single_match(data, "<thumbnail>([^<]*)</thumbnail>")
        channel_parameters["bannermenu"] = scrapertools.find_single_match(data, "<bannermenu>([^<]*)</bannermenu>")
        channel_parameters["fanart"] = scrapertools.find_single_match(data, "<fanart>([^<]*)</fanart>")
        channel_parameters["update_url"] = scrapertools.find_single_match(data, "<update_url>([^<]*)</update_url>")

        if channel_parameters["thumbnail"] and "://" not in channel_parameters["thumbnail"]:
            channel_parameters["thumbnail"] = os.path.join(config.get_runtime_path(), "resources", "images", "squares",
                                                           channel_parameters["thumbnail"])
        if channel_parameters["bannermenu"] and "://" not in channel_parameters["bannermenu"]:
            channel_parameters["bannermenu"] = os.path.join(config.get_runtime_path(), "resources", "images",
                                                            "bannermenu", channel_parameters["bannermenu"])
        if channel_parameters["fanart"] and "://" not in channel_parameters["fanart"]:
            channel_parameters["fanart"] = os.path.join(config.get_runtime_path(), "resources", "images", "fanart",
                                                        channel_parameters["fanart"])

        if channel_parameters["update_url"] == "":
            channel_parameters["update_url"] = DEFAULT_UPDATE_URL

        channel_parameters["include_in_global_search"] = scrapertools.find_single_match(
            data, "<include_in_global_search>([^<]*)</include_in_global_search>")

        category_list = []
        matches = scrapertools.find_multiple_matches(data, "<category>([^<]*)</category>")
        for match in matches:
            category_list.append(match)

        channel_parameters["categories"] = category_list

        # Obtenemos si el canal tiene opciones de configuración
        channel_parameters["has_settings"] = False
        # esta regex devuelve 2 valores por elemento <settings>, el contenido del propio nodo y un \t, por lo que hay
        # posteriormente coger solo el valor del indice 0.
        matches = scrapertools.find_multiple_matches(data, "<settings>((.|\n)*?)<\/settings>")
        for match in matches:
            _id = scrapertools.find_single_match(match[0], "<id>([^<]*)</id>")
            if _id and "include_in_" not in _id:
                channel_parameters["has_settings"] = True
                break

        logger.info(channel_name+" -> "+repr(channel_parameters))

    else:
        logger.info(channel_name+".xml NOT found")

        channel_parameters = dict()
        channel_parameters["adult"] = "false"
        channel_parameters["update_url"] = DEFAULT_UPDATE_URL

    return channel_parameters


def get_channel_json(channel_name):
    # logger.info("channel_name="+channel_name)
    channel_xml = os.path.join(config.get_runtime_path(), 'channels', channel_name + ".xml")
    channel_json = jsontools.xmlTojson(channel_xml)
    return channel_json['channel']


def get_channel_controls_settings(channel_name):
    # logger.info("channel_name="+channel_name)
    dict_settings = {}
    list_controls = []

    settings = get_channel_json(channel_name)['settings']
    if type(settings) == list:
        list_controls = settings
    else:
        list_controls.append(settings)

    # Conversion de str a bool, etc...
    for c in list_controls:
        if 'id' not in c or 'type' not in c or 'default' not in c:
            # Si algun control de la lista  no tiene id, type o default lo ignoramos
            continue

        if 'enabled' not in c or c['enabled'] is None:
            c['enabled'] = True
        else:
            if c['enabled'].lower() == "true":
                c['enabled'] = True
            elif c['enabled'].lower() == "false":
                c['enabled'] = False

        if 'visible' not in c or c['visible'] is None:
            c['visible'] = True

        else:
            if c['visible'].lower() == "true":
                c['visible'] = True
            elif c['visible'].lower() == "false":
                c['visible'] = False

        if c['type'] == 'bool':
            c['default'] = (c['default'].lower() == "true")

        if unicode(c['default']).isnumeric():
            c['default'] = int(c['default'])

        dict_settings[c['id']] = c['default']

    return list_controls, dict_settings


def get_channel_setting(name, channel):
    """
    Retorna el valor de configuracion del parametro solicitado.

    Devuelve el valor del parametro 'name' en la configuracion propia del canal 'channel'.

    Si se especifica el nombre del canal busca en la ruta \addon_data\plugin.video.pelisalacarta\settings_channels el
    archivo channel_data.json y lee el valor del parametro 'name'. Si el archivo channel_data.json no existe busca en la
    carpeta channels el archivo channel.xml y crea un archivo channel_data.json antes de retornar el valor solicitado.


    @param name: nombre del parametro
    @type name: str
    @param channel: nombre del canal
    @type channel: str

    @return: El valor del parametro 'name'
    @rtype: str

    """
    # Creamos la carpeta si no existe
    if not os.path.exists(os.path.join(config.get_data_path(), "settings_channels")):
        os.mkdir(os.path.join(config.get_data_path(), "settings_channels"))

    file_settings = os.path.join(config.get_data_path(), "settings_channels", channel+"_data.json")
    dict_settings = {}
    dict_file = {}
    if os.path.exists(file_settings):
        # Obtenemos configuracion guardada de ../settings/channel_data.json
        try:
            dict_file = jsontools.load_json(open(file_settings, "rb").read())
            if isinstance(dict_file, dict) and 'settings' in dict_file:
                dict_settings = dict_file['settings']
        except EnvironmentError:
            logger.info("ERROR al leer el archivo: %s" % file_settings)

    if len(dict_settings) == 0 or name not in dict_settings:
        # Obtenemos controles del archivo ../channels/channel.xml
        try:
            list_controls, default_settings = get_channel_controls_settings(channel)
        except:
            default_settings = {}
        if name in default_settings:  # Si el parametro existe en el channel.xml creamos el channel_data.json
            default_settings.update(dict_settings)
            dict_settings = default_settings
            dict_file['settings'] = dict_settings
            # Creamos el archivo ../settings/channel_data.json
            json_data = jsontools.dump_json(dict_file)
            try:
                open(file_settings, "wb").write(json_data)
            except EnvironmentError:
                logger.info("ERROR al salvar el archivo: %s" % file_settings)

    # Devolvemos el valor del parametro local 'name' si existe
    if name in dict_settings:
        return dict_settings[name]
    else:
        return None


def set_channel_setting(name, value, channel):
    """
    Fija el valor de configuracion del parametro indicado.

    Establece 'value' como el valor del parametro 'name' en la configuracion propia del canal 'channel'.
    Devuelve el valor cambiado o None si la asignacion no se ha podido completar.

    Si se especifica el nombre del canal busca en la ruta \addon_data\plugin.video.pelisalacarta\settings_channels el
    archivo channel_data.json y establece el parametro 'name' al valor indicado por 'value'.
    Si el parametro 'name' no existe lo añade, con su valor, al archivo correspondiente.

    @param name: nombre del parametro
    @type name: str
    @param value: valor del parametro
    @type value: str
    @param channel: nombre del canal
    @type channel: str

    @return: 'value' en caso de que se haya podido fijar el valor y None en caso contrario
    @rtype: str, None

    """
    # Creamos la carpeta si no existe
    if not os.path.exists(os.path.join(config.get_data_path(), "settings_channels")):
        os.mkdir(os.path.join(config.get_data_path(), "settings_channels"))

    file_settings = os.path.join(config.get_data_path(), "settings_channels", channel+"_data.json")
    dict_settings = {}

    dict_file = None

    if os.path.exists(file_settings):
        # Obtenemos configuracion guardada de ../settings/channel_data.json
        try:
            dict_file = jsontools.load_json(open(file_settings, "r").read())
            dict_settings = dict_file.get('settings', {})
        except EnvironmentError:
            logger.info("ERROR al leer el archivo: %s" % file_settings)

    dict_settings[name] = value

    # comprobamos si existe dict_file y es un diccionario, sino lo creamos
    if dict_file is None or not dict_file:
        dict_file = {}

    dict_file['settings'] = dict_settings

    # Creamos el archivo ../settings/channel_data.json
    try:
        json_data = jsontools.dump_json(dict_file)
        open(file_settings, "w").write(json_data)
    except EnvironmentError:
        logger.info("ERROR al salvar el archivo: %s" % file_settings)
        return None

    return value


def get_channel_module(channel_name, package="channels"):
    # Sustituye al que hay en servertools.py ...
    # ...pero añade la posibilidad de incluir un paquete diferente de "channels"
    if not package.endswith('.'):
        package += '.'
    logger.info("Importando " + package + channel_name)
    channels_module = __import__(package + channel_name)
    channel_module = getattr(channels_module, channel_name)
    logger.info("Importado " + package + channel_name)

    return channel_module


def get_channel_remote_url(channel_name):

    channel_parameters = get_channel_parameters(channel_name)
    remote_channel_url = channel_parameters["update_url"]+channel_name+".py"
    remote_version_url = channel_parameters["update_url"]+channel_name+".xml" 

    logger.info("pelisalacarta.core.channeltools get_channel_remote_url remote_channel_url="+remote_channel_url)
    logger.info("pelisalacarta.core.channeltools get_channel_remote_url remote_version_url="+remote_version_url)
    
    return remote_channel_url, remote_version_url


def get_channel_local_path(channel_name):

    if channel_name != "channelselector":
        local_channel_path = os.path.join(config.get_runtime_path(), 'channels', channel_name + ".py")
        local_version_path = os.path.join(config.get_runtime_path(), 'channels', channel_name + ".xml")
        local_compiled_path = os.path.join(config.get_runtime_path(), 'channels', channel_name + ".pyo")
    else:
        local_channel_path = os.path.join(config.get_runtime_path(), channel_name + ".py")
        local_version_path = os.path.join(config.get_runtime_path(), channel_name + ".xml")
        local_compiled_path = os.path.join(config.get_runtime_path(), channel_name + ".pyo")

    logger.info("pelisalacarta.core.channeltools get_channel_local_path local_channel_path=" + local_channel_path)
    logger.info("pelisalacarta.core.channeltools get_channel_local_path local_version_path=" + local_version_path)
    logger.info("pelisalacarta.core.channeltools get_channel_local_path local_compiled_path=" + local_compiled_path)

    return local_channel_path, local_version_path, local_compiled_path
