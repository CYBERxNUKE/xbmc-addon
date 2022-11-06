# -*- coding: utf-8 -*-
from indexers import navigator, default_menus
from caches.navigator_cache import navigator_cache
from modules import kodi_utils
# logger = kodi_utils.logger

build_url, confirm_dialog, dialog, sleep, kodi_refresh = kodi_utils.build_url, kodi_utils.confirm_dialog, kodi_utils.dialog, kodi_utils.sleep, kodi_utils.kodi_refresh
get_infolabel, select_dialog, notification, execute_builtin = kodi_utils.get_infolabel, kodi_utils.select_dialog, kodi_utils.notification, kodi_utils.execute_builtin
json, tp, ls, parse_qsl, get_icon = kodi_utils.json, kodi_utils.translate_path, kodi_utils.local_string, kodi_utils.parse_qsl, kodi_utils.get_icon
main_menus, main_menu_items, default_menu_items = default_menus.main_menus, default_menus.main_menu_items, default_menus.default_menu_items
get_all_icon_vars = kodi_utils.get_all_icon_vars
main_list_name_dict = {'RootList': ls(32457), 'MovieList': ls(32028), 'TVShowList': ls(32029)}
fen_str, pos_str, top_pos_str, top_str = ls(32036), ls(32707), ls(32708), ls(32709)

