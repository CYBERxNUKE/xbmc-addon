# -*- coding: utf-8 -*-
from threading import Thread
from datetime import datetime
import sqlite3 as database
import metadata
from apis.trakt_api import trakt_watched_unwatched, trakt_official_status, trakt_progress
from caches.trakt_cache import clear_trakt_collection_watchlist_data
from modules import kodi_utils
from modules import settings
from modules.nav_utils import paginate_list
from modules.utils import to_unicode, get_datetime, adjust_premiered_date, sort_for_article, to_utf8, make_thread_list
# from modules.kodi_utils import logger

WATCHED_DB = kodi_utils.translate_path('special://profile/addon_data/plugin.video.fen/watched_status.db')
TRAKT_DB = kodi_utils.translate_path('special://profile/addon_data/plugin.video.fen/traktcache2.db')
ls = kodi_utils.local_string

def get_next_episodes(watched_info):
	seen = set()
	watched_info = [i for i in watched_info if not i[0] is None]
	watched_info.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
	return [{'tmdb_id': i[0], 'season': int(i[1]), 'episode': int(i[2]), 'last_played': i[4]} for i in watched_info if not (i[0] in seen or seen.add(i[0]))]

def get_resumetime(bookmarks, tmdb_id, season='', episode=''):
	try: resumetime = str((int(round(float(detect_bookmark(bookmarks, tmdb_id, season, episode)[0])))/float(100))*2400)
	except: resumetime = '0'
	return resumetime

def get_progress_percent(resumetime, duration):
	try: percent = str(int(round(float(resumetime)/duration*100)))
	except: percent = '0'
	return percent

def detect_bookmark(bookmarks, tmdb_id, season='', episode=''):
	return [(i[1], i[2]) for i in bookmarks if i[0] == str(tmdb_id) and i[3] == season and i[4] == episode][0]

def get_bookmarks(db_type, watched_indicators):
	try:
		if watched_indicators == 1: database_file = TRAKT_DB
		else: database_file = WATCHED_DB
		dbcon = database.connect(database_file)
		dbcur = dbcon.cursor()
		result = dbcur.execute("SELECT media_id, resume_point, curr_time, season, episode FROM progress WHERE db_type = ?", (db_type,))
		return result.fetchall()
	except: pass

def set_bookmark(db_type, tmdb_id, curr_time, total_time, season='', episode=''):
	try:
		erase_bookmark(db_type, tmdb_id, season, episode)
		adjusted_current_time = float(curr_time) - 5
		resume_point = round(adjusted_current_time/float(total_time)*100,1)
		watched_indicators = settings.watched_indicators()
		if watched_indicators == 1:
			trakt_progress('set_progress', db_type, tmdb_id, resume_point, season, episode)
			database_file = TRAKT_DB
		else: database_file = WATCHED_DB
		dbcon = database.connect(database_file)
		dbcur = dbcon.cursor()
		dbcur.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?, ?)", (db_type, tmdb_id, season, episode, str(resume_point), str(curr_time)))
		dbcon.commit()
		if settings.sync_kodi_library_watchstatus():
			from modules.kodi_library import set_bookmark_kodi_library
			set_bookmark_kodi_library(db_type, tmdb_id, curr_time, total_time, season, episode)
	except: pass

def erase_bookmark(db_type, tmdb_id, season='', episode='', refresh='false'):
	try:
		watched_indicators = settings.watched_indicators()
		if watched_indicators == 1:
			bookmarks = get_bookmarks(db_type, watched_indicators)
			if db_type == 'episode': season, episode = int(season), int(episode)
			try: resume_point, curr_time = detect_bookmark(bookmarks, tmdb_id, season, episode)
			except: return
			trakt_progress('clear_progress', db_type, tmdb_id, 0, season, episode)
			database_file = TRAKT_DB
		else: database_file = WATCHED_DB
		dbcon = database.connect(database_file)
		dbcur = dbcon.cursor()
		dbcur.execute("DELETE FROM progress where db_type=? and media_id=? and season = ? and episode = ?", (db_type, tmdb_id, season, episode))
		dbcon.commit()
		refresh_container(refresh)
	except: pass

