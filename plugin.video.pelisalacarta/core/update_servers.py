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
# update_servers.py
# --------------------------------------------------------------------------------

import os
import urlparse

from core import config
from core import scrapertools
from core import servertools

DEBUG = config.get_setting("debug")

remote_url = "https://raw.githubusercontent.com/tvalacarta/pelisalacarta/master/python/main-classic/servers/"
local_folder = os.path.join( config.get_runtime_path(), "servers" )

### Procedures
def update_servers():

    update_servers_files(
        read_remote_servers_list(
            dict( read_local_servers_list() )
        )
    )

def update_servers_files( update_servers_list ):

    # ----------------------------
    from platformcode import platformtools
    progress = platformtools.dialog_progress_bg( "Update servers list" )
    # ----------------------------

    for index, server in enumerate( update_servers_list ):
        # ----------------------------
        percentage = index * 100 / len( update_servers_list )
        # ----------------------------

        data = scrapertools.cache_page( remote_url + server[0] + ".py" )

        f = open( os.path.join( local_folder, server[0] + ".py" ) ,'w' )
        f.write( data )
        f.close()

        # ----------------------------
        progress.update( percentage, ' Update server: "' + server[0] + '"', 'MD5: "' + server[1] + '"' )
        # ----------------------------

    # ----------------------------
    progress.close()
    # ----------------------------

### Functions
## init
def read_remote_servers_list( local_servers ):

    data = scrapertools.cache_page( remote_url + "servertools.py")

    f = open( os.path.join( local_folder, "servertools.py" ) ,'w' )
    f.write( data )
    f.close()

    all_servers = sorted(
        servertools.FREE_SERVERS + \
        servertools.PREMIUM_SERVERS + \
        servertools.FILENIUM_SERVERS + \
        servertools.REALDEBRID_SERVERS + \
        servertools.ALLDEBRID_SERVERS
    )

    servers = []
    for server_id in all_servers:
        if server_id not in servers:
            servers.append( server_id )

    # ----------------------------
    from platformcode import platformtools
    progress = platformtools.dialog_progress_bg( "Remote servers list" )
    # ----------------------------

    remote_servers = []
    update_servers_list = []
    for index, server in enumerate( servers ):
        # ----------------------------
        percentage = index * 100 / len( servers )
        # ----------------------------
        server_file = urlparse.urljoin( remote_url, server + ".py" )

        data = scrapertools.cache_page( server_file )
        if data != "Not Found":
            md5_remote_server = md5_remote( data )
            remote_servers.append( [ server, md5_remote_server ] )

            md5_local_server = local_servers.get( server )
            if md5_local_server:
                if md5_local_server != md5_remote_server:
                    update_servers_list.append( [ server, md5_remote_server, md5_local_server, "Update" ] )
            else:
                update_servers_list.append( [ server, md5_remote_server, "New", "Update" ] )

            # ----------------------------
            progress.update( percentage, ' Remote server: "' + server + '"', 'MD5: "' + md5_remote_server + '"' )
            # ----------------------------

    # ----------------------------
    progress.close()
    # ----------------------------

    return update_servers_list

def read_local_servers_list():

    all_servers = sorted(
        servertools.FREE_SERVERS + \
        servertools.PREMIUM_SERVERS + \
        servertools.FILENIUM_SERVERS + \
        servertools.REALDEBRID_SERVERS + \
        servertools.ALLDEBRID_SERVERS
    )

    servers = []
    for server_id in all_servers:
        if server_id not in servers:
            servers.append( server_id )

    # ----------------------------
    from platformcode import platformtools
    progress = platformtools.dialog_progress_bg( "Local servers list" )
    # ----------------------------

    local_servers = []
    for index, server in enumerate( servers ):
        # ----------------------------
        percentage = index * 100 / len( servers )
        # ----------------------------
        server_file = os.path.join( config.get_runtime_path(), "servers", server + ".py" )
        if os.path.exists( server_file ):
            md5_local_server = md5_local( server_file )
            local_servers.append( [ server, md5_local_server ] )
            # ----------------------------
            progress.update( percentage, ' Local server: "' + server + '"', 'MD5: "' + md5_local_server + '"' )
            # ----------------------------

    # ----------------------------
    progress.close()
    # ----------------------------

    return local_servers

def md5_local( file_server ):

    import hashlib
    hash = hashlib.md5()
    with open( file_server ) as f:
        for chunk in iter( lambda: f.read( 4096 ), "" ):
            hash.update( chunk )

    return hash.hexdigest()

def md5_remote( data_server ):

    import hashlib
    hash = hashlib.md5()
    hash.update( data_server )

    return hash.hexdigest()

### Run
update_servers()
#from threading import Thread
#Thread( target=update_servers ).start()