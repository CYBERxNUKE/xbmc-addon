# -*- coding: utf-8 -*-
from apis.premiumize_api import PremiumizeAPI
from modules.source_utils import get_file_info, supported_video_extensions, internal_results, check_title, \
								get_aliases_titles, seas_ep_filter, release_info_format
from modules.utils import clean_title, clean_file_name, normalize
from modules.settings import enabled_debrids_check, filter_by_name
# from modules.kodi_utils import logger

Premiumize = PremiumizeAPI()

class source:
	def __init__(self):
		self.scrape_provider = 'pm_cloud'

	def results(self, info):
		try:
			if not enabled_debrids_check('pm'): return internal_results(self.scrape_provider, self.sources)
			self.title_filter = filter_by_name(self.scrape_provider)
			self.sources, self.scrape_results = [], []
			self.db_type = info.get('db_type')
			self.title = info.get('title')
			self.year = info.get('year')
			if self.year: self.rootname = '%s (%s)' % (self.title, self.year)
			else: self.rootname = self.title
			self.season = info.get('season')
			self.episode = info.get('episode')
			self.query = clean_title(self.title)
			self.extensions = supported_video_extensions()
			self._scrape_cloud()
			if not self.scrape_results: return internal_results(self.scrape_provider, self.sources)
			self.aliases = get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = normalize(item['name'])
						if self.title_filter:
							if not check_title(self.title, file_name, self.aliases, self.year, self.season, self.episode): continue
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						path = item['path']
						file_dl = item['id']
						size = round(float(item['size'])/1073741824, 2)
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
			logger('FEN premiumize scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _scrape_cloud(self):
		try:
			cloud_files = Premiumize.user_cloud_all()['files']
			cloud_files = [i for i in cloud_files if i['path'].lower().endswith(tuple(self.extensions))]
			cloud_files.sort(key=lambda k: k['name'])
		except: return self.sources
		append = self.scrape_results.append
		for item in cloud_files:
			normalized = normalize(item['name'])
			item_name = clean_title(normalized)
			if self.query in item_name:
				if self.db_type == 'movie':
					if any(x in item['name'] for x in self._year_query_list()): append(item)
				elif seas_ep_filter(self.season, self.episode, normalized): append(item)

	def _year_query_list(self):
		return [str(self.year), str(int(self.year)+1), str(int(self.year)-1)]
