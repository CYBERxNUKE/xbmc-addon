# -*- coding: utf-8 -*-
import re
import time
from sys import exit as sysexit
from caches.main_cache import cache_object
from modules import kodi_utils
# logger = kodi_utils.logger

progress_dialog, notification, kodi_utils.hide_busy_dialog, monitor = kodi_utils.progress_dialog, kodi_utils.notification, kodi_utils.hide_busy_dialog, kodi_utils.monitor
ls, get_setting, set_setting, sleep, ok_dialog = kodi_utils.local_string, kodi_utils.get_setting, kodi_utils.set_setting, kodi_utils.sleep, kodi_utils.ok_dialog
show_busy_dialog, kodi_utils.confirm_dialog, database, clear_property = kodi_utils.show_busy_dialog, kodi_utils.confirm_dialog, kodi_utils.database, kodi_utils.clear_property
path_exists, maincache_db = kodi_utils.path_exists, kodi_utils.maincache_db
set_temp_highlight, restore_highlight, make_settings_dict = kodi_utils.set_temp_highlight, kodi_utils.restore_highlight, kodi_utils.make_settings_dict
pause_settings_change, unpause_settings_change = kodi_utils.pause_settings_change, kodi_utils.unpause_settings_change
base_url = 'https://api.alldebrid.com/v4/'
user_agent = 'fen_for_kodi'
timeout = 20.0
requests = kodi_utils.make_requests()
icon = kodi_utils.get_icon('alldebrid')

