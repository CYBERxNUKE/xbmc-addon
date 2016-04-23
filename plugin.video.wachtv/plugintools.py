# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# Plugin Tools v1.0.8
#---------------------------------------------------------------------------
# Changelog:
# 1.0.4
# - Added get_temp_path, get_runtime_path, get_data_path
# - Added get_setting, set_setting, open_settings_dialog and get_localized_string
# - Added keyboard_input
# - Added message
# 1.0.5
# - Added read_body_and_headers for advanced http handling
# - Added show_picture for picture addons support
# - Added optional parameters "title" and "hidden" to keyboard_input
# 1.0.6
# - Added fanart, show, episode and infolabels to add_item
# 1.0.7
# - Added set_view function
# 1.0.8
# - Added selector
#---------------------------------------------------------------------------

import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui

import urllib
import urllib2
import re
import sys
import os
import time
import socket
from StringIO import StringIO
import gzip

module_log_enabled = False
http_debug_log_enabled = False

LIST = "list"
THUMBNAIL = "thumbnail"
MOVIES = "movies"
TV_SHOWS = "tvshows"
SEASONS = "seasons"
EPISODES = "episodes"
MUSIC = "music"
TV = "tvchannels"
OTHER = "other"
BIGLIST = "biglist"

# Skin Confluence
# List = 50, Full list = 51, Thumb = 500, Poster = 501, Posterwrap = 508, Info del medio 2 = 503, Info del medio 1 = 504, Media 4 = 515, Ancho = 505, Music Info = 511, AddoninfoList = 550, AddonThumbList = 551, LiveTV = 560
# Suggested view codes for each type from different skins (initial list thanks to xbmcswift2 library)
ALL_VIEW_CODES = {
    'list': {
        'skin.confluence': 50, # List
        'skin.aeon.nox': 50, # List
        'skin.droid': 50, # List
        'skin.quartz': 50, # List
        'skin.re-touched': 50, # List
		'skin.titan': 50,
    },
    'thumbnail': {
        'skin.confluence': 500, # Thumbnail
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 51, # Big icons
        'skin.re-touched': 500, #Thumbnail
		'skin.titan': 511, #Thumbs
    },
    'movies': {
        'skin.confluence': 508,  # Media info 3 (515), Movies (508)       
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 52, # Media info
        'skin.re-touched': 500, #Thumbnail
        'skin.neon': 588, # Multiplex
		'skin.titan': 52, #HorizontalPanel
    },
    'tvshows': {
        'skin.confluence': 515, # Thumbnail 515, # Media Info 3
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 52, # Media info
        'skin.re-touched': 500, #Thumbnail
        'skin.neon': 57, # Panel Landscape 
		'skin.titan': 512, #ThumbsDetails		
    },
    'seasons': {
        'skin.confluence': 50, # List
        'skin.aeon.nox': 50, # List
        'skin.droid': 50, # List
        'skin.quartz': 52, # Media info
        'skin.re-touched': 50, # List
		'skin.titan': 50, # 53_PanelDetails

    },
    'episodes': {
        'skin.confluence': 504, # Media Info
        'skin.aeon.nox': 518, # Infopanel
        'skin.droid': 50, # List
        'skin.quartz': 52, # Media info
        'skin.re-touched': 550, # Wide
		'skin.titan': 514, #PosterShift
    },
    'biglist': {
        'skin.confluence': 51, # Big list
        'skin.aeon.nox': 518, # NO DEFINIDO. BUSCAR CÓDIGO!
        'skin.droid': 50, # NO DEFINIDO. BUSCAR CÓDIGO!
        'skin.quartz': 52, # NO DEFINIDO. BUSCAR CÓDIGO!
        'skin.re-touched': 550, # NO DEFINIDO. BUSCAR CÓDIGO!
		'skin.titan': 514, # NO DEFINIDO. BUSCAR CÓDIGO!
    },     
}


# Write something on XBMC log
def log(message):
    xbmc.log(message)

