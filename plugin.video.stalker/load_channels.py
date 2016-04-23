import sys
import urllib
import json
import os
import urlparse
import re, uuid
from time import time
from datetime import datetime
import math
import urllib2
import hashlib
from xml.dom import minidom



key = None;
mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()));
sn = None;
device_id = None;
device_id2 = None;
signature = None;
login = None;
password = None;

cache_version = '5'

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError, e:
    return False
  return True

  
def setMac(nmac):
	global mac;
	
	if re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", nmac.lower()):
		mac = nmac;

		
def setLogin(llogin,ppass):
	global login, password;
	
	login = llogin;
	password = ppass;
	
	
def setSerialNumber(serial):
	global sn, device_id, device_id2, signature, mac, login;

	if serial['send_serial'] == False:
		return;

	if serial['custom'] == False:

		sn = hashlib.md5(mac).hexdigest().upper()[13:];		
		device_id = hashlib.sha256(mac + sn + login).hexdigest().upper();
		device_id2 = hashlib.sha256(mac).hexdigest().upper();
		signature = hashlib.sha256(sn + mac).hexdigest().upper();
		
	elif serial['custom'] == True:

		sn = serial['sn'];
		device_id = serial['device_id'];
		device_id2 = serial['device_id2'];
		signature = serial['signature'];


def handshake(url):
	global key;

	values = {
		'type' : 'stb', 
		'action' : 'handshake',
		'JsHttpRequest' : '1-xml'}
	
	info = retrieveData(url, values)
		
	key = info['js']['token']
		
	return;
	

def getProfile(url):
	global sn, device_id, device_id2, signature;
	global key;
	
	
	values = {
		'type' : 'stb', 
		'action' : 'get_profile',
		'hd' : '1',
		'ver' : 'ImageDescription%3a%200.2.16-250%3b%20ImageDate%3a%2018%20Mar%202013%2019%3a56%3a53%20GMT%2b0200%3b%20PORTAL%20version%3a%204.9.9%3b%20API%20Version%3a%20JS%20API%20version%3a%20328%3b%20STB%20API%20version%3a%20134%3b%20Player%20Engine%20version%3a%200x566',
		'num_banks' : '1',
		'stb_type' : 'MAG250',
		'image_version' : '216',
		'auth_second_step' : '1',
		'hw_version' : '1.7-BD-00',
		'not_valid_token' : '1',
		'JsHttpRequest' : '1-xml' }

	if sn != None:
		values['sn'] = sn;
		values['device_id'] = device_id;
		values['device_id2'] = device_id2;
		values['signature'] = signature;

	info = retrieveData(url, values);


	return info;

	
def getAuth(url):
	global sn, device_id, device_id2, signature;
	global key, login, password;
	
	
	values = {
		'type' : 'stb', 
		'action' : 'do_auth',
		'login' : login,
		'password' : password,
		'JsHttpRequest' : '1-xml' }

	if sn != None:
		values['sn'] = sn;
		values['device_id'] = device_id;
		values['device_id2'] = device_id2;
		values['signature'] = signature;

	info = retrieveData(url, values);


	return info;
	
	
def retrieveData(url, values):
	global key, mac, login, password;

	url += '/stalker_portal'
	load = '/server/load.php'
	refer = '/c/'
	timezone = 'Europe%2FKiev';
	
	user_agent 	= 'Mozilla/5.0 (QtEmbedded; U; Linux; C) AppleWebKit/533.3 (KHTML, like Gecko) MAG200 stbapp ver: 4 rev: 1812 Mobile Safari/533.3';
	
	if key != None:
		headers 	= { 
			'User-Agent' : user_agent, 
			'Cookie' : 'mac=' + mac + '; stb_lang=en; timezone=' + timezone,			
			'Referer' : url + refer,
			'Accept-Charset' : 'UTF-8,*;q=0.8',
#			'Connection' : 'Keep-Alive',
			'X-User-Agent' : 'Model: MAG250; Link: WiFi',
			'Authorization' : 'Bearer ' + key 
			};
	
	else:
		headers 	= { 
			'User-Agent' : user_agent, 
			'Cookie' : 'mac=' + mac + '; stb_lang=en; timezone=' + timezone,
			'Referer' : url + refer,
			'Accept-Charset' : 'UTF-8,*;q=0.8',
#			'Connection' : 'Keep-Alive',
			'X-User-Agent' : 'Model: MAG250; Link: WiFi'
			};


	data = urllib.urlencode(values);
	
	req = urllib2.Request(url + load, data, headers);
	resp = urllib2.urlopen(req).read().decode("utf-8");

