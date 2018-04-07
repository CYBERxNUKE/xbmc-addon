################################################################################
#(_)                                                                           #
# |_________________________________________                                   #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|      If your going to copy       #
# | *  *  *  *  *|==========================|         this addon just          #
# |*  *  *  *  * |##########################|         give credit!!!!          #
# |--------------|==========================|                                  #
# |#########################################|                                  #
# |=========================================|                                  #
# |#########################################|                                  #
# |=========================================|            seduNdneS             #
# |#########################################|                                  #
# |-----------------------------------------|                                  #
# |                                                                            #
# |    Not Sure Add-on                                                         #
# |    Copyright (C) 2017 FTG                                                  #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil,requests
import urllib2,urllib
import re
import time
from datetime import date, datetime, timedelta
ADDON_ID            = 'plugin.video.sedundnes'
AddonTitle          = '[COLOR yellow]Not Sure[/COLOR]'
fanart              = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'fanart.jpg'))
icon                = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID, 'icon.png'))
setting             = xbmcaddon.Addon().getSetting
addonInfo           = xbmcaddon.Addon().getAddonInfo
HOME                = xbmc.translatePath('special://home/')
XXX_SETTINGS        = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID,'settings.xml'))
PARENTAL_FOLDER     = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID , 'parental'))
DATA_FOLDER         = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/' + ADDON_ID))
ADDON_FOLDER        = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID))
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME,     'addons')
USERDATA       = os.path.join(HOME,     'userdata')
PLUGIN         = os.path.join(ADDONS,   ADDON_ID)
ART            = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID , 'resources','skin', 'art'))
TERMS          = "[COLOR yellow]Not Sure by seduNdneS Disclaimer[/COLOR]\n[COLOR snow]This Addon does not host, provide, archive, store, or distribute media of any kind, and acts merely as an index (or directory) of media posted by other webmasters on the internet, which is completely outside of our control.Whereas we do not filter such references, we cannot and do not attempt to control, censor, or block any indexed material that may be considered offensive, abusive, libellous, obnoxious, inaccurate, deceptive, unlawful or otherwise distressing neither do we accept responsibility for this content or the consequences of such content being made available.\nAll users undertake to comply with the national laws applicable to the country they reside in and observe the rights inherent in any copyright material whilst upholding the rights of any copyright owner.All users are advised to use caution, discretion, common sense and personal judgment when using primewire.one or any references detailed within the directory and to respect the wishes of others who may value freedom from censorship, as consenting adults equal to (or possibly superior to) your own personal preferences.[/COLOR]\n\n[COLOR yellow]You must agree and that YOU are legally bound to these Terms and Conditions[/COLOR]"
I_AGREE        = xbmc.translatePath(os.path.join(DATA_FOLDER , 'agreed.txt'))
ADDON_FOLDER = xbmc.translatePath(os.path.join('special://home/addons/' + ADDON_ID))

def message(url):
	n=requests.get('http://pastebin.com/raw/r85dgzUz')
	TextBox('[COLOR yellow][B]NOT SURE[/B][/COLOR]',n.text)
def faq(url):
	n=requests.get('https://pastebin.com/raw/6UCJ6D03')
	TextBox('[COLOR yellow][B]NOT SURE[/B][/COLOR]',n.text)
def AgreeFirst():
	Agree('[COLOR yellow][B]NOT SURE[/B][/COLOR]',TERMS)

def Agree(title,msg):
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
				open(I_AGREE, 'w')
				self.close()

	tb = TextBoxes( "agree.xml" , ADDON_FOLDER, 'DefaultSkin', title=title, msg=msg)
	tb.doModal()
	del tb

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
