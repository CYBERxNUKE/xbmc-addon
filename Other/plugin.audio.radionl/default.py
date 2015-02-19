#-*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import urllib,re,string,os,time,threading

#try:
#    from resources.libs import main, settings
#except Exception, e:
#    dialog = xbmcgui.Dialog()
#    ok=dialog.ok('[B][COLOR=FF67cc33]RadioNL Import Error[/COLOR][/B]','Failed To Import Needed Modules',str(e),'Main and Settings module')
#    xbmc.log('RadioNL ERROR - Importing Modules: '+str(e), xbmc.LOGERROR)

#################### Set Environment ######################
ENV = "Dev"  # "Prod" or "Dev"
###########################################################

ADDON = xbmcaddon.Addon(id='plugin.audio.radionl')
PATH = 'radionl'
VERSION = '1.0.1'

base_url = ''
addon_handle = ''

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])

def getStreams():
    radiostreams={}
    radiostreams[0] = ['3FM',                   '/logos/3fm.png',             'http://icecast.omroep.nl/3fm-bb-mp3']
    radiostreams[1] = ['Q-Music',               '/logos/q-music.jpg',         'http://icecast-qmusic.cdp.triple-it.nl/Qmusic_nl_live_96.mp3']
    radiostreams[2] = ['Q-Music Non Stop',      '/logos/q-music.jpg',         'http://icecast-qmusic.cdp.triple-it.nl/Qmusic_nl_nonstop_96.mp3']
    radiostreams[3] = ['100% NL',               '/logos/100-procent-nl.jpg',  'http://stream.100p.nl:8000/100pctnl.mp3']
    radiostreams[4] = ['Arrow Classic Rock',    '/logos/arrow.png',           'http://www.arrow.nl/streams/Rock128kmp3.pls']
    radiostreams[5] = ['Radio 10',              '/logos/q-music.jpg',         'http://www.radio10.nl/players/stream/radio10.pls']
    radiostreams[6] = ['Radio 538',             '/logos/radio-538.jpg',       'http://82.201.100.9:8000/radio538']
    radiostreams[7] = ['Skyradio',              '/logos/skyradio.jpg',        'http://www.skyradio.nl/player/skyradio.pls']
    radiostreams[8] = ['Studio Brussel',        '/logos/studio-brussel.jpg',  'http://mp3.streampower.be/stubru-high.mp3']
    radiostreams[9] = ['Radio Veronica',        '/logos/radioveronica.jpg',   'http://www.radioveronica.nl/player/radioveronica.pls']
    return radiostreams

def addDirItem(url, name, image):
    if image == '':
        image = 'DefaultFolder.png'
    item = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=item, isFolder=False)
	
def findStream(name):
    radiostreams = getStreams()
    if name in radiostreams:
        return radiostreams[name]
    return ''

def getKeyboardInput():
    keyboard = xbmc.Keyboard('')
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        return keyboard.getText()

def home():
    radiostreams = getStreams()
    for radio in radiostreams:
        addDirItem(radiostreams[radio][2], radiostreams[radio][0].encode("utf-8"), ADDON.getAddonInfo('path') + radiostreams[radio][1])
    xbmcplugin.endOfDirectory(addon_handle)

######## PARAMS and stuff ########
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
plot=None
genre=None
title=None
season=None
episode=None
location=None
path=None

try: name=urllib.unquote_plus(params["name"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: mode=int(params["mode"])
except: pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except: pass
try: plot=urllib.unquote_plus(params["plot"])
except: pass
try:
    fanart=urllib.unquote_plus(params["fanart"])
    fanart = fanart.replace(' ','%20')
except: pass
try: genre=urllib.unquote_plus(params["genre"])
except: pass
try: title=urllib.unquote_plus(params["title"])
except: pass
try: episode=int(params["episode"])
except: pass
try: season=int(params["season"])
except: pass
try: location=urllib.unquote_plus(params["location"])
except: pass
try: path=urllib.unquote_plus(params["path"])
except: pass

if mode==None or url==None or len(url)<1:
    home()

xbmcplugin.endOfDirectory(int(sys.argv[1]))