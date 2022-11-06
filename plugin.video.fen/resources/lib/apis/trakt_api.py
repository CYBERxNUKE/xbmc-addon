# -*- coding: utf-8 -*-
import time
from metadata import movie_meta, movie_meta_external_id, tvshow_meta_external_id
from caches import check_databases, trakt_cache
from caches.main_cache import cache_object
from modules import kodi_utils, settings
from modules.utils import sort_list, sort_for_article, make_thread_list, paginate_list, get_datetime, timedelta, jsondate_to_datetime as js2date, title_key

CLIENT_ID = '645b0f46df29d27e63c4a8d5fff158edd0bef0a6a5d32fc12c1b82388be351af'
CLIENT_SECRET = '422a282ef5fe4b5c47bc60425c009ac3047ebd10a7f6af790303875419f18f98'
ls, json, monitor, sleep, get_setting, set_setting = kodi_utils.local_string, kodi_utils.json, kodi_utils.monitor, kodi_utils.sleep, kodi_utils.get_setting, kodi_utils.set_setting
logger, notification, player, confirm_dialog, get_property = kodi_utils.logger, kodi_utils.notification, kodi_utils.player, kodi_utils.confirm_dialog, kodi_utils.get_property
requests, execute_builtin, select_dialog, kodi_refresh = kodi_utils.requests, kodi_utils.execute_builtin, kodi_utils.select_dialog, kodi_utils.kodi_refresh
set_temp_highlight, restore_highlight, make_settings_dict = kodi_utils.set_temp_highlight, kodi_utils.restore_highlight, kodi_utils.make_settings_dict
pause_settings_change, unpause_settings_change, progress_dialog = kodi_utils.pause_settings_change, kodi_utils.unpause_settings_change, kodi_utils.progress_dialog
dialog, unquote, addon_installed, addon_enabled, addon = kodi_utils.dialog, kodi_utils.unquote, kodi_utils.addon_installed, kodi_utils.addon_enabled, kodi_utils.addon
ignore_articles, lists_sort_order, paginate, page_limit = settings.ignore_articles, settings.lists_sort_order, settings.paginate, settings.page_limit
show_unaired_watchlist, metadata_user_info,  = settings.show_unaired_watchlist, settings.metadata_user_info, 
clear_all_trakt_cache_data, cache_trakt_object, clear_trakt_calendar = trakt_cache.clear_all_trakt_cache_data, trakt_cache.cache_trakt_object, trakt_cache.clear_trakt_calendar
TraktWatched, reset_activity, clear_trakt_list_contents_data = trakt_cache.TraktWatched, trakt_cache.reset_activity, trakt_cache.clear_trakt_list_contents_data
clear_trakt_collection_watchlist_data, clear_trakt_hidden_data = trakt_cache.clear_trakt_collection_watchlist_data, trakt_cache.clear_trakt_hidden_data
clear_trakt_recommendations, clear_trakt_list_data = trakt_cache.clear_trakt_recommendations, trakt_cache.clear_trakt_list_data
trakt_icon, trakt_str = kodi_utils.get_icon('trakt'), ls(32037)
API_ENDPOINT = 'https://api.trakt.tv/%s'
timeout = 20

