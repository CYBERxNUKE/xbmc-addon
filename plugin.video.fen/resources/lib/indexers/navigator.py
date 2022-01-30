# -*- coding: utf-8 -*-
import os
import time
import json
from sys import argv
import sqlite3 as database
from urllib.parse import urlencode
from indexers.default_menus import DefaultMenus
from modules import kodi_utils
from modules.utils import to_utf8
from modules.settings_reader import get_setting, set_setting
from modules import settings as sett
# from modules.kodi_utils import logger

tp = kodi_utils.translate_path
ls = kodi_utils.local_string

NAVIGATOR_DB = tp('special://profile/addon_data/plugin.video.fen/navigator.db')
icon_directory = tp('special://home/addons/script.tikiart/resources/media')
fanart = tp('special://home/addons/plugin.video.fen/fanart.png')
non_folder_items = ('get_search_term', 'build_popular_people')

_in_str, mov_str, tv_str = ls(32484), ls(32028), ls(32029)

class Navigator:
	def __init__(self, params):
		self.view = 'view.main'
		self.params = params
		self.params_get = self.params.get
		self.list_name = self.params_get('action', 'RootList')

	def main(self):
		self.build_main_lists()

	def downloads(self):
		dl_str, pr_str, im_str = ls(32107), ls(32485), ls(32798)
		n_ins, lst_ins = _in_str % (dl_str.upper(), '%s'), '%s %s' % ('%s', dl_str)
		mov_path, ep_path = sett.download_directory('movie'), sett.download_directory('episode')
		prem_path, im_path = sett.download_directory('premium'), sett.download_directory('image')
		self.AD({'mode': 'navigator.folder_navigator', 'folder_path': mov_path, 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'movies.png')
		self.AD({'mode': 'navigator.folder_navigator', 'folder_path': ep_path, 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'tv.png')
		self.AD({'mode': 'navigator.folder_navigator', 'folder_path': prem_path, 'list_name': lst_ins % pr_str}, n_ins % pr_str, 'premium.png')
		self.AD({'mode': 'browser_image', 'folder_path': im_path, 'list_name': lst_ins % im_str}, n_ins % im_str, 'people.png', False)
		self._end_directory()

	def discover_main(self):
		discover_str, his_str, help_str = ls(32451), ls(32486), ls(32487)
		movh_str, tvh_str = '%s %s' % (mov_str, his_str), '%s %s' % (tv_str, his_str)
		n_ins, lst_ins = _in_str % (discover_str.upper(), '%s'), '%s %s' % (discover_str, '%s')
		self.AD({'mode': 'discover.movie', 'db_type': 'movie', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'discover.png')
		self.AD({'mode': 'discover.tvshow', 'db_type': 'tvshow', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'discover.png')
		self.AD({'mode': 'discover.history', 'db_type': 'movie', 'list_name': lst_ins % movh_str}, n_ins % movh_str, 'discover.png')
		self.AD({'mode': 'discover.history', 'db_type': 'tvshow', 'list_name': lst_ins % tvh_str}, n_ins % tvh_str, 'discover.png')
		self.AD({'mode': 'discover.help', 'list_name': lst_ins % help_str}, n_ins % help_str, 'discover.png', False)
		self._end_directory()

	def premium(self):
		from modules.debrid import debrid_enabled
		n_ins = _in_str % (ls(32488).upper(), '%s')
		furk_str, easy_str, rd_str, pm_str, ad_str = ls(32069), ls(32070), ls(32054), ls(32061), ls(32063)
		furk, easynews = sett.furk_active(), sett.easynews_active()
		debrids = debrid_enabled()
		if furk: self.AD({'mode': 'navigator.furk', 'list_name': furk_str}, n_ins % furk_str, 'furk.png')
		if easynews: self.AD({'mode': 'navigator.easynews', 'list_name': easy_str}, n_ins % easy_str, 'easynews.png')
		if 'Real-Debrid' in debrids: self.AD({'mode': 'navigator.real_debrid', 'list_name': rd_str}, n_ins % rd_str, 'realdebrid.png')
		if 'Premiumize.me' in debrids: self.AD({'mode': 'navigator.premiumize', 'list_name': pm_str}, n_ins % pm_str, 'premiumize.png')
		if 'AllDebrid' in debrids: self.AD({'mode': 'navigator.alldebrid', 'list_name': ad_str}, n_ins % ad_str, 'alldebrid.png')
		self._end_directory()

	def furk(self):
		f_str, act_str, fl_str, vid_str = ls(32069), ls(32489), ls(32490), ls(32491)
		aud_str, fl_str, dl_str = ls(32492), ls(32493), ls(32107)
		se_str, his_str, acc_str = ls(32450), ls(32486), ls(32494)
		hvid_str, ha_str = '%s %s' % (his_str, vid_str), '%s %s' % (his_str, aud_str)
		n_ins, lst_ins = _in_str % (f_str.upper(), '%s %s'), (_in_str % (f_str, '%s %s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'furk.search_furk', 'db_type': 'video', 'list_name': lst_ins % (se_str, vid_str)}, n_ins % (se_str, vid_str), 'search.png')
		self.AD({'mode': 'furk.search_furk', 'db_type': 'audio', 'list_name': lst_ins % (se_str, aud_str)}, n_ins % (se_str, aud_str), 'search.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_video', 'list_name': lst_ins % (vid_str, fl_str)}, n_ins % (vid_str, fl_str), 'lists.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_audio', 'list_name': lst_ins % (aud_str, fl_str)}, n_ins % (aud_str, fl_str), 'lists.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_active', 'list_name': lst_ins % (act_str, dl_str)}, n_ins % (act_str, dl_str), 'lists.png')
		self.AD({'mode': 'furk.my_furk_files', 'list_type': 'file_get_failed', 'list_name': lst_ins % (fl_str, dl_str)}, n_ins % (fl_str, dl_str), 'lists.png')
		self.AD({'mode': 'search_history', 'action': 'furk_video', 'list_name': lst_ins % (se_str, hvid_str)}, n_ins % (se_str, hvid_str), 'search.png')
		self.AD({'mode': 'search_history', 'action': 'furk_audio', 'list_name': lst_ins % (se_str, ha_str)}, n_ins % (se_str, ha_str), 'search.png')
		self.AD({'mode': 'furk.account_info', 'list_name': lst_ins % (acc_str, '')}, n_ins % (acc_str, ''), 'furk.png', False)
		self._end_directory()

	def easynews(self):
		easy_str, se_str, his_str, acc_str = ls(32070), ls(32450), ls(32486), ls(32494)
		shis_str, n_ins = '%s %s' % (se_str, his_str), _in_str % (easy_str.upper(), '%s')
		lst_ins = (_in_str % (easy_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'easynews.search_easynews', 'list_name': lst_ins % se_str}, n_ins % se_str, 'search.png')
		self.AD({'mode': 'search_history', 'action': 'easynews_video', 'list_name': lst_ins % shis_str}, n_ins % shis_str, 'search.png')
		self.AD({'mode': 'easynews.account_info', 'list_name': lst_ins % acc_str}, n_ins % acc_str, 'easynews.png', False)
		self._end_directory()

	def real_debrid(self):
		rd_str, acc_str, his_str, cloud_str = ls(32054), ls(32494), ls(32486), ls(32496)
		clca_str, n_ins, lst_ins = ls(32497) % rd_str, _in_str % (rd_str.upper(), '%s'), (_in_str % (rd_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'real_debrid.rd_torrent_cloud', 'list_name': lst_ins % cloud_str}, n_ins % cloud_str, 'realdebrid.png')
		self.AD({'mode': 'real_debrid.rd_downloads', 'list_name': lst_ins % his_str}, n_ins % his_str, 'realdebrid.png')
		self.AD({'mode': 'real_debrid.rd_account_info', 'list_name': lst_ins % acc_str}, n_ins % acc_str, 'realdebrid.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'rd_cloud', 'list_name': lst_ins % clca_str}, n_ins % clca_str, 'realdebrid.png', False)
		self._end_directory()

	def premiumize(self):
		pm_str, acc_str, his_str, cloud_str = ls(32061), ls(32494), ls(32486), ls(32496)
		clca_str, n_ins, lst_ins = ls(32497) % pm_str, _in_str % (pm_str.upper(), '%s'), (_in_str % (pm_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'premiumize.pm_torrent_cloud', 'list_name': lst_ins % cloud_str}, n_ins % cloud_str, 'premiumize.png')
		self.AD({'mode': 'premiumize.pm_transfers', 'list_name': lst_ins % his_str}, n_ins % his_str, 'premiumize.png')
		self.AD({'mode': 'premiumize.pm_account_info', 'list_name': lst_ins % acc_str}, n_ins % acc_str, 'premiumize.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'pm_cloud', 'list_name': lst_ins % clca_str}, n_ins % clca_str, 'premiumize.png', False)
		self._end_directory()

	def alldebrid(self):
		ad_str, acc_str, cloud_str = ls(32063), ls(32494), ls(32496)
		clca_str, n_ins, lst_ins = ls(32497) % ad_str, _in_str % (ad_str.upper(), '%s'), (_in_str % (ad_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'alldebrid.ad_torrent_cloud', 'list_name': lst_ins % cloud_str}, n_ins % cloud_str, 'alldebrid.png')
		self.AD({'mode': 'alldebrid.ad_account_info', 'list_name': lst_ins % acc_str}, n_ins % acc_str, 'alldebrid.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'ad_cloud', 'list_name': lst_ins % clca_str}, n_ins % clca_str, 'alldebrid.png', False)
		self._end_directory()

	def favourites(self):
		fav_str = ls(32453)
		n_ins, lst_ins = _in_str % (fav_str.upper(), '%s'), (_in_str % ('%s', fav_str)).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'build_movie_list', 'action': 'favourites_movies', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'movies.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'favourites_tvshows', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'tv.png')
		self._end_directory()

	def my_content(self):
		trakt_str, imdb_str, coll_str, wlist_str, ls_str = ls(32037), ls(32064), ls(32499), ls(32500), ls(32501)
		t_n_ins, t_lst_ins = _in_str % (trakt_str.upper(), '%s'), (_in_str % (trakt_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		i_n_ins, i_lst_ins = _in_str % (imdb_str.upper(), '%s'), (_in_str % (imdb_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		trakt_status = get_setting('trakt_user') not in ('', None)
		imdb_status = get_setting('imdb_user') not in ('', None)
		if trakt_status or imdb_status:
			if trakt_status:
				self.AD({'mode': 'navigator.trakt_collections', 'list_name': t_lst_ins % coll_str}, t_n_ins % coll_str, 'trakt.png')
				self.AD({'mode': 'navigator.trakt_watchlists', 'list_name': t_lst_ins % wlist_str}, t_n_ins % wlist_str, 'trakt.png')
				self.AD({'mode': 'navigator.trakt_lists', 'list_name': t_lst_ins % ls_str}, t_n_ins % ls_str, 'trakt.png')
			if imdb_status:
				self.AD({'mode': 'navigator.imdb_watchlists', 'list_name': i_lst_ins % wlist_str}, i_n_ins % wlist_str, 'imdb.png')
				self.AD({'mode': 'navigator.imdb_lists', 'list_name': i_lst_ins % ls_str}, i_n_ins % ls_str, 'imdb.png')
			self._end_directory()
		else:
			kodi_utils.notification(33022)

	def trakt_collections(self):
		# use 'new_page' to pass the type of list to be processed when using 'trakt_collection_lists'...
		t_str, col_str = ls(32037), ls(32499)
		tcol_str = '%s %s' % (t_str, col_str)
		n_ins, lst_ins = _in_str % (tcol_str.upper(), '%s'), (_in_str % (tcol_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		mrec_str, mran_str = '%s %s' % (ls(32498), mov_str), '%s %s' % (ls(32504), mov_str)
		tvrec_str, tvran_str, ra_str = '%s %s' % (ls(32498), tv_str), '%s %s' % (ls(32504), tv_str), '%s %s' % (ls(32505), ls(32506))
		n_ins, lst_ins = _in_str % (col_str.upper(), '%s'), (_in_str % (col_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_collection', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_collection', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'trakt.png')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_collection_lists', 'new_page': 'recent', 'list_name': lst_ins % mrec_str}, n_ins % mrec_str, 'trakt.png')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_collection_lists', 'new_page': 'random', 'list_name': lst_ins % mran_str}, n_ins % mran_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_collection_lists', 'new_page': 'recent', 'list_name': lst_ins % tvrec_str}, n_ins % tvrec_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_collection_lists', 'new_page': 'random', 'list_name': lst_ins % tvran_str}, n_ins % tvran_str, 'trakt.png')
		self.AD({'mode': 'get_trakt_my_calendar', 'recently_aired': 'true', 'list_name': lst_ins % ra_str}, n_ins % ra_str, 'trakt.png')
		self._end_directory()

	def trakt_watchlists(self):
		t_str, watchlist_str = ls(32037), ls(32500)
		trakt_watchlist_str = '%s %s' % (t_str, watchlist_str)
		n_ins, lst_ins = _in_str % (trakt_watchlist_str.upper(), '%s'), (_in_str % (trakt_watchlist_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_watchlist', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_watchlist', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'trakt.png')
		self._end_directory()

	def trakt_lists(self):
		t_str, user_str, l_str, ml_str, ll_str, rec_str, cal_str = ls(32037), ls(32065), ls(32501), ls(32454), ls(32502), ls(32503), ls(32081)
		tu_str, pu_str = '%s %s %s' % (ls(32458), user_str, l_str), '%s %s %s' % (ls(32459), user_str, l_str)
		sea_str, n_ins, lst_ins = '%s %s' % (ls(32477), l_str), _in_str % (t_str.upper(), '%s'), (_in_str % (t_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'trakt.list.get_trakt_lists', 'list_type': 'my_lists', 'build_list': 'true', 'list_name': lst_ins % ml_str}, n_ins % ml_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.get_trakt_lists', 'list_type': 'liked_lists', 'build_list': 'true', 'list_name': lst_ins % ll_str}, n_ins % ll_str, 'trakt.png')
		self.AD({'mode': 'navigator.trakt_recommendations', 'list_name': lst_ins % rec_str}, n_ins % rec_str, 'trakt.png')
		self.AD({'mode': 'get_trakt_my_calendar', 'list_name': lst_ins % cal_str}, n_ins % cal_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.get_trakt_trending_popular_lists', 'list_type': 'trending', 'list_name': lst_ins % tu_str}, n_ins % tu_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.get_trakt_trending_popular_lists', 'list_type': 'popular', 'list_name': lst_ins % pu_str}, n_ins % pu_str, 'trakt.png')
		self.AD({'mode': 'trakt.list.search_trakt_lists', 'list_name': lst_ins % sea_str}, n_ins % sea_str, 'trakt.png')
		self._end_directory()

	def trakt_recommendations(self):
		rec_str = ls(32503)
		n_ins, lst_ins = _in_str % (rec_str.upper(), '%s'), (_in_str % (rec_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'build_movie_list', 'action': 'trakt_recommendations', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'trakt.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'trakt_recommendations', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'trakt.png')
		self._end_directory()

	def imdb_watchlists(self):
		imdb_str, watchlist_str = ls(32064), ls(32500)
		imdb_watchlist_str = '%s %s' % (imdb_str, watchlist_str)
		n_ins, lst_ins = _in_str % (imdb_watchlist_str.upper(), '%s'), (_in_str % (imdb_watchlist_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'build_movie_list', 'action': 'imdb_watchlist', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'imdb.png')
		self.AD({'mode': 'build_tvshow_list', 'action': 'imdb_watchlist', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'imdb.png')
		self._end_directory()

	def imdb_lists(self):
		imdb_str, lists_str = ls(32064), ls(32501)
		imdb_lists_str = '%s %s' % (imdb_str, lists_str)
		n_ins, lst_ins = _in_str % (imdb_lists_str.upper(), '%s'), (_in_str % (imdb_lists_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'imdb_build_user_lists', 'db_type': 'movie', 'list_name': lst_ins % mov_str}, n_ins % mov_str, 'imdb.png')
		self.AD({'mode': 'imdb_build_user_lists', 'db_type': 'tvshow', 'list_name': lst_ins % tv_str}, n_ins % tv_str, 'imdb.png')
		self._end_directory()

	def search(self):
		search_str, people_str, history_str, imdb_keyword_str = ls(32450), ls(32507), ls(32486), '%s %s' % (ls(32064), ls(32092))
		kw_mov, kw_tv = '%s %s (%s)' % (ls(32064), ls(32092), mov_str), '%s %s (%s)' % (ls(32064), ls(32092), tv_str)
		n_ins_search = _in_str % (search_str.upper(), '%s')
		lst_ins_search = (_in_str % (search_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		n_ins_history = _in_str % ('%s %s' % (search_str.upper(), history_str.upper()), '%s')
		lst_ins_history = (_in_str % ('%s %s' % (search_str, history_str.capitalize()), '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'get_search_term', 'db_type': 'movie', 'list_name': lst_ins_search % mov_str}, n_ins_search % mov_str, 'search_movie.png', False)
		self.AD({'mode': 'get_search_term', 'db_type': 'tv_show', 'list_name': lst_ins_search % tv_str}, n_ins_search % tv_str, 'search_tv.png', False)
		self.AD({'mode': 'people_search.search', 'list_name': lst_ins_search % people_str}, n_ins_search % people_str, 'genre_comedy.png', False)
		self.AD({'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'db_type': 'movie', 'list_name': lst_ins_search % kw_mov}, n_ins_search % kw_mov, 'search.png', False)
		self.AD({'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'db_type': 'tvshow', 'list_name': lst_ins_search % kw_tv}, n_ins_search % kw_tv, 'search.png', False)
		self.AD({'mode': 'search_history', 'action': 'movie', 'list_name': lst_ins_history % mov_str}, n_ins_history % mov_str, 'search.png')
		self.AD({'mode': 'search_history', 'action': 'tvshow', 'list_name': lst_ins_history % tv_str}, n_ins_history % tv_str, 'search.png')
		self.AD({'mode': 'search_history', 'action': 'people', 'list_name': lst_ins_history % people_str}, n_ins_history % people_str, 'search.png')
		self.AD({'mode': 'search_history', 'action': 'imdb_keyword_movie', 'list_name': lst_ins_history % kw_mov}, n_ins_history % kw_mov, 'search.png')
		self.AD({'mode': 'search_history', 'action': 'imdb_keyword_tvshow', 'list_name': lst_ins_history % kw_tv}, n_ins_history % kw_tv, 'search.png')
		self._end_directory()

	def tools(self):
		tools_str, manager_str, changelog_str, ext_str, short_str, source_str = ls(32456), ls(32513), ls(32508), ls(32118), ls(32514), ls(32515)
		log_viewer_str, tips_str, views_str = ls(32509), ls(32518), ls(32510)
		clean_str, lang_inv_str = ls(32512), ls(33017)
		changelog_log_viewer_str = '%s & %s' % (changelog_str, log_viewer_str)
		shortcut_manager_str, source_manager_str = '%s %s' % (short_str, manager_str), '%s %s' % (source_str, manager_str)
		n_ins, lst_ins = _in_str % (tools_str.upper(), '%s'), (_in_str % (tools_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'navigator.changelogs', 'list_name': lst_ins % changelog_log_viewer_str}, n_ins % changelog_log_viewer_str, 'settings2.png')
		self.AD({'mode': 'navigator.tips', 'list_name': lst_ins % tips_str}, n_ins % tips_str, 'settings2.png')
		self.AD({'mode': 'navigator.set_view_modes', 'list_name': lst_ins % views_str}, n_ins % views_str, 'settings2.png')
		self.AD({'mode': 'navigator.clear_info', 'list_name': lst_ins % clean_str}, n_ins % clean_str, 'settings2.png')
		self.AD({'mode': 'navigator.shortcut_folders', 'list_name': lst_ins % shortcut_manager_str}, n_ins % shortcut_manager_str, 'settings2.png')
		self.AD({'mode': 'navigator.sources_folders', 'list_name': lst_ins % source_manager_str}, n_ins % source_manager_str, 'settings2.png')
		self.AD({'mode': 'toggle_language_invoker', 'list_name': lst_ins % lang_inv_str}, n_ins % lang_inv_str, 'settings2.png', False)
		self._end_directory()

	def settings(self):
		settings_str = ls(32247)
		fen_str, fenom_scr_str, myaccounts_str = ls(32036), ls(32522), ls(33025)
		n_ins, lst_ins = _in_str % (settings_str.upper(), '%s'), (_in_str % (settings_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		self.AD({'mode': 'open_settings', 'query': '0.0', 'list_name': lst_ins % fen_str}, n_ins % fen_str, 'settings.png', False)
		self.AD({'mode': 'external_settings', 'ext_addon': 'script.module.fenomscrapers', 'list_name': lst_ins % fenom_scr_str}, n_ins % fenom_scr_str, 'settings.png', False)
		self.AD({'mode': 'external_settings', 'ext_addon': 'script.module.myaccounts', 'list_name': lst_ins % myaccounts_str}, n_ins % myaccounts_str, 'settings.png', False)
		self._end_directory()

	def clear_info(self):
		cache_str, clca_str, clean_str, all_str, settings_str, fav_str = ls(32524), ls(32497), ls(32526), ls(32525), ls(32247), ls(32453)
		clean_set_cache_str = '[B]%s:[/B] %s %s %s' % (clean_str.upper(), clean_str, ls(32247), ls(32524))
		clean_set_cache_str_list_name = '%s %s %s' % (clean_str, ls(32247), ls(32524))
		clean_databases_str = '[B]%s:[/B] %s %s' % (clean_str.upper(), clean_str, ls(32003))
		clean_databases_str_list_name = '%s %s' % (clean_str, ls(32003))
		clean_all_str = '[B]%s:[/B] %s %s %s' % (clean_str.upper(), clean_str, all_str, settings_str)
		clean_all_str_list_name, search_str = '%s %s %s' % (clean_str, all_str, settings_str), '%s %s' % (ls(32450), ls(32486))
		clear_all_str, clear_meta_str = clca_str % all_str, clca_str % ls(32527)
		clear_list_str, clear_trakt_str = clca_str % ls(32501), clca_str % ls(32037)
		clear_imdb_str, clint_str, clext_str = clca_str % ls(32064), clca_str % ls(32096), clca_str % ls(32118)
		clear_rd_str, clear_pm_str, clear_ad_str = clca_str % ls(32054), clca_str % ls(32061), clca_str % ls(32063)
		clear_fav_str, clear_search_str = clca_str % fav_str, clca_str % search_str
		n_ins, lst_ins = _in_str % (cache_str.upper(), '%s'), (_in_str % (cache_str, '%s')).replace('[B]', '').replace(': [/B]', ' ')
		clear_all_amble = '[B][I][COLOR=grey] (%s %s & %s)[/COLOR][/I][/B]' % (ls(32189), fav_str, search_str)
		clear_all = '[B]%s:[/B] %s' % (clear_all_str.upper(), clear_all_amble)
		self.AD({'mode': 'clean_settings', 'list_name': clean_all_str_list_name}, clean_all_str, 'settings2.png', False)
		self.AD({'mode': 'clear_settings_window_properties', 'list_name': clean_set_cache_str_list_name}, clean_set_cache_str, 'settings2.png', False)
		self.AD({'mode': 'clean_databases', 'list_name': clean_databases_str_list_name}, clean_databases_str, 'settings2.png', False)
		self.AD({'mode': 'clear_all_cache', 'list_name': clear_all_str}, clear_all, 'settings2.png', False)
		self.AD({'mode': 'clear_favourites', 'list_name': lst_ins % clear_fav_str}, n_ins % clear_fav_str, 'settings2.png', False)
		self.AD({'mode': 'clear_search_history', 'list_name': lst_ins % clear_search_str}, n_ins % clear_search_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'meta', 'list_name': lst_ins % clear_meta_str}, n_ins % clear_meta_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'list', 'list_name': lst_ins % clear_list_str}, n_ins % clear_list_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'trakt', 'list_name': lst_ins % clear_trakt_str}, n_ins % clear_trakt_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'imdb', 'list_name': lst_ins % clear_imdb_str}, n_ins % clear_imdb_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'internal_scrapers', 'list_name': lst_ins % clint_str}, n_ins % clint_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'external_scrapers', 'list_name': lst_ins % clint_str}, n_ins % clext_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'rd_cloud', 'list_name': lst_ins % clear_rd_str}, n_ins % clear_rd_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'pm_cloud', 'list_name': lst_ins % clear_pm_str}, n_ins % clear_pm_str, 'settings2.png', False)
		self.AD({'mode': 'clear_cache', 'cache': 'ad_cloud', 'list_name': lst_ins % clear_ad_str}, n_ins % clear_ad_str, 'settings2.png', False)
		self._end_directory()

	def set_view_modes(self):
		set_views_str, lists_str, root_str, movies_str = ls(32510), ls(32501), ls(32457), ls(32028)
		tvshows_str, season_str, episode_str, premium_files_str = ls(32029), ls(32537), ls(32506), ls(32485)
		ep_lists_str, trakt_lists_str = '%s %s' % (episode_str, lists_str), '%s %s' % (ls(32037), lists_str)
		n_ins = _in_str % (set_views_str.upper(), '%s')
		self.AD({'mode': 'choose_view', 'view_type': 'view.main', 'content': '', 'exclude_external': 'true'},n_ins % root_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.movies', 'content': 'movies', 'exclude_external': 'true'},n_ins % movies_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.tvshows', 'content': 'tvshows', 'exclude_external': 'true'},n_ins % tvshows_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.seasons', 'content': 'seasons', 'exclude_external': 'true'},n_ins % season_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.episodes', 'content': 'episodes', 'exclude_external': 'true'},n_ins % episode_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.episode_lists', 'content': 'episodes','exclude_external': 'true'},n_ins % ep_lists_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.trakt_list', 'content': 'movies', 'exclude_external': 'true'},n_ins % trakt_lists_str, 'settings.png')
		self.AD({'mode': 'choose_view', 'view_type': 'view.premium', 'content': 'files', 'exclude_external': 'true'},n_ins % premium_files_str, 'settings.png')
		self._end_directory()

	def changelogs(self):
		fen_str, cl_str, fs_str, ma_str, lv_str, k_str = ls(32036), ls(32508), ls(32522), ls(33025), ls(32509), ls(32538)
		fen_vstr, fen_ic = kodi_utils.addon().getAddonInfo('version'), kodi_utils.addon().getAddonInfo('icon')
		sc_v, sc_ic = kodi_utils.ext_addon('script.module.fenomscrapers').getAddonInfo('version'), kodi_utils.ext_addon('script.module.fenomscrapers').getAddonInfo('icon')
		ma_v, ma_ic = kodi_utils.ext_addon('script.module.myaccounts').getAddonInfo('version'), kodi_utils.ext_addon('script.module.myaccounts').getAddonInfo('icon')
		mt_str, mh_str = tp('special://home/addons/plugin.video.fen/resources/text/changelog.txt'), '%s :  %s  [I](v.%s)[/I]' % (cl_str.upper(), fen_str, fen_vstr)
		sct_str = tp(os.path.join(tp(kodi_utils.ext_addon('script.module.fenomscrapers').getAddonInfo('path')), 'changelog.txt'))
		sch_str = '%s :  %s  [I](v.%s)[/I]' % (cl_str.upper(), fs_str, sc_v)
		mat_str = tp(os.path.join(tp(kodi_utils.ext_addon('script.module.myaccounts').getAddonInfo('path')), 'changelog.txt'))
		mah_str = '%s :  %s  [I](v.%s)[/I]' % (cl_str.upper(), ma_str, ma_v)
		kl_loc, kl_h = os.path.join(tp('special://logpath/'), 'kodi.log'), '%s : %s %s' % (lv_str.upper(), k_str, lv_str)
		self.AD({'mode': 'show_text', 'heading': mh_str, 'file': mt_str, 'exclude_external': 'true'}, mh_str, fen_ic, False)
		self.AD({'mode': 'show_text', 'heading': sch_str, 'file': sct_str, 'exclude_external': 'true'}, sch_str, sc_ic, False)
		self.AD({'mode': 'show_text', 'heading': mah_str, 'file': mat_str, 'exclude_external': 'true'}, mah_str, ma_ic, False)
		self.AD({'mode': 'show_text', 'heading': kl_h, 'file': kl_loc, 'exclude_external': 'true'}, kl_h, 'lists.png', False)
		self._end_directory()

	def certifications(self):
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie': from modules.meta_lists import movie_certifications as certifications
		else: from modules.meta_lists import tvshow_certifications as certifications
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_certifications' if menu_type == 'movie' else 'trakt_tv_certifications'
		lst_ins = self.make_list_name(menu_type)
		for cert in certifications:
			list_name = '%s %s %s' % (lst_ins, cert.upper(), ls(32473))
			self.AD({'mode': mode, 'action': action, 'certification': cert, 'list_name': list_name}, cert.upper(), 'certifications.png')
		self._end_directory()

	def languages(self):
		from modules.meta_lists import languages
		menu_type = self.params_get('menu_type')
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_languages' if menu_type == 'movie' else 'tmdb_tv_languages'
		lst_ins = self.make_list_name(menu_type)
		for lang in languages:
			list_name = '%s %s %s' % (lst_ins, lang[0], ls(32471))
			self.AD({'mode': mode, 'action': action, 'language': lang[1], 'list_name': list_name}, lang[0], 'languages.png')
		self._end_directory()

	def years(self):
		from modules.meta_lists import years
		menu_type = self.params_get('menu_type')
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_year' if menu_type == 'movie' else 'tmdb_tv_year'
		lst_ins = self.make_list_name(menu_type)
		for i in years():
			list_name = '%s %s %s' % (lst_ins, str(i), ls(32460))
			self.AD({'mode': mode, 'action': action, 'year': str(i), 'list_name': list_name}, str(i), 'calender.png')
		self._end_directory()

	def genres(self):
		menu_type = self.params_get('menu_type')
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_genres' if menu_type == 'movie' else 'tmdb_tv_genres'
		lst_ins = self.make_list_name(menu_type)
		if menu_type == 'movie':  from modules.meta_lists import movie_genres as genre_list
		else: from modules.meta_lists import tvshow_genres as genre_list
		self.AD({'mode': mode, 'action': action, 'genre_list': json.dumps(genre_list), 'exclude_external': 'true'}, ls(32789), 'genres.png')
		for genre, value in sorted(genre_list.items()):
			list_name = '%s %s %s' % (lst_ins, genre, ls(32470))
			self.AD({'mode': mode, 'action': action, 'genre_id': value[0], 'list_name': list_name}, genre, value[1])
		self._end_directory()

	def networks(self):
		from modules.meta_lists import networks
		lst_ins = self.make_list_name(self.params_get('menu_type'))
		for item in sorted(networks, key=lambda k: k['name']):
			list_name = '%s %s %s' % (lst_ins, item['name'], ls(32480))
			self.AD({'mode': 'build_tvshow_list', 'action': 'tmdb_tv_networks', 'network_id': item['id'], 'list_name': list_name}, item['name'], item['logo'])
		self._end_directory()

	def trakt_mosts(self):
		menu_type = self.params_get('menu_type')
		final_mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'trakt_movies_mosts' if menu_type == 'movie' else 'trakt_tv_mosts'
		lst_ins = self.make_list_name(menu_type)
		trakt_mosts = {ls(32539): ['played', 'most__played.png'],
					   ls(32540): ['collected', 'most__collected.png'],
					   ls(32475): ['watched', 'most__watched.png']}
		mosts_str = ls(32469)
		n_ins = _in_str % (mosts_str.upper(), '%s')
		for most, value in trakt_mosts.items():
			list_name = '%s %s %s' % (lst_ins, mosts_str, most)
			self.AD({'mode': 'navigator.trakt_mosts_duration', 'action': action, 'period_str': most, 'period': value[0], 'menu_type': menu_type,
							'final_mode': final_mode, 'iconImage': value[1], 'list_name': list_name}, n_ins % most, value[1])
		self._end_directory()

	def trakt_mosts_duration(self):
		lst_ins = self.make_list_name(self.params_get('menu_type'))
		mosts_str, most_str = ls(32469), ls(32970)
		w_str, m_str, y_str, at_str = '%s %s' % (ls(32544), ls(32541)), '%s %s' % (ls(32544), ls(32542)), '%s %s' % (ls(32544), ls(32543)), '%s %s' % (ls(32129), ls(32545))
		durations = [(w_str, 'weekly'), (m_str, 'monthly'), (y_str, 'yearly'), (at_str, 'all')]
		period_str = self.params_get('period_str')
		for duration, urlitem in durations:
			list_name = '%s %s %s %s' % (lst_ins, mosts_str, period_str.capitalize(), duration)
			self.AD({'mode': self.params_get('final_mode'), 'action': self.params_get('action'), 'period': self.params_get('period'), 'duration': urlitem,
							'list_name': list_name}, most_str % (period_str.upper(), duration), self.params_get('iconImage'))
		self._end_directory()

	def folder_navigator(self):
		from modules.utils import clean_file_name, normalize
		from caches.main_cache import main_cache
		def _process():
			for tup in items:
				item = tup[0]
				isFolder = tup[1]
				if sources_folders and isFolder:
					cm = []
					cm_append = cm.append
					normalized_folder_name = normalize(item)
					link_folders_add = {'mode': 'link_folders', 'service': 'FOLDER', 'folder_name': normalized_folder_name, 'action': 'add'}
					link_folders_remove = {'mode': 'link_folders', 'service': 'FOLDER', 'folder_name': normalized_folder_name, 'action': 'remove'}
					string = 'FEN_FOLDER_%s' % normalized_folder_name
					current_link = main_cache.get(string)
					if current_link: ending = '[COLOR=limegreen][B][I]\n%s[/I][/B][/COLOR]' % (linkedto_str % current_link)
					else: ending = ''
				else: ending = ''
				display = '%s%s' % (item, ending)
				url = os.path.join(folder_path, item)
				listitem = kodi_utils.make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'fanart': fanart})
				if sources_folders and isFolder:
					cm_append((link_str,'RunPlugin(%s)' % self._build_url(link_folders_add)))
					if ending != '': cm_append((clear_str,'RunPlugin(%s)' % self._build_url(link_folders_remove)))
					listitem.addContextMenuItems(cm)
				yield (url, listitem, isFolder)
		link_str, clear_str, linkedto_str = ls(32745), ls(32746), ls(32744)
		folder_path = self.params_get('folder_path')
		sources_folders = self.params_get('sources_folders', None)
		if sources_folders: from modules.utils import normalize
		dirs, files = kodi_utils.list_dirs(folder_path)
		items = [(i, True) for i in dirs] + [(i, False) for i in files]
		item_list = list(_process())
		__handle__ = int(argv[1])
		kodi_utils.add_items(__handle__, item_list)
		kodi_utils.set_sort_method(__handle__, 'files')
		self._end_directory()
	
	def sources_folders(self):
		for source in ('folder1', 'folder2', 'folder3', 'folder4', 'folder5'):
			for db_type in ('movie', 'tvshow'):
				folder_path = sett.source_folders_directory(db_type, source)
				if not folder_path: continue
				name = '[B]%s (%s): %s[/B]\n     [I]%s[/I]' % (source.upper(), self.make_list_name(db_type).upper(), get_setting('%s.display_name' % source).upper(), folder_path)
				self.AD({'mode': 'navigator.folder_navigator','sources_folders': 'True', 'folder_path': folder_path, 'list_name': name}, name, 'most__collected.png')
		self._end_directory()

	def tips(self):
		tips_location = tp('special://home/addons/plugin.video.fen/resources/text/tips')
		files = sorted(kodi_utils.list_dirs(tips_location)[1])
		help_str, new_str, spotlight_str = ls(32487).upper(), ls(32857).upper(), ls(32858).upper()
		n_ins = '%s: %s'  % (ls(32546).upper(), '%s')
		tips_list = []
		append = tips_list.append
		for item in files:
			tip = item.replace('.txt', '')[4:]
			if 'COLOR' in tip:
				if 'crimson' in tip: tip, sort_order = tip.replace('[COLOR crimson]', '[COLOR crimson]%s!!![/COLOR] ' % help_str), 0
				elif 'chartreuse' in tip: tip, sort_order = tip.replace('[COLOR chartreuse]', '[COLOR chartreuse]%s!![/COLOR] ' % new_str), 1
				else: tip, sort_order = tip.replace('[COLOR orange]', '[COLOR orange]%s![/COLOR] ' % spotlight_str), 2 #orange
			else:
				sort_order = 3
			tip_name = n_ins % tip
			action = {'mode': 'show_text', 'heading': tip, 'file': tp(os.path.join(tips_location, item))}
			append((action, tip_name, sort_order))
		item_list = sorted(tips_list, key=lambda x: x[2])
		for c, i in enumerate(item_list, 1): self.AD(i[0], '%02d. %s' % (c, i[1]), os.path.join(icon_directory, 'information.png'), False)
		self._end_directory()

	def because_you_watched(self):
		from modules.watched_status import get_watched_info_movie, get_watched_info_tv
		def _convert_fen_watched_episodes_info(watched_indicators):
			final_list = []
			used_names = []
			final_append = final_list.append
			used_append = used_names.append
			_watched = get_watched_info_tv(watched_indicators)
			for item in _watched:
				name = item[3]
				if not name in used_names:
					tv_show = [i for i in _watched if i[3] == name]
					max_tvshow = max(tv_show)
					final_item = (max_tvshow[0], 'foo', [(max_tvshow[1], max_tvshow[2])], max_tvshow[3], max_tvshow[4])
					final_append(final_item)
					used_append(name)
			return final_list
		watched_indicators = sett.watched_indicators()
		db_type = self.params_get('menu_type')
		func = get_watched_info_movie if db_type == 'movie' else _convert_fen_watched_episodes_info
		key_index = 2 if db_type == 'movie' else 4
		name_index = 1 if db_type == 'movie' else 3
		tmdb_index = 0
		mode = 'build_movie_list' if db_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_recommendations' if db_type == 'movie' else 'tmdb_tv_recommendations'
		recently_watched = func(watched_indicators)
		recently_watched = sorted(recently_watched, key=lambda k: k[key_index], reverse=True)
		because_str = ls(32474)
		because_ins = '[I]%s[/I]  [B]%s[/B]' % (because_str, '%s')
		for item in recently_watched:
			if db_type == 'movie':
				name = because_ins % item[name_index]
			else:
				season, episode = item[2][-1]
				name = because_ins % '%s - %sx%s' % (item[name_index], season, episode)
			tmdb_id = item[tmdb_index]
			self.AD({'mode': mode, 'action': action, 'tmdb_id': tmdb_id, 'exclude_external': 'true'}, name, 'because_you_watched.png')
		self._end_directory()

	def make_list_name(self, menu_type):
		return menu_type.replace('tvshow', tv_str).replace('movie', mov_str)
	
	def shortcut_folders(self):
		def _make_icon(chosen_icon):
			return os.path.join(icon_directory, chosen_icon)
		def _make_new_item():
			icon = _make_icon('new.png')
			display_name = '[I]%s...[/I]' % ls(32702)
			url_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_shortcut_folder'}
			url = self._build_url(url_params)
			listitem = kodi_utils.make_listitem()
			listitem.setLabel(display_name)
			listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
			kodi_utils.add_item(__handle__, url, listitem, False)
		def _builder():
			icon = os.path.join(icon_directory, 'genre_foreign.png')
			for i in folders:
				try:
					cm = []
					cm_append = cm.append
					name = i[0]
					display_name = '[B]%s : [/B] %s ' % (short_str.upper(), i[0])
					contents = json.loads(i[1])
					url_params = {'iconImage': 'genre_foreign.png', 
								'mode': 'navigator.build_shortcut_folder_lists',
								'action': name,
								'name': name, 
								'shortcut_folder': 'True',
								'external_list_item': 'True',
								'shortcut_folder': 'True',
								'contents': contents}
					remove_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'delete_shortcut_folder', 'list_name': name}
					remove_all_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'remove_all_shortcut_folders'}
					url = self._build_url(url_params)
					listitem = kodi_utils.make_listitem()
					listitem.setLabel(display_name)
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					cm_append((delete_str,'RunPlugin(%s)'% self._build_url(remove_params)))
					cm_append((all_str,'RunPlugin(%s)'% self._build_url(remove_all_params)))
					listitem.addContextMenuItems(cm)
					yield (url, listitem, True)
				except: pass
		__handle__ = int(argv[1])
		short_str, delete_str, all_str = ls(32514), ls(32703), ls(32704)
		dbcon = database.connect(NAVIGATOR_DB)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT list_name, list_contents FROM navigator WHERE list_type = ?", ('shortcut_folder',))
		folders = dbcur.fetchall()
		try: folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
		except: folders = []
		_make_new_item()
		kodi_utils.add_items(__handle__, list(_builder()))
		self._end_directory()

	def adjust_main_lists(self, params=None):
		def db_execute():
			dbcon = database.connect(NAVIGATOR_DB)
			dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, 'edited'))
			dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'edited', json.dumps(li)))
			dbcon.commit()
			kodi_utils.set_property('fen_%s_edited' % list_name, json.dumps(li))
		def menu_select(heading, multi_line='true', position_list=False):
			def _builder():
				for item in choice_items:
					item_get = item.get
					line2 = pos_str % (menu_name, ls(item['name'])) if position_list else ''
					try: icon = item_get('iconImage', 'discover.png') if item_get('network_id', None) else os.path.join(icon_directory, item_get('iconImage'))
					except: icon = os.path.join(icon_directory, 'discover.png')
					yield {'line1': ls(item['name']), 'line2': line2, 'icon':icon}
			pos_str, top_pos_str, top_str = ls(32707), ls(32708), ls(32709)
			list_items = list(_builder())
			if position_list:
				top_item = {'line1': top_str, 'line2': top_pos_str % menu_name, 'icon': os.path.join(icon_directory, 'top.png')}
				list_items.insert(0, top_item)
			index_list = [list_items.index(i) for i in list_items]
			kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': multi_line}
			return kodi_utils.select_dialog(index_list, **kwargs)
		def select_from_main_menus(current_list=[], item_list=[]):
			include_list = DefaultMenus().DefaultMenuItems()
			menus = DefaultMenus().RootList()
			menus.insert(0, {'name': ls(32457), 'iconImage': 'fen.png', 'mode': 'navigator.main', 'action': 'RootList'})
			include_list = [i for i in include_list if i != current_list]
			menus = [i for i in menus if i.get('action', None) in include_list and not i.get('name') == item_list]
			return menus
		def get_external_name():
			name_append_list = [('RootList', ''), ('MovieList', '%s ' % ls(32028)), ('TVShowList', '%s ' % ls(32029))]
			orig_name = params.get('list_name', None)
			try: name = '%s%s' % ([i[1] for i in name_append_list if i[0] == orig_name][0], ls(menu_item.get('name')))
			except: name = orig_name
			name = kodi_utils.dialog.input('Fen', defaultt=name)
			return name
		def db_execute_shortcut_folder(action='add'):
			dbcon = database.connect(NAVIGATOR_DB)
			dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (menu_name, 'shortcut_folder'))
			if action == 'add': dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (menu_name, 'shortcut_folder', json.dumps(li)))
			dbcon.commit()
			kodi_utils.set_property('fen_%s_shortcut_folder' % menu_name, json.dumps(li))
		def db_execute_add_to_shortcut_folder():
			dbcon = database.connect(NAVIGATOR_DB)
			dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ?", (shortcut_folder_name,))
			dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (menu_name, 'shortcut_folder'))
			if action == 'add': dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (menu_name, 'shortcut_folder', json.dumps(li)))
			dbcon.commit()
			kodi_utils.set_property('fen_%s_shortcut_folder' % list_name, json.dumps(li))
		def check_shortcut_folders():
			dbcon = database.connect(NAVIGATOR_DB)
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT list_name, list_contents FROM navigator WHERE list_type = ?", ('shortcut_folder',))
			folders = dbcur.fetchall()
			try: folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
			except: folders = []
			return folders
		def select_shortcut_folders(make_new=False):
			folders = check_shortcut_folders()
			selection = 0
			if len(folders) > 0:
				folder_names = ['[B]%s[/B]' % i[0] for i in folders]
				icon = os.path.join(icon_directory, 'genre_foreign.png')
				list_items = [{'line1': item.replace('[B]', '').replace('[/B]', ''), 'line2': 'Existing Shortcut Folder', 'icon': icon} for item in folder_names]
				if make_new:
					new_item = {'line1': ls(32715).replace('[B]', '').replace('[/B]', ''), 'line2': ls(32702), 'icon': os.path.join(icon_directory, 'new.png')}
					list_items.insert(0, new_item)
				index_list = [list_items.index(i) for i in list_items]
				kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'true'}
				selection = kodi_utils.select_dialog(index_list, **kwargs)
			return folders, selection
		kodi_utils.clear_property('fen_%s_default')
		kodi_utils.clear_property('fen_%s_edited')
		if not params: params = self.params
		menu_name = params.get('menu_name', '')
		list_name = params.get('list_name', '')
		li = None
		method = params.get('method')
		choice_list = []
		refresh = True
		if not method in ('display_edit_menu', 'add_external', 'add_trakt_external', 'add_imdb_external', 'restore'):
			try:
				current_position = int(params.get('position', '0'))
				default_list, edited_list = self._db_lists(list_name)
				def_file = default_list if not edited_list else edited_list
				li, def_li = def_file, default_list
				choice_items = [i for i in def_li if i not in li]
			except: pass
		try:
			if method == 'display_edit_menu':
				shortcut_folders_active = check_shortcut_folders()
				default_menu = params.get('default_menu')
				edited_list = None if params.get('edited_list') == 'None' else params.get('edited_list')
				list_name = params.get('list_name') if 'list_name' in params else self.list_name
				menu_name = params.get('menu_name')
				position = params.get('position')
				external_list_item = params.get('external_list_item', 'False') == 'True'
				list_is_full = params.get('list_is_full', 'False') == 'True'
				list_slug = params.get('list_slug', '')
				menu_item = json.loads(params.get('menu_item'))
				shortcut_folder = menu_item.get('shortcut_folder', 'False') == 'True'
				menu_item['list_name'] = list_name
				list_heading = ls(32457) if list_name == 'RootList' else ls(32028) if list_name == 'MovieList' else ls(32029)
				listing = []
				if len(default_menu) != 1:
					listing += [(ls(32716) % menu_name, 'move')]
					listing += [(ls(32717) % menu_name, 'remove')]
				if not shortcut_folder:
					listing += [(ls(32718) % menu_name, 'add_external')]
					if shortcut_folders_active: listing += [(ls(32719) % menu_name, 'shortcut_folder_add')]
				if list_name in ('RootList', 'MovieList', 'TVShowList'): listing += [(ls(32720) % list_heading, 'add_trakt')]
				if not list_is_full: listing += [(ls(32721) % list_heading, 'add_original')]
				listing += [(ls(32722) % list_heading, 'restore')]
				listing += [(ls(32723) % list_heading, 'check_update')]
				if not list_slug and not external_list_item: listing += [(ls(32724) % menu_name, 'reload')]
				if list_name in ('RootList', 'MovieList', 'TVShowList'): listing += [(ls(32725), 'shortcut_folder_new')]
				list_items = [{'line1': i[0]} for i in listing]
				kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
				choice = kodi_utils.select_dialog([i[1] for i in listing], **kwargs)
				if choice in (None, 'save_and_exit'): return
				elif choice == 'move': params = {'method': 'move', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
				elif choice == 'remove': params = {'method': 'remove', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
				elif choice == 'add_original': params = {'method': 'add_original', 'list_name': list_name, 'position': position}
				elif choice == 'restore': params = {'method': 'restore', 'list_name': list_name, 'position': position}
				elif choice == 'add_external': params = {'method': 'add_external', 'list_name': list_name, 'menu_item': json.dumps(menu_item)}
				elif choice == 'shortcut_folder_add': params = {'method': 'shortcut_folder_add', 'list_name': list_name, 'menu_item': json.dumps(menu_item)}
				elif choice == 'add_trakt': params = {'method': 'add_trakt', 'list_name': list_name, 'position': position}
				elif choice == 'reload': params = {'method': 'reload_menu_item', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
				elif choice == 'shortcut_folder_new': params = {'method': 'shortcut_folder_new', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
				elif choice == 'check_update': params = {'method': 'check_update_list', 'list_name': list_name, 'menu_name': menu_name, 'position': position}
				return self.adjust_main_lists(params)
			elif method == 'move':
				choice_items = [i for i in li if ls(i['name']) != menu_name]
				new_position = menu_select('Fen', position_list=True)
				if new_position == None or new_position == current_position: return
				li.insert(new_position, li.pop(current_position))
				db_execute()
			elif method == 'remove':
				li = [i for i in li if ls(i['name']) != menu_name]
				db_execute()
			elif method == 'add_original':
				selection = menu_select('Fen', multi_line='false')
				if selection == None: return
				selection = choice_items[selection]
				choice_list = []
				choice_items = li
				item_position = menu_select('Fen', position_list=True)
				if item_position == None: return
				li.insert((item_position), selection)
				db_execute()
			elif method == 'shortcut_folder_add':
				menu_item = json.loads(params['menu_item'])
				if not menu_item: return
				current_shortcut_folders, folder_selection = select_shortcut_folders()
				if not current_shortcut_folders: return kodi_utils.notification(32702)
				if folder_selection == None: return
				name = get_external_name()
				if not name: return
				menu_item['name'] = name
				folder_selection = current_shortcut_folders[folder_selection]
				shortcut_folder_name = folder_selection[0]
				shortcut_folder_contents = json.loads(folder_selection[1])
				choice_items = shortcut_folder_contents
				if len(choice_items) > 0: item_position = menu_select('Fen', position_list=True)
				else: item_position = 0
				if item_position == None: return
				menu_item['external_list_item'] = 'True'
				shortcut_folder_contents.insert((item_position), menu_item)
				menu_name = shortcut_folder_name
				li = shortcut_folder_contents
				db_execute_shortcut_folder()
			elif method == 'add_external':
				menu_item = json.loads(params['menu_item'])
				if not menu_item: return
				if menu_item.get('action') == 'imdb_keywords_list_contents': refresh = False
				name = get_external_name()
				if not name: return
				menu_item['name'] = name
				choice_items = select_from_main_menus(params.get('list_name'), name)
				selection = menu_select(ls(32726) % params.get('list_name'), multi_line='false')
				if selection == None: return
				add_to_menu_choice = choice_items[selection]
				list_name = add_to_menu_choice['action']
				default_list, edited_list = self._db_lists(list_name)
				def_file = default_list if not edited_list else edited_list
				li = def_file
				if menu_item in li: return
				choice_list = []
				choice_items = li
				item_position = menu_select('Fen', position_list=True)
				if item_position == None: return
				menu_item['external_list_item'] = 'True'
				li.insert((item_position), menu_item)
				db_execute()
			elif method == 'add_trakt':
				from apis.trakt_api import get_trakt_list_selection
				trakt_selection = json.loads(params['trakt_selection']) if 'trakt_selection' in params else get_trakt_list_selection(list_choice='nav_edit')
				if not trakt_selection: return
				name = kodi_utils.dialog.input('Fen', defaultt=trakt_selection['name'])
				if not name: return
				choice_list = []
				choice_items = li
				item_position = menu_select('Fen', position_list=True)
				if item_position == None: return
				li.insert(item_position, {'iconImage': 'traktmylists.png', 'mode': 'trakt.lists.build_trakt_list', 'name': name,
											'user': trakt_selection['user'], 'slug': trakt_selection['slug'], 'external_list_item': 'True'})
				db_execute()
			elif method == 'add_trakt_external':
				name = kodi_utils.dialog.input('Fen', defaultt=params['name'])
				if not name: return
				if not li:
					choice_items = select_from_main_menus()
					selection = menu_select(ls(32726) % name, multi_line='false')
					if selection == None: return
					add_to_menu_choice = choice_items[selection]
					list_name = add_to_menu_choice['action']
					default_list, edited_list = self._db_lists(list_name)
					li = default_list if not edited_list else edited_list
				if name in [i['name'] for i in li]: return
				choice_list = []
				choice_items = li
				item_position = 0 if len(li) == 0 else menu_select('Fen', position_list=True)
				if item_position == None: return
				li.insert(item_position, {'iconImage': 'traktmylists.png', 'mode': 'trakt.lists.build_trakt_list', 'name': name, 'user': params['user'],
											'slug': params['slug'], 'external_list_item': 'True'})
				db_execute()
			elif method == 'add_imdb_external':
				name = kodi_utils.dialog.input('Fen', defaultt=params['name'])
				if not name: return
				if not li:
					choice_items = select_from_main_menus()
					selection = menu_select(ls(32726) % name, multi_line='false')
					if selection == None: return
					add_to_menu_choice = choice_items[selection]
					list_name = add_to_menu_choice['action']
					default_list, edited_list = self._db_lists(list_name)
					li = default_list if not edited_list else edited_list
				if name in [i['name'] for i in li]: return
				choice_list = []
				choice_items = li
				item_position = 0 if len(li) == 0 else menu_select('Fen', position_list=True)
				if item_position == None: return
				imdb_params = json.loads(params['imdb_params'])
				imdb_params.update({'iconImage': 'imdb.png', 'name': name, 'external_list_item': 'True'})
				li.insert(item_position, imdb_params)
				db_execute()
			elif method == 'browse':
				selection = menu_select('Fen', multi_line='false')
				if selection == None: return
				mode = choice_items[selection]['mode'] if 'mode' in choice_items[selection] else ''
				action = choice_items[selection]['action'] if 'action' in choice_items[selection] else ''
				url_mode = choice_items[selection]['url_mode'] if 'url_mode' in choice_items[selection] else ''
				menu_type = choice_items[selection]['menu_type'] if 'menu_type' in choice_items[selection] else ''
				query = choice_items[selection]['query'] if 'query' in choice_items[selection] else ''
				db_type = choice_items[selection]['db_type'] if 'db_type' in choice_items[selection] else ''
				kodi_utils.execute_builtin('Container.Update(%s)' % self._build_url({'mode': mode, 'action': action, 'url_mode': url_mode, 'menu_type': menu_type,
																			'query': query, 'db_type': db_type}))
			elif method == 'reload_menu_item':
				default = eval('DefaultMenus().%s()' % list_name)
				default_item = [i for i in default if ls(i['name']) == menu_name][0]
				li = [default_item if x['name'] == menu_name else x for x in def_file]
				list_type = 'edited' if self._db_lists(list_name)[1] else 'default'
				dbcon = database.connect(NAVIGATOR_DB)
				dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, list_type))
				dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, list_type, json.dumps(li)))
				dbcon.commit()
				kodi_utils.set_property('fen_%s_%s' % (list_name, list_type), json.dumps(li))
			elif method == 'shortcut_folder_new':
				make_new_folder = True
				current_shortcut_folders, folder_selection = select_shortcut_folders(make_new=True)
				if folder_selection == None: return
				if folder_selection > 0:
					make_new_folder = False
					folder_selection = current_shortcut_folders[folder_selection-1] # -1 because we added the 'Make New' listitem
					name = folder_selection[0]
					contents = folder_selection[1]
				if make_new_folder:
					name = kodi_utils.dialog.input('Fen')
					if not name: return
					contents = []
				if name in [ls(i['name']) for i in li]: return kodi_utils.notification(32490)
				menu_item = {'iconImage': 'genre_foreign.png', 
							'mode': 'navigator.build_shortcut_folder_lists',
							'action': name,
							'name': name, 
							'shortcut_folder': 'True',
							'external_list_item': 'True',
							'contents': contents}
				choice_list = []
				choice_items = li
				menu_name = name
				item_position = 0 if len(li) == 0 else menu_select('Fen', position_list=True)
				if item_position == None: return
				li.insert(item_position, menu_item)
				db_execute()
				if make_new_folder:
					li = []
					db_execute_shortcut_folder()
			elif method == 'check_update_list':
				dbcon = database.connect(NAVIGATOR_DB)
				dbcur = dbcon.cursor()
				new_contents = eval('DefaultMenus().%s()' % list_name)
				if default_list != new_contents:
					new_entry = [i for i in new_contents if i not in default_list][0]
					text = '%s[CR]%s' % (ls(32727) % ls(new_entry.get('name')), ls(32728))
					if not kodi_utils.confirm_dialog(text=text): return
					choice_items = def_file
					item_position = menu_select('Fen', position_list=True)
					if item_position == None: return
					if edited_list:
						edited_list.insert(item_position, new_entry)
						dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, 'edited'))
						dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'edited', json.dumps(edited_list)))
						kodi_utils.set_property('fen_%s_edited' % list_name, json.dumps(edited_list))
					default_list.insert(item_position, new_entry)
					dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, 'default'))
					dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'default', json.dumps(default_list)))
					kodi_utils.set_property('fen_%s_default' % list_name, json.dumps(default_list))
					dbcon.commit()
					dbcon.close()
				else:
					return kodi_utils.ok_dialog(text=32983, top_space=True)
			elif method == 'restore':
				if not kodi_utils.confirm_dialog(): return
				dbcon = database.connect(NAVIGATOR_DB)
				for item in ['edited', 'default']: dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (list_name, item))
				dbcon.commit()
				dbcon.execute('VACUUM')
				dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'default', json.dumps(eval('DefaultMenus().%s()' % list_name))))
				dbcon.commit()
				for item in ('edited', 'default'): kodi_utils.clear_property('fen_%s_%s' % (list_name, item))
			if not method in ('browse',):
				kodi_utils.notification(32576, time=1500)
				kodi_utils.sleep(200)
				if refresh: kodi_utils.execute_builtin('Container.Refresh')
		except: return kodi_utils.notification(32574)

	def build_main_lists(self):
		def _process():
			for item_position, item in enumerate(self.default_menu):
				try:
					cm = []
					cm_append = cm.append
					item_get = item.get
					is_folder = item['mode'] not in non_folder_items
					name = ls(item_get('name', ''))
					icon = item_get('iconImage') if item_get('network_id', '') != '' else os.path.join(icon_directory, item_get('iconImage'))
					url = self._build_url(item)
					cm_append((edit_str,'RunPlugin(%s)' % self._build_url(
						{'mode': 'navigator.adjust_main_lists', 'method': 'display_edit_menu', 'default_menu': self.default_menu, 'menu_item': json.dumps(item),
						'edited_list': self.edited_list, 'list_name': self.list_name, 'menu_name': name,
						'position': item_position, 'list_is_full': list_is_full, 'list_slug': item_get('slug', ''),
						'external_list_item': item_get('external_list_item', 'False')})))
					if not list_is_full:
						cm_append((browse_str,'RunPlugin(%s)' % \
						self._build_url({'mode': 'navigator.adjust_main_lists', 'method': 'browse', 'list_name': self.list_name, 'position': item_position})))
					listitem = kodi_utils.make_listitem()
					listitem.setLabel(name)
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					listitem.addContextMenuItems(cm)
					yield (url, listitem, is_folder)
				except: pass
		self.default_list, self.edited_list = self._db_lists()
		self.default_menu = self.edited_list or self.default_list
		current_items_from_default = [i for i in self.default_menu if not i.get('external_list_item', 'False') == 'True']
		list_is_full = True if len(current_items_from_default) >= len(self.default_list) else False
		edit_str, browse_str = ls(32705), ls(32706)
		__handle__ = int(argv[1])
		kodi_utils.add_items(__handle__, list(_process()))
		self._end_directory()

	def adjust_shortcut_folder_lists(self, params=None):
		def db_execute_shortcut_folder(action='add'):
			dbcon = database.connect(NAVIGATOR_DB)
			dbcon.execute("DELETE FROM navigator where list_name=? and list_type=?", (menu_name, 'shortcut_folder'))
			if action == 'add':
				dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (menu_name, 'shortcut_folder', json.dumps(li)))
			dbcon.commit()
			kodi_utils.set_property('fen_%s_shortcut_folder' % menu_name, json.dumps(li))
		def menu_select(heading, position_list=False):
			def _builder():
				for item in choice_items:
					item_get = item.get
					line2 = pos_str % (name, ls(item['name'])) if position_list else ''
					try: icon = item_get('iconImage', 'discover.png') if item_get('network_id', None) else os.path.join(icon_directory, item_get('iconImage'))
					except: icon = os.path.join(icon_directory, 'discover.png')
					yield {'line1': ls(item['name']), 'line2': line2, 'icon':icon}
			pos_str, top_pos_str, top_str = ls(32707), ls(32708), ls(32709)
			list_items = list(_builder())
			if position_list:
				top_item = {'line1': top_str, 'line2': top_pos_str % name, 'icon': os.path.join(icon_directory, 'top.png')}
				list_items.insert(0, top_item)
			index_list = [list_items.index(i) for i in list_items]
			kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'true'}
			return kodi_utils.select_dialog(index_list, **kwargs)
		def select_shortcut_folders(select=True):
			dbcon = database.connect(NAVIGATOR_DB)
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT list_name, list_contents FROM navigator WHERE list_type = ?", ('shortcut_folder',))
			folders = dbcur.fetchall()
			try: folders = sorted([(str(i[0]), i[1]) for i in folders], key=lambda s: s[0].lower())
			except: folders = []
			if not select: return folders
			selection = 0
			folder_choice_list = []
			exist_str = ls(32710)
			if len(folders) > 0:
				folder_names = ['[B]%s[/B]' % i[0] for i in folders]
				icon = os.path.join(icon_directory, 'genre_foreign.png')
				list_items = [{'line1': item, 'line2': exist_str, 'icon': icon} for item in folder_names]
				index_list = [list_items.index(i) for i in list_items]
				kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'true'}
				selection = kodi_utils.select_dialog(index_list, **kwargs)
			return folders, selection
		if not params: params = self.params
		menu_name = params.get('menu_name')
		list_name = params.get('list_name')
		li = None
		method = params.get('method')
		choice_list = []
		current_position = int(params.get('position', '0'))
		try:
			if method == 'display_edit_menu':
				position = params.get('position')
				menu_item = json.loads(params.get('menu_item'))
				contents = json.loads(params.get('contents'))
				external_list_item = params.get('external_list_item', 'False') == 'True'
				list_slug = params.get('list_slug', '')
				list_heading = ls(32457) if list_name == 'RootList' else mov_str if list_name == 'MovieList' else tv_str
				string = ls(32711) % list_name
				listing = []
				if len(contents) != 1: listing += [(ls(32712), 'move')]
				listing += [(ls(32713), 'remove')]
				listing += [(ls(32714), 'add_trakt')]
				listing += [('%s %s' % (ls(32671), ls(32129)), 'clear_all')]
				list_items = [{'line1': i[0]} for i in listing]
				kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
				choice = kodi_utils.select_dialog([i[1] for i in listing], **kwargs)
				if choice in (None, 'save_and_exit'): return
				elif choice == 'move':
					params = {'method': 'move', 'list_name': list_name, 'menu_name': menu_name, 'position': position,
								'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
				elif choice == 'remove':
					params = {'method': 'remove', 'list_name': list_name, 'menu_name': menu_name, 'position': position,
								'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
				elif choice == 'add_trakt':
					params = {'method': 'add_trakt', 'list_name': list_name, 'position': position,
								'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
				elif choice == 'clear_all':
					params = {'method': 'clear_all', 'list_name': list_name, 'menu_name': menu_name, 'position': position,
								'menu_item': json.dumps(menu_item), 'contents': json.dumps(contents)}
				return self.adjust_shortcut_folder_lists(params)
			elif method == 'move':
				menu_name = params.get('list_name')
				name = params.get('menu_name')
				li = json.loads(params.get('contents'))
				choice_items = [i for i in li if i['name'] != name]
				new_position = menu_select('Fen', position_list=True)
				if new_position == None or new_position == current_position: return
				li.insert(new_position, li.pop(current_position))
				db_execute_shortcut_folder()
			elif method == 'remove':
				menu_name = params.get('list_name')
				name = params.get('menu_name')
				li = json.loads(params.get('contents'))
				li = [x for x in li if x['name'] != name]
				db_execute_shortcut_folder()
			elif method == 'add_external':
				menu_item = json.loads(params['menu_item'])
				if not menu_item: return
				name = kodi_utils.dialog.input('Fen', defaultt=params['name'])
				if not name: return
				current_shortcut_folders, folder_selection = select_shortcut_folders()
				if folder_selection == None: return
				menu_item['name'] = name
				folder_selection = current_shortcut_folders[folder_selection]
				shortcut_folder_name = folder_selection[0]
				shortcut_folder_contents = json.loads(folder_selection[1])
				choice_items = shortcut_folder_contents
				if len(choice_items) > 0: item_position = menu_select('Fen', position_list=True)
				else: item_position = 0
				if item_position == None: return
				menu_name = shortcut_folder_name
				li = shortcut_folder_contents
				li.insert(item_position, menu_item)
				db_execute_shortcut_folder()
			elif method == 'add_trakt':
				from apis.trakt_api import get_trakt_list_selection
				trakt_selection = json.loads(params['trakt_selection']) if 'trakt_selection' in params else get_trakt_list_selection(list_choice='nav_edit')
				if not trakt_selection: return
				name = kodi_utils.dialog.input('Fen', defaultt=trakt_selection['name'])
				if not name: return
				menu_name = params.get('list_name')
				li = json.loads(params.get('contents'))
				choice_items = li
				item_position = menu_select('Fen', position_list=True)
				if item_position == None: return
				li.insert(item_position, {'iconImage': 'traktmylists.png', 'mode': 'trakt.lists.build_trakt_list', 'name': name,
										'user': trakt_selection['user'], 'slug': trakt_selection['slug'], 'external_list_item': 'True'})
				db_execute_shortcut_folder()
			elif method == 'add_trakt_external':
				name = kodi_utils.dialog.input('Fen', defaultt=params['name'])
				if not name: return
				current_shortcut_folders, folder_selection = select_shortcut_folders()
				if folder_selection == None: return
				folder_selection = current_shortcut_folders[folder_selection]
				shortcut_folder_name = folder_selection[0]
				shortcut_folder_contents = json.loads(folder_selection[1])
				choice_items = shortcut_folder_contents
				if len(choice_items) > 0: item_position = menu_select('Fen', position_list=True)
				else: item_position = 0
				if item_position == None: return
				menu_name = shortcut_folder_name
				li = shortcut_folder_contents
				li.insert(item_position, {'iconImage': 'traktmylists.png', 'mode': 'trakt.lists.build_trakt_list', 'name': name, 'user': params['user'],
										'slug': params['slug'], 'external_list_item': 'True'})
				db_execute_shortcut_folder()
			elif method == 'add_imdb_external':
				name = kodi_utils.dialog.input('Fen', defaultt=params['name'])
				if not name: return
				current_shortcut_folders, folder_selection = select_shortcut_folders()
				if folder_selection == None: return
				folder_selection = current_shortcut_folders[folder_selection]
				shortcut_folder_name = folder_selection[0]
				shortcut_folder_contents = json.loads(folder_selection[1])
				choice_items = shortcut_folder_contents
				if len(choice_items) > 0: item_position = menu_select('Fen', position_list=True)
				else: item_position = 0
				if item_position == None: return
				menu_name = shortcut_folder_name
				li = shortcut_folder_contents
				imdb_params = json.loads(params['imdb_params'])
				imdb_params.update({'iconImage': 'imdb.png', 'name': name, 'external_list_item': 'True'})
				li.insert(item_position, imdb_params)
				db_execute_shortcut_folder()
			elif method == 'clear_all':
				if not kodi_utils.confirm_dialog(): return
				menu_name = params.get('list_name')
				li = []
				db_execute_shortcut_folder()
			elif method == 'add_shortcut_folder':
				name = kodi_utils.dialog.input('Fen')
				if not name: return
				dbcon = database.connect(NAVIGATOR_DB)
				dbcur = dbcon.cursor()
				dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (name, 'shortcut_folder', json.dumps([])))
				dbcon.commit()
			elif method == 'delete_shortcut_folder':
				if not kodi_utils.confirm_dialog(): return
				list_name = params['list_name']
				dbcon = database.connect(NAVIGATOR_DB)
				dbcur = dbcon.cursor()
				dbcur.execute("DELETE FROM navigator WHERE list_name = ?", (list_name,))
				dbcon.commit()
				kodi_utils.clear_property('fen_%s_shortcut_folder' % list_name)
				kodi_utils.ok_dialog(text=32729, top_space=True)
			elif method == 'remove_all_shortcut_folders':
				if not kodi_utils.confirm_dialog(): return
				dbcon = database.connect(NAVIGATOR_DB)
				dbcur = dbcon.cursor()
				dbcon.execute("DELETE FROM navigator WHERE list_type=?", ('shortcut_folder',))
				dbcon.commit()
				kodi_utils.ok_dialog(text=32729, top_space=True)
			kodi_utils.notification(32576, time=1500)
			kodi_utils.sleep(200)
			if not method in ('add_external', 'add_trakt_external'):
				kodi_utils.sleep(200)
				kodi_utils.execute_builtin('Container.Refresh')
		except Exception:
			return kodi_utils.notification(32574, time=1500)
	
	def build_shortcut_folder_lists(self):
		def _build_default():
			icon = os.path.join(icon_directory, 'genre_foreign.png')
			url_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_trakt', 'contents': [], 'menu_item': '',
						'list_name': list_name, 'menu_name': '',
						'position': '', 'list_slug': '',
						'external_list_item': 'False'}
			url = self._build_url(url_params)
			listitem = kodi_utils.make_listitem()
			listitem.setLabel('[B][I]%s...[/I][/B]' % ls(32714))
			listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
			kodi_utils.add_item(__handle__, url, listitem, False)
		def _process():
			for item_position, item in enumerate(contents):
				try:
					cm = []
					is_folder = item['mode'] not in non_folder_items
					item_get = item.get
					name = item_get('name', '')
					icon = item_get('iconImage') if item_get('network_id', '') != '' else os.path.join(icon_directory, item_get('iconImage'))
					url = self._build_url(item)
					cm.append((ls(32705),'RunPlugin(%s)' % self._build_url(
						{'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'display_edit_menu', 'contents': json.dumps(contents), 'menu_item': json.dumps(item),
						'list_name': list_name, 'menu_name': name,
						'position': item_position, 'list_slug': item_get('slug', ''),
						'external_list_item': item_get('external_list_item', 'False')})))
					listitem = kodi_utils.make_listitem()
					listitem.setLabel(name)
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					listitem.addContextMenuItems(cm)
					yield (url, listitem, is_folder)
				except: pass
		__handle__ = int(argv[1])
		contents = self._db_lists_shortcut_folder()
		list_name = self.params_get('name')
		if not contents: _build_default()
		else: kodi_utils.add_items(__handle__, list(_process()))
		self._end_directory()

	def _build_url(self, query):
		try: url = 'plugin://plugin.video.fen/?' + urlencode(query)
		except: url = 'plugin://plugin.video.fen/?' + urlencode(to_utf8(query))
		return url

	def _db_lists(self, list_name=None):
		list_name = self.list_name if not list_name else list_name
		try:
			default_contents = json.loads(kodi_utils.get_property('fen_%s_default' % list_name))
			try: edited_contents = json.loads(kodi_utils.get_property('fen_%s_edited' % list_name))
			except: edited_contents = None
			return default_contents, edited_contents
		except: pass
		try:
			dbcon = database.connect(NAVIGATOR_DB)
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?", (str(list_name), 'default'))
			default_contents = json.loads(dbcur.fetchone()[0])
			dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?", (str(list_name), 'edited'))
			try: edited_contents = json.loads(dbcur.fetchone()[0])
			except: edited_contents = None
			kodi_utils.set_property('fen_%s_default' % list_name, json.dumps(default_contents))
			kodi_utils.set_property('fen_%s_edited' % list_name, json.dumps(edited_contents))
			return default_contents, edited_contents
		except:
			self._build_database()
			return self._db_lists()
	
	def _db_lists_shortcut_folder(self, list_name=None):
		list_name = self.list_name if not list_name else list_name
		try:
			contents = json.loads(kodi_utils.get_property('fen_%s_shortcut_folder' % list_name))
			return contents
		except: pass
		try:
			dbcon = database.connect(NAVIGATOR_DB)
			dbcur = dbcon.cursor()
			dbcur.execute("SELECT list_contents FROM navigator WHERE list_name = ? AND list_type = ?", (str(list_name), 'shortcut_folder'))
			contents = json.loads(dbcur.fetchone()[0])
			kodi_utils.set_property('fen_%s_shortcut_folder' % list_name, json.dumps(contents))
			return contents
		except:
			return []

	def _rebuild_single_database(self, dbcon, list_name):
		dbcon.execute("DELETE FROM navigator WHERE list_type=? and list_name=?", ('default', list_name))
		dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (list_name, 'default', json.dumps(eval('DefaultMenus().%s()' % list_name))))
		dbcon.commit()

	def _build_database(self):
		default_menus = DefaultMenus().DefaultMenuItems()
		dbcon = database.connect(NAVIGATOR_DB)
		dbcon.execute("CREATE TABLE IF NOT EXISTS navigator (list_name text, list_type text, list_contents text)")
		for content in default_menus:
			dbcon.execute("INSERT INTO navigator VALUES (?, ?, ?)", (content, 'default', json.dumps(eval('DefaultMenus().%s()' % content))))
		dbcon.commit()

	def AD(self, url_params, list_name, iconImage='DefaultFolder.png', isFolder=True):
		__handle__ = int(argv[1])
		cm = []
		cm_append = cm.append
		icon = iconImage if 'network_id' in url_params else os.path.join(icon_directory, iconImage)
		url_params['iconImage'] = icon
		url = self._build_url(url_params)
		listitem = kodi_utils.make_listitem()
		listitem.setLabel(list_name)
		listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
		if 'SpecialSort' in url_params:
			listitem.setProperty('SpecialSort', url_params['SpecialSort'])
		if not 'exclude_external' in url_params:
			list_name = url_params['list_name'] if 'list_name' in url_params else self.list_name
			menu_params = {'mode': 'navigator.adjust_main_lists', 'method': 'add_external',
						'list_name': list_name, 'menu_item': json.dumps(url_params)}
			folder_params = {'mode': 'navigator.adjust_shortcut_folder_lists', 'method': 'add_external',
						'name': list_name, 'menu_item': json.dumps(url_params)}
			cm_append((ls(32730),'RunPlugin(%s)'% self._build_url(menu_params)))
			cm_append((ls(32731),'RunPlugin(%s)' % self._build_url(folder_params)))
			listitem.addContextMenuItems(cm)
		kodi_utils.add_item(__handle__, url, listitem, isFolder)

	def _end_directory(self):
		__handle__ = int(argv[1])
		kodi_utils.set_content(__handle__, '')
		kodi_utils.end_directory(__handle__)
		kodi_utils.set_view_mode(self.view, '')


