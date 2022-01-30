# -*- coding: utf-8 -*-
import requests
from caches.main_cache import cache_object
from modules.settings_reader import get_setting, set_setting
# from modules.kodi_utils import logger

base_url = 'https://www.furk.net/api/'
login_url = 'login/login?login=%s&pwd=%s'
file_get_video_url = 'file/get?api_key=%s&type=video'
file_get_audio_url = 'file/get?api_key=%s&type=audio'
file_link_url = 'file/link?api_key=%s&id=%s'
file_unlink_url = 'file/unlink?api_key=%s&id=%s'
file_protect_url = 'file/protect?api_key=%s&id=%s&is_protected=%s'
tfile_url = 'file/get?api_key=%s&t_files=1&id=%s'
add_uncached_url = 'dl/add?api_key=%s&info_hash=%s'
active_dl_url = 'dl/get?api_key=%s&dl_status=active'
failed_dl_url = 'dl/get?api_key=%s&dl_status=failed'
remove_dl_url = 'dl/unlink?api_key=%s&id=%s'
account_info_url = 'account/info?api_key=%s'
search_url = 'plugins/metasearch?api_key=%s&q=%s&cached=all' \
						'&match=%s&moderated=%s%s&sort=relevance&type=video&offset=0&limit=200'
search_direct_url = 'plugins/metasearch?api_key=%s&q=%s&cached=all' \
						'&sort=cached&type=video&offset=0&limit=200'

class FurkAPI:
	def __init__(self):
		self.timeout = 20.0
		self.api_key = self.get_api()
		if not self.api_key: return

	def check_status(self, result):
		return result.get('status', 'not_ok') == 'ok'

	def get_api(self):
		try:
			api_key = get_setting('furk_api_key')
			if not api_key:
				user_name, user_pass = get_setting('furk_login'), get_setting('furk_password')
				if not user_name or not user_pass: return
				url = base_url + login_url % (user_name, user_pass)
				result = requests.post(url, timeout=self.timeout)
				result = p.json()
				if self.check_status(result):
					from modules.kodi_utils import ext_addon
					api_key = result['api_key']
					set_setting('furk_api_key', api_key)
					ext_addon('script.module.myaccounts').setSetting('furk.api.key', api_key)
				else: pass
			return api_key
		except: pass

	def search(self, query):
		try:
			if '@files' in query:
				search_in = ''
				mod_level = 'no'
			else:
				search_in = '&attrs=name'
				mod_setting = int(get_setting('furk.mod.level', '0'))
				mod_level = 'no' if mod_setting == 0 else 'yes' if mod_setting == 1 else 'full'
			url = base_url + search_url % (self.api_key, query, 'extended', mod_level, search_in)
			string = 'fen_FURK_SEARCH_%s' % url
			return cache_object(self._process_files, string, url, json=False, expiration=48)
		except: return

	def direct_search(self, query):
		try:
			url = base_url + search_direct_url % (self.api_key, query)
			string = 'fen_FURK_SEARCH_DIRECT_%s' % url
			return cache_object(self._process_files, string, url, json=False, expiration=48)
		except: return

	def t_files(self, file_id):
		try:
			url = base_url + tfile_url % (self.api_key, file_id)
			string = 'fen_%s_%s' % ('FURK_T_FILE', file_id)
			return cache_object(self._process_tfiles, string, url, json=False, expiration=168)
		except: return

	def file_get_video(self):
		try:
			url = base_url + file_get_video_url % self.api_key
			return self._get(url)['files']
		except: return

	def file_get_audio(self):
		try:
			url = base_url + file_get_audio_url % self.api_key
			return self._get(url)['files']
		except: return

	def file_get_active(self):
		try:
			url = base_url + active_dl_url % self.api_key
			return self._get(url)['torrents']
		except: return

	def file_get_failed(self):
		try:
			url = base_url + failed_dl_url % self.api_key
			return self._get(url)['torrents']
			return files
		except: return

	def file_link(self, item_id):
		try:
			url = base_url + file_link_url % (self.api_key, item_id)
			return self._get(url)
		except: return

	def file_unlink(self, item_id):
		try:
			url = base_url + file_unlink_url % (self.api_key, item_id)
			return self._get(url)
		except: return

	def download_unlink(self, item_id):
		try:
			url = base_url + remove_dl_url % (self.api_key, item_id)
			return self._get(url)
		except: return

	def file_protect(self, item_id, is_protected):
		try:
			url = base_url + file_protect_url % (self.api_key, item_id, is_protected)
			return self._get(url)
		except: return

	def add_uncached(self, item_id):
		try:
			url = base_url + add_uncached_url % (self.api_key, item_id)
			return self._get(url)
		except: return

	def account_info(self):
		try:
			url = base_url + account_info_url % self.api_key
			return self._get(url)
		except: return

	def _process_files(self, url):
		result = self._get(url)
		if not self.check_status(result): return None
		return result['files']

	def _process_tfiles(self, url):
		result = self._get(url)
		if not self.check_status(result) or result['found_files'] != '1': return None
		return result['files'][0]['t_files']

	def _get(self, url):
		result = requests.get(url, timeout=self.timeout)
		return result.json()

def clear_media_results_database():
	import sqlite3 as database
	from modules.kodi_utils import translate_path, clear_property
	FURK_DATABASE = translate_path('special://profile/addon_data/plugin.video.fen/maincache.db')
	dbcon = database.connect(FURK_DATABASE)
	dbcur = dbcon.cursor()
	dbcur.execute("SELECT id FROM maincache WHERE id LIKE 'fen_FURK_SEARCH_%'")
	try:
		furk_results = [str(i[0]) for i in dbcur.fetchall()]
		if not furk_results: return 'success'
		dbcur.execute("DELETE FROM maincache WHERE id LIKE 'fen_FURK_SEARCH_%'")
		dbcon.commit()
		for i in furk_results: clear_property(i)
		return 'success'
	except: return 'failed'
