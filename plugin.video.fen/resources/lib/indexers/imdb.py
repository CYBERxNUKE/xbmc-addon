# -*- coding: utf-8 -*-
import json
from sys import argv
from apis.imdb_api import imdb_user_lists, imdb_keyword_search
from modules import kodi_utils
from modules.history import add_to_search_history
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
make_listitem = kodi_utils.make_listitem
default_imdb_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/imdb.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')

def imdb_build_user_lists(db_type):
	def _builder():
		for item in user_lists:
			cm = []
			cm_append = cm.append
			url_params = {'mode': mode, 'action': 'imdb_user_list_contents', 'list_id': item['list_id']}
			imdb_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_imdb_external', 'name': item['title'], 'imdb_params': json.dumps(url_params)}
			imdb_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_imdb_external', 'name': item['title'], 'imdb_params': json.dumps(url_params)}
			url = build_url(url_params)
			listitem = make_listitem()
			listitem.setLabel(item['title'])
			listitem.setArt({'icon': default_imdb_icon, 'poster': default_imdb_icon, 'thumb': default_imdb_icon, 'fanart': fanart, 'banner': default_imdb_icon})
			cm_append((ls(32730),'RunPlugin(%s)' % build_url(imdb_selection_url)))
			cm_append((ls(32731),'RunPlugin(%s)' % build_url(imdb_folder_selection_url)))
			listitem.addContextMenuItems(cm)
			yield (url, listitem, True)
	__handle__ = int(argv[1])
	user_lists = imdb_user_lists(db_type)
	mode = 'build_%s_list' % db_type
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def imdb_build_keyword_results(db_type, query):
	def _builder():
		for count, item in enumerate(results, 1):
			cm = []
			cm_append = cm.append
			keyword = item[0]
			listings = item[1]
			url_params = {'mode': mode, 'action': 'imdb_keywords_list_contents', 'list_id': keyword.lower(), 'iconImage': 'imdb.png'}
			url_json = json.dumps(url_params)
			add_list_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_external', 'list_name': '%s (IMDb)' % keyword, 'menu_item': url_json}
			add_folder_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_external', 'name': '%s (IMDb)' % keyword, 'menu_item': url_json}
			url = build_url(url_params)
			listitem = make_listitem()
			listitem.setLabel('%02d | [B]%s[/B] [I]%s[/I]' % (count, keyword.upper(), listings))
			listitem.setArt({'icon': default_imdb_icon, 'poster': default_imdb_icon, 'thumb': default_imdb_icon, 'fanart': fanart, 'banner': default_imdb_icon})
			cm_append((ls(32730),'RunPlugin(%s)' % build_url(add_list_params)))
			cm_append((ls(32731),'RunPlugin(%s)' % build_url(add_folder_params)))
			listitem.addContextMenuItems(cm)
			yield (url, listitem, True)
	__handle__ = int(argv[1])
	results = imdb_keyword_search(query)
	add_to_search_history(query, 'imdb_keyword_%s_queries' % db_type)
	if not results: return
	mode = 'build_%s_list' % db_type
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')




