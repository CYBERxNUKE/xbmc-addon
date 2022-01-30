# -*- coding: utf-8 -*-
import requests
from caches.main_cache import cache_object
from modules.settings import tmdb_api_key
# from modules.kodi_utils import logger

EXPIRY_4_HOURS, EXPIRY_2_DAYS, EXPIRY_1_WEEK, EXPIRY_1_MONTH = 4, 48, 168, 672

def tmdb_keyword_id(query):
	string = 'tmdb_keyword_id_%s' % query
	url = 'https://api.themoviedb.org/3/search/keyword?api_key=%s&query=%s' % (tmdb_api_key(), query)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_WEEK)

def tmdb_company_id(query):
	string = 'tmdb_company_id_%s' % query
	url = 'https://api.themoviedb.org/3/search/company?api_key=%s&query=%s' % (tmdb_api_key(), query)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_WEEK)

def tmdb_media_images(db_type, tmdb_id):
	if db_type == 'movies': db_type = 'movie'
	string = 'tmdb_media_images_%s_%s' % (db_type, tmdb_id)
	url = 'https://api.themoviedb.org/3/%s/%s/images?api_key=%s' % (db_type, tmdb_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_WEEK)

def tmdb_media_videos(db_type, tmdb_id):
	if db_type == 'movies': db_type = 'movie'
	if db_type in ('tvshow', 'tvshows'): db_type = 'tv'
	string = 'tmdb_media_videos_%s_%s' % (db_type, tmdb_id)
	url = 'https://api.themoviedb.org/3/%s/%s/videos?api_key=%s' % (db_type, tmdb_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_WEEK)

def tmdb_movies_discover(query, page_no):
	string = query % page_no
	url = query % page_no
	return cache_object(get_tmdb, string, url)

def tmdb_movies_collection(collection_id):
	string = 'tmdb_movies_collection_%s' % collection_id
	url = 'https://api.themoviedb.org/3/collection/%s?api_key=%s&language=en-US' % (collection_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_WEEK)

def tmdb_movies_title_year(title, year=None):
	if year:
		string = 'tmdb_movies_title_year_%s_%s' % (title, year)
		url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&year=%s' % (tmdb_api_key(), title, year)
	else:
		string = 'tmdb_movies_title_year_%s' % title
		url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s' % (tmdb_api_key(), title)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_MONTH)

def tmdb_movies_popular(page_no):
	string = 'tmdb_movies_popular_%s' % page_no
	url = 'https://api.themoviedb.org/3/movie/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_blockbusters(page_no):
	string = 'tmdb_movies_blockbusters_%s' % page_no
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=revenue.desc&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_in_theaters(page_no):
	string = 'tmdb_movies_in_theaters_%s' % page_no
	url = 'https://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_premieres(page_no):
	current_date, previous_date = get_dates(31, reverse=True)
	string = 'tmdb_movies_premieres_%s' % page_no
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=1|3|2&page=%s' \
																											% (tmdb_api_key(), previous_date, current_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_latest_releases(page_no):
	current_date, previous_date = get_dates(31, reverse=True)
	string = 'tmdb_movies_latest_releases_%s' % page_no
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=4|5&page=%s' \
																											% (tmdb_api_key(), previous_date, current_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_top_rated(page_no):
	string = 'tmdb_movies_top_rated_%s' % page_no
	url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_upcoming(page_no):
	current_date, future_date = get_dates(31, reverse=False)
	string = 'tmdb_movies_upcoming_%s' % page_no
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=3|2|1&page=%s' \
																											% (tmdb_api_key(), current_date, future_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_genres(genre_id, page_no):
	string = 'tmdb_movies_genres_%s_%s' % (genre_id, page_no)
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&with_genres=%s&sort_by=popularity.desc&page=%s' % (tmdb_api_key(), genre_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_genres_by_year(genre_id, year, page_no):
	string = 'tmdb_movies_genres_by_year_%s_%s_%s' % (genre_id, year, page_no)
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&with_genres=%s&sort_by=popularity.desc&primary_release_year=%s&page=%s' % (tmdb_api_key(), genre_id, year, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_languages(language, page_no):
	string = 'tmdb_movies_languages_%s_%s' % (language, page_no)
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&with_original_language=%s&page=%s' % (tmdb_api_key(), language, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_certifications(certification, page_no):
	string = 'tmdb_movies_certifications_%s_%s' % (certification, page_no)
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&certification=%s&page=%s' \
																													% (tmdb_api_key(), certification, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_year(year, page_no):
	string = 'tmdb_movies_year_%s_%s' % (year, page_no)
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&primary_release_year=%s&page=%s' \
																																% (tmdb_api_key(), year, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_networks(network_id, page_no):
	string = 'tmdb_movies_networks_%s_%s' % (network_id, page_no)
	url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&with_companies=%s&page=%s' \
																														% (tmdb_api_key(), network_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_similar(tmdb_id, page_no):
	string = 'tmdb_movies_similar_%s_%s' % (tmdb_id, page_no)
	url = 'https://api.themoviedb.org/3/movie/%s/similar?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_recommendations(tmdb_id, page_no):
	string = 'tmdb_movies_recommendations_%s_%s' % (tmdb_id, page_no)
	url = 'https://api.themoviedb.org/3/movie/%s/recommendations?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_movies_search(query, page_no):
	from modules.history import add_to_search_history
	add_to_search_history(query, 'movie_queries')
	string = 'tmdb_movies_search_%s_%s' % (query, page_no)
	url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api_key(), query, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_4_HOURS)

