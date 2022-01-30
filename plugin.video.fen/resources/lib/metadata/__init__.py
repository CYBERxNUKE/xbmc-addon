# -*- coding: utf-8 -*-

from datetime import timedelta
from threading import Thread
from metadata import tmdb
from metadata import fanarttv
from caches.meta_cache import metacache
from modules.kodi_utils import translate_path
from modules.utils import try_parse_int, safe_string, remove_accents, to_utf8
from modules.settings import user_info
# from modules.kodi_utils import logger

movie_data = tmdb.tmdbMovies
movie_external = tmdb.tmdbMoviesExternalID
tvshow_data = tmdb.tmdbTVShows
tvshow_external = tmdb.tmdbTVShowsExternalID
backup_resolutions = {'poster': 'w780', 'fanart': 'w1280', 'still': 'original', 'profile': 'h632'}
writer_credits = ('Author', 'Writer', 'Screenplay', 'Characters')
alt_titles_test = ('US', 'GB', 'UK', '')
trailers_test = ('Trailer', 'Teaser')
finished_show_check = ('ended', 'canceled')

EXPIRES_2_DAYS = timedelta(days=2)
EXPIRES_4_DAYS = timedelta(days=4)
EXPIRES_182_DAYS = timedelta(days=182)

def movie_meta(id_type, media_id, user_info):
	def no_data():
		if id_type == 'tmdb_id': meta = {'tmdb_id': media_id, 'imdb_id': 'tt0000000', 'tvdb_id': '0000000'}
		else: meta = {'tmdb_id': '0000000', 'imdb_id': media_id, 'tvdb_id': '0000000'}
		metacache.set('movie', meta, EXPIRES_2_DAYS)
		return meta
	def tmdb_meta(language):
		return movie_data(media_id, language, tmdb_api) if id_type == 'tmdb_id' else movie_data(movie_external(id_type, media_id, tmdb_api)['id'], language, tmdb_api)
	def fanarttv_meta(fanart_id):
		return fanarttv.get('movies', language, fanart_id, fanart_client_key)
	def cached_meta():
		return metacache.get('movie', id_type, media_id)
	def set_cache_meta():
		metacache.set('movie', meta, EXPIRES_182_DAYS)
	def delete_cache_meta():
		metacache.delete('movie', 'tmdb_id', meta['tmdb_id'])
	def check_tmdb_data(data):
		if language != 'en':
			if data['overview'] in ('', None, 'None'):
				all_trailers, trailer = [], ''
				eng_data = tmdb_meta('en')
				eng_overview = eng_data['overview']
				data['overview'] = eng_overview
				if 'videos' in data:
					all_trailers = data['videos']['results']
					if all_trailers:
						try: trailer_test = [i for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test]
						except: trailer_test = False
					else: trailer_test = False
				else: trailer_test = False
				if not trailer_test:
					if 'videos' in eng_data:
						eng_all_trailers = eng_data['videos']['results']
						if eng_all_trailers:
							data['videos']['results'] = eng_all_trailers
		return data
	if media_id == None: return {}
	meta = None
	tmdb_api = user_info['tmdb_api']
	image_resolution = user_info.get('image_resolution', backup_resolutions)
	language = user_info['language']
	extra_fanart_enabled = user_info['extra_fanart_enabled']
	fanart_client_key = user_info['fanart_client_key']
	meta = cached_meta()
	if meta:
		if extra_fanart_enabled and not meta.get('fanart_added', False):
			try:
				meta = fanarttv.add('movies', language, meta['tmdb_id'], meta, fanart_client_key)
				delete_cache_meta()
				set_cache_meta()
			except: pass
	else:
		try:
			data = check_tmdb_data(tmdb_meta(language))
			if not data: return no_data()
			if extra_fanart_enabled:
				fanarttv_data = fanarttv_meta(data['id'])
				data['external_poster'] = fanarttv_data.get('fanarttv_poster', None)
				data['external_fanart'] = fanarttv_data.get('fanarttv_fanart', None)
			else: fanarttv_data = None
			data['image_resolution'] = image_resolution
			meta = build_movie_meta(data, fanarttv_data=fanarttv_data)
			set_cache_meta()
		except: pass
	return meta

