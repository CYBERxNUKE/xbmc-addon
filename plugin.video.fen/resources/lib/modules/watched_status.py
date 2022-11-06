# -*- coding: utf-8 -*-
from datetime import datetime
import metadata
from apis.trakt_api import trakt_watched_unwatched, trakt_official_status, trakt_progress, trakt_get_hidden_items
from caches.trakt_cache import clear_trakt_collection_watchlist_data
from modules import kodi_utils, settings
from modules.utils import get_datetime, adjust_premiered_date, sort_for_article, make_thread_list, paginate_list
# logger = kodi_utils.logger

ls, database, notification, kodi_refresh = kodi_utils.local_string, kodi_utils.database, kodi_utils.notification, kodi_utils.kodi_refresh
sleep, progressDialogBG, Thread, get_video_database_path = kodi_utils.sleep, kodi_utils.progressDialogBG, kodi_utils.Thread, kodi_utils.get_video_database_path
watched_indicators_function, lists_sort_order, paginate, ignore_articles = settings.watched_indicators, settings.lists_sort_order, settings.paginate, settings.ignore_articles
page_limit, date_offset, metadata_user_info = settings.page_limit, settings.date_offset, settings.metadata_user_info
WATCHED_DB, TRAKT_DB = kodi_utils.watched_db, kodi_utils.trakt_db
indicators_dict = {0: WATCHED_DB, 1: TRAKT_DB}

def get_database(watched_indicators=None):
	return indicators_dict[watched_indicators or watched_indicators_function()]

def make_database_connection(database_file):
	return database.connect(database_file, timeout=40.0, isolation_level=None)

def set_PRAGMAS(dbcon):
	dbcur = dbcon.cursor()
	dbcur.execute('PRAGMA synchronous = OFF')
	dbcur.execute('PRAGMA journal_mode = OFF')
	return dbcur

def get_next_episodes(watched_info):
	seen = set()
	watched_info = [i for i in watched_info if not i[0] is None]
	watched_info.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
	return [{'media_ids': {'tmdb': int(i[0])}, 'season': int(i[1]), 'episode': int(i[2]), 'title': i[3], 'last_played': i[4]} \
							for i in watched_info if not (i[0] in seen or seen.add(i[0]))]

def get_recently_watched(media_type, short_list=1, dummy1=None):
	watched_indicators = watched_indicators_function()
	if media_type == 'movie':
		_watched = get_watched_info_movie(watched_indicators)
		data = [{'media_id': i[0], 'title': i[1], 'last_played': i[2]} for i in _watched]
	else:
		seen = set()
		_watched = get_watched_info_tv(watched_indicators)
		_watched.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
		if short_list: data = [{'media_ids': {'tmdb': int(i[0])}, 'season': int(i[1]), 'episode': int(i[2]), 'last_played': i[4], 'title': i[3]}
				for i in _watched]
		else: data = [{'media_ids': {'tmdb': int(i[0])}, 'season': int(i[1]), 'episode': int(i[2]), 'last_played': i[4], 'title': i[3]}
				for i in _watched if not (i[0] in seen or seen.add(i[0]))]
	watched_info = sorted(data, key=lambda k: (k['last_played']), reverse=True)
	if short_list: return watched_info[0:20], [], 1
	else: return watched_info

def get_progress_percent(bookmarks, tmdb_id, season='', episode=''):
	try: percent = str(round(float(detect_bookmark(bookmarks, tmdb_id, season, episode)[0])))
	except: percent = None
	return percent

def detect_bookmark(bookmarks, tmdb_id, season='', episode=''):
	return [(i[1], i[2], i[5]) for i in bookmarks if i[0] == str(tmdb_id) and i[3] == season and i[4] == episode][0]

def get_bookmarks(watched_indicators, media_type):
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		result = dbcur.execute("SELECT media_id, resume_point, curr_time, season, episode, resume_id FROM progress WHERE db_type = ?", (media_type,))
		return result.fetchall()
	except: pass