# Write this module messages on XBMC log
def _log(message):
    if module_log_enabled:
        xbmc.log("plugintools."+message)

# Parse XBMC params - based on script.module.parsedom addon    
def get_params():
    _log("get_params")
    
    param_string = sys.argv[2]
    
    _log("get_params "+str(param_string))
    
    commands = {}

    if param_string:
        split_commands = param_string[param_string.find('?') + 1:].split('&')
    
        for command in split_commands:
            _log("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command:
                    split_command = command.split('=')
                    key = split_command[0]
                    value = urllib.unquote_plus(split_command[1])
                    commands[key] = value
                else:
                    commands[command] = ""
    
    _log("get_params "+repr(commands))
    return commands

# Fetch text content from an URL
def read(url):
    _log("read "+url)

    f = urllib2.urlopen(url)
    data = f.read()
    f.close()
    
    return data

def read_body_and_headers(url, post=None, headers=[], follow_redirects=False, timeout=None):
    _log("read_body_and_headers "+url)

    if post is not None:
        _log("read_body_and_headers post="+post)

    if len(headers)==0:
        headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"])

    # Start cookie lib
    ficherocookies = os.path.join( get_data_path(), 'cookies.dat' )
    _log("read_body_and_headers cookies_file="+ficherocookies)

    cj = None
    ClientCookie = None
    cookielib = None

    # Let's see if cookielib is available
    try:
        _log("read_body_and_headers importing cookielib")
        import cookielib
    except ImportError:
        _log("read_body_and_headers cookielib no disponible")
        # If importing cookielib fails
        # let's try ClientCookie
        try:
            _log("read_body_and_headers importing ClientCookie")
            import ClientCookie
        except ImportError:
            _log("read_body_and_headers ClientCookie not available")
            # ClientCookie isn't available either
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            _log("read_body_and_headers ClientCookie available")
            # imported ClientCookie
            urlopen = ClientCookie.urlopen
            Request = ClientCookie.Request
            cj = ClientCookie.MozillaCookieJar()

    else:
        _log("read_body_and_headers cookielib available")
        # importing cookielib worked
        urlopen = urllib2.urlopen
        Request = urllib2.Request
        cj = cookielib.MozillaCookieJar()
        # This is a subclass of FileCookieJar
        # that has useful load and save methods

    if cj is not None:
    # we successfully imported
    # one of the two cookie handling modules
        _log("read_body_and_headers Cookies enabled")

        if os.path.isfile(ficherocookies):
            _log("read_body_and_headers Reading cookie file")
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            try:
                cj.load(ficherocookies)
            except:
                _log("read_body_and_headers Wrong cookie file, deleting...")
                os.remove(ficherocookies)

        # Now we need to get our Cookie Jar
        # installed in the opener;
        # for fetching URLs
        if cookielib is not None:
            _log("read_body_and_headers opener using urllib2 (cookielib)")
            # if we use cookielib
            # then we get the HTTPCookieProcessor
            # and install the opener in urllib2
            if not follow_redirects:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=http_debug_log_enabled),urllib2.HTTPCookieProcessor(cj),NoRedirectHandler())
            else:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=http_debug_log_enabled),urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        else:
            _log("read_body_and_headers opener using ClientCookie")
            # if we use ClientCookie
            # then we get the HTTPCookieProcessor
            # and install the opener in ClientCookie
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    # -------------------------------------------------
    # Cookies instaladas, lanza la petición
    # -------------------------------------------------

    # Contador
    inicio = time.clock()

    # Diccionario para las cabeceras
    txheaders = {}

    # Construye el request
    if post is None:
        _log("read_body_and_headers GET request")
    else:
        _log("read_body_and_headers POST request")
    
    # Añade las cabeceras
    _log("read_body_and_headers ---------------------------")
    for header in headers:
        _log("read_body_and_headers header %s=%s" % (str(header[0]),str(header[1])) )
        txheaders[header[0]]=header[1]
    _log("read_body_and_headers ---------------------------")

    req = Request(url, post, txheaders)
    if timeout is None:
        handle=urlopen(req)
    else:        
        #Disponible en python 2.6 en adelante --> handle = urlopen(req, timeout=timeout)
        #Para todas las versiones:
        try:
            import socket
            deftimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)
            handle=urlopen(req)            
            socket.setdefaulttimeout(deftimeout)
        except:
            import sys
            for line in sys.exc_info():
                handle=urlopen(req)            
                _log( "%s" % line )
    
    # Actualiza el almacén de cookies
    cj.save(ficherocookies)

    # Lee los datos y cierra
    if handle.info().get('Content-Encoding') == 'gzip':
        buf = StringIO( handle.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data=handle.read()

    info = handle.info()
    _log("read_body_and_headers Response")

    returnheaders=[]
    _log("read_body_and_headers ---------------------------")
    for header in info:
        _log("read_body_and_headers "+header+"="+info[header])
        returnheaders.append([header,info[header]])
    handle.close()
    _log("read_body_and_headers ---------------------------")

    '''
    # Lanza la petición
    try:
        response = urllib2.urlopen(req)
    # Si falla la repite sustituyendo caracteres especiales
    except:
        req = urllib2.Request(url.replace(" ","%20"))
    
        # Añade las cabeceras
        for header in headers:
            req.add_header(header[0],header[1])

        response = urllib2.urlopen(req)
    '''
    
    # Tiempo transcurrido
    fin = time.clock()
    _log("read_body_and_headers Downloaded in %d seconds " % (fin-inicio+1))
    _log("read_body_and_headers body="+data)
	
    return data,returnheaders

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

# Parse string and extracts multiple matches using regular expressions
def find_multiple_matches(text,pattern):
    _log("find_multiple_matches pattern="+pattern)
    
    matches = re.findall(pattern,text,re.DOTALL)

    return matches
	
def find_multiple_matches_multi(text,pattern):
    _log("find_multiple_matches pattern="+pattern)
    
    matches = re.findall(pattern,text, re.MULTILINE)

    return matches	
	
def find_multiple_matches_multi_multi(text,pattern):
    _log("find_multiple_matches pattern="+pattern)
    
    matches = re.findall(pattern,text, re.MULTILINE|re.DOTALL)

    return matches

import htmlentitydefs
import re

pattern = re.compile("&(\w+?);")

def html_entity_decode_char(m, defs=htmlentitydefs.entitydefs):
    try:
        return defs[m.group(1)]
    except KeyError:
        return m.group(0)

def html_entity_decode(string):
    return pattern.sub(html_entity_decode_char, string)
	
# Parse string and extracts first match as a string
def find_single_match(text,pattern):
    _log("find_single_match pattern="+pattern)

    result = ""
    try:    
        matches = re.findall(pattern,text, flags=re.DOTALL)
        result = matches[0]
    except:
        result = ""

    return result

def add_item( action="" , title="" , plot="" , url="" , thumbnail="" , fanart="" , show="" , episode="" , extra="", page="", info_labels = "", isPlayable = False , folder=True ):
    _log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] fanart=["+fanart+"] show=["+show+"] episode=["+episode+"] extra=["+extra+"] page=["+page+"] isPlayable=["+str(isPlayable)+"] folder=["+str(folder)+"]")

    listitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", thumbnailImage=thumbnail )
    if info_labels is None:
        info_labels = { "Title" : title, "FileName" : title, "Plot" : plot }        
    listitem.setInfo( "video", info_labels )

    if fanart!="":
        listitem.setProperty('fanart_image',fanart)
        xbmcplugin.setPluginFanart(int(sys.argv[1]), fanart)
    
    if url.startswith("plugin://"):
        itemurl = url
        listitem.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
    elif isPlayable:
        listitem.setProperty("Video", "true")
        listitem.setProperty('IsPlayable', 'true')
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s&extra=%s&page=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( extra ) , urllib.quote_plus( page ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)
    else:
        itemurl = '%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s&extra=%s&page=%s' % ( sys.argv[ 0 ] , action , urllib.quote_plus( title ) , urllib.quote_plus(url) , urllib.quote_plus( thumbnail ) , urllib.quote_plus( plot ) , urllib.quote_plus( extra ) , urllib.quote_plus( page ))
        xbmcplugin.addDirectoryItem( handle=int(sys.argv[1]), url=itemurl, listitem=listitem, isFolder=folder)

    

       
   

