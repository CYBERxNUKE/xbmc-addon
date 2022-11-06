# -*- coding: utf-8 -*-
from windows import BaseDialog
from modules.kodi_utils import Thread, empty_poster
from modules.settings import get_art_provider
# from modules.kodi_utils import logger

button_actions = {10: 'close', 11: 'play', 12: 'cancel'}

class NextEpisode(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.closed = False
		self.meta = kwargs.get('meta')
		self.selected = kwargs.get('default_action', 'close')
		self.set_properties()

	def onInit(self):
		self.monitor()

	def run(self):
		self.doModal()
		self.clearProperties()
		self.clear_modals()
		return self.selected

	def onAction(self, action):
		if action in self.closing_actions:
			self.selected = 'close'
			self.closed = True
			self.close()

	def onClick(self, controlID):
		self.closed = True
		self.selected = button_actions[controlID]
		self.close()

	def set_properties(self):
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = get_art_provider()[0:4]
		self.setProperty('title', self.meta['title'])
		self.setProperty('poster', self.original_poster())
		self.setProperty('fanart', self.original_fanart())
		self.setProperty('next_episode', '[B]%s - %02dx%02d[/B] - %s' % (self.meta['title'], self.meta['season'], self.meta['episode'], self.meta['ep_name']))

	def original_poster(self):
		self.poster = self.meta.get('custom_poster') or self.meta.get(self.poster_main) or self.meta.get(self.poster_backup) or empty_poster
		return self.poster

	def original_fanart(self):
		self.fanart = self.meta.get('custom_fanart') or self.meta.get(self.fanart_main) or self.meta.get(self.fanart_backup) or ''
		return self.fanart

	def monitor(self):
		progress_bar = self.getControl(5000)
		total_time = self.player.getTotalTime()
		total_remaining = total_time - self.player.getTime()
		while self.player.isPlaying():
			try:
				if self.closed: break
				current_time = self.player.getTime()
				remaining = round(total_time - current_time)
				current_point = (remaining / float(total_remaining)) * 100
				progress_bar.setPercent(current_point)
				self.sleep(1000)
			except: pass
		self.close()
