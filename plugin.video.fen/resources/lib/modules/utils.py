# -*- coding: utf-8 -*-
import re
import time
import copy
import random
import hashlib
import unicodedata
import _strptime  # fix bug in python import
from base64 import b32decode
from html.parser import HTMLParser
from importlib import import_module
from datetime import datetime, timedelta, date
from modules.settings_reader import get_setting
from modules.kodi_utils import local_string
from modules.kodi_utils import logger

def manual_function_import(location, function_name):
	return getattr(import_module(location), function_name)

def make_thread_list(_target, _list, _thread):
	for item in _list:
		threaded_object = _thread(target=_target, args=(item,))
		threaded_object.start()
		yield threaded_object

def make_thread_list_enumerate(_target, _list, _thread):
	for item_position, item in enumerate(_list):
		threaded_object = _thread(target=_target, args=(item_position, item))
		threaded_object.start()
		yield threaded_object

def chunks(item_list, limit):
	"""
	Yield successive limit-sized chunks from item_list.
	"""
	for i in range(0, len(item_list), limit):
		yield item_list[i:i + limit]

def string_to_float(string, default_return):
	"""
	Remove all alpha from string and return a float.
	Returns float of "default_return" upon ValueError.
	"""
	try: return float(''.join(c for c in string if (c.isdigit() or c =='.')))
	except ValueError: return float(default_return)

def string_alphanum_to_num(string):
	"""
	Remove all alpha from string and return remaining string.
	Returns original string upon ValueError.
	"""
	try: return ''.join(c for c in string if c.isdigit())
	except ValueError: return string

def base32_to_hex(_hash):
	try: _hex = b32decode(_hash).hex()
	except: _hex = None
	return _hex

def jsondate_to_datetime(jsondate_object, resformat, remove_time=False):
	if remove_time: datetime_object = datetime_workaround(jsondate_object, resformat).date()
	else: datetime_object = datetime_workaround(jsondate_object, resformat)
	return datetime_object

def get_datetime(string=False, dt=False):
	d = datetime.now()
	if dt: return d
	if string: return d.strftime('%Y-%m-%d')
	return datetime.date(d)
	
def adjust_premiered_date(orig_date, adjust_hours):
	if not orig_date: return None, None
	orig_date += ' 20:00:00'
	datetime_object = jsondate_to_datetime(orig_date, '%Y-%m-%d %H:%M:%S')
	adjusted_datetime = datetime_object + timedelta(hours=adjust_hours)
	adjusted_string = adjusted_datetime.strftime('%Y-%m-%d')
	return adjusted_datetime.date(), adjusted_string

def make_day(today, date, date_format, use_words=True):
	day_diff = (date - today).days
	try: day = date.strftime(date_format)
	except ValueError: day = date.strftime('%Y-%m-%d')
	if use_words:
		if day_diff == -1: day = local_string(32848).upper()
		elif day_diff == 0: day = local_string(32849).upper()
		elif day_diff == 1: day = local_string(32850).upper()
		elif 1 < day_diff < 7: day = local_string(translate_day(date.strftime('%A').upper()))
	return day

def datetime_workaround(data, str_format):
	try: datetime_object = datetime.strptime(data, str_format)
	except: datetime_object = datetime(*(time.strptime(data, str_format)[0:6]))
	return datetime_object

def translate_day(day):
	days = {'MONDAY': 32971, 'TUESDAY': 32972, 'WEDNESDAY': 32973, 'THURSDAY': 32974, 'FRIDAY': 32975, 'SATURDAY': 32976, 'SUNDAY': 32977}
	return days[day]

def date_difference(current_date, compare_date, difference_tolerance, allow_postive_difference=False):
	try:
		difference = current_date - compare_date
		difference = divmod(difference.total_seconds(), 86400)[0]
		if not allow_postive_difference and difference > 0: return False
		else: difference = abs(difference)
		if difference > difference_tolerance: return False
		return True
	except: return True

