# -*- coding: utf-8 -*-
import sqlite3 as database
from modules.kodi_utils import translate_path
from modules.utils import to_utf8
# from modules.kodi_utils import logger

dbfile = translate_path('special://profile/addon_data/plugin.video.fen/imagehash.db')
timeout = 240

GET_IMAGE = 'SELECT hash, brightness FROM imagehash_data WHERE image = ?'
SET_IMAGE = 'INSERT OR REPLACE INTO imagehash_data VALUES (?, ?, ?)'

class ImagehashCache():
	def get(self, image_path):
		result = None
		try:
			dbcon = self.connect_database()
			dbcur = self.set_PRAGMAS(dbcon)
			dbcur.execute(GET_IMAGE, (image_path,))
			cache_data = dbcur.fetchone()
			if cache_data: result = cache_data
		except: pass
		return result

	def set(self, image_path, data):
		try:
			dbcon = self.connect_database()
			dbcur = self.set_PRAGMAS(dbcon)
			dbcur.execute(SET_IMAGE, (image_path, data[0], data[1]))
			dbcon.commit()
		except: return None

	def connect_database(self):
		return database.connect(dbfile, timeout=timeout)

	def set_PRAGMAS(self, dbcon):
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		return dbcur

_cache = ImagehashCache()

def cache_imagehash_object(function, image_path):
	cache = _cache.get(image_path)
	if cache: return to_utf8(cache)
	result = function(image_path)
	_cache.set(image_path, result)
	return to_utf8(result)