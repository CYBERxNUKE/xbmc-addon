# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
from xbmcaddon import Addon
from urllib.parse import urlencode

__addon__ = Addon(id='plugin.video.fen')
monitor = xbmc.Monitor()
window = xbmcgui.Window(10000)
progressDialog = xbmcgui.DialogProgress()
progressDialogBG = xbmcgui.DialogProgressBG()
dialog = xbmcgui.Dialog()
window_xml_dialog = xbmcgui.WindowXMLDialog
player = xbmc.Player()
xbmc_player = xbmc.Player
numeric_input = xbmcgui.INPUT_NUMERIC
get_infolabel = xbmc.getInfoLabel
get_visibility = xbmc.getCondVisibility
execute_JSON = xbmc.executeJSONRPC
window_xml_info_action = xbmcgui.ACTION_SHOW_INFO
window_xml_closing_actions = (xbmcgui.ACTION_PARENT_DIR, xbmcgui.ACTION_PREVIOUS_MENU, xbmcgui.ACTION_STOP, xbmcgui.ACTION_NAV_BACK)
window_xml_selection_actions = (xbmcgui.ACTION_SELECT_ITEM, xbmcgui.ACTION_MOUSE_START)
window_xml_context_actions = (xbmcgui.ACTION_CONTEXT_MENU, xbmcgui.ACTION_MOUSE_RIGHT_CLICK, xbmcgui.ACTION_MOUSE_LONG_CLICK)
window_xml_left_action, window_xml_right_action = xbmcgui.ACTION_MOVE_LEFT, xbmcgui.ACTION_MOVE_RIGHT
window_xml_up_action, window_xml_down_action = xbmcgui.ACTION_MOVE_UP, xbmcgui.ACTION_MOVE_DOWN
myvideos_db_paths = {18: '116', 19: '119', 20: '119'}
movie_dict_removals = ('fanart_added', 'cast', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id', 'all_trailers',
						'fanart', 'banner', 'clearlogo', 'clearart', 'landscape', 'discart', 'original_title', 'english_title',
						'extra_info', 'alternative_titles', 'country_codes', 'fanarttv_fanart', 'fanarttv_poster', 'fanart2', 'poster2')
tvshow_dict_removals = ('fanart_added', 'cast', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id', 'all_trailers', 'discart',
						'total_episodes', 'total_seasons', 'fanart', 'banner', 'clearlogo', 'clearart', 'landscape', 'season_data',
						'original_title', 'extra_info', 'alternative_titles', 'english_title', 'season_summary', 'country_codes',
						'fanarttv_fanart', 'fanarttv_poster', 'total_aired_eps', 'fanart2', 'poster2')
episode_dict_removals = ('thumb', 'guest_stars')

def get_property(prop):
	return window.getProperty(prop)

def set_property(prop, value):
	return window.setProperty(prop, value)

def clear_property(prop):
	return window.clearProperty(prop)

def addon():
	return Addon(id='plugin.video.fen')

def ext_addon(addon_id):
	return Addon(id=addon_id)

def addon_installed(addon_id):
	return get_visibility('System.HasAddon(%s)' % addon_id)

def add_item(handle, url, listitem, isFolder):
	xbmcplugin.addDirectoryItem(handle, url, listitem, isFolder)

def add_items(handle, item_list):
	xbmcplugin.addDirectoryItems(handle, item_list)

def set_content(handle, content):
	xbmcplugin.setContent(handle, content)

def set_category(handle, category):
	xbmcplugin.setPluginCategory(handle, category)

def set_sort_method(handle, method):
	if method == 'episodes': sort_method = xbmcplugin.SORT_METHOD_EPISODE
	elif method == 'files': sort_method = xbmcplugin.SORT_METHOD_FILE
	else: sort_method = xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE#label
	xbmcplugin.addSortMethod(handle, sort_method)

def end_directory(handle, cacheToDisc=True):
	xbmcplugin.endOfDirectory(handle, cacheToDisc=cacheToDisc)

def set_resolvedurl(handle, item):
	xbmcplugin.setResolvedUrl(handle, True, item)

def make_playlist(_type='video'):
	return xbmc.PlayList(xbmc.PLAYLIST_VIDEO) if _type == 'video' else xbmc.PlayList(xbmc.PLAYLIST_MUSIC)

