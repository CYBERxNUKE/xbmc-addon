# -*- coding: utf-8 -*-
from sys import argv
from threading import Thread
import metadata
from apis.trakt_api import get_trakt_tvshow_id
from modules import kodi_utils
from modules import settings
from modules import watched_status as indicators
from modules.utils import jsondate_to_datetime, adjust_premiered_date, make_day, get_datetime, make_thread_list_enumerate, title_key, date_difference
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
remove_meta_keys = kodi_utils.remove_meta_keys
dict_removals = kodi_utils.episode_dict_removals
string = str
upper = string.upper
poster_empty = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/box_office.png')
fanart_empty = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')
watched_str, unwatched_str, extras_str, options_str, clearprog_str, browse_str = ls(32642), ls(32643), ls(32645), ls(32646), ls(32651), ls(32652)
run_plugin, container_update, unaired_label = 'RunPlugin(%s)', 'Container.Update(%s)', '[COLOR red][I]%s[/I][/COLOR]'

def build_episode_list(params):
	def _process():
		for item in episodes_data:
			try:
				cm = []
				listitem = make_listitem()
				set_property = listitem.setProperty
				cm_append = cm.append
				item_get = item.get
				season = item_get('season')
				episode = item_get('episode')
				ep_name = item_get('title')
				premiered = item_get('premiered')
				all_cast = cast + item_get('guest_stars', [])
				episode_date, premiered = adjust_premiered_date(premiered, adjust_hours)
				playcount, overlay = get_watched_status(watched_info, string(tmdb_id), season, episode)
				resumetime = get_resumetime(bookmarks, tmdb_id, season, episode)
				thumb = item_get('thumb', None) or fanart
				if thumb_fanart: background = thumb
				else: background = fanart
				item.update({'trailer': trailer, 'tvshowtitle': title, 'premiered': premiered, 'genre': genre, 'duration': duration, 'mpaa': mpaa, 'studio': studio,
							'playcount': playcount, 'overlay': overlay})
				extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'db_type': 'tvshow', 'is_widget': is_widget})
				options_params = build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
				url_params = build_url({'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
				display = ep_name
				unaired = False
				if not episode_date or current_date < episode_date:
					if not show_unaired: continue
					if season != 0:
						unaired = True
						display = unaired_label % ep_name
						item['title'] = display
				cm_append((extras_str, run_plugin % extras_params))
				cm_append((options_str, run_plugin % options_params))
				clearprog_params, unwatched_params, watched_params = '', '', ''
				if not unaired:
					if resumetime != '0':
						clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'db_type': 'episode', 'tmdb_id': tmdb_id,
													'season': season, 'episode': episode, 'refresh': 'true'})
						cm_append((clearprog_str, run_plugin % clearprog_params))
						set_property('fen_in_progress', 'true')
					if playcount:
						unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id,
													'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
						cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
					else:
						watched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id,
													'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
						cm_append((watched_str % watched_title, run_plugin % watched_params))
				listitem.setLabel(display)
				listitem.setContentLookup(False)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'poster': show_poster, 'fanart': background, 'thumb': thumb, 'icon':thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo,
								'landscape': thumb, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': thumb, 'tvshow.banner': banner})
				listitem.setCast(all_cast)
				listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				listitem.setInfo('video', remove_meta_keys(item, dict_removals))
				set_property('resumetime', resumetime)
				if is_widget:
					set_property('fen_widget', 'true')
					set_property('fen_playcount', string(playcount))
					set_property('fen_options_menu_params', options_params)
					set_property('fen_extras_menu_params', extras_params)
					set_property('fen_unwatched_params', unwatched_params)
					set_property('fen_watched_params', watched_params)
					set_property('fen_clearprog_params', clearprog_params)
				else: set_property('fen_widget', 'false')
				yield (url_params, listitem, False)
			except: pass
	__handle__ = int(argv[1])
	item_list = []
	append = item_list.append
	meta_user_info, watched_indicators, watched_info, show_unaired, thumb_fanart, is_widget, current_date, adjust_hours, bookmarks = get_episode_info()
	poster_main, poster_backup, fanart_main, fanart_backup = settings.get_art_provider()
	all_episodes = True if params.get('season') == 'all' else False
	meta = metadata.tvshow_meta('tmdb_id', params.get('tmdb_id'), meta_user_info)
	meta_get = meta.get
	tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
	title, year, rootname, banner = meta_get('title'), meta_get('year'), meta_get('rootname'), meta_get('banner')
	show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
	fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
	clearlogo, clearart, landscape = meta_get('clearlogo'), meta_get('clearart'), meta_get('landscape')
	cast, mpaa, duration = meta_get('cast'), meta_get('mpaa'), meta_get('duration')
	trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
	tvshow_plot = meta_get('plot')
	get_resumetime = indicators.get_resumetime
	get_watched_status = indicators.get_watched_status_episode
	watched_title = 'Trakt' if watched_indicators == 1 else 'Fen'
	if all_episodes:
		episodes_data = metadata.all_episodes_meta(meta, meta_user_info)
		if not settings.show_specials(): episodes_data = [i for i in episodes_data if not i['season'] == 0]
	else: episodes_data = metadata.season_episodes_meta(params['season'], meta, meta_user_info)
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_content(__handle__, 'episodes')
	kodi_utils.set_sort_method(__handle__, 'episodes')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.episodes', 'episodes')

