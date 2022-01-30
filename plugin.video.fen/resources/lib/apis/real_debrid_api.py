# -*- coding: utf-8 -*-
import requests
import re
import json
from sys import exit as sysexit
from caches.main_cache import cache_object
from modules.utils import to_utf8
from modules.settings_reader import get_setting, set_setting
from modules.kodi_utils import sleep, confirm_dialog, ok_dialog, monitor, progressDialog, dialog, local_string as ls
from modules.kodi_utils import logger

base_url = 'https://api.real-debrid.com/rest/1.0/'
auth_url = 'https://api.real-debrid.com/oauth/v2/'
device_url = 'device/code?%s'
credentials_url = 'device/credentials?%s'

class RealDebridAPI:
	def __init__(self):
		self.client_ID = get_setting('rd.client_id')
		if self.client_ID == '': self.client_ID = 'X245A4XAIBGVM'
		self.token = get_setting('rd.token')
		self.secret = get_setting('rd.secret')
		self.refresh = get_setting('rd.refresh')
		self.device_code = ''
		self.refresh_retries = 0
		self.auth_timeout = 0
		self.auth_step = 0
		self.timeout = 20.0
		self.break_auth_loop = False

	def auth_loop(self):
		sleep(1000 * self.auth_step)
		url = 'client_id=%s&code=%s' % (self.client_ID, self.device_code)
		url = auth_url + credentials_url % url
		response = json.loads(requests.get(url, timeout=self.timeout).text)
		if 'error' in response:
			return
		try:
			progressDialog.close()
			set_setting('rd.client_id', response['client_id'])
			set_setting('rd.secret', response['client_secret'])
			self.secret = response['client_secret']
			self.client_ID = response['client_id']
		except:
			 ok_dialog(text=ls(32574), top_space=True)
			 self.break_auth_loop = True
		return

	def auth(self):
		self.secret = ''
		self.client_ID = 'X245A4XAIBGVM'
		line = '%s[CR]%s[CR]%s'
		url = 'client_id=%s&new_credentials=yes' % self.client_ID
		url = auth_url + device_url % url
		response = json.loads(requests.get(url, timeout=self.timeout).text)
		progressDialog.create('%s %s' % (ls(32054), ls(32057)), line % ('', '', ''))
		progressDialog.update(-1, line % (ls(32517),ls(32700) % 'https://real-debrid.com/device', ls(32701) % response['user_code']))
		self.auth_timeout = int(response['expires_in'])
		self.auth_step = int(response['interval'])
		self.device_code = response['device_code']

		while self.secret == '':
			if self.break_auth_loop:
				break
			if progressDialog.iscanceled():
				progressDialog.close()
				break
			self.auth_loop()
		self.get_token()

	def get_token(self):
		if self.secret == '': return
		data = {'client_id': self.client_ID, 'client_secret': self.secret, 'code': self.device_code, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
		url = '%stoken' % auth_url
		response = requests.post(url, data=data, timeout=self.timeout).text
		response = json.loads(response)
		self.token = response['access_token']
		self.refresh = response['refresh_token']
		username = self.account_info()['username']
		set_setting('rd.token', self.token)
		set_setting('rd.auth', self.token)
		set_setting('rd.refresh', self.refresh)
		set_setting('rd.username', username)
		ok_dialog(text=32576, top_space=True)

	def refreshToken(self):
		try:
			url = auth_url + 'token'
			data = {'client_id': self.client_ID, 'client_secret': self.secret, 'code': self.refresh, 'grant_type': 'http://oauth.net/grant_type/device/1.0'}
			response = requests.post(url, data=data).json()
			self.token = response['access_token']
			self.refresh = response['refresh_token']
			set_setting('rd.token', self.token)
			set_setting('rd.refresh', self.refresh)
			return True
		except: return False

	def account_info(self):
		url = 'user'
		return self._get(url)

	def check_cache(self, hashes):
		hash_string = '/'.join(hashes)
		url = 'torrents/instantAvailability/%s' % hash_string
		return self._get(url)

	def check_hash(self, hash_string):
		url = 'torrents/instantAvailability/%s' % hash_string
		return self._get(url)

	def check_single_magnet(self, hash_string):
		cache_info = self.check_hash(hash_string)
		cached = False
		if hash_string in cache_info:
			info = cache_info[hash_string]
			if isinstance(info, dict) and len(info.get('rd')) > 0:
				cached = True
		return cached

	def torrents_activeCount(self):
		url = 'torrents/activeCount'
		return self._get(url)

	def user_cloud(self):
		string = 'fen_rd_user_cloud'
		url = 'torrents'
		return cache_object(self._get, string, url, False, 0.5)

	def downloads(self):
		string = 'fen_rd_downloads'
		url = 'downloads'
		return cache_object(self._get, string, url, False, 0.5)

	def user_cloud_info(self, file_id):
		string = 'fen_rd_user_cloud_info_%s' % file_id
		url = 'torrents/info/%s' % file_id
		return cache_object(self._get, string, url, False, 2)

	def torrent_info(self, file_id):
		url = 'torrents/info/%s' % file_id
		return self._get(url)

	def unrestrict_link(self, link):
		url = 'unrestrict/link'
		post_data = {'link': link}
		response = self._post(url, post_data)
		try: return response['download']
		except: return None

	def add_magnet(self, magnet):
		post_data = {'magnet': magnet}
		url = 'torrents/addMagnet'
		return self._post(url, post_data)

	def create_transfer(self, magnet_url):
		from modules.source_utils import supported_video_extensions
		try:
			extensions = supported_video_extensions()
			torrent = self.add_magnet(magnet_url)
			torrent_id = torrent['id']
			info = self.torrent_info(torrent_id)
			files = info['files']
			torrent_keys = [str(item['id']) for item in files if item['path'].lower().endswith(tuple(extensions))]
			torrent_keys = ','.join(torrent_keys)
			self.add_torrent_select(torrent_id, torrent_keys)
			return 'success'
		except:
			self.delete_torrent(torrent_id)
			return 'failed'

	def add_torrent_select(self, torrent_id, file_ids):
		self.clear_cache()
		url = 'torrents/selectFiles/%s' % torrent_id
		post_data = {'files': file_ids}
		return self._post(url, post_data)

	def delete_torrent(self, folder_id):
		if self.token == '': return None
		url = 'torrents/delete/%s&auth_token=%s' % (folder_id, self.token)
		response = requests.delete(base_url + url, timeout=self.timeout)
		return response

	def delete_download(self, download_id):
		if self.token == '': return None
		url = 'downloads/delete/%s&auth_token=%s' % (download_id, self.token)
		response = requests.delete(base_url + url, timeout=self.timeout)
		return response

	def get_hosts(self):
		string = 'fen_rd_valid_hosts'
		url = 'hosts/domains'
		hosts_dict = {'Real-Debrid': []}
		try:
			result = cache_object(self._get, string, url, False, 48)
			hosts_dict['Real-Debrid'] = result
		except: pass
		return hosts_dict

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, extras_filter
		try:
			torrent_id, rd_url, match = None, None, False
			extensions = supported_video_extensions()
			extras_filtering_list = extras_filter()
			torrent_files = self.check_hash(info_hash)
			if not info_hash in torrent_files: return None
			torrent = self.add_magnet(magnet_url)
			torrent_id = torrent['id']
			torrent_files = torrent_files[info_hash]['rd']
			torrent_files = [item for item in torrent_files if self._video_only(item, extensions)]
			if season: episode_title = re.sub(r'[^A-Za-z0-9-]+', '.', title.replace('\'', '').replace('&', 'and').replace('%', '.percent')).lower()
			else:
				m2ts_check = self._m2ts_check(torrent_files)
				if m2ts_check: m2ts_key, torrent_files = self._m2ts_key_value(torrent_files)
				else: torrent_files = self.sort_cache_list([(item, max([i['filesize'] for i in item.values()])) for item in torrent_files])
			for item in torrent_files:
				try:
					if season:
						item_values = [i['filename'] for i in item.values()]
						for value in item_values:
							correct_file_check = seas_ep_filter(season, episode, value)
							if correct_file_check: break
						if not correct_file_check: continue
					elif not m2ts_check:
						item_values = self.sort_cache_list([(i['filename'], i['filesize']) for i in item.values()])
						for value in item_values:
							filename = re.sub(r'[^A-Za-z0-9-]+', '.', value.replace('\'', '').replace('&', 'and').replace('%', '.percent')).lower()
							if any(x in filename for x in extras_filtering_list): continue
							break
					torrent_keys = item.keys()
					if len(torrent_keys) == 0: continue
					torrent_keys = ','.join(torrent_keys)
					self.add_torrent_select(torrent_id, torrent_keys)
					torrent_info = self.user_cloud_info(torrent_id)
					if 'error' in torrent_info: continue
					selected_files = [(idx, i) for idx, i in enumerate([i for i in torrent_info['files'] if i['selected'] == 1])]
					if season:
						correct_files = []
						correct_file_check = False
						for value in selected_files:
							correct_file_check = seas_ep_filter(season, episode, value[1]['path'])
							if correct_file_check:
								correct_files.append(value[1])
								break
						if len(correct_files) == 0: continue
						for i in correct_files:
							compare_link = seas_ep_filter(season, episode, i['path'], split=True)
							compare_link = re.sub(episode_title, '', compare_link)
							if any(x in compare_link for x in extras_filtering_list): continue
							else:
								match = True
								break
						if match:
							index = [i[0] for i in selected_files if i[1]['path'] == correct_files[0]['path']][0]
							break
					elif m2ts_check:
						match, index = True, [i[0] for i in selected_files if i[1]['id'] == m2ts_key][0]
						break
					else:
						match = False
						for value in selected_files:
							filename = re.sub(r'[^A-Za-z0-9-]+', '.', value[1]['path'].rsplit('/', 1)[1].replace('\'', '').replace('&', 'and').replace('%', '.percent')).lower()
							if any(x in filename for x in extras_filtering_list): continue
							match, index = True, value[0]
							break
						if match: break
				except: pass
			if match:
				rd_link = torrent_info['links'][index]
				file_url = self.unrestrict_link(rd_link)
				if file_url.endswith('rar'): file_url = None
				if not any(file_url.lower().endswith(x) for x in extensions): file_url = None
				if not store_to_cloud: self.delete_torrent(torrent_id)
				return file_url
			self.delete_torrent(torrent_id)
		except Exception:
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			video_only_items = []
			list_file_items = []
			append = video_only_items.append
			extensions = supported_video_extensions()
			torrent_files = self.check_hash(info_hash)
			if not info_hash in torrent_files: return None
			torrent = self.add_magnet(magnet_url)
			torrent_id = torrent['id']
			torrent_files = torrent_files[info_hash]['rd']
			torrent_files = [item for item in torrent_files if self._video_only(item, extensions)]
			for item in torrent_files:
				torrent_keys = item.keys()
				if len(torrent_keys) == 0: continue
				append(torrent_keys)
			video_only_items = max(video_only_items, key=len)
			torrent_keys = ','.join(video_only_items)
			self.add_torrent_select(torrent_id, torrent_keys)
			torrent_info = self.user_cloud_info(torrent_id)
			list_file_items = [dict(i, **{'link':torrent_info['links'][idx]})  for idx, i in enumerate([i for i in torrent_info['files'] if i['selected'] == 1])]
			list_file_items = [{'link': i['link'], 'filename': i['path'].replace('/', ''), 'size': i['bytes']} for i in list_file_items]
			self.delete_torrent(torrent_id)
			return list_file_items
		except Exception:
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def _video_only(self, storage_variant, extensions):
		# original from Seren
		return False if len([i for i in storage_variant.values() if not i['filename'].lower().endswith(tuple(extensions))]) > 0 else True

	def _m2ts_check(self, folder_details):
		for item in folder_details:
			if any(i['filename'].endswith('.m2ts') for i in item.values()):
				return True
		return False

	def _m2ts_key_value(self, torrent_files):
		total_max_size, total_min_length = 0, 10000000000
		for item in torrent_files:
			max_filesize, item_length = max([i['filesize'] for i in item.values()]), len(item)
			if max_filesize >= total_max_size:
				if item_length < total_min_length:
					total_max_size, total_min_length = max_filesize, item_length
					dict_item = item
					key = int([k for k,v in iter(item.items()) if v['filesize'] == max_filesize][0])
		return key, [dict_item,]

	def sort_cache_list(self, unsorted_list):
		sorted_list = sorted(unsorted_list, key=lambda x: x[1], reverse=True)
		return [i[0] for i in sorted_list]

	def add_uncached_torrent(self, magnet_url, pack=False):
		from modules.kodi_utils import show_busy_dialog, hide_busy_dialog
		from modules.source_utils import supported_video_extensions
		def _return_failed(message=32574, cancelled=False):
			try: progressDialog.close()
			except Exception: pass
			hide_busy_dialog()
			sleep(500)
			if cancelled:
				if confirm_dialog(text=32044, top_space=True): ok_dialog(heading=32733, text=ls(32732) % ls(32054))
				else: self.delete_torrent(torrent_id)
			else: ok_dialog(heading=32733, text=message)
			return False
		show_busy_dialog()
		try:
			active_count = self.torrents_activeCount()
			if active_count['nb'] >= active_count['limit']:
				return _return_failed()
		except: pass
		interval = 5
		stalled = ('magnet_error', 'error', 'virus', 'dead')
		extensions = supported_video_extensions()
		torrent = self.add_magnet(magnet_url)
		torrent_id = torrent['id']
		if not torrent_id: return _return_failed()
		torrent_info = self.torrent_info(torrent_id)
		if 'error_code' in torrent_info: return _return_failed()
		status = torrent_info['status']
		line = '%s[CR]%s[CR]%s'
		if status == 'magnet_conversion':
			line1 = ls(32737)
			line2 = torrent_info['filename']
			line3 = ls(32738) % torrent_info['seeders']
			timeout = 100
			progressDialog.create(ls(32733), line % (line1, line2, line3))
			while status == 'magnet_conversion' and timeout > 0:
				progressDialog.update(timeout, line % (line1, line2, line3))
				if monitor.abortRequested() == True: return sysexit()
				try:
					if progressDialog.iscanceled():
						return _return_failed(32736, cancelled=True)
				except Exception:
					pass
				timeout -= interval
				sleep(1000 * interval)
				torrent_info = self.torrent_info(torrent_id)
				status = torrent_info['status']
				if any(x in status for x in stalled):
					return _return_failed()
				line3 = ls(32738) % torrent_info['seeders']
			try:
				progressDialog.close()
			except Exception:
				pass
		if status == 'downloaded':
			hide_busy_dialog()
			return True
		if status == 'magnet_conversion':
			return _return_failed()
		if any(x in status for x in stalled):
			return _return_failed(str(status))
		if status == 'waiting_files_selection':
			video_files = []
			append = video_files.append
			all_files = torrent_info['files']
			for item in all_files:
				if any(item['path'].lower().endswith(x) for x in extensions):
					append(item)
			if pack:
				try:
					if len(video_files) == 0: return _return_failed()
					video_files.sort(key=lambda x: x['path'])
					torrent_keys = [str(i['id']) for i in video_files]
					if not torrent_keys: return _return_failed(ls(32736))
					torrent_keys = ','.join(torrent_keys)
					self.add_torrent_select(torrent_id, torrent_keys)
					ok_dialog(text=ls(32732) % ls(32054))
					self.clear_cache()
					hide_busy_dialog()
					return True
				except Exception:
					return _return_failed()
			else:
				try:
					video = max(video_files, key=lambda x: x['bytes'])
					file_id = video['id']
				except ValueError:
					return _return_failed()
				self.add_torrent_select(torrent_id, str(file_id))
			sleep(2000)
			torrent_info = self.torrent_info(torrent_id)
			status = torrent_info['status']
			if status == 'downloaded':
				hide_busy_dialog()
				return True
			file_size = round(float(video['bytes']) / (1000 ** 3), 2)
			line1 = '%s...' % (ls(32732) % ls(32054))
			line2 = torrent_info['filename']
			line3 = status
			progressDialog.create(ls(32733), line % (line1, line2, line3))
			while not status == 'downloaded':
				sleep(1000 * interval)
				torrent_info = self.torrent_info(torrent_id)
				status = torrent_info['status']
				if status == 'downloading':
					line3 = ls(32739) % (file_size, round(float(torrent_info['speed']) / (1000**2), 2), torrent_info['seeders'], torrent_info['progress'])
				else:
					line3 = status
				progressDialog.update(int(float(torrent_info['progress'])), line % (line1, line2, line3))
				if monitor.abortRequested() == True: return sys.exit()
				try:
					if progressDialog.iscanceled(): return _return_failed(32736, cancelled=True)
				except: pass
				if any(x in status for x in stalled): return _return_failed()
			try: progressDialog.close()
			except: pass
			hide_busy_dialog()
			return True
		hide_busy_dialog()
		return False

	def _get(self, url):
		original_url = url
		url = base_url + url
		if self.token == '': return None
		if '?' not in url:
			url += '?auth_token=%s' % self.token
		else:
			url += '&auth_token=%s' % self.token
		response = requests.get(url, timeout=self.timeout).text
		if 'bad_token' in response or 'Bad Request' in response:
			if self.refreshToken():
				response = self._get(original_url)
			else: return None
		try: return to_utf8(json.loads(response))
		except: return to_utf8(response)

	def _post(self, url, post_data):
		original_url = url
		url = base_url + url
		if self.token == '': return None
		if '?' not in url:
			url += '?auth_token=%s' % self.token
		else:
			url += '&auth_token=%s' % self.token
		response = requests.post(url, data=post_data, timeout=self.timeout).text
		if 'bad_token' in response or 'Bad Request' in response:
			if self.refreshToken():
				response = self._post(original_url, post_data)
			else: return None
		try: return to_utf8(json.loads(response))
		except: return to_utf8(response)

	def revoke_auth(self):
		set_setting('rd.auth', '')
		set_setting('rd.client_id', '')
		set_setting('rd.refresh', '')
		set_setting('rd.secret', '')
		set_setting('rd.token', '')
		set_setting('rd.username', '')
		ok_dialog(heading=32054, text='%s %s' % (ls(32059), ls(32576)))

	def clear_cache(self):
		try:
			from modules.kodi_utils import translate_path, clear_property, path_exists
			RD_DATABASE = translate_path('special://profile/addon_data/plugin.video.fen/maincache.db')
			if not path_exists(RD_DATABASE): return True
			import sqlite3 as database
			from caches.debrid_cache import debrid_cache
			user_cloud_success = False
			dbcon = database.connect(RD_DATABASE)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
				dbcur.execute("""SELECT data FROM maincache WHERE id=?""", ('fen_rd_user_cloud',))
				try: 
					user_cloud_cache = eval(dbcur.fetchone()[0])
					user_cloud_info_caches = [i['id'] for i in user_cloud_cache]
				except: user_cloud_success = True
				if not user_cloud_success:
					dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_rd_user_cloud',))
					clear_property("fen_rd_user_cloud")
					for i in user_cloud_info_caches:
						dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_rd_user_cloud_info_%s' % i,))
						clear_property("fen_rd_user_cloud_info_%s" % i)
					dbcon.commit()
					user_cloud_success = True
			except: user_cloud_success = False
			# DOWNLOAD LINKS
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_rd_downloads',))
				clear_property("fen_rd_downloads")
				dbcon.commit()
				download_links_success = True
			except: download_links_success = False
			# HOSTERS
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_rd_valid_hosts',))
				clear_property('fen_rd_valid_hosts')
				dbcon.commit()
				dbcon.close()
				hoster_links_success = True
			except: hoster_links_success = False
			# HASH CACHED STATUS
			try:
				debrid_cache.clear_debrid_results('rd')
				hash_cache_status_success = True
			except: hash_cache_status_success = False
		except: return False
		if False in (user_cloud_success, download_links_success, hoster_links_success, hash_cache_status_success): return False
		return True

