# -*- coding: utf-8 -*-
import re
from threading import Thread
from apis.real_debrid_api import RealDebridAPI
from caches.main_cache import main_cache
from modules.source_utils import get_file_info, supported_video_extensions, internal_results, check_title, \
								get_aliases_titles, seas_ep_filter, seas_ep_query_list, release_info_format
from modules.utils import clean_title, clean_file_name, normalize
from modules.settings import enabled_debrids_check, filter_by_name
# from modules.kodi_utils import logger

RealDebrid = RealDebridAPI()

class source:
	def __init__(self):
		self.scrape_provider = 'rd_cloud'

	def results(self, info):
		try:
			if not enabled_debrids_check('rd'): return internal_results(self.scrape_provider, self.sources)
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
			self._scrape_downloads()
			self._scrape_cloud()
			if not self.scrape_results: return internal_results(self.scrape_provider, self.sources)
			self.aliases = get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = self._get_filename(item['path'])
						if self.title_filter and not 'assigned_folder' in item:
							if not check_title(self.title, file_name, self.aliases, self.year, self.season, self.episode): continue
						file_dl = item['url_link']
						direct_debrid_link = item.get('direct_debrid_link', False)
						folder_name = normalize(item['folder_name'])
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						size = round(float(item['bytes'])/1073741824, 2)
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
										'scrape_provider': self.scrape_provider,
										'direct_debrid_link': direct_debrid_link}
						yield source_item
					except: pass
			self.sources = list(_process())
		except Exception as e:
			from modules.kodi_utils import logger
			logger('FEN real-debrid scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _assigned_content(self, raw_name):
		try:
			string = 'FEN_RD_%s' % raw_name
			return main_cache.get(string)
		except:
			return False

	def _scrape_cloud(self):
		try:
			try: my_cloud_files = RealDebrid.user_cloud()
			except: return self.sources
			append = self.folder_results.append
			for item in my_cloud_files:
				normalized = normalize(item['filename'])
				folder_name = clean_title(normalized)
				assigned_content = self._assigned_content(normalized)
				if assigned_content:
					if assigned_content == self.rootname:
						append((normalized, item['id'], True))
				elif self.folder_query in folder_name or not folder_name:
					append((normalized, item['id'], False))
			if not self.folder_results: return self.sources
			threads = []
			append = threads.append
			for i in self.folder_results: append(Thread(target=self._scrape_folders, args=(i,)))
			[i.start() for i in threads]
			[i.join() for i in threads]
		except: pass

	def _scrape_folders(self, folder_info):
		try:
			assigned_folder = folder_info[2]
			folder_files = RealDebrid.user_cloud_info(folder_info[1])
			contents = [i for i in folder_files['files'] if i['path'].lower().endswith(tuple(self.extensions))]
			file_urls = folder_files['links']
			append = self.scrape_results.append
			for c, i in enumerate(contents):
				try: i.update({'folder_name': folder_info[0], 'url_link': file_urls[c]})
				except: pass
			contents.sort(key=lambda k: k['path'])
			for item in contents:
				match = False
				normalized = normalize(item['path'])
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
		except: pass

	def _scrape_downloads(self):
		try:
			my_downloads = RealDebrid.downloads()
			my_downloads = [i for i in my_downloads if i['download'].lower().endswith(tuple(self.extensions))]
			append = self.scrape_results.append
			for item in my_downloads:
				match = False
				normalized = normalize(item['filename'])
				filename = clean_title(normalized)
				if self.db_type == 'movie':
					if any(x in filename for x in self._year_query_list()): match = True
				else:
					if seas_ep_filter(self.season, self.episode, normalized):
						match = True
				if match and self.folder_query in filename:
					item = self.make_downloads_item(item)
					if item['path'] not in [d['path'] for d in self.scrape_results]: append(item)
		except: pass

	def make_downloads_item(self, item):
		downloads_item = {}
		downloads_item['folder_name'] = item['filename']
		downloads_item['url_link'] = item['download']
		downloads_item['bytes'] = item['filesize']
		downloads_item['path'] = item['filename']
		downloads_item['direct_debrid_link'] = True
		return downloads_item

	def _get_filename(self, name):
		if name.startswith('/'): name = name.split('/')[-1]
		return clean_file_name(normalize(name))

	def _year_query_list(self):
		return [str(self.year), str(int(self.year)+1), str(int(self.year)-1)]
