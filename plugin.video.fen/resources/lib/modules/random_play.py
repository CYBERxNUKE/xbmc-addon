# -*- coding: utf-8 -*-
from random import choice
import metadata
from modules.settings import date_offset
from modules.kodi_utils import execute_builtin, build_url
from modules.utils import adjust_premiered_date, get_datetime
# from modules.kodi_utils import logger

def play_fetch_random(tmdb_id):
	meta_user_info = metadata.retrieve_user_info()
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info)
	adjust_hours = date_offset()
	current_date = get_datetime()
	episodes_data = metadata.all_episodes_meta(meta, meta_user_info)
	episodes_data = [i for i in episodes_data if not i['season']  == 0 and adjust_premiered_date(i['premiered'], adjust_hours)[0] <= current_date]
	if not episodes_data: return {'pass': True}
	chosen_episode = choice(episodes_data)
	title = meta['title']
	season = int(chosen_episode['season'])
	episode = int(chosen_episode['episode'])
	query = title + ' S%.2dE%.2d' % (season, episode)
	display_name = '%s - %dx%.2d' % (title, season, episode)
	ep_name = chosen_episode['title']
	plot = chosen_episode['plot']
	try: premiered = adjust_premiered_date(chosen_episode['premiered'], adjust_hours)[1]
	except: premiered = chosen_episode['premiered']
	meta.update({'vid_type': 'episode', 'rootname': display_name, 'season': season,
				'episode': episode, 'premiered': premiered, 'ep_name': ep_name,
				'plot': plot, 'random': 'true'})
	url_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'], 'query': query,
				'tvshowtitle': meta['rootname'], 'season': season, 'episode': episode, 'autoplay': 'True'}
	return execute_builtin('RunPlugin(%s)' % build_url(url_params))
