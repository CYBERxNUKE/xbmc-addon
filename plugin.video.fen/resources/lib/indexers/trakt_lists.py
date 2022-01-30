# -*- coding: utf-8 -*-
from sys import argv
from apis import trakt_api
from threading import Thread
from indexers.movies import Movies
from indexers.tvshows import TVShows
from modules import kodi_utils
from modules.nav_utils import paginate_list
from modules.utils import make_thread_list_enumerate
from modules.settings import paginate, page_limit
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
trakt_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/trakt.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')

def search_trakt_lists(params):
	def _builder():
		for item in lists:
			try:
				list_key = item['type']
				if list_key == 'officiallist': continue
				list_info = item[list_key]
				name = list_info['name']
				user = list_info['username']
				slug = list_info['ids']['slug']
				item_count = list_info['item_count']
				if list_info['privacy'] == 'private' or item_count == 0: continue
				cm = []
				cm_append = cm.append
				url_params = {'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug}
				trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				like_list_url = {'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug}
				unlike_list_url = {'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug}
				url = build_url(url_params)
				cm_append((ls(32730),'RunPlugin(%s)' % build_url(trakt_selection_url)))
				cm_append((ls(32731),'RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
				cm_append((ls(32776),'RunPlugin(%s)' % build_url(like_list_url)))
				cm_append((ls(32783),'RunPlugin(%s)' % build_url(unlike_list_url)))
				display = '[B]%s[/B] | [I]%s (x%s)[/I]' % (name.upper(), user, str(item_count))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	__handle__ = int(argv[1])
	mode = params.get('mode')
	page = params.get('new_page', '1')
	search_title = params.get('search_title', None) or kodi_utils.dialog.input('Fen')
	if not search_title: return
	lists, pages = trakt_api.trakt_search_lists(search_title, page)
	kodi_utils.add_items(__handle__, list(_builder()))
	if pages > page: kodi_utils.add_dir({'mode': mode, 'search_title': search_title, 'new_page': str(int(page) + 1)}, ls(32799), __handle__, iconImage='item_next.png')
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def get_trakt_lists(params):
	def _process_my_lists():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				name = item['name']
				user = item['user']['ids']['slug']
				slug = item['ids']['slug']
				item_count = item.get('item_count', None)
				if item_count: display_name = '%s (x%s)' % (name, item_count)
				else: display_name = name
				url_params = {'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'list_type': list_type}
				trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				make_new_list_url = {'mode': 'trakt.make_new_trakt_list'}
				delete_list_url = {'mode': 'trakt.delete_trakt_list', 'user': user, 'list_slug': slug}
				url = build_url(url_params)
				cm_append((ls(32730),'RunPlugin(%s)' % build_url(trakt_selection_url)))
				cm_append((ls(32731),'RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
				cm_append((ls(32780),'RunPlugin(%s)' % build_url(make_new_list_url)))
				cm_append((ls(32781),'RunPlugin(%s)' % build_url(delete_list_url)))
				listitem = make_listitem()
				listitem.setLabel(display_name)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	def _process_liked_lists():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				_item = item['list']
				name = _item['name']
				user = _item['user']['ids']['slug']
				slug = _item['ids']['slug']
				item_count = _item.get('item_count', None)
				if item_count: display_name = '%s (x%s) - [I]%s[/I]' % (name, item_count, user)
				else: display_name = '%s - [I]%s[/I]' % (name, user)
				url_params = {'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'list_type': list_type}
				trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				unlike_list_url = {'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display_name)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				cm_append((ls(32730),'RunPlugin(%s)' % build_url(trakt_selection_url)))
				cm_append((ls(32731),'RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
				cm_append((ls(32783),'RunPlugin(%s)' % build_url(unlike_list_url)))
				listitem.addContextMenuItems(cm, replaceItems=False)
				yield (url, listitem, True)
			except: pass
	try:
		__handle__ = int(argv[1])
		list_type = params['list_type']
		lists = trakt_api.trakt_get_lists(list_type)
		if list_type == 'my_lists': _process = _process_my_lists
		elif list_type == 'liked_lists': _process = _process_liked_lists
		kodi_utils.add_items(__handle__, list(_process()))
		kodi_utils.set_content(__handle__, 'files')
		kodi_utils.set_sort_method(__handle__, 'label')
		kodi_utils.end_directory(__handle__)
		kodi_utils.set_view_mode('view.main')
	except: pass

def get_trakt_trending_popular_lists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				_item = item['list']
				name = _item['name']
				user = _item['user']['ids']['slug']
				slug = _item['ids']['slug']
				item_count = _item.get('item_count', None)
				if item_count: display_name = '%s (x%s) - [I] %s[/I]' % (name, item_count, user)
				else: display_name = '%s - [I] %s[/I]' % (name, user)
				url_params = {'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'list_type': 'user_lists'}
				trakt_selection_url = {'mode': 'navigator.adjust_main_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				trakt_folder_selection_url = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt_external', 'name': name, 'user': user, 'slug': slug}
				like_list_url = {'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug}
				unlike_list_url = {'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display_name)
				listitem.setArt({'icon': trakt_icon, 'poster': trakt_icon, 'thumb': trakt_icon, 'fanart': fanart, 'banner': trakt_icon})
				cm_append((ls(32730),'RunPlugin(%s)' % build_url(trakt_selection_url)))
				cm_append((ls(32731),'RunPlugin(%s)' % build_url(trakt_folder_selection_url)))
				cm_append((ls(32776),'RunPlugin(%s)' % build_url(like_list_url)))
				cm_append((ls(32783),'RunPlugin(%s)' % build_url(unlike_list_url)))
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	__handle__ = int(argv[1])
	list_type = params['list_type']
	lists = trakt_api.trakt_trending_popular_lists(list_type)
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def build_trakt_list(params):
	def _process_ids(item_position, item):
		item['media_id'] = trakt_api.get_trakt_movie_id(item['media_ids']) if item['media_type'] == 'movie' else trakt_api.get_trakt_tvshow_id(item['media_ids'])
		final_append((item_position, item))
	def _add_misc_dir(url_params, list_name=ls(32799), iconImage='item_next.png', isFolder=True):
		icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/%s' % iconImage)
		listitem = make_listitem()
		listitem.setLabel(list_name)
		listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
		if url_params['mode'] == 'build_navigate_to_page':
			listitem.setProperty('SpecialSort', 'top')
			listitem.addContextMenuItems([(ls(32784),'RunPlugin(%s)' % build_url({'mode': 'toggle_jump_to'}))])
		else:
			listitem.setProperty('SpecialSort', 'bottom')
		kodi_utils.add_item(__handle__, build_url(url_params), listitem, isFolder)
	__handle__ = int(argv[1])
	is_widget = kodi_utils.external_browse()
	user, slug, list_type = params.get('user'), params.get('slug'), params.get('list_type')
	letter, page_no = params.get('new_letter', 'None'), int(params.get('new_page', '1'))
	original_list, final_list, final_listitems = [], [], []
	original_append, final_append = original_list.append, final_list.append
	result = trakt_api.get_trakt_list_contents(list_type, user, slug)
	for item in result:
		try:
			media_type = item['type']
			if not media_type in ('movie', 'show'): continue
			original_append({'media_type': media_type, 'title': item[media_type]['title'], 'media_ids': item[media_type]['ids']})
		except: pass
	if paginate():
		limit = page_limit()
		trakt_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else:
		trakt_list, total_pages = original_list, 1
	threads = list(make_thread_list_enumerate(_process_ids, trakt_list, Thread))
	[i.join() for i in threads]
	final_list.sort(key=lambda k: k[0])
	final_list = [i[1] for i in final_list]
	movie_list = [(i['media_id'], final_list.index(i), 'movie') for i in final_list if i['media_type'] == 'movie']
	tvshow_list = [(i['media_id'], final_list.index(i), 'tvshow') for i in final_list if i['media_type'] == 'show']
	content = 'movies' if len(movie_list) > len(tvshow_list) else 'tvshows'
	if total_pages > 2 and not is_widget:
		_add_misc_dir({'mode': 'build_navigate_to_page', 'db_type': 'Media', 'user': user, 'slug': slug, 'current_page': page_no, 'total_pages': total_pages,
						'transfer_mode': 'trakt.list.build_trakt_list'}, ls(32964), 'item_jump.png', False)
	if len(movie_list) > 0:
		movie_listitems = Movies({'list': [i[0] for i in movie_list]}).worker()
		final_listitems.extend([(i, x[1]) for i in movie_listitems for x in movie_list if [str(x[0]) == i[1].getUniqueID('tmdb') and x[2] == 'movie'][0]])
	if len(tvshow_list) > 0:
		tvshow_listitems = TVShows({'list': [i[0] for i in tvshow_list]}).worker()
		final_listitems.extend([(i, x[1]) for i in tvshow_listitems for x in tvshow_list if [str(x[0]) == i[1].getUniqueID('tmdb') and x[2] == 'tvshow'][0]])
	final_listitems.sort(key=lambda k: k[1])
	item_list = [i[0] for i in final_listitems]
	kodi_utils.add_items(__handle__, item_list)
	if total_pages > page_no: _add_misc_dir({'mode': 'trakt.list.build_trakt_list', 'user': user, 'slug': slug, 'new_page': str(page_no + 1), 'new_letter': letter})
	kodi_utils.set_content(__handle__, content)
	kodi_utils.end_directory(__handle__)
	if params.get('refreshed'): kodi_utils.sleep(1500)
	kodi_utils.set_view_mode('view.trakt_list', content)
