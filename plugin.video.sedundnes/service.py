# -*- coding: utf-8 -*-

################################################################################
#(_)                                                                           #
# |_________________________________________                                   #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|                                  #
# | *  *  *  *  *|==========================|                                  #
# |*  *  *  *  * |##########################|      If your going to copy       #
# | *  *  *  *  *|==========================|         this addon just          #
# |*  *  *  *  * |##########################|         give credit!!!!          #
# |--------------|==========================|                                  #
# |#########################################|                                  #
# |=========================================|                                  #
# |#########################################|                                  #
# |=========================================|            seduNdneS             #
# |#########################################|                                  #
# |-----------------------------------------|                                  #
# |                                                                            #
# |    Not Sure Add-on                                                         #
# |    Copyright (C) 2016 Exodus                                               #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################

from resources.lib.modules import control
control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))
