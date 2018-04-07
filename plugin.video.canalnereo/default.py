# -*- coding: utf-8 -*-
#------------------------------------------------------------
#Catoal Kodi Addon
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Based on code from youtube addon
#------------------------------------------------------------

import os
import sys
import plugintools
import xbmc,xbmcaddon
from addon.common.addon import Addon

addonID = 'plugin.video.canalnereo'
addon = Addon(addonID, sys.argv)
local = xbmcaddon.Addon(id=addonID)
icon = local.getAddonInfo('icon')

YOUTUBE_CHANNEL_ID_1 = "UCH4cb8IIJmqnRTiz06l60RA"
YOUTUBE_CHANNEL_ID_2 = "UCH4cb8IIJmqnRTiz06l60RA"
YOUTUBE_CHANNEL_ID_3 = "UCH4cb8IIJmqnRTiz06l60RA"
YOUTUBE_CHANNEL_ID_4 = "UCH4cb8IIJmqnRTiz06l60RA"
YOUTUBE_CHANNEL_ID_5 = "UCH4cb8IIJmqnRTiz06l60RA"
YOUTUBE_CHANNEL_ID_6 = "UCH4cb8IIJmqnRTiz06l60RA"
YOUTUBE_CHANNEL_ID_7 = "UCH4cb8IIJmqnRTiz06l60RA"

# Entry point
def run():
    plugintools.log("docu.run")
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
        action = params.get("action")
        exec action+"(params)"
    
    plugintools.close_item_list()

# Main menu
def main_list(params):
    plugintools.log("docu.main_list "+repr(params))

    plugintools.add_item( 
        #action="", 
        title="                                           [COLOR skyblue]Bienvenidos a mi Addon.[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_1+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="                                  [COLOR skyblue]Entra en el mundo de los Tuturiales[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_2+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="                                [COLOR skyblue]Kodi, Addon , Repositorios , buscamos[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_3+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="                                [COLOR skyblue]lo nuevo de Kodi y lo traemos al canal.[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_4+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="                           [COLOR red]No olvides suscribirte a mi Canal de You Tube[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_5+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True )

    plugintools.add_item( 
        #action="", 
        title="                                            [COLOR skyblue]7 segundos y comenzamos.[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_6+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True ) 
		
    plugintools.add_item( 
        #action="", 
        title="                                               [COLOR lime]***** COMENZAR *****[/COLOR]",
        url="plugin://plugin.video.youtube/channel/"+YOUTUBE_CHANNEL_ID_7+"/",
        thumbnail="https://yt3.ggpht.com/-UO0xuh1LWMI/AAAAAAAAAAI/AAAAAAAAAAA/qAoD8rKP_j4/s100-c-k-no-mo-rj-c0xffffff/photo.jpg",
		fanart="https://yt3.ggpht.com/-OZJczfDb27I/VrkSeaJsc9I/AAAAAAAAAJQ/raK5bcqRe_Q/w2120-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no/portada%2Bcanal.jpg",
        folder=True ) 
		
run()
