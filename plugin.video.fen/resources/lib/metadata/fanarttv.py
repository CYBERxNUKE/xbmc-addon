# -*- coding: utf-8 -*-
import requests
from caches.meta_cache import cache_function
# from modules.kodi_utils import logger

# Code snippets from nixgates. Thankyou.

base_url = 'http://webservice.fanart.tv/v3/%s/%s'
api_key = 'a7ad21743fd710fccb738232f2fbdcfc'
default_extra_fanart = {'fanarttv_poster': '', 'fanarttv_fanart': '', 'banner': '', 'clearart': '', 'clearlogo': '', 'landscape': '', 'discart': '', 'fanart_added': True}
default_fanart_meta = {'poster2': '', 'fanart2': '', 'banner': '', 'clearart': '', 'clearlogo': '', 'landscape': '', 'discart': '', 'fanart_added': True}
EXPIRY_6_MONTHS = 4368

def get(db_type, language, remote_id, client_key):
	def request_art(dummy):
		try:
			art = requests.get(query, headers=headers, timeout=20.0)
			return art.json()
		except: return None
	def parse_art(art):
		if art is None: return ''
		try:
			result = [(x['url'], x['likes']) for x in art if x.get('lang') == language]
			if not result and language != 'en': result = [(x['url'], x['likes']) for x in art if x.get('lang') == 'en']
			if not result: result = [(x['url'], x['likes']) for x in art if any(value == x.get('lang') for value in ['00', ''])]
			if not result: result = [(x['url'], x['likes']) for x in art]
			result.sort(key=lambda x: int(x[1]), reverse=True)
			result = [x[0] for x in result][0]
		except: result = ''
		if not 'http' in result: result = ''
		return result
	if not remote_id: return default_extra_fanart
	query = base_url % (db_type, remote_id)
	headers = {'client-key': client_key, 'api-key': api_key}
	string = 'fanart_%s_%s_%s' % (db_type, language, remote_id)
	art = cache_function(request_art, string, 'dummy', EXPIRY_6_MONTHS, json=False)
	if art == None or 'error_message' in art: return default_extra_fanart
	art_get = art.get
	if db_type == 'movies':
		fanart_data = {'fanarttv_poster': parse_art(art_get('movieposter')),
						'fanarttv_fanart': parse_art(art_get('moviebackground')),
						'banner': parse_art(art_get('moviebanner')),
						'clearart': parse_art(art_get('movieart', []) + art_get('hdmovieclearart', [])),
						'clearlogo': parse_art(art_get('movielogo', []) + art_get('hdmovielogo', [])),
						'landscape': parse_art(art_get('moviethumb')),
						'discart': parse_art(art_get('moviedisc')),
						'fanart_added': True}
	else:
		fanart_data = {'fanarttv_poster': parse_art(art_get('tvposter')),
						'fanarttv_fanart': parse_art(art_get('showbackground')),
						'banner': parse_art(art_get('tvbanner')),
						'clearart': parse_art(art_get('clearart', []) + art_get('hdclearart', [])),
						'clearlogo': parse_art(art_get('hdtvlogo', []) + art_get('clearlogo', [])),
						'landscape': parse_art(art_get('tvthumb')),
						'discart': '',
						'fanart_added': True}
	return fanart_data

def add(db_type, language, remote_id, meta, client_key):
	try:
		if not remote_id: return meta.update(default_fanart_meta)
		fanart_data = get(db_type, language, remote_id, client_key)
		meta['poster2'] = fanart_data['fanarttv_poster']
		meta['fanart2'] = fanart_data['fanarttv_fanart']
		meta['banner'] = fanart_data['banner']
		meta['clearart'] = fanart_data['clearart']
		meta['clearlogo'] = fanart_data['clearlogo']
		meta['landscape'] = fanart_data['landscape']
		meta['discart'] = fanart_data['discart']
		meta['fanart_added'] = fanart_data['fanart_added']
	except: pass
	return meta
