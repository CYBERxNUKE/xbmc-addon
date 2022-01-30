# -*- coding: utf-8 -*-
import re
import requests
from caches.main_cache import cache_object
from modules.dom_parser import parseDOM
from modules.utils import imdb_sort_list, to_utf8, remove_accents, replace_html_codes, string_alphanum_to_num
from modules.settings_reader import get_setting
# from modules.kodi_utils import logger

base_url = 'https://www.imdb.com/%s'
watchlist_url = 'user/ur%s/watchlist'
user_list_movies_url = 'list/%s/?view=detail&sort=%s&title_type=movie,short,video,tvShort,tvMovie,tvSpecial&start=1&page=%s'
user_list_tvshows_url = 'list/%s/?view=detail&sort=%s&title_type=tvSeries,tvMiniSeries&start=1&page=%s'
keywords_movies_url = 'search/keyword/?keywords=%s&sort=moviemeter,asc&title_type=movie,short,video,tvShort,tvMovie,tvSpecial&page=%s'
keywords_tvshows_url = 'search/keyword/?keywords=%s&sort=moviemeter,asc&title_type=tvSeries,tvMiniSeries&page=%s'
lists_link = 'user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles'
reviews_url = 'title/%s/reviews?sort=helpfulness'
trivia_url = 'title/%s/trivia'
blunders_url = 'title/%s/goofs'
parentsguide_url = 'title/%s/parentalguide'
images_url = 'title/%s/mediaindex?page=%s'
videos_url = '_json/video/%s'
keywords_url = 'title/%s/keywords?'
keywords_search_url = 'find?s=kw&q=%s'
people_images_url = 'name/%s/mediaindex?page=%s'
people_search_url_backup = 'search/name/?name=%s'
people_search_url = 'https://sg.media-imdb.com/suggests/%s/%s.json'
movie_year_check_url = 'https://v2.sg.media-imdb.com/suggestion/t/%s.json'

def people_get_imdb_id(actor_name, actor_tmdbID=None):
	def _get(dummy):
		imdb_id = None
		if actor_tmdbID:
			from apis.tmdb_api import tmdb_people_full_info
			try: imdb_id = tmdb_people_full_info(actor_tmdbID)['imdb_id']
			except: pass
		if not imdb_id:
			name = actor_name.lower()
			string = 'imdb_people_id_%s' % name
			url = 'https://sg.media-imdb.com/suggests/%s/%s.json' % (name[0], name.replace(' ', '%20'))
			url_backup = base_url % people_search_url_backup % name
			params = {'url': url, 'action': 'imdb_people_id', 'name': name, 'url_backup': url_backup}
			imdb_id = get_imdb(params)[0]
		return imdb_id
	string = 'people_get_imdb_id_%s' % actor_name
	return cache_object(_get, string, 'dummy', False, 8736)

def imdb_user_lists(db_type):
	imdb_user = string_alphanum_to_num(get_setting('imdb_user'))
	string = 'imdb_user_lists_%s_%s' % (db_type, imdb_user)
	url = base_url % lists_link % imdb_user
	params = {'url': url, 'action': 'imdb_user_lists'}
	return cache_object(get_imdb, string, params, False, 0.5)[0]

def imdb_watchlist(db_type, foo_var, page_no):
	imdb_user = string_alphanum_to_num(get_setting('imdb_user'))
	sort = imdb_sort_list()
	string = 'imdb_watchlist_%s_%s_%s_%s' % (db_type, imdb_user, sort, page_no)
	url = base_url % watchlist_url % imdb_user
	params = {'url': url, 'action': 'imdb_watchlist', 'db_type': db_type, 'sort': sort, 'page_no': page_no}
	return cache_object(get_imdb, string, params, False, 0.5)

def imdb_user_list_contents(db_type, list_id, page_no):
	imdb_user = string_alphanum_to_num(get_setting('imdb_user'))
	sort = imdb_sort_list()
	string = 'imdb_user_list_contents_%s_%s_%s_%s_%s' % (db_type, imdb_user, list_id, sort, page_no)
	params = {'url': list_id, 'action': 'imdb_user_list_contents', 'db_type': db_type, 'sort': sort, 'page_no': page_no}
	return cache_object(get_imdb, string, params, False, 0.5)

def imdb_keywords_list_contents(db_type, keywords, page_no):
	keywords = keywords.replace(' ', '-')
	add_url = keywords_movies_url if db_type == 'movie' else keywords_tvshows_url
	url = base_url % add_url % (keywords, page_no)
	string = 'imdb_keywords_list_contents_%s_%s_%s' % (db_type, keywords, page_no)
	params = {'url': url, 'action': 'imdb_keywords_list_contents'}
	return cache_object(get_imdb, string, params, False, 168)

