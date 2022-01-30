# -*- coding: utf-8 -*-
import json
import time
import requests
from myaccounts.modules.trakt import Trakt
from metadata import movie_meta_external_id, tvshow_meta_external_id
from caches import check_databases, trakt_cache
from caches.main_cache import cache_object
from modules import kodi_utils
from modules.nav_utils import paginate_list
from modules.utils import to_utf8, sort_list, sort_for_article, jsondate_to_datetime as js2date
from modules.settings_reader import get_setting
from modules import settings
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
ma_trakt = Trakt()
trakt_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/trakt.png')
trakt_str = ls(32037)
API_ENDPOINT = 'https://api.trakt.tv/%s'
CLIENT_ID = ma_trakt.client_id

def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, method=None, pagination=False, page=1, suppress_error_notification=False):
	def error_notification(line1, error):
		if suppress_error_notification: return
		return kodi_utils.notification('%s: %s' % (line1, error[0:50]), 3000, trakt_icon)
	def send_query():
		resp = None
		if with_auth:
			try:
				ma_addon = kodi_utils.ext_addon('script.module.myaccounts')
				expires_at = float(ma_addon.getSetting('trakt.expires'))
				if time.time() > expires_at:
					trakt_refresh_token()
			except: pass
			token = ma_addon.getSetting('trakt.token')
			if token: headers['Authorization'] = 'Bearer ' + token
		try:
			if method:
				if method == 'post':
					resp = requests.post(API_ENDPOINT % path, headers=headers, timeout=timeout)
				elif method == 'delete':
					resp = requests.delete(API_ENDPOINT % path, headers=headers, timeout=timeout)
				elif method == 'sort_by_headers':
					resp = requests.get(API_ENDPOINT % path, params, headers=headers, timeout=timeout)
			elif data is not None:
				assert not params
				resp = requests.post(API_ENDPOINT % path, json=data, headers=headers, timeout=timeout)
			elif is_delete:
				resp = requests.delete(API_ENDPOINT % path, headers=headers, timeout=timeout)
			else:
				resp = requests.get(API_ENDPOINT % path, params, headers=headers, timeout=timeout)
			resp.raise_for_status()
		except requests.exceptions.RequestException as e:
			return error_notification('Trakt Error', str(e))
		except Exception as e:
			return error_notification('', str(e))
		return resp
	params = dict([(k, to_utf8(v)) for k, v in params.items() if v])
	timeout = 15.0
	numpages = 0
	headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
	if pagination: params['page'] = page
	response = send_query()
	response.raise_for_status()
	if response.status_code == 401:
		if kodi_utils.player.isPlaying() == False:
			if with_auth and kodi_utils.confirm_dialog(heading='%s %s' % (ls(32057), trakt_str), text=32741) and trakt_authenticate():
				response = send_query()
			else: pass
		else: return
	if response.status_code == 429:
		headers = response.headers
		if 'Retry-After' in headers:
			kodi_utils.sleep(1000 * headers['Retry-After'])
			response = send_query()
	response.encoding = 'utf-8'
	try: result = response.json()
	except: result = None
	if method == 'sort_by_headers':
		headers = response.headers
		if 'X-Sort-By' in headers and 'X-Sort-How' in headers:
			result = sort_list(headers['X-Sort-By'], headers['X-Sort-How'], result, settings.ignore_articles())
	if pagination: return (result, response.headers['X-Pagination-Page-Count'])
	else: return result

def trakt_refresh_token():
	from modules.nav_utils import sync_MyAccounts
	ma_trakt.refresh_token()
	sync_MyAccounts(silent=True)

def trakt_authenticate():
	from modules.nav_utils import sync_MyAccounts
	success = ma_trakt.auth()
	sync_MyAccounts()
	return success

def trakt_movies_search(query, page_no, letter):
	from modules.history import add_to_search_history
	add_to_search_history(query, 'movie_queries')
	string = 'trakt_movies_search_%s_%s' % (query, page_no)
	url = {'path': 'search/movie?query=%s', 'path_insert': query, 'params': {'limit': 200}, 'page': page_no}
	original_list = cache_object(get_trakt, string, url, False)
	final_list, total_pages = paginate_list(original_list, page_no, letter)
	return final_list, total_pages