def tvshow_meta(id_type, media_id, user_info):
	def no_data():
		if id_type == 'tmdb_id': meta = {'tmdb_id': media_id, 'imdb_id': 'tt0000000', 'tvdb_id': '0000000'}
		else: meta = {'tmdb_id': '0000000', 'imdb_id': media_id, 'tvdb_id': '0000000'}
		metacache.set('tvshow', meta, EXPIRES_2_DAYS)
		return meta
	def tmdb_meta(language):
		return tvshow_data(media_id, language, tmdb_api) if id_type == 'tmdb_id' else tvshow_data(tvshow_external(id_type, media_id, tmdb_api)['id'], language, tmdb_api)
	def fanarttv_meta(fanart_id):
		return fanarttv.get('tv', language, fanart_id, fanart_client_key)
	def cached_meta():
		return metacache.get('tvshow', id_type, media_id)
	def set_cache_meta(status):
		if status in finished_show_check: time_delta = EXPIRES_182_DAYS
		else: time_delta = EXPIRES_4_DAYS
		metacache.set('tvshow', meta, time_delta)
	def delete_cache_meta():
		metacache.delete('tvshow', 'tmdb_id', meta['tmdb_id'])
	def check_tmdb_data(data):
		if language != 'en':
			if data['overview'] in ('', None, 'None'):
				eng_data = tmdb_meta('en')
				eng_overview = eng_data['overview']
				data['overview'] = eng_overview
				if 'videos' in data:
					all_trailers = data['videos']['results']
					if all_trailers:
						try: trailer_test = [i for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test]
						except: trailer_test = False
					else: trailer_test = False
				else: trailer_test = False
				if not trailer_test:
					if 'videos' in eng_data:
						eng_all_trailers = eng_data['videos']['results']
						if eng_all_trailers:
							data['videos']['results'] = eng_all_trailers
		return data
	if media_id == None: return {}
	meta = None
	tmdb_api = user_info['tmdb_api']
	image_resolution = user_info.get('image_resolution', backup_resolutions)
	language = user_info['language']
	extra_fanart_enabled = user_info['extra_fanart_enabled']
	fanart_client_key = user_info['fanart_client_key']
	meta = cached_meta()
	if meta:
		if extra_fanart_enabled and not meta.get('fanart_added', False):
			try:
				meta = fanarttv.add('tv', language, meta['tvdb_id'], meta, fanart_client_key)
				delete_cache_meta()
				set_cache_meta(meta['status'].lower())
			except: pass
	else:
		try:
			data = check_tmdb_data(tmdb_meta(language))
			if not data: return no_data()
			data['image_resolution'] = image_resolution
			tvdb_id = data['external_ids']['tvdb_id']
			if extra_fanart_enabled:
				fanarttv_data = fanarttv_meta(tvdb_id)
				if not data['poster_path']:
					if fanarttv_data:
						if fanarttv_data['fanarttv_poster'] != '': data['external_poster'] = fanarttv_data['fanarttv_poster']
				if not data['backdrop_path']:
					if fanarttv_data:
						if fanarttv_data['fanarttv_fanart'] != '': data['external_fanart'] = fanarttv_data['fanarttv_fanart']
			else: fanarttv_data = None
			meta = build_tvshow_meta(data, fanarttv_data=fanarttv_data)
			set_cache_meta(meta['status'].lower())
		except: pass
	return meta

def season_episodes_meta(season, meta, user_info):
	data = None
	media_id = meta['tmdb_id']
	string = '%s_%s' % (media_id, season)
	data = metacache.get('season', 'tmdb_id', string)
	if data: return data
	try:
		if meta['status'].lower() in finished_show_check: time_delta = EXPIRES_182_DAYS
		elif meta['total_seasons'] > int(season): time_delta = EXPIRES_182_DAYS
		else: time_delta = EXPIRES_4_DAYS
		image_resolution = user_info.get('image_resolution', backup_resolutions)
		data = tmdb.tmdbSeasonEpisodes(media_id, season, user_info['language'], user_info['tmdb_api'])['episodes']
		data = build_episodes_meta(data, image_resolution)
		metacache.set('season', data, time_delta, string)
	except: pass
	return data

def all_episodes_meta(meta, user_info):
	def _get_tmdb_episodes(season):
		try:
			episodes = season_episodes_meta(season, meta, user_info)
			data.extend(episodes)
		except: pass
	data = []
	threads = []
	append = threads.append
	try:
		season_numbers = [str(i['season_number']) for i in meta['season_data']]
		for i in season_numbers: append(Thread(target=_get_tmdb_episodes, args=(int(i),)))
		[i.start() for i in threads]
		[i.join() for i in threads]
	except: pass
	return data

