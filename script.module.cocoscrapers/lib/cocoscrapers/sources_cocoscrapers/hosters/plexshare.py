# -*- coding: utf-8 -*-
# created by Venom for Fenomscrapers (updated 8-07-2022)
"""
	Fenomscrapers Project
"""

import re
import requests
from urllib.parse import quote
from cocoscrapers.modules.client import parseDOM, replaceHTMLCodes
from cocoscrapers.modules.control import addonEnabled, setting as getSetting
from cocoscrapers.modules import source_utils, cleantitle
PLEX_AUDIO = {'dca': 'dts', 'dca-ma': 'hdma'}


class source:
	priority = 2
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.client_id = getSetting('plex.client_id')
		self.accessToken = getSetting('plexshare.accessToken')
		self.base_link = getSetting('plexshare.url')
		self.composite_installed = addonEnabled('plugin.video.composite_for_plex')
		if self.composite_installed: self.play_link = 'plugin://plugin.video.composite_for_plex/?url=%s' % self.base_link
		else: self.play_link = self.base_link
		self.sourceTitle = getSetting('plexshare.sourceTitle')
		self.moviesearch = '/search?type=1&query=%s&year=%s&limit=100&X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % ('%s', '%s', self.client_id, self.accessToken)
		self.episodesearch = '/hubs/search?query=%s&limit=30&X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % ('%s', self.client_id, self.accessToken)
		# parentIndex = season number ; index = episode number in season
		# self.episodesearch = '/search?type=4&query=%s&parentIndex=%s&index=%s&limit=6000&X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % ('%s', '%s', '%s', self.client_id, self.accessToken)


	def sources(self, data, hostDict):
		sources = []
		if not data or not self.accessToken or not self.base_link: return sources
		sources_append = sources.append
		try:
			aliases = data['aliases']
			year = data['year']
			if 'tvshowtitle' in data:
				title, episode_title = data['tvshowtitle'], data['title']
				hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
				url = '%s%s' % (self.base_link, self.episodesearch % (quote(title+' '+episode_title)))
				years = None
			else:
				title, episode_title = data['title'], None
				hdlr = year
				url = '%s%s' % (self.base_link, self.moviesearch % (quote(title), year))
				years = [str(int(year)-1), str(year), str(int(year)+1)]
			
			#log_utils.log('url = %s' % url)

			try: results = requests.get(url)
			except requests.exceptions.SSLError: results = requests.get(url, verify=False)

			if episode_title: results = re.findall(r'(<Video.+?type="episode".+?</Video>)', results.text, flags=re.M | re.S)
			else: results = re.findall(r'(<Video.+?type="movie".+?</Video>)', results.text, flags=re.M | re.S)

			# undesirables = source_utils.get_undesirables()
			# check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('PLEXSHARE')
			return sources

		for result in results:
			try:
				name = cleantitle.normalize(replaceHTMLCodes(parseDOM(result, 'Part', ret='file')[0].replace(' ', '.')))
				if '/' in name: name = name.rsplit('/', 1)[1]
				elif '\\' in name: name = name.rsplit('\\', 1)[1]
				if not episode_title:
					source_year = re.search(r'(?:19|20)[0-9]{2}', name)
					if not source_year:
						source_year = parseDOM(result, 'Video', ret='year')[0]
						name = name.rsplit('.', 1)
						name = '%s.%s.%s' % (name[0], source_year, name[1])
				file_name = name

				if cleantitle.get(title.replace('&', 'and')) not in cleantitle.get(name.replace('&', 'and')): # use meta title in case file naming is whacked
					if not episode_title:
						meta_title = cleantitle.normalize(replaceHTMLCodes(parseDOM(result, 'Video', ret='title')[0].replace(' ', '.')))
						meta_year = parseDOM(result, 'Video', ret='year')[0]
						name = '%s.%s' % (meta_title, meta_year)
					else:
						meta_title = cleantitle.normalize(replaceHTMLCodes(parseDOM(result, 'Video', ret='grandparentTitle')[0].replace('&amp;', '&').replace(' ', '.')))
						meta_season, meta_episode = parseDOM(result, 'Video', ret='parentIndex')[0], parseDOM(result, 'Video', ret='index')[0]
						name = '%s.%s' % (meta_title, 'S%02dE%02d' % (int(meta_season), int(meta_episode)))

				if not source_utils.check_title(title, aliases, name, hdlr, year, years): continue
				name_info = source_utils.info_from_name(file_name, title, year, hdlr)
				# if source_utils.remove_lang(name_info, check_foreign_audio): continue
				# if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				if not name_info or len(name_info) <= 5: # use meta info because file name lacks info, or has video extension only
					quality = parseDOM(result, 'Media', ret='videoResolution')[0]
					video_codec = parseDOM(result, 'Media', ret='videoCodec')[0]
					audio_codec = parseDOM(result, 'Media', ret='audioCodec')[0]
					try:
						if audio_codec.startswith('dca'): audio_codec = PLEX_AUDIO.get(audio_codec)
					except: pass
					audio_channels = parseDOM(result, 'Media', ret='audioChannels')[0]
					container = parseDOM(result, 'Media', ret='container')[0]
					name_info = '.' + quality + '.' + video_codec + '.' + audio_codec + '.' + audio_channels + 'ch.' + container

				if self.composite_installed:
					key = parseDOM(result, 'Video', ret='key')[0]
					url = '%s%s?X-Plex-Client-Identifier=%s&X-Plex-Token=%s&mode=5' % (self.play_link, key, self.client_id, self.accessToken)
				else:
					key = parseDOM(result, 'Part', ret='key')[0].rsplit('/', 1)[0] # remove "/file.mkv" to replace with true file name for dnld
					url = '%s%s/%s?X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % (self.play_link, key, file_name, self.client_id, self.accessToken)

				size = parseDOM(result, 'Part', ret='size')[0]
				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					dsize, isize = source_utils.convert_size(float(size), to='GB')
					if isize: info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				sources_append({'provider': 'plexshare', 'plexsource': self.sourceTitle, 'source': 'direct', 'name': file_name, 'name_info': name_info,
								'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False, 'size': dsize})
			except:
				source_utils.scraper_error('PLEXSHARE')
		return sources