def erase_bookmark(media_type, tmdb_id, season='', episode='', refresh='false'):
	try:
		watched_indicators = watched_indicators_function()
		bookmarks = get_bookmarks(watched_indicators, media_type)
		if media_type == 'episode': season, episode = int(season), int(episode)
		try: resume_id = detect_bookmark(bookmarks, tmdb_id, season, episode)[2]
		except: return
		if watched_indicators == 1:
			sleep(1000)
			trakt_progress('clear_progress', media_type, tmdb_id, 0, season, episode, resume_id)
		dbcon = make_database_connection(get_database())
		dbcur = set_PRAGMAS(dbcon)
		dbcur.execute("DELETE FROM progress where db_type=? and media_id=? and season = ? and episode = ?", (media_type, tmdb_id, season, episode))
		refresh_container(refresh == 'true')
	except: pass

def batch_erase_bookmark(watched_indicators, insert_list, action):
	try:
		if action == 'mark_as_watched': modified_list = [(i[0], i[1], i[2], i[3]) for i in insert_list]
		else: modified_list = insert_list
		if watched_indicators == 1:
			def _process():
				media_type, tmdb_id = insert_list[0][0], insert_list[0][1]
				bookmarks = get_bookmarks(watched_indicators, media_type)
				for i in insert_list:
					try: resume_point, curr_time, resume_id = detect_bookmark(bookmarks, tmdb_id, i[2], i[3])
					except: continue
					try:
						sleep(1100)
						trakt_progress('clear_progress', i[0], i[1], 0, i[2], i[3], resume_id)
					except: pass
			Thread(target=_process).start()
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.executemany("DELETE FROM progress where db_type=? and media_id=? and season = ? and episode = ?", modified_list)
	except: pass

def set_bookmark(params):
	try:
		media_type, tmdb_id, curr_time, total_time = params.get('media_type'), params.get('tmdb_id'), params.get('curr_time'), params.get('total_time')
		refresh = False if params.get('from_playback', 'false') == 'true' else True
		title, season, episode = params.get('title'), params.get('season'), params.get('episode')
		adjusted_current_time = float(curr_time) - 5
		resume_point = round(adjusted_current_time/float(total_time)*100,1)
		watched_indicators = watched_indicators_function()
		if watched_indicators == 1:
			if trakt_official_status(media_type) == False: return
			else: trakt_progress('set_progress', media_type, tmdb_id, resume_point, season, episode, refresh_trakt=True)
		else:
			erase_bookmark(media_type, tmdb_id, season, episode)
			data_base = get_database(watched_indicators)
			last_played = get_last_played_value(data_base)
			dbcon = make_database_connection(data_base)
			dbcur = set_PRAGMAS(dbcon)
			dbcur.execute("INSERT OR REPLACE INTO progress VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
						(media_type, tmdb_id, season, episode, str(resume_point), str(curr_time), last_played, 0, title))
		refresh_container(refresh)
	except: pass

def get_watched_info_movie(watched_indicators):
	info = []
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.execute("SELECT media_id, title, last_played FROM watched_status WHERE db_type = ?", ('movie',))
		info = dbcur.fetchall()
	except: pass
	return info

def get_watched_info_tv(watched_indicators):
	info = []
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.execute("SELECT media_id, season, episode, title, last_played FROM watched_status WHERE db_type = ?", ('episode',))
		info = dbcur.fetchall()
	except: pass
	return info

def get_in_progress_movies(dummy_arg, page_no):
	dbcon = make_database_connection(get_database())
	dbcur = set_PRAGMAS(dbcon)
	dbcur.execute("SELECT media_id, title, last_played FROM progress WHERE db_type=?", ('movie',))
	data = dbcur.fetchall()
	test = get_watched_info_movie(watched_indicators_function())
	include_watched = True
	data = [{'media_id': i[0], 'title': i[1], 'last_played': i[2]} for i in data if not i[0] == '']
	if lists_sort_order('progress') == 0: original_list = sort_for_article(data, 'title', ignore_articles())
	else: original_list = sorted(data, key=lambda x: x['last_played'], reverse=True)
	if paginate(): final_list, all_pages, total_pages = paginate_list(original_list, page_no, page_limit())
	else: final_list, all_pages, total_pages = original_list, [], 1
	return final_list, all_pages, total_pages

