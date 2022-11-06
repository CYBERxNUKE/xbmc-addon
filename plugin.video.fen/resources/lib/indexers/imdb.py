# -*- coding: utf-8 -*-
from apis.imdb_api import imdb_user_lists, imdb_keyword_search
from modules import kodi_utils
# from modules.kodi_utils import logger

ls, sys, build_url, make_listitem, set_view_mode = kodi_utils.local_string, kodi_utils.sys, kodi_utils.build_url, kodi_utils.make_listitem, kodi_utils.set_view_mode
add_items, set_content, external_browse, end_directory = kodi_utils.add_items, kodi_utils.set_content, kodi_utils.external_browse, kodi_utils.end_directory
default_imdb_icon, fanart, fen_clearlogo = kodi_utils.get_icon('imdb'), kodi_utils.addon_fanart, kodi_utils.addon_clearlogo

def imdb_build_user_lists(media_type):
	def _builder():
		for item in user_lists:
			try:
				cm = []
				cm_append = cm.append
				url = build_url({'mode': mode, 'action': 'imdb_user_list_contents', 'list_id': item['list_id']})
				listitem = make_listitem()
				listitem.setLabel(item['title'])
				listitem.setArt({'icon': default_imdb_icon, 'poster': default_imdb_icon, 'thumb': default_imdb_icon, 'fanart': fanart,
								'banner': default_imdb_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				cm_append((ls(32730),'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': item['title'], 'iconImage': 'imdb'})))
				cm_append((ls(32731),'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': item['title'], 'iconImage': 'imdb'})))
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	handle = int(sys.argv[1])
	user_lists = imdb_user_lists(media_type)
	mode = 'build_%s_list' % media_type
	add_items(handle, list(_builder()))
	set_content(handle, 'files')
	end_directory(handle)
	if not external_browse(): set_view_mode('view.main')

def imdb_build_keyword_results(media_type, query):
	def _builder():
		for count, item in enumerate(results, 1):
			cm = []
			cm_append = cm.append
			keyword = item[0]
			listings = item[1]
			url_params = {'mode': mode, 'action': 'imdb_keywords_list_contents', 'list_id': keyword.lower(), 'iconImage': 'imdb'}
			url = build_url(url_params)
			listitem = make_listitem()
			listitem.setLabel('%02d | [B]%s[/B] [I]%s[/I]' % (count, keyword.upper(), listings))
			listitem.setArt({'icon': default_imdb_icon, 'poster': default_imdb_icon, 'thumb': default_imdb_icon, 'fanart': fanart,
							'banner': default_imdb_icon, 'clearlogo': fen_clearlogo})
			listitem.setInfo('video', {'plot': ' '})
			cm_append((ls(32730),'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': '%s (IMDb)' % keyword.upper(), 'iconImage': 'imdb'})))
			cm_append((ls(32731),'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': '%s (IMDb)' % keyword.upper(), 'iconImage': 'imdb'})))
			listitem.addContextMenuItems(cm)
			yield (url, listitem, True)
	handle = int(sys.argv[1])
	results = imdb_keyword_search(query)
	if not results: return
	mode = 'build_%s_list' % media_type
	add_items(handle, list(_builder()))
	set_content(handle, 'files')
	end_directory(handle)
	if not external_browse(): set_view_mode('view.main')




