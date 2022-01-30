# -*- coding: utf-8 -*-
import time
import sqlite3 as database
from datetime import datetime, timedelta
from modules.kodi_utils import translate_path, confirm_dialog, path_exists
# from modules.kodi_utils import logger

dbfile = translate_path('special://profile/addon_data/plugin.video.fen/providerscache.db')
timeout = 240

SELECT_RESULTS = 'SELECT results, expires FROM results_data WHERE provider = ? AND db_type = ? AND tmdb_id = ? AND title = ? AND year = ? AND season = ? AND episode = ?'
DELETE_RESULTS = 'DELETE FROM results_data WHERE provider = ? AND db_type = ? AND tmdb_id = ? AND title = ? AND year = ? AND season = ? AND episode = ?'
INSERT_RESULTS = 'INSERT OR REPLACE INTO results_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
SINGLE_DELETE = 'DELETE FROM results_data WHERE db_type=? AND tmdb_id=?'
FULL_DELETE = 'DELETE FROM results_data'

class ExternalProvidersCache(object):
	def __init__(self):
		self._connect_database()
		self._set_PRAGMAS()
		self.time = datetime.now()

	def get(self, source, db_type, tmdb_id, title, year, season, episode):
		result = None
		try:
			self._execute(SELECT_RESULTS, (source, db_type, tmdb_id, title, year, season, episode))
			cache_data = self.dbcur.fetchone()
			if cache_data:
				if cache_data[1] > self._get_timestamp(self.time): result = eval(cache_data[0])
				else: self.delete(source, db_type, title, year, tmdb_id, season, episode, dbcon)
		except: pass
		return result

	def set(self, source, db_type, tmdb_id, title, year, season, episode, results, expire_time):
		try:
			expiration = timedelta(hours=expire_time)
			expires = self._get_timestamp(self.time + expiration)
			self._execute(INSERT_RESULTS, (source, db_type, tmdb_id, title, year, season, episode, repr(results), int(expires)))
		except: pass

	def delete(self, source, db_type, tmdb_id, title, season, episode):
		try: self._execute(DELETE_RESULTS, (source, db_type, tmdb_id, title, season, episode))
		except: return

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

	def delete_cache(self, silent=False):
		try:
			if not path_exists(dbfile): return 'failure'
			if not silent and not confirm_dialog(): return 'cancelled'
			self._execute(FULL_DELETE, ())
			self._vacuum()
			return 'success'
		except: return 'failure'

	def delete_cache_single(self, db_type, tmdb_id):
		try:
			if not path_exists(dbfile): return False
			self._execute(SINGLE_DELETE, (db_type, tmdb_id))
			self._vacuum()
			return True
		except: return False

	def _connect_database(self):
		self.dbcon = database.connect(dbfile, timeout=timeout)

	def _commit(self):
		self.dbcon.commit()

	def _close(self):
		self.dbcon.close()

	def _execute(self, command, params):
		self.dbcur.execute(command, params)
		self._commit()

	def _vacuum(self):
		self.dbcur.execute('VACUUM')
		self._commit()
		self._close()

	def _set_PRAGMAS(self):
		self.dbcur = self.dbcon.cursor()
		self.dbcur.execute('''PRAGMA synchronous = OFF''')
		self.dbcur.execute('''PRAGMA journal_mode = OFF''')
