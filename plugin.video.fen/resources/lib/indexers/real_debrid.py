# -*- coding: utf-8 -*-
import re
import urllib
from sys import argv
from html.parser import HTMLParser
from apis.real_debrid_api import RealDebridAPI
from caches.main_cache import main_cache
from modules import kodi_utils
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, clean_title, normalize, jsondate_to_datetime
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
default_rd_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/realdebrid.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')

RealDebrid = RealDebridAPI()

def rd_torrent_cloud():
	def _builder():
		for count, item in enumerate(my_cloud_files, 1):
			try:
				cm = []
				cm_append = cm.append
				folder_name = item['filename']
				normalized_folder_name = normalize(folder_name)
				string = 'FEN_RD_%s' % normalized_folder_name
				link_folders_add = {'mode': 'link_folders', 'service': 'RD', 'folder_name': normalized_folder_name, 'action': 'add'}
				link_folders_remove = {'mode': 'link_folders', 'service': 'RD', 'folder_name': normalized_folder_name, 'action': 'remove'}
				current_link = main_cache.get(string)
				if current_link: ending = '[COLOR=limegreen][B][I]\n      %s[/I][/B][/COLOR]' % (linkedto_str % current_link)
				else: ending = ''
				display = '%02d | [B]%s[/B] | [I]%s [/I]%s' % (count, folder_str, clean_file_name(normalized_folder_name).upper(), ending)
				url_params = {'mode': 'real_debrid.browse_rd_cloud', 'id': item['id']}
				delete_params = {'mode': 'real_debrid.delete', 'id': item['id'], 'cache_type': 'torrent'}
				url = build_url(url_params)
				cm_append(('[B]%s %s[/B]' % (delete_str, folder_str.capitalize()),'RunPlugin(%s)' % build_url(delete_params)))
				cm_append((addlink_str,'RunPlugin(%s)' % build_url(link_folders_add)))
				cm_append((clearlink_str,'RunPlugin(%s)' % build_url(link_folders_remove)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_rd_icon, 'poster': default_rd_icon, 'thumb': default_rd_icon, 'fanart': fanart, 'banner': default_rd_icon})
				yield (url, listitem, True)
			except: pass
	__handle__ = int(argv[1])
	try: my_cloud_files = RealDebrid.user_cloud()
	except: my_cloud_files = None
	if not my_cloud_files: return
	my_cloud_files = [i for i in my_cloud_files if i['status'] == 'downloaded']
	folder_str, linkedto_str, addlink_str, clearlink_str, delete_str = ls(32742).upper(), ls(32744), ls(32745), ls(32746), ls(32785)
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def rd_downloads():
	def _builder():
		for count, item in enumerate(my_downloads, 1):
			try:
				cm = []
				cm_append = cm.append
				datetime_object = jsondate_to_datetime(item['generated'], '%Y-%m-%dT%H:%M:%S.%fZ', remove_time=True)
				filename = item['filename']
				name = clean_file_name(filename).upper()
				size = float(int(item['filesize']))/1073741824
				display = '%02d | %.2f GB | %s  | [I]%s [/I]' % (count, size, datetime_object, name)
				url_link = item['download']
				url_params = {'mode': 'media_play', 'url': url_link, 'media_type': 'video'}
				down_file_params = {'mode': 'downloader', 'name': name, 'url': url_link,
									'action': 'cloud.realdebrid_direct', 'image': default_rd_icon}
				delete_params = {'mode': 'real_debrid.delete', 'id': item['id'], 'cache_type': 'download'}
				cm_append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				cm_append(('[B]%s %s[/B]' % (delete_str, file_str.capitalize()),'RunPlugin(%s)' % build_url(delete_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_rd_icon, 'poster': default_rd_icon, 'thumb': default_rd_icon, 'fanart': fanart, 'banner': default_rd_icon})
				yield (url, listitem, True)
			except: pass
	__handle__ = int(argv[1])
	try: my_downloads = RealDebrid.downloads()
	except: return
	extensions = supported_video_extensions()
	my_downloads = [i for i in my_downloads if i['download'].lower().endswith(tuple(extensions))]
	file_str, down_str, delete_str = ls(32743), ls(32747), ls(32785)
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_rd_cloud(folder_id):
	def _builder():
		for count, item in enumerate(pack_info, 1):
			try:
				cm = []
				name = item['path']
				if name.startswith('/'): name = name.split('/')[-1]
				name = clean_file_name(name).upper()
				url_link = item['url_link']
				if url_link.startswith('/'): url_link = 'http' + url_link
				size = float(int(item['bytes']))/1073741824
				display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_str, size, name)
				url_params = {'mode': 'real_debrid.resolve_rd', 'url': url_link, 'play': 'true'}
				url = build_url(url_params)
				down_file_params = {'mode': 'downloader', 'name': name, 'url': url_link,
									'action': 'cloud.realdebrid', 'image': default_rd_icon}
				cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_rd_icon, 'poster': default_rd_icon, 'thumb': default_rd_icon, 'fanart': fanart, 'banner': default_rd_icon})
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	__handle__ = int(argv[1])
	torrent_files = RealDebrid.user_cloud_info(folder_id)
	extensions = supported_video_extensions()
	file_info = [i for i in torrent_files['files'] if i['path'].lower().endswith(tuple(extensions))]
	file_urls = torrent_files['links']
	for c, i in enumerate(file_info):
		try: i.update({'url_link': file_urls[c]})
		except: pass
	pack_info = sorted(file_info, key=lambda k: k['path'])
	file_str, down_str = ls(32743).upper(), ls(32747)
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def rd_external_browser(magnet, filtering_list):
	try:
		episode_match = False
		torrent_id = None
		torrent_keys = []
		append = torrent_keys.append
		extensions = supported_video_extensions()
		magnet_url = HTMLParser().unescape(magnet)
		r = re.search(r'''magnet:.+?urn:([a-zA-Z0-9]+):([a-zA-Z0-9]+)''', str(magnet), re.I)
		infoHash = r.group(2).lower()
		torrent_files = RealDebrid.check_hash(infoHash)
		torrent_files = torrent_files[infoHash]['rd'][0]
		try: files_tuple = sorted([(k, v['filename'].lower()) for k,v in torrent_files.items() if v['filename'].lower().endswith(tuple(extensions))])
		except: return None
		files_tuple.sort()
		for i in files_tuple:
			if any(x in i[1] for x in filtering_list):
				episode_match = True
			append(i[0])
		if not episode_match: return None
		if not torrent_keys: return None
		torrent_keys = ','.join(torrent_keys)
		torrent = RealDebrid.add_magnet(magnet_url)
		torrent_id = torrent['id']
		RealDebrid.add_torrent_select(torrent_id, torrent_keys)
		torrent_files = RealDebrid.user_cloud_info(torrent_id)
		file_info = [i for i in torrent_files['files'] if i['path'].lower().endswith(tuple(extensions))]
		file_urls = torrent_files['links']
		pack_info = [dict(i.items() + [('url_link', file_urls[c])]) for c, i in enumerate(file_info)]
		pack_info.sort(key=lambda k: k['path'])
		for item in pack_info:
			filename = clean_title(item['path'])
			if any(x in filename for x in filtering_list):
				correct_result = item
				break
		url_link = correct_result['url_link']
		RealDebrid.delete_torrent(torrent_id)
		return resolve_rd({'url': url_link, 'play': 'false'})
	except:
		if torrent_id: RealDebrid.delete_torrent(torrent_id)
		return None

