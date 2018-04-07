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
# filter_tools - se encarga de filtrar resultados
# ------------------------------------------------------------

import os

from core import config
from core import filetools
from core import jsontools
from core import logger
from core.item import Item
from platformcode import platformtools

TAG_TVSHOW_FILTER = "TVSHOW_FILTER"
TAG_NAME = "name"
TAG_ACTIVE = "active"
TAG_LANGUAGE = "language"
TAG_QUALITY_NOT_ALLOWED = "quality_not_allowed"

COLOR = {"parent_item": "yellow", "error": "red", "striped_even_active": "blue",
         "striped_even_inactive": "0xff00bfff", "striped_odd_active": "0xff008000",
         "striped_odd_inactive": "0xff00fa9a", "selected": "blue"
         }


class Filter:
    active = False
    language = ""
    quality_not_allowed = ""

    def __init__(self, dict_filter):
        self.active = dict_filter[TAG_ACTIVE]
        self.language = dict_filter[TAG_LANGUAGE]
        self.quality_not_allowed = dict_filter[TAG_QUALITY_NOT_ALLOWED]

# TODO echar un ojo a https://pyformat.info/, se puede formatear el estilo y hacer referencias directamente a elementos

__channel__ = "filtertools"


def context():
    _context = ""
    '''
    configuración para mostrar la opción de filtro, actualmente sólo se permite en xbmc, se cambiará cuando
    'platformtools.show_channel_settings' esté disponible para las distintas plataformas
    '''
    if config.is_xbmc() or config.get_platform() == "mediaserver":
        _context = [{"title": "Menu Filtro",
                     "action": "config_item",
                     "channel": "filtertools"}]

    # elif command == "guardar_filtro":
    # context_commands.append(("Guardar Filtro Serie", "XBMC.RunPlugin(%s?%s)" % (sys.argv[0], item.clone(
    #     channel="filtertools",
    #     action="save_filter",
    #     from_channel=item.channel
    # ).tourl())))
    #
    # elif command == "borrar_filtro":
    #     context_commands.append(("Eliminar Filtro", "XBMC.RunPlugin(%s?%s)" % (sys.argv[0], item.clone(
    #         channel="filtertools",
    #         action="del_filter",
    #         from_channel=item.channel
    #     ).tourl())))

    return _context

context = context()


def show_option(itemlist, channel, list_idiomas, list_calidad):

    itemlist.append(Item(channel=__channel__, title="[COLOR {0}]Configurar filtro para series...[/COLOR]".
                         format(COLOR.get("parent_item", "auto")),
                         action="load", list_idiomas=list_idiomas, list_calidad=list_calidad, from_channel=channel))

    return itemlist


def load(item):
    return mainlist(channel=item.from_channel, list_idiomas=item.list_idiomas, list_calidad=item.list_calidad)


def get_links(list_item, channel):
    """
    Devuelve una lista de enlaces filtrados.

    :param list_item: lista de enlaces
    :type list_item: list[Item]
    :param channel: nombre del canal a filtrar
    :type channel: str
    :return: lista de Item
    :rtype: list[Item]
    """
    logger.info()

    logger.debug("total de items : {0}".format(len(list_item)))

    new_itemlist = []
    quality_count = 0
    language_count = 0
    _filter = None

    dict_filtered_shows = get_tvshows(channel)
    tvshow = list_item[0].show.lower().strip()
    if tvshow in dict_filtered_shows.keys():
        _filter = Filter(dict_filtered_shows[tvshow])

    if _filter and _filter.active:
        logger.debug("filter datos: {0}".format(_filter))

        for item in list_item:

            is_language_valid = True
            if _filter.language:

                # viene de episodios
                if "[" in item.language:
                    list_language = item.language.replace("[", "").replace("]", "").split(" ")
                    if _filter.language in list_language:
                        language_count += 1
                    else:
                        is_language_valid = False
                # viene de findvideos
                else:
                    if item.language.lower() == _filter.language.lower():
                        language_count += 1
                    else:
                        is_language_valid = False

            is_quality_valid = True
            quality = ""

            if _filter.quality_not_allowed:
                if hasattr(item, 'quality'):
                    if item.quality.lower() not in _filter.quality_not_allowed:
                        quality_count += 1
                    else:
                        is_quality_valid = False

            if is_language_valid and is_quality_valid:
                new_item = item.clone(channel=channel)
                new_itemlist.append(new_item)
                logger.debug("{0} | context: {1}".format(item.title, item.context))
                logger.debug(" -Enlace añadido")

            logger.debug(" idioma valido?: {0}, item.language: {1}, filter.language: {2}"
                         .format(is_language_valid, item.language, _filter.language))
            logger.debug(" calidad valida?: {0}, item.quality: {1}, filter.quality_not_allowed: {2}"
                         .format(is_quality_valid, quality, _filter.quality_not_allowed))

        logger.info("ITEMS FILTRADOS: {0}/{1}, idioma[{2}]:{3}, calidad_no_permitida{4}:{5}"
                    .format(len(new_itemlist), len(list_item), _filter.language, language_count,
                            _filter.quality_not_allowed, quality_count))

        if len(new_itemlist) == 0:
            lista = []
            for i in list_item:
                lista.append(i.tourl())

            new_itemlist.append(Item(channel=__channel__, action="no_filter", lista=lista, show=list_item[0].show,
                                     title="[COLOR {0}]No hay elementos con filtro [{1}] y ![{2}], pulsa para mostrar "
                                           "sin filtro[/COLOR]"
                                     .format(COLOR.get("error", "auto"), _filter.language, _filter.quality_not_allowed),
                                     context="borrar filtro", from_channel=channel))

    else:
        new_itemlist = list_item

    return new_itemlist


