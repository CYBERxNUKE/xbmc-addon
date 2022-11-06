# -*- coding: utf-8 -*-
from windows import BaseDialog
# from modules.kodi_utils import logger

class VideoPlayer(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.video = kwargs['video']

	def onInit(self):
		self.player.play(self.video, windowed=True)
		self.monitor()

	def run(self):
		self.doModal()
		self.clearProperties()
		self.clear_modals()
	
	def onAction(self, action, controlID=None):
		if action in self.closing_actions: self.stop()
		elif action == self.left_action: self.seek_back()
		elif action == self.right_action: self.seek_forward()

	def monitor(self):
		while not self.player.isPlayingVideo(): self.sleep(1000)
		while self.player.isPlayingVideo(): self.sleep(1000)
		self.exit()

	def seek_back(self):
		try: self.player.seekTime(max(self.player.getTime() - 10.0, 0.0))
		except: pass

	def seek_forward(self):
		try: self.player.seekTime(min(self.player.getTime() + 10.0, self.player.getTotalTime() - 1))
		except: pass

	def stop(self):
		self.player.stop()
		self.exit()

	def exit(self):
		self.sleep(500)
		self.close()