def batch_erase_bookmark(insert_list, action, watched_indicators):
	try:
		if action == 'mark_as_watched': modified_list = [(i[0], i[1], i[2], i[3]) for i in insert_list]
		else: modified_list = insert_list
		if watched_indicators == 1:
			def _process(arg):
				try: trakt_progress(*arg)
				except: pass
			process_list = []
			process_list_append = process_list.append
			db_type = insert_list[0][0]
			tmdb_id = insert_list[0][1]
			bookmarks = get_bookmarks(db_type, watched_indicators)
			for i in insert_list:
				try: resume_point, curr_time = detect_bookmark(bookmarks, tmdb_id, i[2], i[3])
				except: continue
				process_list_append(('clear_progress', i[0], i[1], 0, i[2], i[3]))
			if process_list: threads = list(make_thread_list(_process, process_list, Thread))
			database_file = TRAKT_DB
		else: database_file = WATCHED_DB
		dbcon = database.connect(database_file)
		dbcur = dbcon.cursor()
		dbcur.executemany("DELETE FROM progress where db_type=? and media_id=? and season = ? and episode = ?", modified_list)
		dbcon.commit()
	except: pass

def get_watched_info_tv(watched_indicators):
	check_trakt_refresh()
	info = []
	try:
		if watched_indicators == 1: database_file = TRAKT_DB
		else: database_file = WATCHED_DB
		dbcon = database.connect(database_file)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT media_id, season, episode, title, last_played FROM watched_status WHERE db_type = ?", ('episode',))
		info = dbcur.fetchall()
		dbcon.close()
	except: pass
	return info

def get_watched_info_movie(watched_indicators):
	check_trakt_refresh()
	info = []
	try:
		if watched_indicators == 1: database_file = TRAKT_DB
		else: database_file = WATCHED_DB
		dbcon = database.connect(database_file)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT media_id, title, last_played FROM watched_status WHERE db_type = ?", ('movie',))
		info = dbcur.fetchall()
		dbcon.close()
	except: pass
	return info

def get_in_progress_movies(dummy_arg, page_no, letter):
	check_trakt_refresh()
	watched_indicators = settings.watched_indicators()
	paginate = settings.paginate()
	limit = settings.page_limit()
	if watched_indicators == 1: database_file = TRAKT_DB
	else: database_file = WATCHED_DB
	dbcon = database.connect(database_file)
	dbcur = dbcon.cursor()
	dbcur.execute('''SELECT media_id FROM progress WHERE db_type=? ORDER BY rowid DESC''', ('movie',))
	rows = dbcur.fetchall()
	data = reversed([i[0] for i in rows if not i[0] == ''])
	original_list = [{'media_id': i} for i in data]
	if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def get_in_progress_tvshows(dummy_arg, page_no, letter):
	def _process(item):
		tmdb_id = item['media_id']
		meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
		watched_status = get_watched_status_tvshow(watched_info, tmdb_id, meta.get('total_aired_eps'))
		if watched_status[0] == 0: append(item)
	check_trakt_refresh()
	duplicates = set()
	data = []
	append = data.append
	watched_indicators = settings.watched_indicators()
	paginate = settings.paginate()
	limit = settings.page_limit()
	meta_user_info = metadata.retrieve_user_info()
	watched_info = get_watched_info_tv(watched_indicators)
	prelim_data = [{'media_id': i[0], 'title': i[3]} for i in watched_info if not (i[0] in duplicates or duplicates.add(i[0]))]
	threads = list(make_thread_list(_process, prelim_data, Thread))
	[i.join() for i in threads]
	original_list = sort_for_article(data, 'title', settings.ignore_articles())
	if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def get_in_progress_episodes():
	watched_indicators = settings.watched_indicators()
	if watched_indicators == 1: database_file = TRAKT_DB
	else: database_file = WATCHED_DB
	dbcon = database.connect(database_file)
	dbcur = dbcon.cursor()
	dbcur.execute('''SELECT media_id, season, episode, resume_point FROM progress WHERE db_type=? ORDER BY rowid DESC''', ('episode',))
	data = dbcur.fetchall()
	episode_list = reversed([{'tmdb_id': i[0], 'season': int(i[1]), 'episode': int(i[2]), 'resume_point': float(i[3])} for i in data])
	return episode_list

