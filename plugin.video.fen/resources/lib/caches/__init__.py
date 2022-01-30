# -*- coding: utf-8 -*-
from threading import Thread
import sqlite3 as database
from modules.kodi_utils import translate_path, notification, path_exists, make_directorys
from modules.utils import make_thread_list
# from modules.kodi_utils import logger

navigator_db = translate_path('special://profile/addon_data/plugin.video.fen/navigator.db')
watched_db = translate_path('special://profile/addon_data/plugin.video.fen/watched_status.db')
favorites_db = translate_path('special://profile/addon_data/plugin.video.fen/favourites.db')
views_db = translate_path('special://profile/addon_data/plugin.video.fen/views.db')
trakt_db = translate_path('special://profile/addon_data/plugin.video.fen/traktcache2.db')
maincache_db = translate_path('special://profile/addon_data/plugin.video.fen/maincache.db')
metacache_db = translate_path('special://profile/addon_data/plugin.video.fen/metacache3.db')
debridcache_db = translate_path('special://profile/addon_data/plugin.video.fen/debridcache.db')
imagehash_db = translate_path('special://profile/addon_data/plugin.video.fen/imagehash.db')
external_db = translate_path('special://profile/addon_data/plugin.video.fen/providerscache.db')

def check_databases():
	data_path = translate_path('special://profile/addon_data/plugin.video.fen/')
	if not path_exists(data_path): make_directorys(data_path)
	# Navigator
	dbcon = database.connect(navigator_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS navigator (list_name text, list_type text, list_contents text)""")
	dbcon.close()
	# Watched Status
	dbcon = database.connect(watched_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS progress
				(db_type text, media_id text, season integer, episode integer, resume_point text, curr_time text, unique(db_type, media_id, season, episode))""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS watched_status
				(db_type text, media_id text, season integer, episode integer, last_played text, title text, unique(db_type, media_id, season, episode))""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS exclude_from_next_episode (media_id text, title text)""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS unwatched_next_episode (media_id text)""")
	dbcon.close()
	# Favourites
	dbcon = database.connect(favorites_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS favourites (db_type text, tmdb_id text, title text, unique (db_type, tmdb_id))""")
	dbcon.close()
	# Views
	dbcon = database.connect(views_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS views (view_type text, view_id text, unique (view_type))""")
	dbcon.close()
	# Trakt
	dbcon = database.connect(trakt_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS trakt_data (id text unique, data text)""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS watched_status
					(db_type text, media_id text, season integer, episode integer, last_played text, title text, unique(db_type, media_id, season, episode))""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS progress
					(db_type text, media_id text, season integer, episode integer, resume_point text, curr_time text, unique(db_type, media_id, season, episode))""")
	dbcon.close()
	# Main Cache
	dbcon = database.connect(maincache_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS maincache (id text unique, data text, expires integer)""")
	dbcon.close()
	# Meta Cache
	dbcon = database.connect(metacache_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS metadata
					  (db_type text not null, tmdb_id text not null, imdb_id text, tvdb_id text, meta text, expires integer, unique (db_type, tmdb_id))""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS season_metadata (tmdb_id text not null unique, meta text, expires integer)""")
	dbcon.execute("""CREATE TABLE IF NOT EXISTS function_cache (string_id text not null, data text, expires integer)""")
	dbcon.close()
	# Debrid Cache
	dbcon = database.connect(debridcache_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS debrid_data (hash text not null, debrid text not null, cached text, expires integer, unique (hash, debrid))""")
	dbcon.close()
	# Image Hash Cache
	dbcon = database.connect(imagehash_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS imagehash_data (image text not null, hash text not null, brightness bool not null, unique (image, hash, brightness))""")
	dbcon.close()
	# External Providers Cache
	dbcon = database.connect(external_db)
	dbcon.execute("""CREATE TABLE IF NOT EXISTS results_data
	(provider text, db_type text, tmdb_id text, title text, year integer, season text, episode text, results text,
	expires integer, unique (provider, db_type, tmdb_id, title, year, season, episode))""")
	dbcon.close()

def clean_databases(current_time=None, database_check=True, silent=False):
	def _process(args):
		try:
			dbcon = database.connect(args[0], timeout=60.0)
			dbcur = dbcon.cursor()
			dbcur.execute('''PRAGMA synchronous = OFF''')
			dbcur.execute('''PRAGMA journal_mode = OFF''')
			dbcur.execute(args[1], (current_time,))
			dbcon.commit()
			dbcur.execute('VACUUM')
			dbcon.close()
		except: pass
	if database_check: check_databases()
	if not current_time: current_time = get_current_time()
	command_base = 'DELETE from %s WHERE CAST(%s AS INT) <= ?'
	functions_list = []
	functions_list_append = functions_list.append
	functions_list_append((external_db, command_base % ('results_data', 'expires')))
	functions_list_append((maincache_db, command_base % ('maincache', 'expires')))
	functions_list_append((metacache_db, command_base % ('metadata', 'expires')))
	functions_list_append((metacache_db, command_base % ('function_cache', 'expires')))
	functions_list_append((metacache_db, command_base % ('season_metadata', 'expires')))
	functions_list_append((debridcache_db, command_base % ('debrid_data', 'expires')))
	threads = list(make_thread_list(_process, functions_list, Thread))
	[i.join() for i in threads]
	if not silent: notification(32576, time=2000)

def get_current_time():
	import time
	import datetime
	return int(time.mktime(datetime.datetime.now().timetuple()))