# -*- coding: utf-8 -*-
import re
import sys
from cocoscrapers import sources_cocoscrapers
from cocoscrapers.modules.control import getProviderDefaults as coco_default_providers, setProviderDefaults as coco_set_defaults, \
										setting as coco_getSetting, setSetting as coco_setSetting
from metadata import season_episodes_meta
from modules import kodi_utils
from modules.settings import check_prescrape_sources, date_offset, metadata_user_info
from modules.utils import manual_function_import, adjust_premiered_date, get_datetime, jsondate_to_datetime, subtract_dates
# logger = kodi_utils.logger

ls, unquote, unquote_plus, numeric_input, supported_media = kodi_utils.local_string, kodi_utils.unquote, kodi_utils.unquote_plus, kodi_utils.numeric_input, kodi_utils.supported_media
json, set_property, notification, select_dialog, list_dirs = kodi_utils.json, kodi_utils.set_property, kodi_utils.notification, kodi_utils.select_dialog, kodi_utils.list_dirs
string, translate_path, empty_poster, int_window_prop = str, kodi_utils.translate_path, kodi_utils.empty_poster, kodi_utils.int_window_prop
exclude_list = ['furk', 'easynews', 'gdrive', 'library', 'filepursuit', 'plexshare']
RES_4K = ('.4k', 'hd4k', '4khd', '.uhd', 'ultrahd', 'ultra.hd', 'hd2160', '2160hd', '2160', '2160p', '216o', '216op')
RES_1080 = ('1080', '1080p', '1080i', 'hd1080', '1080hd', 'hd1080p', 'm1080p', 'fullhd', 'full.hd', '1o8o', '1o8op', '108o', '108op', '1o80', '1o80p')
RES_720 = ('720', '720p', '720i', 'hd720', '720hd', 'hd720p', '72o', '72op')
CAM = ('.cam.', 'camrip', 'hdcam', '.hd.cam', 'hqcam', '.hq.cam', 'cam.rip', 'dvdcam')
SCR = ('.scr.', 'screener', 'dvdscr', 'dvd.scr', '.r5', '.r6')
TELE = ('.tc.', '.ts.', 'tsrip', 'hdts', 'hdtc', '.hd.tc', 'dvdts', 'telesync', 'tele.sync', 'telecine', 'tele.cine')
VIDEO_3D = ('.3d.', '.sbs.', '.hsbs', 'sidebyside', 'side.by.side', 'stereoscopic', '.tab.', '.htab.', 'topandbottom', 'top.and.bottom')
DOLBY_VISION = ('dolby.vision', 'dolbyvision', '.dovi.', '.dv.')
HDR = ('2160p.bluray.hevc.truehd', '2160p.bluray.hevc.dts', '2160p.bluray.hevc.lpcm', '2160p.blu.ray.hevc.truehd', '2160p.blu.ray.hevc.dts', '2160p.uhd.bluray',
		'2160p.uhd.blu.ray', '2160p.us.bluray.hevc.truehd', '2160p.us.bluray.hevc.dts', '.hdr.', 'hdr10', 'hdr.10', 'uhd.bluray.2160p', 'uhd.blu.ray.2160p')
