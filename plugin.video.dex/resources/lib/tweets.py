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
import datetime
import json
import mainmenu
from resources.lib.utilities import tweet
from resources.lib.utilities import ssutils
from resources.lib.utilities.common_addon import *

class detailsDialog(xbmcgui.WindowXMLDialog):
		
	def __init__( self, *args, **kwargs ):
		self.isRunning = True
		self.hash = kwargs["hash"]
		self.teamObjs = {}

	def onInit(self):
		xbmc.log(msg="[Match Center] Twitter cycle started", level=xbmc.LOGDEBUG)
		self.getControl(32540).setImage(os.path.join(addon_path,"resources","img","goal.png"))
		xbmc.executebuiltin("SetProperty(loading,1,home)")
		self.getTweets()
		xbmc.executebuiltin("ClearProperty(loading,Home)")
		i=0
		while self.isRunning:
			if (float(i*200)/(twitter_update_time*60*1000)).is_integer() and ((i*200)/(3*60*1000)) != 0:
				self.getTweets()
			xbmc.sleep(200)
			i += 1
		xbmc.log(msg="[Match Center] Twitter cycle stopped", level=xbmc.LOGDEBUG)

	def getTweets(self):
		self.getControl(32500).setLabel("#"+self.hash)
		self.getControl(32503).setImage(os.path.join(addon_path,"resources","img","twitter.png"))
		tweetitems = []
		tweets = tweet.get_hashtag_tweets(self.hash)
		if tweets:
			for _tweet in tweets:
				item = xbmcgui.ListItem(_tweet["text"].replace("\n",""))
				item.setProperty("profilepic",_tweet["profilepic"])
				item.setProperty("author","[B]" +"@" + _tweet["author"] + "[/B]")
				tweetitems.append(item)
				#print datetime.datetime.now() - _tweet["date"]
		self.getControl(32501).reset()
		self.getControl(32501).addItems(tweetitems)
		if tweetitems:
			self.setFocusId(32501)
		return

	def savecurrenthash(self):
		media_file = xbmc.getInfoLabel('Player.Filenameandpath')
		media_dict = {"file" : media_file, "hash":self.hash}
		ssutils.write_file(tweet_file,json.dumps(media_dict))
		return

	def reset(self):
		if os.path.exists(tweet_file):
			os.remove(tweet_file)
			xbmcgui.Dialog().ok(translate(32000), translate(32045))
		return

	def stopRunning(self):
		self.isRunning = False
		self.close()
		mainmenu.start()

	def onAction(self,action):
		if action.getId() == 92 or action.getId() == 10:
			self.stopRunning()

	def onClick(self,controlId):
		if controlId == 32501:
			teamid = self.getControl(controlId).getSelectedItem().getProperty("teamid")
			matchhistory.start(teamid)
		elif controlId == 32514:
			self.reset()

def start(twitterhash=None):
	if twitterhash == None:
		if os.path.exists(tweet_file):
			twitter_data = json.loads(ssutils.read_file(tweet_file))
			twitterhash = twitter_data["hash"]
			twitter_mediafile = twitter_data["file"]
			if twitter_mediafile == xbmc.getInfoLabel('Player.Filenameandpath'):
				userInput = False
				main = detailsDialog('script-matchcenter-Twitter.xml', addon_path, 'default', '', hash=twitterhash)
				main.doModal()
				del main
			else:
				userInput = True
		else:
			userInput = True

		if userInput:
			dialog = xbmcgui.Dialog()
			twitterhash = dialog.input(translate(32046), type=xbmcgui.INPUT_ALPHANUM)
			if len(twitterhash) != 0:
				main = detailsDialog('script-matchcenter-Twitter.xml', addon_path, 'default', '', hash=twitterhash.replace("#",""))
				if xbmc.getCondVisibility("Player.HasMedia") and save_hashes_during_playback == 'true':
					main.savecurrenthash()
				main.doModal()
				del main
			else:
				xbmcgui.Dialog().ok(translate(32000), translate(32047))
				mainmenu.start()
	else:
		main = detailsDialog('script-matchcenter-Twitter.xml', addon_path, 'default', '', hash=twitterhash)
		main.doModal()
		del main	