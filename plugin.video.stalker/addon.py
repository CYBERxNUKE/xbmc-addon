# -*- coding: utf-8 -*-
import sys
import os
import json
import urllib
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
import hashlib
import re
import time
import string
import config
import load_channels
import server



addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('profile') )

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])
go = True;

xbmcplugin.setContent(addon_handle, 'movies')

version = xbmc.getInfoLabel('System.BuildVersion')
version = version.split()


def addPortal(portal):

	if portal['url'] == '':
		return;

	url = build_url({
		'mode': 'genres', 
		'portal' : json.dumps(portal)
		});
	
	cmd = 'XBMC.RunPlugin(' + base_url + '?mode=cache&stalker_url=' + portal['url'] + ')';	
	
	li = xbmcgui.ListItem(portal['name'], iconImage='DefaultProgram.png')
	li.addContextMenuItems([ ('Clear Cache', cmd) ]);

	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
	
def build_url(query):
	return base_url + '?' + urllib.urlencode(query)

def homeLevel():
	global portal_1, portal_2, portal_3, go;
	
	# at least portal 1 will be active.

	if go:
		addPortal(portal_1);
		addPortal(portal_2);
		addPortal(portal_3);
	
		xbmcplugin.endOfDirectory(addon_handle);

def genreLevel():
	
	try:
		data = load_channels.getGenres(portal['mac'], portal['url'], portal['serial'], portal['login'], portal['password'], addondir);
		
	except Exception as e:
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		
		return;

	data = data['genres'];

	for id, i in data.iteritems():

		title 	= i["title"];
		title   = string.capwords(title);
		
		url = build_url({
			'mode': 'channels', 
			'genre_id': id, 
			'genre_name': title, 
			'portal' : json.dumps(portal)
			});
		
		if id == '10':
			iconImage = 'OverlayLocked.png';
		else:
			iconImage = 'DefaultVideo.png';
			
		li = xbmcgui.ListItem(title, iconImage=iconImage)
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
		
##########
# create VoD folders
	url = build_url({
		'mode': 'vod',
		'cat_id': '10',
		'genre_name': 'VoD',
		'portal' : json.dumps(portal)
		});
		
	li = xbmcgui.ListItem('VoD', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
	

	url = build_url({
		'mode': 'vod', 
		'cat_id': '12',
		'genre_name': 'VoD Espanol',
		'portal' : json.dumps(portal)
		});

	li = xbmcgui.ListItem('VoD Español', iconImage='DefaultVideo.png')
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True);
##########			
		
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_LABEL);
	xbmcplugin.endOfDirectory(addon_handle);

def vodLevel():
	
	try:
		data = load_channels.getVoD(portal['mac'], portal['url'], portal['serial'], portal['login'], portal['password'], portal['vodpages'], addondir);
		
	except Exception as e:
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		return;
	
	data = data['vod'];
	genre_name = args.get('genre_name', None);
	genre_name = genre_name[0];
	cat_id_main = args.get('cat_id', None);
	cat_id_main = cat_id_main[0];
	genretypes = json.loads ('{"0":"","1":"Action","2":"2","3":"Documentary","4":"Drama","5":"Family","6":"Romance","7":"Comedy","8":"8","9":"9","10":"Adventure","11":"Thriller","12":"Horror","13":"Sci-Fi","14":"","15":"Fantasy","16":"Animation","17":"Family","18":"Music","19":"Western","20":"20","21":"21","22":"Sport","23":"23","24":"24","25":"25","26":"Short","27":"27","28":"28","29":"29","30":"30"}')
	
	for i in data:
	
		name 	= i["name"];
		cmd 	= i["cmd"];
		logo 	= i["logo"];
		cat_id  = i["cat_id"];
		genre_1 = i["genre_1"];
		genre_2 = i["genre_2"];
		genre_3 = i["genre_3"];
		genre_4 = i["genre_4"];
		
		genre   = [genretypes[genre_1], genretypes[genre_2], genretypes[genre_3], genretypes[genre_4]]
		genre   = " ".join(genre)
		genre   = genre.rstrip()
		genre   = genre.replace(" ",", ")

		year    = i["year"];
		direct  = i["direct"];
		mpaa    = i["mpaa"];
		runtime = i["runtime"];
		if version[0] >= '16' and runtime != "":
			runtime = str(int(runtime) * 60)
		rating  = i["rating"];
		country = i["country"]
		
		cast    = i["cast"];
		cast    = tuple(cast.split(', '))

		plot    = i["plot"];
		
		if logo != '':
			logo_url = portal['url'] + logo;
		else:
			logo_url = 'DefaultVideo.png';
		
		if cat_id == cat_id_main:
			url = build_url({
				'mode': 'play', 
				'cmd': cmd, 
				'tmp' : '0', 
				'title' : name.encode("utf-8"),
				'genre_name' : genre_name,
				'logo_url' : logo_url, 
				'portal' : json.dumps(portal)
				});

			li = xbmcgui.ListItem(name, iconImage=logo_url, thumbnailImage=logo_url)
			li.setInfo(type='Video', 
						infoLabels={ 
						"Genre": genre, 
						"Title": name, 
						"Year": year, 
						"Director": direct, 
						"Mpaa": mpaa, 
						"Duration": runtime, 
						"Rating": rating,
						"Country": country,		
						"Cast": cast,  
						"Plot": plot })

			xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)
	
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_UNSORTED);
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_GENRE);
	xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_MPAA_RATING);		
	xbmcplugin.endOfDirectory(addon_handle);

