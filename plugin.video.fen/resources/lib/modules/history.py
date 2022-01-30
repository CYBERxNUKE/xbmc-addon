# -*- coding: utf-8 -*-
import json
from datetime import timedelta
from caches.main_cache import main_cache
from modules import kodi_utils
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/search.png')

EXPIRES_365_DAYS = timedelta(days=365)

def add_to_search_history(search_name, search_list):
	try:
		result = []
		cache = main_cache.get(search_list)
		if cache: result = cache
		if search_name in result: result.remove(search_name)
		result.insert(0, search_name)
		result = result[:10]
		main_cache.set(search_list, result, expiration=EXPIRES_365_DAYS)
	except: return

def remove_from_search_history(params):
	try:
		result = main_cache.get(params['setting_id'])
		result.remove(params.get('query'))
		main_cache.set(params['setting_id'], result, expiration=EXPIRES_365_DAYS)
		kodi_utils.notification(32576, 3500)
		kodi_utils.execute_builtin('Container.Refresh')
	except: return

def clear_search_history():
	delete_str, search_str, hist_str, vid_str, mov_str, key_str = ls(32785), ls(32450), ls(32486), ls(32491), ls(32028), ls(32092)
	tv_str, aud_str, furk_str, easy_str, peop_str, imdb_str = ls(32029), ls(32492), ls(32069), ls(32070), ls(32507), ls(32064)
	choice_list = [('%s %s %s %s' % (delete_str, mov_str, search_str, hist_str), 'movie_queries'),
				   ('%s %s %s %s' % (delete_str, tv_str, search_str, hist_str), 'tvshow_queries'), 
				   ('%s %s %s %s' % (delete_str, peop_str, search_str, hist_str), 'people_queries'),
				   ('%s %s %s %s %s' % (delete_str, imdb_str, key_str, mov_str, hist_str), 'imdb_keyword_movie_queries'),
				   ('%s %s %s %s %s' % (delete_str, imdb_str, key_str, tv_str, hist_str), 'imdb_keyword_tvshow_queries'),
				   ('%s %s %s %s %s' % (delete_str, furk_str, vid_str, search_str, hist_str), 'furk_video_queries'), 
				   ('%s %s %s %s %s' % (delete_str, furk_str, aud_str, search_str, hist_str), 'furk_audio_queries'), 
				   ('%s %s %s %s' % (delete_str, easy_str, search_str, hist_str), 'easynews_video_queries')]
	try:
		list_items = [{'line1': item[0], 'icon': icon} for item in choice_list]
		kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		setting = kodi_utils.select_dialog([item[1] for item in choice_list], **kwargs)
		if setting == None: return
		main_cache.set(setting, '', expiration=EXPIRES_365_DAYS)
		kodi_utils.notification(32576, 3500)
	except: return

	