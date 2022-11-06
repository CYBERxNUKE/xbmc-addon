# -*- coding: utf-8 -*-
from datetime import timedelta
from apis.furk_api import FurkAPI
from caches.main_cache import main_cache
from modules import kodi_utils
from modules.utils import clean_file_name
# logger = kodi_utils.logger

EXPIRES_1_HOUR = timedelta(hours=1)
add_items, set_content, show_text, external_browse, unquote = kodi_utils.add_items, kodi_utils.set_content, kodi_utils.show_text, kodi_utils.external_browse, kodi_utils.unquote
show_busy_dialog, hide_busy_dialog, set_view_mode, end_directory = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.set_view_mode, kodi_utils.end_directory
confirm_dialog, ok_dialog, notification, kodi_refresh = kodi_utils.confirm_dialog, kodi_utils.ok_dialog, kodi_utils.notification, kodi_utils.kodi_refresh
ls, sys, json, build_url, make_listitem = kodi_utils.local_string, kodi_utils.sys, kodi_utils.json, kodi_utils.build_url, kodi_utils.make_listitem
furk_icon, fanart, fen_clearlogo = kodi_utils.get_icon('furk'), kodi_utils.addon_fanart, kodi_utils.addon_clearlogo
remove_str, prot_str, unprot_str, speed_str, files_str, down_str, add_str = ls(32766), ls(32767), ls(32768), ls(32775), ls(32493).upper(), ls(32747), ls(32769)
Furk = FurkAPI()

def my_furk_files(params):
	handle = int(sys.argv[1])
	try:
		files = eval('Furk.%s()' % params.get('list_type'))
		if params.get('list_type') in ('file_get_active', 'file_get_failed'): torrent_status_browser(files) 
		else: furk_file_browser(files, params, 'file_browse', handle)
	except: pass
	set_content(handle, 'files')
	end_directory(handle)
	if not external_browse(): set_view_mode('view.premium')

def torrent_status_browser(files):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				display = '%02d | %s | [COLOR=grey][I]%s | %sGB | %s %% | %s: %s kB/s | (S:%s P:%s)[/I][/COLOR]' \
							% (count, item['name'].replace('magnet:', '').upper(), item['dl_status'].upper(), str(round(float(item['size'])/1048576000, 1)),
								item['have'], speed_str, str(round(float(item['speed'])/1024, 1)), item['seeders'], item['peers'])
				url_params = {'mode': 'furk.remove_from_downloads', 'item_id': item['id']}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': furk_icon, 'poster': furk_icon, 'thumb': furk_icon, 'fanart': fanart, 'banner': furk_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				yield (url, listitem, True)
			except: pass
	handle = int(sys.argv[1])
	add_items(handle, list(_builder()))
	main_cache.set('furk_active_downloads', [i['info_hash'] for i in files], expiration=EXPIRES_1_HOUR)

def search_furk(params):
	handle = int(sys.argv[1])
	search_name = clean_file_name(unquote(params.get('query')))
	try:
		search_method = 'search' if 'accurate_search' in params else 'direct_search'
		files = Furk.direct_search(search_name) if search_method == 'direct_search' else Furk.search(search_name)
		files = [i for i in files if i.get('type') == 'video' and 'url_dl' in i]
		furk_file_browser(files, params, 'search', handle)
	except: pass
	set_content(handle, 'files')
	end_directory(handle, False)
	if not external_browse(): set_view_mode('view.premium')

def furk_tfile_video(params):
	def _builder():
		for count, item in enumerate(t_files, 1):
			try:
				cm = []
				url_params = {'mode': 'media_play', 'url': item['url_dl'], 'obj': 'video'}
				url = build_url(url_params)
				name = clean_file_name(item['name']).upper()
				height = int(item['height'])
				if 1200 < height > 2100: display_res = '4K'
				elif 1000 < height < 1200: display_res = '1080P'
				elif 680 < height < 1000: display_res = '720P'
				else: display_res = 'SD'
				display_name = '%02d | [B]%s[/B] | [B]%.2f GB[/B] | %smbps | [I]%s[/I]' % \
				(count, display_res, float(item['size'])/1048576000, str(round(float(item['bitrate'])/1000, 2)), name)
				listitem = make_listitem()
				listitem.setLabel(display_name)
				down_file_params = {'mode': 'downloader', 'name': item['name'], 'url': item['url_dl'], 'action': 'cloud.furk_direct', 'image': furk_icon}
				cm.append((down_str, 'RunPlugin(%s)' % build_url(down_file_params)))
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': furk_icon, 'poster': furk_icon, 'thumb': furk_icon, 'fanart': fanart, 'banner': furk_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				yield (url, listitem, False)
			except: pass
	handle = int(sys.argv[1])
	t_files = [i for i in Furk.t_files(params.get('item_id')) if 'video' in i['ct'] and 'bitrate' in i]
	add_items(handle, list(_builder()))
	set_content(handle, 'files')
	end_directory(handle, False)
	if not external_browse(): set_view_mode('view.premium')

