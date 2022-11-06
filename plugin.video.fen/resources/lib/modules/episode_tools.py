# -*- coding: utf-8 -*-
from random import choice
from datetime import date
from apis.trakt_api import trakt_get_hidden_items
from metadata import season_episodes_meta, all_episodes_meta
from modules import kodi_utils, settings
from modules.sources import Sources
from modules.watched_status import get_next_episodes, get_watched_info_tv
from modules.utils import adjust_premiered_date, get_datetime, make_thread_list, title_key
# logger = kodi_utils.logger

ls, sys, build_url, json, notification, focus_index = kodi_utils.local_string, kodi_utils.sys, kodi_utils.build_url, kodi_utils.json, kodi_utils.notification, kodi_utils.focus_index 
Thread, get_property, set_property, add_dir, add_items = kodi_utils.Thread, kodi_utils.get_property, kodi_utils.set_property, kodi_utils.add_dir, kodi_utils.add_items
make_listitem, set_content, end_directory, set_view_mode = kodi_utils.make_listitem, kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.set_view_mode
trakt_icon, addon_fanart, fen_clearlogo = kodi_utils.get_icon('trakt'), kodi_utils.addon_fanart, kodi_utils.addon_clearlogo
included_str, excluded_str, heading, window_prop = ls(32804).upper(), ls(32805).upper(), ls(32806), 'fen.random_episode_history'

def build_next_episode_manager():
	def build_content(item):
		try:
			listitem = make_listitem()
			tmdb_id, title = item['media_ids']['tmdb'], item['title']
			if tmdb_id in exclude_list: color, action, status, sort_value = 'red', 'unhide', excluded_str, 1
			else: color, action, status, sort_value = 'green', 'hide', included_str, 0
			display = '[COLOR=%s][%s][/COLOR] %s' % (color, status, title)
			url_params = {'mode': 'trakt.hide_unhide_trakt_items', 'action': action, 'media_type': 'shows', 'media_id': tmdb_id, 'section': 'progress_watched'}
			url = build_url(url_params)
			listitem.setLabel(display)
			listitem.setArt({'poster': trakt_icon, 'fanart': addon_fanart, 'icon': trakt_icon, 'clearlogo': fen_clearlogo})
			listitem.setInfo('video', {'plot': ' '})
			append({'listitem': (url, listitem, False), 'sort_value': sort_value, 'sort_title': title})
		except: pass
	handle = int(sys.argv[1])
	list_items = []
	append = list_items.append
	show_list = get_next_episodes(get_watched_info_tv(1))
	try: exclude_list = trakt_get_hidden_items('progress_watched')
	except: exclude_list = []
	threads = list(make_thread_list(build_content, show_list))
	[i.join() for i in threads]
	item_list = sorted(list_items, key=lambda k: (k['sort_value'], title_key(k['sort_title'], settings.ignore_articles())), reverse=False)
	item_list = [i['listitem'] for i in item_list]
	add_dir({'mode': 'nill'}, '[I][COLOR=grey2]%s[/COLOR][/I]' % heading.upper(), handle, iconImage='settings', isFolder=False)
	add_items(handle, item_list)
	set_content(handle, '')
	end_directory(handle, cacheToDisc=False)
	set_view_mode('view.main', '')
	focus_index(1)