def close_item_list():
    _log("close_item_list")

    xbmcplugin.endOfDirectory(handle=int(sys.argv[1]), succeeded=True)

def play_resolved_url(url):
    #_log("play_resolved_url ["+url+"]")

    listitem = xbmcgui.ListItem(path=url)
    listitem.setProperty('IsPlayable', 'true')
	
    return xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def direct_play(url):
    _log("direct_play ["+url+"]")

    title = ""

    try:
        xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", path=url)
    except:
        xlistitem = xbmcgui.ListItem( title, iconImage="DefaultVideo.png", )
    xlistitem.setInfo( "video", { "Title": title } )

    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    playlist.add( url, xlistitem )

    player_type = xbmc.PLAYER_CORE_AUTO
    xbmcPlayer = xbmc.Player( player_type )
    xbmcPlayer.play(playlist)

def show_picture(url):

    local_folder = os.path.join(get_data_path(),"images")
    if not os.path.exists(local_folder):
        try:
            os.mkdir(local_folder)
        except:
            pass
    local_file = os.path.join(local_folder,"temp.jpg")

    # Download picture
    urllib.urlretrieve(url, local_file)
    
    # Show picture
    xbmc.executebuiltin( "SlideShow("+local_folder+")" )

def get_temp_path():
    _log("get_temp_path")

    dev = xbmc.translatePath( "special://temp/" )
    _log("get_temp_path ->'"+str(dev)+"'")

    return dev

