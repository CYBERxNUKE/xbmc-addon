# -*- coding: utf-8 -*-
import xbmc
from threading import Thread
from services import service_functions
from modules.settings_reader import make_settings_dict
from modules.kodi_utils import clear_property, logger

class FenMonitor(xbmc.Monitor):
	def __init__ (self):
		xbmc.Monitor.__init__(self)
		logger('FEN', 'Main Monitor Service Starting')
		logger('FEN', 'Settings Monitor Service Starting')
		self.startUpServices()
	
	def startUpServices(self):
		threads = []
		functions = (service_functions.DatabaseMaintenance().run, service_functions.TraktMonitor().run)
		for item in functions: threads.append(Thread(target=item))
		while not self.abortRequested():
			try: service_functions.InitializeDatabases().run()
			except: pass
			try: service_functions.CheckSettingsFile().run()
			except: pass
			try: service_functions.SyncMyAccounts().run()
			except: pass
			[i.start() for i in threads]
			try: service_functions.ClearSubs().run()
			except: pass
			try: service_functions.ReuseLanguageInvokerCheck().run()
			except: pass
			try: service_functions.ViewsSetWindowProperties().run()
			except: pass
			try: service_functions.AutoRun().run()
			except: pass
			break

	def onSettingsChanged(self):
		clear_property('fen_settings')
		xbmc.sleep(50)
		refreshed = make_settings_dict()

FenMonitor().waitForAbort()

logger('FEN', 'Settings Monitor Service Finished')
logger('FEN', 'Main Monitor Service Finished')