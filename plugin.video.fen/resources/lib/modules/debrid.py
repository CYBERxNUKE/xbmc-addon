# -*- coding: utf-8 -*-
import time
from threading import Thread
from windows import create_window
from caches.debrid_cache import debrid_cache
from apis.real_debrid_api import RealDebridAPI
from apis.premiumize_api import PremiumizeAPI
from apis.alldebrid_api import AllDebridAPI
from modules.kodi_utils import sleep, show_busy_dialog, hide_busy_dialog, notification, monitor, local_string as ls
from modules.utils import make_thread_list
from modules.settings import display_sleep_time, enabled_debrids_check
from modules.settings_reader import get_setting
# from modules.kodi_utils import logger

rd_api = RealDebridAPI()
pm_api = PremiumizeAPI()
ad_api = AllDebridAPI()
debrid_list = [('Real-Debrid', 'rd', rd_api), ('Premiumize.me', 'pm', pm_api), ('AllDebrid', 'ad', ad_api)]

def debrid_enabled():
	return [i[0] for i in debrid_list if enabled_debrids_check(i[1])]

def debrid_type_enabled(debrid_type, enabled_debrids):
	return [i[0] for i in debrid_list if i[0] in enabled_debrids and get_setting('%s.%s.enabled' % (i[1], debrid_type)) == 'true']

def debrid_valid_hosts(enabled_debrids):
	def _get_hosts(function):
		append(function.get_hosts())
	debrid_hosts = []
	append = debrid_hosts.append
	if enabled_debrids:
		threads = list(make_thread_list(_get_hosts, [i[2] for i in debrid_list if i[0] in enabled_debrids], Thread))
		[i.join() for i in threads]
	return debrid_hosts

def manual_add_magnet_to_cloud(params):
	show_busy_dialog()
	function = [i[2] for i in debrid_list if i[0] == params['provider']][0]
	result = function.create_transfer(params['magnet_url'])
	function.clear_cache()
	hide_busy_dialog()
	if result == 'failed': notification(32490)
	else: notification(32576)