def get_runtime_path():
    _log("get_runtime_path")

    dev = xbmc.translatePath( __settings__.getAddonInfo('Path') )
    _log("get_runtime_path ->'"+str(dev)+"'")

    return dev

def get_data_path():
    _log("get_data_path")

    dev = xbmc.translatePath( __settings__.getAddonInfo('Profile') )
    
    # Parche para XBMC4XBOX
    if not os.path.exists(dev):
        os.makedirs(dev)

    _log("get_data_path ->'"+str(dev)+"'")

    return dev

def get_setting(name):
    _log("get_setting name='"+name+"'")

    dev = __settings__.getSetting( name )

    _log("get_setting ->'"+str(dev)+"'")

    return dev

def set_setting(name,value):
    _log("set_setting name='"+name+"','"+value+"'")

    __settings__.setSetting( name,value )

def open_settings_dialog():
    _log("open_settings_dialog")

    __settings__.openSettings()

def get_localized_string(code):
    _log("get_localized_string code="+str(code))

    dev = __language__(code)
    print dev

    try:
        dev = dev.encode("utf-8")
	#data=body.encode("iso-8859-16")
	#data=unicode(body.decode("utf-8"),"iso-8859-16")
	#s = stripped.encode("iso 8859-16")
	#s = unicode( s, "iso-8859-16" )
    except:
        pass

    _log("get_localized_string ->'"+dev+"'")

    return dev

def keyboard_input(default_text="", title="", hidden=False):
    _log("keyboard_input default_text='"+default_text+"'")

    keyboard = xbmc.Keyboard(default_text,title,hidden)
    keyboard.doModal()
    
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
    else:
        tecleado = ""

    _log("keyboard_input ->'"+tecleado+"'")

    return tecleado

def message(text1, text2="", text3=""):
    _log("message text1='"+text1+"', text2='"+text2+"', text3='"+text3+"'")

    if text3=="":
        xbmcgui.Dialog().ok( text1 , text2 )
    elif text2=="":
        xbmcgui.Dialog().ok( "" , text1 )
    else:
        xbmcgui.Dialog().ok( text1 , text2 , text3 )

