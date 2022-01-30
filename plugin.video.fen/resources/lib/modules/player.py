# -*- coding: utf-8 -*-
import re
import os
import json
from sys import argv
from threading import Thread
from urllib.parse import parse_qsl
from apis.opensubtitles_api import OpenSubtitlesAPI
from apis.trakt_api import make_trakt_slug
from windows import open_window
from modules import kodi_utils
from modules import settings
from modules import watched_status as indicators
from modules.meta_lists import language_choices
from modules.settings_reader import get_setting
from modules.utils import sec2time, clean_file_name, batch_replace, to_utf8
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
poster_empty = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/box_office.png')
fanart_empty = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')

class FenPlayer(kodi_utils.xbmc_player):
	def __init__ (self):
		kodi_utils.xbmc_player.__init__(self)
		self.set_resume = 5
		self.set_watched = 90
		self.media_marked = False
		self.subs_searched = False
		self.nextep_started = False
		self.nextep_info_gathered = False
		self.autoplay_nextep = settings.autoplay_next_episode()
		self.volume_check = get_setting('volumecheck.enabled', 'false') == 'true'

	def run(self, url=None, media_type=None):
		if not url: return
		try:
			if media_type in ('video', 'music'):
				playlist = kodi_utils.make_playlist(media_type)
				playlist.clear()
				listitem = kodi_utils.make_listitem()
				listitem.setInfo(type=media_type, infoLabels={})
				playlist.add(url, listitem)
				kodi_utils.close_all_dialog()
				return self.play(playlist)
			self.meta = json.loads(kodi_utils.get_property('fen_playback_meta'))
			background = self.meta.get('background', False) == True
			library_item = True if 'from_library' in self.meta else False
			if library_item: bookmark = self.bookmarkLibrary()
			else: bookmark = self.bookmarkFen()
			if bookmark == 'cancel': return
			self.meta.update({'url': url, 'bookmark': bookmark})
			try:
				poster_main, poster_backup, fanart_main, fanart_backup = settings.get_art_provider()
				poster = self.meta.get(poster_main) or self.meta.get(poster_backup) or poster_empty
				fanart = self.meta.get(fanart_main) or self.meta.get(fanart_backup) or fanart_empty
				listitem = kodi_utils.make_listitem()
				listitem.setPath(url)
				if not library_item: listitem.setProperty('StartPercent', str(self.meta.get('bookmark')))
				listitem.setArt({'poster': poster, 'fanart': fanart, 'banner': self.meta.get('banner'), 'clearart': self.meta.get('clearart'),
								'clearlogo': self.meta.get('clearlogo'), 'landscape': self.meta.get('landscape'), 'discart': self.meta.get('discart'),
								'tvshow.clearart': self.meta.get('clearart'), 'tvshow.clearlogo': self.meta.get('clearlogo'), 'tvshow.landscape': self.meta.get('landscape'),
								'tvshow.banner': self.meta.get('banner')})
				listitem.setCast(self.meta['cast'])
				if self.meta['vid_type'] == 'movie':
					listitem.setUniqueIDs({'imdb': str(self.meta['imdb_id']), 'tmdb': str(self.meta['tmdb_id'])})
					listitem.setInfo(
						'video', {'mediatype': 'movie', 'trailer': str(self.meta['trailer']),
						'title': self.meta['title'], 'size': '0', 'duration': self.meta['duration'],
						'plot': self.meta['plot'], 'rating': self.meta['rating'], 'premiered': self.meta['premiered'],
						'studio': self.meta['studio'],'year': self.meta['year'], 'genre': self.meta['genre'],
						'tagline': self.meta['tagline'], 'code': self.meta['imdb_id'], 'imdbnumber': self.meta['imdb_id'],
						'director': self.meta['director'], 'writer': self.meta['writer'], 'votes': self.meta['votes']})
				elif self.meta['vid_type'] == 'episode':
					listitem.setUniqueIDs({'imdb': str(self.meta['imdb_id']), 'tmdb': str(self.meta['tmdb_id']), 'tvdb': str(self.meta['tvdb_id'])})
					listitem.setInfo(
						'video', {'mediatype': 'episode', 'trailer': str(self.meta['trailer']), 'title': self.meta['ep_name'], 'imdbnumber': self.meta['imdb_id'],
						'tvshowtitle': self.meta['title'], 'size': '0', 'plot': self.meta['plot'], 'year': self.meta['year'], 'votes': self.meta['votes'],
						'premiered': self.meta['premiered'], 'studio': self.meta['studio'], 'genre': self.meta['genre'], 'season': int(self.meta['season']),
						'episode': int(self.meta['episode']), 'duration': str(self.meta['duration']), 'rating': self.meta['rating'], 'FileNameAndPath': url})
				try:
					kodi_utils.clear_property('script.trakt.ids')
					trakt_ids = {'tmdb': self.meta['tmdb_id'], 'imdb': str(self.meta['imdb_id']), 'slug': make_trakt_slug(self.meta['title'])}
					if self.meta['vid_type'] == 'episode': trakt_ids['tvdb'] = self.meta['tvdb_id']
					kodi_utils.set_property('script.trakt.ids', json.dumps(trakt_ids))
				except: pass
			except: pass
			if library_item and not background: kodi_utils.set_resolvedurl(int(argv[1]), listitem)
			else: self.play(url, listitem)
			self.monitor()
		except: return

	def bookmarkFen(self):
		season = self.meta.get('season', '')
		episode = self.meta.get('episode', '')
		if season == 0: season = ''
		if episode == 0: episode = ''
		bookmark = 0
		watched_indicators = settings.watched_indicators()
		try:
			resume_point, curr_time = indicators.detect_bookmark(indicators.get_bookmarks(self.meta['vid_type'], watched_indicators), self.meta['tmdb_id'], season, episode)
		except: resume_point, curr_time = 0, 0
		resume_check = float(resume_point)
		if resume_check > 0:
			percent = str(resume_point)
			raw_time = float(curr_time)
			if watched_indicators == 1: _time = '%s%%' % str(percent)
			else: _time = sec2time(raw_time, n_msec=0)
			bookmark = self.getResumeStatus(_time, percent, bookmark)
			if bookmark == 0: indicators.erase_bookmark(self.meta['vid_type'], self.meta['tmdb_id'], season, episode)
		return bookmark

	def bookmarkLibrary(self):
		from modules.kodi_library import get_bookmark_kodi_library
		season = self.meta.get('season', '')
		episode = self.meta.get('episode', '')
		if season == 0: season = ''
		if episode == 0: episode = ''
		bookmark = 0
		try: curr_time = get_bookmark_kodi_library(self.meta['vid_type'], self.meta['tmdb_id'], season, episode)
		except: curr_time = 0.0
		if curr_time > 0:
			self.kodi_library_resumed = False
			_time = sec2time(curr_time, n_msec=0)
			bookmark = self.getResumeStatus(_time, curr_time, bookmark)
			if bookmark == 0: indicators.erase_bookmark(self.meta['vid_type'], self.meta['tmdb_id'], season, episode)
		return bookmark

	def getResumeStatus(self, _time, percent, bookmark):
		if settings.auto_resume(self.meta['vid_type']): return percent
		choice = open_window(('windows.yes_no_progress_media', 'YesNoProgressMedia'), 'yes_no_progress_media.xml',
								meta=self.meta, enable_buttons='resume_status', resume_dialog=ls(32790) % _time, percent=percent)
		return percent if choice == True else bookmark if choice == False else 'cancel'

	def monitor(self):
		self.autoplay_next_episode = True if (self.meta['vid_type'] == 'episode' and self.autoplay_nextep and not 'random' in self.meta) else False
		while not self.isPlayingVideo(): kodi_utils.sleep(100)
		kodi_utils.close_all_dialog()
		if self.volume_check: kodi_utils.volume_checker(get_setting('volumecheck.percent', '100'))
		kodi_utils.sleep(1000)
		while self.isPlayingVideo():
			try:
				kodi_utils.sleep(1000)
				self.total_time = self.getTotalTime()
				self.curr_time = self.getTime()
				self.current_point = round(float(self.curr_time/self.total_time * 100), 1)
				if self.current_point >= self.set_watched and not self.media_marked:
					self.mediaWatchedMarker()
				if self.autoplay_next_episode:
					if not self.nextep_info_gathered: self.NextEpInfo()
					self.remaining_time = round(self.total_time - self.curr_time)
					if self.remaining_time <= self.start_prep:
						if not self.nextep_started: self.runNextEp()
			except: pass
			if not self.subs_searched: self.runSubtitles()
		if not self.media_marked: self.mediaWatchedMarker()
		indicators.clear_local_bookmarks()

	def mediaWatchedMarker(self):
		try:
			self.media_marked = True
			if self.set_resume < self.current_point < self.set_watched:
				kodi_utils.clear_property('fen_total_autoplays')
				indicators.set_bookmark(self.meta['vid_type'], self.meta['tmdb_id'], self.curr_time, self.total_time, self.meta.get('season', ''), self.meta.get('episode', ''))
			elif self.current_point >= self.set_watched:
				if self.meta['vid_type'] == 'movie':
					watched_function = indicators.mark_as_watched_unwatched_movie
					watched_params = {'mode': 'mark_as_watched_unwatched_movie', 'action': 'mark_as_watched',
					'tmdb_id': self.meta['tmdb_id'], 'title': self.meta['title'], 'year': self.meta['year'],
					'refresh': 'false', 'from_playback': 'true'}
				else:
					watched_function = indicators.mark_as_watched_unwatched_episode
					watched_params = {'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'season': self.meta['season'],
									'episode': self.meta['episode'], 'tmdb_id': self.meta['tmdb_id'], 'title': self.meta['title'], 'year': self.meta['year'],
									'tvdb_id': self.meta['tvdb_id'], 'refresh': 'false', 'from_playback': 'true'}
				Thread(target=self.runMediaWatched, args=(watched_function, watched_params)).start()
			else: kodi_utils.clear_property('fen_total_autoplays')
		except: pass

	def runMediaWatched(self, function, params):
		try:
			function(params)
			kodi_utils.sleep(1000)
		except: pass

	def NextEpInfo(self):
		try:
			self.nextep_info_gathered = True
			self.nextep_settings = settings.autoplay_next_settings()
			if not self.nextep_settings['run_popup']:
				window_time = round(0.02 * self.total_time)
				self.nextep_settings['window_time'] = window_time
			elif self.nextep_settings['timer_method'] == 'percentage':
				percentage = self.nextep_settings['window_percentage']
				window_time = round((percentage/100) * self.total_time)
				self.nextep_settings['window_time'] = window_time
			else:
				window_time = self.nextep_settings['window_time']
			threshold_check = window_time + 21
			self.start_prep = self.nextep_settings['scraper_time'] + threshold_check
			self.nextep_settings.update({'threshold_check': threshold_check, 'start_prep': self.start_prep})
		except: pass

	def runNextEp(self):
		try:
			self.nextep_started = True
			from indexers.next_episode import execute_nextep
			Thread(target=execute_nextep, args=(self.meta, self.nextep_settings)).start()
		except: pass

	def runSubtitles(self):
		self.subs_searched = True
		try:
			season = int(self.meta['season']) if self.meta['vid_type'] == 'episode' else None
			episode = int(self.meta['episode']) if self.meta['vid_type'] == 'episode' else None
			Thread(target=Subtitles().get, args=(self.meta['title'], self.meta['imdb_id'], season, episode)).start()
		except: pass

	def onAVStarted(self):
		try: kodi_utils.close_all_dialog()
		except: pass

	def onPlayBackStarted(self):
		try: kodi_utils.close_all_dialog()
		except: pass

	# def onPlayBackEnded(self):
	# 	try: self.playlist.clear()
	# 	except: pass

	# def onPlayBackStopped(self):
	# 	try: self.playlist.clear()
	# 	except: pass

	def playAudioAlbum(self, t_files=None, name=None, from_seperate=False):
		__handle__ = int(argv[1])
		default_furk_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/furk.png')
		formats = ('.3gp', ''), ('.aac', ''), ('.flac', ''), ('.m4a', ''), ('.mp3', ''), \
		('.ogg', ''), ('.raw', ''), ('.wav', ''), ('.wma', ''), ('.webm', ''), ('.ra', ''), ('.rm', '')
		params = dict(parse_qsl(argv[2].replace('?','')))
		furk_files_list = []
		append = furk_files_list.append
		playlist = kodi_utils.make_playlist('music')
		playlist.clear()
		if from_seperate: t_files = [i for i in t_files if clean_file_name(i['path']) == params.get('item_path')]
		for item in t_files:
			try:
				name = item['path'] if not name else name
				if not 'audio' in item['ct']: continue
				url = item['url_dl']
				track_name = clean_file_name(batch_replace(to_utf8(item['name']), formats))
				listitem = kodi_utils.make_listitem()
				listitem.setLabel(track_name)
				listitem.setArt({'poster': default_furk_icon, 'thumb': default_furk_icon})
				listitem.setInfo(type='music',infoLabels={'title': track_name, 'size': int(item['size']),
														'album': clean_file_name(batch_replace(to_utf8(name), formats)),'duration': item['length']})
				listitem.setProperty('mimetype', 'audio/mpeg')
				playlist.add(url, listitem)
				if from_seperate: append((url, listitem, False))
			except: pass
		self.play(playlist)
		if from_seperate:
			kodi_utils.add_items(__handle__, furk_files_list)
			kodi_utils.set_content(__handle__, 'files')
			kodi_utils.end_directory(__handle__)
			kodi_utils.set_view_mode('view.premium')

