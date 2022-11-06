# -*- coding: utf-8 -*-
from apis.alldebrid_api import AllDebridAPI
from caches.main_cache import main_cache
from modules import kodi_utils
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, normalize
# logger = kodi_utils.logger

json, build_url, make_listitem, sys, ls = kodi_utils.json, kodi_utils.build_url, kodi_utils.make_listitem, kodi_utils.sys, kodi_utils.local_string
default_ad_icon, fanart, fen_clearlogo, set_view_mode = kodi_utils.get_icon('alldebrid'), kodi_utils.addon_fanart, kodi_utils.addon_clearlogo, kodi_utils.set_view_mode
add_items, set_content, end_directory, external_browse = kodi_utils.add_items, kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.external_browse
show_busy_dialog, hide_busy_dialog, show_text = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.show_text
folder_str, file_str, archive_str, down_str = ls(32742).upper(), ls(32743).upper(), ls(32982), ls(32747)
linked_str, addlink_str, clearlink_str = ls(33074).upper(), ls(33078), ls(33079)
extensions = supported_video_extensions()
AllDebrid = AllDebridAPI()

def assigned_content(folder_id):
	try:
		string = 'FEN_AD_%s' % folder_id
		result = main_cache.get(string)
		return result.get('rootname').upper()
	except: return None

def ad_torrent_cloud(folder_id=None):
	def _builder():
		for count, item in enumerate(cloud_dict, 1):
			try:
				cm = []
				cm_append = cm.append
				folder_name, folder_id = item['filename'], item['id']
				clean_folder_name = clean_file_name(normalize(folder_name)).upper()
				linked_folder = assigned_content(folder_id)
				if linked_folder: display = '%02d | [B]%s | [COLOR limegreen]%s | %s[/B][/COLOR] | [I]%s[/I]' % (count, folder_str, linked_str, linked_folder, clean_folder_name)
				else: display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, folder_str, clean_folder_name)
				url_params = {'mode': 'alldebrid.browse_ad_cloud', 'folder': json.dumps(item['links'])}
				link_folders_add = {'mode': 'link_folders_choice', 'service': 'AD', 'folder_id': folder_id, 'action': 'add'}
				link_folders_remove = {'mode': 'link_folders_choice', 'service': 'AD', 'folder_id': folder_id, 'action': 'remove'}
				url = build_url(url_params)
				cm_append((addlink_str,'RunPlugin(%s)' % build_url(link_folders_add)))
				cm_append((clearlink_str,'RunPlugin(%s)' % build_url(link_folders_remove)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_ad_icon, 'poster': default_ad_icon, 'thumb': default_ad_icon, 'fanart': fanart,
								'banner': default_ad_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				yield (url, listitem, True)
			except: pass
	try: cloud_dict = [i for i in AllDebrid.user_cloud()['magnets'] if i['statusCode'] == 4]
	except: cloud_dict = []
	handle = int(sys.argv[1])
	add_items(handle, list(_builder()))
	set_content(handle, 'files')
	end_directory(handle)
	if not external_browse(): set_view_mode('view.premium')

def browse_ad_cloud(folder):
	def _builder():
		for count, item in enumerate(links, 1):
			try:
				cm = []
				url_link = item['link']
				name = clean_file_name(item['filename']).upper()
				size = item['size']
				display_size = float(int(size))/1073741824
				display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_str, display_size, name)
				url_params = {'mode': 'alldebrid.resolve_ad', 'url': url_link, 'play': 'true'}
				down_file_params = {'mode': 'downloader', 'name': name, 'url': url_link, 'action': 'cloud.alldebrid', 'image': default_ad_icon}
				url = build_url(url_params)
				cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_ad_icon, 'poster': default_ad_icon, 'thumb': default_ad_icon, 'fanart': fanart,
								'banner': default_ad_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				yield (url, listitem, False)
			except: pass
	try: links = [i for i in json.loads(folder) if i['filename'].lower().endswith(tuple(extensions))]
	except: links = []
	handle = int(sys.argv[1])
	add_items(handle, list(_builder()))
	set_content(handle, 'files')
	end_directory(handle, False)
	if not external_browse(): set_view_mode('view.premium')

def resolve_ad(params):
	url = params['url']
	resolved_link = AllDebrid.unrestrict_link(url)
	if params.get('play', 'false') != 'true' : return resolved_link
	from modules.player import FenPlayer
	FenPlayer().run(resolved_link, 'video')

def ad_account_info():
	from datetime import datetime
	try:
		show_busy_dialog()
		account_info = AllDebrid.account_info()['user']
		username = account_info['username']
		email = account_info['email']
		status = 'Premium' if account_info['isPremium'] else 'Not Active'
		expires = datetime.fromtimestamp(account_info['premiumUntil'])
		days_remaining = (expires - datetime.today()).days
		body = []
		append = body.append
		append(ls(32755) % username)
		append(ls(32756) % email)
		append(ls(32757) % status)
		append(ls(32750) % expires)
		append(ls(32751) % days_remaining)
		hide_busy_dialog()
		return show_text(ls(32063).upper(), '\n\n'.join(body), font_size='large')
	except: hide_busy_dialog()