HDR_TRUE = ('.hdr.', 'hdr10', 'hdr.10')
CODEC_H264 = ('avc', 'h264', 'h.264', 'x264', 'x.264')
CODEC_H265 = ('h265', 'h.265', 'hevc', 'x265', 'x.265')
CODEC_XVID = ('xvid', '.x.vid')
CODEC_DIVX = ('divx', 'div2', 'div3', 'div4')
CODEC_MPEG = ('.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.mp4', '.m4p', '.m4v', 'msmpeg', 'mpegurl')
CODEC_MKV = ('.mkv', 'matroska')
REMUX = ('remux', 'bdremux')
BLURAY = ('bluray', 'blu.ray', 'bdrip', 'bd.rip')
DVD = ('dvdrip', 'dvd.rip')
WEB = ('.web.', 'webdl', 'web.dl', 'web-dl', 'webrip', 'web.rip')
HDRIP = ('.hdrip', '.hd.rip')
DOLBY_TRUEHD = ('true.hd', 'truehd')
DOLBY_DIGITALPLUS = ('dolby.digital.plus', 'dolbydigital.plus', 'dolbydigitalplus', 'dd.plus.', 'ddplus', '.ddp.', 'ddp2', 'ddp5', 'ddp7', 'eac3', '.e.ac3')
DOLBY_DIGITALEX = ('.dd.ex.', 'ddex', 'dolby.ex.', 'dolby.digital.ex.', 'dolbydigital.ex.')
DOLBYDIGITAL = ('dd2.', 'dd5', 'dd7', 'dolby.digital', 'dolbydigital', '.ac3', '.ac.3.', '.dd.')
DTSX = ('.dts.x.', 'dtsx')
DTS_HDMA = ('hd.ma', 'hdma')
DTS_HD = ('dts.hd.', 'dtshd')
AUDIO_8CH = ('ch8.', '8ch.', '7.1ch', '7.1.')
AUDIO_7CH = ('ch7.', '7ch.', '6.1ch', '6.1.')
AUDIO_6CH = ('ch6.', '6ch.', '5.1ch', '5.1.')
AUDIO_2CH = ('ch2', '2ch', '2.0ch', '2.0.', 'audio.2.0.', 'stereo')
SUBS = ('subita', 'subfrench', 'subspanish', 'subtitula', 'swesub', 'nl.subs', 'subbed')
ADS = ('1xbet', 'betwin')
MULTI_LANG = ('hindi.eng', 'ara.eng', 'ces.eng', 'chi.eng', 'cze.eng', 'dan.eng', 'dut.eng', 'ell.eng', 'esl.eng', 'esp.eng', 'fin.eng', 'fra.eng', 'fre.eng',
			'frn.eng', 'gai.eng', 'ger.eng', 'gle.eng', 'gre.eng', 'gtm.eng', 'heb.eng', 'hin.eng', 'hun.eng', 'ind.eng', 'iri.eng', 'ita.eng', 'jap.eng', 'jpn.eng',
			'kor.eng', 'lat.eng', 'lebb.eng', 'lit.eng', 'nor.eng', 'pol.eng', 'por.eng', 'rus.eng', 'som.eng', 'spa.eng', 'sve.eng', 'swe.eng', 'tha.eng', 'tur.eng',
			'uae.eng', 'ukr.eng', 'vie.eng', 'zho.eng', 'dual.audio', 'multi')
EXTRAS = ('sample', 'extra', 'extras', 'deleted', 'unused', 'footage', 'inside', 'blooper', 'bloopers', 'making.of', 'feature', 'featurette', 'behind.the.scenes', 'trailer')
UNWANTED_TAGS = ('tamilrockers.com', 'www.tamilrockers.com', 'www.tamilrockers.ws', 'www.tamilrockers.pl', 'www-tamilrockers-cl', 'www.tamilrockers.cl', 'www.tamilrockers.li',
				'www.tamilrockerrs.pl', 'www.tamilmv.bid', 'www.tamilmv.biz', 'www.1tamilmv.org', 'gktorrent-bz', 'gktorrent-com', 'www.torrenting.com', 'www.torrenting.org',
				'www-torrenting-com', 'www-torrenting-org', 'katmoviehd.pw', 'katmoviehd-pw', 'www.torrent9.nz', 'www-torrent9-uno', 'torrent9-cz', 'torrent9.cz',
				'agusiq-torrents-pl', 'oxtorrent-bz', 'oxtorrent-com', 'oxtorrent.com', 'oxtorrent-sh', 'oxtorrent-vc', 'www.movcr.tv', 'movcr-com', 'www.movcr.to', '(imax)',
				'imax', 'xtorrenty.org', 'nastoletni.wilkoak', 'www.scenetime.com', 'kst-vn', 'www.movierulz.vc', 'www-movierulz-ht', 'www.2movierulz.ac', 'www.2movierulz.ms',
				'www.3movierulz.com', 'www.3movierulz.tv', 'www.3movierulz.ws', 'www.3movierulz.ms', 'www.7movierulz.pw', 'www.8movierulz.ws', 'mkvcinemas.live', 'www.bludv.tv',
				'ramin.djawadi', 'extramovies.casa', 'extramovies.wiki', '13+', '18+', 'taht.oyunlar', 'crazy4tv.com', 'karibu', '989pa.com', 'best-torrents-net', '1-3-3-8.com',
				'ssrmovies.club', 'va:', 'zgxybbs-fdns-uk', 'www.tamilblasters.mx', 'www.1tamilmv.work', 'www.xbay.me', 'crazy4tv-com', '(es)')
