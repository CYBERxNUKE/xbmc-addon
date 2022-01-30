# -*- coding: utf-8 -*-
import os
from threading import Thread
from urllib.parse import urlparse
from caches.main_cache import main_cache, cache_object
from modules.source_utils import get_file_info, supported_video_extensions, internal_results, check_title, \
								get_aliases_titles, seas_ep_filter, clean_title, release_info_format
from modules.kodi_utils import list_dirs, open_file
from modules.utils import clean_file_name, normalize, make_thread_list
from modules.settings import source_folders_directory, filter_by_name
# from modules.kodi_utils import logger

class source:
	def __init__(self, scrape_provider, scraper_name):
		self.scrape_provider = scrape_provider
		self.scraper_name = scraper_name
		self.title_filter = filter_by_name('folders')
		self.extensions = supported_video_extensions()
		self.sources, self.scrape_results = [], []

	def results(self, info):
		try:
			self.info = info
			self.db_type = self.info.get('db_type')
			self.folder_path = source_folders_directory(self.db_type, self.scrape_provider)
			if not self.folder_path: return internal_results(self.scraper_name, self.sources)
			self.title = self.info.get('title')
			self.year = self.info.get('year')
			if self.year: self.rootname = '%s (%s)' % (self.title, self.year)
			else: self.rootname = self.title
			self.season = self.info.get('season')
			self.episode = self.info.get('episode')
			self.title_query = clean_title(normalize(self.title))
			self.folder_query = self._season_query_list() if self.db_type == 'episode' else self._year_query_list()
			self._scrape_directory((self.folder_path, False))
			if not self.scrape_results: return internal_results(self.scraper_name, self.sources)
			self.aliases = get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = normalize(item[0])
						if self.title_filter:
							if not check_title(self.title, file_name, self.aliases, self.year, self.season, self.episode): continue
						file_dl = item[1]
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						try: size = item[2]
						except: size = self._get_size(file_dl)
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
										self.scrape_provider : True,
										'direct': True,
										'source': self.scraper_name,
										'scrape_provider': 'folders'}
						yield source_item
					except: pass
			self.sources = list(_process())
		except Exception as e:
			from modules.kodi_utils import logger
			logger('FEN folders scraper Exception', e)
		internal_results(self.scraper_name, self.sources)
		return self.sources

	def _assigned_content(self, raw_name):
		try:
			string = 'FEN_FOLDER_%s' % raw_name
			return main_cache.get(string)
		except:
			return False

	def _make_dirs(self, folder_name):
		folder_files = []
		append = folder_files.append
		dirs, files =  list_dirs(folder_name)
		for i in dirs: append((i, 'folder'))
		for i in files: append((i, 'file'))
		return folder_files

	def _scrape_directory(self, folder_info):
		def _process(item):
			file_type = item[1]
			normalized = normalize(item[0])
			item_name = clean_title(normalized)
			if file_type == 'file':
				ext = os.path.splitext(urlparse(item[0]).path)[-1].lower()
				if ext in self.extensions:
					if self.db_type == 'movie':
						if self.assigned_content or self.title_query in item_name:
							url_path = self.url_path(folder_name, item[0])
							size = self._get_size(url_path)
							scrape_results_append((item[0], url_path, size))
					else:
						if seas_ep_filter(self.season, self.episode, normalized):
							if self.assigned_content or not folder_name in self.folder_path:
								url_path = self.url_path(folder_name, item[0])
								size = self._get_size(url_path)
								scrape_results_append((item[0], url_path, size))
							elif self.title_query in item_name:
								url_path = self.url_path(folder_name, item[0])
								size = self._get_size(url_path)
								scrape_results_append((item[0], url_path, size))  
			elif file_type == 'folder':
				if not assigned_folder:
					self.assigned_content = self._assigned_content(normalize(item[0]))
					if self.assigned_content:
						if self.assigned_content == self.rootname:
							new_folder = os.path.join(folder_name, item[0])
							foler_results_append((new_folder, True))
					elif self.title_query in item_name or any(x in item_name for x in self.folder_query):
						new_folder = os.path.join(folder_name, item[0])
						foler_results_append((new_folder, self.assigned_content))
				elif assigned_folder:
					if any(x in item_name for x in self.folder_query):
						new_folder = os.path.join(folder_name, item[0])
						foler_results_append((new_folder, True))
				elif self.title_query in item_name or any(x in item_name for x in self.folder_query):
					new_folder = os.path.join(folder_name, item[0])
					foler_results_append((new_folder, self.assigned_content))
		folder_results = []
		scrape_results_append = self.scrape_results.append
		foler_results_append = folder_results.append
		assigned_folder = folder_info[1]
		self.assigned_content = assigned_folder if assigned_folder else ''
		folder_name = folder_info[0]
		string = 'fen_FOLDERSCRAPER_%s_%s' % (self.scrape_provider, folder_name)
		folder_files = cache_object(self._make_dirs, string, folder_name, json=False, expiration=4)
		folder_threads = list(make_thread_list(_process, folder_files, Thread))
		[i.join() for i in folder_threads]
		if not folder_results: return
		return self._scraper_worker(folder_results)

	def _scraper_worker(self, folder_results):
		scraper_threads = list(make_thread_list(self._scrape_directory, folder_results, Thread))
		[i.join() for i in scraper_threads]

	def url_path(self, folder, file):
		url_path = os.path.join(folder, file)
		return url_path

	def _get_size(self, file):
		if file.endswith('.strm'): return 'strm'
		with open_file(file) as f: s = f.size()
		size = round(float(s)/1073741824, 2)
		return size

	def _year_query_list(self):
		return (str(self.year), str(int(self.year)+1), str(int(self.year)-1))

	def _season_query_list(self):
		return ['season%02d' % int(self.season), 'season%s' % self.season]