def no_filter(item):
    """
    Muestra los enlaces sin filtrar

    :param item: item
    :type item: Item
    :return: liasta de enlaces
    :rtype: list[Item]
    """
    logger.info()

    lista = []
    for i in item.lista:
        lista.append(Item().fromurl(i))

    return lista


def get_tvshows(from_channel):
    """
    Obtiene las series filtradas de un canal

    :param from_channel: canal que tiene las series filtradas
    :type from_channel: str
    :return: dict con las series
    :rtype: dict
    """
    logger.info()
    dict_series = {}
    name_file = from_channel

    if not os.path.exists(os.path.join(config.get_data_path(), "settings_channels")):
        os.mkdir(os.path.join(config.get_data_path(), "settings_channels"))

    fname = os.path.join(config.get_data_path(), "settings_channels", name_file + "_data.json")

    data = filetools.read(fname)
    dict_data = jsontools.load_json(data)

    check_json_file(data, fname, dict_data)

    if TAG_TVSHOW_FILTER in dict_data:
        dict_series = dict_data[TAG_TVSHOW_FILTER]

    logger.debug("json_series: {0}".format(dict_series))

    return dict_series


def check_json_file(data, fname, dict_data):
    """
    Comprueba que si dict_data(conversion del fichero JSON a dict) no es un diccionario, se genere un fichero con
    data de nombre fname.bk.

    :param data: contenido del fichero fname
    :type data: str
    :param fname: nombre del fichero leido
    :type fname: str
    :param dict_data: nombre del diccionario
    :type dict_data: dict
    """
    logger.info()
    if not dict_data:
        logger.error("Error al cargar el json del fichero {0}".format(fname))

        if data != "":
            # se crea un nuevo fichero
            title = filetools.write("{0}.bk".format(fname), data)
            if title != "":
                logger.error("Ha habido un error al guardar el fichero: {0}.bk"
                             .format(fname))
            else:
                logger.debug("Se ha guardado una copia con el nombre: {0}.bk"
                             .format(fname))
        else:
            logger.debug("Está vacío el fichero: {0}".format(fname))


def mainlist(channel, list_idiomas, list_calidad):
    """
    Muestra una lista de las series filtradas

    :param channel: nombre del canal para obtener las series filtradas
    :type channel: str
    :param list_idiomas: lista de idiomas del canal
    :type list_idiomas: list
    :param list_calidad: lista de calidades del canal
    :type list_calidad: list
    :return: lista de Item
    :rtype: list[Item]
    """
    logger.info()
    itemlist = []
    dict_series = get_tvshows(channel)

    idx = 0
    for tvshow in sorted(dict_series):

        if idx % 2 == 0:
            if dict_series[tvshow][TAG_ACTIVE]:
                tag_color = COLOR.get("striped_even_active", "auto")
            else:
                tag_color = COLOR.get("striped_even_inactive", "auto")
        else:
            if dict_series[tvshow][TAG_ACTIVE]:
                tag_color = COLOR.get("striped_odd_active", "auto")
            else:
                tag_color = COLOR.get("striped_odd_inactive", "auto")

        idx += 1
        name = dict_series.get(tvshow, {}).get(TAG_NAME, tvshow)
        activo = " (desactivado)"
        if dict_series[tvshow][TAG_ACTIVE]:
            activo = ""
        title = "Configurar [COLOR {0}][{1}][/COLOR]{2}".format(tag_color, name, activo)

        itemlist.append(Item(channel=__channel__, action="config_item", title=title, show=name,
                             list_idiomas=list_idiomas, list_calidad=list_calidad, from_channel=channel))

    if len(itemlist) == 0:
        itemlist.append(Item(channel=channel, action="mainlist",
                             title="No existen filtros, busca una serie y pulsa en menú contextual 'Menu Filtro'"))

    return itemlist


