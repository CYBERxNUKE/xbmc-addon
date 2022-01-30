# -*- coding: utf-8 -*-
import sys
from xbmc import executebuiltin, sleep

executebuiltin("RunPlugin(%s)" % sys.listitem.getProperty('fen_clearprog_params'))
sleep(1000)
executebuiltin('UpdateLibrary(video,special://skin/foo)')
