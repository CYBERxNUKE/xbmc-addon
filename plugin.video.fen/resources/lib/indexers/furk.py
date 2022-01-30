import json
from sys import argv
from datetime import timedelta
from urllib.parse import unquote
from apis.furk_api import FurkAPI
from caches.main_cache import main_cache
from modules import kodi_utils
from modules.utils import clean_file_name, to_utf8
# from modules.kodi_utils import logger

EXPIRES_1_HOUR = timedelta(hours=1)
ls = kodi_utils.local_string
build_url = kodi_utils.build_url
make_listitem = kodi_utils.make_listitem
default_furk_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/furk.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')
Furk = FurkAPI()
formats = ('.3gp', ''),('.aac', ''),('.flac', ''),('.m4a', ''),('.mp3', ''),('.ogg', ''),('.raw', ''),('.wav', ''),('.wma', ''),('.webm', ''),('.ra', ''),('.rm', '')

def my_furk_files(params):
	__handle__ = int(argv[1])
	try:
		files = eval('Furk.%s()' % params.get('list_type'))
		if params.get('list_type') in ('file_get_active', 'file_get_failed'):
			torrent_status_browser(files) 
		else: furk_file_browser(files, params, 'file_browse', __handle__)
	except: pass
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def torrent_status_browser(files):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				display = '%02d | %s | [COLOR=grey][I]%s | %sGB | %s %% | %s: %s kB/s | (S:%s P:%s)[/I][/COLOR]' \
							% (count, item['name'].replace('magnet:', '').upper(), item['dl_status'].upper(), str(round(float(item['size'])/1048576000, 1)),
								item['have'], ls(32775), str(round(float(item['speed'])/1024, 1)), item['seeders'], item['peers'])
				url_params = {'mode': 'furk.remove_from_downloads', 'item_id': item['id']}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_furk_icon, 'poster': default_furk_icon, 'thumb': default_furk_icon, 'fanart': fanart, 'banner': default_furk_icon})
				yield (url, listitem, True)
			except: pass
	kodi_utils.add_items(__handle__, list(_builder()))
	main_cache.set('furk_active_downloads', [i['info_hash'] for i in files], expiration=EXPIRES_1_HOUR)

