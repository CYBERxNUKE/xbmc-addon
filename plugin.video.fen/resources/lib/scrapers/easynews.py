# -*- coding: utf-8 -*-
import sys
from apis.easynews_api import import_easynews
from modules.source_utils import get_file_info, check_title, internal_results, get_aliases_titles, release_info_format
from modules.utils import clean_file_name, normalize
from modules.settings import filter_by_name, easynews_language_filter
# from modules.kodi_utils import logger

EasyNews = import_easynews()

class source:
	def __init__(self):
		self.scrape_provider = 'easynews'
		self.title_filter = filter_by_name('easynews')
		self.filter_lang, self.lang_filters = easynews_language_filter()
		self.sources = []

	def results(self, info):
		try:
			self.title = info.get('title')
			self.search_title = clean_file_name(self.title).replace('&', 'and')
			self.db_type = info.get('db_type')
			self.year = info.get('year')
			self.season = info.get('season')
			self.episode = info.get('episode')
			search_name = self._search_name()
			files = EasyNews.search(search_name)
			if not files: return internal_results(self.scrape_provider, self.sources)
			self.aliases = get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in files:
					try:
						file_name = normalize(item['name'])
						if self.title_filter and not check_title(self.title, file_name, self.aliases, self.year, self.season, self.episode): continue
						if self.filter_lang and not any(i in self.lang_filters for i in item['language']) : continue
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						url_dl = item['url_dl']
						size = round(float(int(item['rawSize']))/1073741824, 2)
						video_quality, details = get_file_info(name_info=release_info_format(file_name))
						source_item = {'name': file_name,
										'title': file_name,
										'URLName': URLName,
										'quality': video_quality,
										'size': size,
										'size_label': '%.2f GB' % size,
										'extraInfo': details,
										'url_dl': url_dl,
										'id': url_dl,
										'local': False,
										'direct': True,
										'source': self.scrape_provider,
										'scrape_provider': self.scrape_provider}
						yield source_item
					except Exception as e:
						from modules.kodi_utils import logger
						logger('FEN easynews scraper yield source error', str(e))
			self.sources = list(_process())
		except Exception as e:
			from modules.kodi_utils import logger
			logger('FEN easynews scraper Exception', str(e))
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _search_name(self):
		if self.db_type == 'movie': return '"%s" %d,%d,%d' % (self.search_title, self.year-1, self.year, self.year+1)
		else: return '%s S%02dE%02d' % (self.search_title,  self.season, self.episode)

	def to_bytes(self, num, unit):
		unit = unit.upper()
		if unit.endswith('B'): unit = unit[:-1]
		units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
		try: mult = pow(1024, units.index(unit))
		except: mult = sys.maxint
		return int(float(num) * mult)

