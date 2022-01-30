# -*- coding: utf-8 -*-
from windows import BaseDialog
from modules.settings import get_art_provider
from modules.kodi_utils import translate_path
# from modules.kodi_utils import logger

yes_buttons = (10, 12)
no_buttons = (11, 13)
focus_button = {'resume_status': 10, 'playmode_status': 13}
backup_poster = translate_path('special://home/addons/script.tikiart/resources/media/box_office.png')

class YesNoProgressMedia(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.is_canceled = False
		self.selected = None
		self.meta = kwargs['meta']
		self.buttons = kwargs.get('enable_buttons', '')
		self.resume_dialog = kwargs.get('resume_dialog', '')
		self.percent = float(kwargs.get('percent', '0'))
		self.make_items()
		self.set_properties()

	def onInit(self):
		if self.buttons: self.allow_buttons()

	def run(self):
		self.doModal()
		return self.selected

	def iscanceled(self):
		if self.buttons: return self.selected
		else: return self.is_canceled

	def onAction(self, action):
		if action in self.closing_actions:
			self.is_canceled = True
			self.close()

	def onClick(self, controlID):
		if controlID in yes_buttons: self.selected = True
		elif controlID in no_buttons: self.selected = False
		self.close()

	def allow_buttons(self):
		self.setProperty('tikiskins.source_progress.buttons', self.buttons)
		self.update(self.resume_dialog, self.percent)
		self.setFocusId(focus_button[self.buttons])

	def make_items(self):
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = get_art_provider()
		self.title = self.meta['title']
		self.year = str(self.meta['year'])
		self.poster = self.meta.get(self.poster_main) or self.meta.get(self.poster_backup) or backup_poster
		self.fanart = self.meta.get(self.fanart_main) or self.meta.get(self.fanart_backup) or ''
		self.clearlogo = self.meta['clearlogo']

	def set_properties(self):
		self.setProperty('tikiskins.source_progress.title', self.title)
		self.setProperty('tikiskins.source_progress.year', self.year)
		self.setProperty('tikiskins.source_progress.poster', self.poster)
		self.setProperty('tikiskins.source_progress.fanart', self.fanart)
		self.setProperty('tikiskins.source_progress.clearlogo', self.clearlogo)

	def update(self, content='', percent=0):
		try:
			self.getControl(2000).setText(content)
			self.getControl(5000).setPercent(percent)
		except: pass