def config_item(item):
    """
    muestra una serie filtrada para su configuración

    :param item: item
    :type item: Item
    """
    logger.info()
    logger.info("item {0}".format(item.tostring()))

    # OBTENEMOS LOS DATOS DEL JSON
    dict_series = get_tvshows(item.from_channel)

    tvshow = item.show.lower().strip()

    lang_selected = dict_series.get(tvshow, {}).get(TAG_LANGUAGE, 'Español')
    list_quality = dict_series.get(tvshow, {}).get(TAG_QUALITY_NOT_ALLOWED, "")
    # logger.info("lang selected {}".format(lang_selected))
    # logger.info("list quality {}".format(list_quality))

    active = True
    custom_button = {'visible': False}
    allow_option = False
    if item.show.lower().strip() in dict_series:
        allow_option = True
        active = dict_series.get(item.show.lower().strip(), {}).get(TAG_ACTIVE, False)
        custom_button = {'label': 'Borrar', 'function': 'borrar_filtro', 'visible': True, 'close': True}

    list_controls = []

    if allow_option:
        active_control = {
            "id": "active",
            "type": "bool",
            "label": "¿Activar/Desactivar filtro?",
            "color": "",
            "default": active,
            "enabled": allow_option,
            "visible": allow_option,
        }
        list_controls.append(active_control)

    language_option = {
        "id": "language",
        "type": "list",
        "label": "Idioma",
        "color": "0xFFee66CC",
        "default": item.list_idiomas.index(lang_selected),
        "enabled": True,
        "visible": True,
        "lvalues": item.list_idiomas
    }
    list_controls.append(language_option)

    if item.list_calidad:
        list_controls_calidad = [
            {
                "id": "textoCalidad",
                "type": "label",
                "label": "Calidad NO permitida",
                "color": "0xffC6C384",
                "enabled": True,
                "visible": True,
            },
        ]
        for element in sorted(item.list_calidad, key=str.lower):
            list_controls_calidad.append({
                "id": element,
                "type": "bool",
                "label": element,
                "default": (False, True)[element.lower() in list_quality],
                "enabled": True,
                "visible": True,
            })

        # concatenamos list_controls con list_controls_calidad
        list_controls.extend(list_controls_calidad)

    title = "Filtrado de enlaces para: [COLOR {0}]{1}[/COLOR]".format(COLOR.get("selected", "auto"), item.show)

    platformtools.show_channel_settings(list_controls=list_controls, callback='guardar_valores', item=item,
                                        caption=title, custom_button=custom_button)


def borrar_filtro(item):
    logger.info()
    if item:
        # OBTENEMOS LOS DATOS DEL JSON
        dict_series = get_tvshows(item.from_channel)
        tvshow = item.show.strip().lower()

        heading = "¿Está seguro que desea eliminar el filtro?"
        line1 = "Pulse 'Si' para eliminar el filtro de [COLOR {0}]{1}[/COLOR], pulse 'No' o cierre la ventana para " \
                "no hacer nada.".format(COLOR.get("selected", "auto"), item.show.strip())

        if platformtools.dialog_yesno(heading, line1) == 1:
            lang_selected = dict_series.get(tvshow, {}).get(TAG_LANGUAGE, "")
            dict_series.pop(tvshow, None)

            fname, json_data = update_json_data(dict_series, item.from_channel)
            result = filetools.write(fname, json_data)

            if result:
                message = "FILTRO ELIMINADO"
            else:
                message = "Error al guardar en disco"

            heading = "{0} [{1}]".format(item.show.strip(), lang_selected)
            platformtools.dialog_notification(heading, message)

            if config.get_platform() == "mediaserver":
                platformtools.itemlist_refresh()


def guardar_valores(item, dict_data_saved):
    """
    Guarda los valores configurados en la ventana

    :param item: item
    :type item: Item
    :param dict_data_saved: diccionario con los datos salvados
    :type dict_data_saved: dict
    """
    logger.info()
    # Aqui tienes q gestionar los datos obtenidos del cuadro de dialogo
    if item and dict_data_saved:
        logger.debug('item: {0}\ndatos: {1}'.format(item.tostring(), dict_data_saved))

        # OBTENEMOS LOS DATOS DEL JSON
        if item.from_channel == "biblioteca":
            item.from_channel = item.contentChannel
        dict_series = get_tvshows(item.from_channel)
        tvshow = item.show.strip().lower()

        logger.info("Se actualiza los datos")

        list_quality = []
        for _id, value in dict_data_saved.items():
            if _id in item.list_calidad and value:
                    list_quality.append(_id.lower())

        lang_selected = item.list_idiomas[dict_data_saved[TAG_LANGUAGE]]
        dict_filter = {TAG_NAME: item.show, TAG_ACTIVE: dict_data_saved.get(TAG_ACTIVE, True),
                       TAG_LANGUAGE: lang_selected, TAG_QUALITY_NOT_ALLOWED: list_quality}
        dict_series[tvshow] = dict_filter

        fname, json_data = update_json_data(dict_series, item.from_channel)
        result = filetools.write(fname, json_data)

        if result:
            message = "FILTRO GUARDADO"
        else:
            message = "Error al guardar en disco"

        heading = "{0} [{1}]".format(item.show.strip(), lang_selected)
        platformtools.dialog_notification(heading, message)

        if config.get_platform() == "mediaserver":
            platformtools.itemlist_refresh()