def get_in_progress_tvshows(dummy_arg, page_no):
	def _process(item):
		tmdb_id = item['media_id']
		meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
		watched_status = get_watched_status_tvshow(watched_info, tmdb_id, meta.get('total_aired_eps'))
		if watched_status[0] == 0: data_append(item)
	data, duplicates = [], set()
	data_append, duplicates_add = data.append, duplicates.add
	watched_indicators = watched_indicators_function()
	meta_user_info = metadata_user_info()
	watched_info = get_watched_info_tv(watched_indicators)
	watched_info.sort(key=lambda x: (x[0], x[4]), reverse=True)
	prelim_data = [{'media_id': i[0], 'title': i[3], 'last_played': i[4]} for i in watched_info if not (i[0] in duplicates or duplicates_add(i[0]))]
	if watched_indicators == 1:
		try: exclude_list = trakt_get_hidden_items('progress_watched')
		except: exclude_list = []
		prelim_data = [i for i in prelim_data if not int(i['media_id']) in exclude_list]
	threads = list(make_thread_list(_process, prelim_data))
	[i.join() for i in threads]
	if lists_sort_order('progress') == 0: original_list = sort_for_article(data, 'title', ignore_articles())
	else: original_list = sorted(data, key=lambda x: x['last_played'], reverse=True)
	if paginate(): final_list, all_pages, total_pages = paginate_list(original_list, page_no, page_limit())
	else: final_list, all_pages, total_pages = original_list, [], 1
	return final_list, all_pages, total_pages

def get_in_progress_episodes():
	dbcon = make_database_connection(get_database())
	dbcur = set_PRAGMAS(dbcon)
	dbcur.execute('''SELECT media_id, season, episode, resume_point, last_played, title FROM progress WHERE db_type=?''', ('episode',))
	data = dbcur.fetchall()
	if lists_sort_order('progress') == 0: data = sort_for_article(data, 5, ignore_articles())
	else: data.sort(key=lambda k: k[4], reverse=True)
	episode_list = [{'media_ids': {'tmdb': i[0]}, 'season': int(i[1]), 'episode': int(i[2]), 'resume_point': float(i[3])} for i in data]
	return episode_list

def get_watched_items(media_type, page_no):
	watched_indicators = watched_indicators_function()
	if media_type == 'tvshow':
		def _process(item):
			tmdb_id = item['media_id']
			meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
			watched_status = get_watched_status_tvshow(watched_info, tmdb_id, meta.get('total_aired_eps'))
			if watched_status[0] == 1: data_append(item)
		watched_info = get_watched_info_tv(watched_indicators)
		meta_user_info = metadata_user_info()
		duplicates = set()
		duplicates_add = duplicates.add
		data = []
		data_append = data.append
		prelim_data = [{'media_id': i[0], 'title': i[3], 'last_played': i[4]} for i in watched_info if not (i[0] in duplicates or duplicates_add(i[0]))]
		threads = list(make_thread_list(_process, prelim_data))
		[i.join() for i in threads]
	else:
		watched_info = get_watched_info_movie(watched_indicators)
		data = [{'media_id': i[0], 'title': i[1], 'last_played': i[2]} for i in watched_info]
	if lists_sort_order('watched') == 0: original_list = sort_for_article(data, 'title', ignore_articles())
	else: original_list = sorted(data, key=lambda x: x['last_played'], reverse=True)
	if paginate(): final_list, all_pages, total_pages = paginate_list(original_list, page_no, page_limit())
	else: final_list, all_pages, total_pages = original_list, [], 1
	return final_list, all_pages, total_pages

