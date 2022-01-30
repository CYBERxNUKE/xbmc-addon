# -*- coding: utf-8 -*-
import sys
from xbmc import executebuiltin

params = sys.listitem.getProperty('fen_extras_menu_params')
params += '&is_widget=false&is_home=true'
executebuiltin('RunPlugin(%s)' % params)