# check alternate
	if not is_json(resp) :

		req = urllib2.Request(url + load + '?' + data, headers=headers);
		resp = urllib2.urlopen(req).read().decode("utf-8");

	if not is_json(resp):
		raise Exception(resp)

	info = json.loads(resp)

	
	return info;


def getGenres(portal_mac, url, serial, portal_login, portal_password, path):	
	global key, cache_version, login, password;
	
	now = time();
	portalurl = "_".join(re.findall("[a-zA-Z0-9]+", url));
	portalurl = path + '/' + portalurl + '-genres';
	
	setMac(portal_mac);
	setLogin(portal_login, portal_password);
	setSerialNumber(serial);

	
	if not os.path.exists(path): 
		os.makedirs(path);
	
	if os.path.exists(portalurl):
		#check last time
		with open(portalurl) as data_file: data = json.load(data_file);
		
		if 'version' not in data or data['version'] != cache_version:
			clearCache(url, path);
			
		else:
			time_init = float(data['time']);
			# update 12h
			if ((now - time_init) / 3600) < 12:
				return data;
	
	handshake(url);
	getAuth(url);
	getProfile(url);

	values = {
		'type' : 'itv', 
		'action' : 'get_genres',
		'JsHttpRequest' : '1-xml'}
	
	info = retrieveData(url, values)
		
	results = info['js']
	
	data = '{ "version" : "' + cache_version + '", "time" : "' + str(now) + '", "genres" : {  \n'

	for i in results:
		alias 	= i["alias"]
		id 		= i["id"]
		title 	= i['title']
		data += '"'+ id +'" : {"alias":"'+ alias +'", "title":"'+ title +'"}, \n'

	data = data[:-3] + '\n}}'

	with open(portalurl, 'w') as f: f.write(data.encode('utf-8'));
	
	return json.loads(data.encode('utf-8'));

	
	
def getVoD(portal_mac, url, serial, portal_login, portal_password, portal_vodpages, path):	
	now = time();
	portalurl = "_".join(re.findall("[a-zA-Z0-9]+", url));
	portalurl = path + '/' + portalurl + '-vod';
	
	setMac(portal_mac);
	setLogin(portal_login, portal_password);
	setSerialNumber(serial);
	
	numpages = int(portal_vodpages);
	
	if not os.path.exists(path):
		os.makedirs(path)
	
	if os.path.exists(portalurl):
		#check last time
		with open(portalurl) as data_file: data = json.load(data_file);
	
		if 'version' not in data or data['version'] != cache_version:
			clearCache(url, path);
			
		else:
			time_init = float(data['time']);
			# update 168h (7 days)
			if ((now - time_init) / 3600) < 168:
				return data;

	handshake(url);
	getAuth(url);
	getProfile(url);
	
	data = '{ "version" : "' + cache_version + '", "time" : "' + str(now) + '", "vod" : [  \n'
	
	page = 1;
	pages = 0;
	total_items = 1.0;
	max_page_items = 1.0;
	
	while True:
		info = retrieveData(url, values = {
			'type' : 'vod', 
			'action' : 'get_ordered_list',
			'sortby' : 'added',
			'not_ended' : '0',
			'p' : page,
			'fav' : '0',
			'JsHttpRequest' : '1-xml'})
		
		total_items = float(info['js']['total_items']);
		max_page_items = float(info['js']['max_page_items']);
		pages = math.ceil(total_items/max_page_items);
		
		results = info['js']['data']
		
		for i in results:
			name 	= i["name"]
			cmd 	= i['cmd']
			if cmd.find("redirect/vodcached"):
				cmd = "ffmpeg /media/" + i["id"] + ".mpg";
			logo 	= i["screenshot_uri"]
			cat_id  = i["category_id"]
			genre_1 = i["genre_id_1"]
			genre_2 = i["genre_id_2"]
			genre_3 = i["genre_id_3"]
			genre_4 = i["genre_id_4"]			
			year    = i["year"]
			direct  = i["director"]
			mpaa    = i["rating_mpaa"]
			runtime = i["time"]
			rating  = i["rating_imdb"]
			country = i["country"]
		
			cast    = i["actors"]
			cast    = cast.replace('"',"-")			
			cast    = cast.replace("\r","")
			cast    = cast.replace("\n", "")			

			plot    = i["description"]
			plot    = plot.replace('"',"-")
			plot    = plot.replace("\r","")
			plot    = plot.replace("\n", " ")
			
			data += '{'
			data += '"name":"' + name + '", '
			data += '"cmd":"' + cmd + '", '
			data += '"logo":"' + logo + '", '
			data += '"cat_id":"' + cat_id + '", '
			data += '"genre_1":"' + genre_1 + '", '
			data += '"genre_2":"' + genre_2 + '", '
			data += '"genre_3":"' + genre_3 + '", '
			data += '"genre_4":"' + genre_4 + '", '			
			data += '"year":"' + year + '", '
			data += '"direct":"' + direct + '", '
			data += '"mpaa":"' + mpaa + '", '
			data += '"runtime":"' + runtime + '", '
			data += '"rating":"' + rating + '", '
			data += '"country":"' + country + '", '
			data += '"cast":"' + cast + '", '
			data += '"plot":"' + plot		
			data += '"}, \n'
		
		page += 1;
		if page > pages or page == numpages:
			break;

	data = data[:-3] + '\n]}'

	with open(portalurl, 'w') as f: f.write(data.encode('utf-8'));
	
	return json.loads(data.encode('utf-8'));