def update_json_data(dict_series, filename):
    """
    actualiza el json_data de un fichero con el diccionario pasado

    :param dict_series: diccionario con las series
    :type dict_series: dict
    :param filename: nombre del fichero para guardar
    :type filename: str
    :return: fname, json_data
    :rtype: str, dict
    """
    logger.info()
    if not os.path.exists(os.path.join(config.get_data_path(), "settings_channels")):
        os.mkdir(os.path.join(config.get_data_path(), "settings_channels"))
    fname = os.path.join(config.get_data_path(), "settings_channels", filename + "_data.json")
    data = filetools.read(fname)
    dict_data = jsontools.load_json(data)
    # es un dict
    if dict_data:
        if TAG_TVSHOW_FILTER in dict_data:
            logger.debug("   existe el key SERIES")
            dict_data[TAG_TVSHOW_FILTER] = dict_series
        else:
            logger.debug("   NO existe el key SERIES")
            new_dict = {TAG_TVSHOW_FILTER: dict_series}
            dict_data.update(new_dict)
    else:
        logger.debug("   NO es un dict")
        dict_data = {TAG_TVSHOW_FILTER: dict_series}
    json_data = jsontools.dump_json(dict_data)
    return fname, json_data


# TODO PENDIENTE DE ARREGLAR

# def save_filter(item):
#     """
#     salva el filtro a través del menú contextual
#
#     :param item: item
#     :type item: item
#     """
#     logger.info("[filtertools.py] save_filter")
#
#     dict_series = get_filtered_tvshows(item.from_channel)
#
#     name = item.show.lower().strip()
#     logger.info("[filtertools.py] config_item name {0}".format(name))
#
#     open_tag_idioma = (0, item.title.find("[")+1)[item.title.find("[") >= 0]
#     close_tag_idioma = (0, item.title.find("]"))[item.title.find("]") >= 0]
#     idioma = item.title[open_tag_idioma: close_tag_idioma]
#
#     open_tag_calidad = (0, item.title.find("[", item.title.find("[") + 1)+1)[item.title.find("[", item.title.find("[") + 1) >= 0]
#     close_tag_calidad = (0, item.title.find("]", item.title.find("]") + 1))[item.title.find("]", item.title.find("]") + 1) >= 0]
#     calidad_no_permitida = ""  # item.title[open_tag_calidad: close_tag_calidad]
#
#     # filter_idioma = ""
#     # logger.info("idioma {0}".format(idioma))
#     # if idioma != "":
#     #     filter_idioma = [key for key, value in dict_idiomas.iteritems() if value == idioma][0]
#
#     list_calidad = list()
#
#     dict_filter = {TAG_NAME: item.show, TAG_ACTIVE: True, TAG_LANGUAGE: idioma, TAG_QUALITY_NOT_ALLOWED: list_calidad}
#     dict_series[name] = dict_filter
#
#     # filter_list = item.extra.split("##")
#     # dict_series = eval(filter_list[0])
#     # dict_filter = eval(filter_list[2])
#     # dict_series[filter_list[1].strip().lower()] = dict_filter
#     # logger.info("categoria {0}".format(item.from_channel))
#
#     fname, json_data = update_json_data(dict_series, item.from_channel)
#     result = filetools.write(fname, json_data)
#
#     if result:
#         message = "FILTRO GUARDADO"
#     else:
#         message = "Error al guardar en disco"
#
#     heading = "{0} [1]".format(item.show.strip(), idioma)
#     platformtools.dialog_notification(heading, message)
#
#
# def del_filter(item):
#     """
#     elimina el filtro a través del menú contextual
#
#     :param item: item
#     :type item: item
#     """
#     logger.info("[filtertools.py] del_filter")
#
#     dict_series = get_filtered_tvshows(item.from_channel)
#     dict_series.pop(item.show.lower().strip(), None)
#
#     fname, json_data = update_json_data(dict_series, item.from_channel)
#     result = filetools.write(fname, json_data)
#
#     if result:
#         message = "FILTRO ELIMINADO"
#     else:
#         message = "Error al guardar en disco"
#
#     heading = "{0}".format(item.show.strip())
#     platformtools.dialog_notification(heading, message)
