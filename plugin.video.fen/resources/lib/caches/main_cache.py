# -*- coding: utf-8 -*-
from datetime import timedelta
from modules.kodi_utils import translate_path
from modules.utils import to_utf8
from caches.base_cache import BaseCache
# from modules.kodi_utils import logger

dbfile = translate_path('special://profile/addon_data/plugin.video.fen/maincache.db')

like_select = 'SELECT id from maincache where id LIKE %s'
like_delete = 'DELETE FROM maincache WHERE id LIKE %s'
delete = 'DELETE FROM maincache WHERE id=?'
all_list_add = ' OR id LIKE '

class MainCache(BaseCache):
	def __init__(self):
		BaseCache.__init__(self, dbfile, 'maincache')

	def delete_all_lists(self):
		from modules.meta_lists import media_lists
		media_list = media_lists
		dbcon = self.connect_database()
		dbcur = self.set_PRAGMAS(dbcon)
		len_media_list = len(media_list)
		for count, item in enumerate(media_list, 1):
			if count == 1: command = like_select % item
			else: command += '%s%s' % (all_list_add, item)
		dbcur.execute(command)
		results = dbcur.fetchall()
		try:
			for item in results:
				try:
					dbcur.execute(delete, (str(item[0]),))
					self.delete_memory_cache(str(item[0]))
				except: pass
			dbcon.commit()
			dbcon.execute('VACUUM')
			dbcon.close()
		except: pass

	def delete_all_folderscrapers(self):
		dbcon = self.connect_database()
		dbcur = self.set_PRAGMAS(dbcon)
		dbcur.execute(like_select % "'fen_FOLDERSCRAPER_%'")
		remove_list = [str(i[0]) for i in dbcur.fetchall()]
		if not remove_list: return 'success'
		try:
			dbcur.execute(like_delete % "'fen_FOLDERSCRAPER_%'")
			dbcon.commit()
			dbcon.execute('VACUUM')
			dbcon.close()
			for item in remove_list: self.delete_memory_cache(str(item))
		except: pass

main_cache = MainCache()

def cache_object(function, string, url, json=True, expiration=24):
	cache = main_cache.get(string)
	if cache: return to_utf8(cache)
	if isinstance(url, list): args = tuple(url)
	else: args = (url,)
	if json: result = function(*args).json()
	else: result = function(*args)
	main_cache.set(string, result, expiration=timedelta(hours=expiration))
	return to_utf8(result)