def get_watched_items(db_type, page_no, letter):
	paginate = settings.paginate()
	limit = settings.page_limit()
	watched_indicators = settings.watched_indicators()
	if db_type == 'tvshow':
		from threading import Thread
		from modules.utils import make_thread_list
		def _process(item):
			tmdb_id = item['media_id']
			meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
			watched_status = get_watched_status_tvshow(watched_info, tmdb_id, meta.get('total_aired_eps'))
			if watched_status[0] == 1: append(item)
		meta_user_info = metadata.retrieve_user_info()
		watched_info = get_watched_info_tv(watched_indicators)
		duplicates = set()
		data = []
		append = data.append
		prelim_data = [{'media_id': i[0], 'title': i[3]} for i in watched_info if not (i[0] in duplicates or duplicates.add(i[0]))]
		threads = list(make_thread_list(_process, prelim_data, Thread))
		[i.join() for i in threads]
		original_list = sort_for_article(data, 'title', settings.ignore_articles())
	else:
		watched_info = get_watched_info_movie(watched_indicators)
		data = [{'media_id': i[0], 'title': i[1]} for i in watched_info]
		original_list = sort_for_article(data, 'title', settings.ignore_articles())
	if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def get_watched_status_episode(watched_info, tmdb_id, season='', episode=''):
	try:
		watched = [i for i in watched_info if i[0] == tmdb_id and (i[1],i[2]) == (season,episode)]
		if watched: return 1, 5
		else: return 0, 4
	except: return 0, 4

def get_watched_status_season(watched_info, tmdb_id, season, aired_eps):
	playcount, overlay, watched, unwatched = 0, 4, 0, aired_eps
	try:
		watched = len([i for i in watched_info if i[0] == tmdb_id and i[1] == season])
		unwatched = aired_eps - watched
		if watched >= aired_eps and not aired_eps == 0: playcount, overlay = 1, 5
	except: pass
	return playcount, overlay, watched, unwatched

def get_watched_status_tvshow(watched_info, tmdb_id, aired_eps):
	playcount, overlay, watched, unwatched = 0, 4, 0, aired_eps
	try:
		watched = len([i for i in watched_info if i[0] == tmdb_id])
		unwatched = aired_eps - watched
		if watched >= aired_eps and not aired_eps == 0: playcount, overlay = 1, 5
	except: pass
	return playcount, overlay, watched, unwatched

def get_watched_status_movie(watched_info, tmdb_id):
	try:
		watched = [i for i in watched_info if i[0] == tmdb_id]
		if watched: return 1, 5
		return 0, 4
	except: return 0, 4

