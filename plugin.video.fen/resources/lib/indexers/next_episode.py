# -*- coding: utf-8 -*-
from sys import argv
from datetime import date
from threading import Thread
import _strptime  # fix bug in python import
from windows import open_window
from apis.trakt_api import trakt_get_hidden_items
from indexers.tvshows import get_tvshow_info
from metadata import tvshow_meta, season_episodes_meta, retrieve_user_info
from modules import kodi_utils
from modules.sources import Sources
from modules.player import FenPlayer
from modules.settings import ignore_articles
from modules.watched_status import get_next_episodes, get_watched_status_tvshow
from modules.utils import get_datetime, make_thread_list, title_key
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
remove_meta_keys = kodi_utils.remove_meta_keys
dict_removals = kodi_utils.tvshow_dict_removals
make_listitem = kodi_utils.make_listitem
included_str, excluded_str = ls(32804).upper(), ls(32805).upper()
extras_str, browse_str, heading = ls(32645), ls(32652), ls(32806)

def build_next_episode_manager(params):
	def build_content(tmdb_id):
		try:
			cm = []
			listitem = make_listitem()
			set_property = listitem.setProperty
			cm_append = cm.append
			meta = tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
			meta_get = meta.get
			total_aired_eps = meta_get('total_aired_eps')
			total_seasons = meta_get('total_seasons')
			title = meta_get('title')
			playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(watched_info, tmdb_id, total_aired_eps)
			meta.update({'playcount': playcount, 'overlay': overlay})
			if tmdb_id in exclude_list: color, action, status, sort_value = 'red', 'unhide', excluded_str, 1
			else: color, action, status, sort_value = 'green', 'hide', included_str, 0
			display = '[COLOR=%s][%s][/COLOR] %s' % (color, status, title)
			extras_params = {'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'db_type': 'tvshow', 'is_widget': 'False'}
			url_params = {'mode': 'hide_unhide_trakt_items', 'action': action, 'media_type': 'shows', 'media_id': meta_get('imdb_id'), 'section': 'progress_watched'}
			url = build_url(url_params)
			if show_all_episodes:
				if all_episodes == 1 and total_seasons > 1: browse_params = {'mode': 'build_season_list', 'tmdb_id': tmdb_id}
				else: browse_params = {'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all'}
			else: browse_params = {'mode': 'build_season_list', 'tmdb_id': tmdb_id}
			cm_append((extras_str, 'RunPlugin(%s)' % build_url(extras_params)))
			cm_append((browse_str,'Container.Update(%s)' % build_url(browse_params)))
			listitem.setLabel(display)
			set_property('watchedepisodes', str(total_watched))
			set_property('unwatchedepisodes', str(total_unwatched))
			set_property('totalepisodes', str(total_aired_eps))
			set_property('totalseasons', str(total_seasons))
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': meta_get('poster'), 'fanart': meta_get('fanart'), 'banner': meta_get('banner'), 'clearart': meta_get('clearart'),
							'clearlogo': meta_get('clearlogo'), 'landscape': meta_get('landscape')})
			listitem.setCast(meta['cast'])
			listitem.setInfo('video', remove_meta_keys(meta, dict_removals))
			append({'listitem': (url, listitem, False), 'sort_value': sort_value, 'sort_title': title})
		except: pass
	__handle__ = int(argv[1])
	list_items = []
	append = list_items.append
	meta_user_info, watched_indicators, watched_info, all_episodes, include_year_in_title, open_extras = get_tvshow_info()	
	ep_list = get_next_episodes(watched_info)
	tmdb_list = [i['tmdb_id'] for i in ep_list]
	try: exclude_list = trakt_get_hidden_items('progress_watched')
	except: exclude_list = []
	show_all_episodes = True if all_episodes in (1, 2) else False
	threads = list(make_thread_list(build_content, tmdb_list, Thread))
	[i.join() for i in threads]
	item_list = sorted(list_items, key=lambda k: (k['sort_value'], title_key(k['sort_title'], ignore_articles())), reverse=False)
	item_list = [i['listitem'] for i in item_list]
	kodi_utils.add_dir({'mode': 'nill'}, '[I][COLOR=grey2]%s[/COLOR][/I]' % heading.upper(), __handle__, iconImage='settings.png', isFolder=False)
	kodi_utils.add_items(__handle__, item_list)
	kodi_utils.set_content(__handle__, 'tvshows')
	kodi_utils.end_directory(__handle__, cacheToDisc=False)
	kodi_utils.set_view_mode('view.main', 'tvshows')
	kodi_utils.focus_index(1)