def build_movie_meta(data, fanarttv_data=None):
	data_get = data.get
	image_resolution = data['image_resolution']
	profile_resolution = image_resolution['profile']
	poster_resolution = image_resolution['poster']
	fanart_resolution = image_resolution['fanart']
	cast, studio, all_trailers, country, country_codes = [], [], [], [], []
	writer, mpaa, director, trailer = '', '', '', ''
	tmdb_id = data_get('id', '')
	imdb_id = data_get('imdb_id', '')
	rating = data_get('vote_average', '')
	plot = to_utf8(data_get('overview', ''))
	tagline = to_utf8(data_get('tagline', ''))
	votes = data_get('vote_count', '')
	premiered = data_get('release_date', '')
	if data_get('poster_path'): poster = 'https://image.tmdb.org/t/p/%s%s' % (poster_resolution, data['poster_path'])
	else: poster = ''
	if data_get('backdrop_path'): fanart = 'https://image.tmdb.org/t/p/%s%s' % (fanart_resolution, data['backdrop_path'])
	else: fanart = ''
	if fanarttv_data:
		fanart_added = True
		poster2, fanart2 = fanarttv_data['fanarttv_poster'], fanarttv_data['fanarttv_fanart']
		banner, clearart, clearlogo = fanarttv_data['banner'], fanarttv_data['clearart'], fanarttv_data['clearlogo']
		landscape, discart = fanarttv_data['landscape'], fanarttv_data['discart']
	else:
		fanart_added = False
		poster2, fanart2, banner, clearart, clearlogo, landscape, discart = '', '', '', '', '', '', ''
	try: title = to_utf8(safe_string(remove_accents(data['title'])))
	except: title = to_utf8(safe_string(data['title']))
	try: original_title = to_utf8(safe_string(remove_accents(data['original_title'])))
	except: original_title = to_utf8(safe_string(data['original_title']))
	try: english_title = [i['data']['title'] for i in data['translations']['translations'] if i['iso_639_1'] == 'en'][0]
	except: english_title = None
	try: year = try_parse_int(data['release_date'].split('-')[0])
	except: year = ''
	try: duration = int(data_get('runtime', '90') * 60)
	except: duration = 90 * 60
	rootname = '%s (%s)' % (title, year)
	try: genre = ', '.join([i['name'] for i in data['genres']])
	except: genre == []
	if data_get('production_companies'):
		try: studio = [i['name'] for i in data['production_companies']][0]
		except: pass
	if 'production_countries' in data:
		production_countries = data['production_countries']
		country = [i['name'] for i in production_countries]
		country_codes = [i['iso_3166_1'] for i in production_countries]
	if 'release_dates' in data:
		try: mpaa = [x['certification'] for i in data['release_dates']['results'] for x in i['release_dates'] if i['iso_3166_1'] == 'US'][0]
		except: pass
	if 'credits' in data:
		credits = data['credits']
		if 'cast' in credits:
			try: cast = [{'name': i['name'], 'role': i['character'],
						'thumbnail': 'https://image.tmdb.org/t/p/%s%s' % (profile_resolution, i['profile_path']) if i['profile_path'] else ''}\
						for i in credits['cast']]
			except: pass
		if 'crew' in credits:
			try: writer = ', '.join([i['name'] for i in credits['crew'] if i['job'] in writer_credits])
			except: pass
			try: director = [i['name'] for i in credits['crew'] if i['job'] == 'Director'][0]
			except: pass
	if 'alternative_titles' in data:
		alternatives = data['alternative_titles']['titles']
		alternative_titles = [i['title'] for i in alternatives if i['iso_3166_1']  in alt_titles_test]
	if 'videos' in data:
		all_trailers = data['videos']['results']
		try: trailer = ['plugin://plugin.video.youtube/play/?video_id=%s' % i['key'] for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test][0]
		except: pass
	ei_status = data_get('status', 'N/A')
	ei_homepage = data_get('homepage', 'N/A')
	if data_get('belongs_to_collection', False):
		belongs_to_collection = data['belongs_to_collection']
		ei_collection_name = belongs_to_collection['name']
		ei_collection_id = belongs_to_collection['id']
	else:
		ei_collection_name = None
		ei_collection_id = None
	try: ei_budget = '${:,}'.format(data['budget'])
	except: ei_budget = '$0'
	try: ei_revenue = '${:,}'.format(data['revenue'])
	except: ei_revenue = '$0'
	extra_info = {'status': ei_status, 'collection_name': ei_collection_name, 'collection_id': ei_collection_id,
				'budget': ei_budget, 'revenue': ei_revenue, 'homepage': ei_homepage}
	return {'tmdb_id': tmdb_id, 'imdb_id': imdb_id, 'rating': rating, 'plot': plot, 'tagline': tagline, 'votes': votes, 'premiered': premiered, 'imdbnumber': imdb_id,
			'poster': poster, 'fanart': fanart, 'poster2': poster2, 'fanart2': fanart2, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
			'discart': discart, 'genre': genre, 'title': title, 'original_title': original_title, 'english_title': english_title, 'alternative_titles': alternative_titles,
			'year': year, 'duration': duration,	'rootname': rootname, 'country': country, 'country_codes': country_codes, 'mpaa': mpaa, 'cast': cast, 'writer': writer,
			'director': director, 'all_trailers': all_trailers, 'trailer': trailer, 'studio': studio, 'fanart_added': fanart_added, 'extra_info': extra_info, 'mediatype': 'movie',
			'tvdb_id': 'None'}

