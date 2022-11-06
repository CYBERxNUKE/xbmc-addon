# -*- coding: utf-8 -*-
import re
import os
import time
from apis.opensubtitles_api import OpenSubtitlesAPI
from apis.trakt_api import make_trakt_slug
from modules import kodi_utils as ku, settings as st, watched_status as ws
from modules.utils import sec2time
from modules.meta_lists import language_choices
# logger = ku.logger

set_property, clear_property, convert_language, get_visibility, hide_busy_dialog = ku.set_property, ku.clear_property, ku.convert_language, ku.get_visibility, ku.hide_busy_dialog
Thread, json, ls, xbmc_player, translate_path, execute_builtin, sleep = ku.Thread, ku.json, ku.local_string, ku.xbmc_player, ku.translate_path, ku.execute_builtin, ku.sleep
make_listitem, volume_checker, list_dirs, get_setting, confirm_progress_media = ku.make_listitem, ku.volume_checker, ku.list_dirs, ku.get_setting, ku.confirm_progress_media
close_all_dialog, notification, select_dialog, poster_empty, fanart_empty = ku.close_all_dialog, ku.notification, ku.select_dialog, ku.empty_poster, ku.addon_fanart
get_art_provider, get_fanart_data, watched_indicators, auto_resume = st.get_art_provider, st.get_fanart_data, st.watched_indicators, st.auto_resume
autoplay_next_episode, autoplay_next_settings, disable_content_lookup = st.autoplay_next_episode, st.autoplay_next_settings, st.disable_content_lookup
get_progress_percent, get_bookmarks, erase_bookmark, clear_local_bookmarks = ws.get_progress_percent, ws.get_bookmarks, ws.erase_bookmark, ws.clear_local_bookmarks
set_bookmark, mark_as_watched_unwatched_movie, mark_as_watched_unwatched_episode = ws.set_bookmark, ws.mark_as_watched_unwatched_movie, ws.mark_as_watched_unwatched_episode
build_content_prop = ku.build_content_prop

