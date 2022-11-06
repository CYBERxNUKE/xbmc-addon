# -*- coding: utf-8 -*-
from modules.dom_parser import parseDOM
from modules.kodi_utils import make_session, fanarttv_default_api
# from modules.kodi_utils import logger

# Code snippets from nixgates. Thankyou.
base_url = 'https://webservice.fanart.tv/v3/%s/%s'
blank_image_values = ('00', '', 'None', '')
default_fanart_meta = {'poster2': '', 'fanart2': '', 'clearlogo2': '', 'banner': '', 'clearart': '', 'landscape': '', 'discart': '', 'keyart': '', 'fanart_added': True}
default_fanart_nometa = {'poster2': '', 'fanart2': '', 'clearlogo2': '', 'banner': '', 'clearart': '', 'landscape': '', 'discart': '', 'keyart': '', 'fanart_added': False}
session = make_session('https://webservice.fanart.tv')

def get(media_type, language, media_id, client_key):
	if not media_id: return default_fanart_meta
	query = base_url % (media_type, media_id)
	headers = {'client-key': client_key, 'api-key': fanarttv_default_api}
	try: art = session.get(query, headers=headers, timeout=20.0).json()
	except: art = None
	if art == None or 'error_message' in art: return default_fanart_meta
	art_get = art.get
	if media_type == 'movies':
		fanart_data = {'poster2': parse_art(art_get('movieposter'), language),
						'fanart2': parse_art(art_get('moviebackground'), language),
						'clearlogo2': parse_art(art_get('movielogo', []) + art_get('hdmovielogo', []), language),
						'banner': parse_art(art_get('moviebanner'), language),
						'clearart': parse_art(art_get('movieart', []) + art_get('hdmovieclearart', []), language),
						'landscape': parse_art(art_get('moviethumb'), language),
						'discart': parse_art(art_get('moviedisc'), language),
						'keyart': parse_art(art_get('movieposter'), 'keyart'),
						'fanart_added': True}
	elif media_type == 'tv':
		fanart_data = {'poster2': parse_art(art_get('tvposter'), language),
						'fanart2': parse_art(art_get('showbackground'), language),
						'clearlogo2': parse_art(art_get('hdtvlogo', []) + art_get('clearlogo', []), language),
						'banner': parse_art(art_get('tvbanner'), language),
						'clearart': parse_art(art_get('clearart', []) + art_get('hdclearart', []), language),
						'landscape': parse_art(art_get('tvthumb'), language),
						'discart': '',
						'keyart': '',
						'fanart_added': True}
	return fanart_data

def parse_art(art, language):
	if not art: return ''
	try:
		if language == 'keyart':
			result = [i for i in art if i['lang'] in blank_image_values]
		else:
			result = [i for i in art if i['lang'] == language]
			if not result: result = [i for i in art if i['lang'] in blank_image_values]
			if not result and language != 'en': result = [i for i in art if i['lang'] == 'en']
		result.sort(key=lambda x: int(x['likes']), reverse=True)
		result = result[0]['url']
	except: result = ''
	return result
