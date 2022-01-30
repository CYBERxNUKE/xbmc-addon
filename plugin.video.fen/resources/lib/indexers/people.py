# -*- coding: utf-8 -*-
import os
import json
from urllib.parse import unquote
from apis.tmdb_api import tmdb_people_info
from windows import open_window
from indexers.images import Images
from modules.kodi_utils import translate_path, select_dialog, dialog
# from modules.kodi_utils import logger

icon_directory = translate_path('special://home/addons/script.tikiart/resources/media')
tmdb_image_url = 'https://image.tmdb.org/t/p/h632/%s'

def popular_people():
	Images().run({'mode': 'popular_people_image_results', 'page_no': 1})

def person_data_dialog(params):
	if 'query' in params: query = unquote(params['query'])
	else: query = None
	open_window(['windows.people', 'People'], 'people.xml',
				query=params.get('query', None), actor_name=params.get('actor_name'), actor_image=params.get('actor_image'), actor_id=params.get('actor_id'))

def person_search(actor_name=None):
	def _get_actor_details():
		from modules.history import add_to_search_history
		try: actors = tmdb_people_info(query)
		except: return None, None, None
		if len(actors) == 1:
			actors = actors[0]
			actor_id = actors['id']
			actor_name = actors['name']
			try: image_id = actors['profile_path']
			except: image_id = None
			if not image_id: actor_image = os.path.join(icon_directory, 'genre_family.png')
			else: actor_image = tmdb_image_url % image_id
		else:
			def _builder():
				for item in actors:
					known_for_list = [i.get('title', 'NA') for i in item['known_for']]
					known_for_list = [i for i in known_for_list if not i == 'NA']
					image = tmdb_image_url % item['profile_path'] if item['profile_path'] else os.path.join(icon_directory, 'genre_family.png')
					yield {'line1': item['name'], 'line2': ', '.join(known_for_list) if known_for_list else '', 'icon': image}
			list_items = list(_builder())
			kwargs = {'items': json.dumps(list_items), 'heading': 'Fen', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
			selection = select_dialog(actors, **kwargs)
			if selection == None: return None, None, None
			actor_id = int(selection['id'])
			actor_name = selection['name']
			actor_image = tmdb_image_url % selection['profile_path'] if selection['profile_path'] else os.path.join(icon_directory, 'genre_family.png')
		add_to_search_history(actor_name, 'people_queries')
		return actor_name, actor_image, actor_id
	
	if actor_name in ('None', '', None): actor_name = dialog.input('Fen')
	query = unquote(actor_name)
	if not query: return
	actor_name, actor_image, actor_id = _get_actor_details()
	if not actor_name: return
	return person_data_dialog({'actor_name': actor_name, 'actor_image': actor_image, 'actor_id': actor_id})