def imdb_reviews(imdb_id):
	url = base_url % reviews_url % imdb_id
	string = 'imdb_reviews_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_reviews'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_parentsguide(imdb_id):
	url = base_url % parentsguide_url % imdb_id
	string = 'imdb_parentsguide_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_parentsguide'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_trivia(imdb_id):
	url = base_url % trivia_url % imdb_id
	string = 'imdb_trivia_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_trivia'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_blunders(imdb_id):
	url = base_url % blunders_url % imdb_id
	string = 'imdb_blunders_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_blunders'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_images(imdb_id, page_no):
	url = base_url % images_url % (imdb_id, page_no)
	string = 'imdb_images_%s_%s' % (imdb_id, str(page_no))
	params = {'url': url, 'action': 'imdb_images', 'next_page': int(page_no)+1}
	return cache_object(get_imdb, string, params, False, 168)

def imdb_videos(imdb_id):
	url = base_url % videos_url % imdb_id
	string = 'imdb_videos_%s' % imdb_id
	params = {'url': url, 'imdb_id': imdb_id, 'action': 'imdb_videos'}
	return cache_object(get_imdb, string, params, False, 24)[0]

def imdb_people_images(imdb_id, page_no):
	url = base_url % people_images_url % (imdb_id, page_no)
	string = 'imdb_people_images_%s_%s' % (imdb_id, str(page_no))
	params = {'url': url, 'action': 'imdb_images', 'next_page': 1}
	return cache_object(get_imdb, string, params, False, 168)

def imdb_keywords(imdb_id):
	url = base_url % keywords_url % imdb_id
	string = 'imdb_keywords_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_keywords'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_movie_year(imdb_id):
	url = movie_year_check_url % imdb_id
	string = 'imdb_movie_year_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_movie_year'}
	return cache_object(get_imdb, string, params, False, 720)[0]