class FenPlayer(xbmc_player):
	def __init__ (self):
		xbmc_player.__init__(self)
		hide_busy_dialog()
		volume_checker()

	def run(self, url=None, obj=None):
		hide_busy_dialog()
		if not url: return self.run_error()
		try: return self.play_video(url, obj)
		except: return self.run_error()

	def monitor(self):
		hide_busy_dialog()
		if self.media_type == 'episode':
			play_random_continual = self.meta_get('random_continual', 'false') == 'true'
			play_random = self.meta_get('random', 'false') == 'true'
			disable_autoplay_next_episode = self.meta_get('disable_autoplay_next_episode', 'false') == 'true'
			if any((play_random_continual, play_random, disable_autoplay_next_episode)):
				auto_play_nextep = False
				if disable_autoplay_next_episode: notification('%s - %s %s' % (ls(32135), ls(32178), ls(32736)), 6000)
			else: auto_play_nextep = autoplay_next_episode()
		else: play_random_continual, auto_play_nextep = False, False
		sleep(1000)
		ensure_dialog_dead, bookmark_set = False, False
		while self.isPlayingVideo():
			try:
				if not ensure_dialog_dead:
					ensure_dialog_dead = True
					self.kill_dialog()
					sleep(200)
					close_all_dialog()
				sleep(1000)
				self.total_time, self.curr_time = self.getTotalTime(), self.getTime()
				if not bookmark_set and self.total_time:
					bookmark_set = True
					if self.media_type == 'episode' and any((play_random_continual, play_random)): bookmark = 0
					else: bookmark = self.get_bookmark()
					self.set_bookmark(bookmark)
				self.current_point = round(float(self.curr_time/self.total_time * 100), 1)
				if self.current_point >= self.set_watched:
					if play_random_continual and not self.random_continual_started: self.run_random_continual()
					if not self.media_marked: self.media_watched_marker()
				if auto_play_nextep:
					if not self.nextep_info_gathered: self.info_next_ep()
					self.remaining_time = round(self.total_time - self.curr_time)
					if self.remaining_time <= self.start_prep:
						if not self.nextep_started: self.run_next_ep()
				if not self.subs_searched: self.run_subtitles()
			except: pass
		hide_busy_dialog()
		self.set_build_content('true')
		if not self.media_marked: self.media_watched_marker()
		clear_local_bookmarks()

	def make_listing(self):
		listitem = make_listitem()
		listitem.setPath(self.url)
		if self.disable_lookup: listitem.setContentLookup(False)
		if self.is_generic: listitem.setInfo('video', {'FileNameAndPath': self.url})
		else:
			if isinstance(self.object, dict): self.meta = self.object 
			else: self.meta = self.object.meta
			self.meta_get = self.meta.get
			self.tmdb_id, self.imdb_id, self.tvdb_id = self.meta_get('tmdb_id'), self.meta_get('imdb_id'), self.meta_get('tvdb_id')
			self.media_type, self.title, self.year = self.meta_get('media_type'), self.meta_get('title'), self.meta_get('year')
			self.season, self.episode = self.meta_get('season', ''), self.meta_get('episode', '')
			self.auto_resume = auto_resume(self.media_type)
			poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = get_art_provider()
			poster = self.meta_get('custom_poster') or self.meta_get(poster_main) or self.meta_get(poster_backup) or poster_empty
			fanart = self.meta_get('custom_fanart') or self.meta_get(fanart_main) or self.meta_get(fanart_backup) or fanart_empty
			clearlogo = self.meta_get('custom_clearlogo') or self.meta_get(clearlogo_main) or self.meta_get(clearlogo_backup) or ''
			duration, plot, genre, trailer = self.meta_get('duration'), self.meta_get('plot'), self.meta_get('genre'), self.meta_get('trailer')
			rating, votes, premiered, studio = self.meta_get('rating'), self.meta_get('votes'), self.meta_get('premiered'), self.meta_get('studio')
			if self.media_type == 'movie':
				listitem.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id)})
				listitem.setInfo('video', {'mediatype': 'movie', 'trailer': trailer, 'title': self.title, 'size': '0', 'duration': duration, 'plot': plot,
					'rating': rating, 'premiered': premiered, 'studio': studio,'year': self.year, 'genre': genre, 'tagline': self.meta_get('tagline'), 'code': self.imdb_id,
					'imdbnumber': self.imdb_id, 'director': self.meta_get('director'), 'writer': self.meta_get('writer'), 'votes': votes})
			else:
				listitem.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id), 'tvdb': str(self.tvdb_id)})
				listitem.setInfo('video', {'mediatype': 'episode', 'trailer': trailer, 'title': self.meta_get('ep_name'), 'imdbnumber': self.imdb_id,
					'tvshowtitle': self.title, 'size': '0', 'plot': plot, 'year': self.year, 'votes': votes, 'premiered': premiered, 'studio': studio, 'genre': genre,
					'season': self.season, 'episode': self.episode, 'duration': duration, 'rating': rating, 'FileNameAndPath': self.url})
			listitem.setCast(self.meta_get('cast', []))
			if get_fanart_data():
				banner, clearart, landscape = self.meta_get('banner'), self.meta_get('clearart'), self.meta_get('landscape')
			else: banner, clearart, landscape = '', '', ''
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
							'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape, 'tvshow.banner': banner})
			try:
				clear_property('script.trakt.ids')
				trakt_ids = {'tmdb': self.tmdb_id, 'imdb': self.imdb_id, 'slug': make_trakt_slug(self.title)}
				if self.media_type == 'episode': trakt_ids['tvdb'] = self.tvdb_id
				set_property('script.trakt.ids', json.dumps(trakt_ids))
			except: pass
		return listitem

	def play_video(self, url, obj):
		self.set_constants(url, obj)
		self.suppress_widget_reload()
		self.play(self.url, self.make_listing())
		if not self.is_generic:
			self.playback_successful = self.check_playback_start()
			self.checking_start = False
			if self.playback_successful: self.start_monitor()
			else: self.pause()
			try: del self.kodi_monitor
			except: pass
			return self.playback_successful

	def media_watched_marker(self):
		self.media_marked = True
		try:
			if self.current_point >= self.set_watched:
				if self.media_type == 'movie': watched_function = mark_as_watched_unwatched_movie
				else: watched_function = mark_as_watched_unwatched_episode
				watched_params = {'action': 'mark_as_watched', 'tmdb_id': self.tmdb_id, 'title': self.title, 'year': self.year, 'season': self.season, 'episode': self.episode,
									'tvdb_id': self.tvdb_id, 'from_playback': 'true'}
				Thread(target=self.run_media_progress, args=(watched_function, watched_params)).start()
			else:
				clear_property('fen.random_episode_history')
				if self.current_point >= self.set_resume:
					progress_params = {'media_type': self.media_type, 'tmdb_id': self.tmdb_id, 'curr_time': self.curr_time, 'total_time': self.total_time,
									'title': self.title, 'season': self.season, 'episode': self.episode, 'from_playback': 'true'}
					Thread(target=self.run_media_progress, args=(set_bookmark, progress_params)).start()
		except: pass

	def run_media_progress(self, function, params):
		try: function(params)
		except: pass

	def run_next_ep(self):
		self.nextep_started = True
		from modules.episode_tools import EpisodeTools
		try: Thread(target=EpisodeTools(self.meta, self.nextep_settings).execute_nextep).start()
		except: pass

	def run_random_continual(self):
		self.random_continual_started = True
		from modules.episode_tools import EpisodeTools
		try: Thread(target=EpisodeTools(self.meta).play_random_continual, args=(False,)).start()
		except: pass

	def run_subtitles(self):
		self.subs_searched = True
		try: Thread(target=Subtitles().get, args=(self.title, self.imdb_id, self.season or None, self.episode or None)).start()
		except: pass

	def check_playback_start(self):
		current_time = time.time()
		end_time = current_time + 40
		while current_time < end_time:
			current_time = time.time()
			hide_busy_dialog()
			if self.isPlayingVideo(): return True
			if self.object.progress_dialog.iscanceled() or self.kodi_monitor.abortRequested():
				self.set_build_content('true')
				sleep(500)
				self.stop()
				return True
			if get_visibility('Window.IsTopMost(okdialog)'):
				execute_builtin("SendClick(okdialog, 11)")
				self.stop()
				return False
			if self.playback_failed: return False
			sleep(100)
		return False

	def suppress_widget_reload(self):
		Thread(target=self.set_suppress).start()

	def start_monitor(self):
		Thread(target=self.monitor).start()

	def set_suppress(self):
		self.set_build_content('false')
		sleep(10000)
		self.set_build_content('true')

	def get_bookmark(self):
		percent = get_progress_percent(get_bookmarks(watched_indicators(), self.media_type), self.tmdb_id, self.season, self.episode)
		if percent:
			bookmark = self.get_resume_status(percent)
			if bookmark == 0: erase_bookmark(self.media_type, self.tmdb_id, self.season, self.episode)
		else: bookmark = 0
		return bookmark

	def set_bookmark(self, bookmark):
		if bookmark != 0: self.seekTime(int(float(int(bookmark)/100) * self.total_time))
		if get_visibility('Player.Paused'): self.pause()

	def get_resume_status(self, percent):
		if self.auto_resume: return percent
		self.pause()
		resume_time = sec2time((float(int(percent)/100) * self.total_time), n_msec=0)
		confirm = confirm_progress_media(meta=self.meta, text=ls(32790) % resume_time, enable_buttons=True, true_button=32832, false_button=32833, focus_button=10, percent=percent)
		return percent if confirm == True else 0

	def set_build_content(self, prop):
		set_property(build_content_prop, prop)

	def info_next_ep(self):
		self.nextep_info_gathered = True
		try:
			nextep_settings = autoplay_next_settings()
			percentage = nextep_settings['window_percentage']
			window_time = round((percentage/100) * self.total_time)
			use_window = nextep_settings['alert_method'] == 0
			default_action = nextep_settings['default_action'] if use_window else 'close'
			self.start_prep = nextep_settings['scraper_time'] + window_time
			self.nextep_settings = {'use_window': use_window, 'window_time': window_time, 'default_action': default_action}
		except: pass

	def kill_dialog(self):
		try: self.object._kill_progress_dialog()
		except: close_all_dialog()

	def onPlayBackEnded(self):
		self.playback_failed = True

	def set_constants(self, url, obj):
		self.url = url
		self.object = obj
		self.disable_lookup = disable_content_lookup()
		self.is_generic = self.object == 'video'
		if not self.is_generic:
			self.kodi_monitor = ku.monitor
			self.media_marked, self.subs_searched, self.nextep_info_gathered = False, False, False
			self.playback_failed, self.nextep_started, self.random_continual_started = False, False, False
			self.set_resume, self.set_watched = int(get_setting('playback.resume_percent', '5')), int(get_setting('playback.watched_percent', '90'))

	def run_error(self):
		self.set_build_content('true')
		notification(32121, 3500)
		return False

