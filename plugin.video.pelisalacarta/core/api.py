#------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta 4
# Copyright 2016 tvalacarta@gmail.com
#
# Distributed under the terms of GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
#------------------------------------------------------------
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
#------------------------------------------------------------
# Client for api.tvalacarta.info
#------------------------------------------------------------

import os
import sys
import urlparse
import jsontools
import config
import logger
import scrapertools

import urllib
from item import Item

MAIN_URL = "http://api.tvalacarta.info/v2"
API_KEY = "nzgJy84P9w54H2w"
DEFAULT_HEADERS = [ ["User-Agent",config.PLUGIN_NAME+" "+config.get_platform()] ]

# ---------------------------------------------------------------------------------------------------------
#  Common function for API calls
# ---------------------------------------------------------------------------------------------------------

# Make a remote call using post, ensuring api key is here
def remote_call(url,parameters={},require_session=True):
    logger.info("pelisalacarta.core.api.remote_call url="+url+", parameters="+repr(parameters))

    if not url.startswith("http"):
        url = MAIN_URL + "/" + url

    if not "api_key" in parameters:
        parameters["api_key"] = API_KEY

    # Add session token if not here
    #if not "s" in parameters and require_session:
    #    parameters["s"] = get_session_token()

    headers = DEFAULT_HEADERS
    post = urllib.urlencode(parameters)

    response_body = scrapertools.downloadpage(url,post,headers)

    return jsontools.load_json(response_body)

# ---------------------------------------------------------------------------------------------------------
#  Plugin service calls
# ---------------------------------------------------------------------------------------------------------

def plugins_get_all_packages():
    logger.info("pelisalacarta.core.api.plugins.get_all_packages")

    parameters = { "plugin" : config.PLUGIN_NAME , "platform" : config.get_platform() }
    return remote_call( "plugins/get_all_packages.php" , parameters )

def plugins_get_latest_packages():
    logger.info("pelisalacarta.core.api.plugins.get_latest_packages")

    parameters = { "plugin" : config.PLUGIN_NAME , "platform" : config.get_platform() }
    return remote_call( "plugins/get_latest_packages.php" , parameters )