def trakt_movies_trending(page_no):
	string = 'trakt_movies_trending_%s' % page_no
	url = {'path': 'movies/trending/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_anticipated(page_no):
	string = 'trakt_movies_anticipated_%s' % page_no
	url = {'path': 'movies/anticipated/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_top10_boxoffice(page_no):
	string = 'trakt_movies_top10_boxoffice'
	url = {'path': 'movies/boxoffice/%s', 'pagination': False}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_mosts(period, duration, page_no):
	string = 'trakt_movies_mosts_%s_%s_%s' % (period, duration, page_no)
	url = {'path': 'movies/%s/%s', 'path_insert': (period, duration), 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_related(imdb_id, page_no, letter='None'):
	string = 'trakt_movies_related_%s' % imdb_id
	url = {'path': 'movies/%s/related', 'path_insert': imdb_id, 'params': {'limit': 100}}
	original_list = cache_object(get_trakt, string, url, json=False, expiration=48)
	paginated_list, total_pages = paginate_list(original_list, page_no, letter)
	return paginated_list, total_pages

def trakt_recommendations(db_type):
	string = 'trakt_recommendations_%s' % (db_type)
	url = {'path': '/recommendations/%s', 'path_insert': db_type, 'with_auth': True, 'params': {'limit': 50}, 'pagination': False}
	return trakt_cache.cache_trakt_object(get_trakt, string, url)

def trakt_tv_search(query, page_no, letter):
	from modules.history import add_to_search_history
	add_to_search_history(query, 'tvshow_queries')
	string = 'trakt_tv_search_%s_%s' % (query, page_no)
	url = {'path': 'search/show?query=%s', 'path_insert': query, 'params': {'limit': 200}, 'page': page_no}
	original_list = cache_object(get_trakt, string, url, json=False, expiration=48)
	final_list, total_pages = paginate_list(original_list, page_no, letter)
	return final_list, total_pages

def trakt_tv_trending(page_no):
	string = 'trakt_tv_trending_%s' % page_no
	url = {'path': 'shows/trending/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_anticipated(page_no):
	string = 'trakt_tv_anticipated_%s' % page_no
	url = {'path': 'shows/anticipated/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_certifications(certification, page_no):
	string = 'trakt_tv_certifications_%s_%s' % (certification, page_no)
	url = {'path': 'shows/collected/all?certifications=%s', 'path_insert': certification, 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_mosts(period, duration, page_no):
	string = 'trakt_tv_mosts_%s_%s_%s' % (period, duration, page_no)
	url = {'path': 'shows/%s/%s', 'path_insert': (period, duration), 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_related(imdb_id, page_no, letter='None'):
	string = 'trakt_tv_related_%s' % imdb_id
	url = {'path': 'shows/%s/related', 'path_insert': imdb_id, 'params': {'limit': 100}}
	original_list = cache_object(get_trakt, string, url, json=False, expiration=48)
	paginated_list, total_pages = paginate_list(original_list, page_no, letter)
	return paginated_list, total_pages

def trakt_get_hidden_items(list_type):
	string = 'trakt_hidden_items_%s' % list_type
	url = {'path': 'users/hidden/%s', 'path_insert': list_type, 'params': {'limit': 1000, 'type': 'show'}, 'with_auth': True, 'pagination': False}
	hidden_data = trakt_cache.cache_trakt_object(get_trakt, string, url)
	if list_type == 'progress_watched': return [str(get_trakt_tvshow_id(i['show']['ids'])) for i in hidden_data]

def trakt_watched_unwatched(action, media, media_id, tvdb_id=0, season=None, episode=None, key='tmdb'):
	if action == 'mark_as_watched':
		url, result_key = 'sync/history', 'added'
	else:
		url, result_key = 'sync/history/remove', 'deleted'
	if media == 'movies':
		data = {'movies': [{'ids': {key: media_id}}]}
		success_key = 'movies'
	else:
		success_key = 'episodes'
		if media == 'episode': data = {'shows': [{'seasons': [{'episodes': [{'number': int(episode)}], 'number': int(season)}], 'ids': {key: media_id}}]}
		elif media =='shows': data = {'shows': [{'ids': {key: media_id}}]}
		else: data = {'shows': [{'ids': {key: media_id}, 'seasons': [{'number': int(season)}]}]}#season
	result = call_trakt(url, data=data)
	success = result[result_key][success_key] > 0
	if not success:
		if media != 'movies' and tvdb_id != 0: return trakt_watched_unwatched(action, media, tvdb_id, 0, season, episode, 'tvdb')
	return success

def trakt_progress(action, media, media_id, percent, season=None, episode=None):
	if action == 'set_progress': url = 'scrobble/pause'
	else: url = 'scrobble/pause'
	if media in ('movie', 'movies'): data = {'movie': {'ids': {'tmdb': media_id}}, 'progress': float(percent)}
	else: data = {'show': {'ids': {'tmdb': media_id}}, 'episode': {'season': int(season), 'number': int(episode)}, 'progress': percent}
	result = call_trakt(url, data=data)

def trakt_collection_lists(db_type, param1, param2):
	# param1 = the type of list to be returned (from 'new_page' param), param2 is currently not used
	limit = 20
	string_insert = 'movie' if db_type in ('movie', 'movies') else 'tvshow'
	window_property_name = 'fen_trakt_collection_%s' % string_insert
	try: data = json.loads(kodi_utils.get_property(window_property_name))
	except: data = trakt_fetch_collection_watchlist('collection', db_type)
	if param1 == 'recent':
		data.sort(key=lambda k: k['collected_at'], reverse=True)
	elif param1 == 'random':
		import random
		random.shuffle(data)
	data = data[:limit]
	for item in data:
		item['media_id'] = get_trakt_movie_id(item['media_ids']) if db_type == 'movies' else get_trakt_tvshow_id(item['media_ids'])
	return data, 1

def trakt_collection(db_type, page_no, letter):
	string_insert = 'movie' if db_type in ('movie', 'movies') else 'tvshow'
	original_list = trakt_fetch_collection_watchlist('collection', db_type)
	if settings.paginate():
		limit = settings.page_limit()
		final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	for item in final_list:
		item['media_id'] = get_trakt_movie_id(item['media_ids']) if db_type == 'movies' else get_trakt_tvshow_id(item['media_ids'])
	return final_list, total_pages

def trakt_watchlist(db_type, page_no, letter):
	string_insert = 'movie' if db_type in ('movie', 'movies') else 'tvshow'
	original_list = trakt_fetch_collection_watchlist('watchlist', db_type)
	if settings.paginate():
		limit = settings.page_limit()
		final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	for item in final_list:
		item['media_id'] = get_trakt_movie_id(item['media_ids']) if db_type == 'movies' else get_trakt_tvshow_id(item['media_ids'])
	return final_list, total_pages

def trakt_fetch_collection_watchlist(list_type, db_type):
	key, string_insert = ('movie', 'movie') if db_type in ('movie', 'movies') else ('show', 'tvshow')
	collected_at = 'collected_at' if db_type in ('movie', 'movies') else 'last_collected_at'
	string = 'trakt_%s_%s' % (list_type, string_insert)
	path = 'sync/%s/' % list_type
	url = {'path': path + '%s', 'path_insert': db_type, 'with_auth': True, 'pagination': False}
	data = trakt_cache.cache_trakt_object(get_trakt, string, url)
	if list_type == 'watchlist': data = [i for i in data if i['type'] == key]
	result = [{'media_ids': i[key]['ids'], 'title': i[key]['title'], 'collected_at': i.get(collected_at)} for i in data]
	result = sort_for_article(result, 'title', settings.ignore_articles())
	return result

def add_to_list(user, slug, data):
	result = call_trakt('/users/%s/lists/%s/items' % (user, slug), data=data)
	if result['added']['shows'] > 0 or result['added']['movies'] > 0:
		kodi_utils.notification(32576, 3000)
		trakt_sync_activities()
	else: kodi_utils.notification(32574, 3000)
	return result

def remove_from_list(user, slug, data):
	result = call_trakt('/users/%s/lists/%s/items/remove' % (user, slug), data=data)
	if result['deleted']['shows'] > 0 or result['deleted']['movies'] > 0:
		kodi_utils.notification(32576, 3000)
		trakt_sync_activities()
		kodi_utils.execute_builtin('Container.Refresh')
	else: kodi_utils.notification(32574, 3000)
	return result

def add_to_watchlist(data):
	result = call_trakt('/sync/watchlist', data=data)
	if result['added']['movies'] > 0: db_type = 'movie'
	elif result['added']['shows'] > 0: db_type = 'tvshow'
	else: return kodi_utils.notification(32574, 3000)
	kodi_utils.notification(32576, 6000)
	trakt_sync_activities()
	return result

def remove_from_watchlist(data):
	result = call_trakt('/sync/watchlist/remove', data=data)
	if result['deleted']['movies'] > 0: db_type = 'movie'
	elif result['deleted']['shows'] > 0: db_type = 'tvshow'
	else: return kodi_utils.notification(32574, 3000)
	kodi_utils.notification(32576, 3000)
	trakt_sync_activities()
	kodi_utils.execute_builtin('Container.Refresh')
	return result

def add_to_collection(data):
	result = call_trakt('/sync/collection', data=data)
	if result['added']['movies'] > 0: db_type = 'movie'
	elif result['added']['episodes'] > 0: db_type = 'tvshow'
	else: return kodi_utils.notification(32574, 3000)
	kodi_utils.notification(32576, 6000)
	trakt_sync_activities()
	return result

def remove_from_collection(data):
	result = call_trakt('/sync/collection/remove', data=data)
	if result['deleted']['movies'] > 0: db_type = 'movie'
	elif result['deleted']['episodes'] > 0: db_type = 'tvshow'
	else: return kodi_utils.notification(32574, 3000)
	kodi_utils.notification(32576, 3000)
	trakt_sync_activities()
	kodi_utils.execute_builtin('Container.Refresh')
	return result

def hide_unhide_trakt_items(action, db_type, media_id, list_type):
	db_type = 'movies' if db_type in ['movie', 'movies'] else 'shows'
	key = 'tmdb' if db_type == 'movies' else 'imdb'
	url = 'users/hidden/%s' % list_type if action == 'hide' else 'users/hidden/%s/remove' % list_type
	data = {db_type: [{'ids': {key: media_id}}]}
	call_trakt(url, data=data)
	trakt_sync_activities()
	kodi_utils.execute_builtin('Container.Refresh')

def trakt_search_lists(search_title, page):
	lists, pages = call_trakt('search', params={'type': 'list', 'fields': 'name, description', 'query': search_title, 'limit': 50}, pagination=True, page=page)
	return lists, pages

def get_trakt_list_contents(list_type, user, slug):
	string = 'trakt_list_contents_%s_%s_%s' % (list_type, user, slug)
	url = {'path': 'users/%s/lists/%s/items', 'path_insert': (user, slug), 'params': {'extended':'full'}, 'with_auth': True, 'method': 'sort_by_headers'}
	return trakt_cache.cache_trakt_object(get_trakt, string, url)

def trakt_trending_popular_lists(list_type):
	string = 'trakt_%s_user_lists' % list_type
	path = 'lists/%s/%s' % (list_type, '%s')
	url = {'path': path, 'params': {'limit': 100}}
	return cache_object(get_trakt, string, url, False)

def trakt_get_lists(list_type):
	if list_type == 'my_lists':
		string = 'trakt_my_lists'
		path = 'users/me/lists%s'
	elif list_type == 'liked_lists':
		string = 'trakt_liked_lists'
		path = 'users/likes/lists%s'
	url = {'path': path, 'params': {'limit': 1000}, 'pagination': False, 'with_auth': True}
	return trakt_cache.cache_trakt_object(get_trakt, string, url)

def get_trakt_list_selection(list_choice='none'):
	my_lists = [{'name': item['name'], 'display': ls(32778) % item['name'].upper(), 'user': item['user']['ids']['slug'], 'slug': item['ids']['slug']} \
																											for item in trakt_get_lists('my_lists')]
	my_lists.sort(key=lambda k: k['name'])
	if list_choice == 'nav_edit':
		liked_lists = [{'name': item['list']['name'], 'display': ls(32779) % item['list']['name'].upper(), 'user': item['list']['user']['ids']['slug'],
								'slug': item['list']['ids']['slug']} for item in trakt_get_lists('liked_lists')]
		liked_lists.sort(key=lambda k: (k['display']))
		my_lists.extend(liked_lists)
	else:
		my_lists.insert(0, {'name': 'Collection', 'display': '[B][I]%s [/I][/B]' % ls(32499).upper(), 'user': 'Collection', 'slug': 'Collection'})
		my_lists.insert(0, {'name': 'Watchlist', 'display': '[B][I]%s [/I][/B]' % ls(32500).upper(),  'user': 'Watchlist', 'slug': 'Watchlist'})
	list_items = [{'line1': item['display'], 'icon': trakt_icon} for item in my_lists]
	index_list = [list_items.index(i) for i in list_items]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Select list', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	selection = kodi_utils.select_dialog(my_lists, **kwargs)
	if selection == None: return None
	return selection

def make_new_trakt_list(params):
	from urllib.parse import unquote
	mode = params['mode']
	list_title = kodi_utils.dialog.input('Fen')
	if not list_title: return
	list_name = unquote(list_title)
	data = {'name': list_name, 'privacy': 'private', 'allow_comments': False}
	call_trakt('users/me/lists', data=data)
	trakt_sync_activities()
	kodi_utils.notification(32576, 3000)
	kodi_utils.execute_builtin('Container.Refresh')

def delete_trakt_list(params):
	user = params['user']
	list_slug = params['list_slug']
	if not kodi_utils.confirm_dialog(): return
	url = 'users/%s/lists/%s' % (user, list_slug)
	call_trakt(url, is_delete=True)
	trakt_sync_activities()
	kodi_utils.notification(32576, 3000)
	kodi_utils.execute_builtin('Container.Refresh')

def trakt_add_to_list(params):
	tmdb_id = params['tmdb_id']
	tvdb_id = params['tvdb_id']
	imdb_id = params['imdb_id']
	db_type = params['db_type']
	if db_type == 'movie':
		key, media_key, media_id = ('movies', 'tmdb', int(tmdb_id))
	else:
		key = 'shows'
		media_ids = [(imdb_id, 'imdb'), (tvdb_id, 'tvdb'), (tmdb_id, 'tmdb')]
		media_id, media_key = next(item for item in media_ids if item[0] != 'None')
		if media_id in (tmdb_id, tvdb_id):
			media_id = int(media_id)
	selected = get_trakt_list_selection()
	if selected is not None:
		data = {key: [{'ids': {media_key: media_id}}]}
		if selected['user'] == 'Watchlist':
			add_to_watchlist(data)
		elif selected['user'] == 'Collection':
			add_to_collection(data)
		else:
			user = selected['user']
			slug = selected['slug']
			add_to_list(user, slug, data)

def trakt_remove_from_list(params):
	tmdb_id = params['tmdb_id']
	tvdb_id = params['tvdb_id']
	imdb_id = params['imdb_id']
	db_type = params['db_type']
	if db_type == 'movie':
		key, media_key, media_id = ('movies', 'tmdb', int(tmdb_id))
	else:
		key = 'shows'
		media_ids = [(imdb_id, 'imdb'), (tvdb_id, 'tvdb'), (tmdb_id, 'tmdb')]
		media_id, media_key = next(item for item in media_ids if item[0] != 'None')
		if media_id in (tmdb_id, tvdb_id):
			media_id = int(media_id)
	selected = get_trakt_list_selection()
	if selected is not None:
		data = {key: [{'ids': {media_key: media_id}}]}
		if selected['user'] == 'Watchlist':
			remove_from_watchlist(data)
		elif selected['user'] == 'Collection':
			remove_from_collection(data)
		else:
			user = selected['user']
			slug = selected['slug']
			remove_from_list(user, slug, data)

def trakt_like_a_list(params):
	user = params['user']
	list_slug = params['list_slug']
	try:
		call_trakt('/users/%s/lists/%s/like' % (user, list_slug), method='post')
		kodi_utils.notification(32576, 3000)
		trakt_sync_activities()
	except: kodi_utils.notification(32574, 3000)

def trakt_unlike_a_list(params):
	user = params['user']
	list_slug = params['list_slug']
	try:
		call_trakt('/users/%s/lists/%s/like' % (user, list_slug), method='delete')
		kodi_utils.notification(32576, 3000)
		trakt_sync_activities()
		kodi_utils.execute_builtin('Container.Refresh')
	except: kodi_utils.notification(32574, 3000)

def get_trakt_movie_id(item):
	if item['tmdb']: return item['tmdb']
	tmdb_id = None
	if item['imdb']:
		try:
			meta = movie_meta_external_id('imdb_id', item['imdb'])
			tmdb_id = meta['id']
		except: pass
	return tmdb_id

def get_trakt_tvshow_id(item):
	if item['tmdb']: return item['tmdb']
	tmdb_id = None
	if item['imdb']:
		try: 
			meta = tvshow_meta_external_id('imdb_id', item['imdb'])
			tmdb_id = meta['id']
		except: tmdb_id = None
	if not tmdb_id:
		if item['tvdb']:
			try: 
				meta = tvshow_meta_external_id('tvdb_id', item['tvdb'])
				tmdb_id = meta['id']
			except: tmdb_id = None
	return tmdb_id

def trakt_indicators_movies():
	from threading import Thread
	from modules.utils import make_thread_list
	def _process(item):
		movie = item['movie']
		tmdb_id = get_trakt_movie_id(movie['ids'])
		obj = ('movie', tmdb_id, '', '', item['last_watched_at'], movie['title'])
		insert_append(obj)
	insert_list = []
	insert_append = insert_list.append
	url = {'path': 'sync/watched/movies%s', 'with_auth': True, 'pagination': False}
	result = get_trakt(url)
	threads = list(make_thread_list(_process, result, Thread))
	[i.join() for i in threads]
	trakt_cache.TraktWatched().set_bulk_movie_watched(insert_list)

def trakt_indicators_tv():
	from threading import Thread
	from modules.utils import make_thread_list
	def _process(item):
		show = item['show']
		seasons = item['seasons']
		title = show['title']
		tmdb_id = get_trakt_tvshow_id(show['ids'])
		for s in seasons:
			season_no, episodes = s['number'], s['episodes']
			for e in episodes:
				obj = ('episode', tmdb_id, season_no, e['number'], e['last_watched_at'], title)
				insert_append(obj)
	insert_list = []
	insert_append = insert_list.append
	url = {'path': 'users/me/watched/shows?extended=full%s', 'with_auth': True, 'pagination': False}
	result = get_trakt(url)
	threads = list(make_thread_list(_process, result, Thread))
	[i.join() for i in threads]
	trakt_cache.TraktWatched().set_bulk_tvshow_watched(insert_list)

def trakt_playback_progress():
	url = {'path': 'sync/playback%s', 'with_auth': True, 'pagination': False}
	return get_trakt(url)

def trakt_progress_movies(progress_info):
	from threading import Thread
	from modules.utils import make_thread_list
	def _process(item):
		tmdb_id = get_trakt_movie_id(item['movie']['ids'])
		obj = ('movie', str(tmdb_id), '', '', str(round(item['progress'], 1)), 0)
		insert_append(obj)
	insert_list = []
	insert_append = insert_list.append
	progress_items = [i for i in progress_info if i['progress'] > 1 and i['type'] == 'movie']
	threads = list(make_thread_list(_process, progress_items, Thread))
	[i.join() for i in threads]
	trakt_cache.TraktWatched().set_bulk_movie_progress(insert_list)

def trakt_progress_tv(progress_info):
	from threading import Thread
	from modules.utils import make_thread_list
	def _process_tmdb_ids(item):
		tmdb_id = get_trakt_tvshow_id(item['ids'])
		tmdb_list_append((tmdb_id, item['title']))
	def _process():
		for item in tmdb_list:
			tmdb_id = item[0]
			if not tmdb_id: continue
			title = item[1]
			for p_item in progress_items:
				if p_item['show']['title'] == title:
					season = p_item['episode']['season']
					if season > 0: yield ('episode', str(tmdb_id), season, p_item['episode']['number'], str(round(p_item['progress'], 1)), 0)
	tmdb_list = []
	tmdb_list_append = tmdb_list.append
	progress_items = [i for i in progress_info if i['progress'] > 1 and i['type'] == 'episode']
	all_shows = [i['show'] for i in progress_items]
	all_shows = [i for n, i in enumerate(all_shows) if i not in all_shows[n + 1:]] # remove duplicates
	threads = list(make_thread_list(_process_tmdb_ids, all_shows, Thread))
	[i.join() for i in threads]
	insert_list = list(_process())
	trakt_cache.TraktWatched().set_bulk_tvshow_progress(insert_list)

def trakt_official_status(db_type):
	if not kodi_utils.addon_installed('script.trakt'): return True
	trakt_addon = kodi_utils.ext_addon('script.trakt')
	try: authorization = trakt_addon.getSetting('authorization')
	except: authorization = ''
	if authorization == '': return True
	try: exclude_http = trakt_addon.getSetting('ExcludeHTTP')
	except: exclude_http = ''
	if exclude_http in ('true', ''): return True
	media_setting = 'scrobble_movie' if db_type in ('movie', 'movies') else 'scrobble_episode'
	try: scrobble = trakt_addon.getSetting(media_setting)
	except: scrobble = ''
	if scrobble in ('false', ''): return True
	return False

def trakt_get_my_calendar(recently_aired, current_date):
	def _process(dummy):
		data = get_trakt(url)
		data = [{'sort_title': '%s s%s e%s' % (i['show']['title'], str(i['episode']['season']).zfill(2), str(i['episode']['number']).zfill(2)),
				'ids': i['show']['ids'], 'season': i['episode']['season'], 'episode': i['episode']['number'], 'first_aired': i['first_aired']} \
									for i in data if i['episode']['season'] > 0]
		data = [i for n, i in enumerate(data) if i not in data[n + 1:]] # remove duplicates
		return data
	start, finish = trakt_calendar_days(recently_aired, current_date)
	string = 'trakt_get_my_calendar_%s_%s' % (start, finish)
	url = {'path': 'calendars/my/shows/%s/%s', 'path_insert': (start, finish), 'with_auth': True, 'pagination': False}
	return trakt_cache.cache_trakt_object(_process, string, url)

def trakt_calendar_days(recently_aired, current_date):
	from datetime import timedelta
	if recently_aired:
		start, finish = (current_date - timedelta(days=7)).strftime('%Y-%m-%d'), '7'
	else:
		previous_days = int(get_setting('trakt.calendar_previous_days', '3'))
		future_days = int(get_setting('trakt.calendar_future_days', '7'))
		start = (current_date - timedelta(days=previous_days)).strftime('%Y-%m-%d')
		finish = str(previous_days + future_days)
	return start, finish

def get_trakt(params):
	result = call_trakt(params['path'] % params.get('path_insert', ''), params=params.get('params', {}), data=params.get('data'),
						is_delete=params.get('is_delete', False), with_auth=params.get('with_auth', False), method=params.get('method'),
						pagination=params.get('pagination', True), page=params.get('page'))
	return result[0] if params.get('pagination', True) else result

def make_trakt_slug(name):
	import re
	name = name.strip()
	name = name.lower()
	name = re.sub('[^a-z0-9_]', '-', name)
	name = re.sub('--+', '-', name)
	return name

def trakt_get_activity():
	url = {'path': 'sync/last_activities%s', 'with_auth': True, 'pagination': False}
	return get_trakt(url)

def trakt_sync_activities(force_update=False):
	def _get_timestamp(date_time):
		return int(time.mktime(date_time.timetuple()))
	def _compare(latest, cached):
		return _get_timestamp(js2date(latest, res_format)) > _get_timestamp(js2date(cached, res_format))
	if not get_setting('trakt_user', ''): return 'no account'
	if force_update:
		check_databases()
		trakt_cache.clear_all_trakt_cache_data(silent=True, confirm=False)
	res_format = '%Y-%m-%dT%H:%M:%S.%fZ'
	try: latest = trakt_get_activity()
	except: return 'failed'
	latest = trakt_get_activity()
	cached = trakt_cache.reset_activity(latest)
	trakt_cache.clear_trakt_calendar()
	if not _compare(latest['all'], cached['all']):
		trakt_cache.clear_trakt_list_contents_data('liked_lists')
		return 'not needed'
	clear_list_contents, lists_actions = False, []
	refresh_movies_progress, refresh_shows_progress = False, False
	cached_movies, latest_movies = cached['movies'], latest['movies']
	cached_shows, latest_shows = cached['shows'], latest['shows']
	cached_episodes, latest_episodes = cached['episodes'], latest['episodes']
	cached_lists, latest_lists = cached['lists'], latest['lists']
	if _compare(latest_movies['collected_at'], cached_movies['collected_at']): trakt_cache.clear_trakt_collection_watchlist_data('collection', 'movie')
	if _compare(latest_episodes['collected_at'], cached_episodes['collected_at']): trakt_cache.clear_trakt_collection_watchlist_data('collection', 'tvshow')
	if _compare(latest_movies['watchlisted_at'], cached_movies['watchlisted_at']): trakt_cache.clear_trakt_collection_watchlist_data('watchlist', 'movie')
	if _compare(latest_shows['watchlisted_at'], cached_shows['watchlisted_at']): trakt_cache.clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	if _compare(latest_shows['hidden_at'], cached_shows['hidden_at']): trakt_cache.clear_trakt_hidden_data('progress_watched')
	if _compare(latest_movies['recommendations_at'], cached_movies['recommendations_at']): trakt_cache.clear_trakt_recommendations('movies')
	if _compare(latest_shows['recommendations_at'], cached_shows['recommendations_at']): trakt_cache.clear_trakt_recommendations('shows')
	if _compare(latest_movies['watched_at'], cached_movies['watched_at']): trakt_indicators_movies()
	if _compare(latest_episodes['watched_at'], cached_episodes['watched_at']): trakt_indicators_tv()
	if _compare(latest_movies['paused_at'], cached_movies['paused_at']): refresh_movies_progress = True
	if _compare(latest_episodes['paused_at'], cached_episodes['paused_at']): refresh_shows_progress = True
	if _compare(latest_lists['updated_at'], cached_lists['updated_at']):
		clear_list_contents = True
		lists_actions.append('my_lists')
	if _compare(latest_lists['liked_at'], cached_lists['liked_at']):
		clear_list_contents = True
		lists_actions.append('liked_lists')
	if refresh_movies_progress or refresh_shows_progress:
		progress_info = trakt_playback_progress()
		if refresh_movies_progress: trakt_progress_movies(progress_info)
		if refresh_shows_progress: trakt_progress_tv(progress_info)
	if clear_list_contents:
		for item in lists_actions:
			trakt_cache.clear_trakt_list_data(item)
			trakt_cache.clear_trakt_list_contents_data(item)
	else: trakt_cache.clear_trakt_list_contents_data('liked_lists')
	return 'success'
