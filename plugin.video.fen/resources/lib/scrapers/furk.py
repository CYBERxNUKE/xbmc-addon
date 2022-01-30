# -*- coding: utf-8 -*-
from apis.furk_api import FurkAPI
from modules.source_utils import get_file_info, internal_results, check_title, get_aliases_titles, release_info_format
from modules.utils import clean_file_name, normalize
from modules.settings import filter_by_name
# from modules.kodi_utils import logger

Furk = FurkAPI()

class source:
	def __init__(self):
		self.scrape_provider = 'furk'
		self.title_filter = filter_by_name('furk')
		self.sources = []

	def results(self, info):
		try:
			self.info = info
			self.title = self.info.get('title')
			self.search_title = clean_file_name(self.title).replace(' ', '+').replace('&', 'and')
			self.db_type = self.info.get('db_type')
			self.year = self.info.get('year')
			self.season = self.info.get('season')
			self.episode = self.info.get('episode')
			search_name = self._search_name()
			files = Furk.search(search_name)
			if not files: return internal_results(self.scrape_provider, self.sources)
			cached_files = [i for i in files if i.get('type') not in ('default', 'audio', '') and i.get('is_ready') == '1']
			self.aliases = get_aliases_titles(info.get('aliases', []))
			def _process():
				for i in cached_files:
					try:
						size = round(float(int(i['size']))/1073741824, 2)
						if self.info.get('db_type') == 'movie': files_num_video = 1
						else: files_num_video = int(i['files_num_video'])
						if files_num_video > 3:
							package = 'true'
							size = float(size)/files_num_video
						else: package = 'false'
						file_name = normalize(i['name'])
						if self.title_filter and package == 'false':
							if not check_title(self.title, file_name, self.aliases, self.year, self.season, self.episode): continue
						file_id = i['id']
						file_dl = i['url_dl']
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						video_quality, details = get_file_info(name_info=release_info_format(file_name))
						source_item = {'name': file_name,
										'title': file_name,
										'URLName': URLName,
										'quality': video_quality,
										'size': size,
										'size_label': '%.2f GB' % size,
										'extraInfo': details,
										'url_dl': file_dl,
										'id': file_id,
										'local': False,
										'direct': True,
										'package': package,
										'source': self.scrape_provider,
										'scrape_provider': self.scrape_provider}
						yield source_item
					except Exception as e:
						from modules.kodi_utils import logger
						logger('FURK ERROR - 65', e)
			self.sources = list(_process())
		except Exception as e:
			from modules.kodi_utils import logger
			logger('FEN furk scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _search_name(self):
		if self.db_type == 'movie': return '@name+%s+%d+|+%d+|+%d' % (self.search_title, self.year - 1, self.year, self.year + 1)
		else: return '@name+%s+@files+%s+|+%s+|+%s+|+%s+|+%s+|+%s+|+%s' % self.tvshow_query()

	def tvshow_query(self):
		return (self.search_title,
				's%de%02d' % (self.season, self.episode),
				's%02de%02d' % (self.season, self.episode),
				'%dx%02d' % (self.season, self.episode),
				'%02dx%02d' % (self.season, self.episode),
				'"season %d episode %d"' % (self.season, self.episode),
				'"season %d episode %02d"' % (self.season, self.episode),
				'"season %02d episode %02d"' % (self.season, self.episode))
