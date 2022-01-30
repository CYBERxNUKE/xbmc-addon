# -*- coding: utf-8 -*-
from sys import argv
from threading import Thread
import metadata
from apis.trakt_api import get_trakt_movie_id
from modules import kodi_utils
from modules.meta_lists import oscar_winners
from modules.utils import manual_function_import, make_thread_list_enumerate
from modules.watched_status import get_watched_info_movie, get_watched_status_movie, get_resumetime, get_bookmarks
from modules import settings
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
remove_meta_keys = kodi_utils.remove_meta_keys
dict_removals = kodi_utils.movie_dict_removals
string = str
tmdb_main = ('tmdb_movies_popular','tmdb_movies_blockbusters','tmdb_movies_in_theaters', 'tmdb_movies_top_rated',
			'tmdb_movies_upcoming', 'tmdb_movies_latest_releases','tmdb_movies_premieres')
trakt_main = ('trakt_movies_trending','trakt_movies_anticipated','trakt_movies_top10_boxoffice')
trakt_personal = ('trakt_collection', 'trakt_watchlist', 'trakt_collection_lists')
imdb_personal = ('imdb_watchlist', 'imdb_user_list_contents', 'imdb_keywords_list_contents')
personal = ('in_progress_movies', 'favourites_movies', 'watched_movies')
similar = ('tmdb_movies_similar', 'tmdb_movies_recommendations')
tmdb_special = ('tmdb_movies_languages', 'tmdb_movies_networks', 'tmdb_movies_year', 'tmdb_movies_certifications')
tmdb_special_key_dict = {'tmdb_movies_languages': 'language', 'tmdb_movies_networks': 'company',
						'tmdb_movies_year': 'year', 'tmdb_movies_certifications': 'certification'}
item_jump = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/item_jump.png')
item_next = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/item_next.png')
poster_empty = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/box_office.png')
fanart_empty = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')
watched_str, unwatched_str, traktmanager_str = ls(32642), ls(32643), ls(32198)
favmanager_str, extras_str, options_str = ls(32197), ls(32645), ls(32646)
hide_str, exit_str, clearprog_str, play_str = ls(32648), ls(32649), ls(32651), '[B]%s...[/B]' % ls(32174)
nextpage_str, switchjump_str, jumpto_str, genre_str = ls(32799), ls(32784), ls(32964), ls(32847)
run_plugin = 'RunPlugin(%s)'
container_refresh = 'Container.Refresh(%s)'

