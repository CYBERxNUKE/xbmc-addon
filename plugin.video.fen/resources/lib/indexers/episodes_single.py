# -*- coding: utf-8 -*-
from apis.trakt_api import get_trakt_tvshow_id, trakt_fetch_collection_watchlist, trakt_get_hidden_items, trakt_get_my_calendar
from indexers.episodes import build_single_episode
from modules.utils import get_datetime
from modules.settings import nextep_content_settings, watched_indicators, calendar_sort_order
from modules.watched_status import get_in_progress_episodes, get_next_episodes, get_watched_info_tv
# from modules.kodi_utils import logger

def build_in_progress_episode():
	data = get_in_progress_episodes()
	build_single_episode('progress', data)

def build_next_episode():
	nextep_settings = nextep_content_settings()
	include_unwatched = nextep_settings['include_unwatched']
	indicators = watched_indicators()
	watched_info = get_watched_info_tv(indicators)
	data = get_next_episodes(watched_info)
	if indicators == 1:
		list_type = 'next_episode_trakt'
		try: hidden_data = trakt_get_hidden_items('progress_watched')
		except: hidden_data = []
		data = [i for i in data if not i['tmdb_id'] in hidden_data]
	else: list_type = 'next_episode_fen'
	if include_unwatched:
		try: unwatched = [{'tmdb_id': get_trakt_tvshow_id(i['media_ids']), 'season': 1, 'episode': 0, 'unwatched': True} \
						for i in trakt_fetch_collection_watchlist('watchlist', 'tvshow')]
		except: unwatched = []
		data += unwatched
	build_single_episode(list_type, data)

def get_trakt_my_calendar(params):
	current_date = get_datetime()
	recently_aired = params.get('recently_aired', None)
	data = trakt_get_my_calendar(recently_aired, current_date)
	if recently_aired:
		list_type = 'trakt_recently_aired'
		data = data[:20]
		reverse = True
	else:
		list_type = 'trakt_calendar'
		data.sort(key=lambda k: k['sort_title'], reverse=False)
		reverse = calendar_sort_order() == 0
	data.sort(key=lambda k: k['first_aired'], reverse=reverse)
	build_single_episode(list_type, data)
