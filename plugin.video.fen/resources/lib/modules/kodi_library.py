# -*- coding: utf-8 -*-
import json
from metadata import movie_meta, tvshow_meta, retrieve_user_info
from modules.kodi_utils import sleep, progressDialogBG, execute_JSON, local_string as ls
from modules.utils import clean_file_name, to_utf8
# from modules.kodi_utils import logger

def get_library_video(db_type, title, year, season=None, episode=None):
	try:
		years = (year, str(int(year)+1), str(int(year)-1))
		if db_type == 'movie':
			r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title", "originaltitle", "file"]}, "id": 1}' % years)
			r = to_utf8(r)
			r = json.loads(r)['result']['movies']
			try:
				r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()]
			except:
				return None
			r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["streamdetails", "file"], "movieid": %s }, "id": 1}' % str(r['movieid']))
			r = to_utf8(r)
			r = json.loads(r)['result']['moviedetails']
		elif db_type  == 'tvshow':
			r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title", "year"]}, "id": 1}' % years)
			r = to_utf8(r)
			r = json.loads(r)['result']['tvshows']
			try:
				r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
				return r
			except:
				return None
	except: pass

def set_bookmark_kodi_library(db_type, tmdb_id, curr_time, total_time, season='', episode=''):
	meta_user_info = retrieve_user_info()
	try:
		info = movie_meta('tmdb_id', tmdb_id, meta_user_info) if db_type == 'movie' else tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
		title = info['title']
		year = info['year']
		years = (str(year), str(int(year)+1), str(int(year)-1))
		if db_type == 'movie': r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
		else: r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
		r = to_utf8(r)
		r = json.loads(r)['result']['movies'] if db_type == 'movie' else json.loads(r)['result']['tvshows']
		if db_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()][0]
		else: r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
		if db_type == 'episode':
			r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
			r = to_utf8(r)
			r = json.loads(r)['result']['episodes'][0]
		(method, id_name, library_id) = ('SetMovieDetails', 'movieid', r['movieid']) if db_type == 'movie' else ('SetEpisodeDetails', 'episodeid', r['episodeid'])
		query = {"jsonrpc": "2.0", "id": "setResumePoint", "method": "VideoLibrary."+method, "params": {id_name: library_id, "resume": {"position": curr_time, "total": total_time}}}
		execute_JSON(json.dumps(query))
	except: pass
	
def get_bookmark_kodi_library(db_type, tmdb_id, season='', episode=''):
	resume = '0'
	meta_user_info = retrieve_user_info()
	try:
		info = movie_meta('tmdb_id', tmdb_id, meta_user_info) if db_type == 'movie' else tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
		title = info['title']
		year = info['year']
		years = (str(year), str(int(year)+1), str(int(year)-1))
		if db_type == 'movie': r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title", "resume"]}, "id": 1}' % years)
		else: r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
		r = to_utf8(r)
		r = json.loads(r)['result']['movies'] if db_type == 'movie' else json.loads(r)['result']['tvshows']
		if db_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()][0]
		else: r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
		if db_type == 'episode':
			r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
			r = to_utf8(r)
			r = json.loads(r)['result']['episodes'][0]
		(method, id_name, library_id, results_key) = ('GetMovieDetails', 'movieid', r['movieid'], 'moviedetails') if db_type == 'movie' else ('GetEpisodeDetails', 'episodeid', r['episodeid'], 'episodedetails')
		query = {"jsonrpc": "2.0", "id": "getResumePoint", "method": "VideoLibrary."+method, "params": {id_name: library_id, "properties": ["title", "resume"]}}
		r = to_utf8(json.loads(execute_JSON(json.dumps(query))))
		resume = r["result"][results_key]["resume"]["position"]
		return resume
	except: pass

def mark_as_watched_unwatched_kodi_library(db_type, action, title, year, season=None, episode=None):
	try:
		playcount = 1 if action == 'mark_as_watched' else 0
		years = (str(year), str(int(year)+1), str(int(year)-1))
		if db_type == 'movie': r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
		else: r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
		r = to_utf8(r)
		r = json.loads(r)['result']['movies'] if db_type == 'movie' else json.loads(r)['result']['tvshows']
		if db_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()][0]
		else: r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
		if db_type == 'episode':
			r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
			r = to_utf8(r)
			r = json.loads(r)['result']['episodes'][0]
		(method, id_name, library_id) = ('SetMovieDetails', 'movieid', r['movieid']) if db_type == 'movie' else ('SetEpisodeDetails', 'episodeid', r['episodeid'])
		query = {"jsonrpc": "2.0", "method": "VideoLibrary."+method, "params": {id_name : library_id, "playcount" : playcount }, "id": 1 }
		execute_JSON(json.dumps(query))
		query = {"jsonrpc": "2.0", "id": "setResumePoint", "method": "VideoLibrary."+method, "params": {id_name: library_id, "resume": {"position": 0,}}}
		execute_JSON(json.dumps(query))
	except: pass

def batch_mark_episodes_as_watched_unwatched_kodi_library(action, show_info, episode_list):
	playcount = 1 if action == 'mark_as_watched' else 0
	tvshowid = str(show_info['tvshowid'])
	ep_ids = []
	action_list = []
	ep_ids_append = ep_ids.append
	action_append = action_list.append
	progressDialogBG.create(ls(32577), '')
	try:
		for item in episode_list:
			try:
				season = item[2]
				episode = item[3]
				r = execute_JSON('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file", "playcount"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(tvshowid)))
				r = to_utf8(r)
				r = json.loads(r)['result']['episodes'][0]
				ep_ids_append((r['episodeid'], r['playcount']))
			except: pass
		for count, item in enumerate(ep_ids, 1):
			try:
				ep_id = item[0]
				current_playcount = item[1]
				if int(current_playcount) != playcount:
					sleep(50)
					display = ls(32856)
					progressDialogBG.update(int(float(count) / float(len(ep_ids)) * 100), ls(32577), display)
					t = '{"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid" : %d, "playcount" : %d }, "id": 1 }' % (int(ep_id) ,playcount)
					t = json.loads(t)
					action_append(t)
				else: pass
			except: pass
		progressDialogBG.update(100, ls(32577), ls(32788))
		r = execute_JSON(json.dumps(action_list))
		progressDialogBG.close()
		return r
	except: pass

		