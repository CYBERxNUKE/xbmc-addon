# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta 4
# Copyright 2015 tvalacarta@gmail.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------------------
# This file is part of pelisalacarta 4.
#
# pelisalacarta 4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pelisalacarta 4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pelisalacarta 4.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------
# Version Tools
# --------------------------------------------------------------------------------

import os
import re
import sys
import time

import config
import logger
import scrapertools

def get_current_plugin_version():
    return 4204

def get_current_plugin_version_tag():
    return "4.2.0-final"

def get_current_plugin_date():
    return "30/04/2017"
    
def get_current_channels_version():

    f = open( os.path.join( config.get_runtime_path() , "channels" , "version.xml" ) )
    data = f.read()
    f.close()

    return int(scrapertools.find_single_match(data,"<version>([^<]+)</version>"))
    
def get_current_servers_version():

    f = open( os.path.join( config.get_runtime_path() , "servers" , "version.xml" ) )
    data = f.read()
    f.close()

    return int(scrapertools.find_single_match(data,"<version>([^<]+)</version>"))
