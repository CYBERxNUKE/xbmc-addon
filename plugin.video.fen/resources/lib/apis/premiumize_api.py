# -*- coding: utf-8 -*-
import re
import time
from sys import exit as sysexit
from modules import kodi_utils
from caches.main_cache import cache_object
# logger = kodi_utils.logger

monitor, progress_dialog, dialog, urlencode, get_icon = kodi_utils.monitor, kodi_utils.progress_dialog, kodi_utils.dialog, kodi_utils.urlencode, kodi_utils.get_icon
make_requests, json, sleep, confirm_dialog, ok_dialog = kodi_utils.make_requests, kodi_utils.json, kodi_utils.sleep, kodi_utils.confirm_dialog, kodi_utils.ok_dialog
ls, notification, get_setting, set_setting = kodi_utils.local_string, kodi_utils.notification, kodi_utils.get_setting, kodi_utils.set_setting
set_temp_highlight, restore_highlight, make_settings_dict = kodi_utils.set_temp_highlight, kodi_utils.restore_highlight, kodi_utils.make_settings_dict
pause_settings_change, unpause_settings_change = kodi_utils.pause_settings_change, kodi_utils.unpause_settings_change

base_url = 'https://www.premiumize.me/api/'
timeout = 20.0
requests = make_requests()
icon = get_icon('premiumize')