def convert_language(lang):
	return xbmc.convertLanguage(lang, xbmc.ISO_639_2)

def supported_media():
	return xbmc.getSupportedMedia('video')

def path_exists(path):
	return xbmcvfs.exists(path)

def make_directory(path):
	xbmcvfs.mkdir(path)

def make_directorys(path):
	xbmcvfs.mkdirs(path)

def open_file(_file, mode='r'):
	return xbmcvfs.File(_file, mode)

def delete_file(_file):
	xbmcvfs.delete(_file)

def rename_file(old, new):
	xbmcvfs.rename(old, new)

def list_dirs(location):
	return xbmcvfs.listdir(location)

def make_listitem():
	return xbmcgui.ListItem(offscreen=True)

def local_string(string):
	try: string = int(string)
	except: return string
	try: string = str(__addon__.getLocalizedString(string))
	except: string = __addon__.getLocalizedString(string)
	return string

def translate_path(path):
	return xbmcvfs.translatePath(path)

def sleep(time):
	return xbmc.sleep(time)

def execute_builtin(command):
	return xbmc.executebuiltin(command)

def get_kodi_version():
	return int(get_infolabel('System.BuildVersion')[0:2])

def current_skin():
	return xbmc.getSkinDir()

def current_window_id():
	return xbmcgui.Window(xbmcgui.getCurrentWindowId())

def get_video_database_path():
	return translate_path('special://profile/Database/MyVideos%s.db' % myvideos_db_paths[get_kodi_version()])

def show_busy_dialog():
	return execute_builtin('ActivateWindow(busydialognocancel)')

def hide_busy_dialog():
	execute_builtin('Dialog.Close(busydialognocancel)')
	execute_builtin('Dialog.Close(busydialog)')

def close_all_dialog():
	execute_builtin('Dialog.Close(all,true)')

def container_content():
	return get_infolabel('Container.Content')

def external_browse():
	return 'fen' not in get_infolabel('Container.PluginName')

def widget_refresh():
	return execute_builtin('UpdateLibrary(video,special://skin/foo)')

def ok_dialog(heading='Fen', text='', highlight='royalblue', ok_label=local_string(32839), top_space=False):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	if not text: text = '[CR][CR]%s' % local_string(32760)
	elif top_space: text = '[CR][CR]%s' % text
	kwargs = {'heading': heading, 'text': text, 'highlight': highlight, 'ok_label': ok_label}
	return open_window(('windows.select_ok', 'OK'), 'ok.xml', **kwargs)

def confirm_dialog(heading='Fen', text='', highlight='royalblue', ok_label=local_string(32839), cancel_label=local_string(32840), top_space=False, default_control=11):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	if isinstance(ok_label, int): ok_label = local_string(ok_label)
	if isinstance(cancel_label, int): cancel_label = local_string(cancel_label)
	if not text: text = '[CR][CR]%s' % local_string(32580)
	elif top_space: text = '[CR][CR]%s' % text
	kwargs = {'heading': heading, 'text': text, 'highlight': highlight, 'ok_label': ok_label, 'cancel_label': cancel_label, 'default_control': default_control}
	return open_window(('windows.select_ok', 'YesNo'), 'yesno.xml', **kwargs)

def select_dialog(function_list, **kwargs):
	from windows import open_window
	selection = open_window(('windows.select_ok', 'Select'), 'select.xml', **kwargs)
	if selection in ([], None): return None
	if kwargs.get('multi_choice', 'false') == 'true': return [function_list[i] for i in selection]
	return function_list[selection]

def show_text(heading, text=None, file=None, font_size='small'):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if file:
		with open(file, encoding='utf-8') as r: text = r.read()
	return open_window(['windows.textviewer', 'TextViewer'], 'textviewer.xml', heading=heading, text=text, font_size=font_size)

def notification(line1, time=5000, icon=None, sound=False):
	if isinstance(line1, int): line1 = local_string(line1)
	icon = icon or translate_path('special://home/addons/plugin.video.fen/icon.png')
	xbmcgui.Dialog().notification('Fen', line1, icon, time, sound)

