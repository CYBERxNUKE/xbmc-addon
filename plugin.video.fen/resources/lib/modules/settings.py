# -*- coding: utf-8 -*-
from modules.kodi_utils import translate_path
from modules.settings_reader import get_setting
# from modules.kodi_utils import logger

def skin_location():
	return translate_path('special://home/addons/plugin.video.fen')

def date_offset():
	return int(get_setting('datetime.offset', '0')) + 5

def results_xml_style():
	return str(get_setting('results.xml_style', 'List Contrast Details').lower())

def results_xml_window_number(window_style=None):
	if not window_style: window_style = results_xml_style()
	return {'list': 2000, 'infolist': 2001, 'rows': 2002, 'shift': 2003, 'thumb': 2004}[window_style.split(' ')[0]]

def store_resolved_torrent_to_cloud(debrid_service):
	return get_setting('store_torrent.%s' % debrid_service.lower()) == 'true'

def enabled_debrids_check(debrid_service):
	enabled = get_setting('%s.enabled' % debrid_service) == 'true'
	if not enabled: return False
	authed = get_setting('%s.token' % debrid_service)
	if authed in (None, ''): return False
	return True

def display_sleep_time():
	return 100

def show_specials():
	return get_setting('show_specials') == 'true'

def include_year_in_title(db_type):
	settings_dict = {'movie': (1, 3), 'tvshow': (2, 3)}
	setting = int(get_setting('include_year_in_title', '0'))
	return setting in settings_dict[db_type]
	
def movies_directory():
	return translate_path(get_setting('movies_directory'))
	
def tv_show_directory():
	return translate_path(get_setting('tv_shows_directory'))

def download_directory(db_type):
	if db_type == 'movie': setting = 'movie_download_directory'
	elif db_type == 'episode': setting = 'tvshow_download_directory'
	elif db_type in ('thumb_url', 'image_url', 'image'): setting = 'image_download_directory'
	else: setting = 'premium_download_directory'
	if get_setting(setting) != '': return translate_path(get_setting(setting))
	else: return False

def source_folders_directory(db_type, source):
	setting = '%s.movies_directory' % source if db_type == 'movie' else '%s.tv_shows_directory' % source
	if get_setting(setting) not in ('', 'None', None): return translate_path( get_setting(setting))
	else: return False

def paginate():
	return get_setting('paginate.lists') == 'true'

def page_limit():
	return int(get_setting('page_limit', '20'))

def ignore_articles():
	return get_setting('ignore_articles') == 'true'

def default_all_episodes():
	return int(get_setting('default_all_episodes'))

def quality_filter(setting):
	return get_setting(setting).split(', ')

def include_prerelease_results():
	return get_setting('include_prerelease_results') == 'true'

def auto_play(db_type):
	return get_setting('auto_play_%s' % db_type) == 'true'

def autoplay_next_episode():
	if auto_play('episode') and get_setting('autoplay_next_episode') == 'true': return True
	else: return False

def autoplay_next_check_threshold():
	return int(get_setting('autoplay_next_check_threshold', '3'))

def autoplay_next_show_window():
	return get_setting('autoplay_next_show_window') == 'true'

def autoplay_next_window_time():
	return int(get_setting('autoplay_next_window_time', '20'))

def autoplay_next_window_percentage():
	return int(get_setting('autoplay_next_window_percentage', '95'))

def autoplay_next_window_timer_method():
	return {'0': 'time', '1': 'percentage'}[get_setting('autoplay_next_window_timer_method')]

def autoplay_next_settings():
	scraper_time = int(get_setting('scrapers.timeout.1', '60')) + 20
	threshold = autoplay_next_check_threshold()
	run_popup = autoplay_next_show_window()
	timer_method = autoplay_next_window_timer_method()
	window_time = autoplay_next_window_time() + 1
	window_percentage = 100 - autoplay_next_window_percentage()
	return {'scraper_time': scraper_time, 'threshold': threshold, 'run_popup': run_popup, 'timer_method': timer_method,
			'window_time': window_time, 'window_percentage': window_percentage}

def filter_status(filter_type):
	return int(get_setting('filter_%s' % filter_type, '0'))

def ignore_results_filter():
	return get_setting('ignore_results_filter') == 'true'

def display_uncached_torrents():
	return get_setting('torrent.display.uncached', 'false') == 'true'
	
def trakt_sync_interval():
	setting = get_setting('trakt.sync_interval', '25')
	interval = int(setting) * 60
	return setting, interval

def trakt_sync_refresh_widgets():
	return get_setting('trakt.sync_refresh_widgets') == 'true'

def calendar_focus_today():
	return get_setting('trakt.calendar_focus_today') == 'true'

def calendar_sort_order():
	return int(get_setting('trakt.calendar_sort_order', '0'))

def auto_start_fen():
	return get_setting('auto_start_fen') == 'true'

def sync_kodi_library_watchstatus():
	return get_setting('sync_kodi_library_watchstatus') == 'true'

