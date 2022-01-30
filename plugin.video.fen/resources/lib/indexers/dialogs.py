# -*- coding: utf-8 -*-
import json
import metadata
from windows import open_window	
from modules import kodi_utils
from modules import settings
from modules.source_utils import clear_and_rescrape, clear_scrapers_cache, rescrape_with_disabled, scrape_with_custom_values
from modules.nav_utils import open_settings, clear_cache, refresh_cached_data
from modules.settings_reader import get_setting, set_setting
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
icon = kodi_utils.translate_path('special://home/addons/plugin.video.fen/icon.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')
icon_directory = 'special://home/addons/script.tikiart/resources/media/%s'

def trailer_choice(db_type, poster, tmdb_id, trailer_url, all_trailers=[]):
	if settings.get_language() != 'en' and not trailer_url and not all_trailers:
		from apis.tmdb_api import tmdb_media_videos
		try: all_trailers = tmdb_media_videos(db_type, tmdb_id)['results']
		except: pass
	if all_trailers:
		from modules.utils import clean_file_name, to_utf8
		if len(all_trailers) == 1:
			video_id = all_trailers[0].get('key')
		else:
			items = [{'line': clean_file_name(i['name']), 'function': i['key']} for i in all_trailers]
			video_id = open_window(['windows.extras', 'ShowSelectMedia'], 'select_media.xml', items=items, poster=poster)
			if video_id == None: return 'canceled'
		trailer_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
	return trailer_url

def genres_choice(db_type, genres, poster, return_genres=False):
	from modules.meta_lists import movie_genres, tvshow_genres
	def _process_dicts(genre_str, _dict):
		final_genres_list = []
		append = final_genres_list.append
		for key, value in _dict.items():
			if key in genre_str: append({'genre': key, 'value': value})
		return final_genres_list
	if db_type in ('movie', 'movies'): genre_action, meta_type, action = movie_genres, 'movie', 'tmdb_movies_genres'
	else: genre_action, meta_type, action = tvshow_genres, 'tvshow', 'tmdb_tv_genres'
	genre_list = _process_dicts(genres, genre_action)
	if return_genres: return genre_list
	if len(genre_list) == 0:
		kodi_utils.notification(32760, 2500)
		return None
	mode = 'build_%s_list' % meta_type
	items = [{'line': item['genre'], 'function': json.dumps({'mode': mode, 'action': action, 'genre_id': item['value'][0]})} for item in genre_list]
	return open_window(['windows.extras', 'ShowSelectMedia'], 'select_media.xml', items=items, poster=poster)

def imdb_keywords_choice(db_type, imdb_id, poster):
	from apis.imdb_api import imdb_keywords
	def _builder():
		for item in keywords_info:
			obj = {'line': item, 'function': json.dumps({'mode': mode, 'action': 'imdb_keywords_list_contents', 'list_id': item, 'iconImage': 'imdb.png'})}
			yield obj
	kodi_utils.show_busy_dialog()
	keywords_info = imdb_keywords(imdb_id)
	if len(keywords_info) == 0:
		kodi_utils.hide_busy_dialog()
		kodi_utils.notification(32760, 2500)
		return None
	meta_type = 'movie' if db_type == 'movies' else 'tvshow'
	mode = 'build_%s_list' % meta_type
	items = list(_builder())
	kodi_utils.hide_busy_dialog()
	return open_window(['windows.extras', 'ShowSelectMedia'], 'select_media.xml', items=items, poster=poster, context_active_action='keywords')

def imdb_videos_choice(videos, poster, media=True):
	try: videos = json.loads(videos)
	except: pass
	videos.sort(key=lambda x: x['quality_rank'])
	if media:
		items = [{'line': i['quality'], 'function': i['url']} for i in videos]
		choice = open_window(['windows.extras', 'ShowSelectMedia'], 'select_media.xml', items=items, poster=poster)
	else:
		dl = [i['quality'] for i in videos]
		fl = [i['url'] for i in videos]
		list_items = [{'line1': item, 'icon': poster} for item in dl]
		kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		choice = kodi_utils.select_dialog(fl, **kwargs)
	return choice

def trakt_manager_choice(params):
	if not get_setting('trakt_user', ''): return kodi_utils.notification(32760, 3500)
	icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/trakt.png')
	choices = [('%s %s...' % (ls(32602), ls(32199)), 'Add'), ('%s %s...' % (ls(32603), ls(32199)), 'Remove')]
	list_items = [{'line1': item[0], 'icon': icon} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32198).replace('[B]', '').replace('[/B]', ''), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = kodi_utils.select_dialog([i[1] for i in choices], **kwargs)
	if choice == None: return
	if choice == 'Add':
		from apis.trakt_api import trakt_add_to_list
		trakt_add_to_list(params)
	else:
		from apis.trakt_api import trakt_remove_from_list
		trakt_remove_from_list(params)

