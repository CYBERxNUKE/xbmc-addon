import sys
import os
import json
import urllib
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import load_channels
import hashlib
import re


addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
addondir    = xbmc.translatePath( addon.getAddonInfo('profile') ) 


def portalConfig(number):

	portal = {};
	
	portal['parental'] = addon.getSetting("parental");
	portal['ppassword'] = addon.getSetting("ppassword");
	
	portal['name'] = addon.getSetting("portal_name_" + number);
	portal['url'] = configUrl(number);
	portal['mac'] = configMac(number);
	portal['serial'] = configSerialNumber(number);
	portal['login'] = configLogin(number);
	portal['password'] = configPassword(number);
	portal['vodpages'] = addon.getSetting("vodpages_" + number)
	
	return portal;

	
def configUrl(number):

	serverid = addon.getSetting('portal_server_' + number);

	if serverid == "0":
		portal_url = "http://portal1.iptvprivateserver.tv";
	elif serverid == "1":
		portal_url = "http://portal2.iptvprivateserver.tv";
	elif serverid == "2":
		portal_url = "http://portal3.iptvprivateserver.tv";
	elif serverid == "3":
		portal_url = "http://portal4.iptvprivateserver.tv";
	elif serverid == "4":
		portal_url = "http://portal5.iptvprivateserver.tv";
	elif serverid == "5":
		portal_url = "http://portal.iptvrocket.tv";
	elif serverid == "6":
		portal_url = "http://mw1.iptv66.tv";
	else :
		portal_url = "";	
	return portal_url;


def configMac(number):
	global go;
	
	portal_mac = addon.getSetting('portal_mac_' + number);
	portal_mac = "00:1A:78:" + portal_mac;
	
	if not (portal_mac == '' or re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", portal_mac.lower()) != None):
		xbmcgui.Dialog().notification(addonname, 'Custom Mac ' + number + ' is Invalid.', xbmcgui.NOTIFICATION_ERROR );
		portal_mac = '';
		go=False;
		
	return portal_mac;

	
def configSerialNumber(number):
	global go;
	
	send_serial = addon.getSetting('send_serial_' + number);
	custom_serial = addon.getSetting('custom_serial_' + number);
	serial_number = addon.getSetting('serial_number_' + number);
	device_id = addon.getSetting('device_id_' + number);
	device_id2 = addon.getSetting('device_id2_' + number);
	signature = addon.getSetting('signature_' + number);
	
	if send_serial != 'true':
		return {'send_serial' : False};
	
	if send_serial == 'true' and custom_serial == 'false':
		return {'send_serial' : True, 'custom' : False};
		
	elif send_serial == 'true' and custom_serial == 'true':
	
#		if serial_number == '' or device_id == '' or device_id2 == '' or signature == '':
#			xbmcgui.Dialog().notification(addonname, 'Serial information is invalid.', xbmcgui.NOTIFICATION_ERROR );
#			go=False;
#			return None;

		return {'send_serial' : True, 
		        'custom' : True, 
				'sn' : serial_number, 
				'device_id' : device_id, 
				'device_id2' : device_id2, 
				'signature' : signature }; 
		
	return None;

	
def configLogin(number):
	global go;
	
	login = addon.getSetting('login_' + number);
	if login == '':
		xbmcgui.Dialog().notification(addonname, 'login' + number + ' is invalid.', xbmcgui.NOTIFICATION_ERROR );
		go=False;
		return None;

	return login;

	
def configPassword(number):
	global go;
	
	password = addon.getSetting('password_' + number);
	if password == '':
		xbmcgui.Dialog().notification(addonname, 'password' + number + ' is invalid.', xbmcgui.NOTIFICATION_ERROR );
		go=False;
		return None;

	return password;