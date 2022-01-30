# -*- coding: utf-8 -*-
import os
import json
import ssl
from threading import Thread
from urllib.parse import unquote, parse_qsl, urlparse
from urllib.request import Request, urlopen
from modules import kodi_utils
from modules.sources import Sources
from modules.utils import clean_file_name, clean_title, to_utf8, safe_string, remove_accents
from modules.settings_reader import get_setting
from modules.settings import download_directory, get_art_provider
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
levels =['../../../..', '../../..', '../..', '..']
poster_empty = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/box_office.png')
video_extensions = ('m4v', '3g2', '3gp', 'nsv', 'tp', 'ts', 'ty', 'pls', 'rm', 'rmvb', 'mpd', 'ifo', 'mov', 'qt', 'divx', 'xvid', 'bivx', 'vob', 'nrg', 'img', 'iso', 'udf', 'pva',
					'wmv', 'asf', 'asx', 'ogm', 'm2v', 'avi', 'bin', 'dat', 'mpg', 'mpeg', 'mp4', 'mkv', 'mk3d', 'avc', 'vp3', 'svq3', 'nuv', 'viv', 'dv', 'fli', 'flv', 'wpl',
					'xspf', 'vdr', 'dvr-ms', 'xsp', 'mts', 'm2t', 'm2ts', 'evo', 'ogv', 'sdp', 'avs', 'rec', 'url', 'pxml', 'vc1', 'h264', 'rcv', 'rss', 'mpls', 'mpl', 'webm',
					'bdmv', 'bdm', 'wtv', 'trp', 'f4v', 'pvr', 'disc')
audio_extensions = ('wav', 'mp3', 'ogg', 'flac', 'wma', 'aac')
image_extensions = ('jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi', 'bmp', 'dib', 'png', 'gif', 'webp', 'tiff', 'tif',
					'psd', 'raw', 'arw', 'cr2', 'nrw', 'k25', 'jp2', 'j2k', 'jpf', 'jpx', 'jpm', 'mj2')

def runner(params):
	kodi_utils.show_busy_dialog()
	threads = []
	append = threads.append
	action = params.get('action')
	if action == 'meta.single':
		Downloader(params).run()
	elif action == 'image':
		for item in ('thumb_url', 'image_url'):
			image_params = params
			image_params['url'] = params.pop(item)
			image_params['db_type'] = item
			Downloader(image_params).run()
	elif action.startswith('cloud'):
		Downloader(params).run()
	elif action == 'meta.pack':
		from modules.source_utils import find_season_in_release_title
		provider = params['provider']
		if provider == 'furk':
			try:
				t_files = Sources().furkPacks(params['file_name'], params['file_id'], download=True)
				pack_choices = [dict(params, **{'pack_files':{'link': item['url_dl'], 'filename': item['name'], 'size': item['size']}}) for item in t_files]
				icon = 'furk.png'
			except: return kodi_utils.notification(32692)
		else:
			try:
				debrid_files, debrid_function = Sources().debridPacks(provider, params['name'], params['magnet_url'], params['info_hash'], download=True)
				pack_choices = [dict(params, **{'pack_files':item}) for item in debrid_files]
				icon = {'Real-Debrid': 'realdebrid.png', 'Premiumize.me': 'premiumize.png', 'AllDebrid': 'alldebrid.png'}[provider]
			except: return kodi_utils.notification(32692)
		default_icon = kodi_utils.translate_path('special://home/addons/script.tikiart/resources/media/%s' % icon)
		chosen_list = select_pack_item(pack_choices, params['highlight'], default_icon)
		if not chosen_list: return
		if provider == 'furk': show_package = True
		else: show_package = json.loads(params['source']).get('package') == 'show'
		meta  = json.loads(chosen_list[0].get('meta'))
		default_name = '%s (%s)' % (clean_file_name(get_title(meta)), meta.get('year'))
		default_foldername = kodi_utils.dialog.input(ls(32228), defaultt=default_name)
		for item in chosen_list:
			if show_package:
				season = find_season_in_release_title(item['pack_files']['filename'])
				if season:
					meta['season'] = season
					item['meta'] = json.dumps(meta)
					item['default_foldername'] = default_foldername
				else: pass
			append(Thread(target=Downloader(item).run))
		[i.start() for i in threads]