def mark_as_watched_unwatched_episode(params):
	action = params.get('action')
	db_type = 'episode'
	tmdb_id = params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	season = int(params.get('season'))
	episode = int(params.get('episode'))
	title = params.get('title')
	year = params.get('year')
	refresh = params.get('refresh', 'true')
	from_playback = params.get('from_playback', 'false')
	watched_indicators = settings.watched_indicators()
	if season == 0: kodi_utils.notification(32490); return
	if watched_indicators == 1:
		if from_playback == 'true'and trakt_official_status(db_type) == False: skip_trakt_mark = True
		else: skip_trakt_mark = False
		if skip_trakt_mark: kodi_utils.sleep(3000)
		elif not trakt_watched_unwatched(action, db_type, tmdb_id, tvdb_id, season, episode): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
		data_base = TRAKT_DB
	else: data_base = WATCHED_DB
	mark_as_watched_unwatched(db_type, tmdb_id, action, season, episode, title, data_base)
	erase_bookmark(db_type, tmdb_id, season, episode)
	if settings.sync_kodi_library_watchstatus():
		from modules.kodi_library import mark_as_watched_unwatched_kodi_library
		mark_as_watched_unwatched_kodi_library(db_type, action, title, year, season, episode)
	refresh_container(refresh)

def mark_as_watched_unwatched_season(params):
	season = int(params.get('season'))
	if season == 0: return kodi_utils.notification(32490)
	action = params.get('action')
	title = params.get('title')
	year = params.get('year')
	tmdb_id = params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	watched_indicators = settings.watched_indicators()
	insert_list = []
	insert_append = insert_list.append
	kodi_utils.progressDialogBG.create(ls(32577), '')
	if watched_indicators == 1:
		if not trakt_watched_unwatched(action, 'season', tmdb_id, tvdb_id, season): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
		data_base = TRAKT_DB
		data_base = TRAKT_DB
	else: data_base = WATCHED_DB
	meta_user_info = metadata.retrieve_user_info()
	adjust_hours = settings.date_offset()
	current_date = get_datetime()
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
	ep_data = metadata.season_episodes_meta(season, meta, meta_user_info)
	last_played = get_last_played_value(data_base)
	for count, item in enumerate(ep_data, 1):
		season_number = item['season']
		ep_number = item['episode']
		display = 'S%.2dE%.2d' % (season_number, ep_number)
		episode_date, premiered = adjust_premiered_date(item['premiered'], adjust_hours)
		if not episode_date or current_date < episode_date: continue
		kodi_utils.progressDialogBG.update(int(float(count) / float(len(ep_data)) * 100), ls(32577), '%s' % display)
		insert_append(make_batch_insert(action, 'episode', tmdb_id, season_number, ep_number, last_played, title))
	batch_mark_as_watched_unwatched(insert_list, action, data_base)
	batch_erase_bookmark(insert_list, action, watched_indicators)
	kodi_utils.progressDialogBG.close()
	if settings.sync_kodi_library_watchstatus(): batch_mark_kodi_library(action, insert_list, title, year)
	refresh_container()

def mark_as_watched_unwatched_tvshow(params):
	action = params.get('action')
	tmdb_id = params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	watched_indicators = settings.watched_indicators()
	kodi_utils.progressDialogBG.create(ls(32577), '')
	if watched_indicators == 1:
		if not trakt_watched_unwatched(action, 'shows', tmdb_id, tvdb_id): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
		data_base = TRAKT_DB
	else: data_base = WATCHED_DB
	title = params.get('title', '')
	year = params.get('year', '')
	meta_user_info = metadata.retrieve_user_info()
	adjust_hours = settings.date_offset()
	current_date = get_datetime()
	insert_list = []
	insert_append = insert_list.append
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
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
			kodi_utils.progressDialogBG.update(int(float(count)/float(total)*100), ls(32577), '%s' % display)
			episode_date, premiered = adjust_premiered_date(ep['premiered'], adjust_hours)
			if not episode_date or current_date < episode_date: continue
			insert_append(make_batch_insert(action, 'episode', tmdb_id, season_number, ep_number, last_played, title))
	batch_mark_as_watched_unwatched(insert_list, action, data_base)
	batch_erase_bookmark(insert_list, action, watched_indicators)
	kodi_utils.progressDialogBG.close()
	if settings.sync_kodi_library_watchstatus(): batch_mark_kodi_library(action, insert_list, title, year)
	refresh_container()