def get_watched_status_movie(watched_info, tmdb_id):
	try:
		watched = [i for i in watched_info if i[0] == tmdb_id]
		if watched: return 1, 5
		return 0, 4
	except: return 0, 4

def get_watched_status_tvshow(watched_info, tmdb_id, aired_eps):
	playcount, overlay, watched, unwatched = 0, 4, 0, aired_eps
	try:
		watched = min(len([i for i in watched_info if i[0] == tmdb_id]), aired_eps)
		unwatched = aired_eps - watched
		if watched >= aired_eps and not aired_eps == 0: playcount, overlay = 1, 5
	except: pass
	return playcount, overlay, watched, unwatched

def get_watched_status_season(watched_info, tmdb_id, season, aired_eps):
	playcount, overlay, watched, unwatched = 0, 4, 0, aired_eps
	try:
		watched = min(len([i for i in watched_info if i[0] == tmdb_id and i[1] == season]), aired_eps)
		unwatched = aired_eps - watched
		if watched >= aired_eps and not aired_eps == 0: playcount, overlay = 1, 5
	except: pass
	return playcount, overlay, watched, unwatched

def get_watched_status_episode(watched_info, tmdb_id, season='', episode=''):
	try:
		watched = [i for i in watched_info if i[0] == tmdb_id and (i[1], i[2]) == (season, episode)]
		if watched: return 1, 5
		else: return 0, 4
	except: return 0, 4

def mark_as_watched_unwatched_movie(params):
	action, media_type = params.get('action'), 'movie'
	refresh, from_playback = params.get('refresh', 'true') == 'true', params.get('from_playback', 'false') == 'true'
	if from_playback: refresh = False
	tmdb_id, title, year = params.get('tmdb_id'), params.get('title'), params.get('year')
	watched_indicators = watched_indicators_function()
	if watched_indicators == 1:
		if from_playback == 'true' and trakt_official_status(media_type) == False: sleep(1000)
		elif not trakt_watched_unwatched(action, 'movies', tmdb_id): return notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', media_type)
	mark_as_watched_unwatched(watched_indicators, media_type, tmdb_id, action, title=title)
	refresh_container(refresh)

def mark_as_watched_unwatched_tvshow(params):
	action, tmdb_id = params.get('action'), params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	watched_indicators = watched_indicators_function()
	progressDialogBG.create(ls(32577), '')
	if watched_indicators == 1:
		if not trakt_watched_unwatched(action, 'shows', tmdb_id, tvdb_id): return notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	data_base = get_database(watched_indicators)
	title, year = params.get('title', ''), params.get('year', '')
	meta_user_info = metadata_user_info()
	current_date = get_datetime()
	insert_list = []
	insert_append = insert_list.append
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
	season_data = meta['season_data']
	season_data = [i for i in season_data if i['season_number'] > 0]
	total = len(season_data)
	last_played = get_last_played_value(data_base)
	for count, item in enumerate(season_data, 1):
		season_number = item['season_number']
		ep_data = metadata.season_episodes_meta(season_number, meta, meta_user_info)
		for ep in ep_data:
			season_number = ep['season']
			ep_number = ep['episode']
			display = 'S%.2dE%.2d' % (int(season_number), int(ep_number))
			progressDialogBG.update(int(float(count)/float(total)*100), ls(32577), '%s' % display)
			episode_date, premiered = adjust_premiered_date(ep['premiered'], date_offset())
			if not episode_date or current_date < episode_date: continue
			insert_append(make_batch_insert(action, 'episode', tmdb_id, season_number, ep_number, last_played, title))
	batch_mark_as_watched_unwatched(watched_indicators, insert_list, action)
	progressDialogBG.close()
	refresh_container()

