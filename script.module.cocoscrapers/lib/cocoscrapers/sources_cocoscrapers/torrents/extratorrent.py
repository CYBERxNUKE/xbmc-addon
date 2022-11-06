# -*- coding: utf-8 -*-
# created by Venom for Fenomscrapers (updated 7-19-2022)
"""
	Fenomscrapers Project
"""

import re
from urllib.parse import quote_plus, unquote_plus
# from cocoscrapers.modules import cfscrape # proxy in use not behind CloudFlare
from cocoscrapers.modules import client
from cocoscrapers.modules import source_utils
from cocoscrapers.modules import workers


class source:
	priority = 4
	pack_capable = True
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		# self.base_link = "https://extratorrent.si" # dead
		# self.base_link = "https://extratorrent.proxyninja.org" #v2 challenge now, tested 2-26-22
		self.base_link = "https://extratorrent.unblockit.name" # 6-28-22
		self.msearch_link = '/search/?new=1&search=%s&s_cat=1'
		self.tvsearch_link = '/search/?new=1&search=%s&s_cat=2'
		# self.packsearch_link = '/search/?page=2&new=1&search=%s&s_cat=2' # page1 appears broken, scrape page2 only for packs
		self.min_seeders = 1

	def sources(self, data, hostDict):
		self.sources = []
		if not data: return self.sources
		self.sources_append = self.sources.append
		try:
			# self.scraper = cfscrape.create_scraper()
			self.aliases = data['aliases']
			self.year = data['year']
			if 'tvshowtitle' in data:
				self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ').replace('$', 's')
				self.episode_title = data['title']
				self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
				search_link = self.tvsearch_link
			else:
				self.title = data['title'].replace('&', 'and').replace('/', ' ').replace('$', 's')
				self.episode_title = None
				self.hdlr = self.year
				search_link = self.msearch_link
			query = '%s %s' % (re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title), self.hdlr)
			urls = []
			url = '%s%s' % (self.base_link, search_link % quote_plus(query))
			urls.append(url)
			urls.append('%s%s' % (url, '&page=2')) # next page seems to be working once again
			# log_utils.log('urls = %s' % urls)
			self.undesirables = source_utils.get_undesirables()
			self.check_foreign_audio = source_utils.check_foreign_audio()
			threads = []
			append = threads.append
			for url in urls:
				append(workers.Thread(self.get_sources, url))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return self.sources

	def get_sources(self, url):
		try:
			# results = self.scraper.get(url, timeout=10).text
			results = client.request(url, timeout=10)
			if not results: return
			rows = client.parseDOM(results, 'tr', attrs={'class': 'tlr'})
			rows += client.parseDOM(results, 'tr', attrs={'class': 'tlz'})
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return

		for row in rows:
			try:
				row = re.sub(r'\n', '', row)
				row = re.sub(r'\t', '', row)
				columns = re.findall(r'<td.*?>(.+?)</td>', row, re.DOTALL)

				url = re.search(r'href\s*=\s*["\'](magnet:[^"\']+)["\']', columns[0], re.I).group(1)
				url = unquote_plus(url).replace('&amp;', '&').replace('&amp;', '&').replace(' ', '.').split('&tr')[0] # some links on extratorrent dbl "&amp;amp;"
				url = source_utils.strip_non_ascii_and_unprintable(url)
				if url in str(self.sources): continue
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(url.split('&dn=')[1])

				if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): continue
				name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
				if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
				if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

				if not self.episode_title: # filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
					name_lower = name.lower()
					if any(re.search(item, name_lower) for item in ep_strings): continue

				try:
					seeders = int(columns[4].replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils._size(columns[3])
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				self.sources_append({'provider': 'extratorrent', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
												'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('EXTRATORRENT')

	def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		self.sources = []
		if not data: return self.sources
		self.sources_append = self.sources.append
		try:
			# self.scraper = cfscrape.create_scraper()
			self.search_series = search_series
			self.total_seasons = total_seasons
			self.bypass_filter = bypass_filter

			self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU')
			self.aliases = data['aliases']
			self.imdb = data['imdb']
			self.year = data['year']
			self.season_x = data['season']
			self.season_xx = self.season_x.zfill(2)
			self.undesirables = source_utils.get_undesirables()
			self.check_foreign_audio = source_utils.check_foreign_audio()

			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title)
			if search_series:
				queries = [
						self.tvsearch_link % quote_plus(query + ' Season'),
						self.tvsearch_link % quote_plus(query + ' Complete')]
			else:
				queries = [
						self.tvsearch_link % quote_plus(query + ' S%s' % self.season_xx),
						self.tvsearch_link % quote_plus(query + ' Season %s' % self.season_x)]
			threads = []
			append = threads.append
			for url in queries:
				link = '%s%s' % (self.base_link, url)
				append(workers.Thread(self.get_sources_packs, link))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return self.sources

	def get_sources_packs(self, link):
		try:
			# log_utils.log('link = %s' % link)
			# results = self.scraper.get(link, timeout=10).text
			results = client.request(link, timeout=10)
			if not results: return
			rows = client.parseDOM(results, 'tr', attrs={'class': 'tlr'})
			rows += client.parseDOM(results, 'tr', attrs={'class': 'tlz'})
		except:
			source_utils.scraper_error('EXTRATORRENT')
			return
		for row in rows:
			try:
				row = re.sub(r'\n', '', row)
				row = re.sub(r'\t', '', row)
				columns = re.findall(r'<td.*?>(.+?)</td>', row, re.DOTALL)
				url = re.search(r'href\s*=\s*["\'](magnet:[^"\']+)["\']', columns[0], re.I).group(1)
				url = unquote_plus(url).replace('&amp;', '&').replace('&amp;', '&').replace(' ', '.').split('&tr')[0] # some links on extratorrent dbl "&amp;amp;"
				url = source_utils.strip_non_ascii_and_unprintable(url)
				if url in str(self.sources): continue
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(url.split('&dn=')[1])

				episode_start, episode_end = 0, 0
				if not self.search_series:
					if not self.bypass_filter:
						valid, episode_start, episode_end = source_utils.filter_season_pack(self.title, self.aliases, self.year, self.season_x, name)
						if not valid: continue
					package = 'season'

				elif self.search_series:
					if not self.bypass_filter:
						valid, last_season = source_utils.filter_show_pack(self.title, self.aliases, self.imdb, self.year, self.season_x, name, self.total_seasons)
						if not valid: continue
					else: last_season = self.total_seasons
					package = 'show'

				name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
				if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
				if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

				try:
					seeders = int(columns[4].replace(',', ''))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils._size(columns[3])
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'extratorrent', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if self.search_series: item.update({'last_season': last_season})
				elif episode_start: item.update({'episode_start': episode_start, 'episode_end': episode_end}) # for partial season packs
				self.sources_append(item)
			except:
				source_utils.scraper_error('EXTRATORRENT')