# -*- coding: utf-8 -*-
from modules.kodi_utils import sys, parse_qsl
# from modules.kodi_utils import logger

def routing():
	params = dict(parse_qsl(sys.argv[2][1:], keep_blank_values=True))
	_get = params.get
	mode = _get('mode', 'navigator.main')
	if 'navigator.' in mode:
		from indexers.navigator import Navigator
		exec('Navigator(params).%s()' % mode.split('.')[1])
	elif 'menu_editor' in mode:
		from modules.menu_editor import MenuEditor
		exec('MenuEditor(params).%s()' % mode.split('.')[1])
	elif 'discover.' in mode:
		from indexers.discover import Discover
		exec('Discover(params).%s()' % mode.split('.')[1])
	elif 'furk.' in mode:
		if mode == 'furk.browse_packs':
			from modules.sources import Sources
			Sources().furkPacks(_get('file_name'), _get('file_id'))
		elif mode == 'furk.add_to_files':
			from indexers.furk import add_to_files
			add_to_files(_get('item_id'))
		elif mode == 'furk.remove_from_files':
			from indexers.furk import remove_from_files
			remove_from_files(_get('item_id'))
		elif mode == 'furk.remove_from_downloads':
			from indexers.furk import remove_from_downloads
			remove_from_downloads(_get('item_id'))
		elif mode == 'furk.remove_from_files':
			from indexers.furk import add_uncached_file
			add_uncached_file(_get('id'))
		elif mode == 'furk.myfiles_protect_unprotect':
			from indexers.furk import myfiles_protect_unprotect
			myfiles_protect_unprotect(_get('action'), _get('name'), _get('item_id'))
		else:
			from indexers import furk
			exec('furk.%s(params)' % mode.split('.')[1])
	elif 'easynews.' in mode:
		from indexers import easynews
		exec('easynews.%s(params)' % mode.split('.')[1])
	elif '_play' in mode or 'play_' in mode:
		if mode == 'play_media':
			from modules.sources import Sources
			Sources().playback_prep(params)
		elif mode == 'media_play':
			from modules.player import FenPlayer
			FenPlayer().run(_get('url', None), _get('obj', None))
	elif 'choice' in mode:
		from indexers import dialogs
		if mode == 'scraper_color_choice': dialogs.scraper_color_choice(_get('setting'))
		elif mode == 'scraper_dialog_color_choice': dialogs.scraper_dialog_color_choice(_get('setting'))
		elif mode == 'scraper_quality_color_choice': dialogs.scraper_quality_color_choice(_get('setting'))
		elif mode == 'imdb_images_choice': dialogs.imdb_images_choice(_get('imdb_id'), _get('rootname'))
		elif mode == 'set_quality_choice': dialogs.set_quality_choice(_get('quality_setting'))
		elif mode == 'results_sorting_choice': dialogs.results_sorting_choice()
		elif mode == 'results_layout_choice': dialogs.results_layout_choice()
		elif mode == 'options_menu_choice': dialogs.options_menu(params)
		elif mode == 'meta_language_choice': dialogs.meta_language_choice()
		elif mode == 'extras_menu_choice': dialogs.extras_menu(params)
		elif mode == 'enable_scrapers_choice': dialogs.enable_scrapers_choice()
		elif mode == 'favorites_choice': dialogs.favorites_choice(params)
		elif mode == 'trakt_manager_choice': dialogs.trakt_manager_choice(params)
		elif mode == 'folder_scraper_manager_choice': dialogs.folder_scraper_manager_choice(params)
		elif mode == 'set_language_filter_choice': dialogs.set_language_filter_choice(_get('filter_setting'))
		elif mode == 'media_extra_info_choice': dialogs.media_extra_info(_get('media_type'), _get('meta'))
		elif mode == 'extras_lists_choice': dialogs.extras_lists_choice()
		elif mode == 'highlight_choice': dialogs.highlight_choice()
		elif mode == 'easynews_use_custom_farm_choice': dialogs.easynews_use_custom_farm_choice()
		elif mode == 'easynews_server_choice': dialogs.easynews_server_choice()
		elif mode == 'navigate_to_page_choice': dialogs.navigate_to_page_choice(params)
		elif mode == 'link_folders_choice': dialogs.link_folders_choice(params['service'], params['folder_id'], params['action'])
		elif mode == 'movie_sets_to_collection_choice': dialogs.movie_sets_to_collection_choice(_get('collection_id'))
		elif mode == 'clear_favourites_choice': dialogs.clear_favourites_choice()
	elif 'trakt.' in mode:
		if '.list' in mode:
			from indexers import trakt_lists
			exec('trakt_lists.%s(params)' % mode.split('.')[2])
		else:
			from apis import trakt_api
			exec('trakt_api.%s(params)' % mode.split('.')[1])
	elif 'build' in mode:
		if mode == 'build_movie_list':
			from indexers.movies import Movies
			Movies(params).fetch_list()
		elif mode == 'build_tvshow_list':
			from indexers.tvshows import TVShows
			TVShows(params).fetch_list()
		elif mode == 'build_season_list':
			from indexers.seasons import build_season_list
			build_season_list(params)
		elif mode == 'build_episode_list':
			from indexers.episodes import build_episode_list
			build_episode_list(params)
		elif mode == 'build_in_progress_episode':
			from indexers.episodes import build_single_episode
			build_single_episode('episode.progress')
		elif mode == 'build_recently_watched_episode':
			from indexers.episodes import build_single_episode
			build_single_episode('episode.recently_watched')
		elif mode == 'build_next_episode':
			from indexers.episodes import build_single_episode
			build_single_episode('episode.next')
		elif mode == 'build_my_calendar':
			from indexers.episodes import build_single_episode
			build_single_episode('episode.trakt', params)
		elif mode == 'build_next_episode_manager':
			from modules.episode_tools import build_next_episode_manager
			build_next_episode_manager()
		elif mode == 'imdb_build_user_lists':
			from indexers.imdb import imdb_build_user_lists
			imdb_build_user_lists(_get('media_type'))
		elif mode == 'build_popular_people':
			from indexers.people import popular_people
			popular_people()
		elif mode == 'imdb_build_keyword_results':
			from indexers.imdb import imdb_build_keyword_results
			imdb_build_keyword_results(_get('media_type'), _get('query'))
	elif 'watched_unwatched' in mode:
		if mode == 'mark_as_watched_unwatched_episode':
			from modules.watched_status import mark_as_watched_unwatched_episode
			mark_as_watched_unwatched_episode(params)
		elif mode == 'mark_as_watched_unwatched_season':
			from modules.watched_status import mark_as_watched_unwatched_season
			mark_as_watched_unwatched_season(params)
		elif mode == 'mark_as_watched_unwatched_tvshow':
			from modules.watched_status import mark_as_watched_unwatched_tvshow
			mark_as_watched_unwatched_tvshow(params)
		elif mode == 'mark_as_watched_unwatched_movie':
			from modules.watched_status import mark_as_watched_unwatched_movie
			mark_as_watched_unwatched_movie(params)
		elif mode == 'watched_unwatched_erase_bookmark':
			from modules.watched_status import erase_bookmark
			erase_bookmark(_get('media_type'), _get('tmdb_id'), _get('season', ''), _get('episode', ''), _get('refresh', 'false'))
	elif 'history' in mode:
		if mode == 'search_history':
			from indexers.history import search_history
			search_history(params)
		elif mode == 'clear_search_history':
			from modules.history import clear_search_history
			clear_search_history()
		elif mode == 'remove_from_history':
			from modules.history import remove_from_search_history
			remove_from_search_history(params)
		elif mode == 'clear_all_history':
			from modules.history import clear_all_history
			clear_all_history(_get('setting_id'), _get('refresh', 'false'))
	elif 'real_debrid' in mode:
		if mode == 'real_debrid.rd_torrent_cloud':
			from indexers.real_debrid import rd_torrent_cloud
			rd_torrent_cloud()
		if mode == 'real_debrid.rd_downloads':
			from indexers.real_debrid import rd_downloads
			rd_downloads()
		elif mode == 'real_debrid.browse_rd_cloud':
			from indexers.real_debrid import browse_rd_cloud
			browse_rd_cloud(_get('id'))
		elif mode == 'real_debrid.resolve_rd':
			from indexers.real_debrid import resolve_rd
			resolve_rd(params)
		elif mode == 'real_debrid.rd_account_info':
			from indexers.real_debrid import rd_account_info
			rd_account_info()
		elif mode == 'real_debrid.delete':
			from indexers.real_debrid import rd_delete
			rd_delete(_get('id'), _get('cache_type'))
		elif mode == 'real_debrid.authenticate':
			from apis.real_debrid_api import RealDebridAPI
			RealDebridAPI().auth()
		elif mode == 'real_debrid.revoke_authentication':
			from apis.real_debrid_api import RealDebridAPI
			RealDebridAPI().revoke()
	elif 'premiumize' in mode:
		if mode == 'premiumize.pm_torrent_cloud':
			from indexers.premiumize import pm_torrent_cloud
			pm_torrent_cloud(_get('id', None), _get('folder_name', None))
		elif mode == 'premiumize.pm_transfers':
			from indexers.premiumize import pm_transfers
			pm_transfers()
		elif mode == 'premiumize.pm_account_info':
			from indexers.premiumize import pm_account_info
			pm_account_info()
		elif mode == 'premiumize.rename':
			from indexers.premiumize import pm_rename
			pm_rename(_get('file_type'), _get('id'), _get('name'))
		elif mode == 'premiumize.delete':
			from indexers.premiumize import pm_delete
			pm_delete(_get('file_type'), _get('id'))
		elif mode == 'premiumize.authenticate':
			from apis.premiumize_api import PremiumizeAPI
			PremiumizeAPI().auth()
		elif mode == 'premiumize.revoke_authentication':
			from apis.premiumize_api import PremiumizeAPI
			PremiumizeAPI().revoke()
	elif 'alldebrid' in mode:
		if mode == 'alldebrid.ad_torrent_cloud':
			from indexers.alldebrid import ad_torrent_cloud
			ad_torrent_cloud(_get('id', None))
		elif mode == 'alldebrid.browse_ad_cloud':
			from indexers.alldebrid import browse_ad_cloud
			browse_ad_cloud(_get('folder'))
		elif mode == 'alldebrid.resolve_ad':
			from indexers.alldebrid import resolve_ad
			resolve_ad(params)
		elif mode == 'alldebrid.ad_account_info':
			from indexers.alldebrid import ad_account_info
			ad_account_info()
		elif mode == 'alldebrid.authenticate':
			from apis.alldebrid_api import AllDebridAPI
			AllDebridAPI().auth()
		elif mode == 'alldebrid.revoke_authentication':
			from apis.alldebrid_api import AllDebridAPI
			AllDebridAPI().revoke()
	elif '_settings' in mode:
		if mode == 'open_settings':
			from modules.kodi_utils import open_settings
			open_settings(_get('query', '0.0'), _get('addon', 'plugin.video.fen'))
		elif mode == 'clean_settings':
			from modules.kodi_utils import clean_settings
			clean_settings()
		elif mode == 'clear_settings_window_properties':
			from modules.kodi_utils import clear_settings_window_properties
			clear_settings_window_properties()
	elif '_cache' in mode:
		import caches
		if mode == 'clear_cache':
			caches.clear_cache(_get('cache'))
		elif mode == 'clear_all_cache':
			caches.clear_all_cache()
		elif mode == 'clean_databases_cache':
			caches.clean_databases()
		elif mode == 'check_corrupt_databases_cache':
			caches.check_corrupt_databases()
	elif '_image' in mode:
		from indexers.images import Images
		Images().run(params)
	elif '_text' in mode:
		if mode == 'show_text':
			from modules.kodi_utils import show_text
			show_text(_get('heading'), _get('text', None), _get('file', None), _get('font_size', 'small'), _get('kodi_log', 'false') == 'true')
		elif mode == 'show_text_media':
			from modules.kodi_utils import show_text_media
			show_text(_get('heading'), _get('text', None), _get('file', None), _get('meta'), {})
	elif '_view' in mode:
		from modules import kodi_utils
		if mode == 'choose_view':
			kodi_utils.choose_view(_get('view_type'), _get('content', ''))
		elif mode == 'set_view':
			kodi_utils.set_view(_get('view_type'))
	##EXTRA modes##
	elif mode == 'kodi_refresh':
		from modules.kodi_utils import kodi_refresh
		kodi_refresh()
	elif mode == 'get_search_term':
		from modules.history import get_search_term
		get_search_term(params)
	elif mode == 'person_data_dialog':
		from indexers.people import person_data_dialog
		person_data_dialog(params)
	elif mode == 'downloader':
		from modules.downloader import runner
		runner(params)
	elif mode == 'download_manager':
		from modules.downloader import download_manager
		download_manager(params)
	elif mode == 'manual_add_magnet_to_cloud':
		from modules.debrid import manual_add_magnet_to_cloud
		manual_add_magnet_to_cloud(params)
	elif mode == 'debrid.browse_packs':
		from modules.sources import Sources
		Sources().debridPacks(_get('provider'), _get('name'), _get('magnet_url'), _get('info_hash'))
	elif mode == 'upload_logfile':
		from modules.kodi_utils import upload_logfile
		upload_logfile()
	elif mode == 'toggle_language_invoker':
		from modules.kodi_utils import toggle_language_invoker
		toggle_language_invoker()