def mark_as_watched_unwatched_movie(params):
	action = params.get('action')
	db_type = 'movie'
	tmdb_id = params.get('tmdb_id')
	title = params.get('title')
	year = params.get('year')
	refresh = params.get('refresh', 'true')
	from_playback = params.get('from_playback', 'false')
	watched_indicators = settings.watched_indicators()
	if watched_indicators == 1:
		if from_playback == 'true'and trakt_official_status(db_type) == False: skip_trakt_mark = True
		else: skip_trakt_mark = False
		if skip_trakt_mark: kodi_utils.sleep(3000)
		elif not trakt_watched_unwatched(action, 'movies', tmdb_id): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', db_type)
		data_base = TRAKT_DB
		data_base = TRAKT_DB
	else: data_base = WATCHED_DB
	mark_as_watched_unwatched(db_type, tmdb_id, action, title=title, data_base=data_base)
	erase_bookmark(db_type, tmdb_id)
	if settings.sync_kodi_library_watchstatus():
		from modules.kodi_library import mark_as_watched_unwatched_kodi_library
		mark_as_watched_unwatched_kodi_library(db_type, action, title, year)
	refresh_container(refresh)

def mark_as_watched_unwatched(db_type='', tmdb_id='', action='', season='', episode='', title='', data_base=WATCHED_DB):
	try:
		last_played = get_last_played_value(data_base)
		dbcon = database.connect(data_base, timeout=40.0)
		erase_bookmark(db_type, tmdb_id, season, episode)
		if action == 'mark_as_watched':
			dbcon.execute("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", (db_type, tmdb_id, season, episode, last_played, to_unicode(title)))
		elif action == 'mark_as_unwatched':
			dbcon.execute("DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", (db_type, tmdb_id, season, episode))
		dbcon.commit()
	except: kodi_utils.notification(32574)

def batch_mark_as_watched_unwatched(insert_list, action, data_base=WATCHED_DB):
	try:
		dbcon = database.connect(data_base, timeout=40.0)
		if action == 'mark_as_watched':
			dbcon.executemany("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", insert_list)
		elif action == 'mark_as_unwatched':
			dbcon.executemany("DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", insert_list)
		dbcon.commit()
	except: kodi_utils.notification(32574)

def get_last_played_value(database_type):
	if database_type == WATCHED_DB: return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	else: return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')

def make_batch_insert(action, db_type, tmdb_id, season, episode, last_played, title):
	if action == 'mark_as_watched': return (db_type, tmdb_id, season, episode, last_played, to_unicode(title))
	else: return (db_type, tmdb_id, season, episode)

def batch_mark_kodi_library(action, insert_list, title, year):
	from modules.kodi_library import get_library_video, batch_mark_episodes_as_watched_unwatched_kodi_library
	in_library = get_library_video('tvshow', title, year)
	if not in_library: return
	if batch_mark_episodes_as_watched_unwatched_kodi_library(action, in_library, insert_list):
		kodi_utils.notification(32787, time=5000)

def check_trakt_refresh():
	if kodi_utils.get_property('fen_refresh_trakt_info') == 'true':
		from apis.trakt_api import trakt_sync_activities
		trakt_sync_activities(force_update=True)
		kodi_utils.clear_property('fen_refresh_trakt_info')

def refresh_container(refresh='true'):
	if refresh == 'true': kodi_utils.execute_builtin('Container.Refresh')

def clear_local_bookmarks():
	try:
		dbcon = database.connect(kodi_utils.get_video_database_path())
		dbcur = dbcon.cursor()
		file_ids = dbcur.execute("SELECT idFile FROM files WHERE strFilename LIKE 'plugin.video.fen%'").fetchall()
		for i in ('bookmark', 'streamdetails', 'files'):
			dbcur.executemany("DELETE FROM %s WHERE idFile=?" % i, file_ids)
		dbcur.connection.commit()
		dbcon.close()
	except: pass