def playback_choice(content, poster, meta):
	items = [{'line': ls(32014), 'function': 'clear_and_rescrape'},
			{'line': ls(32006), 'function': 'rescrape_with_disabled'},
			{'line': ls(32135), 'function': 'scrape_with_custom_values'}]
	choice = open_window(['windows.extras', 'ShowSelectMedia'], 'select_media.xml', items=items, poster=poster)
	if choice == None: return
	from modules.source_utils import clear_and_rescrape, rescrape_with_disabled, scrape_with_custom_values
	if choice == 'clear_and_rescrape': clear_and_rescrape(content, meta)
	elif choice == 'rescrape_with_disabled': rescrape_with_disabled(content, meta)
	else: scrape_with_custom_values(content, meta)

def set_quality_choice(quality_setting):
	include = ls(32188)
	dl = ['%s SD' % include, '%s 720p' % include, '%s 1080p' % include, '%s 4K' % include]
	fl = ['SD', '720p', '1080p', '4K']
	try: preselect = [fl.index(i) for i in get_setting(quality_setting).split(', ')]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	choice = kodi_utils.select_dialog(fl, **kwargs)
	if choice is None: return
	if choice == []:
		kodi_utils.ok_dialog(text=32574, top_space=True)
		return set_quality_choice(quality_setting)
	set_setting(quality_setting, ', '.join(choice))

def extras_lists_choice():
	screenshots_directory = 'special://home/addons/script.tikiart/resources/screenshots/extras/%s'
	fl = [2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062]
	dl = [
			{'name': ls(32503),                            'image': kodi_utils.translate_path(screenshots_directory % '001_recommended.jpg')},
			{'name': ls(32607),                            'image': kodi_utils.translate_path(screenshots_directory % '002_reviews.jpg')},
			{'name': ls(32984),                            'image': kodi_utils.translate_path(screenshots_directory % '003_trivia.jpg')},
			{'name': ls(32986),                            'image': kodi_utils.translate_path(screenshots_directory % '004_blunders.jpg')},
			{'name': ls(32989),                            'image': kodi_utils.translate_path(screenshots_directory % '005_parentalguide.jpg')},
			{'name': ls(33032),                            'image': kodi_utils.translate_path(screenshots_directory % '006_videos.jpg')},
			{'name': ls(32616),                            'image': kodi_utils.translate_path(screenshots_directory % '007_posters.jpg')},
			{'name': ls(32617),                            'image': kodi_utils.translate_path(screenshots_directory % '008_fanart.jpg')},
			{'name': '%s %s' % (ls(32612), ls(32543)),     'image': kodi_utils.translate_path(screenshots_directory % '009_morefromyear.jpg')},
			{'name': '%s %s' % (ls(32612), ls(32470)),     'image': kodi_utils.translate_path(screenshots_directory % '010_morefromgenres.jpg')},
			{'name': '%s %s' % (ls(32612), ls(32480)),     'image': kodi_utils.translate_path(screenshots_directory % '011_morefromnetwork.jpg')},
			{'name': '%s %s' % (ls(32612), ls(32499)),     'image': kodi_utils.translate_path(screenshots_directory % '012_collection.jpg')}
			]
	try: preselect = [fl.index(i) for i in settings.extras_enabled_lists()]
	except: preselect = []
	kwargs = {'items': json.dumps(dl), 'preselect': preselect}
	selection = open_window(('windows.extras', 'ExtrasChooser'), 'extras_chooser.xml', **kwargs)
	if selection  == []: return set_setting('extras.enabled_lists', 'noop')
	elif selection == None: return
	selection = [str(fl[i]) for i in selection]
	set_setting('extras.enabled_lists', ','.join(selection))

def set_language_filter_choice(filter_setting):
	from modules.meta_lists import language_choices
	lang_choices = language_choices
	lang_choices.pop('None')
	dl = list(lang_choices.keys())
	fl = list(lang_choices.values())
	try: preselect = [fl.index(i) for i in get_setting(filter_setting).split(', ')]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	choice = kodi_utils.select_dialog(fl, **kwargs)
	if choice == None: return
	if choice == []:
		return set_setting(filter_setting, 'eng')
	set_setting(filter_setting, ', '.join(choice))