def furk_active():
	if get_setting('provider.furk', 'false') == 'true':
		if not get_setting('furk_api_key'):
			furk_status = False if '' in (get_setting('furk_login'), get_setting('furk_password')) else True
		else: furk_status = True
	else: furk_status = False
	return furk_status

def easynews_active():
	if get_setting('provider.easynews', 'false') == 'true':
		easynews_status = False if '' in (get_setting('easynews_user'), get_setting('easynews_password')) else True
	else: easynews_status = False
	return easynews_status

def watched_indicators():
	if get_setting('trakt_user') == '': return 0
	return int(get_setting('watched_indicators','0'))

def extras_open_action(db_type):
	return int(get_setting('extras.open_action', '0')) in {'movie': (1, 3), 'tvshow': (2, 3)}[db_type]

def extras_enable_scrollbars():
	return get_setting('extras.enable_scrollbars', 'true')

def extras_enable_highlight_colors():
	return get_setting('extras.enable_highlight_colors', 'true') == 'true'

def extras_exclude_non_acting():
	return get_setting('extras.exclude_non_acting_roles', 'true') == 'true'

def extras_enabled_lists():
	settings = get_setting('extras.enabled_lists')
	if settings in ('', None, 'noop', []): return []
	return [int(i) for i in get_setting('extras.enabled_lists').split(',')]

def check_prescrape_sources(scraper):
	if scraper in ('furk', 'easynews', 'rd_cloud', 'pm_cloud', 'ad_cloud'): return get_setting('check.%s' % scraper) == 'true'
	if get_setting('check.%s' % scraper) == 'true' and get_setting('auto_play') != 'true': return True
	else: return False

def filter_by_name(scraper):
	return get_setting('%s.title_filter' % scraper, 'false') == 'true'

def easynews_language_filter():
	enabled = get_setting('easynews.filter_lang') == 'true'
	if enabled: filters = get_setting('easynews.lang_filters').split(', ')
	else: filters = []
	return enabled, filters

def results_sort_order():
	return (
			lambda k: (k['quality_rank'], k['provider_rank'], -k['size']), #Quality, Provider, Size
			lambda k: (k['quality_rank'], -k['size'], k['provider_rank']), #Quality, Size, Provider
			lambda k: (k['provider_rank'], k['quality_rank'], -k['size']), #Provider, Quality, Size
			lambda k: (k['provider_rank'], -k['size'], k['quality_rank']), #Provider, Size, Quality
			lambda k: (-k['size'], k['quality_rank'], k['provider_rank']), #Size, Quality, Provider
			lambda k: (-k['size'], k['provider_rank'], k['quality_rank'])  #Size, Provider, Quality
			)[int(get_setting('results.sort_order', '1'))]

def active_internal_scrapers():
	clouds = [('rd', 'provider.rd_cloud'), ('pm', 'provider.pm_cloud'), ('ad', 'provider.ad_cloud')]
	settings = ['provider.external', 'provider.furk', 'provider.easynews', 'provider.folders']
	settings_append = settings.append
	for item in clouds:
		if enabled_debrids_check(item[0]):
			settings_append(item[1])
	active = [i.split('.')[1] for i in settings if get_setting(i) == 'true']
	return active

def provider_sort_ranks():
	fu_priority = int(get_setting('fu.priority', '6'))
	en_priority = int(get_setting('en.priority', '7'))
	pm_priority = int(get_setting('pm.priority', '8'))
	ad_priority = int(get_setting('ad.priority', '9'))
	rd_priority = int(get_setting('rd.priority', '10'))
	return {'furk': fu_priority, 'easynews': en_priority, 'real-debrid': rd_priority, 'premiumize.me': pm_priority, 'alldebrid': ad_priority,
			'rd_cloud': rd_priority, 'pm_cloud': pm_priority, 'ad_cloud': ad_priority, 'folders': 0}

def sort_to_top(provider):
	return get_setting({'folders': 'results.sort_folders_first', 'rd_cloud': 'results.sort_rdcloud_first', 'pm_cloud': 'results.sort_pmcloud_first',
						'ad_cloud': 'results.sort_adcloud_first'}[provider]) == 'true'

def auto_resume(db_type):
	auto_resume = get_setting('auto_resume_%s' % db_type)
	if auto_resume == '1': return True
	if auto_resume == '2' and auto_play(db_type): return True
	else: return False

def nav_jump_use_alphabet():
	return get_setting('nav_jump') == '1'

def use_season_title():
	return get_setting('use_season_title') == 'true'

def show_unaired():
	return get_setting('show_unaired') == 'true'

def thumb_fanart():
	return get_setting('thumb_fanart') == 'true'

def single_ep_format():
	return {0: '%d-%m-%Y', 1: '%Y-%m-%d', 2: '%m-%d-%Y'}[int(get_setting('single_ep_format', '1'))]

def single_ep_display_title():
	return int(get_setting('single_ep_display', '0'))

