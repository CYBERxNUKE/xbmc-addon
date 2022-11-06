# -*- coding: utf-8 -*-
from metadata import movie_meta, movieset_meta
from modules import kodi_utils, settings
from modules.meta_lists import oscar_winners
from modules.utils import manual_function_import, get_datetime, make_thread_list_enumerate, adjust_premiered_date, get_current_timestamp
from modules.watched_status import get_watched_info_movie, get_watched_status_movie, get_bookmarks, get_progress_percent
# logger = kodi_utils.logger

meta_function, get_datetime_function, add_item, select_dialog, fen_clearlogo = movie_meta, get_datetime, kodi_utils.add_item, kodi_utils.select_dialog, kodi_utils.addon_clearlogo
progress_percent_function, get_watched_function, get_watched_info_function = get_progress_percent, get_watched_status_movie, get_watched_info_movie
set_content, end_directory, set_view_mode, get_infolabel = kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.set_view_mode, kodi_utils.get_infolabel
string, ls, sys, external_browse, add_items, add_dir = str, kodi_utils.local_string, kodi_utils.sys, kodi_utils.external_browse, kodi_utils.add_items, kodi_utils.add_dir
make_listitem, build_url, remove_meta_keys, dict_removals = kodi_utils.make_listitem, kodi_utils.build_url, kodi_utils.remove_meta_keys, kodi_utils.movie_dict_removals
poster_empty, fanart_empty, build_content = kodi_utils.empty_poster, kodi_utils.addon_fanart, kodi_utils.build_content
metadata_user_info, watched_indicators, page_reference, date_offset = settings.metadata_user_info, settings.watched_indicators, settings.page_reference, settings.date_offset
sleep, extras_open_action, get_art_provider, get_resolution = kodi_utils.sleep, settings.extras_open_action, settings.get_art_provider, settings.get_resolution
max_threads, widget_hide_next_page = settings.max_threads, settings.widget_hide_next_page
fen_str, trakt_str, watched_str, unwatched_str, extras_str, options_str = ls(32036), ls(32037), ls(32642), ls(32643), ls(32645), ls(32646)
hide_str, exit_str, clearprog_str, nextpage_str, jumpto_str, play_str = ls(32648), ls(32649), ls(32651), ls(32799), ls(32964), '[B]%s...[/B]' % ls(32174)
addmenu_str, addshortcut_str, add_coll_str = ls(32730), ls(32731), ls(33081)
run_plugin, container_refresh, container_update = 'RunPlugin(%s)', 'Container.Refresh(%s)', 'Container.Update(%s)'
tmdb_main = ('tmdb_movies_popular','tmdb_movies_blockbusters','tmdb_movies_in_theaters', 'tmdb_movies_upcoming', 'tmdb_movies_latest_releases', 'tmdb_movies_premieres')
trakt_main = ('trakt_movies_trending', 'trakt_movies_trending_recent', 'trakt_movies_most_watched', 'trakt_movies_top10_boxoffice', 'trakt_recommendations')
trakt_personal = ('trakt_collection', 'trakt_watchlist', 'trakt_collection_lists')
imdb_personal  = ('imdb_watchlist', 'imdb_user_list_contents', 'imdb_keywords_list_contents')
tmdb_special = {'tmdb_movies_languages': 'language', 'tmdb_movies_networks': 'company', 'tmdb_movies_year': 'year', 'tmdb_movies_decade': 'decade',
				'tmdb_movies_certifications': 'certification', 'tmdb_movies_recommendations': 'tmdb_id', 'tmdb_movies_genres': 'genre_id', 'tmdb_movies_search': 'query',
				'tmdb_movies_search_sets': 'query'}
personal = {'in_progress_movies': ('modules.watched_status', 'get_in_progress_movies'), 'favourites_movies': ('modules.favourites', 'get_favourites'),
				'watched_movies': ('modules.watched_status', 'get_watched_items'), 'recent_watched_movies': ('modules.watched_status', 'get_recently_watched')}