def choose_view(view_type, content):
	from sys import argv
	__handle__ = int(argv[1])
	set_view_str = local_string(32547)
	settings_icon = translate_path('special://home/addons/script.tikiart/resources/media/settings.png')
	fanart = translate_path('special://home/addons/plugin.video.fen/fanart.png')
	listitem = make_listitem()
	listitem.setLabel(set_view_str)
	params_url = build_url({'mode': 'set_view', 'view_type': view_type})
	listitem.setArt({'icon': settings_icon, 'poster': settings_icon, 'thumb': settings_icon, 'fanart': fanart, 'banner': settings_icon})
	add_item(__handle__, params_url, listitem, False)
	set_content(__handle__, content)
	end_directory(__handle__)
	set_view_mode(view_type, content)

def set_view(view_type):
	import sqlite3 as database
	view_id = str(current_window_id().getFocusId())
	dbcon = database.connect(translate_path('special://profile/addon_data/plugin.video.fen/views.db'))
	dbcon.execute("DELETE FROM views WHERE view_type = ?", (view_type,))
	dbcon.execute("INSERT INTO views VALUES (?, ?)", (view_type, view_id))
	dbcon.commit()
	set_view_property(view_type, view_id)
	notification(get_infolabel('Container.Viewmode').upper(), time=1500)

def set_view_property(view_type, view_id):
	set_property('fen_%s' % view_type, view_id)

def set_view_properties():
	import sqlite3 as database
	dbcon = database.connect(translate_path('special://profile/addon_data/plugin.video.fen/views.db'))
	dbcur = dbcon.cursor()
	dbcur.execute("SELECT * FROM views")
	view_ids = dbcur.fetchall()
	for item in view_ids: set_property('fen_%s' % item[0], item[1])

def set_view_mode(view_type, content='files'):
	if external_browse(): return
	sleep(100)
	view_id = get_property('fen_%s' % view_type)
	if not view_id:
		try:
			import sqlite3 as database
			dbcon = database.connect(translate_path('special://profile/addon_data/plugin.video.fen/views.db'))
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT view_id FROM views WHERE view_type = ?", (str(view_type),))
			view_id = dbcur.fetchone()[0]
		except: view_id = ''
	try:
		t = 0
		while not container_content() == content:
			t += 1
			if t < 5000: sleep(1)
			else: return
		if view_id: execute_builtin('Container.SetViewMode(%s)' % view_id)
	except: return

def timeIt(func):
	# Thanks to 123Venom
	import time
	fnc_name = func.__name__
	def wrap(*args, **kwargs):
		started_at = time.time()
		result = func(*args, **kwargs)
		logger('%s.%s' % (__name__ , fnc_name), (time.time() - started_at))
		return result
	return wrap

def logger(heading, function):
	xbmc.log('###%s###: %s' % (heading, function), 1)

def build_url(url_params):
	try: url = 'plugin://plugin.video.fen/?' + urlencode(url_params)
	except: url = 'plugin://plugin.video.fen/?' + urlencode(to_utf8(url_params))
	return url

def add_dir(url_params, list_name, __handle__, iconImage='DefaultFolder.png', fanartImage=None, isFolder=True):
	if not fanartImage: fanartImage = translate_path('special://home/addons/plugin.video.fen/fanart.png')
	icon = translate_path('special://home/addons/script.tikiart/resources/media/%s' % iconImage)
	url = build_url(url_params)
	listitem = make_listitem()
	listitem.setLabel(list_name)
	listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanartImage, 'banner': icon})
	add_item(__handle__, url, listitem, isFolder)

def remove_meta_keys(dict_item, dict_removals):
	for k in dict_removals: dict_item.pop(k, None)
	return dict_item

def volume_checker(volume_setting):
	# 0% == -60db, 100% == 0db
	try:
		if get_visibility('Player.Muted'): return
		from modules.utils import string_alphanum_to_num
		max_volume = int(min(int(volume_setting), 100))
		current_volume_db = int(string_alphanum_to_num(get_infolabel('Player.Volume').split('.')[0]))
		current_volume_percent = int(100 - ((float(current_volume_db)/60)*100))
		if current_volume_percent > max_volume: execute_builtin('SetVolume(%d)' % int(max_volume))
	except: pass

def focus_index(index, sleep_time=100):
	sleep(sleep_time)
	current_window = current_window_id()
	focus_id = current_window.getFocusId()
	try: current_window.getControl(focus_id).selectItem(index)
	except: pass

def clear_settings_window_properties():
	clear_property('fen_settings')
	notification(32576, 2500)