def_host_dict = ['flashbit.cc', 'flashx.co', 'mega.nz', 'uploadfiles.eu', 'pandafiles.com', 'file4safe.com', 'nowvideo.club', 'flashx.pw', 'piecejointe.net', 'ulozto.sk',
				'turbobit.cc', 'k2s.cc', 'mixdrop.sx', 'uloz.to', 'tenvoi.com', 'clicknupload.cc', 'filefox.cc', 'soundcloud.com', 'vidto-do.com', 'clicknupload.com',
				'filefactory.com', 'catshare.net', 'mixloads.com', 'ul.to', 'worldbytez.com', 'vidoza.org', 'nitroflare.com', 'letsupload.to', 'voeunblck.com',
				'adblockeronstreamtape.com', 'voe-un-block.com', 'wupfile.com', 'vk.com', 'uploader.link', 'nowvideo.pw', 'dailymotion.com', 'uploaded.net', 'rapidgator.asia',
				'uploaded.to', 'megadl.fr', 'nitro.download', 'katfile.com', 'bdupload.asia', 'streamon.to', 'voeunblock1.com', 'reputationsheriffkennethsand.com',
				'docs.google.com', 'isrbx.net', 'dropgalaxy.in', 'hexupload.net', '9xupload.asia', 'uploadgig.com', 'filedot.xyz', 'uploadcloud.pro', 'vivo.sx', 'keep2share.cc',
				'uploadev.org', 'youtube.com', 'hotlink.cc', 'ulozto.net', 'upstore.net', '9xupload.info', 'upstream.to', 'letsupload.io', 'filerio.in', 'playvidto.com',
				'ulozto.cz', 'voe-unblock.com', 'vidoza.net', 'tezfiles.com', 'yodbox.com', 'clicknupload.to', 'apkadmin.com', 'inclouddrive.com', 'fastclick.to', 'oboom.com',
				'uploadbox.io', 'wipfiles.net', 'harefile.com', 'dl4free.com', 'turbobit.net', 'filesabc.com', 'cloudvideo.tv', 'anzfile.net', 'launchreliantcleaverriver.com',
				'indishare.me', 'di.fm', 'feurl.com', 'rapidu.net', 'speed-down.org', 'voeunblock.com', 'fastbit.cc', 'archive.org', 'rutube.ru', 'clipwatching.com',
				'clicknupload.club', 'down.fast-down.com', 'israbox-music.org', 'fileaxa.com', 'mega4upload.com', 'dfiles.ru', 'uptobox.com', 'ubiqfile.com', 'flashx.bz',
				'flashx.cc', 'fshare.vn', 'strcloud.link', 'uploadrar.com', 'voeunbl0ck.com', 'voeun-block.net', 'upbam.org', 'cosmobox.org', 'example.net', '4shared.com',
				'highstream.tv', 'un-block-voe.net', 'drop.download', 'fboom.me', 'filestore.to', 'dfichiers.com', 'jazzradio.com', 'wayupload.com', 'gigapeta.com', '1fichier.com',
				'fastfile.cc', 'vivo.st', 'turb.pw', 'mp4upload.com', 'turbobit5.net', 'mixdrop.club', 'file.al', 'uploadev.com', 'audaciousdefaulthouse.com', 'thevideo.me',
				'vipfile.cc', 'rapidrar.com', 'tvad.me', 'depositfiles.org', 'voe.sx', 'alfafile.net', 'hitf.to', 'upload-4ever.com', 'ddownload.com', 'youporn.com', 'mexa.sh',
				'earn4files.com', 'uploadc.com', '2shared.com', 'sky.fm', 'radiotunes.com', 'strcloud.sx', 'solidfiles.com', 'turbo.to', 'mega4up.org', 'k2share.cc', 'hitf.cc',
				'rg.to', 'sendit.cloud', 'v-o-e-unblock.com', 'dropapk.com', 'rapidfileshare.net', 'voeunblock2.com', 'mesfichiers.org', 'cornfile.com', 'uploadc.ch',
				'upload42.com', 'dailyuploads.net', 'bayfiles.com', 'btafile.com', 'turb.to', '4downfiles.org', 'filer.net', 'uploadmx.com', 'uploadboy.me', 'userscloud.com',
				'zachowajto.pl', 'datafilehost.com', 'classicalradio.com', 'fireget.com', 'world-files.com', 'mexashare.com', 'nelion.me', 'tusfiles.net', 'rockfile.co',
				'uploadbank.com', 'salefiles.com', 'unibytes.com', 'goloady.com', 'drive.google.com', 'modsbase.com', 'rarefile.net', 'vev.io', 'hitfile.net', 'uptostream.com',
				'daofile.com', 'dfiles.eu', 'userupload.net', 'turbobit.pw', 'turbobit.cloud', 'cjoint.net', 'clicknupload.me', 'file-up.org', 'flashx.tv', 'clicknupload.co',
				'backin.net', 'filerio.com', 'hulkshare.com', 'keep2s.cc', 'icerbox.com', 'hot4share.com', 'douploads.net', 'clicknupload.link', 'redbunker.net', 'thevideo.io',
				'israbox.ch', 'vidcloud.co', 'vimeo.com', 'thevideo.website', 'fileup.cc', 'letsupload.cc', 'turb.cc', 'desfichiers.com', 'tusfiles.com', 'uppit.com',
				'file-upload.com', 'up-load.io', 'letsupload.co', 'extmatrix.com', 'dropapk.to', 'rapidgator.net', 'load.to', 'pjointe.com', 'voeunblk.com', 'prefiles.com',
				'turbo-bit.net', 'europeup.com', 'vidlox.tv', 'mediafire.com', 'wdupload.com', 'ddl.to', 'simfileshare.net', 'vidtodo.com', 'sharemods.com', 'sendspace.com',
				'voe-unblock.net', 'streamtape.com', 'mixdrop.co', 'pornfile.cz', 'alldebrid.com', 'mega.co.nz', 'scribd.com', 'rockfile.eu', 'faststore.org', 'redtube.com',
				'vidcloud.ru', 'xubster.com', 'example.com', 'florenfile.com', 'dl.free.fr', 'brupload.net', 'easybytez.com', 'bdupload.in', 'depositfiles.com', 'down.mdiaload.com',
				'uploadydl.com', 'clicknupload.org', 'videobin.co', 'wushare.com', 'zippyshare.com', 'isra.cloud', 'gulf-up.com', 'ex-load.com', 'letsupload.org', 'exload.com',
				'uploadboy.com', 'alterupload.com', 'mixdrop.to', 'flashx.ws', 'fileupload.pw', 'gounlimited.to', 'usersdrive.com', 'filespace.com', 'filenext.com', 'ninjastream.to',
				'takefile.link', 'filezip.cc', 'heroupload.com', 'vidoza.co', 'real-debrid.com', 'transfert.free.fr']