def build_tvshow_meta(data, fanarttv_data=None):
	data_get = data.get
	image_resolution = data['image_resolution']
	profile_resolution = image_resolution['profile']
	poster_resolution = image_resolution['poster']
	fanart_resolution = image_resolution['fanart']
	cast, studio, all_trailers, country, country_codes = [], [], [], [], []
	writer, mpaa, director, trailer = '', '', '', ''
	tmdb_id = data_get('id', '')
	imdb_id = data['external_ids'].get('imdb_id', '')
	tvdb_id = data['external_ids'].get('tvdb_id', 'None')
	rating = data_get('vote_average', '')
	plot = to_utf8(data_get('overview', ''))
	tagline = to_utf8(data_get('tagline', ''))
	votes = data_get('vote_count', '')
	premiered = data_get('first_air_date', '')
	season_data = data['seasons']
	total_seasons = data['number_of_seasons']
	total_aired_eps = data['number_of_episodes']
	if data_get('poster_path'): poster = 'https://image.tmdb.org/t/p/%s%s' % (poster_resolution, data['poster_path'])
	else: poster = ''
	if data_get('backdrop_path'): fanart = 'https://image.tmdb.org/t/p/%s%s' % (fanart_resolution, data['backdrop_path'])
	else: fanart = ''
	if fanarttv_data:
		fanart_added = True
		poster2, fanart2 = fanarttv_data['fanarttv_poster'], fanarttv_data['fanarttv_fanart']
		banner, clearart, clearlogo = fanarttv_data['banner'], fanarttv_data['clearart'], fanarttv_data['clearlogo']
		landscape, discart = fanarttv_data['landscape'], fanarttv_data['discart']
	else:
		fanart_added = False
		poster2, fanart2, banner, clearart, clearlogo, landscape, discart = '', '', '', '', '', '', ''
	try: title = to_utf8(safe_string(remove_accents(data['name'])))
	except: title = to_utf8(safe_string(data['name']))
	try: original_title = to_utf8(safe_string(remove_accents(data['original_name'])))
	except: original_title = to_utf8(safe_string(data['original_name']))
	try: english_title = [i['data']['name'] for i in data['translations']['translations'] if i['iso_639_1'] == 'en'][0]
	except: english_title = None
	try: year = try_parse_int(data['first_air_date'].split('-')[0])
	except: year = ''
	try: duration = min(data['episode_run_time']) * 60
	except: duration = 30 * 60
	rootname = '%s (%s)' % (title, year)
	try: genre = ', '.join([i['name'] for i in data['genres']])
	except: genre == []
	if data_get('networks'):
		try: studio = [i['name'] for i in data['networks']][0]
		except: pass
	if 'production_countries' in data:
		production_countries = data['production_countries']
		country = [i['name'] for i in production_countries]
		country_codes = [i['iso_3166_1'] for i in production_countries]
	if 'content_ratings' in data:
		try: mpaa = [i['rating'] for i in data['content_ratings']['results'] if i['iso_3166_1'] == 'US'][0]
		except: pass
	elif 'release_dates' in data:
		try: mpaa = [i['release_dates'][0]['certification'] for i in data['release_dates']['results'] if i['iso_3166_1'] == 'US'][0]
		except: pass
	if 'credits' in data:
		credits = data['credits']
		if 'cast' in credits:
			try: cast = [{'name': i['name'], 'role': i['character'],
						'thumbnail': 'https://image.tmdb.org/t/p/%s%s' % (profile_resolution, i['profile_path']) if i['profile_path'] else ''}\
						for i in credits['cast']]
			except: pass
		if 'crew' in credits:
			try: writer = ', '.join([i['name'] for i in credits['crew'] if i['job'] in writer_credits])
			except: pass
			try: director = [i['name'] for i in credits['crew'] if i['job'] == 'Director'][0]
			except: pass
	if 'alternative_titles' in data:
		alternatives = data['alternative_titles']['results']
		alternative_titles = [i['title'] for i in alternatives if i['iso_3166_1'] in alt_titles_test]
	if 'videos' in data:
		all_trailers = data['videos']['results']
		try: trailer = ['plugin://plugin.video.youtube/play/?video_id=%s' % i['key'] for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test][0]
		except: pass
	status = data_get('status', 'N/A')
	ei_type = data_get('type', 'N/A')
	ei_homepage = data_get('homepage', 'N/A')
	if data_get('created_by', False):
		try: ei_created_by = ', '.join([i['name'] for i in data['created_by']])
		except: ei_created_by = 'N/A'
	else: ei_created_by = 'N/A'
	if data_get('next_episode_to_air', False):
		ei_next_episode_to_air = data['next_episode_to_air']
	else: ei_next_episode_to_air = None
	if data_get('last_episode_to_air', False):
		ei_last_episode_to_air = data['last_episode_to_air']
		if not status.lower() in finished_show_check:
			total_aired_eps = sum([i['episode_count'] for i in data['seasons'] if i['season_number'] < ei_last_episode_to_air['season_number'] and i['season_number'] != 0]) \
									+ ei_last_episode_to_air['episode_number']
	else: ei_last_episode_to_air = None
	extra_info = {'status': status, 'type': ei_type, 'homepage': ei_homepage, 'created_by': ei_created_by, 'next_episode_to_air': ei_next_episode_to_air,
				  'last_episode_to_air': ei_last_episode_to_air}
	return {'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'imdb_id': imdb_id, 'rating': rating, 'plot': plot, 'tagline': tagline, 'votes': votes, 'premiered': premiered,
			'poster': poster, 'fanart': fanart, 'poster2': poster2, 'fanart2': fanart2, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
			'discart': discart, 'genre': genre, 'title': title, 'original_title': original_title, 'english_title': english_title, 'alternative_titles': alternative_titles,
			'year': year, 'duration': duration, 'rootname': rootname, 'imdbnumber': imdb_id, 'country': country, 'country_codes': country_codes, 'mpaa': mpaa, 'cast': cast,
			'writer': writer, 'director': director, 'all_trailers': all_trailers, 'trailer': trailer, 'studio': studio, 'fanart_added': fanart_added, 'extra_info': extra_info,
			'mediatype': 'tvshow', 'season_data': season_data, 'total_seasons': total_seasons, 'total_aired_eps': total_aired_eps, 'tvshowtitle': title, 'status': status}

