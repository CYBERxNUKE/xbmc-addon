# -*- coding: utf-8 -*-
from sys import argv
from urllib.parse import unquote
from caches.main_cache import main_cache
from modules import kodi_utils
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
make_listitem = kodi_utils.make_listitem
icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/search.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')
folder_actions = ('movie', 'tvshow', 'people', 'imdb_keyword_movie', 'imdb_keyword_tvshow')

def search_history(params):
	def _builder():
		for h in history:
			try:
				cm = []
				query = unquote(h)
				url_params = {'mode': 'get_search_term', 'db_type': 'movie', 'query': query} if action == 'movie' \
						else {'mode': 'get_search_term', 'db_type': 'tv_show', 'query': query} if action == 'tvshow' \
						else {'mode': 'people_search.search', 'actor_name': query} if action == 'people' \
						else {'mode': 'furk.search_furk', 'db_type': 'video', 'query': query} if action == 'furk_video' \
						else {'mode': 'furk.search_furk', 'db_type': 'audio', 'music': True, 'query': query} if action == 'furk_audio' \
						else {'mode': 'easynews.search_easynews', 'query': query} if action == 'easynews_video' \
						else {'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'db_type': 'movie', 'query': query} if action == 'imdb_keyword_movie' \
						else {'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'db_type': 'tvshow', 'query': query} if action == 'imdb_keyword_tvshow' \
						else ''
				isFolder = False if action in folder_actions else True
				display = '[B]%s %s : [/B]' % (display_title, sear_str) + query 
				url = build_url(url_params)
				cm.append((remove_str,'RunPlugin(%s)' % build_url({'mode': 'remove_from_history', 'setting_id':search_setting, 'query': query})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, isFolder)
			except: pass
	try:
		__handle__ = int(argv[1])
		sear_str, mov_str, tv_str, peop_str = ls(32450).upper(), ls(32028).upper(), ls(32029).upper(), ls(32507).upper()
		furkvid_str = '%s %s' % (ls(32069).upper(), ls(32491).upper())
		furkaud_str = '%s %s' % (ls(32069).upper(), ls(32492).upper())
		imdb_key_mov_str, imdb_key_tv_str = '%s %s %s' % (ls(32064).upper(), ls(32092).upper(), mov_str), '%s %s %s' % (ls(32064).upper(), ls(32092).upper(), tv_str)
		remove_str, easy_str = ls(32786), ls(32070).upper()
		action = params['action']
		search_setting, display_title = {'movie': ('movie_queries', mov_str), 'tvshow': ('tvshow_queries', tv_str), 'people': ('people_queries', peop_str),
		'furk_video': ('furk_video_queries', furkvid_str), 'furk_audio': ('furk_audio_queries', furkaud_str), 'easynews_video': ('easynews_video_queries', easy_str),
		'imdb_keyword_movie': ('imdb_keyword_movie_queries', imdb_key_mov_str), 'imdb_keyword_tvshow': ('imdb_keyword_tvshow_queries', imdb_key_tv_str)}[action]
		history = main_cache.get(search_setting)
		__handle__ = int(argv[1])
		kodi_utils.add_items(__handle__, list(_builder()))
	except: pass
	kodi_utils.set_content(__handle__, '')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main', '')
	