def enable_scrapers_choice():
	scrapers = ['external', 'furk', 'easynews', 'rd_cloud', 'pm_cloud', 'ad_cloud', 'folders']
	cloud_scrapers = {'rd_cloud': 'rd.enabled', 'pm_cloud': 'pm.enabled', 'ad_cloud': 'ad.enabled'}
	scraper_names = [ls(32118).upper(), ls(32069).upper(), ls(32070).upper(), ls(32098).upper(), ls(32097).upper(), ls(32099).upper(), ls(32108).upper()]
	preselect = [scrapers.index(i) for i in settings.active_internal_scrapers()]
	list_items = [{'line1': item} for item in scraper_names]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	choice = kodi_utils.select_dialog(scrapers, **kwargs)
	if choice is None: return
	for i in scrapers:
		set_setting('provider.%s' % i, ('true' if i in choice else 'false'))
		if i in cloud_scrapers and i in choice:
			set_setting(cloud_scrapers[i], 'true')

def folder_scraper_manager_choice(folder_info=None):
	def _get_property(setting_id):
		return kodi_utils.get_property('fen_%s' % setting_id) or get_setting(setting_id)
	def _set_property(setting_id, setting_value):
		kodi_utils.set_property('fen_%s' % setting_id, setting_value)
	def _clear_property(setting_id):
		kodi_utils.clear_property(setting_id)
	def _exit_save_settings():
		for folder_no in range(1,6):
			set_setting(name_setting % folder_no,  _get_property(name_setting % folder_no))
			set_setting(movie_dir_setting % folder_no,  _get_property(movie_dir_setting % folder_no))
			set_setting(tvshow_dir_setting % folder_no,  _get_property(tvshow_dir_setting % folder_no))
			_clear_property('fen_%s' % name_setting % folder_no)
			_clear_property('fen_%s' % movie_dir_setting % folder_no)
			_clear_property('fen_%s' % tvshow_dir_setting % folder_no)
	def _return(passed_folder_info):
		return folder_scraper_manager_choice(passed_folder_info)
	def _make_folders():
		return [{'number': folder_no, 'name': folder_names[folder_no], 'display_setting': name_setting % folder_no,
				'movie_setting': movie_dir_setting % folder_no, 'tvshow_setting': tvshow_dir_setting % folder_no, 'display': _get_property(name_setting % folder_no),
				'movie_dir': _get_property(movie_dir_setting % folder_no), 'tvshow_dir': _get_property(tvshow_dir_setting % folder_no)} \
				for folder_no in range(1,6)]
	def _update_folder_info():
		folder_info.update({'display': _get_property(name_setting % folder_info['number']), 'movie_dir': _get_property(movie_dir_setting % folder_info['number']),
							'tvshow_dir': _get_property(tvshow_dir_setting % folder_info['number'])})
	def _make_listing():
		return [('[B]%s[/B]:  [I]%s[/I]' % (folder_name_str, folder_info['display']), folder_info['display_setting']),
				('[B]%s[/B]:  [I]%s[/I]' % (movie_dir_str, folder_info['movie_dir']), folder_info['movie_setting']),
				('[B]%s[/B]:  [I]%s[/I]' % (tv_dir_str, folder_info['tvshow_dir']), folder_info['tvshow_setting'])]
	def _process_setting():
		if setting == None: _return(None)
		if 'display_name' in setting: _set_display()
		else: _set_folder_path()
	def _set_display():
		default = folder_info['display']
		folder_title = kodi_utils.dialog.input(folder_name_str, defaultt=default)
		if not folder_title: folder_title = 'None'
		_set_property(folder_info['display_setting'], folder_title)
		_return(folder_info)
	def _set_folder_path():
		if _get_property(setting) not in ('', 'None'):
			list_items = [{'line1': item} for item in [ls(32682), ls(32683)]]
			kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
			action = kodi_utils.select_dialog([1, 2], **kwargs)
			if action == None: _return(folder_info)
			if action == 1:
				_set_property(setting, 'None')
				_return(folder_info)
			else:
				folder = kodi_utils.dialog.browse(0, 'Fen', '')
				if not folder: folder = 'None'
				_set_property(setting, folder)
				_return(folder_info)
		else:
			folder = kodi_utils.dialog.browse(0, 'Fen', '')
			if not folder: folder = 'None'
			_set_property(setting, folder)
			_return(folder_info)
	try:
		choose_folder_str, folder_name_str, movie_dir_str, tv_dir_str = ls(32109), ls(32115), ls(32116), ls(32117)
		name_setting, movie_dir_setting, tvshow_dir_setting = 'folder%d.display_name', 'folder%d.movies_directory', 'folder%d.tv_shows_directory'
		folder_names = {1: ls(32110), 2: ls(32111), 3: ls(32112), 4: ls(32113), 5: ls(32114)}
		if not folder_info:
			folders = _make_folders()
			list_items = [{'line1': '%s:  [I]%s[/I]' % (item['name'], item['display'])} for item in folders]
			kwargs = {'items': json.dumps(list_items), 'heading': choose_folder_str, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
			folder_info = kodi_utils.select_dialog(folders, **kwargs)
			if folder_info == None: return _exit_save_settings()
		else: _update_folder_info()
		listing = _make_listing()
		list_items = [{'line1': item[0]} for item in listing]
		kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		setting = kodi_utils.select_dialog([i[1] for i in listing], **kwargs)
		_process_setting()
	except Exception as e:
		return

def results_sorting_choice():
	quality, provider, size = ls(32241), ls(32583), ls(32584)
	choices = [('%s, %s, %s' % (quality, provider, size), '0'), ('%s, %s, %s' % (quality, size, provider), '1'), ('%s, %s, %s' % (provider, quality, size), '2'),
			   ('%s, %s, %s' % (provider, size, quality), '3'), ('%s, %s, %s' % (size, quality, provider), '4'), ('%s, %s, %s' % (size, provider, quality), '5')]
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = kodi_utils.select_dialog(choices, **kwargs)
	if choice:
		set_setting('results.sort_order_display', choice[0])
		set_setting('results.sort_order', choice[1])

def results_highlights_choice():
	choices = ((ls(32240), '0'), (ls(32583), '1'), (ls(32241), '2'))
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = kodi_utils.select_dialog([i[1] for i in choices], **kwargs)
	if choice: return set_setting('highlight.type', choice)

def results_layout_choice():
	screenshots_directory = 'special://home/addons/script.tikiart/resources/screenshots/results/%s'
	xml_choices = [
					('List Default',                 kodi_utils.translate_path(screenshots_directory % 'source_results_list.default.jpg')),
					('List Contrast Default',        kodi_utils.translate_path(screenshots_directory % 'source_results_list.contrast.default.jpg')),
					('List Details',                 kodi_utils.translate_path(screenshots_directory % 'source_results_list.details.jpg')),
					('List Contrast Details',        kodi_utils.translate_path(screenshots_directory % 'source_results_list.contrast.details.jpg')),
					('InfoList Default',             kodi_utils.translate_path(screenshots_directory % 'source_results_infolist.default.jpg')),
					('InfoList Contrast Default',    kodi_utils.translate_path(screenshots_directory % 'source_results_infolist.contrast.default.jpg')),
					('InfoList Details',             kodi_utils.translate_path(screenshots_directory % 'source_results_infolist.details.jpg')),
					('InfoList Contrast Details',    kodi_utils.translate_path(screenshots_directory % 'source_results_infolist.contrast.details.jpg')),
					('Rows Default',                 kodi_utils.translate_path(screenshots_directory % 'source_results_rows.default.jpg')),
					('Rows Contrast Default',        kodi_utils.translate_path(screenshots_directory % 'source_results_rows.contrast.default.jpg')),
					('Rows Details',                 kodi_utils.translate_path(screenshots_directory % 'source_results_rows.details.jpg')),
					('Rows Contrast Details',        kodi_utils.translate_path(screenshots_directory % 'source_results_rows.contrast.details.jpg')),
					('Shift Default',                kodi_utils.translate_path(screenshots_directory % 'source_results_shift.default.jpg')),
					('Shift Contrast Default',       kodi_utils.translate_path(screenshots_directory % 'source_results_shift.contrast.default.jpg')),
					('Shift Details',                kodi_utils.translate_path(screenshots_directory % 'source_results_shift.details.jpg')),
					('Shift Contrast Details',       kodi_utils.translate_path(screenshots_directory % 'source_results_shift.contrast.details.jpg')),
					('Thumb Default',                kodi_utils.translate_path(screenshots_directory % 'source_results_thumb.default.jpg')),
					('Thumb Contrast Default',       kodi_utils.translate_path(screenshots_directory % 'source_results_thumb.contrast.default.jpg')),
					('Thumb Details',                kodi_utils.translate_path(screenshots_directory % 'source_results_thumb.details.jpg')),
					('Thumb Contrast Details',       kodi_utils.translate_path(screenshots_directory % 'source_results_thumb.contrast.details.jpg'))
					]
	choice = open_window(['windows.sources', 'SourceResultsChooser'], 'sources_chooser.xml', xml_choices=xml_choices)
	if choice: set_setting('results.xml_style', choice)

def set_subtitle_choice():
	choices = ((ls(32192), '0'), (ls(32193), '1'), (ls(32027), '2'))
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = kodi_utils.select_dialog([i[1] for i in choices], **kwargs)
	if choice: return set_setting('subtitles.subs_action', choice)

def scraper_dialog_color_choice(setting):
	setting ='int_dialog_highlight' if setting == 'internal' else 'ext_dialog_highlight'
	chosen_color = color_chooser('Fen')
	if chosen_color: set_setting(setting, chosen_color)

def scraper_quality_color_choice(setting):
	chosen_color = color_chooser('Fen')
	if chosen_color: set_setting(setting, chosen_color)

def scraper_color_choice(setting):
	choices = [('furk', 'provider.furk_colour'),
				('easynews', 'provider.easynews_colour'),
				('debrid_cloud', 'provider.debrid_cloud_colour'),
				('folders', 'provider.folders_colour'),
				('hoster', 'hoster.identify'),
				('torrent', 'torrent.identify'),
				('rd', 'provider.rd_colour'),
				('pm', 'provider.pm_colour'),
				('ad', 'provider.ad_colour'),
				('free', 'provider.free_colour')]
	setting = [i[1] for i in choices if i[0] == setting][0]
	chosen_color = color_chooser('Fen')
	if chosen_color: set_setting(setting, chosen_color)

def external_scrapers_manager():
	icon = kodi_utils.ext_addon('script.module.fenomscrapers').getAddonInfo('icon')
	all_color, hosters_color, torrent_color = 'mediumvioletred', get_setting('hoster.identify'), get_setting('torrent.identify')
	enable_string, disable_string, specific_string, all_string = ls(32055), ls(32024), ls(32536), ls(32525)
	scrapers_string, hosters_string, torrent_string = ls(32533), ls(33031), ls(32535)
	fs_default_string = ls(32137)
	all_scrapers_string = '%s %s' % (all_string, scrapers_string)
	hosters_scrapers_string = '%s %s' % (hosters_string, scrapers_string)
	torrent_scrapers_string = '%s %s' % (torrent_string, scrapers_string)
	enable_string_base = '%s %s %s %s' % (enable_string, all_string, '%s', scrapers_string)
	disable_string_base = '%s %s %s %s' % (disable_string, all_string, '%s', scrapers_string)
	enable_disable_string_base = '%s/%s %s %s %s' % (enable_string, disable_string, specific_string, '%s', scrapers_string)
	all_scrapers_base = '[COLOR %s]%s [/COLOR]' % (all_color, all_scrapers_string.upper())
	debrid_scrapers_base = '[COLOR %s]%s [/COLOR]' % (hosters_color, hosters_scrapers_string.upper())
	torrent_scrapers_base = '[COLOR %s]%s [/COLOR]' % (torrent_color, torrent_scrapers_string.upper())
	tools_menu = \
		[(all_scrapers_base, fs_default_string, {'mode': 'set_default_scrapers'}),
		(all_scrapers_base, enable_string_base % '', {'mode': 'toggle_all', 'folder': 'all', 'setting': 'true'}),
		(all_scrapers_base, disable_string_base % '', {'mode': 'toggle_all', 'folder': 'all', 'setting': 'false'}),
		(all_scrapers_base, enable_disable_string_base % '', {'mode': 'enable_disable', 'folder': 'all'}),
		(debrid_scrapers_base, enable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'true'}),
		(debrid_scrapers_base, disable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'false'}),
		(debrid_scrapers_base, enable_disable_string_base % hosters_string, {'mode': 'enable_disable', 'folder': 'hosters'}),
		(torrent_scrapers_base, enable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'true'}),
		(torrent_scrapers_base, disable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'false'}),
		(torrent_scrapers_base, enable_disable_string_base % torrent_string, {'mode': 'enable_disable', 'folder': 'torrents'})]
	list_items = [{'line1': item[0], 'line2': item[1], 'icon': icon} for item in tools_menu]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'true'}
	chosen_tool = kodi_utils.select_dialog(tools_menu, **kwargs)
	if chosen_tool == None: return
	from modules import source_utils
	params = chosen_tool[2]
	mode = params['mode']
	if mode == 'toggle_all':
		source_utils.toggle_all(params['folder'], params['setting'])
	elif mode == 'enable_disable':
		source_utils.enable_disable(params['folder'])
	elif mode == 'set_default_scrapers':
		source_utils.set_default_scrapers()
	kodi_utils.sleep(350)
	return external_scrapers_manager()

