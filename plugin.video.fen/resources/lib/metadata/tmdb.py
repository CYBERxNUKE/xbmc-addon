# -*- coding: utf-8 -*-
from caches.meta_cache import cache_function
from modules.settings import tmdb_api_key
from modules.kodi_utils import make_session
# from modules.kodi_utils import logger

EXPIRY_1_MONTH, EXPIRY_1_YEAR = 30, 365
base_url = 'https://api.themoviedb.org/3'
movies_append = 'external_ids,videos,credits,release_dates,alternative_titles,translations,images'
tvshows_append = 'external_ids,videos,credits,content_ratings,alternative_titles,translations,images'
session = make_session(base_url)
timeout = 20.0

def movie_details(tmdb_id, language, tmdb_api=None):
	try:
		url = '%s/movie/%s?api_key=%s&language=%s&append_to_response=%s' % (base_url, tmdb_id, get_tmdb_api(tmdb_api), language, movies_append)
		return get_tmdb(url).json()
	except: return None

def tvshow_details(tmdb_id, language, tmdb_api=None):
	try:
		url = '%s/tv/%s?api_key=%s&language=%s&append_to_response=%s' % (base_url, tmdb_id, get_tmdb_api(tmdb_api), language, tvshows_append)
		return get_tmdb(url).json()
	except: return None

def movie_set_details(collection_id, tmdb_api=None):
	try:
		url = '%s/collection/%s?api_key=%s&language=en-US' % (base_url, collection_id, get_tmdb_api(tmdb_api))
		return get_tmdb(url).json()
	except: return None

def season_episodes_details(tmdb_id, season_no, language, tmdb_api=None):
	try:
		url = '%s/tv/%s/season/%s?api_key=%s&language=%s&append_to_response=credits' % (base_url, tmdb_id, season_no, get_tmdb_api(tmdb_api), language)
		return get_tmdb(url).json()
	except: return None

def movie_external_id(external_source, external_id, tmdb_api=None):
	try:
		string = 'movie_external_id_%s_%s' % (external_source, external_id)
		url = '%s/find/%s?api_key=%s&external_source=%s' % (base_url, external_id, get_tmdb_api(tmdb_api), external_source)
		result = cache_function(get_tmdb, string, url, EXPIRY_1_MONTH)
		result = result['movie_results']
		if result: return result[0]
		else: return None
	except: return None

def tvshow_external_id(external_source, external_id, tmdb_api=None):
	try:
		string = 'tvshow_external_id_%s_%s' % (external_source, external_id)
		url = '%s/find/%s?api_key=%s&external_source=%s' % (base_url, external_id, get_tmdb_api(tmdb_api), external_source)
		result = cache_function(get_tmdb, string, url, EXPIRY_1_MONTH)
		result = result['tv_results']
		if result: return result[0]
		else: return None
	except: return None

def movie_title_year(title, year, tmdb_api=None):
	try:
		string = 'movie_title_year_%s_%s' % (title, year)
		url = '%s/search/movie?api_key=%s&query=%s&year=%s&page=%s' % (base_url, get_tmdb_api(tmdb_api), title, year)
		result = cache_function(string, url, EXPIRY_1_MONTH)
		result = result['results']
		if result: return result[0]
		else: return None
	except: return None

def tvshow_title_year(title, year, tmdb_api=None):
	try:
		string = 'tvshow_title_year_%s_%s' % (title, year)
		url = '%s/search/tv?api_key=%s&query=%s&first_air_date_year=%s' % (base_url, get_tmdb_api(tmdb_api), title, year)
		result = cache_function(get_tmdb, string, url, EXPIRY_1_MONTH)
		result = result['results']
		if result: return result[0]
		else: return None
	except: return None

def english_translation(media_type, tmdb_id, tmdb_api=None):
	try:
		string = 'english_translation_%s_%s' % (media_type, tmdb_id)
		url = '%s/%s/%s/translations?api_key=%s' % (base_url, media_type, tmdb_id, get_tmdb_api(tmdb_api))
		result = cache_function(get_tmdb, string, url, EXPIRY_1_YEAR)['']
		try: result = result['translations']
		except: result = None
		return result
	except: return None

def get_tmdb(url):
	response = None
	try: response = session.get(url, timeout=timeout)
	except: response = session.get(url, verify=False, timeout=timeout)
	return response
	

def get_tmdb_api(tmdb_api=None):
	return tmdb_api or tmdb_api_key()

