# -*- coding: utf-8 -*-
import re
from caches.main_cache import cache_object
from modules.dom_parser import parseDOM
from modules.kodi_utils import make_session, json, get_setting, local_string as ls
from modules.utils import imdb_sort_list, remove_accents, replace_html_codes, string_alphanum_to_num
# from modules.kodi_utils import logger

base_url = 'https://www.imdb.com/%s'
watchlist_url = 'user/ur%s/watchlist'
user_list_movies_url = 'list/%s/?view=detail&sort=%s&title_type=movie,short,video,tvShort,tvMovie,tvSpecial&start=1&page=%s'
user_list_tvshows_url = 'list/%s/?view=detail&sort=%s&title_type=tvSeries,tvMiniSeries&start=1&page=%s'
keywords_movies_url = 'search/keyword/?keywords=%s&sort=moviemeter,asc&title_type=movie,short,video,tvShort,tvMovie,tvSpecial&page=%s'
keywords_tvshows_url = 'search/keyword/?keywords=%s&sort=moviemeter,asc&title_type=tvSeries,tvMiniSeries&page=%s'
lists_link = 'user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles'
reviews_url = 'title/%s/reviews/_ajax?ref_=undefined&paginationKey=%s'
trivia_url = 'title/%s/trivia'
blunders_url = 'title/%s/goofs'
parentsguide_url = 'title/%s/parentalguide'
images_url = 'title/%s/mediaindex?page=%s'
videos_url = '_json/video/%s'
keywords_url = 'title/%s/keywords?'
keywords_search_url = 'find?s=kw&q=%s'
people_images_url = 'name/%s/mediaindex?page=%s'
people_trivia_url = 'name/%s/bio'
people_search_url_backup = 'search/name/?name=%s'
people_search_url = 'https://sg.media-imdb.com/suggests/%s/%s.json'
year_check_url = 'https://v2.sg.media-imdb.com/suggestion/t/%s.json'
timeout = 20.0
session = make_session()

def people_get_imdb_id(actor_name):
	string = 'people_get_imdb_id_%s' % actor_name
	name = actor_name.lower()
	string = 'imdb_people_id_%s' % name
	url, url_backup = people_search_url % (name[0], name.replace(' ', '%20')), base_url % people_search_url_backup % name
	params = {'url': url, 'action': 'imdb_people_id', 'name': name, 'url_backup': url_backup}
	return cache_object(get_imdb, string, params, False, 8736)[0]

def imdb_user_lists(media_type):
	imdb_user = string_alphanum_to_num(get_setting('imdb_user'))
	string = 'imdb_user_lists_%s_%s' % (media_type, imdb_user)
	url = base_url % lists_link % imdb_user
	params = {'url': url, 'action': 'imdb_user_lists'}
	return cache_object(get_imdb, string, params, False, 2)[0]

def imdb_watchlist(media_type, foo_var, page_no):
	imdb_user = string_alphanum_to_num(get_setting('imdb_user'))
	sort = imdb_sort_list()
	string = 'imdb_watchlist_%s_%s_%s_%s' % (media_type, imdb_user, sort, page_no)
	url = base_url % watchlist_url % imdb_user
	params = {'url': url, 'action': 'imdb_watchlist', 'imdb_user': imdb_user, 'media_type': media_type, 'sort': sort, 'page_no': page_no}
	return cache_object(get_imdb, string, params, False, 2)

def imdb_user_list_contents(media_type, list_id, page_no):
	imdb_user = string_alphanum_to_num(get_setting('imdb_user'))
	sort = imdb_sort_list()
	string = 'imdb_user_list_contents_%s_%s_%s_%s_%s' % (media_type, imdb_user, list_id, sort, page_no)
	params = {'url': list_id, 'action': 'imdb_user_list_contents', 'media_type': media_type, 'sort': sort, 'page_no': page_no}
	return cache_object(get_imdb, string, params, False, 2)

def imdb_keywords_list_contents(media_type, keywords, page_no):
	keywords = keywords.replace(' ', '-')
	add_url = keywords_movies_url if media_type == 'movie' else keywords_tvshows_url
	url = base_url % add_url % (keywords, page_no)
	string = 'imdb_keywords_list_contents_%s_%s_%s' % (media_type, keywords, page_no)
	params = {'url': url, 'action': 'imdb_keywords_list_contents'}
	return cache_object(get_imdb, string, params, False, 168)

def imdb_reviews(imdb_id):
	string = 'imdb_reviews_%s' % imdb_id
	params = {'action': 'imdb_reviews', 'imdb_id': imdb_id}
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