def internal_sources(active_sources, prescrape=False):
	def import_info():
		for item in files:
			try:
				module_name = item.split('.')[0]
				if module_name in ('__init__', 'external', 'folders'): continue
				if module_name not in active_sources: continue
				if prescrape and not check_prescrape_sources(module_name): continue
				module = manual_function_import('scrapers.%s' % module_name, 'source')
				yield ('internal', module, module_name)
			except: pass
	files = list_dirs(translate_path('special://home/addons/plugin.video.fen/resources/lib/scrapers'))[1]
	try: sourceDict = list(import_info())
	except: sourceDict = []
	return sourceDict

def external_sources(ret_all=False, ret_default_only=False):
	def import_info():
		for source_folder, files in all_sources:
			for item in files:
				module_name = item.split('.')[0]
				if module_name == '__init__': continue
				if module_name in exclude_list: continue
				if not ret_all:
					if default_providers:
						if not module_name in default_providers: continue
					elif not coco_getSetting('provider.' + module_name) == 'true': continue
				module = manual_function_import('cocoscrapers.sources_cocoscrapers.%s.%s' % (source_folder, module_name), 'source')
				yield (module_name, module)
	default_providers = get_external_default_providers() if (ret_default_only and not ret_all) else None
	all_sources = sources_cocoscrapers.total_providers.items()
	try: sourceDict = list(import_info())
	except: sourceDict = []
	return sourceDict