class Subtitles(kodi_utils.xbmc_player):
	def __init__(self):
		kodi_utils.xbmc_player.__init__(self)
		self.os = OpenSubtitlesAPI()
		self.language_dict = language_choices
		self.auto_enable = get_setting('subtitles.auto_enable')
		self.subs_action = get_setting('subtitles.subs_action')
		self.language1 = self.language_dict[get_setting('subtitles.language')]
		self.quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webdl', 'webrip', 'webcap', 'web', 'hdtv', 'hdrip']

	def get(self, query, imdb_id, season, episode):
		def _notification(line, _time=3500):
			return kodi_utils.notification(line, _time)
		def _video_file_subs():
			try: available_sub_language = self.getSubtitles()
			except: available_sub_language = ''
			if available_sub_language == self.language1:
				if self.auto_enable == 'true': self.showSubtitles(True)
				_notification(32852)
				return True
			return False
		def _downloaded_subs():
			files = kodi_utils.list_dirs(subtitle_path)[1]
			if len(files) > 0:
				match_lang1 = None
				match_lang2 = None
				files = [i for i in files if i.endswith('.srt')]
				for item in files:
					if item == search_filename:
						match_lang1 = item
						break
				final_match = match_lang1 if match_lang1 else match_lang2 if match_lang2 else None
				if final_match:
					subtitle = os.path.join(subtitle_path, final_match)
					_notification(32792)
					return subtitle
			return False
		def _searched_subs():
			chosen_sub = None
			search_language = self.language1
			result = self.os.search(query, imdb_id, search_language, season, episode)
			if not result or len(result) == 0:
				_notification(32793)
				return False
			try: video_path = self.getPlayingFile()
			except: video_path = ''
			if '|' in video_path: video_path = video_path.split('|')[0]
			video_path = os.path.basename(video_path)
			if self.subs_action == '1':
				self.pause()
				choices = [i for i in result if i['SubLanguageID'] == search_language and i['SubSumCD'] == '1']
				if len(choices) == 0:
					_notification(32793)
					return False
				string = '%s - %s' % (ls(32246).upper(), video_path)
				dialog_list = ['[B]%s[/B] | [I]%s[/I]' % (i['SubLanguageID'].upper(), i['MovieReleaseName']) for i in choices]
				list_items = [{'line1': item} for item in dialog_list]
				kwargs = {'items': json.dumps(list_items), 'heading': string, 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
				chosen_sub = kodi_utils.select_dialog(choices, **kwargs)
				self.pause()
				if not chosen_sub:
					_notification(32736, _time=1500)
					return False
			else:
				try: chosen_sub = [i for i in result if i['MovieReleaseName'].lower() in video_path.lower() and i['SubLanguageID'] == search_language and i['SubSumCD'] == '1'][0]
				except: pass
				if not chosen_sub:
					fmt = re.split(r'\.|\(|\)|\[|\]|\s|\-', video_path)
					fmt = [i.lower() for i in fmt]
					fmt = [i for i in fmt if i in self.quality]
					if season and fmt == '': fmt = 'hdtv'
					result = [i for i in result if i['SubSumCD'] == '1']
					filter = [i for i in result if i['SubLanguageID'] == search_language \
												and any(x in i['MovieReleaseName'].lower() for x in fmt) and any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if i['SubLanguageID'] == search_language]
					if len(filter) > 0: chosen_sub = filter[0]
					else: chosen_sub = result[0]
			try: lang = kodi_utils.convert_language(chosen_sub['SubLanguageID'])
			except: lang = chosen_sub['SubLanguageID']
			sub_format = chosen_sub['SubFormat']
			final_filename = sub_filename + '_%s.%s' % (lang, sub_format)
			download_url = chosen_sub['ZipDownloadLink']
			temp_zip = os.path.join(subtitle_path, 'temp.zip')
			temp_path = os.path.join(subtitle_path, chosen_sub['SubFileName'])
			final_path = os.path.join(subtitle_path, final_filename)
			subtitle = self.os.download(download_url, subtitle_path, temp_zip, temp_path, final_path)
			kodi_utils.sleep(1000)
			return subtitle
		if self.subs_action == '2': return
		kodi_utils.sleep(2500)
		imdb_id = re.sub(r'[^0-9]', '', imdb_id)
		subtitle_path = kodi_utils.translate_path('special://temp/')
		sub_filename = 'FENSubs_%s_%s_%s' % (imdb_id, season, episode) if season else 'FENSubs_%s' % imdb_id
		search_filename = sub_filename + '_%s.srt' % self.language1
		subtitle = _video_file_subs()
		if subtitle: return
		subtitle = _downloaded_subs()
		if subtitle: return self.setSubtitles(subtitle)
		subtitle = _searched_subs()
		if subtitle: return self.setSubtitles(subtitle)