def calculate_age(born, str_format, died=None):
	''' born and died are str objects e.g. '1972-05-28' '''
	born = datetime_workaround(born, str_format)
	if not died: today = date.today()
	else: today = datetime_workaround(died, str_format)
	return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def batch_replace(s, replace_info):
	for r in replace_info:
		s = str(s).replace(r[0], r[1])
	return s

def clean_file_name(s, use_encoding=False, use_blanks=True):
	try:
		hex_entities = [['&#x26;', '&'], ['&#x27;', '\''], ['&#xC6;', 'AE'], ['&#xC7;', 'C'],
					['&#xF4;', 'o'], ['&#xE9;', 'e'], ['&#xEB;', 'e'], ['&#xED;', 'i'],
					['&#xEE;', 'i'], ['&#xA2;', 'c'], ['&#xE2;', 'a'], ['&#xEF;', 'i'],
					['&#xE1;', 'a'], ['&#xE8;', 'e'], ['%2E', '.'], ['&frac12;', '%BD'],
					['&#xBD;', '%BD'], ['&#xB3;', '%B3'], ['&#xB0;', '%B0'], ['&amp;', '&'],
					['&#xB7;', '.'], ['&#xE4;', 'A'], ['\xe2\x80\x99', '']]
		special_encoded = [['"', '%22'], ['*', '%2A'], ['/', '%2F'], [':', ','], ['<', '%3C'],
							['>', '%3E'], ['?', '%3F'], ['\\', '%5C'], ['|', '%7C']]
		
		special_blanks = [['"', ' '], ['/', ' '], [':', ''], ['<', ' '],
							['>', ' '], ['?', ' '], ['\\', ' '], ['|', ' '], ['%BD;', ' '],
							['%B3;', ' '], ['%B0;', ' '], ["'", ""], [' - ', ' '], ['.', ' '],
							['!', ''], [';', ''], [',', '']]
		s = batch_replace(s, hex_entities)
		if use_encoding: s = batch_replace(s, special_encoded)
		if use_blanks: s = batch_replace(s, special_blanks)
		s = s.strip()
	except: pass
	return s

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

def to_utf8(obj):
	try:
		if isinstance(obj, unicode):
			obj = obj.encode('utf-8', 'ignore')
		elif isinstance(obj, dict):
			obj = copy.deepcopy(obj)
			for key, val in obj.items():
				obj[key] = to_utf8(val)
		elif obj is not None and hasattr(obj, "__iter__"):
			obj = obj.__class__([to_utf8(x) for x in obj])
		else: pass
	except: pass
	return obj

def to_unicode(obj):
	try:
		if isinstance(obj, basestring):
			try: obj = unicode(obj, 'utf-8')
			except TypeError: pass
		elif isinstance(obj, dict):
			obj = copy.deepcopy(obj)
			for key, val in obj.items():
				obj[key] = to_unicode(val)
		elif obj is not None and hasattr(obj, "__iter__"):
			obj = obj.__class__([to_unicode(x) for x in obj])
		else: pass
	except: pass
	return obj

def byteify(data, ignore_dicts=False):
	try:
		if isinstance(data, unicode): return data.encode('utf-8')
		if isinstance(data, list): return [byteify(item, ignore_dicts=True) for item in data]
		if isinstance(data, dict) and not ignore_dicts:
			return dict([(byteify(key, ignore_dicts=True), byteify(value, ignore_dicts=True)) for key, value in data.iteritems()])
	except: pass
	return data

def normalize(txt):
	txt = re.sub(r'[^\x00-\x7f]',r'', txt)
	return txt

def safe_string(obj):
	try:
		try: return str(obj)
		except UnicodeEncodeError: return obj.encode('utf-8', 'ignore').decode('ascii', 'ignore')
		except: return ""
	except: return obj

def remove_accents(obj):
	try:
		try: obj = u'%s' % obj
		except: pass
		obj = ''.join(c for c in unicodedata.normalize('NFD', obj) if unicodedata.category(c) != 'Mn')
	except: pass
	return obj

def try_parse_int(string):
	try: return int(string)
	except: return 0

def regex_from_to(text, from_string, to_string, excluding=True):
	if excluding: r = re.search(r"(?i)" + from_string + r"([\S\s]+?)" + to_string, text).group(1)
	else: r = re.search(r"(?i)(" + from_string + r"[\S\s]+?" + to_string + ")", text).group(1)
	return r

