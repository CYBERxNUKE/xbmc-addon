# -*- coding: utf-8 -*-
from threading import Thread
from apis.alldebrid_api import AllDebridAPI
from caches.main_cache import main_cache
from modules.source_utils import get_file_info, supported_video_extensions, internal_results, clean_title, \
							check_title, get_aliases_titles, seas_ep_filter, seas_ep_query_list, release_info_format
from modules.utils import clean_file_name, normalize
from modules.settings import enabled_debrids_check, filter_by_name
# from modules.kodi_utils import logger

AllDebrid = AllDebridAPI()

class source:
	def __init__(self):
		self.scrape_provider = 'ad_cloud'

	def results(self, info):
		try:
			if not enabled_debrids_check('ad'): return internal_results(self.scrape_provider, self.sources)
			self.title_filter = filter_by_name(self.scrape_provider)
			self.sources, self.folder_results, self.scrape_results = [], [], []
			self.db_type = info.get('db_type')
			self.title = info.get('title')
			self.year = info.get('year')
			if self.year: self.rootname = '%s (%s)' % (self.title, self.year)
			else: self.rootname = self.title
			self.season = info.get('season')
			self.episode = info.get('episode')
			if self.db_type == 'episode': self.seas_ep_query_list = seas_ep_query_list(self.season, self.episode)
			self.extensions = supported_video_extensions()
			self.folder_query = clean_title(normalize(self.title))
			self._scrape_cloud()
			if not self.scrape_results: return internal_results(self.scrape_provider, self.sources)
			self.aliases = get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = normalize(item['filename'])
						if self.title_filter and not 'assigned_folder' in item:
							if not check_title(self.title, file_name, self.aliases, self.year, self.season, self.episode): continue
						file_dl = item['link']
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						size = round(float(int(item['size']))/1073741824, 2)
						video_quality, details = get_file_info(name_info=release_info_format(file_name))
						source_item = {'name': file_name,
										'title': file_name,
										'URLName': URLName,
										'quality': video_quality,
										'size': size,
										'size_label': '%.2f GB' % size,
										'extraInfo': details,
										'url_dl': file_dl,
										'id': file_dl,
										'downloads': False,
										'direct': True,
										'source': self.scrape_provider,
										'scrape_provider': self.scrape_provider}
						yield source_item
					except: pass
			self.sources = list(_process())
		except Exception as e:
				from modules.kodi_utils import logger
				logger('FEN alldebrid scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _assigned_content(self, raw_name):
		try:
			string = 'FEN_AD_%s' % raw_name
			return main_cache.get(string)
		except:
			return False

	def _scrape_cloud(self):
		try:
			threads = []
			results_append = self.folder_results.append
			append = threads.append
			try: my_cloud_files = AllDebrid.user_cloud()['magnets']
			except: return self.sources
			my_cloud_files = [i for i in my_cloud_files if i['statusCode'] == 4]
			for item in my_cloud_files:
				folder_name = clean_title(normalize(item['filename']))
				assigned_content = self._assigned_content(normalize(item['filename']))
				if assigned_content:
					if assigned_content == self.rootname:
						results_append((normalize(item['filename']), item, True))
				elif self.folder_query in folder_name or not folder_name:
					results_append((normalize(item['filename']), item, False))
			if not self.folder_results: return self.sources
			for i in self.folder_results: append(Thread(target=self._scrape_folders, args=(i,)))
			[i.start() for i in threads]
			[i.join() for i in threads]
		except: pass

	def _scrape_folders(self, folder_info):
		try:
			assigned_folder = folder_info[2]
			torrent_folder = folder_info[1]
			links = torrent_folder['links']
			append = self.scrape_results.append
			links = [i for i in links if i['filename'].lower().endswith(tuple(self.extensions))]
			for item in links:
				match = False
				normalized = normalize(item['filename'])
				filename = clean_title(normalized)
				if assigned_folder and self.db_type == 'movie': match = True
				else:
					if self.db_type == 'movie':
						if any(x in filename for x in self._year_query_list()) and self.folder_query in filename: match = True
					else:
						if assigned_folder:
							if any(x in normalized.lower() for x in self.seas_ep_query_list): match = True
						elif seas_ep_filter(self.season, self.episode, normalized): match = True
				if match:
					if assigned_folder: item['assigned_folder'] = True
					append(item)
		except: return

	def _year_query_list(self):
		return [str(self.year), str(int(self.year)+1), str(int(self.year)-1)]