def select_pack_item(pack_choices, highlight, icon):
	list_items = [{'line1': '%.2f GB | %s' % (float(item['pack_files']['size'])/1073741824, clean_file_name(item['pack_files']['filename']).upper()), 'icon': icon} \
				for item in pack_choices]
	heading = '%s - %s' % (ls(32031), clean_file_name(json.loads(pack_choices[0].get('source')).get('name')))
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'highlight': highlight, 'enumerate': 'true', 'multi_choice': 'true', 'multi_line': 'false'}
	return kodi_utils.select_dialog(pack_choices, **kwargs)

def get_title(meta):
	language = get_setting('meta_language')
	if 'custom_title' in meta: title = meta['custom_title']
	else:
		if language == 'en': title = meta['title']
		else:
			title = None
			if 'english_title' in meta: title = meta['english_title']
			else:
				try:
					db_type = 'movie' if meta['vid_type'] == 'movie' else 'tv'
					meta_user_info = metadata.retrieve_user_info()
					english_title = metadata.english_translation(db_type, meta['tmdb_id'], meta_user_info)
					if english_title: title = english_title
					else: title = meta['original_title']
				except: pass
			if not title: title = meta['original_title']
		if '(' in title: title = title.split('(')[0]
		if '/' in title: title = title.replace('/', ' ')
	return title

