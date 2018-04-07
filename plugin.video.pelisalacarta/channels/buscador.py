# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import glob
import os
import re
import time
from threading import Thread

from core import channeltools
from core import config
from core import logger
from core.item import Item
from platformcode import platformtools


def mainlist(item):
    logger.info()

    itemlist = list()
    context = [{"title": "Elegir canales incluidos",
                "action": "settingCanal",
                "channel": item.channel}]
    itemlist.append(Item(channel=item.channel, action="search",
                         title="Buscar por titulo", context=context,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="search",
                         title="Buscar por categorias (busqueda avanzada)", extra="categorias",
                         context=context,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    # itemlist.append(Item(channel=item.channel, action="opciones", title="Opciones"))

    saved_searches_list = get_saved_searches()
    context2 = context[:]
    context2.append({"title": "Borrar búsquedas guardadas",
                     "action": "clear_saved_searches",
                     "channel": item.channel})
    logger.info("saved_searches_list=%s" % saved_searches_list)
    if saved_searches_list != []:
        itemlist.append(Item(channel=item.channel, action="",
                             title="Busquedas guardadas:", context=context2,
                             thumbnail=get_thumbnail_path("thumb_buscar.png")))
        for saved_search_text in saved_searches_list:
            itemlist.append(Item(channel=item.channel, action="do_search",
                                 title='    "' + saved_search_text + '"',
                                 extra=saved_search_text, context=context2,
                                 category=saved_search_text,
                                 thumbnail=get_thumbnail_path("thumb_buscar.png")))

    return itemlist


def opciones(item):
    itemlist = list()
    itemlist.append(Item(channel=item.channel, action="settingCanal",
                         title="Elegir canales incluidos en la búsqueda",
                         folder=False, thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="clear_saved_searches",
                         title="Borrar búsquedas guardadas", folder=False,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    itemlist.append(Item(channel=item.channel, action="settings",
                         title="Otros ajustes", folder=False,
                         thumbnail=get_thumbnail_path("thumb_buscar.png")))
    return itemlist


def get_thumbnail_path(thumb_name):
    import urlparse
    web_path = "http://media.tvalacarta.info/pelisalacarta/squares/"
    return urlparse.urljoin(web_path, thumb_name)


def settings(item):
    return platformtools.show_channel_settings()


def settingCanal(item):
    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    channel_language = config.get_setting("channel_language")

    if channel_language == "":
        channel_language = "all"

    list_controls = []
    for infile in sorted(glob.glob(channels_path)):
        channel_name = os.path.basename(infile)[:-4]
        channel_parameters = channeltools.get_channel_parameters(channel_name)

        # No incluir si es un canal inactivo
        if channel_parameters["active"] != "true":
            continue

        # No incluir si es un canal para adultos, y el modo adulto está desactivado
        if channel_parameters["adult"] == "true" and config.get_setting("adult_mode") == "false":
            continue

        # No incluir si el canal es en un idioma filtrado
        if channel_language != "all" and channel_parameters["language"] != channel_language:
            continue

        # No incluir si en la configuracion del canal no existe "include_in_global_search"
        include = channel_parameters["include_in_global_search"]
        if include not in ["", "true"]:
            continue
        else:
            # Se busca en la configuración del canal el valor guardado
            include_in_global_search = config.get_setting("include_in_global_search", channel_name)

        # Si no hay valor en la configuración del canal se coloca como True ya que así estaba por defecto
        if include_in_global_search == "":
            include_in_global_search = True

        control = {'id': channel_name,
                   'type': "bool",
                   'label': channel_parameters["title"],
                   'default': include_in_global_search,
                   'enabled': True,
                   'visible': True}

        list_controls.append(control)

    return platformtools.show_channel_settings(list_controls=list_controls,
                                               caption="Canales incluidos en la búsqueda global",
                                               callback="save_settings", item=item, custom_button={'visible': False})


def save_settings(item, dict_values):
    for v in dict_values:
        config.set_setting("include_in_global_search", dict_values[v], v)


def searchbycat(item):
    # Only in xbmc/kodi
    # Abre un cuadro de dialogo con las categorías en las que hacer la búsqueda

    categories = ["Películas", "Series", "Anime", "Documentales", "VOS", "Latino"]
    categories_id = ["movie", "serie", "anime", "documentary", "vos", "latino"]
    list_controls = []
    for i, category in enumerate(categories):
        control = {'id': categories_id[i],
                   'type': "bool",
                   'label': category,
                   'default': False,
                   'enabled': True,
                   'visible': True}

        list_controls.append(control)
    control = {'id': "separador",
               'type': "label",
               'label': '',
               'default': "",
               'enabled': True,
               'visible': True}
    list_controls.append(control)
    control = {'id': "torrent",
               'type': "bool",
               'label': 'Incluir en la búsqueda canales Torrent',
               'default': True,
               'enabled': True,
               'visible': True}
    list_controls.append(control)

    return platformtools.show_channel_settings(list_controls=list_controls, caption="Elegir categorías",
                                               callback="search_cb", item=item)


def search_cb(item, values=""):
    cat = []
    for c in values:
        if values[c]:
            cat.append(c)

    if not len(cat):
        return None
    else:
        logger.info(item.tostring())
        logger.info(str(cat))
        return do_search(item, cat)


# Al llamar a esta función, el sistema pedirá primero el texto a buscar
# y lo pasará en el parámetro "tecleado"
def search(item, tecleado):
    logger.info()
    tecleado = tecleado.replace("+", " ")
    item.category = tecleado

    if tecleado != "":
        save_search(tecleado)

    if item.extra == "categorias":
        item.extra = tecleado
        return searchbycat(item)

    item.extra = tecleado
    return do_search(item, [])


def channel_result(item):
    extra = item.extra.split("{}")[0]
    channel = item.extra.split("{}")[1]
    tecleado = item.extra.split("{}")[2]
    exec "from channels import " + channel + " as module"
    item.channel = channel
    item.extra = extra
    # print item.url
    try:
        itemlist = module.search(item, tecleado)
    except:
        import traceback
        logger.error(traceback.format_exc())
        itemlist = []

    return itemlist


def channel_search(search_results, channel_parameters, tecleado):
    try:
        exec "from channels import " + channel_parameters["channel"] + " as module"
        mainlist = module.mainlist(Item(channel=channel_parameters["channel"]))
        search_items = [item for item in mainlist if item.action == "search"]
        if not search_items:
            search_items = [Item(channel=channel_parameters["channel"], action="search")]

        for item in search_items:
            result = module.search(item.clone(), tecleado)
            if result is None:
                result = []
            if len(result):
                if not channel_parameters["title"] in search_results:
                    search_results[channel_parameters["title"]] = []

                search_results[channel_parameters["title"]].append({"item": item, "itemlist": result})

    except:
        logger.error("No se puede buscar en: %s" % channel_parameters["title"])
        import traceback
        logger.error(traceback.format_exc())


# Esta es la función que realmente realiza la búsqueda
def do_search(item, categories=[]):
    multithread = config.get_setting("multithread", "buscador")
    result_mode = config.get_setting("result_mode", "buscador")
    logger.info()

    tecleado = item.extra

    itemlist = []

    channels_path = os.path.join(config.get_runtime_path(), "channels", '*.xml')
    logger.info("channels_path=%s" % channels_path)

    channel_language = config.get_setting("channel_language")
    logger.info("channel_language=%s" % channel_language)
    if channel_language == "":
        channel_language = "all"
        logger.info("channel_language=%s" % channel_language)

    # Para Kodi es necesario esperar antes de cargar el progreso, de lo contrario
    # el cuadro de progreso queda "detras" del cuadro "cargando..." y no se le puede dar a cancelar
    time.sleep(0.5)
    progreso = platformtools.dialog_progress("Buscando '%s'..." % tecleado, "")
    channel_files = sorted(glob.glob(channels_path), key=lambda x: os.path.basename(x))
    number_of_channels = len(channel_files)

    searches = []
    search_results = {}
    start_time = time.time()

    if multithread:
        progreso.update(0, "Buscando '%s'..." % tecleado)

    for index, infile in enumerate(channel_files):
        try:
            percentage = (index * 100) / number_of_channels

            basename = os.path.basename(infile)
            basename_without_extension = basename[:-4]
            logger.info("%s..." % basename_without_extension)

            channel_parameters = channeltools.get_channel_parameters(basename_without_extension)

            # No busca si es un canal inactivo
            if channel_parameters["active"] != "true":
                logger.info("%s no incluido" % basename_without_extension)
                continue

            # En caso de busqueda por categorias
            if categories:
                if not any(cat in channel_parameters["categories"] for cat in categories):
                    logger.info("%s no incluido" % basename_without_extension)
                    continue

            # No busca si es un canal para adultos, y el modo adulto está desactivado
            if channel_parameters["adult"] == "true" and config.get_setting("adult_mode") == "false":
                logger.info("%s no incluido" % basename_without_extension)
                continue

            # No busca si el canal es en un idioma filtrado
            if channel_language != "all" and channel_parameters["language"] != channel_language:
                logger.info("%s no incluido" % basename_without_extension)
                continue

            # No busca si es un canal excluido de la busqueda global
            include_in_global_search = channel_parameters["include_in_global_search"]
            if include_in_global_search in ["", "true"]:
                # Buscar en la configuracion del canal
                include_in_global_search = str(config.get_setting("include_in_global_search", basename_without_extension))
                # Si no hay valor en la configuración del canal se incluye ya que así estaba por defecto
                '''if include_in_global_search == "":
                    include_in_global_search = "true"'''

            if include_in_global_search.lower() != "true":
                logger.info("%s no incluido" % basename_without_extension)
                continue

            if progreso.iscanceled():
                progreso.close()
                logger.info("Busqueda cancelada")
                return itemlist

            # Modo Multi Thread
            if multithread:
                t = Thread(target=channel_search, args=[search_results, channel_parameters, tecleado],
                           name=channel_parameters["title"])
                t.setDaemon(True)
                t.start()
                searches.append(t)

            # Modo single Thread
            else:
                logger.info("Intentado busqueda en " + basename_without_extension + " de " + tecleado)
                channel_search(search_results, channel_parameters, tecleado)

            logger.info("%s incluido en la busqueda" % basename_without_extension)
            progreso.update(percentage / 2, "Iniciada busqueda de '%s' en %s..." % (tecleado, channel_parameters["title"]))

        except:
            continue
            logger.error("No se puede buscar en: %s" % channel_parameters["title"])
            import traceback
            logger.error(traceback.format_exc())

    # Modo Multi Thread
    # Usando isAlive() no es necesario try-except,
    # ya que esta funcion (a diferencia de is_alive())
    # es compatible tanto con versiones antiguas de python como nuevas
    if multithread:
        pendent = [a for a in searches if a.isAlive()]
        while pendent:
            percentage = (len(searches) - len(pendent)) * 100 / len(searches)
            completed = len(searches) - len(pendent)

            if len(pendent) > 5:
                progreso.update(percentage, "Busqueda terminada en %d de %d canales..." % (completed, len(searches)))
            else:
                list_pendent_names = [a.getName() for a in pendent]
                mensaje = "Buscando en %s" % (", ".join(list_pendent_names))
                progreso.update(percentage, mensaje)
                logger.debug(mensaje)

            if progreso.iscanceled():
                logger.info("Busqueda cancelada")
                break

            time.sleep(0.5)
            pendent = [a for a in searches if a.isAlive()]

    total = 0

    for channel in sorted(search_results.keys()):
        for search in search_results[channel]:
            total += len(search["itemlist"])
            title = channel
            if result_mode == 0:
                if len(search_results[channel]) > 1:
                    title += " [" + search["item"].title.strip() + "]"
                title += " (" + str(len(search["itemlist"])) + ")"

                title = re.sub("\[COLOR [^\]]+\]", "", title)
                title = re.sub("\[/COLOR]", "", title)

                extra = search["item"].extra + "{}" + search["item"].channel + "{}" + tecleado
                itemlist.append(Item(title=title, channel="buscador", action="channel_result", url=search["item"].url,
                                     extra=extra, folder=True))
            else:
                title = ">> Resultados del canal %s:" % title
                itemlist.append(Item(title=title, channel="buscador", action="",
                                     folder=False, text_color="yellow"))
                itemlist.extend(search["itemlist"])
                # itemlist.append(Item(title="", channel="buscador", action="", folder=False))

    title = "Buscando: '%s' | Encontrado: %d vídeos | Tiempo: %2.f segundos" % (tecleado, total, time.time()-start_time)
    itemlist.insert(0, Item(title=title, text_color='yellow'))

    progreso.close()

    return itemlist


def save_search(text):

    saved_searches_limit = int((10, 20, 30, 40, )[int(config.get_setting("saved_searches_limit", "buscador"))])

    current_saved_searches_list = config.get_setting("saved_searches_list", "buscador")
    if current_saved_searches_list is None:
        saved_searches_list = []
    else:
        saved_searches_list = list(current_saved_searches_list)

    if text in saved_searches_list:
        saved_searches_list.remove(text)

    saved_searches_list.insert(0, text)

    config.set_setting("saved_searches_list", saved_searches_list[:saved_searches_limit], "buscador")


def clear_saved_searches(item):

    config.set_setting("saved_searches_list", list(), "buscador")
    platformtools.dialog_ok("Buscador", "Búsquedas borradas correctamente")


def get_saved_searches():

    current_saved_searches_list = config.get_setting("saved_searches_list", "buscador")
    if current_saved_searches_list is None:
        saved_searches_list = []
    else:
        saved_searches_list = list(current_saved_searches_list)

    return saved_searches_list