class AllDebridAPI:
	def __init__(self):
		self.token = get_setting('ad.token')
		self.break_auth_loop = False

	def auth(self):
		pause_settings_change()
		self.token = ''
		line = '%s[CR]%s[CR]%s'
		url = base_url + 'pin/get?agent=%s' % user_agent
		response = requests.get(url, timeout=timeout).json()
		response = response['data']
		expires_in = int(response['expires_in'])
		poll_url = response['check_url']
		sleep_interval = 5
		content = line % (ls(32517), ls(32700) % response.get('base_url'), ls(32701) % '[COLOR goldenrod]%s[/COLOR]' % response.get('pin'))
		current_highlight = set_temp_highlight('goldenrod')
		progressDialog = progress_dialog('%s %s' % (ls(32063), ls(32057)), icon)
		progressDialog.update(content, 0)
		start, time_passed = time.time(), 0
		sleep(2000)
		while not progressDialog.iscanceled() and time_passed < expires_in and not self.token:
			sleep(1000 * sleep_interval)
			response = requests.get(poll_url, timeout=timeout).json()
			response = response['data']
			activated = response['activated']
			if not activated:
				time_passed = time.time() - start
				progress = int(100 * time_passed/float(expires_in))
				progressDialog.update(content, progress)
				continue
			try:
				progressDialog.close()
				self.token = str(response['apikey'])
				set_setting('ad.token', self.token)
			except:
				ok_dialog(text=32574)
				break
		try: progressDialog.close()
		except: pass
		restore_highlight(current_highlight)
		if self.token:
			sleep(2000)
			account_info = self._get('user')
			set_setting('ad.account_id', str(account_info['user']['username']))
			set_setting('ad.enabled', 'true')
			ok_dialog(text=32576)
		unpause_settings_change()
		make_settings_dict()

	def revoke(self):
		pause_settings_change()
		set_setting('ad.token', '')
		set_setting('ad.account_id', '')
		set_setting('ad.enabled', 'false')
		unpause_settings_change()
		make_settings_dict()
		notification('All Debrid Authorization Reset', 3000)

	def account_info(self):
		response = self._get('user')
		return response

	def check_cache(self, hashes):
		data = {'magnets[]': hashes}
		response = self._post('magnet/instant', data)
		return response

	def check_single_magnet(self, hash_string):
		cache_info = self.check_cache(hash_string)['magnets'][0]
		return cache_info['instant']

	def user_cloud(self):
		url = 'magnet/status'
		string = 'fen_ad_user_cloud'
		return cache_object(self._get, string, url, False, 0.5)

	def unrestrict_link(self, link):
		url = 'link/unlock'
		url_append = '&link=%s' % link
		response = self._get(url, url_append)
		try: return response['link']
		except: return None

	def create_transfer(self, magnet):
		url = 'magnet/upload'
		url_append = '&magnet=%s' % magnet
		result = self._get(url, url_append)
		result = result['magnets'][0]
		return result.get('id', '')

	def list_transfer(self, transfer_id):
		url = 'magnet/status'
		url_append = '&id=%s' % transfer_id
		result = self._get(url, url_append)
		result = result['magnets']
		return result

	def delete_transfer(self, transfer_id):
		url = 'magnet/delete'
		url_append = '&id=%s' % transfer_id
		result = self._get(url, url_append)
		if result.get('success', False):
			return True

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, EXTRAS
		try:
			file_url, media_id = None, None
			extensions = supported_video_extensions()
			correct_files = []
			correct_files_append = correct_files.append
			transfer_id = self.create_transfer(magnet_url)
			transfer_info = self.list_transfer(transfer_id)
			valid_results = [i for i in transfer_info['links'] if any(i.get('filename').lower().endswith(x) for x in extensions) and not i.get('link', '') == '']
			if valid_results:
				if season:
					correct_files = [i for i in valid_results if seas_ep_filter(season, episode, i['filename'])]
					if correct_files:
						episode_title = re.sub(r'[^A-Za-z0-9-]+', '.', title.replace('\'', '').replace('&', 'and').replace('%', '.percent')).lower()
						try: media_id = [i['link'] for i in correct_files if not any(x in re.sub(episode_title, '', seas_ep_filter(season, episode, i['filename'], split=True)) \
											for x in EXTRAS)][0]
						except: media_id = None
				else: media_id = max(valid_results, key=lambda x: x.get('size')).get('link', None)
			if not store_to_cloud: self.delete_transfer(transfer_id)
			if media_id:
				file_url = self.unrestrict_link(media_id)
				if not any(file_url.lower().endswith(x) for x in extensions): file_url = None
			return file_url
		except:
			try:
				if transfer_id: self.delete_transfer(transfer_id)
			except: pass
			return None
	
	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			extensions = supported_video_extensions()
			transfer_id = self.create_transfer(magnet_url)
			transfer_info = self.list_transfer(transfer_id)
			end_results = []
			append = end_results.append
			for item in transfer_info.get('links'):
				if any(item.get('filename').lower().endswith(x) for x in extensions) and not item.get('link', '') == '':
					append({'link': item['link'], 'filename': item['filename'], 'size': item['size']})
			self.delete_transfer(transfer_id)
			return end_results
		except:
			try:
				if transfer_id: self.delete_transfer(transfer_id)
			except: pass
			return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		def _return_failed(message=32574, cancelled=False):
			try: progressDialog.close()
			except Exception: pass
			hide_busy_dialog()
			sleep(500)
			if cancelled:
				if confirm_dialog(text=32044): ok_dialog(heading=32733, text=ls(32732) % ls(32063))
				else: self.delete_transfer(transfer_id)
			else: ok_dialog(heading=2733, text=message)
			return False
		show_busy_dialog()
		transfer_id = self.create_transfer(magnet_url)
		if not transfer_id: return _return_failed()
		transfer_info = self.list_transfer(transfer_id)
		if not transfer_info: return _return_failed()
		if pack:
			self.clear_cache(clear_hashes=False)
			hide_busy_dialog()
			ok_dialog(text=ls(32732) % ls(32063), top_space=False)
			return True
		interval = 5
		line = '%s[CR]%s[CR]%s'
		line1 = '%s...' % (ls(32732) % ls(32063))
		line2 = transfer_info['filename']
		line3 = transfer_info['status']
		progressDialog = progress_dialog(ls(32733), icon)
		progressDialog.update(line % (line1, line2, line3), 0)
		while not transfer_info['statusCode'] == 4:
			sleep(1000 * interval)
			transfer_info = self.list_transfer(transfer_id)
			file_size = transfer_info['size']
			line2 = transfer_info['filename']
			if transfer_info['statusCode'] == 1:
				download_speed = round(float(transfer_info['downloadSpeed']) / (1000**2), 2)
				progress = int(float(transfer_info['downloaded']) / file_size * 100) if file_size > 0 else 0
				line3 = ls(32734) % (download_speed, transfer_info['seeders'], progress, round(float(file_size) / (1000 ** 3), 2))
			elif transfer_info['statusCode'] == 3:
				upload_speed = round(float(transfer_info['uploadSpeed']) / (1000 ** 2), 2)
				progress = int(float(transfer_info['uploaded']) / file_size * 100) if file_size > 0 else 0
				line3 = ls(32735) % (upload_speed, progress, round(float(file_size) / (1000 ** 3), 2))
			else:
				line3 = transfer_info['status']
				progress = 0
			progressDialog.update(line % (line1, line2, line3), progress)
			if monitor.abortRequested() == True: return sysexit()
			try:
				if progressDialog.iscanceled():
					return _return_failed(32736, cancelled=True)
			except Exception:
				pass
			if 5 <= transfer_info['statusCode'] <= 10:
				return _return_failed()
		sleep(1000 * interval)
		try: progressDialog.close()
		except: pass
		hide_busy_dialog()
		return True

	def get_hosts(self):
		string = 'fen_ad_valid_hosts'
		url = 'hosts'
		hosts_dict = {'AllDebrid': []}
		hosts = []
		try:
			result = cache_object(self._get, string, url, False, 168)
			result = result['hosts']
			for k, v in result.items():
				try: hosts.extend(v['domains'])
				except: pass
			hosts = list(set(hosts))
			hosts_dict['AllDebrid'] = hosts
		except: pass
		return hosts_dict

	def _get(self, url, url_append=''):
		result = None
		try:
			if self.token == '': return None
			url = base_url + url + '?agent=%s&apikey=%s' % (user_agent, self.token) + url_append
			result = requests.get(url, timeout=timeout).json()
			if result.get('status') == 'success' and 'data' in result: result = result['data']
		except: pass
		return result

	def _post(self, url, data={}):
		result = None
		try:
			if self.token == '': return None
			url = base_url + url + '?agent=%s&apikey=%s' % (user_agent, self.token)
			result = requests.post(url, data=data, timeout=timeout).json()
			if result.get('status') == 'success' and 'data' in result: result = result['data']
		except: pass
		return result

	def revoke_auth(self):
		set_setting('ad.account_id', '')
		set_setting('ad.token', '')
		ok_dialog(heading=32063, text='%s %s' % (ls(32059), ls(32576)), top_space=False)

	def clear_cache(self, clear_hashes=True):
		try:
			if not path_exists(maincache_db): return True
			from caches.debrid_cache import debrid_cache
			dbcon = database.connect(maincache_db)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_ad_user_cloud',))
				clear_property('fen_ad_user_cloud')
				dbcon.commit()
				user_cloud_success = True
			except: user_cloud_success = False
			# HOSTERS
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('fen_ad_valid_hosts',))
				clear_property('fen_ad_valid_hosts')
				dbcon.commit()
				dbcon.close()
				hoster_links_success = True
			except: hoster_links_success = False
			# HASH CACHED STATUS
			if clear_hashes:
				try:
					debrid_cache.clear_debrid_results('ad')
					hash_cache_status_success = True
				except: hash_cache_status_success = False
			else: hash_cache_status_success = True
		except: return False
		if False in (user_cloud_success, hoster_links_success, hash_cache_status_success): return False
		return True