def search_furk(params):
	from modules.history import add_to_search_history
	__handle__ = int(argv[1])
	search_title = clean_file_name(params.get('query')) if ('query' in params and params.get('query') != 'NA') else None
	if not search_title: search_title = kodi_utils.dialog.input('Fen')
	try:
		search_name = clean_file_name(unquote(search_title))
		search_method = 'search' if 'accurate_search' in params else 'direct_search'
		search_setting = 'furk_video_queries' if params.get('db_type') == 'video' else 'furk_audio_queries'
		list_type = 'video' if params.get('db_type') == 'video' else 'audio'
		add_to_search_history(search_name, search_setting)
		files = Furk.direct_search(search_name) if search_method == 'direct_search' else Furk.search(search_name)
		if not files: return kodi_utils.ok_dialog(text=32760, top_space=True)
		try: files = [i for i in files if i.get('is_ready', '0') == '1' and i['type'] == list_type]
		except: return kodi_utils.ok_dialog(text=32760, top_space=True)
		furk_file_browser(files, params, 'search', __handle__)
	except: pass
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def furk_tfile_video(params):
	def _builder():
		for count, item in enumerate(t_files, 1):
			try:
				cm = []
				url_params = {'mode': 'media_play', 'url': item['url_dl'], 'media_type': 'video'}
				url = build_url(url_params)
				name = clean_file_name(item['name']).upper()
				height = int(item['height'])
				if 1200 < height > 2100: display_res = '4K'
				elif 1000 < height < 1200: display_res = '1080P'
				elif 680 < height < 1000: display_res = '720P'
				else: display_res = 'SD'
				display_name = '%02d | [B]%s[/B] | [B]%.2f GB[/B] | %smbps | [I]%s[/I]' % \
				(count, display_res, float(item['size'])/1073741824, str(round(float(item['bitrate'])/1000, 2)), name)
				listitem = make_listitem()
				listitem.setLabel(display_name)
				down_file_params = {'mode': 'downloader', 'name': item['name'], 'url': item['url_dl'], 'action': 'cloud.furk_direct', 'image': default_furk_icon}
				cm.append((ls(32747),'RunPlugin(%s)' % build_url(down_file_params)))
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_furk_icon, 'poster': default_furk_icon, 'thumb': default_furk_icon, 'fanart': fanart, 'banner': default_furk_icon})
				yield (url, listitem, False)
			except: pass
	__handle__ = int(argv[1])
	t_files = [i for i in Furk.t_files(params.get('item_id')) if 'video' in i['ct'] and 'bitrate' in i]
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def furk_tfile_audio(params):
	__handle__ = int(argv[1])
	kodi_utils.clear_property('furk_t_files_json')
	excludes = ('', 'cover', 'covers', 'scan', 'scans', 'playlists')
	t_files = Furk.t_files(params.get('item_id'))
	item_path_list = list(set([clean_file_name(i['path']) for i in t_files if clean_file_name(i['path']).lower() not in excludes]))
	item_path_list.sort()
	line = '%s[CR]%s[CR]%s'
	if not item_path_list:
		if kodi_utils.confirm_dialog(text=32763, ok_label=32652, cancel_label=32764, top_space=True):
			return browse_audio_album(t_files, params.get('name'))
		from modules.player import FenPlayer
		FenPlayer().playAudioAlbum(t_files)
		return browse_audio_album(t_files, __handle__)
	def _builder():
		for x in item_path_list:
			try:
				url_params = {'mode': 'furk.browse_audio_album', 'item_path': x, 'handle': __handle__}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(x.upper())
				listitem.setArt({'icon': default_furk_icon, 'poster': default_furk_icon, 'thumb': default_furk_icon, 'fanart': fanart, 'banner': default_furk_icon})
				yield (url, listitem, True)
			except: pass
	t_files_json = json.dumps(t_files)
	kodi_utils.set_property('furk_t_files_json', str(t_files_json))
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_audio_album(t_files, item_path=None):
	def build_list_object():
		try:
			cm = []
			url_params = {'mode': 'media_play', 'url': item['url_dl'], 'media_type': 'music'}
			url = build_url(url_params)
			track_name = clean_file_name(batch_replace(to_utf8(item['name']), formats)).upper()
			listitem = make_listitem()
			listitem.setLabel(track_name)
			down_file_params = {'mode': 'downloader', 'name': item['name'], 'url': item['url_dl'], 'action': 'audio', 'image': default_furk_icon}
			cm.append((ls(32747),'RunPlugin(%s)' % build_url(down_file_params)))
			listitem.addContextMenuItems(cm)
			listitem.setArt({'icon': default_furk_icon, 'poster': default_furk_icon, 'thumb': default_furk_icon, 'fanart': fanart, 'banner': default_furk_icon})
			kodi_utils.add_item(__handle__, url, listitem, True)
		except: pass
	from modules.utils import batch_replace
	__handle__ = int(argv[1])
	seperate = False
	if not t_files:
		seperate = True
		t_fs = kodi_utils.get_property('furk_t_files_json')
		t_files = json.loads(t_fs)
	t_files = [i for i in t_files if 'audio' in i['ct']]
	line = '%s[CR]%s[CR]%s'
	if seperate:
		if kodi_utils.confirm_dialog(text=32763, ok_label=32838, cancel_label=32764, top_space=True):
			for item in t_files:
				t_path = clean_file_name(item['path'])
				if t_path == item_path:
					build_list_object()
			kodi_utils.set_content(__handle__, 'files')
			kodi_utils.end_directory(__handle__)
			kodi_utils.set_view_mode('view.premium')
		else:
			from modules.player import FenPlayer
			FenPlayer().playAudioAlbum(t_files, from_seperate=True)
	else:
		for item in t_files:
			build_list_object()
		kodi_utils.set_content(__handle__, 'files')
		kodi_utils.end_directory(__handle__)
		kodi_utils.set_view_mode('view.premium')

