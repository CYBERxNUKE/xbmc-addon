# -*- coding: utf-8 -*-
import json
from modules.kodi_utils import addon, translate_path, path_exists, make_directorys, get_property, set_property
# from modules.kodi_utils import logger

def set_setting(setting_id, value):
	addon().setSetting(setting_id, value)

def get_setting(setting_id, fallback=None):
	try: settings_dict = json.loads(get_property('fen_settings'))
	except: settings_dict = make_settings_dict()
	if settings_dict is None: settings_dict = get_setting_fallback(setting_id)
	value = settings_dict.get(setting_id, '')
	if fallback is None: return value
	if value == '': return fallback
	return value

def get_setting_fallback(setting_id):
	return {setting_id: addon().getSetting(setting_id)}

def make_settings_dict():
	import xml.etree.ElementTree as ET
	settings_dict = None
	try:
		test_path = translate_path('special://profile/addon_data/plugin.video.fen/')
		profile_dir = 'special://profile/addon_data/plugin.video.fen/%s'
		if not path_exists(test_path): make_directorys(test_path)
		settings_xml = translate_path(profile_dir % 'settings.xml')
		root = ET.parse(settings_xml).getroot()
		settings_dict = {}
		for item in root:
			setting_id = item.get('id')
			setting_value = item.text
			if setting_value is None: setting_value = ''
			dict_item = {setting_id: setting_value}
			settings_dict.update(dict_item)
		set_property('fen_settings', json.dumps(settings_dict))
	except: pass
	return settings_dict