class MenuEditor:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		if 'menu_item' in self.params: self.menu_item = json.loads(self.params.get('menu_item'))
		else: self.menu_item = dict(parse_qsl(get_infolabel("ListItem.FileNameAndPath").replace('plugin://plugin.video.fen/?','')))
		self.menu_item_get = self.menu_item.get

	def edit_menu(self):
		active_list, position = self.params_get('active_list'), int(self.params_get('position', '0'))
		menu_name = self.menu_item_get('name')
		menu_name_translated = ls(menu_name)
		menu_name_translated_display = menu_name_translated.replace('[B]', '').replace('[/B]', '')
		external_list_item, shortcut_folder = self.menu_item_get('external_list_item', 'False') == 'True', self.menu_item_get('shortcut_folder', 'False') == 'True'
		list_name =  main_list_name_dict[active_list]
		listing = []
		if len(active_list) != 1:
			listing.append((ls(32716) % menu_name_translated_display, self.move))
			listing.append((ls(32717) % menu_name_translated_display, self.remove))
		if not shortcut_folder:
			listing.append((ls(32718) % menu_name_translated_display, self.add_original_external))
			listing.append((ls(32719) % menu_name_translated_display, self.shortcut_folder_add_item))
		listing.append((ls(32721) % list_name, self.add_original))
		listing.append((ls(32725) % list_name, self.shortcut_folder_add_to_main_menu))
		listing.append((ls(32720) % list_name, self.add_trakt))
		listing.append((ls(32722) % list_name, self.restore))
		listing.append((ls(32723) % list_name, self.check_update_list))
		if not external_list_item: listing.append((ls(32724) % menu_name_translated_display, self.reload_menu_item))
		list_items = [{'line1': i[0]} for i in listing]
		kwargs = {'items': json.dumps(list_items), 'heading': fen_str, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		function = select_dialog([i[1] for i in listing], **kwargs)
		if function == None: return
		self.params = {'active_list': active_list, 'list_name': list_name, 'menu_name': menu_name, 'menu_name_translated': menu_name_translated, 'position': position}
		self.params_get = self.params.get
		return function()

	def edit_menu_shortcut_folder(self):
		listing = [(ls(32712), 'move'), (ls(32713), 'remove'), ('%s %s' % (ls(32671), ls(32129)), 'clear_all')]
		list_items = [{'line1': i[0]} for i in listing]
		kwargs = {'items': json.dumps(list_items), 'heading': fen_str, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		self.action = select_dialog([i[1] for i in listing], **kwargs)
		if self.action == None: return
		return self.shortcut_folder_contents_adjust()

	def browse(self):
		active_list = self.params_get('active_list')
		list_name =  main_list_name_dict[active_list]
		try: choice_items = self._get_removed_items(active_list)
		except: return notification(32760, 1500)
		browse_item = self._menu_select(choice_items, list_name)
		if browse_item == None: return
		browse_item = choice_items[browse_item]
		if browse_item.get('mode') == 'build_popular_people': command = 'RunPlugin(%s)'
		else: command = 'Container.Update(%s)'
		execute_builtin(command % build_url(browse_item))

	def move(self):
		active_list = self.params_get('active_list')
		list_items = navigator_cache.currently_used_list(active_list)
		if len(list_items) == 1: return notification(32736, 1500)
		choice_items = [i for i in list_items if str(i['name']) != str(self.params_get('menu_name'))]
		current_position = self.params_get('position')
		new_position = self._menu_select(choice_items, self.params_get('menu_name_translated'), multi_line='true', position_list=True)
		if new_position == None or new_position == current_position: return
		list_items.insert(new_position, list_items.pop(current_position))
		self._db_execute('set', active_list, list_items)

	def remove(self):
		if not confirm_dialog(): return notification(32736, 1500)
		active_list = self.params_get('active_list')
		list_items = navigator_cache.currently_used_list(active_list)
		if len(list_items) == 1: return notification(32736, 1500)
		list_items = [i for i in list_items if str(i['name']) != str(self.params_get('menu_name'))]
		self._db_execute('set', active_list, list_items)

	def add_original(self):
		active_list = self.params_get('active_list')
		try: choice_items = self._get_removed_items(active_list)
		except: return notification(32760, 1500)
		menu_name_translated = self.params_get('menu_name_translated')
		choice = self._menu_select(choice_items, menu_name_translated)
		if choice == None: return notification(32736, 1500)
		choice_list = choice_items[choice]
		list_items = navigator_cache.currently_used_list(active_list)
		position = self._menu_select(list_items, menu_name_translated, multi_line='true', position_list=True)
		if position == None: return notification(32736, 1500)
		list_items.insert(position, choice_list)
		self._db_execute('set', active_list, list_items)

	def add_original_external(self):
		active_list = self.params_get('active_list')
		choice_items = self._get_main_menu_items(active_list)
		choice = self._menu_select([i[1] for i in choice_items], '')
		if choice == None: return notification(32736, 1500)
		menu_name_translated = self.params_get('menu_name_translated')
		choice_name, choice_list = choice_items[choice]
		list_items = navigator_cache.currently_used_list(choice_list['action'])
		menu_name = self._get_external_name_input(menu_name_translated)
		position = self._menu_select(list_items, menu_name or menu_name_translated, multi_line='true', position_list=True)
		if position == None: return notification(32736, 1500)
		list_items.insert(position, self._add_external_info_to_item(self.menu_item, menu_name, False))
		self._db_execute('set', choice_name, list_items, refresh=False)

	def add_trakt(self):
		from apis.trakt_api import get_trakt_list_selection
		trakt_selection = get_trakt_list_selection(list_choice='nav_edit')
		if trakt_selection == None: return notification(32736, 1500)
		active_list = self.params_get('active_list')
		list_items = navigator_cache.currently_used_list(active_list)
		menu_name = self._get_external_name_input(trakt_selection['name'])
		position = self._menu_select(list_items, menu_name or trakt_selection['name'], multi_line='true', position_list=True)
		if position == None: return notification(32736, 1500)
		trakt_selection.update({'iconImage': 'trakt', 'mode': 'trakt.lists.build_trakt_list'})
		list_items.insert(position, self._add_external_info_to_item(trakt_selection, menu_name, False))
		self._db_execute('set', active_list, list_items)

	def restore(self):
		if not confirm_dialog(): return notification(32736, 1500)
		active_list = self.params_get('active_list')
		self._db_execute('delete', active_list, list_type='edited', refresh=False)
		self._db_execute('set', active_list, main_menus[active_list], 'default')

	def reload_menu_item(self):
		active_list = self.params_get('active_list')
		default, edited = navigator_cache.get_main_lists(active_list)
		list_type = 'edited' if edited else 'default'
		current_list = edited or default
		menu_name = self.params_get('menu_name')
		try: new_item = [i for i in default if str(i['name']) == str(menu_name)][0]
		except: return notification(32760, 1500)
		list_items = [i for i in current_list if str(i['name']) != str(menu_name)]
		list_items.insert(self.params_get('position', 0), new_item)
		self._db_execute('set', active_list, list_items, list_type)

	def check_update_list(self):
		active_list = self.params_get('active_list')
		new_contents = main_menus[active_list]
		default, edited = navigator_cache.get_main_lists(active_list)
		list_type = 'edited' if edited else'default'
		current_list = edited or default
		if default == new_contents: return notification(32983, 1500)
		new_entry = [i for i in new_contents if not i in default][0]
		new_entry_translated_name = ls(new_entry.get('name'))
		if not confirm_dialog(text='%s[CR]%s' % (ls(32727) % new_entry_translated_name, ls(32728)), top_space=False): return notification(32736, 1500)
		item_position = self._menu_select(current_list, new_entry_translated_name, position_list=True)
		if item_position == None: return notification(32736, 1500)
		current_list.insert(item_position, new_entry)
		self._db_execute('set', active_list, current_list, list_type)
		if list_type == 'edited': self._db_execute('set', active_list, new_contents, 'default')

	def add_external(self):
		choice_items = self._get_main_menu_items([])
		choice = self._menu_select([i[1] for i in choice_items], '')
		if choice == None: return notification(32736, 1500)
		name = self._clean_name(self.params_get('name'))
		choice_name, choice_list = choice_items[choice]
		list_items = navigator_cache.currently_used_list(choice_list['action'])
		menu_name = self._get_external_name_input(name) or name
		position = self._menu_select(list_items, menu_name, multi_line='true', position_list=True)
		if position == None: return notification(32736, 1500)
		list_items.insert(position, self._add_external_info_to_item(self.menu_item, menu_name))
		self._db_execute('set', choice_name, list_items, refresh=False)

	def _menu_select(self, choice_items, menu_name, heading=fen_str, multi_line='false', position_list=False):
		def _builder():
			for item in choice_items:
				item_get = item.get
				line2 = pos_str % (menu_name, ls(item_get('name', None) or item_get('list_name')) if position_list else '')
				iconImage = item_get('iconImage', None)
				if iconImage: icon = iconImage if iconImage.startswith('http') else get_icon(item_get('iconImage'))
				else: icon = get_icon('folder')
				yield {'line1': ls(item_get('name')), 'line2': line2, 'icon':icon}
		list_items = list(_builder())
		if position_list: list_items.insert(0, {'line1': top_str, 'line2': top_pos_str % menu_name, 'icon': get_icon('top')})
		index_list = [list_items.index(i) for i in list_items]
		kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': multi_line}
		return select_dialog(index_list, **kwargs)

	def _icon_select(self, folder_first=True):
		all_icons = get_all_icon_vars()
		if folder_first:
			try:
				all_icons.remove('folder')
				all_icons.insert(0, 'folder')
			except: pass
			list_items = [{'line1': i if i != 'folder' else 'folder (default)', 'icon': get_icon(i)} for i in all_icons]
		else: list_items = [{'line1': i, 'icon': get_icon(i)} for i in all_icons]
		kwargs = {'items': json.dumps(list_items), 'heading': fen_str, 'window_xml': 'select.xml'}
		icon_choice = select_dialog(all_icons, **kwargs) or 'folder'
		return icon_choice

	def _clean_name(self, name):
		name = name.replace('[B]', '').replace('[/B]', '').replace(':', '')
		name = ' '.join(i.lower().title() for i in name.split())
		name = name.replace('  ', ' ').replace('Tv', 'TV')
		return name

	def _get_removed_items(self, active_list):
		default_list_items, list_items = navigator_cache.get_main_lists(active_list)
		return [i for i in default_list_items if not i in list_items]

	def _get_external_name_input(self, current_name):
		new_name = dialog.input(fen_str, defaultt=current_name)
		if new_name == current_name: return None
		return new_name

	def _add_external_info_to_item(self, menu_item, menu_name=None, add_all_params=True):
		if add_all_params:
			self.params.pop('mode', None)
			menu_item.update(self.params)
		if menu_name: menu_item['name'] = menu_name
		menu_item['external_list_item'] = 'True'
		return menu_item

	def _get_main_menu_items(self, active_list):
		choice_list = [i for i in default_menu_items if i != active_list]
		return [(i, main_menu_items[i]) for i in choice_list]

	def _remove_active_shortcut_folder(self, main_menu_items_list, folder_name):
		for x in main_menu_items_list:
			try:
				match = [i for i in x[1] if str(i['name']) == str(folder_name)][0]
				new_list = [i for i in x[1] if i != match]
				self._db_execute('set', x[0], new_list, refresh=False)
			except: pass

	def _db_execute(self, db_action, list_name, list_contents=[], list_type='edited', refresh=True):
		if db_action == 'set': navigator_cache.set_list(list_name, list_type, list_contents)
		elif db_action == 'delete': navigator_cache.delete_list(list_name, list_type)
		elif db_action == 'make_new_folder': navigator_cache.set_list(list_name, 'shortcut_folder', list_contents)
		notification(32576, 1500)
		sleep(200)
		if refresh: kodi_refresh()

	def shortcut_folder_contents_adjust(self):
		active_list = self.params_get('active_list')
		if self.action == 'clear_all':
			if not confirm_dialog(): return notification(32736, 1500)
			list_items = []
		else:
			list_name = self.menu_item_get('name')
			list_items = navigator_cache.get_shortcut_folder_contents(active_list)
			if self.action == 'remove':
				if not confirm_dialog(): return notification(32736, 1500)
				list_items = [i for i in list_items if str(i['name']) != str(list_name)]
			else:
				if len(list_items) == 1: return notification(32736, 1500)
				choice_items = [i for i in list_items if str(i['name']) != str(list_name)]
				current_position = int(self.params_get('position', '0'))
				new_position = self._menu_select(choice_items, list_name, multi_line='true', position_list=True)
				if new_position == None or new_position == current_position: return
				list_items.insert(new_position, list_items.pop(current_position))
		self._db_execute('set', active_list, list_items, 'shortcut_folder', True)

	def shortcut_folder_make(self):
		list_name = dialog.input(fen_str)
		if not list_name: return
		self._db_execute('make_new_folder', list_name, list_type='shortcut_folder')

	def shortcut_folder_add_item(self):
		shortcut_folders = navigator_cache.get_shortcut_folders()
		if len(shortcut_folders) == 1: choice_name, choice_list = shortcut_folders[0]
		elif shortcut_folders:
			choice = self._menu_select([{'name': i[0], 'iconImage': 'folder'} for i in shortcut_folders], '')
			if choice == None: return notification(32736, 1500)
			shortcut_folders[choice]
			choice_name, choice_list = shortcut_folders[choice]
		else:
			if not confirm_dialog(text=32702, default_control=10): return notification(32736, 1500)
			self.shortcut_folder_make()
			try: choice_name, choice_list = navigator_cache.get_shortcut_folders()[0]
			except: return notification(32736, 1500)
		list_items = eval(choice_list)
		name = self._clean_name(self.params_get('name') or self.params_get('menu_name_translated'))
		menu_name = self._get_external_name_input(name) or name
		self.menu_item.update({'name': menu_name, 'iconImage': self.params_get('iconImage', None) or self.menu_item_get('iconImage')})
		if list_items:
			position = self._menu_select(list_items, menu_name, multi_line='true', position_list=True)
			if position == None: return notification(32736, 1500)
		else: position = 0
		list_items.insert(position, self.menu_item)
		self._db_execute('set', choice_name, list_items, 'shortcut_folder', False)

	def shortcut_folder_add_to_main_menu(self):
		shortcut_folders = navigator_cache.get_shortcut_folders()
		if len(shortcut_folders) == 1: name = shortcut_folders[0][0]
		elif shortcut_folders:
			choice = self._menu_select([{'name': i[0], 'iconImage': 'folder'} for i in shortcut_folders], '')
			if choice == None: return notification(32736, 1500)
			shortcut_folders[choice]
			name = shortcut_folders[choice][0]
		else:
			if not confirm_dialog(text=32702, default_control=10): return notification(32736, 1500)
			self.shortcut_folder_make()
			try: name = navigator_cache.get_shortcut_folders()[0][0]
			except: return notification(32736, 1500)
		active_list = self.params_get('active_list')
		list_items = navigator_cache.currently_used_list(active_list)
		position = self._menu_select(list_items, self.params_get('menu_name_translated'), multi_line='true', position_list=True)
		if position == None: return notification(32736, 1500)
		icon_choice = self._icon_select()
		chosen_folder = {'mode': 'navigator.build_shortcut_folder_list', 'name': name, 'iconImage': icon_choice, 'shortcut_folder': 'True', 'external_list_item': 'True'}
		list_items.insert(position, chosen_folder)
		self._db_execute('set', active_list, list_items)

	def shortcut_folder_delete(self):
		if not confirm_dialog(): return notification(32736, 1500)
		main_menu_items_list = [(i, navigator_cache.currently_used_list(i)) for i in default_menu_items]
		folder_name = self.menu_item_get('name')
		self._db_execute('delete', folder_name, list_type='shortcut_folder')
		self._remove_active_shortcut_folder(main_menu_items_list, folder_name)