def furk_file_browser(files, params, display_mode, __handle__):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				uncached = True if not 'url_dl' in item else False
				if uncached:
					active_downloads = get_active_downloads()
					mode = 'furk.add_uncached_file'
					if item['info_hash'] in active_downloads: info = '%02d | [COLOR=green][B]%s[/B][/COLOR] |' % (count, active_str)
					else: info = '%02d | [COLOR=red][B]%s[/B][/COLOR] |' % (count, uncached_str)
				else: mode = orig_mode
				name = clean_file_name(item['name']).upper()
				item_id = item['id'] if not uncached else item['info_hash']
				url_dl = item['url_dl'] if not uncached else item['info_hash']
				size = item['size']
				if not uncached:
					is_protected = item.get('is_protected')
					display_size = str(round(float(size)/1048576000, 1))
					info_unprotected = '[B] %s GB | %s %s | [/B]' % (display_size, item[files_num], files_str)
					info_protected = '[COLOR=green]%s[/COLOR]' % info_unprotected
					info_search = '%02d | [B]%s GB[/B] | [B]%s %s[/B] |' % (count, display_size, item[files_num], files_str)
					info = info_search if display_mode == 'search' else info_protected if is_protected == '1' else info_unprotected if is_protected == '0' else None
				display = '%s [I] %s [/I]' % (info, name)
				url_params = {'mode': mode, 'name': name, 'item_id': item_id}
				url = build_url(url_params)
				cm = []
				cm_append = cm.append
				if not uncached:
					con_download_archive = {'mode': 'downloader', 'name': item.get('name'), 'url': url_dl, 'action': 'archive', 'image': default_furk_icon}
					con_remove_files = {'mode': 'furk.remove_from_files', 'item_id': item_id}
					con_protect_files = {'mode': 'furk.myfiles_protect_unprotect', 'action': 'protect', 'name': name, 'item_id': item_id}
					con_unprotect_files = {'mode': 'furk.myfiles_protect_unprotect', 'action': 'unprotect', 'name': name, 'item_id': item_id}
					con_add_to_files = {'mode': 'furk.add_to_files', 'item_id': item_id}
					if display_mode == 'search': cm_append((add_str,'RunPlugin(%s)' % build_url(con_add_to_files)))
					cm_append((down_str,'RunPlugin(%s)' % build_url(con_download_archive)))
					cm_append((remove_str,'RunPlugin(%s)' % build_url(con_remove_files)))
					if is_protected == '0': cm_append((prot_str,'RunPlugin(%s)' % build_url(con_protect_files)))
					if is_protected == '1': cm_append((unprot_str,'RunPlugin(%s)' % build_url(con_unprotect_files)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_furk_icon, 'poster': default_furk_icon, 'thumb': default_furk_icon, 'fanart': fanart, 'banner': default_furk_icon})
				yield (url, listitem, True)
			except: pass
	is_video = params.get('list_type') == 'file_get_video' or params.get('db_type') == 'video'
	files_num = 'files_num_video' if is_video else 'files_num_audio'
	orig_mode = 'furk.furk_tfile_video' if is_video else 'furk.furk_tfile_audio'
	active_str, uncached_str, files_str, down_str, add_str = ls(32489).upper(), ls(32765).upper(), ls(32493).upper(), ls(32747), ls(32769)
	remove_str, prot_str, unprot_str = ls(32766), ls(32767), ls(32768)
	kodi_utils.add_items(__handle__, list(_builder()))

def t_file_browser(item_id, filtering_list=None, source=None):
	t_files = [i for i in Furk.t_files(item_id) if 'video' in i['ct']]
	name, url_dl, size = filter_furk_tlist(t_files, filtering_list)
	return [{'name': name, 'url_dl': url_dl, 'size': size}]

def filter_furk_tlist(t_files, filtering_list=None):
	from modules.utils import clean_title, normalize
	t_files = [i for i in t_files if 'video' in i['ct'] and any(x in clean_title(normalize(i['name'])) for x in filtering_list) \
				and not any(x in i['name'].lower() for x in ['furk320', 'sample'])][0] if filtering_list else [i for i in t_files if 'is_largest' in i][0]
	return t_files['name'], t_files['url_dl'], t_files['size']