def meta_language_choice():
	from modules.meta_lists import meta_languages
	langs = meta_languages
	list_items = [{'line1': i['name']} for i in langs]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32145), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	list_choose = kodi_utils.select_dialog(langs, **kwargs)
	if list_choose == None: return None
	from caches.meta_cache import delete_meta_cache
	chosen_language = list_choose['iso']
	chosen_language_display = list_choose['name']
	set_setting('meta_language', chosen_language)
	set_setting('meta_language_display', chosen_language_display)
	delete_meta_cache(silent=True)

def favorites_choice(params):
	from modules.favourites import Favourites
	favourites = Favourites(params)
	db_type = params['db_type']
	tmdb_id = params['tmdb_id']
	title = params['title']
	current_favourites = favourites.get_favourites(db_type)
	if any(i['tmdb_id'] == tmdb_id for i in current_favourites):
		action = favourites.remove_from_favourites
		text = '%s Fen %s?' % (ls(32603), ls(32453))
	else:
		action = favourites.add_to_favourites
		text = '%s Fen %s?' % (ls(32602), ls(32453))
	if not kodi_utils.confirm_dialog(heading='Fen - %s' % title, text=text, top_space=True): return
	action()

def options_menu(params, meta=None):
	def _builder():
		for item in listing:
			line1 = item[0]
			line2 = item[1]
			if line2 == '': line2 = line1
			yield {'line1': line1, 'line2': line2}
	content = params.get('content', None)
	if not content: content = kodi_utils.container_content()[:-1]
	season = params.get('season', None)
	episode = params.get('episode', None)
	if not meta:
		function = metadata.movie_meta if content == 'movie' else metadata.tvshow_meta
		meta_user_info = metadata.retrieve_user_info()
		meta = function('tmdb_id', params['tmdb_id'], meta_user_info)
	watched_indicators = settings.watched_indicators()
	on_str, off_str, currently_str, open_str, settings_str = ls(32090), ls(32027), ls(32598), ls(32641), ls(32247)
	autoplay_status, autoplay_toggle, quality_setting = (on_str, 'false', 'autoplay_quality_%s' % content) if settings.auto_play(content) \
													else (off_str, 'true', 'results_quality_%s' % content)
	quality_filter_setting = 'autoplay_quality_%s' % content if autoplay_status == on_str else 'results_quality_%s' % content
	autoplay_next_status, autoplay_next_toggle = (on_str, 'false') if settings.autoplay_next_episode() else (off_str, 'true')
	results_xml_style_status = get_setting('results.xml_style', 'Default')
	results_filter_ignore_status, results_filter_ignore_toggle = (on_str, 'false') if settings.ignore_results_filter() else (off_str, 'true')
	results_sorting_status = get_setting('results.sort_order_display').replace('$ADDON[plugin.video.fen 32582]', ls(32582))
	current_results_highlights_action = get_setting('highlight.type')
	results_highlights_status = ls(32240) if current_results_highlights_action == '0' else ls(32583) if current_results_highlights_action == '1' else ls(32241)
	current_subs_action = get_setting('subtitles.subs_action')
	current_subs_action_status = 'Auto' if current_subs_action == '0' else ls(32193) if current_subs_action == '1' else off_str
	active_internal_scrapers = [i.replace('_', '') for i in settings.active_internal_scrapers()]
	current_scrapers_status = ', '.join([i for i in active_internal_scrapers]) if len(active_internal_scrapers) > 0 else 'N/A'
	current_quality_status =  ', '.join(settings.quality_filter(quality_setting))
	uncached_torrents_status, uncached_torrents_toggle = (on_str, 'false') if settings.display_uncached_torrents() else (off_str, 'true')
	listing = []
	base_str1 = '%s%s'
	base_str2 = '%s: [B]%s[/B]' % (currently_str, '%s')
	if content in ('movie', 'episode'):
		multi_line = 'true'
		listing += [(ls(32014), '', 'clear_and_rescrape')]
		listing += [(ls(32006), '', 'rescrape_with_disabled')]
		listing += [(ls(32135), '', 'scrape_with_custom_values')]
		listing += [(base_str1 % (ls(32175), ' (%s)' % content), base_str2 % autoplay_status, 'toggle_autoplay')]
		if autoplay_status == on_str and content == 'episode':
			listing += [(base_str1 % (ls(32178), ''), base_str2 % autoplay_next_status, 'toggle_autoplay_next')]
		listing += [(base_str1 % (ls(32105), ' (%s)' % content), base_str2 % current_quality_status, 'set_quality')]
		listing += [(base_str1 % ('', '%s %s' % (ls(32055), ls(32533))), base_str2 % current_scrapers_status, 'enable_scrapers')]
		if autoplay_status == off_str:
			listing += [(base_str1 % ('', ls(32140)), base_str2 % results_xml_style_status, 'set_results_xml_display')]
			listing += [(base_str1 % ('', ls(32151)), base_str2 % results_sorting_status, 'set_results_sorting')]
			listing += [(base_str1 % ('', ls(32138)), base_str2 % results_highlights_status, 'set_results_highlights')]
		listing += [(base_str1 % ('', ls(32686)), base_str2 % results_filter_ignore_status, 'set_results_filter_ignore')]
		listing += [(base_str1 % ('', ls(32183)), base_str2 % current_subs_action_status, 'set_subs_action')]
		if 'external' in active_internal_scrapers:
			listing += [(base_str1 % ('', ls(32160)), base_str2 % uncached_torrents_status, 'toggle_torrents_display_uncached')]
	else: multi_line = 'false'
	listing += [(ls(32046), '', 'extras_lists_choice')]
	if content in ('movie', 'tvshow') and meta: listing += [(ls(32604) % (ls(32028) if meta['mediatype'] == 'movie' else ls(32029)), '', 'clear_media_cache')]
	if watched_indicators == 1: listing += [(ls(32497) % ls(32037), '', 'clear_trakt_cache')]
	if content in ('movie', 'episode'): listing += [(ls(32637), '', 'clear_scrapers_cache')]
	listing += [('%s %s' % (ls(32118), ls(32513)), '', 'open_external_scrapers_manager')]
	listing += [('%s %s %s' % (open_str, ls(32522), settings_str), '', 'open_scraper_settings')]
	listing += [('%s %s %s' % (open_str, ls(32036), settings_str), '', 'open_fen_settings')]
	listing += [(ls(32640), '', 'save_and_exit')]
	list_items = list(_builder())
	heading = ls(32646).replace('[B]', '').replace('[/B]', '')
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': multi_line}
	choice = kodi_utils.select_dialog([i[2] for i in listing], **kwargs)
	if choice in (None, 'save_and_exit'): return
	elif choice == 'clear_and_rescrape': return clear_and_rescrape(content, meta, season, episode)
	elif choice == 'rescrape_with_disabled': return rescrape_with_disabled(content, meta, season, episode)
	elif choice == 'scrape_with_custom_values': return scrape_with_custom_values(content, meta, season, episode)
	elif choice == 'toggle_autoplay': set_setting('auto_play_%s' % content, autoplay_toggle)
	elif choice == 'toggle_autoplay_next': set_setting('autoplay_next_episode', autoplay_next_toggle)
	elif choice == 'enable_scrapers': enable_scrapers_choice()
	elif choice == 'set_results_xml_display': results_layout_choice()
	elif choice == 'set_results_sorting': results_sorting_choice()
	elif choice == 'set_results_filter_ignore': set_setting('ignore_results_filter', results_filter_ignore_toggle)
	elif choice == 'set_results_highlights': results_highlights_choice()
	elif choice == 'set_quality': set_quality_choice(quality_filter_setting)
	elif choice == 'set_subs_action': set_subtitle_choice()
	elif choice == 'extras_lists_choice': extras_lists_choice()
	elif choice == 'clear_media_cache': return refresh_cached_data(meta['mediatype'], 'tmdb_id', meta['tmdb_id'], meta['tvdb_id'], settings.get_language())
	elif choice == 'toggle_torrents_display_uncached': set_setting('torrent.display.uncached', uncached_torrents_toggle)
	elif choice == 'clear_trakt_cache': return clear_cache('trakt')
	elif choice == 'clear_scrapers_cache': return clear_scrapers_cache()
	elif choice == 'open_external_scrapers_manager': return external_scrapers_manager()
	elif choice == 'open_scraper_settings': return kodi_utils.execute_builtin('Addon.OpenSettings(script.module.fenomscrapers)')
	elif choice == 'open_fen_settings': return open_settings('0.0')
	if choice == 'clear_trakt_cache' and content in ('movie', 'tvshow', 'season', 'episode'): kodi_utils.execute_builtin('Container.Refresh')
	kodi_utils.show_busy_dialog()
	kodi_utils.sleep(200)
	kodi_utils.hide_busy_dialog()
	options_menu(params, meta=meta)

