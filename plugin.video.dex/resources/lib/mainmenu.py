# -*- coding: utf-8 -*-
'''
    script.matchcenter - Football information for Kodi
    A program addon that can be mapped to a key on your remote to display football information.
    Livescores, Event details, Line-ups, League tables, next and previous matches by team. Follow what
    others are saying about the match in twitter.
    Copyright (C) 2016 enen92

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmcgui
import xbmc
import sys
import os
import livescores
import leagueselection
import tweets
from utilities import ssutils
from utilities.common_addon import *

MAIN_MENU = {
	"livescores" : {"label" : translate(32001), "icon" : os.path.join(addon_path,"resources","img","goal.png")},
	"tables" : {"label" : "Table", "icon" : os.path.join(addon_path,"resources","img","tables.png")},
	"Pay Per View" : {"label" : "PPV", "icon" : os.path.join(addon_path,"resources","img","twitter.png")}
}


class Main(xbmcgui.WindowXMLDialog):
	
	def __init__( self, *args, **kwargs ):
		pass

	def onInit(self):
		items = []
		for menuentry in MAIN_MENU.keys():
			item = xbmcgui.ListItem(MAIN_MENU[menuentry]["label"])
			item.setProperty("thumb",str(MAIN_MENU[menuentry]["icon"]))
			item.setProperty("identifier",str(menuentry))
			items.append(item)
		self.getControl(32500).addItems(items)

	def onClick(self,controlId):
		if controlId == 32500:
			identifier = self.getControl(32500).getSelectedItem().getProperty("identifier")
			if identifier == "livescores":
				self.close()
				livescores.start()
			elif identifier == "tables":
				self.close()
				leagueselection.start()
			elif identifier == "Pay Per View":
				self.close()
				tweets.start()


def start():
	main = Main(
			'script-matchcenter-MainMenu.xml',
			addon_path,
			'default',
			'',
			)
	main.doModal()
	del main