def get_external_default_providers():
	return [k.split('.')[1] for k, v in coco_default_providers().items() if v == 'true']

def internal_folders_import(folders):
	def import_info():
		for item in folders:
			scraper_name = item[0]
			module = manual_function_import('scrapers.folders', 'source')
			yield ('folders', (module, (item[1], scraper_name)), scraper_name)
	sourceDict = list(import_info())
	try: sourceDict = list(import_info())
	except: sourceDict = []
	return sourceDict

def get_aliases_titles(aliases):
	try: result = [i['title'] for i in aliases]
	except: result = []
	return result

def make_alias_dict(meta, title):
	aliases = []
	alternative_titles = meta.get('alternative_titles', [])
	original_title = meta['original_title']
	country_codes = set([i.replace('GB', 'UK') for i in meta.get('country_codes', [])])
	if alternative_titles: aliases = [{'title': i, 'country': ''} for i in alternative_titles]
	if original_title not in alternative_titles: aliases.append({'title': original_title, 'country': ''})
	if country_codes: aliases.extend([{'title': '%s %s' % (title, i), 'country': ''} for i in country_codes])
	return aliases

def internal_results(provider, sources):
	set_property(int_window_prop % provider, json.dumps(sources))

def normalize(title):
	import unicodedata
	try:
		title = ''.join(c for c in unicodedata.normalize('NFKD', title) if unicodedata.category(c) != 'Mn')
		return string(title)
	except: return title

def _ext_scrapers_notice(status):
	notification(status, 2500)

def toggle_all(folder, setting, silent=False):
	try:
		sourcelist = scraper_names(folder)
		for i in sourcelist: coco_setSetting('provider.%s' % i, setting)
		if silent: return
		return _ext_scrapers_notice(32576)
	except:
		if silent: return
		return _ext_scrapers_notice(32574)

