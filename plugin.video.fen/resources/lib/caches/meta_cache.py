# -*- coding: utf-8 -*-
import time
import sqlite3 as database
from datetime import datetime, timedelta
from modules.kodi_utils import translate_path, get_property, set_property, clear_property
from modules.utils import to_utf8
# from modules.kodi_utils import logger

EXPIRES_1_DAY = timedelta(days=1)
EXPIRES_30_DAYS = timedelta(days=30)

class MetaCache(object):
	def __init__(self):
		self.dbfile = translate_path('special://profile/addon_data/plugin.video.fen/metacache3.db')
		self.time = datetime.now()
		self.timeout = 240

	def get(self, db_type, id_type, media_id):
		result = None
		try:
			current_time = self._get_timestamp(self.time)
			result = self.get_memory_cache(db_type, id_type, media_id, current_time)
			if result is None:
				dbcon = database.connect(self.dbfile, timeout=self.timeout)
				dbcur = self._set_PRAGMAS(dbcon)
				if db_type in ('movie', 'tvshow'):
					dbcur.execute("SELECT meta, expires FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
				else: # season
					dbcur.execute("SELECT meta, expires FROM season_metadata WHERE tmdb_id = ?", (str(media_id),))
				cache_data = dbcur.fetchone()
				if cache_data:
					if cache_data[1] > current_time:
						result = eval(cache_data[0])
						if db_type in ('movie', 'tvshow'): tmdb_id = result['tmdb_id']
						else: tmdb_id = media_id
						self.set_memory_cache(db_type, result, cache_data[1], tmdb_id)
					else:
						self.delete(db_type, id_type, media_id, dbcon=dbcon)
		except: pass
		return result

	def set(self, db_type, meta, expiration=EXPIRES_30_DAYS, tmdb_id=None):
		try:
			expires = self._get_timestamp(self.time + expiration)
			dbcon = database.connect(self.dbfile, timeout=self.timeout)
			dbcur = self._set_PRAGMAS(dbcon)
			if db_type in ('movie', 'tvshow'):
				dbcur.execute("INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)", (str(db_type), str(meta['tmdb_id']), str(meta['imdb_id']), str(meta['tvdb_id']), repr(meta), int(expires)))
			else: # season
				dbcur.execute("INSERT INTO season_metadata VALUES (?, ?, ?)", (str(tmdb_id), repr(meta), int(expires)))
			dbcon.commit()
		except: return None
		self.set_memory_cache(db_type, meta, int(expires), tmdb_id)

	def get_memory_cache(self, db_type, id_type, media_id, current_time):
		result = None
		try:
			if db_type in ('movie', 'tvshow'):
				string = '%s_%s_%s' % (db_type, id_type, media_id)
			else:
				string = 'meta_season_%s' % str(media_id)
			try: cachedata = get_property(string.encode('utf-8'))
			except: cachedata = get_property(string)
			if cachedata:
				cachedata = eval(cachedata)
				if cachedata[0] > current_time:
					result = cachedata[1]
		except: pass
		return result

	def set_memory_cache(self, db_type, meta, expires, tmdb_id):
		try:
			if db_type in ('movie', 'tvshow'):
				string = '%s_%s_%s' % (str(db_type), 'tmdb_id', str(meta['tmdb_id']))
				cachedata = (expires, meta)
			else: # season
				string = 'meta_season_%s' % str(tmdb_id)
				cachedata = (expires, meta)
			try: cachedata_repr = repr(cachedata).encode('utf-8')
			except: cachedata_repr = repr(cachedata)
			set_property(string, cachedata_repr)
		except: pass

	def get_function(self, string):
		result = None
		try:
			current_time = self._get_timestamp(self.time)
			dbcon = database.connect(self.dbfile, timeout=self.timeout)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute("SELECT string_id, data, expires FROM function_cache WHERE string_id = ?", (string,))
			cache_data = dbcur.fetchone()
			if cache_data:
				if cache_data[2] > current_time:
					result = eval(cache_data[1])
				else:
					dbcur.execute("DELETE FROM function_cache WHERE string_id = ?", (string,))
					dbcon.commit()
		except: pass
		return result

	def set_function(self, string, result, expiration=EXPIRES_1_DAY):
		try:
			expires = self._get_timestamp(self.time + expiration)
			dbcon = database.connect(self.dbfile, timeout=self.timeout)
			dbcur = self._set_PRAGMAS(dbcon)
			dbcur.execute("INSERT INTO function_cache VALUES (?, ?, ?)", (string, repr(result), int(expires)))
			dbcon.commit()
		except: return

	def delete(self, db_type, id_type, media_id, dbcon=None, meta_language=None, tvdb_id=None):
		# 'meta_language' and 'tvdb_id' are used when "refreshing" metadata so that the fanart function_cache item is cleaned as well.
		try:
			if not dbcon: dbcon = database.connect(self.dbfile, timeout=self.timeout)
			dbcur = dbcon.cursor()
			fanart_function_string = None
			if db_type  == 'movie':
				dbcur.execute("DELETE FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
				if meta_language:
					fanart_id, fanart_db_type = media_id, 'movies'
			elif db_type == 'tvshow':
				dbcur.execute("DELETE FROM season_metadata WHERE tmdb_id LIKE ?", (str(media_id)+'%',))
				dbcur.execute("DELETE FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
				if meta_language:
					fanart_id, fanart_db_type = tvdb_id, 'tv'
			else:# season
				dbcur.execute("DELETE FROM season_metadata WHERE tmdb_id = ?", (str(media_id),))
			if meta_language:
				dbcur.execute("DELETE FROM function_cache WHERE string_id = ?", ('fanart_%s_%s_%s' % (fanart_db_type, meta_language, str(fanart_id)),))
			self.delete_memory_cache(db_type, id_type, media_id)
			dbcon.commit()
		except: return

	def delete_memory_cache(self, db_type, id_type, media_id):
		try:
			if db_type in ('movie', 'tvshow'):
				string = '%s_%s_%s' % (db_type, id_type, str(media_id))
				clear_property(string)
			else: # season
				string = 'meta_season_%s' % str(media_id)
				clear_property(string)
		except: pass

	def delete_all_seasons_memory_cache(self, media_id):
		for item in range(1,51):
			string = 'meta_season_%s_%s' % (str(media_id), str(item))
			clear_property(string)

	def delete_all(self):
		try:
			dbcon = database.connect(self.dbfile, timeout=self.timeout)
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT db_type, tmdb_id FROM metadata")
			all_entries = dbcur.fetchall()
			for i in ('metadata', 'season_metadata', 'function_cache'): dbcur.execute("DELETE FROM %s" % i)
			dbcon.commit()
			dbcon.execute('VACUUM')
			dbcon.close()
			for i in all_entries:
				try:
					self.delete_memory_cache(str(i[0]), 'tmdb_id', str(i[1]))
					self.delete_all_seasons_memory_cache(str(i[1]))
				except: pass
		except: return

	def _set_PRAGMAS(self, dbcon):
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		return dbcur

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

metacache = MetaCache()

def cache_function(function, string, url, expiration=96, json=True):
	data = metacache.get_function(string)
	if data: return to_utf8(data)
	if json: result = function(url).json()
	else: result = function(url)
	metacache.set_function(string, result, expiration=timedelta(hours=expiration))
	return to_utf8(result)

def delete_meta_cache(silent=False):
	from modules.kodi_utils import confirm_dialog
	try:
		if not silent:
			if not confirm_dialog(): return False
		metacache.delete_all()
		return True
	except:
		return False