def build_single_episode(list_type, data):
	def _sort_results(items):
		if list_type_starts_with('next_episode'):
			def func(function):
				if sort_key == 'fen_name': return title_key(function, ignore_articles)
				elif sort_key == 'fen_last_played': return jsondate_to_datetime(function, resformat)
				else: return function
			sort_key = nextep_settings['sort_key']
			sort_direction = nextep_settings['sort_direction']
			if nextep_settings['sort_airing_today_to_top']:
				airing_today = [i for i in items if date_difference(current_date, jsondate_to_datetime(i[1].getProperty('fen_first_aired'), '%Y-%m-%d').date(), 0)]
				airing_today = sorted(airing_today, key=lambda i: i[1].getProperty('fen_first_aired'))
				remainder = [i for i in items if not i in airing_today]
				remainder = sorted(remainder, key=lambda i: func(i[1].getProperty(sort_key)), reverse=sort_direction)
				unaired = [i for i in remainder if i[1].getProperty('fen_unaired') == 'true']
				aired = [i for i in remainder if not i in unaired]
				remainder = aired + unaired
				items = airing_today + remainder
			else:
				items = sorted(items, key=lambda i: func(i[1].getProperty(sort_key)), reverse=sort_direction)
				unaired = [i for i in items if i[1].getProperty('fen_unaired') == 'true']
				aired = [i for i in items if not i in unaired]
				items = aired + unaired
		else: items.sort(key=lambda k: int(k[1].getProperty('fen_sort_order')))
		return items
	def _process(item_position, ep_data):
		try:
			cm = []
			listitem = make_listitem()
			set_property = listitem.setProperty
			cm_append = cm.append
			ep_data_get = ep_data.get
			if list_type_starts_with('trakt_'): tmdb_id = get_trakt_tvshow_id(ep_data_get('ids'))
			else: tmdb_id = ep_data_get('tmdb_id')
			if not tmdb_id: return
			meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
			meta_get = meta.get
			tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
			title, year, rootname, banner = meta_get('title'), meta_get('year'), meta_get('rootname'), meta_get('banner')
			show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
			fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
			clearlogo, clearart, landscape = meta_get('clearlogo'), meta_get('clearart'), meta_get('landscape')
			cast, mpaa, duration = meta_get('cast'), meta_get('mpaa'), meta_get('duration')
			trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
			tvshow_plot = meta_get('plot')
			orig_season = ep_data_get('season')
			orig_episode = ep_data_get('episode')
			if list_type_starts_with('next_episode'):
				season_data = meta_get('season_data')
				curr_season_data = [i for i in season_data if i['season_number'] == orig_season][0]
				orig_season = orig_season if orig_episode < curr_season_data['episode_count'] else orig_season + 1
				orig_episode = orig_episode + 1 if orig_episode < curr_season_data['episode_count'] else 1
			episodes_data = metadata.season_episodes_meta(orig_season, meta, meta_user_info)
			try: item = [i for i in episodes_data if i['episode'] == orig_episode][0]
			except: return
			item_get = item.get
			season = item_get('season')
			episode = item_get('episode')
			ep_name = item_get('title')
			orig_premiered = item_get('premiered')
			all_cast = cast + item_get('guest_stars', [])
			episode_date, premiered = adjust_premiered_date(orig_premiered, adjust_hours)
			if not episode_date or current_date < episode_date:
				if list_type_starts_with('next_episode'):
					if not include_unaired: return
					if not date_difference(current_date, episode_date, 7): return
				elif not show_unaired: return
				unaired = True
				set_property('fen_unaired', 'true')
			else:
				unaired = False
				set_property('fen_unaired', 'false')
			playcount, overlay = get_watched_status(watched_info, string(tmdb_id), season, episode)
			resumetime = get_resumetime(bookmarks, tmdb_id, season, episode)
			if display_title == 0: title_string = '%s: ' % title
			else: title_string = ''
			if display_title in (0,1): seas_ep = '%dx%.2d - ' % (season, episode)
			else: seas_ep = ''
			if list_type_starts_with('next_episode'):
				unwatched = ep_data_get('unwatched', False)
				if episode_date: display_premiered = make_day(current_date, episode_date, date_format)
				else: display_premiered == 'UNKNOWN'
				airdate = '[[COLOR magenta]%s[/COLOR]] ' % display_premiered if include_airdate else ''
				highlight_color = unwatched_color if unwatched else unaired_color if unaired else ''
				italics_open, italics_close = ('[I]', '[/I]') if highlight_color else ('', '')
				if highlight_color: episode_info = '%s[COLOR %s]%s %s[/COLOR]%s' % (italics_open, highlight_color, seas_ep, ep_name, italics_close)
				else: episode_info = '%s%s%s%s' % (italics_open, seas_ep, ep_name, italics_close)
				display = '%s%s%s' % (airdate, upper(title_string), episode_info)
			elif list_type == 'trakt_calendar':
				if episode_date: display_premiered = make_day(current_date, episode_date, date_format)
				else: display_premiered == 'UNKNOWN'
				display = '[%s]%s%s%s' % (display_premiered, upper(title_string), seas_ep, item_get('title'))
				if unaired:
					displays = display.split(']')
					display = '[COLOR red]' + displays[0] + '][/COLOR]' + displays[1]
			else:
				color_tags = ('[COLOR red]', '[/COLOR]') if unaired else ('', '')
				display = '%s%s%s%s%s' % (upper(title_string), color_tags[0], seas_ep, ep_name, color_tags[1])
			thumb = item_get('thumb', None) or fanart
			if thumb_fanart: background = thumb
			else: background = fanart
			item.update({'trailer': trailer, 'tvshowtitle': title, 'premiered': premiered, 'genre': genre, 'duration': duration,
						'mpaa': mpaa, 'studio': studio, 'playcount': playcount, 'overlay': overlay, 'title': display})
			extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'db_type': 'tvshow', 'is_widget': is_widget})
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
			url_params = build_url({'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
			if show_all_episodes:
				if all_episodes == 1 and meta_get('total_seasons') > 1: browse_params = build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
				else: browse_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all'})
			else: browse_params = build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
			cm_append((extras_str, run_plugin % extras_params))
			cm_append((options_str, run_plugin % options_params))
			cm_append((browse_str, container_update % browse_params))
			clearprog_params, unwatched_params, watched_params = '', '', ''
			if not unaired:
				if resumetime != '0':
					clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'db_type': 'episode', 'tmdb_id': tmdb_id,
												'season': season, 'episode': episode, 'refresh': 'true'})
					cm_append((clearprog_str, run_plugin % clearprog_params))
					set_property('fen_in_progress', 'true')
				if playcount:
					unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id,
												'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
					cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
				else:
					watched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id,
												'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
					cm_append((watched_str % watched_title, run_plugin % watched_params))
			if list_type == 'next_episode_trakt': cm_append((ls(32599), container_update % build_url({'mode': 'build_next_episode_manager'})))
			listitem.setLabel(display)
			listitem.setContentLookup(False)
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': show_poster, 'fanart': background, 'thumb': thumb, 'icon':thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo,
							'landscape': thumb, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': thumb, 'tvshow.banner': banner})
			listitem.setCast(all_cast)
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
			listitem.setInfo('video', remove_meta_keys(item, dict_removals))
			set_property('resumetime', resumetime)
			set_property('fen_name', '%s - %.2dx%.2d' % (title, season, episode))
			if list_type_starts_with('next_episode'):
				last_played = ep_data_get('last_played', resinsert)
				set_property('fen_last_played', last_played)
				set_property('fen_first_aired', premiered)
			else: set_property('fen_sort_order', string(item_position))
			if is_widget:
				set_property('fen_widget', 'true')
				set_property('fen_playcount', string(playcount))
				set_property('fen_browse_params', browse_params)
				set_property('fen_options_menu_params', options_params)
				set_property('fen_extras_menu_params', extras_params)
				set_property('fen_unwatched_params', unwatched_params)
				set_property('fen_watched_params', watched_params)
				set_property('fen_clearprog_params', clearprog_params)
			else: set_property('fen_widget', 'false')
			append((url_params, listitem, False))
		except: pass
	__handle__ = int(argv[1])
	item_list = []
	append = item_list.append
	list_type_starts_with = list_type.startswith
	get_resumetime = indicators.get_resumetime
	get_watched_status = indicators.get_watched_status_episode
	meta_user_info, watched_indicators, watched_info, show_unaired, thumb_fanart, is_widget, current_date, adjust_hours, bookmarks = get_episode_info()
	display_title, date_format, art_keys, all_episodes = get_single_episode_info()
	show_all_episodes = all_episodes in (1, 2)
	poster_main, poster_backup, fanart_main, fanart_backup = settings.get_art_provider()
	ignore_articles = settings.ignore_articles()
	watched_title = 'Trakt' if watched_indicators == 1 else 'Fen'
	if list_type_starts_with('next_episode'):
		nextep_settings, nextep_display_settings = settings.nextep_content_settings(), settings.nextep_display_settings()
		unaired_color, unwatched_color = nextep_display_settings['unaired_color'], nextep_display_settings['unwatched_color']
		include_airdate = nextep_display_settings['include_airdate']
		include_unaired = nextep_settings['include_unaired']
		if watched_indicators == 1: resformat, resinsert = '%Y-%m-%dT%H:%M:%S.%fZ', '2000-01-01T00:00:00.000Z'
		else: resformat, resinsert = '%Y-%m-%d %H:%M:%S', '2000-01-01 00:00:00'
	threads = list(make_thread_list_enumerate(_process, data, Thread))
	[i.join() for i in threads]
	item_list = _sort_results(item_list)
	kodi_utils.add_items(__handle__, item_list)
	kodi_utils.set_content(__handle__, 'episodes')
	kodi_utils.end_directory(__handle__, cacheToDisc=False)
	kodi_utils.set_view_mode('view.episodes', 'episodes')
	if list_type == 'trakt_calendar' and settings.calendar_focus_today():
		today = '[%s]' % ls(32849).upper()
		try: index = max([i for i, x in enumerate([i[1].getLabel() for i in item_list]) if today in x])
		except: return
		kodi_utils.focus_index(index)

def get_episode_info():
	meta_user_info = metadata.retrieve_user_info()
	watched_indicators = settings.watched_indicators()
	watched_info = indicators.get_watched_info_tv(watched_indicators)
	show_unaired = settings.show_unaired()
	thumb_fanart = settings.thumb_fanart()
	is_widget = kodi_utils.external_browse()
	current_date = get_datetime()
	adjust_hours = settings.date_offset()
	bookmarks = indicators.get_bookmarks('episode', watched_indicators)
	return meta_user_info, watched_indicators, watched_info, show_unaired, thumb_fanart, is_widget, current_date, adjust_hours, bookmarks

def get_single_episode_info():
	display_title = settings.single_ep_display_title()
	date_format = settings.single_ep_format()
	art_keys = settings.get_art_provider()
	all_episodes = settings.default_all_episodes()
	return display_title, date_format, art_keys, all_episodes