def orderChannels(channels):
      	n_data = {};
      	for i in channels:	
      		number 		= i["number"];
      		n_data[int(number)] = i;
      	
      	ordered = sorted(n_data);
      	data = {};
      	for i in ordered:	
      		data[i] = n_data[i];
      		
      	return data.values();


def getAllChannels(portal_mac, url, serial, portal_login, portal_password, path):

	global login, password;
	added = False;
	
	now = time();
	
	portalurl = "_".join(re.findall("[a-zA-Z0-9]+", url));
	portalurl = path + '/' + portalurl
	
	setMac(portal_mac);
	setLogin(portal_login, portal_password);
	setSerialNumber(serial);
	
	if not os.path.exists(path):
		os.makedirs(path)

	if os.path.exists(portalurl):
		#check last time
		with open(portalurl) as data_file: data = json.load(data_file);
	
		if 'version' not in data or data['version'] != cache_version:
			clearCache(url, path);
			
		else:
			time_init = float(data['time']);
			# update 12h
			if ((now - time_init) / 3600) < 12:
				return data;

	handshake(url);
	getAuth(url);
	getProfile(url);
	
	genres = getGenres(portal_mac, url, serial, login, password, path);
	genres = genres["genres"];
	
	values = {
		'type' : 'itv', 
		'action' : 'get_all_channels',
		'JsHttpRequest' : '1-xml'}
	
	info = retrieveData(url, values)
	
	results = info['js']['data'];

	data = '{ "version" : "' + cache_version + '", "time" : "' + str(now) + '", "channels" : { \n'

	for i in results:
		id 		= i["id"]
		number 	= i["number"]
		name 	= i["name"]
		cmd 	= i['cmd']
		logo 	= i["logo"]
		tmp 	= i["use_http_tmp_link"]
		genre_id 	= i["tv_genre_id"];		
		genre_title = genres[genre_id]['title'];
		
		_s1 = cmd.split(' ');	
		_s2 = _s1[0];
		if len(_s1)>1:
			_s2 = _s1[1];
		
		added = True;
		data += '"' + id + '": {"number":"'+ number +'", "name":"'+ name +'", "cmd":"'+ cmd +'", "logo":"'+ logo +'", "tmp":"'+ str(tmp) +'", "genre_id":"'+ str(genre_id) +'", "genre_title":"'+ genre_title +'"}, \n'


	page = 1;
	pages = 0;
	total_items = 0;
	max_page_items = 0;

	while True:
		# retrieve adults
		
		values = {
			'type' : 'itv', 
			'action' : 'get_ordered_list',
			'genre' : '10',
			'p' : page,
			'fav' : '0',
			'JsHttpRequest' : '1-xml'}
		
		info = retrieveData(url, values)
	
		total_items = float(info['js']['total_items']);
		max_page_items = float(info['js']['max_page_items']);
		pages = math.ceil(total_items/max_page_items);
	
		results = info['js']['data']

		for i in results:
			id 		= i["id"]
			number 	= i["number"]
			name 	= i["name"]
			cmd 	= i['cmd']
			logo 	= i["logo"]
			tmp 	= i["use_http_tmp_link"]
			genre_id 	= i["tv_genre_id"];
			genre_title = genres[genre_id]['title'];
		
			data += '"' + id + '": {"number":"'+ number +'", "name":"'+ name +'", "cmd":"'+ cmd +'", "logo":"'+ logo +'", "tmp":"'+ str(tmp) +'", "genre_id":"'+ str(genre_id) +'", "genre_title":"'+ genre_title +'"}, \n'
			
			added = True;

		page += 1;
		if page > pages:
			break;
	

	if not added:
		data = data + '\n}}';
	else:
		data = data[:-3] + '\n}}';

	
	with open(portalurl, 'w') as f: f.write(data.encode('utf-8'));
	
	return json.loads(data.encode('utf-8'));


