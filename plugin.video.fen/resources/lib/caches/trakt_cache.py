# -*- coding: utf-8 -*-
import sqlite3 as database
from modules.utils import to_utf8
from modules.kodi_utils import translate_path, sleep, confirm_dialog, close_all_dialog
# from modules.kodi_utils import logger

dbfile = translate_path('special://profile/addon_data/plugin.video.fen/traktcache2.db')
timeout = 60

SELECT = 'SELECT id FROM trakt_data'
DELETE = 'DELETE FROM trakt_data WHERE id=?'
DELETE_LIKE = 'DELETE FROM trakt_data WHERE id LIKE "%s"'
WATCHED_INSERT = 'INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)'
WATCHED_DELETE = 'DELETE FROM watched_status WHERE db_type = ?'
PROGRESS_INSERT = 'INSERT OR IGNORE INTO progress VALUES (?, ?, ?, ?, ?, ?)'
PROGRESS_DELETE = 'DELETE FROM progress WHERE db_type = ?'
BASE_DELETE = 'DELETE FROM %s'
TC_BASE_GET = 'SELECT data FROM trakt_data WHERE id = ?'
TC_BASE_SET = 'INSERT OR REPLACE INTO trakt_data (id, data) VALUES (?, ?)'
TC_BASE_DELETE = 'DELETE FROM trakt_data WHERE id = ?'

class TraktWatched:
	def __init__(self):
		self._connect_database()
		self._set_PRAGMAS()

	def set_bulk_movie_watched(self, insert_list):
		self._delete(WATCHED_DELETE, ('movie',))
		self._executemany(WATCHED_INSERT, insert_list)
		self._close()

	def set_bulk_tvshow_watched(self, insert_list):
		self._delete(WATCHED_DELETE, ('episode',))
		self._executemany(WATCHED_INSERT, insert_list)
		self._close()

	def set_bulk_movie_progress(self, insert_list):
		self._delete(PROGRESS_DELETE, ('movie',))
		self._executemany(PROGRESS_INSERT, insert_list)
		self._close()

	def set_bulk_tvshow_progress(self, insert_list):
		self._delete(PROGRESS_DELETE, ('episode',))
		self._executemany(PROGRESS_INSERT, insert_list)
		self._close()

	def _executemany(self, command, insert_list):
		self.dbcur.executemany(command, insert_list)
		self._commit()

	def _delete(self, command, args):
		self.dbcur.execute(command, args)
		self._commit()
		self.dbcur.execute('VACUUM')

	def _connect_database(self):
		self.dbcon = database.connect(dbfile, timeout=timeout)

	def _commit(self):
		self.dbcon.commit()

	def _close(self):
		self.dbcon.close()

	def _set_PRAGMAS(self):
		self.dbcur = self.dbcon.cursor()
		self.dbcur.execute('''PRAGMA synchronous = OFF''')
		self.dbcur.execute('''PRAGMA journal_mode = OFF''')

class TraktCache:
	def get(self, string):
		result = None
		try:
			dbcon = self.connect_database()
			dbcur = self.set_PRAGMAS(dbcon)
			dbcur.execute(TC_BASE_GET, (string,))
			cache_data = dbcur.fetchone()
			if cache_data: result = eval(cache_data[0])
		except: pass
		return result

	def set(self, string, data):
		try:
			dbcon = self.connect_database()
			dbcur = self.set_PRAGMAS(dbcon)
			dbcur.execute(TC_BASE_SET, (string, repr(data)))
			dbcon.commit()
		except: return None

	def delete(self, string, dbcon=None):
		try:
			if not dbcon: self.connect_database()
			dbcur = dbcon.cursor()
			dbcur.execute(TC_BASE_DELETE, (string,))
			dbcon.commit()
		except: pass

	def connect_database(self):
		return database.connect(dbfile, timeout=timeout)

	def set_PRAGMAS(self, dbcon):
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		return dbcur

_cache = TraktCache()

def cache_trakt_object(function, string, url):
	cache = _cache.get(string)
	if cache: return to_utf8(cache)
	result = function(url)
	_cache.set(string, result)
	return to_utf8(result)

def reset_activity(latest_activities):
	cached_data = None
	try:
		action = 'trakt_get_activity'
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute('SELECT data FROM trakt_data WHERE id=?', (action,))
		cached_data = dbcur.fetchone()
		if cached_data: cached_data = eval(cached_data[0])
		else: cached_data = default_activities()
		dbcur.execute(DELETE, (action,))
		dbcon.commit()
		_cache.set(action, latest_activities)
	except: pass
	return cached_data