def enable_disable(folder):
	try:
		icon = translate_path('special://home/addons/script.module.cocoscrapers/icon.png')
		enabled, disabled = scrapers_status(folder)
		all_sources = sorted(enabled + disabled)
		preselect = [all_sources.index(i) for i in enabled]
		list_items = [{'line1': i.upper(), 'icon': icon} for i in all_sources]
		kwargs = {'items': json.dumps(list_items), 'heading': ls(32036), 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
		chosen = select_dialog(all_sources, **kwargs)
		if chosen == None: return
		for i in all_sources:
			if i in chosen: coco_setSetting('provider.%s' % i, 'true')
			else: coco_setSetting('provider.' + i, 'false')
		return _ext_scrapers_notice(32576)
	except: return _ext_scrapers_notice(32574)

def set_default_scrapers():
	coco_set_defaults()

def scrapers_status(folder='all'):
	providers = scraper_names(folder)
	enabled = [i for i in providers if coco_getSetting('provider.%s' % i) == 'true']
	disabled = [i for i in providers if i not in enabled]
	return enabled, disabled

def scraper_names(folder):
	if folder == 'torrents': return [i for i in sources_cocoscrapers.torrent_providers if not i in exclude_list]
	elif folder == 'hosters': return [i for i in sources_cocoscrapers.hoster_providers if not i in exclude_list]
	else: return [i for i in sources_cocoscrapers.all_providers if not i in exclude_list]

def pack_enable_check(meta, season, episode):
	try:
		status = meta['extra_info']['status']
		if status in ('Ended', 'Canceled'): return True, True
		adjust_hours, current_date, meta_user_info = date_offset(), get_datetime(), metadata_user_info()
		episodes_data = season_episodes_meta(season, meta, meta_user_info)
		unaired_episodes = [adjust_premiered_date(i['premiered'], adjust_hours)[0] for i in episodes_data]
		if None in unaired_episodes or any(i > current_date for i in unaired_episodes): return False, False
		else: return True, False
	except: pass
	return False, False

def clear_scrapers_cache(silent=False):
	from caches import clear_cache
	for item in ('internal_scrapers', 'external_scrapers'): clear_cache(item, silent=True)
	if not silent: notification(32576)

def supported_video_extensions():
	supported_video_extensions = supported_media().split('|')
	return [i for i in supported_video_extensions if not i in ('','.zip')]

def seas_ep_filter(season, episode, release_title, split=False, return_match=False):
	str_season, str_episode = string(season), string(episode)
	season_fill, episode_fill = str_season.zfill(2), str_episode.zfill(2)
	str_ep_plus_1, str_ep_minus_1 = string(episode+1), string(episode-1)
	release_title = re.sub(r'[^A-Za-z0-9-]+', '.', unquote(release_title).replace('\'', '')).lower()
	string1 = r'(s<<S>>[.-]?e[p]?[.-]?<<E>>[.-])'
	string2 = r'(season[.-]?<<S>>[.-]?episode[.-]?<<E>>[.-])|([s]?<<S>>[x.]<<E>>[.-])'
	string3 = r'(s<<S>>e<<E1>>[.-]?e?<<E2>>[.-])'
	string4 = r'([.-]<<S>>[.-]?<<E>>[.-])'
	string_list = []
	string_list_append = string_list.append
	string_list_append(string1.replace('<<S>>', season_fill).replace('<<E>>', episode_fill))
	string_list_append(string1.replace('<<S>>', str_season).replace('<<E>>', episode_fill))
	string_list_append(string1.replace('<<S>>', season_fill).replace('<<E>>', str_episode))
	string_list_append(string1.replace('<<S>>', str_season).replace('<<E>>', str_episode))
	string_list_append(string2.replace('<<S>>', season_fill).replace('<<E>>', episode_fill))
	string_list_append(string2.replace('<<S>>', str_season).replace('<<E>>', episode_fill))
	string_list_append(string2.replace('<<S>>', season_fill).replace('<<E>>', str_episode))
	string_list_append(string2.replace('<<S>>', str_season).replace('<<E>>', str_episode))
	string_list_append(string3.replace('<<S>>', season_fill).replace('<<E1>>', str_ep_minus_1.zfill(2)).replace('<<E2>>', episode_fill))
	string_list_append(string3.replace('<<S>>', season_fill).replace('<<E1>>', episode_fill).replace('<<E2>>', str_ep_plus_1.zfill(2)))
	string_list_append(string4.replace('<<S>>', season_fill).replace('<<E>>', episode_fill))
	string_list_append(string4.replace('<<S>>', str_season).replace('<<E>>', episode_fill))
	final_string = '|'.join(string_list)
	reg_pattern = re.compile(final_string)
	if split: return release_title.split(re.search(reg_pattern, release_title).group(), 1)[1]
	elif return_match: return re.search(reg_pattern, release_title).group()
	else: return bool(re.search(reg_pattern, release_title))

def find_season_in_release_title(release_title):
	release_title = re.sub(r'[^A-Za-z0-9-]+', '.', unquote(release_title).replace('\'', '')).lower()
	match = None
	regex_list = [r's(\d+)', r's\.(\d+)', r'(\d+)x', r'(\d+)\.x', r'season(\d+)', r'season\.(\d+)']
	for item in regex_list:
		try:
			match = re.search(item, release_title)
			if match:
				match = int(string(match.group(1)).lstrip('0'))
				break
		except: pass
	return match

def check_title(title, release_title, aliases, year, season, episode):
	try:
		all_titles = [title]
		if aliases: all_titles += aliases
		cleaned_titles = []
		cleaned_titles_append = cleaned_titles.append
		year = string(year)
		for i in all_titles:
			cleaned_titles_append(
				i.lower().replace('\'', '').replace(':', '').replace('!', '').replace('(', '').replace(')', '').replace('&', 'and').replace(' ', '.').replace(year, ''))
		release_title = strip_non_ascii_and_unprintable(release_title).lstrip('/ ').replace(' ', '.').replace(':', '.').lower()
		releasetitle_startswith = release_title.startswith
		for i in UNWANTED_TAGS:
			if releasetitle_startswith(i):
				i_startswith = i.startswith
				pattern = r'\%s' % i if i_startswith('[') or i_startswith('+') else r'%s' % i
				release_title = re.sub(r'^%s' % pattern, '', release_title, 1, re.I)
		release_title = release_title.lstrip('.-:/')
		release_title = re.sub(r'^\[.*?]', '', release_title, 1, re.I)
		release_title = release_title.lstrip('.-[](){}:/')
		if season:
			if season == 'pack': hdlr = ''
			else:
				try: hdlr = seas_ep_filter(season, episode, release_title, return_match=True)
				except: return False
		else: hdlr = year
		if hdlr:
			release_title = release_title.split(hdlr.lower())[0]
			release_title = release_title.replace(year, '').replace('(', '').replace(')', '').replace('&', 'and').rstrip('.-').rstrip('.').rstrip('-').replace(':', '')
			if not any(release_title == i for i in cleaned_titles): return False
		else:
			release_title = release_title.replace(year, '').replace('(', '').replace(')', '').replace('&', 'and').rstrip('.-').rstrip('.').rstrip('-').replace(':', '')
			if not any(i in release_title for i in cleaned_titles): return False
		return True
	except: return True

def strip_non_ascii_and_unprintable(text):
	try:
		result = ''.join(char for char in text if char in printable)
		return result.encode('ascii', errors='ignore').decode('ascii', errors='ignore')
	except: pass
	return text

def release_info_format(release_title):
	try:
		release_title = url_strip(release_title)
		release_title = release_title.lower().replace("'", "").lstrip('.').rstrip('.')
		fmt = '.%s.' % re.sub(r'[^a-z0-9-~]+', '.', release_title).replace('.-.', '.').replace('-.', '.').replace('.-', '.').replace('--', '.')
		return fmt
	except:
		return release_title.lower()

def clean_title(title):
	try:
		if not title: return
		title = title.lower()
		title = re.sub(r'&#(\d+);', '', title)
		title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = re.sub(r'(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
		title = title.replace('&quot;', '\"').replace('&amp;', '&')
		title = re.sub(r'\n|([\[({].+?[})\]])|([:;–\-"\',!_.?~$@])|\s', '', title)
	except: pass
	return title

def get_release_quality(release_info):
	if any(i in release_info for i in SCR): return 'SCR'
	if any(i in release_info for i in CAM): return 'CAM'
	if any(i in release_info for i in TELE): return 'TELE'
	if any(i in release_info for i in RES_4K): return '4K'
	if any(i in release_info for i in RES_1080): return '1080p'
	if any(i in release_info for i in RES_720): return '720p'
	return 'SD'

def url_strip(url):
	try:
		url = unquote_plus(url)
		if 'magnet:' in url: url = url.split('&dn=')[1]
		url = url.lower().replace("'", "").lstrip('.').rstrip('.')
		fmt = re.sub(r'[^a-z0-9]+', ' ', url)
		if 'http' in fmt: return None
		if fmt == '': return None
		return fmt
	except: return None

def get_file_info(name_info=None, url=None):
	# thanks 123Venom and gaiaaaiaai, whom I knicked most of this code from. :)
	fmt = None
	info = []
	info_append = info.append
	if name_info: fmt = name_info
	elif url: fmt = url_strip(url)
	if not fmt: return ''
	quality = get_release_quality(fmt)
	if any(i in fmt for i in VIDEO_3D):  info_append('[B]3D[/B]')
	if '.sdr' in fmt: info_append('SDR')
	elif any(i in fmt for i in DOLBY_VISION): info_append('[B]D/VISION[/B]')
	elif any(i in fmt for i in HDR): info_append('[B]HDR[/B]')
	elif all(i in fmt for i in ('2160p', 'remux')): info_append('[B]HDR[/B]')
	if '[B]D/VISION[/B]' in info:
		if any(i in fmt for i in HDR_TRUE) or 'hybrid' in fmt: info_append('[B]HDR[/B]')
		if '[B]HDR[/B]' in info: info_append('[B]HYBRID[/B]')
	if any(i in fmt for i in CODEC_H264): info_append('AVC')
	elif '.av1.' in fmt: info_append('[B]AV1[/B]')
	elif any(i in fmt for i in CODEC_H265): info_append('[B]HEVC[/B]')
	elif any(i in info for i in ('[B]HDR[/B]', '[B]D/VISION[/B]')): info_append('[B]HEVC[/B]')
	elif any(i in fmt for i in CODEC_XVID): info_append('XVID')
	elif any(i in fmt for i in CODEC_DIVX): info_append('DIVX')
	if any(i in fmt for i in REMUX): info_append('REMUX')
	if any(i in fmt for i in BLURAY): info_append('BLURAY')
	elif any(i in fmt for i in DVD): info_append('DVD')
	elif any(i in fmt for i in WEB): info_append('WEB')
	elif 'hdtv' in fmt: info_append('HDTV')
	elif 'pdtv' in fmt: info_append('PDTV')
	elif any(i in fmt for i in HDRIP): info_append('HDRIP')
	if 'atmos' in fmt: info_append('ATMOS')
	if any(i in fmt for i in DOLBY_TRUEHD): info_append('TRUEHD')
	if any(i in fmt for i in DOLBY_DIGITALPLUS): info_append('DD+')
	elif any(i in fmt for i in DOLBY_DIGITALEX): info_append('DD-EX')
	elif any(i in fmt for i in DOLBYDIGITAL): info_append('DD')
	if 'aac' in fmt: info_append('AAC')
	elif 'mp3' in fmt: info_append('MP3')
	elif '.flac.' in fmt: info_append('FLAC')
	elif 'opus' in fmt and not fmt.endswith('opus.'): info_append('OPUS')
	if any(i in fmt for i in DTSX): info_append('DTS-X')
	elif any(i in fmt for i in DTS_HDMA): info_append('DTS-HD MA')
	elif any(i in fmt for i in DTS_HD): info_append('DTS-HD')
	elif '.dts' in fmt: info_append('DTS')
	if any(i in fmt for i in AUDIO_8CH): info_append('8CH')
	elif any(i in fmt for i in AUDIO_7CH): info_append('7CH')
	elif any(i in fmt for i in AUDIO_6CH): info_append('6CH')
	elif any(i in fmt for i in AUDIO_2CH): info_append('2CH')
	if '.wmv' in fmt: info_append('WMV')
	elif any(i in fmt for i in CODEC_MPEG): info_append('MPEG')
	elif '.avi' in fmt: info_append('AVI')
	elif any(i in fmt for i in CODEC_MKV): info_append('MKV')
	if any(i in fmt for i in MULTI_LANG): info_append('MULTI-LANG')
	if any(i in fmt for i in ADS): info_append('ADS')
	if any(i in fmt for i in SUBS): info_append('SUBS')
	info = ' | '.join(filter(None, info))
	return quality, info

def get_cache_expiry(media_type, meta, season):
	try:
		current_date = get_datetime()
		if media_type == 'movie':
			premiered = jsondate_to_datetime(meta['premiered'], '%Y-%m-%d', remove_time=True)
			difference = subtract_dates(current_date, premiered)
			if difference == 0: single_expiry = int(24*0.125)
			elif difference <= 7: single_expiry = 24*1
			elif difference <= 14: single_expiry = 24*2
			elif difference <= 21: single_expiry = 24*3
			elif difference <= 30: single_expiry = 24*4
			elif difference <= 60: single_expiry = 24*7
			else: single_expiry = 24*14
			season_expiry, show_expiry = 0, 0
		else:
			recently_ended = False
			extra_info = meta['extra_info']
			ended = extra_info['status'] in ('Ended', 'Canceled')
			premiered = adjust_premiered_date(meta['premiered'], date_offset())[0]
			difference = subtract_dates(current_date, premiered)
			last_episode_to_air = jsondate_to_datetime(extra_info['last_episode_to_air']['air_date'], '%Y-%m-%d', remove_time=True)
			last_ep_difference = subtract_dates(current_date, last_episode_to_air)
			if ended and last_ep_difference <= 14: recently_ended = True
			if not ended or recently_ended:
				if difference == 0: single_expiry = int(24*0.125)
				elif difference <= 3: single_expiry = 24*1
				elif difference <= 7: single_expiry = 24*3
				else: single_expiry = 24*7
				if meta['total_seasons'] == season:
					if last_ep_difference <= 7: season_expiry = 24*3
					else: season_expiry = 24*10
				else: season_expiry = 24*30
				show_expiry = 24*10
			else: single_expiry, season_expiry, show_expiry = 24*10, 24*30, 24*30
	except: single_expiry, season_expiry, show_expiry = 24*3, 24*3, 24*10
	return single_expiry, season_expiry, show_expiry