def nextep_playback_info(meta):
	def _build_next_episode_play():
		ep_data = season_episodes_meta(season, meta, meta_user_info)
		if not ep_data: return 'no_next_episode'
		ep_data = [i for i in ep_data if i['episode'] == episode][0]
		airdate = ep_data['premiered']
		d = airdate.split('-')
		episode_date = date(int(d[0]), int(d[1]), int(d[2]))
		if current_date < episode_date: return 'no_next_episode'
		custom_title = meta_get('custom_title', None)
		title = custom_title or meta_get('title')
		display_name = '%s - %dx%.2d' % (title, int(season), int(episode))
		meta.update({'vid_type': 'episode', 'rootname': display_name, 'season': season, 'ep_name': ep_data['title'],
					'episode': episode, 'premiered': airdate, 'plot': ep_data['plot']})
		url_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': tmdb_id, 'tvshowtitle': meta_get('rootname'), 'season': season,
					'episode': episode, 'background': 'true'}
		if custom_title: url_params['custom_title'] = custom_title
		return url_params
	meta_get = meta.get
	meta_user_info = retrieve_user_info()
	tmdb_id, current_season, current_episode = meta_get('tmdb_id'), int(meta_get('season')), int(meta_get('episode'))
	try:
		current_date = get_datetime()
		season_data = meta_get('season_data')
		curr_season_data = [i for i in season_data if i['season_number'] == current_season][0]
		season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
		episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
		nextep_info = _build_next_episode_play()
	except: nextep_info = 'error'
	return meta, nextep_info

def execute_nextep(meta, nextep_settings):
	def _get_nextep_params():
		nextep_params = nextep_playback_info(meta)
		return nextep_params
	def _get_nextep_url():
		Sources().playback_prep(nextep_params)
		return kodi_utils.get_property('fen_nextep_url')
	def _confirm_threshold():
		nextep_threshold = nextep_settings['threshold']
		if nextep_threshold == 0: return True
		try: current_number = int(kodi_utils.get_property('fen_total_autoplays'))
		except: current_number = 1
		if current_number == nextep_threshold:
			current_number = 1
			kodi_utils.set_property('fen_total_autoplays', str(current_number))
			if open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=nextep_meta, function='confirm'): return True
			else:
				kodi_utils.notification(32736, 1500)
				return False
		else:
			current_number += 1
			kodi_utils.set_property('fen_total_autoplays', str(current_number))
			return True
	def _continue_action():
		if run_popup: action = open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=nextep_meta, function='next_ep')
		else: action = 'close'
		return action
	def _control():
		confirm_threshold = False
		final_action = 'cancel'
		while player.isPlayingVideo():
			try:
				total_time = player.getTotalTime()
				curr_time = player.getTime()
				remaining_time = round(total_time - curr_time)
				if remaining_time <= nextep_threshold_check:
					if not confirm_threshold:
						confirm_threshold = _confirm_threshold()
						if not confirm_threshold:
							final_action = 'cancel'
							break
				if remaining_time <= display_nextep_popup:
					final_action = _continue_action()
					break
				kodi_utils.sleep(200)
			except: pass
		return final_action
	kodi_utils.clear_property('fen_nextep_url')
	player = FenPlayer()
	run_popup, display_nextep_popup = nextep_settings['run_popup'], nextep_settings['window_time']
	nextep_prep, nextep_threshold_check = nextep_settings['start_prep'], nextep_settings['threshold_check']
	nextep_meta, nextep_params = _get_nextep_params()
	if nextep_params == 'error': return kodi_utils.notification(32574, 3000)
	elif nextep_params == 'no_next_episode': return
	nextep_url = _get_nextep_url()
	if not nextep_url: return kodi_utils.notification(32760, 3000)
	action = _control()
	if action == 'cancel': return kodi_utils.notification(32736, 3000)
	elif action == 'play': player.stop()
	elif action == 'close':
		if not run_popup: kodi_utils.notification('%s %s S%02dE%02d' % (ls(32801), nextep_meta['title'], nextep_meta['season'], nextep_meta['episode']), 6500, nextep_meta['poster'])
		while player.isPlayingVideo(): kodi_utils.sleep(100)
	kodi_utils.sleep(1000)
	player.run(nextep_url)




