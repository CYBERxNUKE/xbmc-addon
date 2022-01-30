# -*- coding: utf-8 -*-
import time
import sqlite3 as database
from datetime import datetime, timedelta
from modules.kodi_utils import translate_path
# from modules.kodi_utils import logger

dbfile = translate_path('special://profile/addon_data/plugin.video.fen/debridcache.db')

GET_MANY = 'SELECT * FROM debrid_data WHERE hash in (%s)'
SET_MANY = 'INSERT INTO debrid_data VALUES (?, ?, ?, ?)'
REMOVE_MANY = 'DELETE FROM debrid_data WHERE hash=?'
CLEAR = 'DELETE FROM debrid_data'
CLEAR_DEBRID = 'DELETE FROM debrid_data WHERE debrid=?'

EXPIRES_1_DAY = timedelta(days=1)

class DebridCache:
	def get_many(self, hash_list):
		result = None
		try:
			current_time = self._get_timestamp(datetime.now())
			dbcon = database.connect(dbfile, timeout=40.0)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute(GET_MANY % (', '.join('?' for _ in hash_list)), hash_list)
			cache_data = dbcur.fetchall()
			if cache_data:
				if cache_data[0][3] > current_time: result = cache_data
				else: self.remove_many(cache_data)
		except: pass
		return result

	def set_many(self, hash_list, debrid, expiration=EXPIRES_1_DAY):
		try:
			expires = self._get_timestamp(datetime.now() + expiration)
			insert_list = [(i[0], debrid, i[1], expires) for i in hash_list]
			dbcon = database.connect(dbfile, timeout=40.0)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.executemany(SET_MANY, insert_list)
			dbcon.commit()
		except: pass

	def remove_many(self, old_cached_data):
		try:
			old_cached_data = [(str(i[0]),) for i in old_cached_data]
			dbcon = database.connect(dbfile, timeout=40.0)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.executemany(REMOVE_MANY, old_cached_data)
			dbcon.commit()
		except: pass

	def clear_debrid_results(self, debrid):
		try:
			dbcon = database.connect(dbfile, timeout=40.0)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute(CLEAR_DEBRID, (debrid,))
			dbcon.commit()
			dbcur.execute('VACUUM')
			dbcon.close()
			return True
		except: return False

	def _set_PRAGMAS(self, dbcon):
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		return dbcur

	def clear_database(self):
		try:
			dbcon = database.connect(dbfile)
			dbcur = dbcon.cursor()
			dbcur.execute(CLEAR)
			dbcon.commit()
			dbcur.execute('VACUUM')
			dbcon.close()
			return 'success'
		except: return 'failure'

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

debrid_cache = DebridCache()