class Downloader:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get

	def run(self):
		self.downPrep()
		self.getDownFolder()
		if not self.getDestinationFolder(): return kodi_utils.hide_busy_dialog()
		self.getURLandHeaders()
		if self.url in (None, 'None', ''):
			kodi_utils.hide_busy_dialog()
			return kodi_utils.notification(32692, 4000)
		self.getFilename()
		self.getExtension()
		self.download_runner(self.url, self.final_destination, self.extension)

	def downPrep(self):
		if 'meta' in self.params:
			art_provider = get_art_provider()
			self.meta = json.loads(self.params_get('meta'))
			self.meta_get = self.meta.get
			title = get_title(self.meta)
			self.db_type = self.meta_get('vid_type')
			self.year = self.meta_get('year')
			self.image = self.meta_get('poster')
			self.image = self.meta_get(art_provider[0]) or self.meta_get(art_provider[1]) or poster_empty
			self.season = self.meta_get('season')
			self.name = self.params_get('name')
		else:
			self.meta = None
			title = self.params_get('name')
			self.db_type = self.params_get('db_type')
			self.image = self.params_get('image')
			self.name = None
		self.title = clean_file_name(title)
		self.provider = self.params_get('provider')
		self.action = self.params_get('action')
		self.source = self.params_get('source')
		self.final_name = None

	def download_runner(self, url, folder_dest, ext):
		dest = os.path.join(folder_dest, self.final_name + ext)
		self.doDownload(url, dest)

	def getURLandHeaders(self):
		url = self.params_get('url')
		if url in (None, 'None', ''):
			if self.action == 'meta.single':
				source = json.loads(self.source)
				url = Sources().resolve_sources(source, self.meta)
			elif self.action == 'meta.pack':
				if self.provider == 'Real-Debrid':
					from apis.real_debrid_api import RealDebridAPI as debrid_function
				elif self.provider == 'Premiumize.me':
					from apis.premiumize_api import PremiumizeAPI as debrid_function
				elif self.provider == 'AllDebrid':
					from apis.alldebrid_api import AllDebridAPI as debrid_function
				url = self.params_get('pack_files')['link']
				if self.provider in ('Real-Debrid', 'AllDebrid'):
					url = debrid_function().unrestrict_link(url)
				elif self.provider == 'Premiumize.me':
					url = debrid_function().add_headers_to_url(url)
		else:
			if self.action.startswith('cloud'):
				if '_direct' in self.action:
					url = self.params_get('url')
				elif 'realdebrid' in self.action:
					from indexers.real_debrid import resolve_rd
					url = resolve_rd(self.params)
				elif 'alldebrid' in self.action:
					from indexers.alldebrid import resolve_ad
					url = resolve_ad(self.params)
				elif 'premiumize' in self.action:
					from apis.premiumize_api import PremiumizeAPI
					url = PremiumizeAPI().add_headers_to_url(url)
				elif 'easynews' in self.action:
					from indexers.easynews import resolve_easynews
					url = resolve_easynews(self.params)
		try: headers = dict(parse_qsl(url.rsplit('|', 1)[1]))
		except: headers = dict('')
		try: url = url.split('|')[0]
		except: pass
		self.url = url
		self.headers = headers

	def getDownFolder(self):
		self.down_folder = download_directory(self.db_type)
		if self.db_type == 'thumb_url':
			self.down_folder = os.path.join(self.down_folder, '.thumbs')
		for level in levels:
			try: kodi_utils.make_directory(os.path.abspath(os.path.join(self.down_folder, level)))
			except: pass

	def getDestinationFolder(self):
		if self.action == 'image':
			self.final_destination = self.down_folder
		elif self.action in ('meta.single', 'meta.pack'):
			default_name = '%s (%s)' % (self.title, self.year)
			if self.action == 'meta.single': folder_rootname = kodi_utils.dialog.input(ls(32228), defaultt=default_name)
			else: folder_rootname = self.params_get('default_foldername', default_name)
			if not folder_rootname: return False
			if self.db_type == 'episode':
				inter = os.path.join(self.down_folder, folder_rootname)
				kodi_utils.make_directory(inter)
				self.final_destination = os.path.join(inter, 'Season %02d' %  int(self.season))
			else:
				self.final_destination = os.path.join(self.down_folder, folder_rootname)
		else:
			self.final_destination = self.down_folder
		kodi_utils.make_directory(self.final_destination)
		return True

	def getFilename(self):
		if self.final_name: final_name = self.final_name
		elif self.action == 'meta.pack':
			name = self.params_get('pack_files')['filename']
			final_name = os.path.splitext(urlparse(name).path)[0].split('/')[-1]
		elif self.action == 'image':
			final_name = self.title
		else:
			name_url = unquote(self.url)
			file_name = clean_title(name_url.split('/')[-1])
			if clean_title(self.title).lower() in file_name.lower():
				final_name = os.path.splitext(urlparse(name_url).path)[0].split('/')[-1]
			else:
				try: final_name = self.name.translate(None, r'\/:*?"<>|').strip('.')
				except: final_name = os.path.splitext(urlparse(name_url).path)[0].split('/')[-1]
		self.final_name = to_utf8(safe_string(remove_accents(final_name)))

	def getExtension(self):
		if self.action == 'archive':
			ext = '.zip'
		if self.action == 'audio':
			ext = os.path.splitext(urlparse(self.url).path)[1][1:]
			if not ext in audio_extensions: ext = 'mp3'
			ext = '.%s' % ext
		elif self.action == 'image':
			ext = os.path.splitext(urlparse(self.url).path)[1][1:]
			if not ext in image_extensions: ext = 'jpg'
			ext = '.%s' % ext
		else:
			ext = os.path.splitext(urlparse(self.url).path)[1][1:]
			if not ext in video_extensions: ext = 'mp4'
			ext = '.%s' % ext
		self.extension = ext

	def confirmDownload(self, mb):
		if self.action not in ('image', 'meta.pack'):
			line = '%s[CR]%s[CR]%s'
			if not kodi_utils.confirm_dialog(text=line % ('[B]%s[/B]' % self.final_name.upper(), ls(32688) % mb, ls(32689))): return False
		return True

	def doDownload(self, url, dest):
		headers = self.headers
		file = dest.rsplit(os.sep, 1)[-1]
		resp = self.getResponse(url, headers, 0)
		if not resp:
			kodi_utils.hide_busy_dialog()
			kodi_utils.ok_dialog(text=32490, top_space=True)
			return
		try:    content = int(resp.headers['Content-Length'])
		except: content = 0
		try:    resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
		except: resumable = False
		if content < 1:
			kodi_utils.hide_busy_dialog()
			kodi_utils.ok_dialog(text=32490, top_space=True)
			return
		size = 1024 * 1024
		mb   = content / (1024 * 1024)
		if content < size:
			size = content
		kodi_utils.hide_busy_dialog()
		if not self.confirmDownload(mb): return
		if self.action not in ('image', 'meta.pack'):
			show_notifications = True
			notification_frequency = 25
		else:
			if self.action == 'meta.pack': kodi_utils.notification(32134, 3500, self.image)
			show_notifications = False
			notification_frequency = 0
		notify, total, errors, count, resume, sleep_time  = 25, 0, 0, 0, 0, 0
		f = kodi_utils.open_file(dest, 'w')
		chunk  = None
		chunks = []
		while True:
			downloaded = total
			for c in chunks: downloaded += len(c)
			percent = min(round(float(downloaded)*100 / content), 100)
			playing = kodi_utils.player.isPlaying()
			if show_notifications:
				if percent >= notify:
					notify += notification_frequency
					try:
						line1 = '%s - [I]%s[/I]' % (str(percent)+'%', self.final_name)
						if not playing: kodi_utils.notification(line1, 3000, self.image)
					except: pass
			chunk = None
			error = False
			try:        
				chunk  = resp.read(size)
				if not chunk:
					if percent < 99:
						error = True
					else:
						while len(chunks) > 0:
							c = chunks.pop(0)
							f.write(c)
							del c
						f.close()
						try: progressDialog.close()
						except: pass
						return self.done(self.final_name, self.db_type, True, self.image)
			except Exception as e:
				error = True
				sleep_time = 10
				errno = 0
				if hasattr(e, 'errno'):
					errno = e.errno
				if errno == 10035: # 'A non-blocking socket operation could not be completed immediately'
					pass
				if errno == 10054: #'An existing connection was forcibly closed by the remote host'
					errors = 10 #force resume
					sleep_time  = 30
				if errno == 11001: # 'getaddrinfo failed'
					errors = 10 #force resume
					sleep_time  = 30
			if chunk:
				errors = 0
				chunks.append(chunk)
				if len(chunks) > 5:
					c = chunks.pop(0)
					f.write(c)
					total += len(c)
					del c
			if error:
				errors += 1
				count  += 1
				kodi_utils.sleep(sleep_time*1000)
			if (resumable and errors > 0) or errors >= 10:
				if (not resumable and resume >= 50) or resume >= 500:
					try: progressDialog.close()
					except: pass
					return self.done(self.final_name, self.db_type, False, self.image)
				resume += 1
				errors  = 0
				if resumable:
					chunks  = []
					resp = self.getResponse(url, headers, total)
				else: pass

	def getResponse(self, url, headers, size):
		try:
			if size > 0:
				size = int(size)
				headers['Range'] = 'bytes=%d-' % size
			req = Request(url, headers=headers)
			resp = urlopen(req, context=ctx, timeout=30)
			return resp
		except: return None

	def done(self, title, db_type, downloaded, image):
		if self.db_type == 'thumb_url': return
		if self.db_type == 'image_url':
			if downloaded: kodi_utils.notification('[I]%s[/I]' % ls(32576), 2500, image)
			else: kodi_utils.notification('[I]%s[/I]' % ls(32691), 2500, image)
		else:
			playing = kodi_utils.player.isPlaying()
			if downloaded: text = '[B]%s[/B] : %s' % (title, '[COLOR forestgreen]%s %s[/COLOR]' % (ls(32107), ls(32576)))
			else: text = '[B]%s[/B] : %s' % (title, '[COLOR red]%s %s[/COLOR]' % (ls(32107), ls(32490)))
			if not downloaded or not playing: 
				kodi_utils.ok_dialog(text=text)