def rd_delete(file_id, cache_type):
	if not kodi_utils.confirm_dialog(): return
	if cache_type == 'torrent': result = RealDebrid.delete_torrent(file_id)
	else: result = RealDebrid.delete_download(file_id) # cache_type: 'download'
	if result.status_code in (401, 403, 404):
		return kodi_utils.notification(32574)
	RealDebrid.clear_cache()
	kodi_utils.execute_builtin('Container.Refresh')

def resolve_rd(params):
	url = params['url']
	resolved_link = RealDebrid.unrestrict_link(url)
	if params.get('play', 'false') != 'true' : return resolved_link
	from modules.player import FenPlayer
	FenPlayer().run(resolved_link, 'video')

def rd_account_info():
	from datetime import datetime
	from modules.utils import datetime_workaround
	try:
		account_info = RealDebrid.account_info()
		expires = datetime_workaround(account_info['expiration'], '%Y-%m-%dT%H:%M:%S.%fZ')
		days_remaining = (expires - datetime.today()).days
		heading = ls(32054).upper()
		body = []
		append = body.append
		append(ls(32758) % account_info['email'])
		append(ls(32755) % account_info['username'])
		append(ls(32757) % account_info['type'].capitalize())
		append(ls(32750) % expires)
		append(ls(32751) % days_remaining)
		append(ls(32759) % account_info['points'])
		return kodi_utils.show_text(heading, '\n\n'.join(body), font_size='large')
	except: pass