class EpisodeTools:
	def __init__(self, meta, nextep_settings=None):
		self.meta = meta
		self.meta_get = self.meta.get
		self.nextep_settings = nextep_settings

	def execute_nextep(self):
		try:
			current_date = get_datetime()
			season_data = self.meta_get('season_data')
			current_season, current_episode = int(self.meta_get('season')), int(self.meta_get('episode'))
			curr_season_data = [i for i in season_data if i['season_number'] == current_season][0]
			season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
			episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
			ep_data = season_episodes_meta(season, self.meta, settings.metadata_user_info())
			if not ep_data: url_params = 'no_next_episode'
			ep_data = [i for i in ep_data if i['episode'] == episode][0]
			airdate = ep_data['premiered']
			d = airdate.split('-')
			episode_date = date(int(d[0]), int(d[1]), int(d[2]))
			if current_date < episode_date: url_params = 'no_next_episode'
			custom_title = self.meta_get('custom_title', None)
			title = custom_title or self.meta_get('title')
			display_name = '%s - %dx%.2d' % (title, int(season), int(episode))
			self.meta.update({'media_type': 'episode', 'rootname': display_name, 'season': season, 'ep_name': ep_data['title'],
						'episode': episode, 'premiered': airdate, 'plot': ep_data['plot']})
			url_params = {'media_type': 'episode', 'tmdb_id': self.meta_get('tmdb_id'), 'tvshowtitle': self.meta_get('rootname'), 'season': season,
						'episode': episode, 'background': 'true', 'nextep_settings': self.nextep_settings, 'play_type': 'next_episode', 'meta': json.dumps(self.meta)}
			if custom_title: url_params['custom_title'] = custom_title
			if 'custom_year' in self.meta: url_params['custom_year'] = self.meta_get('custom_year')
		except: url_params = 'error'
		if url_params == 'error': return notification('%s %s' % (ls(33041), ls(32574)), 3000)
		elif url_params == 'no_next_episode': return
		return Sources().playback_prep(url_params)

	def get_random_episode(self, continual=False, first_run=True):
		try:
			meta_user_info, adjust_hours, current_date = settings.metadata_user_info(), settings.date_offset(), get_datetime()
			tmdb_id = self.meta_get('tmdb_id')
			tmdb_key = str(tmdb_id)		
			try: episodes_data = [i for i in all_episodes_meta(self.meta, meta_user_info) if i['premiered'] and adjust_premiered_date(i['premiered'], adjust_hours)[0] <= current_date]
			except: return None
			if continual:
				episode_list = []
				try:
					episode_history = json.loads(get_property(window_prop))
					if tmdb_key in episode_history: episode_list = episode_history[tmdb_key]
					else: set_property(window_prop, '')
				except: pass
				episodes_data = [i for i in episodes_data if not i in episode_list]
				if not episodes_data:
					set_property(window_prop, '')
					return self.get_random_episode(continual=True)
			chosen_episode = choice(episodes_data)
			if continual:
				episode_list.append(chosen_episode)
				episode_history = {str(tmdb_id): episode_list}
				set_property(window_prop, json.dumps(episode_history))
			title, season, episode = self.meta['title'], int(chosen_episode['season']), int(chosen_episode['episode'])
			query = title + ' S%.2dE%.2d' % (season, episode)
			display_name = '%s - %dx%.2d' % (title, season, episode)
			ep_name, plot = chosen_episode['title'], chosen_episode['plot']
			try: premiered = adjust_premiered_date(chosen_episode['premiered'], adjust_hours)[1]
			except: premiered = chosen_episode['premiered']
			self.meta.update({'media_type': 'episode', 'rootname': display_name, 'season': season, 'ep_name': ep_name,
							'episode': episode, 'premiered': premiered, 'plot': plot})
			url_params = {'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'tvshowtitle': self.meta_get('rootname'), 'season': season, 'episode': episode,
						'autoplay': 'true', 'meta': json.dumps(self.meta)}
			if continual: url_params['random_continual'] = 'true'
			else: url_params['random'] = 'true'
			if not first_run:
				url_params['background'] = 'true'
				url_params['play_type'] = 'random_continual'
		except: url_params = 'error'
		return url_params

	def play_random(self):
		url_params = self.get_random_episode()
		if url_params == 'error': return notification('%s %s' % (ls(32541), ls(32574)), 3000)
		return Sources().playback_prep(url_params)

	def play_random_continual(self, first_run=True):
		url_params = self.get_random_episode(continual=True, first_run=first_run)
		if url_params == 'error': return notification('%s %s' % (ls(32542), ls(32574)), 3000)
		return Sources().playback_prep(url_params)