def nextep_display_settings():
	include_airdate = get_setting('nextep.include_airdate') == 'true'
	return {'unaired_color': 'red', 'unwatched_color': 'darkgoldenrod', 'include_airdate': include_airdate}

def nextep_content_settings():
	sort_type = int(get_setting('nextep.sort_type'))
	sort_order = int(get_setting('nextep.sort_order'))
	sort_direction = sort_order == 0
	sort_key = 'fen_last_played' if sort_type == 0 else 'fen_first_aired' if sort_type == 1 else 'fen_name'
	include_unaired = get_setting('nextep.include_unaired') == 'true'
	include_unwatched = get_setting('nextep.include_unwatched') == 'true'
	sort_airing_today_to_top = get_setting('nextep.sort_airing_today_to_top', 'false') == 'true'
	return {'sort_key': sort_key, 'sort_direction': sort_direction, 'sort_type': sort_type, 'sort_order':sort_order,
			'include_unaired': include_unaired, 'include_unwatched': include_unwatched, 'sort_airing_today_to_top': sort_airing_today_to_top}

def scraping_settings():
	def provider_color(provider, fallback):
		return get_setting('provider.%s_colour' % provider, fallback)
	highlight_type = int(get_setting('highlight.type', '0'))
	hoster_highlight, torrent_highlight = '', ''
	furk_highlight, easynews_highlight, debrid_cloud_highlight, folders_highlight = '', '', '', ''
	rd_highlight, pm_highlight, ad_highlight = '', '', ''
	highlight_4K, highlight_1080P, highlight_720P, highlight_SD = '', '', '', ''
	if highlight_type in (0, 1):
		furk_highlight = provider_color('furk', 'crimson')
		easynews_highlight = provider_color('easynews', 'limegreen')
		debrid_cloud_highlight = provider_color('debrid_cloud', 'darkviolet')
		folders_highlight = provider_color('folders', 'darkgoldenrod')
		if highlight_type == 0:
			hoster_highlight = get_setting('hoster.identify', 'dodgerblue')
			torrent_highlight = get_setting('torrent.identify', 'fuchsia')
		else:
			rd_highlight = provider_color('rd', 'seagreen')
			pm_highlight = provider_color('pm', 'orangered')
			ad_highlight = provider_color('ad', 'goldenrod')
	else:
		highlight_4K = get_setting('scraper_4k_highlight', 'fuchsia')
		highlight_1080P = get_setting('scraper_1080p_highlight', 'lawngreen')
		highlight_720P = get_setting('scraper_720p_highlight', 'gold')
		highlight_SD = get_setting('scraper_SD_highlight', 'lightsaltegray')
	return {'highlight_type': highlight_type, 'hoster_highlight': hoster_highlight, 'torrent_highlight': torrent_highlight,'real-debrid': rd_highlight, 'premiumize': pm_highlight,
			'alldebrid': ad_highlight, 'rd_cloud': debrid_cloud_highlight, 'pm_cloud': debrid_cloud_highlight, 'ad_cloud': debrid_cloud_highlight, 'furk': furk_highlight,
			'easynews': easynews_highlight, 'folders': folders_highlight, '4k': highlight_4K, '1080p': highlight_1080P, '720p': highlight_720P, 'sd': highlight_SD}

def get_fanart_data():
	return get_setting('get_fanart_data') == 'true'

def fanarttv_client_key():
	return get_setting('fanart_client_key', 'fe073550acf157bdb8a4217f215c0882')

def tmdb_api_key():
	return get_setting('tmdb_api', '050ee5c6c85883b200be501c878a2aed')

def get_resolution():
	return (
			{'poster': 'w185', 'fanart': 'w300', 'still': 'w185', 'profile': 'w185'},
			{'poster': 'w342', 'fanart': 'w780', 'still': 'w300', 'profile': 'w185'},
			{'poster': 'w780', 'fanart': 'w1280', 'still': 'original', 'profile': 'h632'},
			{'poster': 'original', 'fanart': 'original', 'still': 'original', 'profile': 'original'}
			)[int(get_setting('image_resolutions', '2'))]

def get_language():
	return get_setting('meta_language', 'en')

def get_art_provider():
	if not get_fanart_data(): return ('poster', 'poster2', 'fanart', 'fanart2')
	return {True: ('poster2', 'poster', 'fanart2', 'fanart'), False: ('poster', 'poster2', 'fanart', 'fanart2')}[get_setting('fanarttv.default') == 'true']

def user_info():
	tmdb_api = tmdb_api_key()
	extra_fanart_enabled = get_fanart_data()
	image_resolution = get_resolution()
	meta_language = get_language()
	if extra_fanart_enabled: fanart_client_key = fanarttv_client_key()
	else: fanart_client_key = ''
	return {'extra_fanart_enabled': extra_fanart_enabled, 'image_resolution': image_resolution , 'language': meta_language,
			'fanart_client_key': fanart_client_key, 'tmdb_api': tmdb_api}

def make_global_list():
	global global_list
	global_list = []
