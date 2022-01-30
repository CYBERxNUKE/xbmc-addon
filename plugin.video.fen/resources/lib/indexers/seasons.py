# -*- coding: utf-8 -*-
from sys import argv
import metadata
from modules import kodi_utils
from modules.utils import adjust_premiered_date, get_datetime
from modules.watched_status import get_watched_info_tv, get_watched_status_season
from modules import settings
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
poster_empty = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/box_office.png')
fanart_empty = kodi_utils.translate_path('special://home/addons/plugin.video.fen/fanart.png')
season_str, watched_str, unwatched_str, extras_str, options_str = ls(32537), ls(32642), ls(32643), ls(32645), ls(32646)
run_plugin, unaired_label = 'RunPlugin(%s)', '[COLOR red][I]%s[/I][/COLOR]'
string = str

def build_season_list(params):
	def _process():
		running_ep_count = total_aired_eps
		def _unaired_status():
			if episode_count == 0: return True
			season_date_start = adjust_premiered_date(air_date, 0)[0]
			if not season_date_start or current_date < season_date_start: return True
			return False
		for item in season_data:
			try:
				listitem = make_listitem()
				set_property = listitem.setProperty
				cm = []
				cm_append = cm.append
				item_get = item.get
				overview = item_get('overview')
				name = item_get('name')
				poster_path = item_get('poster_path')
				air_date = item_get('air_date')
				season_number = item_get('season_number')
				episode_count = item_get('episode_count')
				season_poster = 'https://image.tmdb.org/t/p/%s%s' % (image_resolution, poster_path) if poster_path is not None else show_poster
				if season_number == 0: unaired = False
				else:
					unaired = _unaired_status()
					if unaired:
						if not show_unaired: return
						episode_count = 0
					else:
						running_ep_count -= episode_count
						if running_ep_count < 0: episode_count = running_ep_count + episode_count
				try: year = air_date.split('-')[0]
				except: year = show_year
				plot = overview if overview != '' else show_plot
				title = name if use_season_title and name != '' else '%s %s' % (season_str, string(season_number))
				if unaired: title = unaired_label % title
				playcount, overlay, watched, unwatched = get_watched_status_season(watched_info, string(tmdb_id), season_number, episode_count)
				url_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': season_number})
				extras_params = build_url({'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'db_type': 'tvshow', 'is_widget': is_widget})
				options_params = build_url({'mode': 'options_menu_choice', 'content': 'season', 'tmdb_id': tmdb_id})
				cm_append((extras_str, run_plugin % extras_params))
				cm_append((options_str, run_plugin % options_params))
				if not playcount:
					watched_params = build_url({'mode': 'mark_as_watched_unwatched_season', 'action': 'mark_as_watched', 'title': show_title, 'year': show_year,
														  'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season_number})
					cm_append((watched_str % watched_title, run_plugin % watched_params))
				if watched:
					unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_season', 'action': 'mark_as_unwatched', 'title': show_title, 'year': show_year,
															'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season_number})
					cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
				listitem.setLabel(title)
				listitem.setContentLookup(False)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'poster': season_poster, 'icon': season_poster, 'thumb': season_poster, 'fanart': fanart, 'banner': banner, 'clearart': clearart,
								'clearlogo': clearlogo, 'landscape': landscape, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape,
								'tvshow.banner': banner})
				listitem.setCast(cast)
				listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				listitem.setInfo('video', {'mediatype': 'season', 'trailer': trailer, 'title': title, 'size': '0', 'duration': episode_run_time, 'plot': plot, 'rating': rating,
								'premiered': premiered, 'studio': studio, 'year': year,'genre': genre, 'mpaa': mpaa, 'tvshowtitle': show_title, 'imdbnumber': imdb_id,
								'votes': votes, 'season': season_number,'playcount': playcount, 'overlay': overlay})
				set_property('watchedepisodes', string(watched))
				set_property('unwatchedepisodes', string(unwatched))
				set_property('totalepisodes', string(episode_count))
				if is_widget:
					set_property('fen_widget', 'true')
					set_property('fen_playcount', string(playcount))
					set_property('fen_extras_menu_params', extras_params)
					set_property('fen_options_menu_params', options_params)
				else: set_property('fen_widget', 'false')
				yield (url_params, listitem, True)
			except: pass
	__handle__ = int(argv[1])
	meta_user_info = metadata.retrieve_user_info()
	watched_indicators = settings.watched_indicators()
	watched_info = get_watched_info_tv(watched_indicators)
	show_unaired = settings.show_unaired()
	is_widget = kodi_utils.external_browse()
	current_date = get_datetime()
	image_resolution = meta_user_info['image_resolution']['poster']
	poster_main, poster_backup, fanart_main, fanart_backup = settings.get_art_provider()
	meta = metadata.tvshow_meta('tmdb_id', params['tmdb_id'], meta_user_info)
	meta_get = meta.get
	season_data = meta_get('season_data')
	if not season_data: return
	tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
	show_title, show_year, show_plot, banner = meta_get('title'), meta_get('year'), meta_get('plot'), meta_get('banner')
	show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
	fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
	clearlogo, clearart, landscape = meta_get('clearlogo'), meta_get('clearart'), meta_get('landscape')
	cast, mpaa, votes = meta_get('cast'), meta_get('mpaa'), meta_get('votes')
	trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
	episode_run_time, rating, premiered = meta_get('episode_run_time'), meta_get('rating'), meta_get('premiered')
	total_seasons = meta_get('total_seasons')
	total_aired_eps = meta_get('total_aired_eps')
	if not settings.show_specials(): season_data = [i for i in season_data if not i['season_number'] == 0]
	season_data.sort(key=lambda k: k['season_number'])
	use_season_title = settings.use_season_title()
	watched_title = 'Trakt' if watched_indicators == 1 else 'Fen'
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_content(__handle__, 'seasons')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.seasons', 'seasons')