def clear_trakt_hidden_data(list_type):
	action = 'trakt_hidden_items_%s' % list_type
	try:
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute(DELETE, (action,))
		dbcon.commit()
	except: pass

def clear_trakt_collection_watchlist_data(list_type, db_type):
	if db_type == 'movies': db_type = 'movie' 
	if db_type in ('tvshows', 'shows'): db_type = 'tvshow' 
	action = 'trakt_%s_%s' % (list_type, db_type)
	try:
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute(DELETE, (action,))
		dbcon.commit()
	except: pass

def clear_trakt_list_contents_data(list_type):
	action = 'trakt_list_contents_' + list_type + '_%'
	try:
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute(DELETE_LIKE % action)
		dbcon.commit()
	except: pass

def clear_trakt_list_data(list_type):
	action = 'trakt_%s' % list_type
	try:
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute(DELETE, (action,))
		dbcon.commit()
	except: pass

def clear_trakt_calendar():
	try:
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute(DELETE_LIKE % 'trakt_get_my_calendar_%')
		dbcon.commit()
	except: return

def clear_trakt_recommendations(db_type):
	action = 'trakt_recommendations_%s' % (db_type)
	try:
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		dbcur.execute(DELETE, (action,))
		dbcon.commit()
	except: pass

def clear_all_trakt_cache_data(silent=False, confirm=True):
	def _process():
		dbcon = _cache.connect_database()
		dbcur = dbcon.cursor()
		for table in ('trakt_data', 'progress', 'watched_status'):
			dbcur.execute(BASE_DELETE % table)
			dbcon.commit()
		dbcur.execute('VACUUM')
		dbcon.close()
	if silent:
		return _process()
	else:
		if confirm:
			if not confirm_dialog(): return False
		from apis.trakt_api import trakt_sync_activities
		close_all_dialog()
		sleep(200)
		try:
			_process()
			trakt_sync_activities()
			return True
		except: return False

def default_activities():
	return {
			'all': '2020-01-01T00:00:01.000Z',
			'movies':
				{
				'watched_at': '2020-01-01T00:00:01.000Z',
				'collected_at': '2020-01-01T00:00:01.000Z',
				'rated_at': '2020-01-01T00:00:01.000Z',
				'watchlisted_at': '2020-01-01T00:00:01.000Z',
				'recommendations_at': '2020-01-01T00:00:01.000Z',
				'commented_at': '2020-01-01T00:00:01.000Z',
				'paused_at': '2020-01-01T00:00:01.000Z',
				'hidden_at': '2020-01-01T00:00:01.000Z'
				},
			'episodes':
				{
				'watched_at': '2020-01-01T00:00:01.000Z',
				'collected_at': '2020-01-01T00:00:01.000Z',
				'rated_at': '2020-01-01T00:00:01.000Z',
				'watchlisted_at': '2020-01-01T00:00:01.000Z',
				'commented_at': '2020-01-01T00:00:01.000Z',
				'paused_at': '2020-01-01T00:00:01.000Z'
				},
			'shows':
				{
				'rated_at': '2020-01-01T00:00:01.000Z',
				'watchlisted_at': '2020-01-01T00:00:01.000Z',
				'recommendations_at': '2020-01-01T00:00:01.000Z',
				'commented_at': '2020-01-01T00:00:01.000Z', 
				'hidden_at': '2020-01-01T00:00:01.000Z'
				},
			'seasons':
				{
				'rated_at': '2020-01-01T00:00:01.000Z',
				'watchlisted_at': '2020-01-01T00:00:01.000Z',
				'commented_at': '2020-01-01T00:00:01.000Z',
				'hidden_at': '2020-01-01T00:00:01.000Z'
				},
			'comments':
				{
				'liked_at': '2020-01-01T00:00:01.000Z'
				},
			'lists':
				{
				'liked_at': '2020-01-01T00:00:01.000Z',
				'updated_at': '2020-01-01T00:00:01.000Z',
				'commented_at': '2020-01-01T00:00:01.000Z'
				},
			'watchlist':
				{
				'updated_at': '2020-01-01T00:00:01.000Z'
				},
			'recommendations':
				{
				'updated_at': '2020-01-01T00:00:01.000Z'
				},
			'account':
				{
				'settings_at': '2020-01-01T00:00:01.000Z',
				'followed_at': '2020-01-01T00:00:01.000Z',
				'following_at': '2020-01-01T00:00:01.000Z',
				'pending_at': '2020-01-01T00:00:01.000Z'
				}
			}
	