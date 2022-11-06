# -*- coding: utf-8 -*-
from windows import BaseDialog
from modules.kodi_utils import json, empty_poster, addon_fanart, notification
from modules.settings import get_resolution, get_art_provider
# from modules.kodi_utils import logger

tmdb_image_url = 'https://image.tmdb.org/t/p/%s%s'
image_resolutions = {'poster': 'w342', 'fanart': 'w780', 'clearlogo': 'original'}
meta_keys = {'posters': 'poster', 'backdrops': 'fanart', 'logos': 'clearlogo'}
list_ids = {'posters': 2020, 'backdrops': 2021, 'logos': 2022}
custom_key, count_name, count_insert = 'custom_%s', '%s.number', '%02d'

class SelectArtwork(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.kwargs = kwargs
		self.kwargs_get = self.kwargs.get
		self.images = self.kwargs_get('images')
		self.meta = self.kwargs_get('meta')
		self.meta_get = self.meta.get
		self.selected = {}
		self.active_items = []
		self.final_resolution = get_resolution()
		self.get_starting_artwork()

	def onInit(self):
		for image_type, image_list in self.images.items(): self.make_menu(image_type, image_list)
		if not self.active_items:
			notification(33069, 2000)
			return self.close()
		self.setFocusId(sorted(self.active_items)[0])

	def run(self):
		self.doModal()
		self.clearProperties()
		return self.selected

	def onAction(self, action):
		if action in self.selection_actions:
			chosen_listitem = self.get_listitem(self.getFocusId())
			if chosen_listitem.getProperty('check_status') == 'checked': return
			chosen_meta_key = chosen_listitem.getProperty('meta_key')
			for item in self.get_attribute(self, '%s_listitems' % chosen_meta_key):
				if item.getProperty('check_status') == 'checked': item.setProperty('check_status', '')
			chosen_listitem.setProperty('check_status', 'checked')			
			chosen_image = tmdb_image_url % (self.final_resolution[chosen_meta_key], chosen_listitem.getProperty('file_path'))
			self.set_attribute(self, chosen_meta_key, chosen_image)
			self.selected[custom_key % chosen_meta_key] = chosen_image
		elif action in self.closing_actions:
			return self.close()

	def make_menu(self, image_type, image_list):
		def builder():
			for count, item in enumerate(image_list):
				try:
					file_path = item['file_path']
					ext = 'png' if image_type == 'logos' else 'jpg'
					if not file_path.endswith(ext): file_path = file_path.replace(file_path.split('.')[-1], ext)
					image = tmdb_image_url % (image_resolutions[meta_key], file_path)
					listitem = self.make_listitem()
					listitem.setProperty('image', image)
					listitem.setProperty('meta_key', meta_key)
					listitem.setProperty('file_path', file_path)
					if image == self.get_attribute(self, meta_key):
						listitem.setProperty('check_status', 'checked')
						self.focus_index = count
					else: listitem.setProperty('check_status', '')
					yield listitem
				except: pass
		try:
			self.focus_index = 0
			meta_key = meta_keys[image_type]
			list_id = list_ids[image_type]
			item_list = list(builder())
			if not item_list: return
			self.setProperty(count_name % meta_key, count_insert % len(item_list))
			self.set_attribute(self, '%s_listitems' % meta_key, item_list)
			self.add_items(list_id, item_list)
			self.set_focus(list_id)
			self.add_active(list_id)
		except: pass

	def get_starting_artwork(self):
		poster_main, poster_backup, fanart_main, fanart_backup, clearlogo_main, clearlogo_backup = get_art_provider()
		self.poster = self.meta_get('custom_poster') or self.meta_get(poster_main) or self.meta_get(poster_backup) or empty_poster
		self.fanart = self.meta_get('custom_fanart') or self.meta_get(fanart_main) or self.meta_get(fanart_backup) or addon_fanart
		self.clearlogo = self.meta_get('custom_clearlogo') or self.meta_get(clearlogo_main) or self.meta_get(clearlogo_backup) or ''

	def add_items(self, _id, items):
		self.getControl(_id).addItems(items)

	def set_focus(self, _id):
		self.getControl(_id).selectItem(self.focus_index)

	def add_active(self, _id):
		self.active_items.append(_id)