def imdb_people_trivia(imdb_id):
	url = base_url % people_trivia_url % imdb_id
	string = 'imdb_people_trivia_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_people_trivia'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_keywords(imdb_id):
	url = base_url % keywords_url % imdb_id
	string = 'imdb_keywords_%s' % imdb_id
	params = {'url': url, 'action': 'imdb_keywords'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def imdb_year_check(imdb_id):
	url = year_check_url % imdb_id
	string = 'imdb_year_check%s' % imdb_id
	params = {'url': url, 'imdb_id': imdb_id, 'action': 'imdb_year_check'}
	return cache_object(get_imdb, string, params, False, 8736)[0]

def imdb_keyword_search(keyword):
	url = base_url % keywords_search_url % keyword
	string = 'imdb_keyword_search_%s' % keyword
	params = {'url': url, 'action': 'imdb_keyword_search'}
	return cache_object(get_imdb, string, params, False, 168)[0]

def get_imdb(params):
	imdb_list = []
	action = params.get('action')
	url = params.get('url')
	next_page = None
	if 'date' in params:
		from datetime import datetime, timedelta
		date_time = (datetime.utcnow() - timedelta(hours=5))
		for i in re.findall(r'date\[(\d+)\]', url):
			url = url.replace('date[%s]' % i, (date_time - timedelta(days = int(i))).strftime('%Y-%m-%d'))
	if action in ('imdb_watchlist', 'imdb_user_list_contents', 'imdb_keywords_list_contents'):
		def _process():
			for item in items:
				try:
					title = parseDOM(item, 'a')[1]
					year = parseDOM(item, 'span', attrs={'class': 'lister-item-year.+?'})
					year = re.search(r'(\d{4})', year[0]).group(1)
					imdb_id = parseDOM(item, 'a', ret='href')[0]
					imdb_id = re.search(r'(tt\d*)', imdb_id).group(1)
					yield {'title': str(title), 'year': str(year), 'imdb_id': str(imdb_id)}
				except: pass
		if action in ('imdb_watchlist', 'imdb_user_list_contents'):
			list_url_type = user_list_movies_url if params['media_type'] == 'movie' else user_list_tvshows_url
			if action == 'imdb_watchlist':
				def _get_watchlist_id(dummy):
					return parseDOM(remove_accents(session.get(url, timeout=timeout).text), 'meta', ret='content', attrs = {'property': 'pageId'})[0]
				url = cache_object(_get_watchlist_id, 'imdb_watchlist_id_%s' % params['imdb_user'], 'dummy', False, 672)
			url = base_url % list_url_type % (url, params['sort'], params['page_no'])
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
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
			for item in items:
				try:
					title = parseDOM(item, 'a')[0]
					title = replace_html_codes(title)
					url = parseDOM(item, 'a', ret='href')[0]
					list_id = url.split('/list/', 1)[-1].strip('/')
					yield {'title': title, 'list_id': list_id}
				except: pass
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
		items = parseDOM(result, 'li', attrs={'class': 'ipl-zebra-list__item user-list'})
		imdb_list = list(_process())
	elif action in ('imdb_trivia', 'imdb_blunders'):
		def _process():
			for count, item in enumerate(items, 1):
				try:
					content = re.sub(r'<a href="\S+">', '', item).replace('</a>', '')
					content = replace_html_codes(content)
					content = content.replace('<br/><br/>', '\n')
					content = '[B]%s %02d.[/B][CR][CR]%s' % (_str, count, content)
					yield content
				except: pass
		if action == 'imdb_trivia': _str = ls(32984).upper()
		else: _str =  ls(32986).upper()
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
		result = result.replace('\n', ' ')
		items = parseDOM(result, 'div', attrs={'class': 'sodatext'})
		imdb_list = list(_process())
	elif action == 'imdb_people_trivia':
		def _process():
			for count, item in enumerate(items, 1):
				try:
					content = re.sub(r'<a href=".+?">', '', item).replace('</a>', '').replace('<p> ', '').replace('<br />', '').replace('  ', '')
					content = replace_html_codes(content)
					content = '[B]%s %02d.[/B][CR][CR]%s' % (trivia_str, count, content)
					yield content
				except: pass
		trivia_str = ls(32984).upper()
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
		result = result.replace('\n', ' ')
		result = re.search(r'<a name="trivia"></a>(.*?)Personal Quotes', result).group(1)
		items = parseDOM(result, 'div', attrs={'class': 'soda .+?'})
		imdb_list = list(_process())
	elif action == 'imdb_reviews':
		def _process():
			for count, listing in enumerate(all_reviews, 1):
				try: spoiler = listing['spoiler']
				except: spoiler = False
				try: listing = listing['content']
				except: continue
				try:
					try:
						content = parseDOM(listing, 'div', attrs={'class': 'text show-more__control'})[0]
						content = replace_html_codes(content)
						content = content.replace('<br/><br/>', '\n')
					except: continue
					try: title = parseDOM(listing, 'a', attrs={'class': 'title'})[0]
					except: title = ''
					try: date = parseDOM(listing, 'span', attrs={'class': 'review-date'})[0]
					except: date = ''
					try:
						rating = parseDOM(listing, 'span', attrs={'class': 'rating-other-user-rating'})
						rating = parseDOM(rating, 'span')
						rating = rating[0] + rating[1]
					except: rating = ''
					review = '[B]%02d. [I]%s - %s - %s[/I][/B][CR][CR]%s' % (count, rating, date, title, content)
					if spoiler: review = '[B][COLOR red][%s][/COLOR][CR][/B]' % spoiler_str + review
					yield review
				except: pass
		spoiler_str = ls(32985).upper()
		imdb_id = params['imdb_id']
		paginationKey = ''
		non_spoiler_list = []
		spoiler_list = []
		count = 0
		while count < 3:
			url = base_url % reviews_url % (imdb_id, paginationKey)
			result = session.get(url, timeout=timeout)
			result = remove_accents(result.text)
			result = result.replace('\n', ' ')
			non_spoilers = parseDOM(result, 'div', attrs={'class': 'lister-item mode-detail imdb-user-review  collapsable'})
			non_spoiler_list.extend([{'spoiler': False, 'content': i} for i in non_spoilers])
			spoilers = parseDOM(result, 'div', attrs={'class': 'lister-item mode-detail imdb-user-review  with-spoiler'})
			spoiler_list.extend([{'spoiler': True, 'content': i} for i in spoilers])
			try: paginationKey = re.search(r'data-key="(.+?)"', result, re.DOTALL).group(1)
			except: break
			count += 1
		all_reviews = non_spoiler_list + spoiler_list
		imdb_list = list(_process())
	elif action == 'imdb_images':
		def _process():
			for item in image_results:
				try:
					try: title = re.search(r'alt="(.+?)"', item, re.DOTALL).group(1)
					except: title = ''
					try:
						thumb = re.search(r'src="(.+?)"', item, re.DOTALL).group(1)
						split = thumb.split('_V1_')[0]
						thumb = split + '_V1_UY300_CR26,0,300,300_AL_.jpg'
						image = split + '_V1_.jpg'
						images = {'title': title, 'thumb': thumb, 'image': image}
					except: continue
					yield images
				except: pass
		image_results = []
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
		result = result.replace('\n', ' ')
		try:
			pages = parseDOM(result, 'span', attrs={'class': 'page_list'})[0]
			pages = [int(i) for i in parseDOM(pages, 'a')]
		except: pages = [1]
		if params['next_page'] in pages: next_page = params['next_page']
		try:
			image_results = parseDOM(result, 'div', attrs={'class': 'media_index_thumb_list'})[0]
			image_results = parseDOM(image_results, 'a')
		except: pass
		if image_results: imdb_list = list(_process())
	elif action == 'imdb_videos':
		def _process():
			for count, item in enumerate(playlists, 1):
				videos = []
				vid_id = item['videoId']
				metadata = videoMetadata[vid_id]
				title = '%01d. %s' % (count, metadata['title'])
				poster = metadata['slate']['url']
				for i in metadata['encodings']:
					quality = i['definition']
					if quality == 'auto': continue
					if quality == 'SD': quality = '360p'
					quality_rank = quality_ranks_dict[quality]
					videos.append({'quality': quality, 'quality_rank': quality_rank, 'url': i['videoUrl']})
				yield {'title': title, 'poster': poster, 'videos': videos}
		quality_ranks_dict = {'360p': 3, '480p': 2, '720p': 1, '1080p': 0}
		result = session.get(url, timeout=timeout).json()
		playlists = result['playlists'][params['imdb_id']]['listItems']
		videoMetadata = result['videoMetadata']
		imdb_list = list(_process())
	elif action == 'imdb_people_id':
		try:
			name = params['name']
			result = session.get(url, timeout=timeout).text
			results = json.loads(re.sub(r'imdb\$(.+?)\(', '', result)[:-1])['d']
			imdb_list = [i['id'] for i in results if i['id'].startswith('nm') and i['l'].lower() == name][0]
		except: imdb_list = []
		if not imdb_list:
			try:
				result = session.get(params['url_backup'], timeout=timeout)
				result = remove_accents(result.text)
				result = result.replace('\n', ' ')
				result = parseDOM(result, 'div', attrs={'class': 'lister-item-image'})[0]
				imdb_list = re.search(r'href="/name/(.+?)"', result, re.DOTALL).group(1)
			except: pass
	elif action == 'imdb_year_check':
		try:
			imdb_id = params.get('imdb_id')
			result = session.get(url, timeout=timeout).json()
			result = result['d']
			imdb_list = [str(i['y']) for i in result if i['id'] == imdb_id][0]
		except: pass
	elif action == 'imdb_parentsguide':
		spoiler_results = None
		spoiler_list, final_list = [], []
		spoiler_append, final_list_append, imdb_append = spoiler_list.append, final_list.append, imdb_list.append
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
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
					title = replace_html_codes(re.search(r'(.+?)</h4>', item, re.DOTALL).group(1))
					item_dict['title'] = title
				except: continue
				try:
					listings = parseDOM(item, 'li', attrs={'class': 'ipl-zebra-list__item'})
					item_dict['listings'] = []
				except: continue
				dict_listings_append = item_dict['listings'].append
				for item in listings:
					try:
						listing = replace_html_codes(re.search(r'(.+?)     <div class="', item, re.DOTALL).group(1))
						if not listing in item_dict['listings']: dict_listings_append(listing)
					except: pass
				if not item_dict in spoiler_list: spoiler_append(item_dict)
		for item in results:
			item_dict = {}
			try:
				title = replace_html_codes(parseDOM(item, 'h4', attrs={'class': 'ipl-list-title'})[0])
				item_dict['title'] = title
			except: continue
			try:
				ranking = replace_html_codes(parseDOM(item, 'span', attrs={'class': 'ipl-status-pill ipl-status-pill--(.+?)'})[0])
				item_dict['ranking'] = ranking
			except: item_dict['ranking'] = 'none'
			try:
				listings = parseDOM(item, 'li', attrs={'class': 'ipl-zebra-list__item'})
				item_dict['listings'] = []
			except: pass
			if listings:
				dict_listings_append = item_dict['listings'].append
				for item in listings:
					try:
						listing = replace_html_codes(re.search(r'(.+?)     <div class="', item, re.DOTALL).group(1))
						if not listing in item_dict['listings']: dict_listings_append(listing)
					except: pass
			elif item_dict['ranking'] == 'none': continue
			if item_dict: final_list_append(item_dict)
		if spoiler_list:
			for imdb in imdb_list:
				for spo in spoiler_list:
					if spo['title'] == imdb['title']:
						imdb['listings'].extend(spo['listings'])
		for item in final_list:
			new_dict = {}
			listings = list(set(item['listings']))
			item['listings'] = list(set(item['listings']))
			new_dict['title'] = item['title']
			new_dict['ranking'] = item['ranking']
			new_dict['content'] = '\n\n'.join(['%02d. %s' % (count, i) for count, i in enumerate(listings, 1)])
			new_dict['total_count'] = len(listings)
			imdb_append(new_dict)
	elif action == 'imdb_keywords':
		def _process():
			for item in items:
				try:
					keyword = re.search(r'" >(.+?)</a>', item, re.DOTALL).group(1)
					yield keyword
				except: pass
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
		result = result.replace('\n', ' ')
		items = parseDOM(result, 'div', attrs={'class': 'sodatext'})
		imdb_list = list(_process())
		imdb_list = sorted(imdb_list)
	elif action == 'imdb_keyword_search':
		def _process():
			for item in items:
				try:
					keyword = re.search(r'keywords=(.+?)"', item, re.DOTALL).group(1)
					listings = re.search(r'</a> (.+?) </td>', item, re.DOTALL).group(1)
					yield (keyword, listings)
				except: pass
		result = session.get(url, timeout=timeout)
		result = remove_accents(result.text)
		result = result.replace('\n', ' ')
		items_odd = parseDOM(result, 'tr', attrs={'class': 'findResult odd'})
		items_even = parseDOM(result, 'tr', attrs={'class': 'findResult even'})
		items = [x for y in zip(items_odd, items_even) for x in y]
		imdb_list = list(_process())
	return (imdb_list, next_page)

def clear_imdb_cache(silent=False):
	from modules.kodi_utils import path_exists, clear_property, database, maincache_db
	try:
		if not path_exists(maincache_db): return True
		dbcon = database.connect(maincache_db, timeout=40.0, isolation_level=None)
		dbcur = dbcon.cursor()
		dbcur.execute('''PRAGMA synchronous = OFF''')
		dbcur.execute('''PRAGMA journal_mode = OFF''')
		dbcur.execute("SELECT id FROM maincache WHERE id LIKE ?", ('imdb_%',))
		imdb_results = [str(i[0]) for i in dbcur.fetchall()]
		if not imdb_results: return True
		dbcur.execute("DELETE FROM maincache WHERE id LIKE ?", ('imdb_%',))
		for i in imdb_results: clear_property(i)
		return True
	except: return False






