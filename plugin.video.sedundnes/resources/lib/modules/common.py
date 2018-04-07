
import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs
from urllib import FancyURLopener
from HTMLParser import HTMLParser
import platform
import shutil
import urllib2,urllib
import re
import requests
import glob
import time
import errno
import socket
import json
addon_id = 'plugin.video.sedundnes'
ADDON = xbmcaddon.Addon(id=addon_id)
HOME         =  xbmc.translatePath('special://home/')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
FANART              = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
ICON                = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
ADDON_FOLDER = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id))


def SHOW_PICTURE(url):
    SHOW = "ShowPicture(" + url + ')'
    xbmc.executebuiltin(SHOW)
    sys.exit(1)

def message(url):
	f=requests.get('http://pastebin.com/raw/r85dgzUz')
	TextBox('[COLOR yellow][B]NOT SURE[/B][/COLOR]',f.text)

def TextBox(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):
		def onInit(self):
			self.title      = 100
			self.msg        = 101
			self.okbutton   = 102
			self.scrollbar  = 104

			self.showdialog()

		def showdialog(self):
		
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

			
		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()
			elif (controlId == self.uploadbutton):
				uploadlog.main(argv=None)	

	tb = TextBoxes( "textbox.xml" , ADDON_FOLDER, 'DefaultSkin', title=title, msg=msg)
	tb.doModal()
	del tb


def OPEN_URL(url):
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36')
		response = urllib2.urlopen(req, timeout = 30)
		link=response.read()
		response.close()
		return link

