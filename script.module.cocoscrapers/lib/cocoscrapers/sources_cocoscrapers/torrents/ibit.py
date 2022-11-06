# -*- coding: utf-8 -*-
# created by Venom for Fenomscrapers (updated 7-19-2022)
"""
	Fenomscrapers Project
"""

import re
from urllib.parse import quote_plus, unquote_plus
from cocoscrapers.modules import cfscrape
from cocoscrapers.modules import client
from cocoscrapers.modules import source_utils
from cocoscrapers.modules import workers
_DATA = re.compile(r'<a\s*href\s*=\s*["\'](/torrent/.+?/)["\']\s*title\s*=\s*["\'](.+?)["\'].*?<td\s*class\s*=\s*["\']digits["\']>(.*?)<.*?<td\s*class\s*=["\']digits["\']\s*data-title\s*=\s*["\']S["\']>(.*?)</td>', re.I)


class source:
	priority = 7
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "https://ibit.to"
		self.tvsearch = "/torrent-search/{0}/TV/size:desc/1/"
		self.moviesearch = "/torrent-search/{0}/Movies/size:desc/1/"
		self.min_seeders = 0

	def sources(self, data, hostDict):
		self.sources = []
		if not data: return self.sources
		self.sources_append = self.sources.append
		try:
			self.scraper = cfscrape.create_scraper()
			self.aliases = data['aliases']
			self.year = data['year']
			if 'tvshowtitle' in data:
				self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ').replace('$', 's')
				self.episode_title = data['title']
				self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
				search_link = self.tvsearch
			else:
				self.title = data['title'].replace('&', 'and').replace('/', ' ').replace('$', 's')
				self.episode_title = None
				self.hdlr = self.year
				search_link = self.moviesearch
			query = '%s %s' % (re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title), self.hdlr)
			url = '%s%s' % (self.base_link, search_link.format(quote_plus(query)))
			# log_utils.log('url = %s' % url)
			results = self.scraper.get(url, timeout=5).text
			if not results or '<tbody' not in results: return
			rows = client.parseDOM(results, 'tr')
			self.undesirables = source_utils.get_undesirables()
			self.check_foreign_audio = source_utils.check_foreign_audio()
			threads = []
			append = threads.append
			for row in rows:
				append(workers.Thread(self.get_sources, row))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('IBIT')
			return self.sources

	def get_sources(self, row):
		row = re.sub(r'[\n\t]', '', row)
		data = _DATA.findall(row)
		if not data: return
		for items in data:
			try:
				link = '%s%s' % (self.base_link, items[0])
				result = self.scraper.get(link, timeout=10).text
				if not result: continue

				try: url = unquote_plus(re.search(r'(magnet:.*?)["\']', result).group(1).replace('\\x26', '&').replace('\\x2b', '+').replace('X-X', '')).split('&tr=')[0]
				except: continue
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(url.split('&dn=')[1])

				if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): continue
				name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
				if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
				if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

				if not self.episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
					name_lower = name.lower()
					if any(re.search(item, name_lower) for item in ep_strings): continue

				try:
					seeders = int(items[3].replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils._size(items[2])
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				self.sources_append({'provider': 'ibit', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
													'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('IBIT')