def imdb_keyword_search(keyword):
	url = base_url % keywords_search_url % keyword
	string = 'imdb_keyword_search_%s' % keyword
	params = {'url': url, 'action': 'imdb_keyword_search'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def get_imdb(params):
	imdb_list = []
	action = params['action']
	url = params['url']
	next_page = None
	if 'date' in params:
		from datetime import datetime, timedelta
		date_time = (datetime.utcnow() - timedelta(hours=5))
		for i in re.findall(r'date\[(\d+)\]', url):
			url = url.replace('date[%s]' % i, (date_time - timedelta(days = int(i))).strftime('%Y-%m-%d'))
	if action in ('imdb_watchlist', 'imdb_user_list_contents', 'imdb_keywords_list_contents'):
		def _process():
			for item in to_utf8(items):
				try:
					title = parseDOM(item, 'a')[1]
					year = parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
					year = re.findall(r'(\d{4})', year[0])[0]
					imdb_id = parseDOM(item, 'a', ret='href')[0]
					imdb_id = re.findall(r'(tt\d*)', imdb_id)[0]
					yield {'title': str(title), 'year': str(year), 'imdb_id': str(imdb_id)}
				except: pass
		if action in ('imdb_watchlist', 'imdb_user_list_contents'):
			list_url_type = user_list_movies_url if params['db_type'] == 'movie' else user_list_tvshows_url
			if action == 'imdb_watchlist':
				url = parseDOM(to_utf8(remove_accents(requests.get(url).text)), 'meta', ret='content', attrs = {'property': 'pageId'})[0]
			url = base_url % list_url_type % (url, params['sort'], params['page_no'])
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		items = parseDOM(result, 'div', attrs={'class': '.+? lister-item'})
		items += parseDOM(result, 'div', attrs={'class': 'lister-item .+?'})
		items += parseDOM(result, 'div', attrs={'class': 'list_item.+?'})
		imdb_list = list(_process())
		try:
			result = result.replace('"class="lister-page-next', '" class="lister-page-next')
			next_page = parseDOM(result, 'a', ret='href', attrs={'class': '.*?lister-page-next.*?'})
			if len(next_page) == 0:
				next_page = parseDOM(result, 'div', attrs = {'class': 'pagination'})[0]
				next_page = zip(parseDOM(next_page, 'a', ret='href'), parseDOM(next_page, 'a'))
				next_page = [i[0] for i in next_page if 'Next' in i[1]]
		except: pass
	elif action == 'imdb_user_lists':
		def _process():
			for item in to_utf8(items):
				try:
					title = parseDOM(item, 'a')[0]
					title = replace_html_codes(title)
					url = parseDOM(item, 'a', ret='href')[0]
					list_id = url.split('/list/', 1)[-1].strip('/')
					yield {'title': title, 'list_id': list_id}
				except: pass
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		items = parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
		imdb_list = list(_process())
	elif action in ('imdb_trivia', 'imdb_blunders'):
		def _process():
			for item in to_utf8(items):
				try:
					content = re.sub(r'<a href="\S+">', '', item).replace('</a>', '')
					content = replace_html_codes(content)
					content = content.replace('<br/><br/>', '\n')
					yield content
				except: pass
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		items = parseDOM(result, 'div', attrs={'class': 'sodatext'})
		imdb_list = list(_process())
	elif action == 'imdb_reviews':
		def _process():
			for listing in to_utf8(all_reviews):
				try: spoiler = listing['spoiler']
				except: spoiler = False
				try: listing = listing['content']
				except: continue
				try:
					try:
						title = parseDOM(listing, 'a', attrs={'class': 'title'})[0]
						title = to_utf8(remove_accents(title))
					except: title = ''
					try:
						date = parseDOM(listing, 'span', attrs={'class': 'review-date'})[0]
						date = to_utf8(remove_accents(date))
					except: date = ''
					try:
						rating = parseDOM(listing, 'span', attrs={'class': 'rating-other-user-rating'})
						rating = parseDOM(rating, 'span')
						rating = rating[0] + rating[1]
						rating = to_utf8(remove_accents(rating))
					except: rating = ''			
					try:
						content = parseDOM(listing, 'div', attrs={'class': 'text show-more__control'})[0]
						content = replace_html_codes(content)
						content = to_utf8(remove_accents(content))
						content = content.replace('<br/><br/>', '\n')
					except: continue
					review = {'spoiler': spoiler, 'title': title, 'date': date, 'rating': rating, 'content': content}
					yield review
				except: pass
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		non_spoilers = parseDOM(result, 'div', attrs={'class': 'lister-item mode-detail imdb-user-review  collapsable'})
		spoilers = parseDOM(result, 'div', attrs={'class': 'lister-item mode-detail imdb-user-review  with-spoiler'})
		non_spoilers = [{'spoiler': False, 'content': i} for i in non_spoilers]
		spoilers = [{'spoiler': True, 'content': i} for i in spoilers]
		all_reviews = non_spoilers + spoilers
		imdb_list = list(_process())
	elif action == 'imdb_images':
		def _process():
			for item in to_utf8(image_results):
				try:
					try: title = re.findall(r'alt="(.+?)"', item, re.DOTALL)[0]
					except: title = ''
					try:
						thumb = re.findall(r'src="(.+?)"', item, re.DOTALL)[0]
						split = thumb.split('_V1_')[0]
						thumb = split + '_V1_UY300_CR26,0,300,300_AL_.jpg'
						image = split + '_V1_.jpg'
						images = {'title': title, 'thumb': thumb, 'image': image}
					except: continue
					yield images
				except: pass
		image_results = []
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		try:
			pages = parseDOM(result, 'span', attrs={'class': 'page_list'})[0]
			pages = [int(i) for i in parseDOM(pages, 'a')]
		except: pages = [1]
		if params['next_page'] in pages:
			next_page = params['next_page']
		try:
			image_results = parseDOM(result, 'div', attrs={'class': 'media_index_thumb_list'})[0]
			image_results = parseDOM(image_results, 'a')
		except: pass
		if image_results: imdb_list = list(_process())
	elif action == 'imdb_videos':
		def _process():
			for item in playlists:
				videos = []
				vid_id = item['videoId']
				metadata = videoMetadata[vid_id]
				title = metadata['title']
				poster = metadata['slate']['url']
				for i in metadata['encodings']:
					quality = i['definition']
					if quality == 'auto': continue
					if quality == 'SD': quality = '360p'
					quality_rank = quality_ranks_dict[quality]
					videos.append({'quality': quality, 'quality_rank': quality_rank, 'url': i['videoUrl']})
				yield {'title': title, 'poster': poster, 'videos': videos}
		quality_ranks_dict = {'360p': 3, '480p': 2, '720p': 1, '1080p': 0}
		result = requests.get(url).json()
		playlists = result['playlists'][params['imdb_id']]['listItems']
		videoMetadata = result['videoMetadata']
		imdb_list = list(_process())
	elif action == 'imdb_people_id':
		try:
			import json
			name = params['name']
			result = requests.get(url).content
			result = to_utf8(json.loads(result.replace('imdb$%s(' % name.replace(' ', '_'), '')[:-1]))['d']
			imdb_list = [i['id'] for i in results if i['id'].startswith('nm') and i['l'].lower() == name][0]
		except: pass
		if not imdb_list:
			result = requests.get(params['url_backup'])
			result = to_utf8(remove_accents(result.text))
			result = result.replace('\n', ' ')
			try:
				result = parseDOM(result, 'div', attrs={'class': 'lister-item-image'})[0]
				imdb_list = re.findall(r'href="/name/(.+?)"', result, re.DOTALL)[0]
			except: pass
	elif action == 'imdb_movie_year':
		result = requests.get(url).json()
		try:
			result = result['d'][0]
			imdb_list = int(result['y'])
		except: pass
	elif action == 'imdb_parentsguide':
		spoiler_results = None
		spoiler_list = []
		spoiler_append = spoiler_list.append
		imdb_append = imdb_list.append
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		results = parseDOM(result, 'section', attrs={'id': r'advisory-(.+?)'})
		try: spoiler_results = parseDOM(result, 'section', attrs={'id': 'advisory-spoilers'})[0]
		except: pass
		if spoiler_results:
			results = [i for i in results if not i in spoiler_results]
			spoiler_results = spoiler_results.split('<h4 class="ipl-list-title">')[1:]
			for item in spoiler_results:
				item_dict = {}
				try:
					title = replace_html_codes(re.findall(r'(.+?)</h4>', item, re.DOTALL)[0])
					title = to_utf8(remove_accents(title))
					item_dict['title'] = title
				except: continue
				try:
					listings = parseDOM(item, 'li', attrs={'class': 'ipl-zebra-list__item'})
					item_dict['listings'] = []
				except: continue
				dict_listings_append = item_dict['listings'].append
				for item in listings:
					try:
						listing = replace_html_codes(re.findall(r'(.+?)     <div class="', item, re.DOTALL)[0])
						listing = to_utf8(remove_accents(listing))
						if not listing in item_dict['listings']: dict_listings_append(listing)
					except: pass
				if not item_dict in spoiler_list: spoiler_append(item_dict)
		for item in to_utf8(results):
			item_dict = {}
			try:
				title = replace_html_codes(parseDOM(item, 'h4', attrs={'class': 'ipl-list-title'})[0])
				title = to_utf8(remove_accents(title))
				item_dict['title'] = title
			except: continue
			try:
				ranking = replace_html_codes(parseDOM(item, 'span', attrs={'class': 'ipl-status-pill ipl-status-pill--(.+?)'})[0])
				ranking = to_utf8(remove_accents(ranking))
				item_dict['ranking'] = ranking
			except: continue
			try:
				listings = parseDOM(item, 'li', attrs={'class': 'ipl-zebra-list__item'})
				item_dict['listings'] = []
			except: continue
			dict_listings_append = item_dict['listings'].append
			for item in listings:
				try:
					listing = replace_html_codes(re.findall(r'(.+?)     <div class="', item, re.DOTALL)[0])
					listing = to_utf8(remove_accents(listing))
					if not listing in item_dict['listings']: dict_listings_append(listing)
				except: pass
			if item_dict: imdb_append(item_dict)
		if spoiler_list:
			for imdb in imdb_list:
				for spo in spoiler_list:
					if spo['title'] == imdb['title']:
						imdb['listings'].extend(spo['listings'])
		for item in imdb_list:
			item['listings'] = list(set(item['listings']))
	elif action == 'imdb_keywords':
		def _process():
			for item in to_utf8(items):
				try:
					keyword = re.findall(r'" >(.+?)</a>', item, re.DOTALL)[0]
					yield keyword
				except: pass
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		items = parseDOM(result, 'div', attrs={'class': 'sodatext'})
		imdb_list = list(_process())
		imdb_list = sorted(imdb_list)
	elif action == 'imdb_keyword_search':
		def _process():
			for item in items:
				try:
					keyword = re.findall(r'keywords=(.+?)"', item, re.DOTALL)[0]
					listings = re.findall(r'</a> (.+?) </td>', item, re.DOTALL)[0]
					yield (keyword, listings)
				except: pass
		result = requests.get(url)
		result = to_utf8(remove_accents(result.text))
		result = result.replace('\n', ' ')
		items_odd = parseDOM(result, 'tr', attrs={'class': 'findResult odd'})
		items_even = parseDOM(result, 'tr', attrs={'class': 'findResult even'})
		items = [x for y in zip(items_odd, items_even) for x in y]
		imdb_list = list(_process())
	return (imdb_list, next_page)

def clear_imdb_cache(silent=False):
	import sqlite3 as database
	from modules.kodi_utils import translate_path, path_exists, clear_property
	try:
		IMDB_DATABASE = translate_path('special://profile/addon_data/plugin.video.fen/maincache.db')
		if not path_exists(IMDB_DATABASE): return True
		dbcon = database.connect(IMDB_DATABASE)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT id FROM maincache WHERE id LIKE ?", ('imdb_%',))
		imdb_results = [str(i[0]) for i in dbcur.fetchall()]
		if not imdb_results: return True
		dbcur.execute("DELETE FROM maincache WHERE id LIKE ?", ('imdb_%',))
		dbcon.commit()
		dbcon.close()
		for i in imdb_results: clear_property(i)
		return True
	except: return False