def extras_menu(params):
	function = metadata.movie_meta if params['db_type'] == 'movie' else metadata.tvshow_meta
	meta_user_info = metadata.retrieve_user_info()
	meta = function('tmdb_id', params['tmdb_id'], meta_user_info)
	open_window(['windows.extras', 'Extras'], 'extras.xml', meta=meta, is_widget=params.get('is_widget', 'false'), is_home=params.get('is_home', 'false'))

def media_extra_info(media_type, meta):
	extra_info = meta.get('extra_info', None)
	body = []
	append = body.append
	tagline_str, premiered_str, rating_str, votes_str, runtime_str = ls(32619), ls(32620), ls(32621), ls(32623), ls(32622)
	genres_str, budget_str, revenue_str, director_str, writer_str = ls(32624), ls(32625), ls(32626), ls(32627), ls(32628)
	studio_str, collection_str, homepage_str, status_str, type_str, classification_str = ls(32615), ls(32499), ls(32629), ls(32630), ls(32631), ls(32632)
	network_str, created_by_str, last_aired_str, next_aired_str, seasons_str, episodes_str = ls(32480), ls(32633), ls(32634), ls(32635), ls(32636), ls(32506)
	try:
		if media_type == 'movie':
			if 'tagline' in meta and meta['tagline']: append('[B]%s:[/B] %s' % (tagline_str, meta['tagline']))
			if 'alternative_titles' in meta and meta['alternative_titles']: append('[B]%s:[/B] %s' % ('Aliases', ', '.join(meta['alternative_titles'])))
			if 'status' in extra_info: append('[B]%s:[/B] %s' % (status_str, extra_info['status']))
			append('[B]%s:[/B] %s' % (premiered_str, meta['premiered']))
			append('[B]%s:[/B] %s (%s %s)' % (rating_str, meta['rating'], meta['votes'], votes_str))
			append('[B]%s:[/B] %d mins' % (runtime_str, int(float(meta['duration'])/60)))
			append('[B]%s:[/B] %s' % (genres_str, meta['genre']))
			if 'budget' in extra_info: append('[B]%s:[/B] %s' % (budget_str, extra_info['budget']))
			if 'revenue' in extra_info: append('[B]%s:[/B] %s' % (revenue_str, extra_info['revenue']))
			append('[B]%s:[/B] %s' % (director_str, meta['director']))
			append('[B]%s:[/B] %s' % (writer_str, meta['writer'] or 'N/A'))
			append('[B]%s:[/B] %s' % (studio_str, meta['studio'] or 'N/A'))
			if extra_info.get('collection_name'): append('[B]%s:[/B] %s' % (collection_str, extra_info['collection_name']))
			if extra_info.get('homepage'): append('[B]%s:[/B] %s' % (homepage_str, extra_info['homepage']))
		else:
			if 'type' in extra_info: append('[B]%s:[/B] %s' % (type_str, extra_info['type']))
			if 'alternative_titles' in meta and meta['alternative_titles']: append('[B]%s:[/B] %s' % ('Aliases', ', '.join(meta['alternative_titles'])))
			if 'status' in extra_info: append('[B]%s:[/B] %s' % (status_str, extra_info['status']))
			append('[B]%s:[/B] %s' % (premiered_str, meta['premiered']))
			append('[B]%s:[/B] %s (%s %s)' % (rating_str, meta['rating'], meta['votes'], votes_str))
			append('[B]%s:[/B] %d mins' % (runtime_str, int(float(meta['duration'])/60)))
			append('[B]%s:[/B] %s' % (classification_str, meta['mpaa']))
			append('[B]%s:[/B] %s' % (genres_str, meta['genre']))
			append('[B]%s:[/B] %s' % (network_str, meta['studio']))
			if 'created_by' in extra_info: append('[B]%s:[/B] %s' % (created_by_str, extra_info['created_by']))
			if extra_info.get('last_episode_to_air', False):
				last_ep = extra_info['last_episode_to_air']
				lastep_str = '[%s] S%.2dE%.2d - %s' % (last_ep['air_date'], last_ep['season_number'], last_ep['episode_number'], last_ep['name'])
				append('[B]%s:[/B] %s' % (last_aired_str, lastep_str))
			if extra_info.get('next_episode_to_air', False):
				next_ep = extra_info['next_episode_to_air']
				nextep_str = '[%s] S%.2dE%.2d - %s' % (next_ep['air_date'], next_ep['season_number'], next_ep['episode_number'], next_ep['name'])
				append('[B]%s:[/B] %s' % (next_aired_str, nextep_str))
			append('[B]%s:[/B] %s' % (seasons_str, meta['total_seasons']))
			append('[B]%s:[/B] %s' % (episodes_str, meta['total_aired_eps']))
			if 'homepage' in extra_info: append('[B]%s:[/B] %s' % (homepage_str, extra_info['homepage']))
	except: return kodi_utils.notification(32574, 2000)
	return '\n\n'.join(body)

def color_chooser(msg_dialog, no_color=False):
	from modules.meta_lists import meta_colors
	color_chart = meta_colors
	color_display = ['[COLOR=%s]%s[/COLOR]' % (i, i.capitalize()) for i in color_chart]
	if no_color:
		color_chart.insert(0, 'No Color')
		color_display.insert(0, 'No Color')
	list_items = [{'line1': item} for item in color_display]
	kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = kodi_utils.select_dialog(color_chart, **kwargs)
	if choice == None: return
	return choice