class PremiumizeAPI:
	def __init__(self):
		self.client_id = '663882072'
		self.user_agent = 'Fen for Kodi'
		self.token = get_setting('pm.token')

	def auth(self):
		pause_settings_change()
		self.token = ''
		line = '%s[CR]%s[CR]%s'
		data = {'response_type': 'device_code', 'client_id': self.client_id}
		url = 'https://www.premiumize.me/token'
		response = self._post(url, data)
		content = line % (ls(32517), ls(32700) % response.get('verification_uri'), ls(32701) % '[COLOR orangered]%s[/COLOR]' % response.get('user_code'))
		current_highlight = set_temp_highlight('orangered')
		progressDialog = progress_dialog('%s %s' % (ls(32061), ls(32057)), icon)
		progressDialog.update(content, 0)
		device_code = response['device_code']
		expires_in = int(response['expires_in'])
		sleep_interval = int(response['interval'])
		poll_url = 'https://www.premiumize.me/token'
		data = {'grant_type': 'device_code', 'client_id': self.client_id, 'code': device_code}
		start, time_passed = time.time(), 0
		while not progressDialog.iscanceled() and time_passed < expires_in and not self.token:
			sleep(1000 * sleep_interval)
			response = self._post(poll_url, data)
			if 'error' in response:
				time_passed = time.time() - start
				progress = int(100 * time_passed/float(expires_in))
				progressDialog.update(content, progress)
				continue
			try:
				progressDialog.close()
				self.token = str(response['access_token'])
				set_setting('pm.token', self.token)
			except:
				 ok_dialog(text=32574)
				 break
		try: progressDialog.close()
		except: pass
		restore_highlight(current_highlight)
		if self.token:
			account_info = self.account_info()
			set_setting('pm.account_id', str(account_info['customer_id']))
			set_setting('pm.enabled', 'true')
			ok_dialog(text=32576)
		unpause_settings_change()
		make_settings_dict()

	def revoke(self):
		pause_settings_change()
		set_setting('pm.token', '')
		set_setting('pm.account_id', '')
		set_setting('pm.enabled', 'false')
		unpause_settings_change()
		make_settings_dict()
		notification('Premiumize Authorization Reset', 3000)

	def account_info(self):
		url = 'account/info'
		response = self._post(url)
		return response

	def check_cache(self, hashes):
		url = 'cache/check'
		data = {'items[]': hashes}
		response = self._post(url, data)
		return response

	def check_single_magnet(self, hash_string):
		cache_info = self.check_cache(hash_string)['response']
		return cache_info[0]

	def zip_folder(self, folder_id):
		url = 'zip/generate'
		data = {'folders[]': folder_id}
		response = self._post(url, data)
		return response

	def unrestrict_link(self, link):
		data = {'src': link}
		url = 'transfer/directdl'
		response = self._post(url, data)
		try: return self.add_headers_to_url(response['content'][0]['link'])
		except: return None

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, EXTRAS
		try:
			file_url = None
			correct_files = []
			append = correct_files.append
			extensions = supported_video_extensions()
			result = self.instant_transfer(magnet_url)
			if not 'status' in result or result['status'] != 'success': return None
			valid_results = [i for i in result.get('content') if any(i.get('path').lower().endswith(x) for x in extensions) and not i.get('link', '') == '']
			if len(valid_results) == 0: return
			if season:
				episode_title = re.sub(r'[^A-Za-z0-9-]+', '.', title.replace('\'', '').replace('&', 'and').replace('%', '.percent')).lower()
				for item in valid_results:
					if seas_ep_filter(season, episode, item['path'].split('/')[-1]): append(item)
					if len(correct_files) == 0: continue
					for i in correct_files:
						compare_link = seas_ep_filter(season, episode, i['path'], split=True)
						compare_link = re.sub(episode_title, '', compare_link)
						if not any(x in compare_link for x in EXTRAS):
							file_url = i['link']
							break
			else:
				file_url = max(valid_results, key=lambda x: int(x.get('size'))).get('link', None)
				if not any(file_url.lower().endswith(x) for x in extensions): file_url = None
			if file_url:
				if store_to_cloud: self.create_transfer(magnet_url)
				return self.add_headers_to_url(file_url)
		except: return None

	def download_link_magnet_zip(self, magnet_url, info_hash):
		try:
			result = self.create_transfer(magnet_url)
			if not 'status' in result or result['status'] != 'success': return None
			transfer_id = result['id']
			transfers = self.transfers_list()['transfers']
			folder_id = [i['folder_id'] for i in transfers if i['id'] == transfer_id][0]
			result = self.zip_folder(folder_id)
			if result['status'] == 'success':
				return result['location']
			else: return None
		except:
			pass

	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			end_results = []
			append = end_results.append
			extensions = supported_video_extensions()
			result = self.instant_transfer(magnet_url)
			if not 'status' in result or result['status'] != 'success': return None
			for item in result.get('content'):
				if any(item.get('path').lower().endswith(x) for x in extensions) and not item.get('link', '') == '':
					try: path = item['path'].split('/')[-1]
					except: path = item['path']
					append({'link': item['link'], 'filename': path, 'size': item['size']})
			return end_results
		except: return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		from modules.kodi_utils import show_busy_dialog, hide_busy_dialog
		from modules.source_utils import supported_video_extensions
		def _transfer_info(transfer_id):
			info = self.transfers_list()
			if 'status' in info and info['status'] == 'success':
				for item in info['transfers']:
					if item['id'] == transfer_id:
						return item
			return {}
		def _return_failed(message=32574, cancelled=False):
			try:
				progressDialog.close()
			except Exception:
				pass
			hide_busy_dialog()
			sleep(500)
			if cancelled:
				if confirm_dialog(heading=32733, text=32044): ok_dialog(heading=32733, text=ls(32732) % ls(32061), top_space=False)
				else: self.delete_transfer(transfer_id)
			else: ok_dialog(heading=32733, text=message, top_space=False)
			return False
		show_busy_dialog()
		extensions = supported_video_extensions()
		transfer_id = self.create_transfer(magnet_url)
		if not transfer_id['status'] == 'success':
			return _return_failed(transfer_id.get('message'))
		transfer_id = transfer_id['id']
		transfer_info = _transfer_info(transfer_id)
		if not transfer_info: return _return_failed()
		if pack:
			self.clear_cache(clear_hashes=False)
			hide_busy_dialog()
			ok_dialog(text=ls(32732) % ls(32061), top_space=False)
			return True
		interval = 5
		line = '%s[CR]%s[CR]%s'
		line1 = '%s...' % (ls(32732) % ls(32061))
		line2 = transfer_info['name']
		line3 = transfer_info['message']
		progressDialog = progress_dialog(ls(32733), icon)
		progressDialog.update(line % (line1, line2, line3), 0)
		while not transfer_info['status'] == 'seeding':
			sleep(1000 * interval)
			transfer_info = _transfer_info(transfer_id)
			line3 = transfer_info['message']
			progressDialog.update(line % (line1, line2, line3), int(float(transfer_info['progress']) * 100))
			if monitor.abortRequested() == True: return sysexit()
			try:
				if progressDialog.iscanceled():
					return _return_failed(ls(32736), cancelled=True)
			except Exception:
				pass
			if transfer_info.get('status') == 'stalled':
				return _return_failed()
		sleep(1000 * interval)
		try:
			progressDialog.close()
		except Exception:
			pass
		hide_busy_dialog()
		return True

	def user_cloud(self, folder_id=None):
		if folder_id:
			string = 'fen_pm_user_cloud_%s' % folder_id
			url = 'folder/list?id=%s' % folder_id
		else:
			string = 'fen_pm_user_cloud_root'
			url = 'folder/list'
		return cache_object(self._get, string, url, False, 0.5)

	def user_cloud_all(self):
		string = 'fen_pm_user_cloud_all_files'
		url = 'item/listall'
		return cache_object(self._get, string, url, False, 0.5)

	def transfers_list(self):
		url = 'transfer/list'
		return self._get(url)

	def instant_transfer(self, magnet_url):
		url = 'transfer/directdl'
		data = {'src': magnet_url}
		return self._post(url, data)

	def rename_cache_item(self, file_type, file_id, new_name):
		if file_type == 'folder': url = 'folder/rename'
		else: url = 'item/rename'
		data = {'id': file_id , 'name': new_name}
		response = self._post(url, data)
		return response['status']

	def create_transfer(self, magnet):
		data = {'src': magnet, 'folder_id': 0}
		url = 'transfer/create'
		return self._post(url, data)

	def delete_transfer(self, transfer_id):
		data = {'id': transfer_id}
		url = 'transfer/delete'
		return self._post(url, data)

	def delete_object(self, object_type, object_id):
		data = {'id': object_id}
		url = '%s/delete' % object_type
		response = self._post(url, data)
		return response['status']

	def get_item_details(self, item_id):
		string = 'fen_pm_item_details_%s' % item_id
		url = 'item/details'
		data = {'id': item_id}
		args = [url, data]
		return cache_object(self._post, string, args, False, 24)

	def get_hosts(self):
		string = 'fen_pm_valid_hosts'
		url = 'services/list'
		hosts_dict = {'Premiumize.me': []}
		hosts = []
		append = hosts.append
		try:
			result = cache_object(self._get, string, url, False, 168)
			for x in result['directdl']:
				for alias in result['aliases'][x]: append(alias)
			hosts_dict['Premiumize.me'] = list(set(hosts))
		except: pass
		return hosts_dict

	def add_headers_to_url(self, url):
		return url + '|' + urlencode(self.headers())

	def headers(self):
		return {'User-Agent': self.user_agent, 'Authorization': 'Bearer %s' % self.token}

	def _get(self, url, data={}):
		if self.token == '': return None
		headers = {'User-Agent': self.user_agent, 'Authorization': 'Bearer %s' % self.token}
		url = base_url + url
		response = requests.get(url, data=data, headers=headers, timeout=timeout).text
		try: return json.loads(response)
		except: return response

	def _post(self, url, data={}):
		if self.token == '' and not 'token' in url: return None
		headers = {'User-Agent': self.user_agent, 'Authorization': 'Bearer %s' % self.token}
		if not 'token' in url: url = base_url + url
		response = requests.post(url, data=data, headers=headers, timeout=timeout).text
		try: return json.loads(response)
		except: return response

	def revoke_auth(self):
		set_setting('pm.account_id', '')
		set_setting('pm.token', '')
		ok_dialog(heading=32061, text='%s %s' % (ls(32059), ls(32576)), top_space=False)

	def clear_cache(self, clear_hashes=True):
		try:
			from modules.kodi_utils import clear_property, path_exists, database, maincache_db
			if not path_exists(maincache_db): return True
			from caches.debrid_cache import debrid_cache
			user_cloud_success = False
			dbcon = database.connect(maincache_db)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
				dbcur.execute("""SELECT id FROM maincache WHERE id LIKE ?""", ('fen_pm_user_cloud%',))
				try:
					user_cloud_cache = dbcur.fetchall()
					user_cloud_cache = [i[0] for i in user_cloud_cache]
				except:
					user_cloud_success = True
				if not user_cloud_success:
					for i in user_cloud_cache:
						dbcur.execute("""DELETE FROM maincache WHERE id=?""", (i,))
						clear_property(str(i))
					dbcon.commit()
					user_cloud_success = True
			except: user_cloud_success = False
			# DOWNLOAD LINKS
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_pm_transfers_list',))
				clear_property("fen_pm_transfers_list")
				dbcon.commit()
				download_links_success = True
			except: download_links_success = False
			# HOSTERS
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_pm_valid_hosts',))
				clear_property('fen_pm_valid_hosts')
				dbcon.commit()
				dbcon.close()
				hoster_links_success = True
			except: hoster_links_success = False
			# HASH CACHED STATUS
			if clear_hashes:
				try:
					debrid_cache.clear_debrid_results('pm')
					hash_cache_status_success = True
				except: hash_cache_status_success = False
			else: hash_cache_status_success = True
		except: return False
		if False in (user_cloud_success, download_links_success, hoster_links_success, hash_cache_status_success): return False
		return True