def add_to_files(item_id):
	if not kodi_utils.confirm_dialog(text=32580, top_space=True): return
	response = Furk.file_link(item_id)
	if Furk.check_status(response): kodi_utils.notification(32576, 3500)
	else: kodi_utils.notification(32574, 3500)
	return (None, None)

def remove_from_files(item_id):
	if not kodi_utils.confirm_dialog(): return
	response = Furk.file_unlink(item_id)
	if Furk.check_status(response):
		kodi_utils.notification(32576, 3500)
		kodi_utils.execute_builtin('Container.Refresh')
	else:
		kodi_utils.notification(32574, 3500)
	return (None, None)

def remove_from_downloads(item_id):
	if not kodi_utils.confirm_dialog(): return
	response = Furk.download_unlink(item_id)
	if Furk.check_status(response):
		main_cache.set('furk_active_downloads', None, expiration=EXPIRES_1_HOUR)
		kodi_utils.notification(32576, 3500)
	else:
		kodi_utils.notification(32574, 3500)
	return (None, None)

def myfiles_protect_unprotect(action, name, item_id):
	is_protected = '1' if action == 'protect' else '0'
	try:
		response = Furk.file_protect(item_id, is_protected)
		if Furk.check_status(response):
			kodi_utils.execute_builtin('Container.Refresh')
			return kodi_utils.notification(32576)
		else:
			kodi_utils.notification(32574)
	except: return

def get_active_downloads():
	cache = main_cache.get('furk_active_downloads')
	if cache != None: result = cache
	else:
		active_downloads = Furk.file_get_active()
		result = [i['info_hash'] for i in active_downloads]
		main_cache.set('furk_active_downloads', result, expiration=EXPIRES_1_HOUR)
	return result

def add_uncached_file(item_id):
	if not kodi_utils.confirm_dialog(): return
	try:
		response = Furk.add_uncached(item_id)
		if Furk.check_status(response):
			main_cache.set('furk_active_downloads', None, expiration=EXPIRES_1_HOUR)
			return kodi_utils.ok_dialog(text=32576, top_space=True)
		elif response['status'] == 'error':
			return kodi_utils.ok_dialog(text=32574, top_space=True)
	except: return

def account_info(params):
	try:
		accinfo = Furk.account_info()
		account_type = accinfo['premium']['name']
		month_time_left = float(accinfo['premium']['bw_month_time_left'])/60/60/24
		try: total_time_left = float(accinfo['premium']['time_left'])/60/60/24
		except: total_time_left = ''
		try: renewal_date = accinfo['premium']['to_dt']
		except: renewal_date = ''
		try: is_not_last_month = accinfo['premium']['is_not_last_month']
		except: is_not_last_month = ''
		try: bw_used_month = float(accinfo['premium']['bw_used_month'])/1073741824
		except: bw_used_month = ''
		try: bw_limit_month = float(accinfo['premium']['bw_limit_month'])/1073741824
		except: bw_limit_month = ''
		try: rem_bw_limit_month = bw_limit_month - bw_used_month
		except: rem_bw_limit_month = ''
		heading = ls(32069).upper()
		body = []
		append = body.append
		append(ls(32758) % account_type.upper())
		append(ls(32770) % str(round(bw_limit_month, 0)))
		append(ls(32771))
		append('        - %s' % ls(32751) % str(round(month_time_left, 2)))
		append('        - %s GB' % ls(32761) % str(round(bw_used_month, 2)))
		append('        - %s GB' % ls(32762) % str(round(rem_bw_limit_month, 2)))
		if not account_type == 'LIFETIME':
			append(ls(32772))
			append('[B]        - %s' % ls(32751) % str(round(total_time_left, 0)))
			if is_not_last_month == '1': append('        - %s' % ls(32773) % renewal_date)
			else: append('        - %s' % ls(32774) % renewal_date)
		return kodi_utils.show_text(heading, '\n\n'.join(body), font_size='large')
	except: pass


