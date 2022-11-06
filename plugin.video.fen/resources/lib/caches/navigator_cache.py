# -*- coding: utf-8 -*-
from indexers import default_menus
from modules.kodi_utils import get_property, set_property, clear_property, database, navigator_db
# from modules.kodi_utils import logger

timeout = 60
main_menus, default_menu_items = default_menus.main_menus, default_menus.default_menu_items
GET_LIST = 'SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?'
SET_LIST = 'INSERT OR REPLACE INTO navigator VALUES (?, ?, ?)'
DELETE_LIST = 'DELETE FROM navigator WHERE list_name=? and list_type=?'
GET_FOLDERS = 'SELECT list_name, list_contents FROM navigator WHERE list_type = ?'
GET_FOLDER_CONTENTS = 'SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?'
prop_dict = {'default': 'fen_%s_default', 'edited': 'fen_%s_edited', 'shortcut_folder': 'fen_%s_shortcut_folder'}

class NavigatorCache:
	def __init__(self):
		self._connect_database()
		self._set_PRAGMAS()

	def get_main_lists(self, list_name):
		default_contents = self.get_memory_cache(list_name, 'default')
		if not default_contents:
			default_contents = self.get_list(list_name, 'default')
			if default_contents == None:
				self.rebuild_database()
				return self.get_main_lists(list_name)
			try: edited_contents = self.get_list(list_name, 'edited')
			except: edited_contents = None
		else: edited_contents = self.get_memory_cache(list_name, 'edited')
		return default_contents, edited_contents

	def get_list(self, list_name, list_type):
		contents = None
		try: contents = eval(self.dbcur.execute(GET_LIST, (list_name, list_type)).fetchone()[0])
		except: pass
		return contents

	def set_list(self, list_name, list_type, list_contents):
		self.dbcur.execute(SET_LIST, (list_name, list_type, repr(list_contents)))
		self.set_memory_cache(list_name, list_type, list_contents)

	def delete_list(self, list_name, list_type):
		self.dbcur.execute(DELETE_LIST, (list_name, list_type))
		self.delete_memory_cache(list_name, list_type)
		self.dbcon.execute('VACUUM')
	
	def get_memory_cache(self, list_name, list_type):
		try: return eval(get_property(self._get_list_prop(list_type) % list_name))
		except: return None
	
	def set_memory_cache(self, list_name, list_type, list_contents):
		set_property(self._get_list_prop(list_type) % list_name, repr(list_contents))

	def delete_memory_cache(self, list_name, list_type):
		clear_property(self._get_list_prop(list_type) % list_name)

	def get_shortcut_folders(self):
		try:
			folders = self.dbcur.execute(GET_FOLDERS, ('shortcut_folder',)).fetchall()
			folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
		except: folders = []
		return folders

	def get_shortcut_folder_contents(self, list_name):
		contents = []
		try: contents = eval(self.dbcur.execute(GET_FOLDER_CONTENTS, (list_name, 'shortcut_folder')).fetchone()[0])
		except: pass
		return contents

	def currently_used_list(self, list_name):
		default_contents, edited_contents = self.get_main_lists(list_name)
		list_items = edited_contents or default_contents
		return list_items

	def rebuild_database(self):
		for list_name in default_menu_items: self.set_list(list_name, 'default', main_menus[list_name])

	def _get_list_prop(self, list_type):
		return prop_dict[list_type]

	def _connect_database(self):
		self.dbcon = database.connect(navigator_db, timeout=timeout, isolation_level=None)

	def _set_PRAGMAS(self):
		self.dbcur = self.dbcon.cursor()
		self.dbcur.execute('''PRAGMA synchronous = OFF''')
		self.dbcur.execute('''PRAGMA journal_mode = OFF''')

navigator_cache = NavigatorCache()