def mark_as_watched_unwatched_season(params):
	season = int(params.get('season'))
	if season == 0: return notification(32490)
	action, title, year, tmdb_id = params.get('action'), params.get('title'), params.get('year'), params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	watched_indicators = watched_indicators_function()
	insert_list = []
	insert_append = insert_list.append
	progressDialogBG.create(ls(32577), '')
	if watched_indicators == 1:
		if not trakt_watched_unwatched(action, 'season', tmdb_id, tvdb_id, season): return notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	data_base = get_database(watched_indicators)
	meta_user_info = metadata_user_info()
	current_date = get_datetime()
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
	ep_data = metadata.season_episodes_meta(season, meta, meta_user_info)
	last_played = get_last_played_value(data_base)
	for count, item in enumerate(ep_data, 1):
		season_number = item['season']
		ep_number = item['episode']
		display = 'S%.2dE%.2d' % (season_number, ep_number)
		episode_date, premiered = adjust_premiered_date(item['premiered'], date_offset())
		if not episode_date or current_date < episode_date: continue
		progressDialogBG.update(int(float(count) / float(len(ep_data)) * 100), ls(32577), '%s' % display)
		insert_append(make_batch_insert(action, 'episode', tmdb_id, season_number, ep_number, last_played, title))
	batch_mark_as_watched_unwatched(watched_indicators, insert_list, action)
	progressDialogBG.close()
	refresh_container()

def mark_as_watched_unwatched_episode(params):
	action, media_type = params.get('action'), 'episode'
	refresh, from_playback = params.get('refresh', 'true') == 'true', params.get('from_playback', 'false') == 'true'
	if from_playback: refresh = False
	tmdb_id = params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	season, episode, title, year = int(params.get('season')), int(params.get('episode')), params.get('title'), params.get('year')
	watched_indicators = watched_indicators_function()
	if season == 0: notification(32490); return
	if watched_indicators == 1:
		if from_playback == 'true' and trakt_official_status(media_type) == False: sleep(1000)
		elif not trakt_watched_unwatched(action, media_type, tmdb_id, tvdb_id, season, episode): return notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	mark_as_watched_unwatched(watched_indicators, media_type, tmdb_id, action, season, episode, title)
	refresh_container(refresh)

def mark_as_watched_unwatched(watched_indicators, media_type='', tmdb_id='', action='', season='', episode='', title=''):
	try:
		data_base = get_database(watched_indicators)
		last_played = get_last_played_value(data_base)
		dbcon = make_database_connection(data_base)
		dbcur = set_PRAGMAS(dbcon)
		if action == 'mark_as_watched':
			dbcur.execute("INSERT OR REPLACE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", (media_type, tmdb_id, season, episode, last_played, title))
		elif action == 'mark_as_unwatched':
			dbcur.execute("DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", (media_type, tmdb_id, season, episode))
		erase_bookmark(media_type, tmdb_id, season, episode)
	except: notification(32574)

def batch_mark_as_watched_unwatched(watched_indicators, insert_list, action):
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		if action == 'mark_as_watched':
			dbcur.executemany("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", insert_list)
		elif action == 'mark_as_unwatched':
			dbcur.executemany("DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", insert_list)
		batch_erase_bookmark(watched_indicators, insert_list, action)
	except: notification(32574)

def get_last_played_value(database_type):
	if database_type == WATCHED_DB: return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	else: return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')

def make_batch_insert(action, media_type, tmdb_id, season, episode, last_played, title):
	if action == 'mark_as_watched': return (media_type, tmdb_id, season, episode, last_played, title)
	else: return (media_type, tmdb_id, season, episode)

def clear_local_bookmarks():
	try:
		dbcon = make_database_connection(get_video_database_path())
		dbcur = set_PRAGMAS(dbcon)
		file_ids = dbcur.execute("SELECT idFile FROM files WHERE strFilename LIKE 'plugin.video.fen%'").fetchall()
		for i in ('bookmark', 'streamdetails', 'files'):
			dbcur.executemany("DELETE FROM %s WHERE idFile=?" % i, file_ids)
	except: pass

def refresh_container(refresh=True):
	if refresh: kodi_refresh()