def furk_file_browser(files, params, display_mode, handle):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				item_get = item.get
				cm = []
				cm_append = cm.append
				name, size, info_hash = clean_file_name(item_get('name')).upper(), item_get('size'), item_get('info_hash')
				item_id, url_dl, files_num_video, is_protected = item_get('id'), item_get('url_dl'), item_get('files_num_video'), item_get('is_protected')
				try: thumb = item_get('ss_urls_tn')[0] or furk_icon
				except: thumb = furk_icon
				display_size = str(round(float(size)/1048576000, 1))
				info_unprotected = '[B] %s GB | %s %s | [/B]' % (display_size, files_num_video, files_str)
				info_protected = '[COLOR=green]%s[/COLOR]' % info_unprotected
				info_search = '%02d | [B]%s GB[/B] | [B]%s %s[/B] |' % (count, display_size, files_num_video, files_str)
				info = info_search if display_mode == 'search' else info_protected if is_protected == '1' else info_unprotected if is_protected == '0' else None
				add_to_files = build_url({'mode': 'furk.add_to_files', 'item_id': item_id})
				remove_files = build_url({'mode': 'furk.remove_from_files', 'item_id': item_id})
				download_archive = build_url({'mode': 'downloader', 'name': name, 'url': url_dl, 'action': 'archive', 'image': furk_icon})
				protect_files = build_url({'mode': 'furk.myfiles_protect_unprotect', 'action': 'protect', 'name': name, 'item_id': item_id})
				unprotect_files = build_url({'mode': 'furk.myfiles_protect_unprotect', 'action': 'unprotect', 'name': name, 'item_id': item_id})
				if display_mode == 'search': cm_append((add_str,'RunPlugin(%s)' % add_to_files))
				cm_append((remove_str, 'RunPlugin(%s)' % remove_files))
				cm_append((down_str, 'RunPlugin(%s)' % download_archive))
				if is_protected == '0': cm_append((prot_str, 'RunPlugin(%s)' % protect_files))
				elif is_protected == '1': cm_append((unprot_str, 'RunPlugin(%s)' % unprotect_files))
				display = '%s [I] %s [/I]' % (info, name)
				url_params = {'mode': 'furk.furk_tfile_video', 'name': name, 'item_id': item_id}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': thumb, 'poster': thumb, 'thumb': thumb, 'fanart': fanart, 'banner': furk_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				yield (url, listitem, True)
			except: pass
	add_items(handle, list(_builder()))

def t_file_browser(item_id, media_type, season, episode):
	from modules.source_utils import seas_ep_filter
	from modules.utils import clean_title, normalize
	t_files = [i for i in Furk.t_files(item_id) if 'video' in i['ct'] and not any(x in i['name'].lower() for x in ('furk320', 'sample'))]
	if media_type == 'movie':
		try: url = [i['url_dl'] for i in t_files if 'is_largest' in i][0]
		except: url = None
	else:
		try: url = [i['url_dl'] for i in t_files if seas_ep_filter(season, episode, normalize(i['name']))][0]
		except: url = None
	return url

def add_to_files(item_id):
	if not confirm_dialog(text=32580): return
	response = Furk.file_link(item_id)
	if Furk.check_status(response): notification(32576, 3500)
	else: notification(32574, 3500)
	return (None, None)

def remove_from_files(item_id):
	if not confirm_dialog(): return
	response = Furk.file_unlink(item_id)
	if Furk.check_status(response):
		notification(32576, 3500)
		kodi_refresh()
	else: notification(32574, 3500)
	return (None, None)

def remove_from_downloads(item_id):
	if not confirm_dialog(): return
	response = Furk.download_unlink(item_id)
	if Furk.check_status(response):
		main_cache.set('furk_active_downloads', None, expiration=EXPIRES_1_HOUR)
		notification(32576, 3500)
	else: notification(32574, 3500)
	return (None, None)

def myfiles_protect_unprotect(action, name, item_id):
	is_protected = '1' if action == 'protect' else '0'
	try:
		response = Furk.file_protect(item_id, is_protected)
		if Furk.check_status(response):
			kodi_refresh()
			return notification(32576)
		else: notification(32574)
	except: return

def add_uncached_file(item_id):
	if not confirm_dialog(): return
	try:
		response = Furk.add_uncached(item_id)
		if Furk.check_status(response):
			main_cache.set('furk_active_downloads', None, expiration=EXPIRES_1_HOUR)
			return ok_dialog(text=32576)
		elif response['status'] == 'error':
			return ok_dialog(text=32574)
	except: return

def account_info(params):
	try:
		show_busy_dialog()
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
		hide_busy_dialog()
		return show_text(heading, '\n\n'.join(body), font_size='large')
	except: hide_busy_dialog()


