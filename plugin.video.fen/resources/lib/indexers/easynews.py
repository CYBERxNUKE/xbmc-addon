# -*- coding: utf-8 -*-
from apis.easynews_api import import_easynews
from modules import kodi_utils
from modules.utils import clean_file_name
# from modules.kodi_utils import logger

ls, sys, build_url, unquote, urlencode, quote = kodi_utils.local_string, kodi_utils.sys, kodi_utils.build_url, kodi_utils.unquote, kodi_utils.urlencode, kodi_utils.quote
default_easynews_icon, fanart, fen_clearlogo, sleep = kodi_utils.get_icon('easynews'), kodi_utils.addon_fanart, kodi_utils.addon_clearlogo, kodi_utils.sleep
add_items, set_content, end_directory, external_browse = kodi_utils.add_items, kodi_utils.set_content, kodi_utils.end_directory, kodi_utils.external_browse
show_busy_dialog, hide_busy_dialog, show_text, set_view_mode = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.show_text, kodi_utils.set_view_mode
down_str = ls(32747)
EasyNews = import_easynews()

def search_easynews(params):
	handle = int(sys.argv[1])
	search_name = clean_file_name(unquote(params.get('query')))
	try:
		files = EasyNews.search(search_name)
		easynews_file_browser(files, handle)
	except: pass
	set_content(handle, 'files')
	end_directory(handle, False)
	if not external_browse(): set_view_mode('view.premium')

def easynews_file_browser(files, handle):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				cm = []
				item_get = item.get
				name = clean_file_name(item_get('name')).upper()
				url_dl = item_get('url_dl')
				size = str(round(float(int(item_get('rawSize')))/1048576000, 1))
				display = '%02d | [B]%s GB[/B] | [I]%s [/I]' % (count, size, name)
				url_params = {'mode': 'easynews.resolve_easynews', 'url_dl': url_dl, 'play': 'true'}
				url = build_url(url_params)
				down_file_params = {'mode': 'downloader', 'name': item_get('name'), 'url': url_dl, 'action': 'cloud.easynews_direct', 'image': default_easynews_icon}
				cm.append((down_str, 'RunPlugin(%s)' % build_url(down_file_params)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				thumbnail = item.get('thumbnail', default_easynews_icon)
				listitem.setArt({'icon': thumbnail, 'poster': thumbnail, 'thumb': thumbnail, 'fanart': fanart, 'banner': default_easynews_icon, 'clearlogo': fen_clearlogo})
				listitem.setInfo('video', {'plot': ' '})
				yield (url, listitem, False)
			except: pass
	make_listitem = kodi_utils.make_listitem
	add_items(handle, list(_builder()))

def resolve_easynews(params):
	url_dl = params['url_dl']
	resolved_link = EasyNews.resolve_easynews(url_dl)
	if params.get('play', 'false') != 'true' :
		sleep(500)
		return resolved_link
	from modules.player import FenPlayer
	FenPlayer().run(resolved_link, 'video')

def account_info(params):
	from datetime import datetime
	from modules.utils import jsondate_to_datetime
	try:
		show_busy_dialog()
		account_info, usage_info = EasyNews.account()
		if not account_info or not usage_info: return kodi_utils.ok_dialog(text=32574)
		body = []
		append = body.append
		expires = jsondate_to_datetime(account_info[2], '%Y-%m-%d')
		days_remaining = (expires - datetime.today()).days
		append(ls(32758) % account_info[1])
		append(ls(32755) % account_info[0])
		append(ls(32757) % account_info[3])
		append(ls(32750) % expires)
		append(ls(32751) % days_remaining)
		append('%s %s' % (ls(32772), usage_info[2].replace('years', ls(32472))))
		append(ls(32761) % usage_info[0].replace('Gigs', 'GB'))
		append(ls(32762) % usage_info[1].replace('Gigs', 'GB'))
		hide_busy_dialog()
		return show_text(ls(32070).upper(), '\n\n'.join(body), font_size='large')
	except: hide_busy_dialog()