def build_episodes_meta(data, image_resolution):
	def _process():
		for ep_data in data:
			writer, director = '', ''
			guest_stars = []
			title = ep_data['name']
			plot = ep_data['overview']
			premiered = ep_data['air_date']
			season = ep_data['season_number']
			episode = ep_data['episode_number']
			rating = ep_data['vote_average']
			votes = ep_data['vote_count']
			if ep_data.get('still_path', None): thumb = 'https://image.tmdb.org/t/p/%s%s' % (still_resolution, ep_data['still_path'])
			else: thumb = None
			if 'guest_stars' in ep_data:
				try: guest_stars = [{'name': i['name'], 'role': i['character'],
							'thumbnail': 'https://image.tmdb.org/t/p/%s%s' % (profile_resolution, i['profile_path']) if i['profile_path'] else ''}\
							for i in ep_data['guest_stars']]
				except: pass
			if 'crew' in ep_data:
				try: writer = ', '.join([i['name'] for i in ep_data['crew'] if i['job'] in writer_credits])
				except: pass
				try: director = [i['name'] for i in ep_data['crew'] if i['job'] == 'Director'][0]
				except: pass
			yield {'writer': writer, 'director': director, 'guest_stars': guest_stars, 'mediatype': 'episode', 'title': title, 'plot': plot,
					'premiered': premiered, 'season': season, 'episode': episode, 'rating': rating, 'votes': votes, 'thumb': thumb}
	still_resolution = image_resolution['still']
	profile_resolution = image_resolution['profile']
	return list(_process())

def movie_meta_external_id(external_source, external_id):
	return tmdb.tmdbMoviesExternalID(external_source, external_id)

def tvshow_meta_external_id(external_source, external_id):
	return tmdb.tmdbTVShowsExternalID(external_source, external_id)

def english_translation(db_type, media_id, user_info):
	key = 'title' if db_type == 'movie' else 'name'
	translations = tmdb.tmdbEnglishTranslation(db_type, media_id, user_info['tmdb_api'])
	try: english = [i['data'][key] for i in translations if i['iso_639_1'] == 'en'][0]
	except: english = ''
	return english

def retrieve_user_info():
	return user_info()
