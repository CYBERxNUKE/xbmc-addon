# -*- coding: utf-8 -*-
import sys
from xbmc import executebuiltin

executebuiltin("RunPlugin(%s)" % sys.listitem.getProperty('fen_trakt_manager_params'))