def message_yes_no(text1, text2="", text3=""):
    _log("message_yes_no text1='"+text1+"', text2='"+text2+"', text3='"+text3+"'")

    if text3=="":
        yes_pressed = xbmcgui.Dialog().yesno( text1 , text2 )
    elif text2=="":
        yes_pressed = xbmcgui.Dialog().yesno( "" , text1 )
    else:
        yes_pressed = xbmcgui.Dialog().yesno( text1 , text2 , text3 )

    return yes_pressed

def selector(option_list,title="Select one"):
    _log("selector title='"+title+"', options="+repr(option_list))

    dia = xbmcgui.Dialog()
    selection = dia.select(title,option_list)
    return selection

def set_view(view_mode, view_code=0):
    _log("set_view view_mode='"+view_mode+"', view_code="+str(view_code))

    # Set the content for extended library views if needed
    if view_mode==MOVIES:
        _log("set_view content is movies")
        xbmcplugin.setContent( int(sys.argv[1]) ,"movies" )
    elif view_mode==TV_SHOWS:
        _log("set_view content is tvshows")
        xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
    elif view_mode==SEASONS:
        _log("set_view content is seasons")
        xbmcplugin.setContent( int(sys.argv[1]) ,"seasons" )
    elif view_mode==EPISODES:
        _log("set_view content is episodes")
        xbmcplugin.setContent( int(sys.argv[1]) ,"episodes" )
    elif view_mode==TV:
        _log("set_view content is channels")
        xbmcplugin.setContent( int(sys.argv[1]) ,"channels" )
    elif view_mode==MUSIC:
        _log("set_view content is music")
        xbmcplugin.setContent( int(sys.argv[1]) ,"music" )
    elif view_mode==BIGLIST:
        _log("set_view content is biglist")
        xbmcplugin.setContent( int(sys.argv[1]) ,"biglist" )        
      

    # Reads skin name
    skin_name = xbmc.getSkinDir()
    _log("set_view skin_name='"+skin_name+"'")

    try:
        if view_code==0:
            _log("set_view view mode is "+view_mode)
            view_codes = ALL_VIEW_CODES.get(view_mode)
            view_code = view_codes.get(skin_name)
            _log("set_view view code for "+view_mode+" in "+skin_name+" is "+str(view_code))
            xbmc.executebuiltin("Container.SetViewMode("+str(view_code)+")")
        else:
            _log("set_view view code forced to "+str(view_code))
            xbmc.executebuiltin("Container.SetViewMode("+str(view_code)+")")
    except:
        _log("Unable to find view code for view mode "+str(view_mode)+" and skin "+skin_name)

f = open( os.path.join( os.path.dirname(__file__) , "addon.xml") )
data = f.read()
f.close()

addon_id = find_single_match(data,'id="([^"]+)"')
if addon_id=="":
    addon_id = find_single_match(data,"id='([^']+)'")

__settings__ = xbmcaddon.Addon(id=addon_id)
__language__ = __settings__.getLocalizedString


def modo_vista(show):

    if show == "":
        show = "list"
    elif show == "0":
        show = "movies"
    elif show == "1":
        show = "seasons"
    elif show == "2":
        show = "fanart"
    elif show == "3":
        show = "list"
    elif show == "4":
        show = "thumbnail"
    elif show == "5":
        show = "movies"
    elif show == "6":
        show = "tvshows"
    elif show == "7":
        show = "episodes"
    elif show == "8":
        show = "biglist"         

    if show == "music":        
        set_view(THUMBNAIL)
    elif show == "series":
        set_view(THUMBNAIL)
    elif show == "tvshows":
        set_view(THUMBNAIL)
    elif show == "thumbnail":
        set_view(THUMBNAIL)
    elif show == "movies":
        set_view(THUMBNAIL)
    elif show == "list":
        set_view(LIST)
    elif show == "seasons":
        set_view(THUMBNAIL)
    elif show == "episodes":
        set_view(THUMBNAIL)
    elif show == "tvshows":
        set_view(TTHUMBNAIL)
    elif show == "biglist":
        set_view(THUMBNAIL)
    else:
        set_view(LIST)