class DebridCheck:
	def run(self, hash_list, background, debrid_enabled, meta, progress_dialog):
		self.sleep_time = display_sleep_time()
		self.timeout = 20.0
		self.cached_hashes, self.main_threads = [], []
		self.rd_cached_hashes, self.rd_hashes_unchecked, self.rd_process_results = [], [], []
		self.pm_cached_hashes, self.pm_hashes_unchecked, self.pm_process_results = [], [], []
		self.ad_cached_hashes, self.ad_hashes_unchecked, self.ad_process_results = [], [], []
		self.meta = meta
		self.hash_list = hash_list
		self.progress_dialog = progress_dialog
		self._query_local_cache(self.hash_list)
		main_threads_append = self.main_threads.append
		if 'AllDebrid' in debrid_enabled:
			self.ad_cached_hashes, self.ad_hashes_unchecked = self.cached_check('ad')
			if self.ad_hashes_unchecked: main_threads_append(Thread(target=self.AD_cache_checker, name='AllDebrid'))
		if 'Premiumize.me' in debrid_enabled:
			self.pm_cached_hashes, self.pm_hashes_unchecked = self.cached_check('pm')
			if self.pm_hashes_unchecked: main_threads_append(Thread(target=self.PM_cache_checker, name='Premiumize.me'))
		if 'Real-Debrid' in debrid_enabled:
			self.rd_cached_hashes, self.rd_hashes_unchecked = self.cached_check('rd')
			if self.rd_hashes_unchecked: main_threads_append(Thread(target=self.RD_cache_checker, name='Real-Debrid'))
		if self.main_threads:
			[i.start() for i in self.main_threads]
			if background: [i.join() for i in self.main_threads]
			else:
				self._make_progress_dialog()
				self.debrid_check_dialog()
		self._kill_progress_dialog()
		return {'rd_cached_hashes': self.rd_cached_hashes, 'pm_cached_hashes': self.pm_cached_hashes, 'ad_cached_hashes': self.ad_cached_hashes}

	def cached_check(self, debrid):
		cached_list = [i[0] for i in self.cached_hashes if i[1] == debrid and i[2] == 'True']
		unchecked_list = [i for i in self.hash_list if not any([h for h in self.cached_hashes if h[0] == i and h[1] == debrid])]
		return cached_list, unchecked_list

	def debrid_check_dialog(self):
		start_time = time.time()
		end_time = start_time + self.timeout
		line = '%s[CR]%s[CR]%s'
		plswait_str, checking_debrid, remaining_debrid = ls(32577), ls(32578), ls(32579)
		while not self.progress_dialog.iscanceled():
			try:
				if monitor.abortRequested() is True: break
				remaining_debrids = [x.getName() for x in self.main_threads if x.is_alive() is True]
				current_time = time.time()
				current_progress = current_time - start_time
				try:
					line3 = remaining_debrid % ', '.join(remaining_debrids).upper()
					percent = int((current_progress/float(self.timeout))*100)
					self.progress_dialog.update(line % (plswait_str, checking_debrid, line3), percent)
				except: pass
				sleep(self.sleep_time)
				if len(remaining_debrids) == 0: break
				if current_time > end_time: break
			except Exception: pass

	def RD_cache_checker(self):
		hashes = self.rd_hashes_unchecked
		self._rd_lookup(hashes)
		self._add_to_local_cache(self.rd_process_results, 'rd')

	def PM_cache_checker(self):
		hashes = self.pm_hashes_unchecked
		self._pm_lookup(hashes)
		self._add_to_local_cache(self.pm_process_results, 'pm')

	def AD_cache_checker(self):
		hashes = self.ad_hashes_unchecked
		self._ad_lookup(hashes)
		self._add_to_local_cache(self.ad_process_results, 'ad')

	def _rd_lookup(self, hash_list):
		rd_cache = rd_api.check_cache(hash_list)
		if not rd_cache: return
		cached_append = self.rd_cached_hashes.append
		process_append = self.rd_process_results.append
		try:
			for h in hash_list:
				cached = 'False'
				if h in rd_cache:
					info = rd_cache[h]
					if isinstance(info, dict) and len(info.get('rd')) > 0:
						cached_append(h)
						cached = 'True'
				process_append((h, cached))
		except:
			for i in hash_list: process_append((i, 'False'))

	def _pm_lookup(self, hash_list):
		pm_cache = pm_api.check_cache(hash_list)
		if not pm_cache: return
		cached_append = self.pm_cached_hashes.append
		process_append = self.pm_process_results.append
		try:
			pm_cache = pm_cache['response']
			for c, h in enumerate(hash_list):
				cached = 'False'
				if pm_cache[c] is True:
					cached_append(h)
					cached = 'True'
				process_append((h, cached))
		except:
			for i in hash_list: process_append((i, 'False'))

	def _ad_lookup(self, hash_list):
		ad_cache = ad_api.check_cache(hash_list)
		if not ad_cache: return
		cached_append = self.ad_cached_hashes.append
		process_append = self.ad_process_results.append
		try:
			ad_cache = ad_cache['magnets']
			for i in ad_cache:
				cached = 'False'
				if i['instant'] == True:
					cached_append(i['hash'])
					cached = 'True'
				process_append((i['hash'], cached))
		except:
			for i in hash_list: process_append((i, 'False'))

	def _query_local_cache(self, hash_list):
		cached = debrid_cache.get_many(hash_list)
		if cached:
			self.cached_hashes = cached

	def _add_to_local_cache(self, hash_list, debrid):
		debrid_cache.set_many(hash_list, debrid)

	def _make_progress_dialog(self):
		if not self.progress_dialog:
			self.progress_dialog = create_window(('windows.yes_no_progress_media', 'YesNoProgressMedia'), 'yes_no_progress_media.xml', meta=self.meta)
			Thread(target=self.progress_dialog.run).start()

	def _kill_progress_dialog(self):
		try: self.progress_dialog.close()
		except: pass
		try: del self.progress_dialog
		except: pass

debrid_check = DebridCheck()
