# -*- coding: utf-8 -*-
import time
import metadata
from windows import open_window, create_window
from scrapers import external, folders
from modules import debrid, kodi_utils, settings
from modules.player import FenPlayer
from modules.source_utils import internal_sources, external_sources, internal_folders_import, scraper_names, get_cache_expiry, make_alias_dict
from modules.utils import clean_file_name, string_to_float, safe_string, remove_accents, get_datetime, manual_function_import
# logger = kodi_utils.logger

json, show_busy_dialog, hide_busy_dialog, confirm_progress_media = kodi_utils.json, kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.confirm_progress_media
select_dialog, confirm_dialog, get_setting, close_all_dialog = kodi_utils.select_dialog, kodi_utils.confirm_dialog, kodi_utils.get_setting, kodi_utils.close_all_dialog
ls, get_icon, notification, sleep, execute_builtin = kodi_utils.local_string, kodi_utils.get_icon, kodi_utils.notification, kodi_utils.sleep, kodi_utils.execute_builtin
Thread, get_property, set_property, clear_property = kodi_utils.Thread, kodi_utils.get_property, kodi_utils.set_property, kodi_utils.clear_property
display_sleep_time, scraping_settings, include_prerelease_results = settings.display_sleep_time, settings.scraping_settings, settings.include_prerelease_results
auto_play, active_internal_scrapers, provider_sort_ranks,  = settings.auto_play, settings.active_internal_scrapers, settings.provider_sort_ranks
ignore_results_filter, filter_status, results_sort_order = settings.ignore_results_filter, settings.filter_status, settings.results_sort_order
metadata_user_info, quality_filter, sort_to_top  = settings.metadata_user_info, settings.quality_filter, settings.sort_to_top
display_uncached_torrents, check_prescrape_sources = settings.display_uncached_torrents, settings.check_prescrape_sources
results_style, results_xml_window_number = settings.results_style, settings.results_xml_window_number
debrid_enabled, debrid_type_enabled, debrid_valid_hosts = debrid.debrid_enabled, debrid.debrid_type_enabled, debrid.debrid_valid_hosts
rd_info, pm_info, ad_info = ('apis.real_debrid_api', 'RealDebridAPI'), ('apis.premiumize_api', 'PremiumizeAPI'), ('apis.alldebrid_api', 'AllDebridAPI')
debrids = {'Real-Debrid': rd_info, 'rd_cloud': rd_info, 'rd_browse': rd_info, 'Premiumize.me': pm_info, 'pm_cloud': pm_info, 'pm_browse': pm_info,
			'AllDebrid': ad_info, 'ad_cloud': ad_info, 'ad_browse': ad_info}
debrid_providers = ('Real-Debrid', 'Premiumize.me', 'AllDebrid')
quality_ranks = {'4K': 1, '1080p': 2, '720p': 3, 'SD': 4, 'SCR': 5, 'CAM': 5, 'TELE': 5}
cloud_scrapers, folder_scrapers = ('rd_cloud', 'pm_cloud', 'ad_cloud'), ('folder1', 'folder2', 'folder3', 'folder4', 'folder5')
default_internal_scrapers = ('furk', 'easynews', 'rd_cloud', 'pm_cloud', 'ad_cloud', 'folders')
hevc_filter_key, hdr_filter_key, dolby_vision_filter_key, av1_filter_key = '[B]HEVC[/B]', '[B]HDR[/B]', '[B]D/VISION[/B]', '[B]AV1[/B]'
dialog_format, remaining_format = '[COLOR %s][B]%s[/B][/COLOR] 4K: %s | 1080p: %s | 720p: %s | SD: %s | Total: %s', ls(32676)
main_line, int_window_prop = '%s[CR]%s[CR]%s', kodi_utils.int_window_prop

