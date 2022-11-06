# -*- coding: utf-8 -*-
import time
import datetime
import xml.etree.ElementTree as ET
from caches import check_databases, clean_databases
from apis.trakt_api import trakt_sync_activities
from modules import kodi_utils, settings

logger, json, run_addon, confirm_dialog, close_dialog = kodi_utils.logger, kodi_utils.json, kodi_utils.run_addon, kodi_utils.confirm_dialog, kodi_utils.close_dialog
ls, path_exists, translate_path, execute_builtin = kodi_utils.local_string, kodi_utils.path_exists, kodi_utils.translate_path, kodi_utils.execute_builtin
get_property, set_property, clear_property, get_visibility = kodi_utils.get_property, kodi_utils.set_property, kodi_utils.clear_property, kodi_utils.get_visibility
make_directories, kodi_refresh, list_dirs, delete_file = kodi_utils.make_directories, kodi_utils.kodi_refresh, kodi_utils.list_dirs, kodi_utils.delete_file
get_setting, set_setting, make_settings_dict, external_browse = kodi_utils.get_setting, kodi_utils.set_setting, kodi_utils.make_settings_dict, kodi_utils.external_browse
disable_enable_addon, update_local_addons, get_infolabel, run_plugin = kodi_utils.disable_enable_addon, kodi_utils.update_local_addons, kodi_utils.get_infolabel, kodi_utils.run_plugin
get_window_id, clean_settings, Thread, make_window_properties = kodi_utils.get_window_id, kodi_utils.clean_settings, kodi_utils.Thread, kodi_utils.make_window_properties
trakt_sync_interval, trakt_sync_refresh_widgets, auto_start_fen = settings.trakt_sync_interval, settings.trakt_sync_refresh_widgets, settings.auto_start_fen
custom_context_prop, custom_info_prop, pause_settings_prop = kodi_utils.custom_context_prop, kodi_utils.custom_info_prop, kodi_utils.pause_settings_prop
pause_services_prop = kodi_utils.pause_services_prop
media_db_types, media_windows = ('movie', 'tvshow', 'season', 'episode'), (10000, 10025)
fen_str, window_top_str = ls(32036).upper(), 'Window.IsTopMost(%s)'

class InitializeDatabases:
	def run(self):
		logger(fen_str, 'InitializeDatabases Service Starting')
		check_databases()
		return logger(fen_str, 'InitializeDatabases Service Finished')

class DatabaseMaintenance:
	def run(self):
		logger(fen_str, 'Database Maintenance Service Starting')
		time = datetime.datetime.now()
		current_time = self._get_timestamp(time)
		due_clean = int(get_setting('database.maintenance.due', '0'))
		if due_clean == 0:
			next_clean = str(int(self._get_timestamp(time + datetime.timedelta(days=3))))
			set_setting('database.maintenance.due', next_clean)
			return logger(fen_str, 'Database Maintenance Service First Run - Skipping')
		if current_time >= due_clean:
			clean_databases(current_time, database_check=False, silent=True)
			next_clean = str(int(self._get_timestamp(time + datetime.timedelta(days=3))))
			set_setting('database.maintenance.due', next_clean)
			return logger(fen_str, 'Database Maintenance Service Finished')
		else: return logger(fen_str, 'Database Maintenance Service Finished - Not Run')

	def _get_timestamp(self, date_time):
		return int(time.mktime(date_time.timetuple()))

class CheckSettings:
	def run(self):
		logger(fen_str, 'CheckSettingsFile Service Starting')
		monitor = kodi_utils.monitor
		clear_property('fen_settings')
		profile_dir = kodi_utils.userdata_path
		if not path_exists(profile_dir): make_directories(profile_dir)
		addon_version = kodi_utils.addon().getAddonInfo('version')
		set_setting('version_number', addon_version)
		monitor.waitForAbort(0.5)
		make_settings_dict()
		make_window_properties()
		try: del monitor
		except: pass
		return logger(fen_str, 'CheckSettingsFile Service Finished')

class CleanSettings:
	def run(self):
		logger(fen_str, 'CleanSettings Service Starting')
		clean_settings(silent=True)
		return logger(fen_str, 'CleanSettings Service Finished')

class FirstRunActions:
	def run(self):
		logger(fen_str, 'CheckUpdateActions Service Starting')
		addon_version, settings_version =  self.remove_alpha(kodi_utils.addon().getAddonInfo('version')), self.remove_alpha(get_setting('version_number'))
		if addon_version != settings_version:
			set_setting('version_number', addon_version)
			logger(fen_str, 'CheckUpdateActions Running Update Actions....')
			self.update_action()
		return logger(fen_str, 'CheckUpdateActions Service Finished')

	def update_action(self):
		''' Put code that needs to run once on update here'''
		return

	def remove_alpha(self, string):
		return ''.join(c for c in string if (c.isdigit() or c =='.'))

