# -*- coding: utf-8 -*-
import requests
from caches.meta_cache import cache_function
from modules.settings import tmdb_api_key
# from modules.kodi_utils import logger

EXPIRY_1_MONTH, EXPIRY_1_YEAR = 672, 8760
movies_append = 'external_ids,videos,credits,release_dates,alternative_titles,translations'
tvshows_append = 'external_ids,videos,credits,content_ratings,alternative_titles,translations'

def tmdbMovies(tmdb_id, language, tmdb_api=None):
	try:
		url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=%s' % (tmdb_id, getTmdbAPI(tmdb_api), language, movies_append)
		return getTmdb(url).json()
	except: return None

def tmdbMoviesExternalID(external_source, external_id, tmdb_api=None):
	try:
		string = 'tmdbMoviesExternalID_%s_%s' % (external_source, external_id)
		url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=%s' % (external_id, getTmdbAPI(tmdb_api), external_source)
		return cache_function(getTmdb, string, url, EXPIRY_1_MONTH)['movie_results'][0]
	except: return None

def tmdbMoviesTitleYear(title, year, tmdb_api=None):
	try:
		string = 'tmdbMoviesTitleYear_%s_%s' % (title, year)
		url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&query=%s&year=%s&page=%s' % (getTmdbAPI(tmdb_api), title, year)
		return cache_function(string, url, EXPIRY_1_MONTH)['results'][0]
	except: return None

def tmdbTVShows(tmdb_id, language, tmdb_api=None):
	try:
		url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=%s&append_to_response=%s' % (tmdb_id, getTmdbAPI(tmdb_api), language, tvshows_append)
		return getTmdb(url).json()
	except: return None

def tmdbTVShowsExternalID(external_source, external_id, tmdb_api=None):
	try:
		string = 'tmdbTVShowsExternalID_%s_%s' % (external_source, external_id)
		url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=%s' % (external_id, getTmdbAPI(tmdb_api), external_source)
		return cache_function(getTmdb, string, url, EXPIRY_1_MONTH)['tv_results'][0]
	except: return None

def tmdbTVShowsTitleYear(title, year, tmdb_api=None):
	try:
		string = 'tmdbTVShowsTitleYear_%s_%s' % (title, year)
		url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&first_air_date_year=%s' % (getTmdbAPI(tmdb_api), title, year)
		return cache_function(getTmdb, string, url, EXPIRY_1_MONTH)['results'][0]
	except: return None

def tmdbSeasonEpisodes(tmdb_id, season_no, language, tmdb_api=None):
	try:
		url = 'https://api.themoviedb.org/3/tv/%s/season/%s?api_key=%s&language=%s&append_to_response=credits' % (tmdb_id, season_no, getTmdbAPI(tmdb_api), language)
		return getTmdb(url).json()
	except: return None

def tmdbEnglishTranslation(db_type, tmdb_id, tmdb_api=None):
	try:
		string = 'tmdbEnglishTranslation_%s_%s' % (db_type, tmdb_id)
		url = 'https://api.themoviedb.org/3/%s/%s/translations?api_key=%s' % (db_type, tmdb_id, getTmdbAPI(tmdb_api))
		return cache_function(getTmdb, string, url, EXPIRY_1_YEAR)['translations']
	except: return None

def getTmdb(url):
	try: response = requests.get(url, timeout=20.0)
	except: response = requests.get(url, verify=False)
	return response

def getTmdbAPI(tmdb_api):
	return tmdb_api or tmdb_api_key()