class Sources():
	def __init__(self):
		self.params = {}
		self.prescrape_scrapers, self.prescrape_threads, self.prescrape_sources, self.uncached_torrents = [], [], [], []
		self.threads, self.providers, self.sources, self.internal_scraper_names = [], [], [], []
		self.clear_properties, self.filters_ignored, self.active_folders, self.resolve_dialog_made = True, False, False, False
		self.remove_scrapers = ['external']# needs to be mutable so leave as list.
		self.sourcesTotal = self.sources4K = self.sources1080p = self.sources720p = self.sourcesSD = 0
		self.prescrape, self.disabled_ext_ignored, self.default_ext_only = 'true', 'false', 'false'
		self.language = get_setting('meta_language')
		self.progress_dialog = None
		self.player = FenPlayer()

	def playback_prep(self, params=None):
		hide_busy_dialog()
		if params: self.params = params
		params_get = self.params.get
		self.play_type, self.background, self.prescrape = params_get('play_type', ''), params_get('background', 'false') == 'true', params_get('prescrape', self.prescrape) == 'true'
		self.random, self.random_continual,  = params_get('random', 'false') == 'true', params_get('random_continual', 'false') == 'true'
		self.nextep_settings, self.disable_autoplay_next_episode = params_get('nextep_settings', {}), params_get('disable_autoplay_next_episode', 'false') == 'true'
		self.ignore_scrape_filters = params_get('ignore_scrape_filters', 'false') == 'true'
		self.folders_ignore_filters = get_setting('results.folders_ignore_filters', 'false') == 'true'
		self.disabled_ext_ignored = params_get('disabled_ext_ignored', self.disabled_ext_ignored) == 'true'
		self.default_ext_only = params_get('default_ext_only', self.default_ext_only) == 'true'
		self.media_type, self.tmdb_id, self.ep_name, self.plot = params_get('media_type'), params_get('tmdb_id'), params_get('ep_name'), params_get('plot')
		self.custom_title, self.custom_year = params_get('custom_title', None), params_get('custom_year', None)
		self.custom_season, self.custom_episode = params_get('custom_season', None), params_get('custom_episode', None)
		if 'autoplay' in self.params: self.autoplay = self.params.get('autoplay', 'false') == 'true'
		else: self.autoplay = auto_play(self.media_type)
		if 'season' in self.params: self.season = int(params_get('season'))
		else: self.season = ''
		if 'episode' in self.params: self.episode = int(params_get('episode'))
		else: self.episode = ''
		if 'meta' in self.params: self.meta = json.loads(params_get('meta'))
		else: self._grab_meta()
		self.active_internal_scrapers = active_internal_scrapers()
		if not 'external' in self.active_internal_scrapers and (self.disabled_ext_ignored or self.default_ext_only): self.active_internal_scrapers.append('external')
		self.active_external = 'external' in self.active_internal_scrapers
		self.provider_sort_ranks, self.sleep_time, self.scraper_settings = provider_sort_ranks(), display_sleep_time(), scraping_settings()
		self.include_prerelease_results, self.ignore_results_filter = include_prerelease_results(), ignore_results_filter()
		self.filter_hevc, self.filter_hdr, self.filter_dv, self.filter_av1 = filter_status('hevc'), filter_status('hdr'), filter_status('dv'), filter_status('av1')
		self.sort_function, self.display_uncached_torrents, self.quality_filter = results_sort_order(), display_uncached_torrents(), self._quality_filter()
		self.hybrid_allowed, self.filter_size_method = self.filter_hdr in (0, 2), int(get_setting('results.filter_size_method', '0'))
		self.include_unknown_size, self.include_3D_results = get_setting('results.include.unknown.size', 'false') == 'true', get_setting('include_3d_results', 'true') == 'true'
		self._update_meta()
		self._search_info()
		return self.get_sources()

	def get_sources(self):
		if not self.progress_dialog and not self.background:
			self._make_progress_dialog()
		results = []
		if self.prescrape and any(x in self.active_internal_scrapers for x in default_internal_scrapers):
			if self.prepare_internal_scrapers():
				results = self.collect_prescrape_results()
				if results: results = self.process_results(results)
		if not results:
			self.prescrape = False
			self.prepare_internal_scrapers()
			if self.active_external:
				self.activate_debrid_info()
				self.activate_external_providers()
			elif not self.active_internal_scrapers: self._kill_progress_dialog()
			self.orig_results = self.collect_results()
			if not self.orig_results and not self.active_external: self._kill_progress_dialog()
			results = self.process_results(self.orig_results)
			if not results: return self._process_post_results()
		return self.play_source(results)

	def collect_results(self):
		self.sources.extend(self.prescrape_sources)
		threads_append = self.threads.append
		if self.active_folders: self.append_folder_scrapers(self.providers)
		self.providers.extend(internal_sources(self.active_internal_scrapers))
		if self.providers:
			for i in self.providers: threads_append(Thread(target=self.activate_providers, args=(i[0], i[1], False), name=i[2]))
			[i.start() for i in self.threads]
		if self.active_external or self.background:
			if self.active_external:
				self.external_args = (self.meta, self.external_providers, self.debrid_torrent_enabled, self.debrid_hoster_enabled, self.internal_scraper_names,
										self.prescrape_sources, self.progress_dialog, self.disabled_ext_ignored)
				self.activate_providers('external', external, False)
			if self.background: [i.join() for i in self.threads]
		else: self.scrapers_dialog()
		return self.sources

	def collect_prescrape_results(self):
		threads_append = self.prescrape_threads.append
		if self.active_folders:
			if self.autoplay or check_prescrape_sources('folders'):
				self.append_folder_scrapers(self.prescrape_scrapers)
				self.remove_scrapers.append('folders')
		self.prescrape_scrapers.extend(internal_sources(self.active_internal_scrapers, True))
		if not self.prescrape_scrapers: return []
		for i in self.prescrape_scrapers: threads_append(Thread(target=self.activate_providers, args=(i[0], i[1], True), name=i[2]))
		[i.start() for i in self.prescrape_threads]
		self.remove_scrapers.extend(i[2] for i in self.prescrape_scrapers)
		if self.background: [i.join() for i in self.prescrape_threads]
		else: self.scrapers_dialog()
		return self.prescrape_sources

	def process_results(self, results):
		if self.prescrape: self.all_scrapers = self.active_internal_scrapers
		else:
			self.all_scrapers = list(set(self.active_internal_scrapers + self.remove_scrapers))
			clear_property('fs_filterless_search')
		self.uncached_torrents = self.sort_results([i for i in results if 'Uncached' in i.get('cache_provider', '')])
		if not self.display_uncached_torrents: results = [i for i in results if not i in self.uncached_torrents]
		if self.ignore_scrape_filters:
			self.filters_ignored = True
			results = self.sort_results(results)
			results = self._sort_first(results)
		else:
			results = self.filter_results(results)
			results = self.sort_results(results)
			results = self._special_filter(results, hevc_filter_key, self.filter_hevc)
			results = self._special_filter(results, hdr_filter_key, self.filter_hdr)
			results = self._special_filter(results, dolby_vision_filter_key, self.filter_dv)
			results = self._special_filter(results, av1_filter_key, self.filter_av1)
			results = self._sort_first(results)
		return results

	def filter_results(self, results):
		if self.folders_ignore_filters:
			folder_results = [i for i in results if i['scrape_provider'] == 'folders']
			results = [i for i in results if not i in folder_results]
		else:
			folder_results = []
		results = [i for i in results if i['quality'] in self.quality_filter]
		if not self.include_3D_results: results = [i for i in results if not '3D' in i['extraInfo']]
		if self.filter_size_method:
			if self.filter_size_method == 1:
				duration = self.meta['duration'] or (5400 if self.media_type == 'movie' else 2400)
				max_size = ((0.125 * (0.90 * string_to_float(get_setting('results.size.auto', '20'), '20'))) * duration)/1000
			elif self.filter_size_method == 2:
				max_size = string_to_float(get_setting('results.size.manual', '10000'), '10000') / 1000
			if self.include_unknown_size: results = [i for i in results if i['scrape_provider'] == 'folders' or i['size'] <= max_size]
			else: results = [i for i in results if i['scrape_provider'] == 'folders' or 0.01 < i['size'] <= max_size]
		results += folder_results
		return results

	def sort_results(self, results):
		def _add_keys(item):
			provider = item['scrape_provider']
			if provider == 'external': account_type = item['debrid'].lower()
			else: account_type = provider.lower()
			item['provider_rank'] = self._get_provider_rank(account_type)
			item['quality_rank'] = self._get_quality_rank(item.get('quality', 'SD'))
		for item in results: _add_keys(item)
		results.sort(key=self.sort_function)
		results = self._sort_uncached_torrents(results)
		return results

	def prepare_internal_scrapers(self):
		if self.active_external and len(self.active_internal_scrapers) == 1: return
		active_internal_scrapers = [i for i in self.active_internal_scrapers if not i in self.remove_scrapers]
		if self.prescrape and not self.active_external and all([check_prescrape_sources(i) for i in active_internal_scrapers]): return False
		self.active_folders = 'folders' in active_internal_scrapers
		if self.active_folders:
			self.folder_info = self.get_folderscraper_info()
			self.internal_scraper_names = [i for i in active_internal_scrapers if not i == 'folders'] + [i[0] for i in self.folder_info]
		else:
			self.folder_info = []
			self.internal_scraper_names = active_internal_scrapers[:]
		self.active_internal_scrapers = active_internal_scrapers
		if self.clear_properties: self._clear_properties()
		return True

	def activate_providers(self, module_type, function, prescrape):
		sources = self._get_module(module_type, function).results(self.search_info)
		if not sources: return
		if prescrape: self.prescrape_sources.extend(sources)
		else: self.sources.extend(sources)

	def activate_debrid_info(self):
		self.debrid_enabled = debrid_enabled()
		self.debrid_torrent_enabled = debrid_type_enabled('torrent', self.debrid_enabled)
		self.debrid_hoster_enabled = debrid_valid_hosts(debrid_type_enabled('hoster', self.debrid_enabled))

	def activate_external_providers(self):
		if not self.debrid_torrent_enabled and not self.debrid_hoster_enabled:
			if len(self.active_internal_scrapers) == 1 and 'external' in self.active_internal_scrapers: notification(32854, 2000)
			self.active_external = False
		else:
			exclude_list = []
			if not self.debrid_torrent_enabled: exclude_list.extend(scraper_names('torrents'))
			elif not self.debrid_hoster_enabled: exclude_list.extend(scraper_names('hosters'))
			self.external_providers = external_sources(ret_all=self.disabled_ext_ignored, ret_default_only=self.default_ext_only)
			if exclude_list: self.external_providers = [i for i in self.external_providers if not i[0] in exclude_list]

	def play_source(self, results):
		if self.background or self.autoplay: return self.play_file(results, autoplay=self.autoplay, background=self.background)
		return self.display_results(results)

	def append_folder_scrapers(self, current_list):
		current_list.extend(internal_folders_import(self.folder_info))

	def get_folderscraper_info(self):
		folder_info = [(get_setting('%s.display_name' % i), i) for i in folder_scrapers]
		return [i for i in folder_info if not i[0] in (None, 'None', '')]

	def scrapers_dialog(self):
		def _scraperDialog():
			monitor = kodi_utils.monitor
			while not self.progress_dialog.iscanceled():
				try:
					if monitor.abortRequested(): break
					remaining_providers = [x.getName() for x in _threads if x.is_alive() is True]
					self._process_internal_results()
					s4k_label, s1080_label = total_format % self.sources4K, total_format % self.sources1080p
					s720_label, ssd_label, stotal_label = total_format % self.sources720p, total_format % self.sourcesSD, total_format % self.sourcesTotal
					try:
						current_time = time.time()
						current_progress = current_time - start_time
						line2 = dialog_format % (int_dialog_hl, line2_inst, s4k_label, s1080_label, s720_label, ssd_label, stotal_label)
						line3 = remaining_format % ', '.join(remaining_providers).upper()
						percent = int((current_progress/float(timeout))*100)
						self.progress_dialog.update(main_line % (line1, line2, line3), percent)
						sleep(self.sleep_time)
						if len(remaining_providers) == 0: break
						if percent >= 100: break
					except: pass
				except: pass
		if self.prescrape: scraper_list, _threads, line1_inst, line2_inst = self.prescrape_scrapers, self.prescrape_threads, '%s %s' % (ls(32829), ls(32830)), 'Pre:'
		else: scraper_list, _threads, line1_inst, line2_inst = self.providers, self.threads, ls(32096), 'Int:'
		self.internal_scrapers = self._get_active_scraper_names(scraper_list)
		if not self.internal_scrapers: return
		timeout = 25
		int_dialog_hl = get_setting('int_dialog_highlight') or 'dodgerblue'
		total_format = '[COLOR %s][B]%s[/B][/COLOR]' % (int_dialog_hl, '%s')
		line1 = '[COLOR %s][B]%s[/B][/COLOR]' % (int_dialog_hl, line1_inst)
		start_time = time.time()
		end_time = start_time + timeout
		_scraperDialog()
		try: del monitor
		except: pass

	def display_results(self, results):
		window_style = results_style()
		action, chosen_item = open_window(('windows.sources', 'SourceResults'), 'sources_results.xml',
				window_style=window_style, window_id=results_xml_window_number(window_style), results=results, meta=self.meta,
				scraper_settings=self.scraper_settings, prescrape=self.prescrape, filters_ignored=self.filters_ignored, uncached_torrents=self.uncached_torrents)
		if not action: self._kill_progress_dialog()
		elif action == 'play':
			return self.play_file(results, chosen_item)
		elif self.prescrape and action == 'perform_full_search':
			self.prescrape, self.clear_properties = False, False
			return self.playback_prep()

	def _get_active_scraper_names(self, scraper_list):
		return [i[2] for i in scraper_list]

	def _process_post_results(self):
		if self.orig_results:
			if self.display_uncached_torrents and not self.autoplay: return self.play_source(self.uncached_torrents)
			if self.ignore_results_filter == 0: return self._no_results()
			if self.ignore_results_filter == 1 or confirm_progress_media(meta=self.meta, text=32021, enable_buttons=True): return self._process_ignore_filters()
		return self._no_results()

	def _process_ignore_filters(self):
		if self.autoplay: notification('%s & %s' % (ls(32686), ls(32071)))
		self.filters_ignored, self.autoplay = True, False
		results = self.sort_results(self.orig_results)
		results = self._sort_first(results)
		return self.play_source(results)

	def _no_results(self):
		self._kill_progress_dialog()
		hide_busy_dialog()
		if self.background: return notification('%s %s' % (ls(32801), ls(32760)), 5000)
		notification(32760, 2000)

	def _update_meta(self):
		self.meta.update({'media_type': self.media_type, 'season': self.season, 'episode': self.episode, 'background': self.background})
		if self.custom_title: self.meta['custom_title'] = self.custom_title
		if self.custom_year: self.meta['custom_year'] = self.custom_year
		if self.media_type == 'episode':
			if self.custom_season: self.meta['custom_season'] = self.custom_season
			if self.custom_episode: self.meta['custom_episode'] = self.custom_episode
			if self.disable_autoplay_next_episode: self.meta['disable_autoplay_next_episode'] = 'true'
			if self.random: self.meta['random'] = 'true'
			if self.random_continual: self.meta['random_continual'] = 'true'

	def _search_info(self):
		title = self.get_search_title()
		year = self.get_search_year()
		season = self.get_search_season()
		episode = self.get_search_episode()
		ep_name = self.get_ep_name()
		aliases = make_alias_dict(self.meta, title)
		expiry_times = get_cache_expiry(self.media_type, self.meta, self.season)
		self.search_info = {'media_type': self.media_type, 'title': title, 'year': year, 'tmdb_id': self.tmdb_id, 'imdb_id': self.meta.get('imdb_id'), 'aliases': aliases,
							'season': season, 'episode': episode, 'tvdb_id': self.meta.get('tvdb_id'), 'ep_name': ep_name, 'expiry_times': expiry_times,
							'total_seasons': self.meta.get('total_seasons', 1)}

	def get_search_title(self):
		if 'custom_title' in self.meta: search_title = self.meta['custom_title']
		else:
			if self.language == 'en': search_title = self.meta['title']
			else:
				search_title = None
				if 'english_title' in self.meta: search_title = self.meta['english_title']
				else:
					try:
						media_type = 'movie' if self.media_type == 'movie' else 'tv'
						meta_user_info = metadata_user_info()
						english_title = metadata.english_translation(media_type, self.meta['tmdb_id'], meta_user_info)
						if english_title: search_title = english_title
						else: search_title = meta['original_title']
					except: pass
				if not search_title: search_title = self.meta['original_title']
			if '(' in search_title: search_title = search_title.split('(')[0]
			search_title.replace('/', ' ')
		return search_title

	def get_search_year(self):
		if 'custom_year' in self.meta: year = self.meta['custom_year']
		else:
			year = self.meta.get('year')
			if self.active_external and get_setting('search.enable.yearcheck', 'false') == 'true':
				from apis.imdb_api import imdb_year_check
				try:
					imdb_year = str(imdb_year_check(self.meta.get('imdb_id')))
					if imdb_year: year = imdb_year
				except: pass
		return year

	def get_search_season(self):
		if 'custom_season' in self.meta: season = int(self.meta['custom_season'])
		else: season = self.meta['season']
		return season

	def get_search_episode(self):
		if 'custom_episode' in self.meta: episode = int(self.meta['custom_episode'])
		else: episode = self.meta['episode']
		return episode

	def get_ep_name(self):
		ep_name = None
		if self.meta['media_type'] == 'episode':
			ep_name = self.meta.get('ep_name')
			try: ep_name = safe_string(remove_accents(ep_name))
			except: ep_name = safe_string(ep_name)
		return ep_name

	def _process_internal_results(self):
		for i in self.internal_scrapers:
			win_property = get_property(int_window_prop % i)
			if win_property in ('checked', '', None): continue
			try: sources = json.loads(win_property)
			except: continue
			set_property(int_window_prop % i, 'checked')
			self._sources_quality_count(sources)
	
	def _sources_quality_count(self, sources):
		for i in sources:
			quality = i['quality']
			if quality == '4K': self.sources4K += 1
			elif quality in ('1440p', '1080p'): self.sources1080p += 1
			elif quality in ('720p', 'HD'): self.sources720p += 1
			else: self.sourcesSD += 1
			self.sourcesTotal += 1

	def _quality_filter(self):
		setting = 'results_quality_%s' % self.media_type if not self.autoplay else 'autoplay_quality_%s' % self.media_type
		filter_list = quality_filter(setting)
		if self.include_prerelease_results and 'SD' in filter_list: filter_list += ['SCR', 'CAM', 'TELE']
		return filter_list

	def _get_quality_rank(self, quality):
		return quality_ranks[quality]

	def _get_provider_rank(self, account_type):
		return self.provider_sort_ranks[account_type] or 11

	def _sort_first(self, results):
		try:
			sort_first_scrapers = []
			if 'folders' in self.all_scrapers and sort_to_top('folders'): sort_first_scrapers.append('folders')
			sort_first_scrapers.extend([i for i in self.all_scrapers if i in cloud_scrapers and sort_to_top(i)])
			if not sort_first_scrapers: return results
			sort_first = [i for i in results if i['scrape_provider'] in sort_first_scrapers]
			sort_first.sort(key=lambda k: (self._sort_folder_to_top(k['scrape_provider']), k['quality_rank']))
			sort_last = [i for i in results if not i in sort_first]
			results = sort_first + sort_last
		except: pass
		return results

	def _sort_folder_to_top(self, provider):
		if provider == 'folders': return 0
		else: return 1

	def _sort_uncached_torrents(self, results):
		uncached = [i for i in results if 'Uncached' in i.get('cache_provider', '')]
		cached = [i for i in results if not i in uncached]
		return cached + uncached

	def _special_filter(self, results, key, enable_setting):
		if key == hevc_filter_key and enable_setting in (0,2):
			hevc_max_quality = self._get_quality_rank(get_setting('filter_hevc.%s' % ('max_autoplay_quality' if self.autoplay else 'max_quality'), '4K'))
			results = [i for i in results if not key in i['extraInfo'] or i['quality_rank'] >= hevc_max_quality]
		if enable_setting == 1:
			if key == dolby_vision_filter_key and self.hybrid_allowed:
				results = [i for i in results if all(x in i['extraInfo'] for x in (key, hdr_filter_key)) or not key in i['extraInfo']]
			else: results = [i for i in results if not key in i['extraInfo']]
		elif enable_setting == 2 and self.autoplay:
			priority_list = [i for i in results if key in i['extraInfo']]
			remainder_list = [i for i in results if not i in priority_list]
			results = priority_list + remainder_list
		return results

	def _grab_meta(self):
		meta_user_info = metadata_user_info()
		if self.media_type == 'movie': self.meta = metadata.movie_meta('tmdb_id', self.tmdb_id, meta_user_info, get_datetime())
		else:
			self.meta = metadata.tvshow_meta('tmdb_id', self.tmdb_id, meta_user_info, get_datetime())
			episodes_data = metadata.season_episodes_meta(self.season, self.meta, meta_user_info)
			try:
				episode_data = [i for i in episodes_data if i['episode'] == self.episode][0]
				self.meta.update({'media_type': 'episode', 'season': episode_data['season'], 'episode': episode_data['episode'], 'premiered': episode_data['premiered'],
								'ep_name': episode_data['title'], 'plot': episode_data['plot']})
			except: pass

	def _get_module(self, module_type, function):
		if module_type == 'external': module = function.source(*self.external_args)
		elif module_type == 'folders': module = function[0](*function[1])
		else: module = function()
		return module

	def _clear_properties(self):
		for item in default_internal_scrapers: clear_property(int_window_prop % item)
		if self.active_folders:
			for item in self.folder_info: clear_property(int_window_prop % item[0])

	def _make_progress_dialog(self):
		self.progress_dialog = confirm_progress_media(meta=self.meta, enable_fullscreen=True)

	def _make_resolve_dialog(self):
		self.resolve_dialog_made = True
		if not self.progress_dialog: self._make_progress_dialog()
		self.progress_dialog.enable_resolver()

	def _kill_progress_dialog(self):
		try: self.progress_dialog.close()
		except: close_all_dialog()
		try: del self.progress_dialog
		except: pass
		self.progress_dialog = None

	def furkPacks(self, name, file_id, download=False):
		from apis.furk_api import FurkAPI
		show_busy_dialog()
		t_files = FurkAPI().t_files(file_id)
		t_files = [i for i in t_files if 'video' in i['ct'] and 'bitrate' in i]
		t_files.sort(key=lambda k: k['name'].lower())
		hide_busy_dialog()
		if download: return t_files
		default_furk_icon = get_icon('furk')
		list_items = [{'line1': '%.2f GB | %s' % (float(item['size'])/1073741824, clean_file_name(item['name']).upper()), 'icon': default_furk_icon} for item in t_files]
		kwargs = {'items': json.dumps(list_items), 'heading': name, 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
		chosen_result = select_dialog(t_files, **kwargs)
		if chosen_result is None: return None
		link = chosen_result['url_dl']
		name = chosen_result['name']
		return self.player.run(link, 'video')

	def debridPacks(self, debrid_provider, name, magnet_url, info_hash, download=False):
		show_busy_dialog()
		debrid_info = {'Real-Debrid': ('rd_browse', 'realdebrid'), 'Premiumize.me': ('pm_browse', 'premiumize'), 'AllDebrid': ('ad_browse', 'alldebrid')}[debrid_provider]
		debrid_function = self.debrid_importer(debrid_info[0])
		try: debrid_files = debrid_function().display_magnet_pack(magnet_url, info_hash)
		except: debrid_files = None
		debrid_files = debrid_function().display_magnet_pack(magnet_url, info_hash)
		hide_busy_dialog()
		if not debrid_files: return notification(32574)
		debrid_files.sort(key=lambda k: k['filename'].lower())
		if download: return debrid_files, debrid_function
		icon = get_icon(debrid_info[1])
		list_items = [{'line1': '%.2f GB | %s' % (float(item['size'])/1073741824, clean_file_name(item['filename']).upper()), 'icon': icon} for item in debrid_files]
		kwargs = {'items': json.dumps(list_items), 'heading': name, 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
		chosen_result = select_dialog(debrid_files, **kwargs)
		if chosen_result is None: return None
		link = self.resolve_internal_sources(debrid_info[0], chosen_result['link'], '')
		name = chosen_result['filename']
		return self.player.run(link, 'video')

	def play_file(self, results, source={}, autoplay=False, background=False):
		hide_busy_dialog()
		playback_successful = False
		try:
			if autoplay:
				items = [i for i in results if not 'Uncached' in i.get('cache_provider', '')]
			elif source:
				results = [i for i in results if not 'Uncached' in i.get('cache_provider', '') or i == source]
				source_index = results.index(source)
				leading_index = max(source_index-3, 0)
				items_prev = results[leading_index:source_index]
				trailing_index = 7 - len(items_prev)
				items_next = results[source_index+1:source_index+trailing_index]
				items = [source] + items_next + items_prev
			else: items = results
			first_item = items[0]
			if 'Uncached' in first_item.get('cache_provider', ''):
				self._kill_progress_dialog()
				return self.resolve_uncached_torrents(first_item['debrid'], first_item['url'], 'package' in first_item)
			if not self.continue_resolve_check(): return self._kill_progress_dialog()
			if not self.resolve_dialog_made: self._make_resolve_dialog()
			monitor = kodi_utils.monitor
			easynews_retry, url = False, None
			hide_busy_dialog()
			for count, item in enumerate(items, 1):
				hide_busy_dialog()
				playback_successful, url = False, None
				provider = item['scrape_provider']
				try:
					if provider == 'external': provider = item['debrid'].replace('.me', '').upper()
					elif provider == 'folders': provider = item['source'].upper()
					else: provider = provider.upper()
					text = ('%02d. [B]%s[/B]'% (count, provider), item['display_name'].upper())
					if self.progress_dialog.iscanceled() or monitor.abortRequested(): break
					try: self.progress_dialog.update_resolver(text)
					except: pass
					url = self.resolve_sources(item)
					if url:
						if self.progress_dialog.iscanceled() or monitor.abortRequested(): break
						sleep(1000)
						playback_successful = self.player.run(url, self)
				except: pass
				if playback_successful:
					clear_property('fen.playback_check')
					break
				if provider == 'EASYNEWS':
					if not easynews_retry:
						easynews_retry = True
						try:
							text = ('%02d. [B]%s (RETRY)[/B]'% (count, provider), item['display_name'].upper())
							try: self.progress_dialog.update_resolver(text)
							except: pass
							url = self.resolve_sources(item)
							if url:
								if self.progress_dialog.iscanceled() or monitor.abortRequested(): break
								sleep(1000)
								playback_successful = self.player.run(url, self)
							if playback_successful: break
						except: pass
					else: easynews_retry = False
				if count == len(items): self.player.stop()
		except: pass
		try: del monitor
		except: pass
		if not playback_successful or not url: self.playback_failed_action()

	def playback_failed_action(self):
		self._kill_progress_dialog()
		if self.prescrape and self.autoplay:
			self.resolve_dialog_made, self.prescrape, self.prescrape_sources = False, False, []
			self.get_sources()
		else: notification(32121, 3500)

	def continue_resolve_check(self):
		try:
			if not self.background: return True
			if self.play_type == 'next_episode': return self.next_episode_handler()
			else: return self.random_continual_handler()
		except: return False

	def random_continual_handler(self):
		notification('%s %s S%02dE%02d' % (ls(32801), self.meta.get('title'), self.meta.get('season'), self.meta.get('episode')), 6500, self.meta.get('poster'))
		while self.player.isPlayingVideo(): sleep(100)
		self._make_resolve_dialog()
		return True

	def next_episode_handler(self):
		if not self.nextep_settings: return False
		if self.player.isPlayingVideo():
			action = None
			total_time = self.player.getTotalTime()
			use_window = self.nextep_settings['use_window']
			window_time = self.nextep_settings['window_time']
			default_action = self.nextep_settings['default_action']
			while self.player.isPlayingVideo():
				try:
					sleep(100)
					curr_time = self.player.getTime()
					if round(total_time - curr_time) <= window_time:
						if use_window:
							action = open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=self.meta, default_action=default_action)
						else:
							notification('%s %s S%02dE%02d' % (ls(32801), self.meta.get('title'), self.meta.get('season'), self.meta.get('episode')), 6500, self.meta.get('poster'))
						break
				except: pass
			if not action: action = default_action
			if action == 'cancel':
				notification('%s %s' % (ls(32483), ls(32736)), 3000)
				return False
			else:
				if action == 'play':
					self._make_resolve_dialog()
					self.player.stop()
				else:
					while self.player.isPlayingVideo(): sleep(100)
					self._make_resolve_dialog()
				return True
		else: return False

	def resolve_sources(self, item, meta=None):
		if meta: self.meta = meta
		try:
			if 'cache_provider' in item:
				cache_provider = item['cache_provider']
				if self.meta['media_type'] == 'episode': title, season, episode, pack = self.get_ep_name(), self.get_search_season(), self.get_search_episode(), 'package' in item
				else: title, season, episode, pack = self.get_search_title(), None, None, False
				if cache_provider in debrid_providers:
					url = self.resolve_cached_torrents(cache_provider, item['url'], item['hash'], title, season, episode, pack)
					return url
			if item.get('scrape_provider', None) in default_internal_scrapers:
				url = self.resolve_internal_sources(item['scrape_provider'], item['id'], item['url_dl'], item.get('direct_debrid_link', False))
				return url
			if item.get('debrid') in debrid_providers and not item['source'].lower() == 'torrent':
				url = self.resolve_debrid(item['debrid'], item['provider'], item['url'])
				if url is not None: return url
				else: return None
			else:
				url = item['url']
				return url
		except: return

	def debrid_importer(self, debrid_provider):
		return manual_function_import(*debrids[debrid_provider])

	def resolve_cached_torrents(self, debrid_provider, item_url, _hash, title, season, episode, pack):
		url = None
		debrid_function = self.debrid_importer(debrid_provider)
		store_to_cloud = settings.store_resolved_torrent_to_cloud(debrid_provider, pack)
		try: url = debrid_function().resolve_magnet(item_url, _hash, store_to_cloud, title, season, episode)
		except: pass
		return url

	def resolve_uncached_torrents(self, debrid_provider, item_url, pack):
		if not confirm_dialog(text=ls(32831) % debrid_provider.upper()): return None
		debrid_function = self.debrid_importer(debrid_provider)
		try: debrid_function().add_uncached_torrent(item_url, pack)
		except: return notification(32490, 3500)

	def resolve_debrid(self, debrid_provider, item_provider, item_url):
		url = None
		debrid_function = self.debrid_importer(debrid_provider)
		try: url = debrid_function().unrestrict_link(item_url)
		except: pass
		return url

	def resolve_internal_sources(self, scrape_provider, item_id, url_dl, direct_debrid_link=False):
		url = None
		try:
			if direct_debrid_link: return url_dl
			if scrape_provider == 'furk':
				from indexers.furk import t_file_browser
				url = t_file_browser(item_id, self.meta['media_type'], self.meta['season'], self.meta['episode'])
			elif scrape_provider == 'easynews':
				from indexers.easynews import resolve_easynews
				url = resolve_easynews({'url_dl': url_dl, 'play': 'false'})
			elif scrape_provider == 'folders': url = url_dl
			else:
				debrid_function = self.debrid_importer(scrape_provider)
				if any(i in scrape_provider for i in ('rd_', 'ad_')):
					url = debrid_function().unrestrict_link(item_id)
				else:
					if '_cloud' in scrape_provider: item_id = debrid_function().get_item_details(item_id)['link']
					url = debrid_function().add_headers_to_url(item_id)
		except: pass
		return url