class Subtitles(xbmc_player):
	def __init__(self):
		xbmc_player.__init__(self)
		self.os = OpenSubtitlesAPI()
		self.language_dict = language_choices
		self.auto_enable = get_setting('subtitles.auto_enable')
		self.subs_action = get_setting('subtitles.subs_action')
		self.language = self.language_dict[get_setting('subtitles.language')]
		self.quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webdl', 'webrip', 'webcap', 'web', 'hdtv', 'hdrip']

	def get(self, query, imdb_id, season, episode):
		def _notification(line, _time=3500):
			return notification(line, _time)
		def _video_file_subs():
			try: available_sub_language = self.getSubtitles()
			except: available_sub_language = ''
			if available_sub_language == self.language:
				if self.auto_enable == 'true': self.showSubtitles(True)
				_notification(32852)
				return True
			return False
		def _downloaded_subs():
			files = list_dirs(subtitle_path)[1]
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
			result = self.os.search(query, imdb_id, self.language, season, episode)
			if not result or len(result) == 0:
				_notification(32793)
				return False
			try: video_path = self.getPlayingFile()
			except: video_path = ''
			if '|' in video_path: video_path = video_path.split('|')[0]
			video_path = os.path.basename(video_path)
			if self.subs_action == '1':
				self.pause()
				choices = [i for i in result if i['SubLanguageID'] == self.language and i['SubSumCD'] == '1']
				if len(choices) == 0:
					_notification(32793)
					return False
				dialog_list = ['[B]%s[/B] | [I]%s[/I]' % (i['SubLanguageID'].upper(), i['MovieReleaseName']) for i in choices]
				list_items = [{'line1': item} for item in dialog_list]
				kwargs = {'items': json.dumps(list_items), 'heading': video_path.replace('%20', ' '), 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
				chosen_sub = select_dialog(choices, **kwargs)
				self.pause()
				if not chosen_sub:
					_notification(32736, _time=1500)
					return False
			else:
				try: chosen_sub = [i for i in result if i['MovieReleaseName'].lower() in video_path.lower() and i['SubLanguageID'] == self.language and i['SubSumCD'] == '1'][0]
				except: pass
				if not chosen_sub:
					fmt = re.split(r'\.|\(|\)|\[|\]|\s|\-', video_path)
					fmt = [i.lower() for i in fmt]
					fmt = [i for i in fmt if i in self.quality]
					if season and fmt == '': fmt = 'hdtv'
					result = [i for i in result if i['SubSumCD'] == '1']
					filter = [i for i in result if i['SubLanguageID'] == self.language \
												and any(x in i['MovieReleaseName'].lower() for x in fmt) and any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if i['SubLanguageID'] == self.language]
					if len(filter) > 0: chosen_sub = filter[0]
					else: chosen_sub = result[0]
			try: lang = convert_language(chosen_sub['SubLanguageID'])
			except: lang = chosen_sub['SubLanguageID']
			sub_format = chosen_sub['SubFormat']
			final_filename = sub_filename + '_%s.%s' % (lang, sub_format)
			download_url = chosen_sub['ZipDownloadLink']
			temp_zip = os.path.join(subtitle_path, 'temp.zip')
			temp_path = os.path.join(subtitle_path, chosen_sub['SubFileName'])
			final_path = os.path.join(subtitle_path, final_filename)
			subtitle = self.os.download(download_url, subtitle_path, temp_zip, temp_path, final_path)
			sleep(1000)
			return subtitle
		if self.subs_action == '2': return
		sleep(2500)
		imdb_id = re.sub(r'[^0-9]', '', imdb_id)
		subtitle_path = translate_path('special://temp/')
		sub_filename = 'FENSubs_%s_%s_%s' % (imdb_id, season, episode) if season else 'FENSubs_%s' % imdb_id
		search_filename = sub_filename + '_%s.srt' % self.language
		subtitle = _video_file_subs()
		if subtitle: return
		subtitle = _downloaded_subs()
		if subtitle: return self.setSubtitles(subtitle)
		subtitle = _searched_subs()
		if subtitle: return self.setSubtitles(subtitle)
