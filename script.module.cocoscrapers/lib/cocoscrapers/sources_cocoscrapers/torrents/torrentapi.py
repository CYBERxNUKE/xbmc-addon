# -*- coding: utf-8 -*-
# modified by Venom for Fenomscrapers (updated 7-19-2022)
"""
	Fenomscrapers Project
"""

import re
from urllib.parse import unquote_plus
from cocoscrapers.modules import cache
from cocoscrapers.modules import cfscrape
from cocoscrapers.modules import source_utils


class source:
	priority = 1
	pack_capable = True
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "https://torrentapi.org" # just to satisfy scraper_test
		# self.tvsearch = "https://torrentapi.org/pubapi_v2.php?app_id=FenomScrapers&token={0}&mode=search&search_string={1}&ranked=0&limit=100&format=json_extended" # string query
		self.tvshowsearch = "https://torrentapi.org/pubapi_v2.php?app_id=FenomScrapers&token={0}&mode=search&search_imdb={1}&search_string={2}&ranked=0&limit=100&format=json_extended" # imdb_id + string query
		self.msearch = "https://torrentapi.org/pubapi_v2.php?app_id=FenomScrapers&token={0}&mode=search&search_imdb={1}&ranked=0&limit=100&format=json_extended"
		self.getToken_url = "https://torrentapi.org/pubapi_v2.php?app_id=FenomScrapers&get_token=get_token"
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'} # cfscrape has some old User-Agents that fail
		self.min_seeders = 0

	def _get_token(self):
		token = '1ujibgdf5q' # fallback
		response = self.scraper.get(self.getToken_url, headers=self.headers)
		if response.status_code in (200, 201):
			token = response.json()['token']
		else:
			from cocoscrapers.modules import log_utils
			log_utils.log('TORRENTAPI: Token Refresh Error --> %s' % str(response))
		return token

	def sources(self, data, hostDict):
		sources = []
		if not data: return sources
		sources_append = sources.append
		try:
			self.scraper = cfscrape.create_scraper()
			key = cache.get(self._get_token, 0.2) # 800secs() token is valid for
			aliases = data['aliases']
			year = data['year']
			if 'tvshowtitle' in data:
				title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ').replace('$', 's')
				episode_title = data['title']
				hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
				years = None
				search_link = self.tvshowsearch.format(key, data['imdb'], hdlr)
			else:
				title = data['title'].replace('&', 'and').replace('/', ' ').replace('$', 's')
				episode_title = None
				hdlr = year
				years = [str(int(year)-1), str(year), str(int(year)+1)]
				search_link = self.msearch.format(key, data['imdb'])
			# log_utils.log('search_link = %s' % str(search_link))
			results = self.scraper.get(search_link, headers=self.headers, timeout=5)
			if results.status_code == 200: rjson = results.json()
			else:
				from cocoscrapers.modules import log_utils
				log_utils.log('TORRENTAPI: Failed query for (%s) : %s' % (search_link, results))
				return sources
			if 'torrent_results' not in rjson: return sources
			files = rjson['torrent_results']
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('TORRENTAPI')
			return sources

		for file in files:
			try:
				url = file["download"].split('&tr')[0]
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(unquote_plus(file["title"]))

				if not source_utils.check_title(title, aliases, name, hdlr, year, years): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				if not episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
					name_lower = name.lower()
					if any(re.search(item, name_lower) for item in ep_strings): continue

				try:
					seeders = int(file["seeders"])
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils.convert_size(file["size"], to='GB')
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources_append({'provider': 'torrentapi', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
											'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('TORRENTAPI')
		return sources

	def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		sources = []
		if search_series: return sources # torrentapi does not have showPacks
		if not data: return sources
		sources_append = sources.append
		try:
			self.scraper = cfscrape.create_scraper()
			key = cache.get(self._get_token, 0.2) # 800 secs token is valid for
			title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ').replace('$', 's')
			aliases = data['aliases']
			year = data['year']
			season = data['season']
			season_xx = season.zfill(2)
			search_link = self.tvshowsearch.format(key, data['imdb'], 'S%s' % season_xx)
			results = self.scraper.get(search_link, headers=self.headers, timeout=5)
			if results.status_code == 200: rjson = results.json()
			else:
				from cocoscrapers.modules import log_utils
				log_utils.log('TORRENTAPI: Failed query for (%s) : %s' % (search_link, results))
				return sources
			if 'torrent_results' not in rjson: return sources
			files = rjson['torrent_results']
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('TORRENTAPI')
			return sources

		for file in files:
			try:
				url = file["download"].split('&tr')[0]
				hash = re.search(r'btih:(.*?)&', url, re.I).group(1)
				name = source_utils.clean_name(unquote_plus(file["title"]))

				episode_start, episode_end = 0, 0
				if not bypass_filter:
					valid, episode_start, episode_end = source_utils.filter_season_pack(title, aliases, year, season, name)
					if not valid: continue
				package = 'season'

				name_info = source_utils.info_from_name(name, title, year, season=season, pack=package)
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue
				try:
					seeders = int(file["seeders"])
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils.convert_size(file["size"], to='GB')
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'torrentapi', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if episode_start: item.update({'episode_start': episode_start, 'episode_end': episode_end}) # for partial season packs
				sources_append(item)
			except:
				source_utils.scraper_error('TORRENTAPI')
		return sources