def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, method=None, pagination=False, page=1):
	def send_query():
		resp = None
		if with_auth:
			try:
				try: expires_at = float(get_setting('trakt.expires'))
				except: expires_at = 0.0
				if time.time() > expires_at: trakt_refresh_token()
			except: pass
			token = get_setting('trakt.token')
			if token: headers['Authorization'] = 'Bearer ' + token
		try:
			if method:
				if method == 'post':
					resp = requests.post(API_ENDPOINT % path, headers=headers, timeout=timeout)
				elif method == 'delete':
					resp = requests.delete(API_ENDPOINT % path, headers=headers, timeout=timeout)
				elif method == 'sort_by_headers':
					resp = requests.get(API_ENDPOINT % path, params=params, headers=headers, timeout=timeout)
			elif data is not None:
				assert not params
				resp = requests.post(API_ENDPOINT % path, json=data, headers=headers, timeout=timeout)
			elif is_delete: resp = requests.delete(API_ENDPOINT % path, headers=headers, timeout=timeout)
			else: resp = requests.get(API_ENDPOINT % path, params=params, headers=headers, timeout=timeout)
			resp.raise_for_status()
		except Exception as e: return logger('Trakt Error', str(e))
		return resp
	headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
	if pagination: params['page'] = page
	response = send_query()
	try: status_code = response.status_code
	except: return None
	if status_code == 401:
		if player.isPlaying() == False:
			if with_auth and confirm_dialog(heading='%s %s' % (ls(32057), trakt_str), text=32741) and trakt_authenticate():
				response = send_query()
			else: pass
		else: return
	elif status_code == 429:
		headers = response.headers
		if 'Retry-After' in headers:
			sleep(1000 * headers['Retry-After'])
			response = send_query()
	response.encoding = 'utf-8'
	try: result = response.json()
	except: return None
	if method == 'sort_by_headers':
		try:
			headers = response.headers
			if 'X-Sort-By' in headers and 'X-Sort-How' in headers: result = sort_list(headers['X-Sort-By'], headers['X-Sort-How'], result, ignore_articles())
		except: pass
	if pagination: return (result, response.headers['X-Pagination-Page-Count'])
	else: return result
			
def trakt_get_device_code():
	data = {'client_id': CLIENT_ID}
	return call_trakt('oauth/device/code', data=data, with_auth=False)