def retriveUrl(portal_mac, url, serial, portal_login, portal_password, channel, tmp):

	setMac(portal_mac);
	setLogin(portal_login, portal_password);
	setSerialNumber(serial);
	
	if 'matrix' in channel:
		return retrieve_matrixUrl(url, channel);
		
	else:
		return retrive_defaultUrl(url, channel, tmp);
	
		
def retrive_defaultUrl(url, channel, tmp):

	global login, password;

	if tmp == '0':
		s = channel.split(' ');
		url = s[0];
		if len(s)>1:
			url = s[1];
		return url;

	handshake(url);
	getAuth(url);
	getProfile(url);

	values = {
		'type' : 'itv' if (tmp != "") else 'vod', 
		'action' : 'create_link',
		'cmd' : channel,
		'JsHttpRequest' : '1-xml'}
	
	info = retrieveData(url, values );
	
	cmd = info['js']['cmd'];
		
	s = cmd.split(' ');
			
	url = s[0];
	
	if len(s)>1:
		url = s[1];

	# RETRIEVE THE 1 EXTM3U
	request = urllib2.Request(url)
	request.get_method = lambda : 'HEAD'
	response  = urllib2.urlopen(request);
	data = response.read().decode("utf-8");
	
	data = data.splitlines();
	data = data[len(data) - 1];

	# RETRIEVE THE 2 EXTM3U
	url = response.geturl().split('?')[0];
	url_base = url[: -(len(url) - url.rfind('/'))]
	return url_base + '/' + data;
	
	return url;


def retrieve_matrixUrl(url, channel):

	global login, password;

	channel = channel.split('/');
	channel = channel[len(channel) -1];
	
	url += '/stalker_portal/server/api/matrix.php?channel=' + channel + '&mac=' + mac;

	
	# RETRIEVE THE 1 EXTM3U
	request = urllib2.Request(url)
	response  = urllib2.urlopen(request);
	data = response.read().decode("utf-8");

	_s1 = data.split(' ');	
	data = _s1[0];
	if len(_s1)>1:
		data = _s1[len(_s1) -1];
	
	return data;

	
def clearCache(url, path):
	
	portalurl = "_".join(re.findall("[a-zA-Z0-9]+", url));
	
	for root, dirs, files in os.walk(path):
		for file in files:
			if file.startswith(portalurl):
				os.remove(root + '/' + file);


def main(argv):

	if argv[0] == 'load':
		data = getAllChannels(argv[1], argv[2], json.loads(argv[3]), argv[4], argv[5], argv[6]);
   	
	elif argv[0] == 'genres':
		getGenres(argv[1], argv[2], None, argv[3], argv[4], argv[5]);
      	
	elif argv[0] == 'channel':     	
		url = retriveUrl(argv[1], argv[2], json.loads(argv[3]), argv[4], argv[5], argv[6], argv[7]);
	
	elif argv[0] == 'vod_url':
		url = retriveVoD('', argv[1], argv[2]);
      	
	elif argv[0] == 'cache':
		clearCache(argv[1], argv[2]);
      	
	elif argv[0] == 'profile':
		handshake(argv[1]);
      	
 
if __name__ == "__main__":
	main(sys.argv[1:])