def tmdb_movies_reviews(tmdb_id):
	string = 'tmdb_movies_reviews_%s' % tmdb_id
	url = 'https://api.themoviedb.org/3/movie/%s/reviews?api_key=%s' % (tmdb_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_4_HOURS)

def tmdb_tv_discover(query, page_no):
	string = query % page_no
	url = query % page_no
	return cache_object(get_tmdb, string, url)

def tmdb_tv_title_year(title, year=None):
	if year:
		string = 'tmdb_tv_title_year_%s_%s' % (title, year)
		url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&first_air_date_year=%s&language=en-US' % (tmdb_api_key(), title, year)
	else:
		string = 'tmdb_tv_title_year_%s' % title
		url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&language=en-US' % (tmdb_api_key(), title)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_MONTH)

def tmdb_tv_popular(page_no):
	string = 'tmdb_tv_popular_%s' % page_no
	url = 'https://api.themoviedb.org/3/tv/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_premieres(page_no):
	current_date, previous_date = get_dates(31, reverse=True)
	string = 'tmdb_tv_premieres_%s' % page_no
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' \
																									% (tmdb_api_key(), previous_date, current_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_upcoming(page_no):
	current_date, future_date = get_dates(31, reverse=False)
	string = 'tmdb_tv_upcoming_%s' % page_no
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' \
																									% (tmdb_api_key(), current_date, future_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_top_rated(page_no):
	string = 'tmdb_tv_top_rated_%s' % page_no
	url = 'https://api.themoviedb.org/3/tv/top_rated?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_airing_today(page_no):
	string = 'tmdb_tv_airing_today_%s' % page_no
	url = 'https://api.themoviedb.org/3/tv/airing_today?api_key=%s&timezone=America/Edmonton&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_on_the_air(page_no):
	string = 'tmdb_tv_on_the_air_%s' % page_no
	url = 'https://api.themoviedb.org/3/tv/on_the_air?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_genres(genre_id, page_no):
	string = 'tmdb_tv_genres_%s_%s' % (genre_id, page_no)
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&sort_by=popularity.desc&include_null_first_air_dates=false&page=%s' \
																											% (tmdb_api_key(), genre_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_genres_by_year(genre_id, year, page_no):
	string = 'tmdb_tv_genres_by_year_%s_%s_%s' % (genre_id, year, page_no)
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&first_air_date_year=%s&sort_by=popularity.desc&include_null_first_air_dates=false&page=%s' \
																															% (tmdb_api_key(), genre_id, year, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_languages(language, page_no):
	string = 'tmdb_tv_languages_%s_%s' % (language, page_no)
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language=%s&page=%s' \
																																		% (tmdb_api_key(), language, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_year(year, page_no):
	string = 'tmdb_tv_year_%s_%s' % (year, page_no)
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&first_air_date_year=%s&page=%s' \
																																		% (tmdb_api_key(), year, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_networks(network_id, page_no):
	string = 'tmdb_tv_networks_%s_%s' % (network_id, page_no)
	url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&with_networks=%s&page=%s' \
																															% (tmdb_api_key(), network_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_similar(tmdb_id, page_no):
	string = 'tmdb_tv_similar_%s_%s' % (tmdb_id, page_no)
	url = 'https://api.themoviedb.org/3/tv/%s/similar?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_recommendations(tmdb_id, page_no):
	string = 'tmdb_tv_recommendations_%s_%s' % (tmdb_id, page_no)
	url = 'https://api.themoviedb.org/3/tv/%s/recommendations?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_2_DAYS)

def tmdb_tv_search(query, page_no):
	from modules.history import add_to_search_history
	add_to_search_history(query, 'tvshow_queries')
	string = 'tmdb_tv_search_%s_%s' % (query, page_no)
	url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api_key(), query, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_4_HOURS)

def tmdb_popular_people(page_no):
	string = 'tmdb_popular_people_%s' % page_no
	url = 'https://api.themoviedb.org/3/person/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url)

def tmdb_people_full_info(actor_id, language=None):
	if not language:
		from modules.settings import get_language
		language = get_language()
	string = 'tmdb_people_full_info_%s_%s' % (actor_id, language)
	url = 'https://api.themoviedb.org/3/person/%s?api_key=%s&language=%s&append_to_response=external_ids,combined_credits,images,tagged_images' % (actor_id, tmdb_api_key(), language)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_1_WEEK)

def tmdb_people_info(query):
	string = 'tmdb_people_info_%s' % query
	url = 'https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s' % (tmdb_api_key(), query)
	return cache_object(get_tmdb, string, url, expiration=EXPIRY_4_HOURS)['results']

def get_dates(days, reverse=True):
	import datetime
	current_date = datetime.date.today()
	if reverse: new_date = (current_date - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
	else: new_date = (current_date + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
	return str(current_date), new_date

def get_tmdb(url):
	try: response = requests.get(url, timeout=20.0)
	except: response = requests.get(url, verify=False)
	return response