class ReuseLanguageInvokerCheck:
	def run(self):
		logger(fen_str, 'ReuseLanguageInvokerCheck Service Starting')
		addon_xml = translate_path('special://home/addons/plugin.video.fen/addon.xml')
		tree = ET.parse(addon_xml)
		root = tree.getroot()
		current_addon_setting = get_setting('reuse_language_invoker', 'true')
		refresh, text = True, '%s\n%s' % (ls(33021), ls(33020))
		for item in root.iter('reuselanguageinvoker'):
			if item.text == current_addon_setting: refresh = False; break
			item.text = current_addon_setting
			tree.write(addon_xml)
			break
		if refresh and confirm_dialog(text=text):
			update_local_addons()
			disable_enable_addon()
		return logger(fen_str, 'ReuseLanguageInvokerCheck Service Finished')

class TraktMonitor:
	def run(self):
		logger(fen_str, 'TraktMonitor Service Starting')
		monitor, player = kodi_utils.monitor, kodi_utils.player
		trakt_service_string = 'TraktMonitor Service Update %s - %s'
		update_string = 'Next Update in %s minutes...'
		interval = 30 * 60
		while not monitor.abortRequested():
			try:
				while player.isPlayingVideo() or get_property(pause_services_prop) == 'true': monitor.waitForAbort(10)
				value, interval = trakt_sync_interval()
				next_update_string = update_string % value
				status = trakt_sync_activities()
				if status == 'success':
					logger(fen_str, trakt_service_string % ('Success', 'Trakt Update Performed'))
					if trakt_sync_refresh_widgets():
						kodi_refresh()
						logger(fen_str, trakt_service_string % ('Widgets Refresh', 'Setting Activated. Widget Refresh Performed'))
					else: logger(fen_str, trakt_service_string % ('Widgets Refresh', 'Setting Disabled. Skipping Widget Refresh'))
				elif status == 'no account': logger(fen_str, trakt_service_string % ('Aborted. No Trakt Account Active', next_update_string))
				elif status == 'failed': logger(fen_str, trakt_service_string % ('Failed. Error from Trakt', next_update_string))
				else: logger(fen_str, trakt_service_string % ('Success. No Changes Needed', next_update_string))# 'not needed'
			except Exception as e: logger(fen_str, trakt_service_string % ('Failed', 'The following Error Occured: %s' % str(e)))
			monitor.waitForAbort(interval)
		try: del monitor
		except: pass
		try: del player
		except: pass
		return logger(fen_str, 'TraktMonitor Service Finished')

class CustomActions:
	def run(self, dialog_type):
		logger(fen_str, 'CustomActions %s Service Starting' % dialog_type.upper())
		monitor, player = kodi_utils.monitor, kodi_utils.player
		if dialog_type == 'context_menu': window, setting_property, params = 'contextmenu', custom_context_prop, 'fen_options_params'
		else: window, setting_property, params = 'movieinformation', custom_info_prop, 'fen_extras_params'
		while not monitor.abortRequested():
			if not get_property(setting_property) == 'true' or get_property(pause_services_prop) == 'true' or player.isPlayingVideo():
				monitor.waitForAbort(2)
				continue
			while not get_visibility(window_top_str % window):
				if monitor.abortRequested(): break
				if not get_property(setting_property) == 'true' or get_property(pause_services_prop) == 'true' or player.isPlayingVideo(): monitor.waitForAbort(2)
				while not get_window_id() in media_windows: monitor.waitForAbort(2)
				in_fen = not external_browse()
				is_widget = get_infolabel('ListItem.Property(fen_widget)') == 'true'
				if (in_fen or is_widget):
					db_type, action = get_infolabel('ListItem.dbtype'), get_infolabel('ListItem.Property(%s)' % params)
					monitor.waitForAbort(0.25)
				else: monitor.waitForAbort(1)
			try:
				if (in_fen or is_widget) and db_type in media_db_types and action:
					close_dialog(window)
					Thread(target=run_plugin, args=(action,)).start()
					while get_visibility(window_top_str % window): monitor.waitForAbort(0.25)
				else: monitor.waitForAbort(1)
			except: monitor.waitForAbort(2)
		try: del monitor
		except: pass
		try: del player
		except: pass
		return logger(fen_str, 'CustomActions %s Service Finished' % dialog_type.upper())

class ClearSubs:
	def run(self):
		logger(fen_str, 'Clear Subtitles Service Starting')
		sub_formats = ('.srt', '.ssa', '.smi', '.sub', '.idx', '.nfo')
		subtitle_path = 'special://temp/%s'
		files = list_dirs(translate_path('special://temp/'))[1]
		for i in files:
			if i.startswith('FENSubs_') or i.endswith(sub_formats): delete_file(translate_path(subtitle_path % i))
		return logger(fen_str, 'Clear Subtitles Service Finished')

class AutoRun:
	def run(self):
		logger(fen_str, 'AutoRun Service Starting')
		if auto_start_fen(): run_addon()
		return logger(fen_str, 'AutoRun Service Finished')

class OnSettingsChangedActions:
	def run(self):
		if get_property(pause_settings_prop) != 'true':
			make_settings_dict()
			make_window_properties(override=True)

class OnNotificationActions:
	def run(self, sender, method, data):
		if sender == 'xbmc':
			if method in ('GUI.OnScreensaverActivated', 'System.OnSleep'): set_property(pause_services_prop, 'true')
			elif method in ('GUI.OnScreensaverDeactivated', 'System.OnWake'): clear_property(pause_services_prop)