def channelLevel():

	stop=False;
		
	try:
		data = load_channels.getAllChannels(portal['mac'], portal['url'], portal['serial'],portal['login'], portal['password'], addondir);
		
	except Exception as e:
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		return;
		
	data = data['channels'];
	genre_name 	= args.get('genre_name', None);	
	genre_id_main = args.get('genre_id', None);
	genre_id_main = genre_id_main[0];
	
	if genre_id_main == '10' and portal['parental'] == 'true':
		result = xbmcgui.Dialog().input('Parental', hashlib.md5(portal['ppassword'].encode('utf-8')).hexdigest(), type=xbmcgui.INPUT_PASSWORD, option=xbmcgui.PASSWORD_VERIFY);
		if result == '':
			stop = True;
	
	if stop == False:
		for i in data.values():
			
			name 		= i["name"];
			cmd 		= i["cmd"];
			tmp 		= i["tmp"];
			number 		= i["number"];
			genre_id 	= i["genre_id"];
			logo 		= i["logo"];
		
			if genre_id_main == '*' and genre_id == '10' and portal['parental'] == 'true':
				continue;
				
			if genre_id_main == genre_id or genre_id_main == '*':
		
				if logo != '':
					logo_url = portal['url'] + '/stalker_portal/misc/logos/320/' + logo;
				else:
					logo_url = 'DefaultVideo.png';
								
				url = build_url({
					'mode': 'play', 
					'cmd': cmd, 
					'tmp' : tmp, 
					'title' : name.encode("utf-8"),
					'genre_name' : genre_name,
					'logo_url' : logo_url,  
					'portal' : json.dumps(portal)
					});
			
				li = xbmcgui.ListItem(name, iconImage=logo_url, thumbnailImage=logo_url);
				li.setInfo(type='Video', infoLabels={ 
					'title': name,
					'count' : number
					});

				xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li);
		
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_PLAYLIST_ORDER);
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_TITLE);
		xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_PROGRAM_COUNT);
			
		xbmcplugin.endOfDirectory(addon_handle);

def playLevel():
	
	dp = xbmcgui.DialogProgressBG();
	dp.create('IPTV', 'Loading ...');
	
	title 	= args['title'][0];
	cmd 	= args['cmd'][0];
	tmp 	= args['tmp'][0];
	genre_name 	= args['genre_name'][0];
	logo_url 	= args['logo_url'][0];

	if genre_name == 'VoD' or genre_name == 'VoD Espanol':
		tmp = "";

	try :
		url = load_channels.retriveUrl(portal['mac'], portal['url'], portal['serial'], portal['login'], portal['password'], cmd, tmp);
			
	except Exception as e:
		dp.close();
		xbmcgui.Dialog().notification(addonname, str(e), xbmcgui.NOTIFICATION_ERROR );
		return;

	
	dp.update(80);
	
	title = title.decode("utf-8");
	
	title += ' (' + portal['name'] + ')';
	
	li = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=logo_url);
	li.setInfo('video', {'Title': title, 'Genre': genre_name});
	xbmc.Player().play(item=url, listitem=li);
	
	dp.update(100);
	
	dp.close();


mode = args.get('mode', None);
portal =  args.get('portal', None)


if portal is None:
	portal_1 = config.portalConfig('1');
	portal_2 = config.portalConfig('2');
	portal_3 = config.portalConfig('3');	

else:
#  Force outside call to portal_1
	portal = json.loads(portal[0]);
	portal_2 = config.portalConfig('2');
	portal_3 = config.portalConfig('3');	

	if not ( portal['name'] == portal_2['name'] or portal['name'] == portal_3['name'] ) :
		portal = config.portalConfig('1');


if mode is None:
	homeLevel();

elif mode[0] == 'cache':	
	stalker_url = args.get('stalker_url', None);
	stalker_url = stalker_url[0];	
	load_channels.clearCache(stalker_url, addondir);

elif mode[0] == 'genres':
	genreLevel();
		
elif mode[0] == 'vod':
	vodLevel();

elif mode[0] == 'channels':
	channelLevel();
	
elif mode[0] == 'play':
	playLevel();
	
elif mode[0] == 'server':
	port = addon.getSetting('server_port');
	
	action =  args.get('action', None);
	action = action[0];
	
	dp = xbmcgui.DialogProgressBG();
	dp.create('M3U Server', 'Working ...');
	
	if action == 'start':
	
		if server.serverOnline():
			xbmcgui.Dialog().notification(addonname, 'Server already started.\nPort: ' + str(port), xbmcgui.NOTIFICATION_INFO );
		else:
			server.startServer();
			time.sleep(5);
			if server.serverOnline():
				xbmcgui.Dialog().notification(addonname, 'Server started.\nPort: ' + str(port), xbmcgui.NOTIFICATION_INFO );
			else:
				xbmcgui.Dialog().notification(addonname, 'Server not started. Wait a minute and try again. ', xbmcgui.NOTIFICATION_ERROR );
				
	else:
		if server.serverOnline():
			server.stopServer();
			time.sleep(5);
			xbmcgui.Dialog().notification(addonname, 'Server stopped.', xbmcgui.NOTIFICATION_INFO );
		else:
			xbmcgui.Dialog().notification(addonname, 'Server is already stopped.', xbmcgui.NOTIFICATION_INFO );
			
	dp.close();