class Movies:
	def __init__(self, params):
		self.params = params
		self.items = []
		self.new_page = {}
		self.total_pages = None
		self.exit_list_params = None
		self.is_widget = 'unchecked'
		self.id_type = 'tmdb_id'
		self.list = params.get('list', [])
		self.action = params.get('action', None)

	def fetch_list(self):
		try:
			params_get = self.params.get
			self.is_widget = kodi_utils.external_browse()
			self.exit_list_params = params_get('exit_list_params', None) or kodi_utils.get_infolabel('Container.FolderPath')
			self.handle = int(argv[1])
			content_type = 'movies'
			mode = params_get('mode')
			try: page_no = int(params_get('new_page', '1'))
			except ValueError: page_no = params_get('new_page')
			letter = params_get('new_letter', 'None')
			list_append = self.list.append
			if self.action in personal:
				if self.action == 'favourites_movies': var_module, import_function = 'modules.favourites', 'retrieve_favourites'
				elif self.action == 'in_progress_movies': var_module, import_function = 'modules.watched_status', 'get_in_progress_movies'
				else: var_module, import_function = 'modules.watched_status', 'get_watched_items'
			else: var_module, import_function = 'apis.%s_api' % self.action.split('_')[0], self.action
			try: function = manual_function_import(var_module, import_function)
			except: pass
			if self.action in tmdb_main:
				data = function(page_no)
				for item in data['results']: list_append(item['id'])
				self.new_page = {'new_page': string((data['page'] if 'tmdb' in self.action else page_no) + 1)}
			elif self.action in trakt_main:
				data = function(page_no)
				for item in data: list_append(get_trakt_movie_id(item['movie']['ids']))
				if self.action not in ('trakt_movies_top10_boxoffice'):
					self.new_page = {'new_page': string((data['page'] if 'tmdb' in self.action else page_no) + 1)}
			elif self.action in trakt_personal:
				data, total_pages = function('movies', page_no, letter)
				self.list = [i['media_id'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				try:
					if total_pages > page_no: self.new_page = {'new_page': string(page_no + 1), 'new_letter': letter}
				except: pass
			elif self.action in imdb_personal:
				self.id_type = 'imdb_id'
				list_id = params_get('list_id', None)
				data, next_page = function('movie', list_id, page_no)
				self.list = [i['imdb_id'] for i in data]
				if next_page:
					self.new_page = {'list_id': list_id, 'new_page': string(page_no + 1), 'new_letter': letter}
			elif self.action in personal:
				data, total_pages = function('movie', page_no, letter)
				self.list = [i['media_id'] for i in data]
				if total_pages > 2: self.total_pages = total_pages
				if total_pages > page_no:
					self.new_page = {'new_page': string(page_no + 1), 'new_letter': letter}
			elif self.action in similar:
				tmdb_id = params_get('tmdb_id')
				data = function(tmdb_id, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['page'] < data['total_pages']:
					self.new_page = {'new_page': string(data['page'] + 1), 'tmdb_id': tmdb_id}
			elif self.action in tmdb_special:
				key = tmdb_special_key_dict[self.action]
				function_var = params_get(key, None)
				if not function_var: return
				data = function(function_var, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['page'] < data['total_pages']:
					self.new_page = {'new_page': string(data['page'] + 1), key: function_var}
			elif self.action == 'tmdb_movies_discover':
				from indexers.discover import set_history
				name = self.params['name']
				query = self.params['query']
				if page_no == 1: set_history('movie', name, query)
				data = function(query, page_no)
				for item in data['results']: list_append(item['id'])
				if data['page'] < data['total_pages']:
					self.new_page = {'query': query, 'name': name, 'new_page': string(data['page'] + 1)}
			elif self.action == 'imdb_movies_oscar_winners':
				self.list = oscar_winners
			elif self.action == 'trakt_movies_mosts':
				for item in (function(self.params['period'], self.params['duration'], page_no)): list_append(get_trakt_movie_id(item['movie']['ids']))
				self.new_page = {'period': self.params['period'], 'duration': self.params['duration'], 'new_page': string(page_no + 1)}
			elif self.action == 'trakt_movies_related':
				imdb_id = params_get('imdb_id')
				data, total_pages = function(imdb_id, page_no)
				for item in data: list_append(get_trakt_movie_id(item['ids']))
				if total_pages > page_no:
					self.new_page = {'new_page': string(page_no + 1), 'imdb_id': imdb_id}
			elif self.action == 'tmdb_movies_genres':
				genre_id = self.params['genre_id'] if 'genre_id' in self.params else self.multiselect_genres(params_get('genre_list'))
				if not genre_id: return
				data = function(genre_id, page_no)
				self.list = [i['id'] for i in data['results']]
				if data['page'] < data['total_pages']:
					self.new_page = {'new_page': string(data['page'] + 1), 'genre_id': genre_id}
			elif self.action == 'trakt_recommendations':
				for item in function('movies'): list_append(get_trakt_movie_id(item['ids']))
			elif self.action  == 'tmdb_movies_search':
				query = self.params['query']
				data = function(query, page_no)
				total_pages = data['total_pages']
				if total_pages > page_no:
					self.new_page = {'new_page': string(page_no + 1), 'new_letter': letter, 'query': query}
				self.list = [i['id'] for i in data['results']]
			elif self.action  == 'trakt_movies_search':
				query = self.params['query']
				data, total_pages = function(query, page_no, letter)
				for item in data: list_append(get_trakt_movie_id(item['movie']['ids']))
				if total_pages > page_no:
					self.new_page = {'new_page': string(page_no + 1), 'new_letter': letter, 'query': query}
			if self.total_pages and not self.is_widget:
				url_params = {'mode': 'build_navigate_to_page', 'db_type': 'Movies', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode,
							'transfer_action': self.action, 'query': params_get('search_name', ''), 'actor_id': params_get('actor_id', '')}
				self.add_dir(url_params, jumpto_str, item_jump, False)
			kodi_utils.add_items(self.handle, self.worker())
			if self.new_page:
					self.new_page.update({'mode': mode, 'action': self.action, 'exit_list_params': self.exit_list_params})
					self.add_dir(self.new_page)
		except: pass
		kodi_utils.set_content(self.handle, content_type)
		kodi_utils.end_directory(self.handle)
		kodi_utils.set_view_mode('view.movies', content_type)
	
	def build_movie_content(self, item_position, _id):
		try:
			cm = []
			cm_append = cm.append
			meta, playcount = self.set_meta(_id)
			meta_get = meta.get
			listitem = make_listitem()
			set_property = listitem.setProperty
			rootname = meta_get('rootname')
			tmdb_id = meta_get('tmdb_id')
			imdb_id = meta_get('imdb_id')
			title = meta_get('title')
			year = meta_get('year')
			poster = meta_get(self.poster_main) or meta_get(self.poster_backup) or poster_empty
			fanart = meta_get(self.fanart_main) or meta_get(self.fanart_backup) or fanart_empty
			resumetime = get_resumetime(self.bookmarks, tmdb_id)
			play_params = build_url({'mode': 'play_media', 'vid_type': 'movie', 'tmdb_id': tmdb_id})
			extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'db_type': 'movie', 'is_widget': self.is_widget})
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'movie', 'tmdb_id': tmdb_id})
			trakt_manager_params = build_url({'mode': 'trakt_manager_choice', 'tmdb_id': tmdb_id, 'imdb_id': imdb_id, 'tvdb_id': 'None', 'db_type': 'movie'})
			fav_manager_params = build_url({'mode': 'favorites_choice', 'db_type': 'movie', 'tmdb_id': tmdb_id, 'title': title})
			if self.open_extras:
				url_params = extras_params
				cm.append((play_str, run_plugin % play_params))
			else:
				url_params = play_params
				cm_append((extras_str, run_plugin % extras_params))
			cm_append((options_str, run_plugin % options_params))
			cm_append((traktmanager_str, run_plugin % trakt_manager_params))
			cm_append((favmanager_str, run_plugin % fav_manager_params))
			clearprog_params, unwatched_params, watched_params = '', '', ''
			if resumetime != '0':
				clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'db_type': 'movie', 'tmdb_id': tmdb_id, 'refresh': 'true'})
				cm_append((clearprog_str, run_plugin % clearprog_params))
				set_property('fen_in_progress', 'true')
			if playcount:
				unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_movie', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id, 'title': title, 'year': year})
				cm_append((unwatched_str % self.watched_title, run_plugin % unwatched_params))
			else:
				watched_params = build_url({'mode': 'mark_as_watched_unwatched_movie', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id, 'title': title, 'year': year})
				cm_append((watched_str % self.watched_title, run_plugin % watched_params))
			cm_append((exit_str, container_refresh % self.exit_list_params))
			listitem.setLabel(rootname if self.include_year_in_title else title)
			listitem.setContentLookup(False)
			listitem.addContextMenuItems(cm)
			listitem.setCast(meta_get('cast'))
			listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id)})
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': meta_get('banner'), 'clearart': meta_get('clearart'),
							'clearlogo': meta_get('clearlogo'), 'landscape': meta_get('landscape'), 'discart': meta_get('discart')})
			listitem.setInfo('Video', remove_meta_keys(meta, dict_removals))
			set_property('resumetime', resumetime)
			set_property('fen_tmdb_id', string(tmdb_id))
			set_property('fen_db_type', 'movie')
			set_property('fen_sort_order', string(item_position))
			if self.is_widget:
				set_property('fen_widget', 'true')
				set_property('fen_playcount', string(playcount))
				set_property('fen_extras_menu_params', extras_params)
				set_property('fen_options_menu_params', options_params)
				set_property('fen_trakt_manager_params', trakt_manager_params)
				set_property('fen_fav_manager_params', fav_manager_params)
				set_property('fen_unwatched_params', unwatched_params)
				set_property('fen_watched_params', watched_params)
				set_property('fen_clearprog_params', clearprog_params)
			else: set_property('fen_widget', 'false')
			self.append((url_params, listitem, False))
		except: pass

	def set_meta(self, _id):
		meta = metadata.movie_meta(self.id_type, _id, self.meta_user_info)
		if not meta: return
		playcount, overlay = get_watched_status_movie(self.watched_info, string(meta['tmdb_id']))
		meta.update({'playcount': playcount, 'overlay': overlay})
		return meta, playcount

	def worker(self):
		if self.is_widget == 'unchecked': self.is_widget = kodi_utils.external_browse()
		if not self.exit_list_params: self.exit_list_params = kodi_utils.get_infolabel('Container.FolderPath')
		self.get_info()
		self.watched_title = 'Trakt' if self.watched_indicators == 1 else 'Fen'
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = settings.get_art_provider()
		self.append = self.items.append
		threads = list(make_thread_list_enumerate(self.build_movie_content, self.list, Thread))
		[i.join() for i in threads]
		self.items.sort(key=lambda k: int(k[1].getProperty('fen_sort_order')))
		return self.items

	def get_info(self):
		self.meta_user_info = metadata.retrieve_user_info()
		self.watched_indicators = settings.watched_indicators()
		self.watched_info = get_watched_info_movie(self.watched_indicators)
		self.bookmarks = get_bookmarks('movie', self.watched_indicators)
		self.include_year_in_title = settings.include_year_in_title('movie')
		self.open_extras = settings.extras_open_action('movie')

	def multiselect_genres(self, genre_list):
		import json
		from modules.kodi_utils import select_dialog
		def _builder():
			for genre, value in sorted(genre_list.items()):
				append(value[0])
				yield {'line1': genre, 'icon': kodi_utils.translate_path(icon_directory % value[1])}
		function_list = []
		append = function_list.append
		icon_directory = 'special://home/addons/script.tikiart/resources/media/%s'
		genre_list = json.loads(genre_list)
		list_items = list(_builder())
		kwargs = {'items': json.dumps(list_items), 'heading': genre_str, 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false'}
		genre_ids = select_dialog(function_list, **kwargs)
		if genre_ids == None: return
		return ','.join(genre_ids)

	def get_company(self, company_name):
		from apis.tmdb_api import tmdb_company_id
		company_choice = None
		try:
			results = tmdb_company_id(company_name)
			if results['total_results'] == 1: return results['results'][0]
			try: company_choice = [i for i in results['results'] if i['name'] == company_name][0]
			except: pass
		except: pass
		return company_choice

	def add_dir(self, url_params, list_name=nextpage_str, iconImage=item_next, isFolder=True):
		url = build_url(url_params)
		listitem = make_listitem()
		listitem.setLabel(list_name)
		set_property = listitem.setProperty
		listitem.setArt({'icon': iconImage, 'fanart': fanart_empty})
		if url_params['mode'] == 'build_navigate_to_page':
			set_property('SpecialSort', 'top')
			listitem.addContextMenuItems([(switchjump_str, run_plugin % build_url({'mode': 'toggle_jump_to'}))])
		else:
			set_property('SpecialSort', 'bottom')
		kodi_utils.add_item(self.handle, url, listitem, isFolder)