def regex_get_all(text, start_with, end_with):
	r = re.findall(r"(?i)(" + start_with + r"[\S\s]+?" + end_with + ")", text)
	return r

def replace_html_codes(txt):
	txt = to_utf8(txt)
	txt = re.sub(r"(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
	txt = HTMLParser().unescape(txt)
	txt = txt.replace("&quot;", "\"")
	txt = txt.replace("&amp;", "&")
	return txt

def gen_file_hash(file):
	try:
		md5_hash = hashlib.md5()
		with open(file, 'rb') as afile:
			buf = afile.read()
			md5_hash.update(buf)
			return md5_hash.hexdigest()
	except: pass

def sec2time(sec, n_msec=3):
	''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
	if hasattr(sec,'__len__'): return [sec2time(s) for s in sec]
	m, s = divmod(sec, 60)
	h, m = divmod(m, 60)
	d, h = divmod(h, 24)
	if n_msec > 0: pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
	else: pattern = '%02d:%02d:%02d'
	if d == 0: return pattern % (h, m, s)
	return ('%d days, ' + pattern) % (d, h, m, s)

def released_key(item):
	if 'released' in item: return item['released']
	elif 'first_aired' in item: return item['first_aired']
	else: return 0

def title_key(title, ignore_articles):
	if not ignore_articles: return title
	try:
		if title is None: title = ''
		articles = ['the', 'a', 'an']
		match = re.match(r'^((\w+)\s+)', title.lower())
		if match and match.group(2) in articles: offset = len(match.group(1))
		else: offset = 0
		return title[offset:]
	except: return title

def sort_for_article(_list, _key, ignore_articles):
	if not ignore_articles: _list.sort(key=lambda k: k[_key])
	else: _list.sort(key=lambda k: re.sub(r'(^the |^a |^an )', '', k[_key].lower()))
	return _list
	
def sort_list(sort_key, sort_direction, list_data, ignore_articles):
	try:
		reverse = False if sort_direction == 'asc' else True
		if sort_key == 'rank': return sorted(list_data, key=lambda x: x['rank'], reverse=reverse)
		elif sort_key == 'added': return sorted(list_data, key=lambda x: x['listed_at'], reverse=reverse)
		elif sort_key == 'title': return sorted(list_data, key=lambda x: title_key(x[x['type']].get('title'), ignore_articles), reverse=reverse)
		elif sort_key == 'released': return sorted(list_data, key=lambda x: released_key(x[x['type']]), reverse=reverse)
		elif sort_key == 'runtime': return sorted(list_data, key=lambda x: x[x['type']].get('runtime', 0), reverse=reverse)
		elif sort_key == 'popularity': return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
		elif sort_key == 'percentage': return sorted(list_data, key=lambda x: x[x['type']].get('rating', 0), reverse=reverse)
		elif sort_key == 'votes': return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
		elif sort_key == 'random':
			return sorted(list_data, key=lambda k: random.random())
		else: return list_data
	except: return list_data

def imdb_sort_list():
	# From Exodus Codebase
	sort = int(get_setting('imdb_lists.sort_type'))
	sort_order = int(get_setting('imdb_lists.sort_direction'))
	if sort == 0: imdb_sort = 'list_order' # Default
	elif sort == 1: imdb_sort = 'alpha' # Alphabetical
	elif sort == 2: imdb_sort = 'user_rating' # IMDb Rating
	elif sort == 3: imdb_sort = 'moviemeter' # Popularity
	elif sort == 4: imdb_sort = 'your_rating' # Your Rating
	elif sort == 5: imdb_sort = 'num_votes' # Number Of Ratings
	elif sort == 6: imdb_sort = 'release_date' # Release Date
	elif sort == 7: imdb_sort = 'runtime' # Runtime
	elif sort == 8: imdb_sort = 'date_added' # Date Added
	imdb_sort_order = ',asc' if sort_order == 0 else ',desc'
	sort_string = imdb_sort + imdb_sort_order
	return sort_string