view_mode, content_type = 'view.movies', 'movies'

class Movies:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.id_type, self.list, self.action = self.params_get('id_type', 'tmdb_id'), self.params_get('list', []), self.params_get('action', None)
		self.items, self.new_page, self.total_pages, self.is_widget, self.max_threads = [], {}, None, external_browse(), max_threads()
		self.widget_hide_next_page = False if not self.is_widget else widget_hide_next_page()
		self.exit_list_params = self.params_get('exit_list_params', None) or get_infolabel('Container.FolderPath')
		self.append = self.items.append

	def fetch_list(self):
		handle = int(sys.argv[1])
		if build_content():
			try:
				builder, mode = self.worker, self.params_get('mode')
				try: page_no = int(self.params_get('new_page', '1'))
				except ValueError: page_no = self.params_get('new_page')
				if self.action in personal: var_module, import_function = personal[self.action]
				else: var_module, import_function = 'apis.%s_api' % self.action.split('_')[0], self.action
				try: function = manual_function_import(var_module, import_function)
				except: pass
				if self.action in tmdb_main:
					data = function(page_no)
					self.list = [i['id'] for i in data['results']]
					self.new_page = {'new_page': string(data['page'] + 1)}
				elif self.action in tmdb_special:
					if self.action == 'tmdb_movies_search_sets': builder = self.movie_sets_worker
					key = tmdb_special[self.action]
					function_var = self.params_get(key, None)
					if not function_var: return
					data = function(function_var, page_no)
					self.list = [i['id'] for i in data['results']]
					if data['total_pages'] > page_no: self.new_page = {'new_page': string(data['page'] + 1), key: function_var}
				elif self.action in personal:
					data, all_pages, total_pages = function('movie', page_no)
					self.list = [i['media_id'] for i in data]
					if total_pages > 2: self.total_pages = total_pages
					if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1)}
				elif self.action in trakt_main:
					self.id_type = 'trakt_dict'
					data = function(page_no)
					try: self.list = [i['movie']['ids'] for i in data]
					except: self.list = [i['ids'] for i in data]
					if self.action not in ('trakt_movies_top10_boxoffice', 'trakt_recommendations'): self.new_page = {'new_page': string(page_no + 1)}
				elif self.action in trakt_personal:
					self.id_type = 'trakt_dict'
					data, all_pages, total_pages = function('movies', page_no)
					self.list = [i['media_ids'] for i in data]
					if total_pages > 2: self.total_pages = total_pages
					try:
						if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1)}
					except: pass
				elif self.action in imdb_personal:
					self.id_type = 'imdb_id'
					list_id = self.params_get('list_id', None)
					data, next_page = function('movie', list_id, page_no)
					self.list = [i['imdb_id'] for i in data]
					if next_page: self.new_page = {'list_id': list_id, 'new_page': string(page_no + 1)}
				elif self.action == 'tmdb_movies_discover':
					name, query = self.params_get('name'), self.params_get('query')
					if page_no == 1:
						from indexers.discover import set_history
						set_history('movie', name, query)
					data = function(query, page_no)
					self.list = [i['id'] for i in data['results']]
					if data['total_pages'] > page_no: self.new_page = {'query': query, 'name': name, 'new_page': string(data['page'] + 1)}
				elif self.action  == 'tmdb_movies_sets':
					data = sorted(movieset_meta(self.params_get('tmdb_id'), metadata_user_info())['parts'], key=lambda k: k['release_date'] or '2050')
					self.list = [i['id'] for i in data]
				elif self.action == 'imdb_movies_oscar_winners':
					data = oscar_winners
					self.list = data[page_no-1]
					if len(data) > page_no: self.new_page = {'new_page': string(page_no + 1)}
				if self.total_pages and not self.is_widget:
					page_ref = page_reference()
					if page_ref != 3:
						url_params = {'mode': 'navigate_to_page_choice', 'media_type': 'Movies', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode,
									'transfer_action': self.action, 'query': self.params_get('search_name', ''), 'all_pages': all_pages, 'page_reference': page_ref}
						add_dir(url_params, jumpto_str, handle, 'item_jump', isFolder=False)
				add_items(handle, builder())
				if self.new_page and not self.widget_hide_next_page:
					self.new_page.update({'mode': mode, 'action': self.action, 'exit_list_params': self.exit_list_params})
					add_dir(self.new_page, nextpage_str % self.new_page['new_page'], handle, 'item_next')
			except: pass
		set_content(handle, content_type)
		end_directory(handle, False if self.is_widget else None)
		if self.params_get('refreshed') == 'true': sleep(1000)
		if not self.is_widget: set_view_mode(view_mode, content_type)

	def build_movie_content(self, item_position, _id):
		try:
			meta = meta_function(self.id_type, _id, self.meta_user_info, self.current_date, self.current_time)
			if not meta or 'blank_entry' in meta: return
			meta_get = meta.get
			playcount, overlay = get_watched_function(self.watched_info, string(meta_get('tmdb_id')))
			meta.update({'playcount': playcount, 'overlay': overlay})
			cm = []
			cm_append = cm.append
			listitem = make_listitem()
			set_properties = listitem.setProperties
			clearprog_params, watched_unwatched_params = '', ''
			title, year = meta_get('title'), meta_get('year')
			tmdb_id, imdb_id = meta_get('tmdb_id'), meta_get('imdb_id')
			poster = meta_get('custom_poster') or meta_get(self.poster_main) or meta_get(self.poster_backup) or poster_empty
			fanart = meta_get('custom_fanart') or meta_get(self.fanart_main) or meta_get(self.fanart_backup) or fanart_empty
			clearlogo = meta_get('custom_clearlogo') or meta_get(self.clearlogo_main) or meta_get(self.clearlogo_backup) or ''
			progress = progress_percent_function(self.bookmarks, tmdb_id)
			if playcount:
				if self.widget_hide_watched: return
				watched_action, watchedstr = 'mark_as_unwatched', unwatched_str
			else: watched_action, watchedstr = 'mark_as_watched', watched_str
			watched_unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_movie', 'action': watched_action, 'tmdb_id': tmdb_id, 'title': title, 'year': year})
			play_params = build_url({'mode': 'play_media', 'media_type': 'movie', 'tmdb_id': tmdb_id})
			extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'movie', 'is_widget': self.is_widget})
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'movie', 'tmdb_id': tmdb_id, 'poster': poster, 'playcount': playcount,
										'progress': progress, 'exit_menu': self.exit_list_params, 'is_widget': self.is_widget})
			if self.fanart_enabled: banner, clearart, landscape, discart = meta_get('banner'), meta_get('clearart'), meta_get('landscape'), meta_get('discart')
			else: banner, clearart, landscape, discart = '', '', '', ''
			if self.open_extras:
				url_params = extras_params
				cm_append((play_str, run_plugin % play_params))
			else:
				url_params = play_params
				cm_append((extras_str, run_plugin % extras_params))
			cm_append((options_str, run_plugin % options_params))
			if progress:
				clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'media_type': 'movie', 'tmdb_id': tmdb_id, 'refresh': 'true'})
				set_properties({'WatchedProgress': progress, 'resumetime': progress, 'fen_in_progress': 'true'})
				cm_append((clearprog_str, run_plugin % clearprog_params))
			cm_append((watchedstr % self.watched_title, run_plugin % watched_unwatched_params))
			cm_append((exit_str, container_refresh % self.exit_list_params))
			listitem.setLabel(title)
			listitem.addContextMenuItems(cm)
			listitem.setCast(meta_get('cast', []))
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id)})
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart,
							'clearlogo': clearlogo, 'landscape': landscape, 'discart': discart})
			listitem.setInfo('video', remove_meta_keys(meta, dict_removals))
			set_properties({'fen_sort_order': string(item_position), 'fen_playcount': string(playcount), 'fen_extras_params': extras_params, 'fen_clearprog_params': clearprog_params,
							'fen_options_params': options_params, 'fen_unwatched_params': watched_unwatched_params, 'fen_watched_params': watched_unwatched_params})
			if self.is_widget: set_properties({'fen_widget': 'true'})
			self.append((url_params, listitem, False))
		except: pass

	def worker(self):
		self.current_date, self.current_time = get_datetime_function(), get_current_timestamp()
		self.meta_user_info, self.watched_indicators = metadata_user_info(), watched_indicators()
		self.watched_info, self.bookmarks = get_watched_info_function(self.watched_indicators), get_bookmarks(self.watched_indicators, 'movie')
		self.open_extras, self.watched_title = extras_open_action('movie'), trakt_str if self.watched_indicators == 1 else fen_str
		self.fanart_enabled, self.widget_hide_watched = self.meta_user_info['extra_fanart_enabled'], self.is_widget and self.meta_user_info['widget_hide_watched']
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup, self.clearlogo_main, self.clearlogo_backup = get_art_provider()
		threads = list(make_thread_list_enumerate(self.build_movie_content, self.list, self.max_threads))
		[i.join() for i in threads]
		self.items.sort(key=lambda k: int(k[1].getProperty('fen_sort_order')))
		return self.items

	def build_movie_sets_content(self, item_position, _id):
		try:
			cm = []
			cm_append = cm.append
			meta = movieset_meta(_id, self.meta_user_info, self.current_date)
			if not meta or 'blank_entry' in meta: return
			meta_get = meta.get
			parts = meta_get('parts')
			if len(parts) <= 1: return
			if len([i for i in parts if i['release_date'] and adjust_premiered_date(i['release_date'], self.adjust_hours)[0] <= self.current_date]) <= 1: return
			title, plot, tmdb_id = meta_get('title'), meta_get('plot'), meta_get('tmdb_id')
			poster = meta_get(self.poster_main) or meta_get(self.poster_backup) or poster_empty
			fanart = meta_get(self.fanart_main) or meta_get(self.fanart_backup) or fanart_empty
			clearlogo = meta_get('clearlogo2') or fen_clearlogo
			if self.fanart_enabled: banner, clearart, landscape, discart = meta_get('banner'), meta_get('clearart'), meta_get('landscape'), meta_get('discart')
			else: banner, clearart, landscape, discart = '', '', '', ''
			url_params = build_url({'mode': 'build_movie_list', 'action': 'tmdb_movies_sets', 'tmdb_id': tmdb_id})
			listitem = make_listitem()
			cm_append((addmenu_str, run_plugin % build_url({'mode': 'menu_editor.add_external', 'name': title, 'iconImage': poster})))
			cm_append((addshortcut_str, run_plugin % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': title, 'iconImage': poster})))
			cm_append((add_coll_str, run_plugin % build_url({'mode': 'movie_sets_to_collection_choice', 'collection_id': tmdb_id})))
			listitem.setLabel(title)
			listitem.addContextMenuItems(cm)
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart,
							'clearlogo': clearlogo, 'landscape': landscape, 'discart': discart})
			listitem.setInfo('video', {'mediatype': 'movie', 'plot': plot})
			listitem.setProperty('fen_sort_order', string(item_position))
			self.append((url_params, listitem, True))
		except: pass

	def movie_sets_worker(self):
		self.meta_user_info, self.current_date, self.current_time, self.adjust_hours = metadata_user_info(), get_datetime_function(), get_current_timestamp(), date_offset()
		self.fanart_enabled = self.meta_user_info['extra_fanart_enabled']
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = get_art_provider()[0:4]
		threads = list(make_thread_list_enumerate(self.build_movie_sets_content, self.list, self.max_threads))
		[i.join() for i in threads]
		self.items.sort(key=lambda k: int(k[1].getProperty('fen_sort_order')))
		return self.items