def trakt_get_device_token(device_codes):
	result = None
	try:
		headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
		data = {'code': device_codes['device_code'], 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
		start = time.time()
		expires_in = device_codes['expires_in']
		sleep_interval = device_codes['interval']
		content = '[CR]%s[CR]%s' % (ls(32700) % str(device_codes['verification_url']), ls(32701) % '[COLOR red]%s[/COLOR]' % str(device_codes['user_code']))
		current_highlight = set_temp_highlight('red')
		progressDialog = progress_dialog('%s %s' % (ls(32037), ls(32057)), trakt_icon)
		progressDialog.update(content, 0)
		try:
			time_passed = 0
			while not progressDialog.iscanceled() and time_passed < expires_in:
				sleep(max(sleep_interval, 1)*1000)
				response = requests.post(API_ENDPOINT % 'oauth/device/token', data=json.dumps(data), headers=headers, timeout=timeout)
				status_code = response.status_code
				if status_code == 200:
					result = response.json()
					break
				elif status_code == 400:
					time_passed = time.time() - start
					progress = int(100 * time_passed/expires_in)
					progressDialog.update(content, progress)
				else: break
		except: pass
		try: progressDialog.close()
		except: pass
		restore_highlight(current_highlight)
	except: pass
	return result

def trakt_refresh_token():
	data = {        
		'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
		'grant_type': 'refresh_token', 'refresh_token': get_setting('trakt.refresh')}
	response = call_trakt("oauth/token", data=data, with_auth=False)
	if response:
		pause_settings_change()
		set_setting('trakt.token', response["access_token"])
		set_setting('trakt.refresh', response["refresh_token"])
		set_setting('trakt.expires', str(time.time() + 7776000))
		unpause_settings_change()
		make_settings_dict()

def trakt_authenticate(dummy):
	code = trakt_get_device_code()
	token = trakt_get_device_token(code)
	if token:
		pause_settings_change()
		set_setting('trakt.token', token["access_token"])
		set_setting('trakt.refresh', token["refresh_token"])
		set_setting('trakt.expires', str(time.time() + 7776000))
		set_setting('trakt.indicators_active', 'true')
		set_setting('watched_indicators', '1')
		unpause_settings_change()
		make_settings_dict()
		sleep(1000)
		try:
			user = call_trakt('/users/me', with_auth=True)
			set_setting('trakt.user', str(user['username']))
		except: pass
		notification('Trakt Account Authorized', 3000)
		trakt_sync_activities(force_update=True)
		return True
	notification('Trakt Error Authorizing', 3000)
	return False

def trakt_revoke_authentication(dummy):
	data = {'token': get_setting('trakt.token'), 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
	response = call_trakt("oauth/revoke", data=data, with_auth=False)
	pause_settings_change()
	set_setting('trakt.user', '')
	set_setting('trakt.expires', '')
	set_setting('trakt.token', '')
	set_setting('trakt.refresh', '')
	set_setting('trakt.indicators_active', 'false')
	set_setting('watched_indicators', '0')
	unpause_settings_change()
	make_settings_dict()
	clear_all_trakt_cache_data(silent=True, refresh=False)
	notification('Trakt Account Authorization Reset', 3000)

def trakt_movies_trending(page_no):
	string = 'trakt_movies_trending_%s' % page_no
	url = {'path': 'movies/trending/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_trending_recent(page_no):
	current_year = get_datetime().year
	years = '%s-%s' % (str(current_year-1), str(current_year))
	string = 'trakt_movies_trending_recent_%s' % page_no
	url = {'path': 'movies/trending/%s', 'params': {'limit': 20, 'years': years}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_top10_boxoffice(page_no):
	string = 'trakt_movies_top10_boxoffice'
	url = {'path': 'movies/boxoffice/%s', 'pagination': False}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_movies_most_watched(page_no):
	string = 'trakt_movies_most_watched_%s' % page_no
	url = {'path': 'movies/watched/weekly/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_recommendations(media_type):
	string = 'trakt_recommendations_%s' % (media_type)
	url = {'path': '/recommendations/%s', 'path_insert': media_type, 'with_auth': True, 'params': {'limit': 50}, 'pagination': False}
	return cache_trakt_object(get_trakt, string, url)

def trakt_tv_trending(page_no):
	string = 'trakt_tv_trending_%s' % page_no
	url = {'path': 'shows/trending/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_trending_recent(page_no):
	current_year = get_datetime().year
	years = '%s-%s' % (str(current_year-1), str(current_year))
	string = 'trakt_tv_trending_recent_%s' % page_no
	url = {'path': 'shows/trending/%s', 'params': {'limit': 20, 'years': years}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_most_watched(page_no):
	string = 'trakt_tv_most_watched_%s' % page_no
	url = {'path': 'shows/watched/weekly/%s', 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_tv_certifications(certification, page_no):
	string = 'trakt_tv_certifications_%s_%s' % (certification, page_no)
	url = {'path': 'shows/collected/all?certifications=%s', 'path_insert': certification, 'params': {'limit': 20}, 'page': page_no}
	return cache_object(get_trakt, string, url, json=False, expiration=48)

def trakt_get_hidden_items(list_type):
	def _get_trakt_ids(item):
		tmdb_id = get_trakt_tvshow_id(item['show']['ids'])
		results_append(tmdb_id)
	def _process(url):
		hidden_data = get_trakt(url)
		threads = list(make_thread_list(_get_trakt_ids, hidden_data))
		[i.join() for i in threads]
		return results
	results = []
	results_append = results.append
	string = 'trakt_hidden_items_%s' % list_type
	url = {'path': 'users/hidden/%s', 'path_insert': list_type, 'params': {'limit': 1000, 'type': 'show'}, 'with_auth': True, 'pagination': False}
	return cache_trakt_object(_process, string, url)

def trakt_watched_unwatched(action, media, media_id, tvdb_id=0, season=None, episode=None, key='tmdb'):
	if action == 'mark_as_watched': url, result_key = 'sync/history', 'added'
	else: url, result_key = 'sync/history/remove', 'deleted'
	if media == 'movies':
		success_key = 'movies'
		data = {'movies': [{'ids': {key: media_id}}]}
	else:
		success_key = 'episodes'
		if media == 'episode': data = {'shows': [{'seasons': [{'episodes': [{'number': int(episode)}], 'number': int(season)}], 'ids': {key: media_id}}]}
		elif media =='shows': data = {'shows': [{'ids': {key: media_id}}]}
		else: data = {'shows': [{'ids': {key: media_id}, 'seasons': [{'number': int(season)}]}]}#season
	result = call_trakt(url, data=data)
	success = result[result_key][success_key] > 0
	if not success:
		if media != 'movies' and tvdb_id != 0 and key != 'tvdb': return trakt_watched_unwatched(action, media, tvdb_id, 0, season, episode, 'tvdb')
	return success

def trakt_progress(action, media, media_id, percent, season=None, episode=None, resume_id=None, refresh_trakt=False):
	if action == 'clear_progress':
		url = 'sync/playback/%s' % resume_id
		result = call_trakt(url, is_delete=True)
	else:
		url = 'scrobble/pause'
		if media in ('movie', 'movies'): data = {'movie': {'ids': {'tmdb': media_id}}, 'progress': float(percent)}
		else: data = {'show': {'ids': {'tmdb': media_id}}, 'episode': {'season': int(season), 'number': int(episode)}, 'progress': float(percent)}
		call_trakt(url, data=data)
	if refresh_trakt: trakt_sync_activities()

def trakt_collection_lists(media_type, list_type):
	limit = 20
	string_insert = 'movie' if media_type in ('movie', 'movies') else 'tvshow'
	window_property_name = 'fen_trakt_collection_%s' % string_insert
	try: data = json.loads(get_property(window_property_name))
	except: data = trakt_fetch_collection_watchlist('collection', media_type)
	if list_type == 'recent':
		data.sort(key=lambda k: k['collected_at'], reverse=True)
	elif list_type == 'random':
		import random
		random.shuffle(data)
	data = data[:limit]
	return data, [], 1

def trakt_collection(media_type, page_no):
	string_insert = 'movie' if media_type in ('movie', 'movies') else 'tvshow'
	original_list = trakt_fetch_collection_watchlist('collection', media_type)
	sort_order = lists_sort_order('collection')
	if sort_order == 0: original_list = sort_for_article(original_list, 'title', ignore_articles())
	elif sort_order == 1: original_list.sort(key=lambda k: k['collected_at'], reverse=True)
	else: original_list.sort(key=lambda k: k['released'], reverse=True)
	if paginate(): final_list, all_pages, total_pages = paginate_list(original_list, page_no, page_limit())
	else: final_list, all_pages, total_pages = original_list, [], 1
	return final_list, all_pages, total_pages

def trakt_watchlist(media_type, page_no):
	string_insert = 'movie' if media_type in ('movie', 'movies') else 'tvshow'
	original_list = trakt_fetch_collection_watchlist('watchlist', media_type)
	if not show_unaired_watchlist():
		current_date = get_datetime()
		str_format = '%Y-%m-%d' if media_type in ('movie', 'movies') else '%Y-%m-%dT%H:%M:%S.%fZ'
		original_list = [i for i in original_list if i.get('released', None) and js2date(i.get('released'), str_format, remove_time=True) <= current_date]
	sort_order = lists_sort_order('watchlist')
	if sort_order == 0: original_list = sort_for_article(original_list, 'title', ignore_articles())
	elif sort_order == 1: original_list.sort(key=lambda k: k['collected_at'], reverse=True)
	else: original_list.sort(key=lambda k: k['released'], reverse=True)
	if paginate(): final_list, all_pages, total_pages = paginate_list(original_list, page_no, page_limit())
	else: final_list, all_pages, total_pages = original_list, [], 1
	return final_list, all_pages, total_pages

def trakt_fetch_collection_watchlist(list_type, media_type):
	def _process(url):
		data = get_trakt(url)
		if list_type == 'watchlist': data = [i for i in data if i['type'] == key]
		return [{'media_ids': i[key]['ids'], 'title': i[key]['title'], 'collected_at': i.get(collected_at), 'released': i[key].get(release_key, '2050-01-01')} for i in data]
	key, string_insert, release_key = ('movie', 'movie', 'released') if media_type in ('movie', 'movies') else ('show', 'tvshow', 'first_aired')
	collected_at = 'listed_at' if list_type == 'watchlist' else 'collected_at' if media_type in ('movie', 'movies') else 'last_collected_at'
	string = 'trakt_%s_%s' % (list_type, string_insert)
	path = 'sync/%s/%s?extended=full'
	url = {'path': path, 'path_insert': (list_type, media_type), 'with_auth': True, 'pagination': False}
	return cache_trakt_object(_process, string, url)

def trakt_fetch_movie_sets():
	from caches import trakt_cache
	def _process_metadata(media_id):
		extra_info = movie_meta('trakt_dict', media_id, meta_user_info, current_date)['extra_info']
		collection_id = extra_info['collection_id']
		if collection_id: collection_info_append({'title': extra_info['collection_name'], 'id': collection_id})
	def _process(collection_info):
		media_ids = [i['media_ids'] for i in trakt_fetch_collection_watchlist('collection', 'movies')]
		threads = list(make_thread_list(_process_metadata, media_ids))
		[i.join() for i in threads]
		collection_info = [i for n, i in enumerate(collection_info) if not i in collection_info[n + 1:]] # remove duplicates
		return collection_info
	meta_user_info, current_date = metadata_user_info(), get_datetime()
	collection_info = []
	collection_info_append = collection_info.append
	return cache_trakt_object(_process, 'trakt_movie_sets', collection_info)

def add_to_list(user, slug, data):
	result = call_trakt('/users/%s/lists/%s/items' % (user, slug), data=data)
	if result['existing']['movies'] + result['existing']['shows'] > 0: return notification(32082, 3000)
	if result['added']['movies'] + result['added']['shows'] == 0: return notification(32574, 3000)
	notification(32576, 3000)
	trakt_sync_activities()
	kodi_refresh()
	return result

def remove_from_list(user, slug, data):
	result = call_trakt('/users/%s/lists/%s/items/remove' % (user, slug), data=data)
	if result['deleted']['movies'] + result['deleted']['shows'] == 0: return notification(32574, 3000)
	notification(32576, 3000)
	trakt_sync_activities()
	kodi_refresh()
	return result

def add_to_watchlist(data):
	result = call_trakt('/sync/watchlist', data=data)
	if result['existing']['movies'] + result['existing']['shows'] > 0: return notification(32082, 3000)
	if result['added']['movies'] + result['added']['shows'] == 0: return notification(32574, 3000)
	notification(32576, 3000)
	trakt_sync_activities()
	kodi_refresh()
	return result

def remove_from_watchlist(data):
	result = call_trakt('/sync/watchlist/remove', data=data)
	if result['deleted']['movies'] + result['deleted']['shows'] == 0: return notification(32574, 3000)
	notification(32576, 3000)
	trakt_sync_activities()
	kodi_refresh()
	return result

def add_to_collection(data, multi=False):
	result = call_trakt('/sync/collection', data=data)
	if not multi:
		if result['existing']['movies'] + result['existing']['episodes'] > 0: return notification(32082, 3000)
		if result['added']['movies'] + result['added']['episodes'] == 0: return notification(32574, 3000)
		notification(32576, 3000)
		trakt_sync_activities()
		kodi_refresh()
	return result

def remove_from_collection(data):
	result = call_trakt('/sync/collection/remove', data=data)
	if result['deleted']['movies'] + result['deleted']['episodes'] == 0: return notification(32574, 3000)
	notification(32576, 3000)
	trakt_sync_activities()
	kodi_refresh()
	return result

def hide_unhide_trakt_items(params):
	action, media_type, media_id, list_type = params['action'], params['media_type'], params['media_id'], params['section']
	media_type = 'movies' if media_type in ('movie', 'movies') else 'shows'
	key = 'tmdb'# if media_type == 'movies' else 'imdb'
	url = 'users/hidden/%s' % list_type if action == 'hide' else 'users/hidden/%s/remove' % list_type
	data = {media_type: [{'ids': {key: media_id}}]}
	call_trakt(url, data=data)
	trakt_sync_activities()
	kodi_refresh()

def trakt_search_lists(search_title, page):
	lists, pages = call_trakt('search', params={'type': 'list', 'fields': 'name, description', 'query': search_title, 'limit': 50}, pagination=True, page=page)
	return lists, pages

def get_trakt_list_contents(list_type, user, slug):
	string = 'trakt_list_contents_%s_%s_%s' % (list_type, user, slug)
	if user == 'Trakt Official':
		url = {'path': 'lists/%s/items', 'path_insert': slug, 'params': {'extended':'full'}, 'with_auth': True, 'method': 'sort_by_headers'}
	else:
		url = {'path': 'users/%s/lists/%s/items', 'path_insert': (user, slug), 'params': {'extended':'full'}, 'with_auth': True, 'method': 'sort_by_headers'}
	return cache_trakt_object(get_trakt, string, url)

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
	return cache_trakt_object(get_trakt, string, url)

def get_trakt_list_selection(list_choice=None):
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
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32193), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	selection = select_dialog(my_lists, **kwargs)
	if selection == None: return None
	return selection

def make_new_trakt_list(params):
	mode = params['mode']
	list_title = dialog.input(ls(32036))
	if not list_title: return
	list_name = unquote(list_title)
	data = {'name': list_name, 'privacy': 'private', 'allow_comments': False}
	call_trakt('users/me/lists', data=data)
	trakt_sync_activities()
	notification(32576, 3000)
	kodi_refresh()

def delete_trakt_list(params):
	user = params['user']
	list_slug = params['list_slug']
	if not confirm_dialog(): return
	url = 'users/%s/lists/%s' % (user, list_slug)
	call_trakt(url, is_delete=True)
	trakt_sync_activities()
	notification(32576, 3000)
	kodi_refresh()

def trakt_add_to_list(params):
	tmdb_id, tvdb_id, imdb_id, media_type = params['tmdb_id'], params['tvdb_id'], params['imdb_id'], params['media_type']
	if media_type == 'movie':
		key, media_key, media_id = ('movies', 'tmdb', int(tmdb_id))
	else:
		key = 'shows'
		media_ids = [(imdb_id, 'imdb'), (tvdb_id, 'tvdb'), (tmdb_id, 'tmdb')]
		media_id, media_key = next(item for item in media_ids if item[0] != 'None')
		if media_id in (tmdb_id, tvdb_id): media_id = int(media_id)
	selected = get_trakt_list_selection()
	if selected is not None:
		data = {key: [{'ids': {media_key: media_id}}]}
		if selected['user'] == 'Watchlist': add_to_watchlist(data)
		elif selected['user'] == 'Collection': add_to_collection(data)
		else:
			user = selected['user']
			slug = selected['slug']
			add_to_list(user, slug, data)

def trakt_remove_from_list(params):
	tmdb_id, tvdb_id, imdb_id, media_type = params['tmdb_id'], params['tvdb_id'], params['imdb_id'], params['media_type']
	if media_type == 'movie':
		key, media_key, media_id = ('movies', 'tmdb', int(tmdb_id))
	else:
		key = 'shows'
		media_ids = [(imdb_id, 'imdb'), (tvdb_id, 'tvdb'), (tmdb_id, 'tmdb')]
		media_id, media_key = next(item for item in media_ids if item[0] != 'None')
		if media_id in (tmdb_id, tvdb_id): media_id = int(media_id)
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
		notification(32576, 3000)
		trakt_sync_activities()
		kodi_refresh()
	except: notification(32574, 3000)

def trakt_unlike_a_list(params):
	user = params['user']
	list_slug = params['list_slug']
	try:
		call_trakt('/users/%s/lists/%s/like' % (user, list_slug), method='delete')
		notification(32576, 3000)
		trakt_sync_activities()
		kodi_refresh()
	except: notification(32574, 3000)

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
	def _process(item):
		movie = item['movie']
		tmdb_id = get_trakt_movie_id(movie['ids'])
		if not tmdb_id: return
		obj = ('movie', tmdb_id, '', '', item['last_watched_at'], movie['title'])
		insert_append(obj)
	insert_list = []
	insert_append = insert_list.append
	url = {'path': 'sync/watched/movies%s', 'with_auth': True, 'pagination': False}
	result = get_trakt(url)
	logger('result', result)
	threads = list(make_thread_list(_process, result))
	[i.join() for i in threads]
	TraktWatched().set_bulk_movie_watched(insert_list)

def trakt_indicators_tv():
	def _process(item):
		show = item['show']
		seasons = item['seasons']
		title = show['title']
		tmdb_id = get_trakt_tvshow_id(show['ids'])
		if not tmdb_id: return
		for s in seasons:
			season_no, episodes = s['number'], s['episodes']
			for e in episodes:
				obj = ('episode', tmdb_id, season_no, e['number'], e['last_watched_at'], title)
				insert_append(obj)
	insert_list = []
	insert_append = insert_list.append
	url = {'path': 'users/me/watched/shows?extended=full%s', 'with_auth': True, 'pagination': False}
	result = get_trakt(url)
	threads = list(make_thread_list(_process, result))
	[i.join() for i in threads]
	TraktWatched().set_bulk_tvshow_watched(insert_list)

def trakt_playback_progress():
	url = {'path': 'sync/playback%s', 'with_auth': True, 'pagination': False}
	return get_trakt(url)

def trakt_progress_movies(progress_info):
	def _process(item):
		tmdb_id = get_trakt_movie_id(item['movie']['ids'])
		if not tmdb_id: return
		obj = ('movie', str(tmdb_id), '', '', str(round(item['progress'], 1)), 0, item['paused_at'], item['id'], item['movie']['title'])
		insert_append(obj)
	insert_list = []
	insert_append = insert_list.append
	progress_items = [i for i in progress_info  if i['type'] == 'movie' and i['progress'] > 1]
	if not progress_items: return
	threads = list(make_thread_list(_process, progress_items))
	[i.join() for i in threads]
	TraktWatched().set_bulk_movie_progress(insert_list)

def trakt_progress_tv(progress_info):
	def _process_tmdb_ids(item):
		tmdb_id = get_trakt_tvshow_id(item['ids'])
		tmdb_list_append((tmdb_id, item['title']))
	def _process():
		for item in tmdb_list:
			try:
				tmdb_id = item[0]
				if not tmdb_id: continue
				title = item[1]
				for p_item in progress_items:
					if p_item['show']['title'] == title:
						season = p_item['episode']['season']
						if season > 0: yield ('episode', str(tmdb_id), season, p_item['episode']['number'], str(round(p_item['progress'], 1)),
												0, p_item['paused_at'], p_item['id'], p_item['show']['title'])
			except: pass
	tmdb_list = []
	tmdb_list_append = tmdb_list.append
	progress_items = [i for i in progress_info if i['type'] == 'episode' and i['progress'] > 1]
	if not progress_items: return
	all_shows = [i['show'] for i in progress_items]
	all_shows = [i for n, i in enumerate(all_shows) if not i in all_shows[n + 1:]] # remove duplicates
	threads = list(make_thread_list(_process_tmdb_ids, all_shows))
	[i.join() for i in threads]
	insert_list = list(_process())
	TraktWatched().set_bulk_tvshow_progress(insert_list)

def trakt_official_status(media_type):
	if not addon_installed('script.trakt'): return True
	if not addon_enabled('script.trakt'): return True
	trakt_addon = addon('script.trakt')
	try: authorization = trakt_addon.getSetting('authorization')
	except: authorization = ''
	if authorization == '': return True
	try: exclude_http = trakt_addon.getSetting('ExcludeHTTP')
	except: exclude_http = ''
	if exclude_http in ('true', ''): return True
	media_setting = 'scrobble_movie' if media_type in ('movie', 'movies') else 'scrobble_episode'
	try: scrobble = trakt_addon.getSetting(media_setting)
	except: scrobble = ''
	if scrobble in ('false', ''): return True
	return False

def trakt_get_my_calendar(recently_aired, current_date):
	def _process(dummy):
		data = get_trakt(url)
		data = [{'sort_title': '%s s%s e%s' % (i['show']['title'], str(i['episode']['season']).zfill(2), str(i['episode']['number']).zfill(2)),
				'media_ids': i['show']['ids'], 'season': i['episode']['season'], 'episode': i['episode']['number'], 'first_aired': i['first_aired']} \
									for i in data if i['episode']['season'] > 0]
		data = [i for n, i in enumerate(data) if i not in data[n + 1:]] # remove duplicates
		return data
	start, finish = trakt_calendar_days(recently_aired, current_date)
	string = 'trakt_get_my_calendar_%s_%s' % (start, finish)
	url = {'path': 'calendars/my/shows/%s/%s', 'path_insert': (start, finish), 'with_auth': True, 'pagination': False}
	return cache_trakt_object(_process, string, url)

def trakt_calendar_days(recently_aired, current_date):
	if recently_aired: start, finish = (current_date - timedelta(days=14)).strftime('%Y-%m-%d'), '14'
	else:
		previous_days = int(get_setting('trakt.calendar_previous_days', '3'))
		future_days = int(get_setting('trakt.calendar_future_days', '7'))
		start = (current_date - timedelta(days=previous_days)).strftime('%Y-%m-%d')
		finish = str(previous_days + future_days)
	return start, finish

def get_trakt(params):
	result = call_trakt(params['path'] % params.get('path_insert', ''), params=params.get('params', {}), data=params.get('data'), is_delete=params.get('is_delete', False),
						with_auth=params.get('with_auth', False), method=params.get('method'), pagination=params.get('pagination', True), page=params.get('page'))
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
		try: result = _get_timestamp(js2date(latest, res_format)) > _get_timestamp(js2date(cached, res_format))
		except: result = True
		return result
	if not get_setting('trakt.user', '') and not force_update: return 'no account'
	if force_update:
		check_databases()
		clear_all_trakt_cache_data(silent=True, refresh=False)
	res_format = '%Y-%m-%dT%H:%M:%S.%fZ'
	clear_trakt_calendar()
	try: latest = trakt_get_activity()
	except: return 'failed'
	cached = reset_activity(latest)
	clear_trakt_list_contents_data('user_lists')
	if not _compare(latest['all'], cached['all']):
		clear_trakt_list_contents_data('liked_lists')
		return 'not needed'
	clear_list_contents, lists_actions = False, []
	refresh_movies_progress, refresh_shows_progress = False, False
	cached_movies, latest_movies = cached['movies'], latest['movies']
	cached_shows, latest_shows = cached['shows'], latest['shows']
	cached_episodes, latest_episodes = cached['episodes'], latest['episodes']
	cached_lists, latest_lists = cached['lists'], latest['lists']
	if _compare(latest_movies['collected_at'], cached_movies['collected_at']): clear_trakt_collection_watchlist_data('collection', 'movie')
	if _compare(latest_episodes['collected_at'], cached_episodes['collected_at']): clear_trakt_collection_watchlist_data('collection', 'tvshow')
	if _compare(latest_movies['watchlisted_at'], cached_movies['watchlisted_at']): clear_trakt_collection_watchlist_data('watchlist', 'movie')
	if _compare(latest_shows['watchlisted_at'], cached_shows['watchlisted_at']): clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	if _compare(latest_shows['hidden_at'], cached_shows['hidden_at']): clear_trakt_hidden_data('progress_watched')
	if _compare(latest_movies['recommendations_at'], cached_movies['recommendations_at']): clear_trakt_recommendations('movies')
	if _compare(latest_shows['recommendations_at'], cached_shows['recommendations_at']): clear_trakt_recommendations('shows')
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
			clear_trakt_list_data(item)
			clear_trakt_list_contents_data(item)
	else: clear_trakt_list_contents_data('liked_lists')
	return 'success'
