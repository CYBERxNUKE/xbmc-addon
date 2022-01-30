# -*- coding: utf-8 -*-
import sys
from xbmc import executebuiltin

executebuiltin("ActivateWindow(Videos,%s)" % sys.listitem.getProperty("fen_browse_params"))