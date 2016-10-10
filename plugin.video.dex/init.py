import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,datetime,os,json,base64,plugintools,requests,time
import xml.etree.ElementTree as ElementTree
reload(sys)
sys.setdefaultencoding('utf8')
SKIN_VIEW_FOR_MOVIES="515"
addonDir = plugintools.get_runtime_path()
dialog = xbmcgui.Dialog()
thumbnailPath = xbmc.translatePath('special://thumbnails');
cachePath = os.path.join(xbmc.translatePath('special://home'), 'cache')
tempPath = xbmc.translatePath('special://temp')
addonPath = os.path.join(os.path.join(xbmc.translatePath('special://home'), 'addons'),'plugin.video.dex')
mediaPath = os.path.join(addonPath, 'media')
databasePath = xbmc.translatePath('special://database')


class cacheEntry:
    def __init__(self, namei, pathi):
        self.name = namei
        self.path = pathi

global kontroll
background = "YmFja2dyb3VuZC5wbmc="
defaultlogo = "ZGVmYXVsdGxvZ28ucG5n"
hometheater = "aG9tZXRoZWF0ZXIuanBn"
noposter = "bm9wb3N0ZXIuanBn"
theater = "dGhlYXRlci5qcGc="
addonxml = "YWRkb24ueG1s"
addonpy = "ZGVmYXVsdC5weQ=="
icon = "aWNvbi5wbmc="
fanart = "ZmFuYXJ0LnBuZw=="
message = "V2VsY29tZSBUbyBEZXh0ZXI="
fanart2 = "fHVzZXItYWdlbnQ9UGlwY2Fu"
ADDON = xbmcaddon.Addon(id='plugin.video.dex')
first=xbmcplugin.getSetting(int(sys.argv[1]), 'first')
kasutajanimi=xbmcplugin.getSetting(int(sys.argv[1]), 'kasutajanimi')
salasona=xbmcplugin.getSetting(int(sys.argv[1]), 'salasona')
showmenu=xbmcplugin.getSetting(int(sys.argv[1]), 'showmenu')
addon = xbmcaddon.Addon(id='plugin.video.dex')
addon_path = addon.getAddonInfo('path')
addon_userdata = xbmc.translatePath(addon.getAddonInfo('profile')).decode('utf-8')
addon_name = addon.getAddonInfo('name')
ADDON_ID   = 'plugin.video.dex'
HOME       =  ADDON.getAddonInfo('path')
repoversion = addon.getAddonInfo('version')

max_Bps = 0.0
currently_downloaded_bytes = 0.0
def login(params):
    searchStr = ''
    keyboard = xbmc.Keyboard(searchStr, 'Search')
    keyboard.doModal()
    searchStr=keyboard.getText()    
    restart_service(searchStr)

def run():
    global pnimi
    global televisioonilink
    global andmelink
    global uuenduslink
    global lehekylg1
    global LOAD_LIVE
    global uuendused
    global vanemalukk
    global version
    version = int("3")
    kasutajanimi=plugintools.get_setting(get_live("a2FzdXRhamFuaW1p"))
    salasona=plugintools.get_setting(vod_channels("c2FsYXNvbmE="))
    lehekylg1=plugintools.get_setting(vod_channels("bGVoZWt5bGcx"))
    pordinumber=plugintools.get_setting(get_live("cG9yZGludW1iZXI="))
    uuendused=plugintools.get_setting(sync_data("dXVlbmR1c2Vk"))
    vanemalukk=plugintools.get_setting(sync_data("dmFuZW1hbHVraw=="))
    pnimi = get_live("RGV4dGVyUHJvIA==")
    LOAD_LIVE = os.path.join( plugintools.get_runtime_path() , get_live("cmVzb3VyY2Vz") , vod_channels("YXJ0") )
    televisioonilink = get_live("JXM6JXMvZW5pZ21hMi5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmdHlwZT1nZXRfbGl2ZV9jYXRlZ29yaWVz")%(lehekylg1,pordinumber,kasutajanimi,salasona)
    andmelink = vod_channels("JXM6JXMvcGFuZWxfYXBpLnBocD91c2VybmFtZT0lcyZwYXNzd29yZD0lcw==")%(lehekylg1,pordinumber,kasutajanimi,salasona)
    uuenduslink = ("http://158.69.54.54/plugin.video.dex.zip")
    if get_live("RGV4dGVyUHJv") not in open(addonDir+"/"+sync_data("YWRkb24ueG1s")).read():
       check_user(params)
    params = plugintools.get_params()
    
    if params.get("action") is None:
        peamenyy(params)
    else:
        action = params.get("action")
        exec action+"(params)"

    plugintools.close_item_list()
def clearpackage(params):
    dialog = xbmcgui.Dialog()
    r = os.listdir(addon_userdata+'../../../addons/packages')
    for i in r:
        os.remove(addon_userdata+'../../../addons/packages'+'/'+i)
    dialog.ok('All Done','Your Packages Are Cleared')
def peamenyy(params):
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
    plugintools.add_item( action="News", title='News' , url='', thumbnail='', plot='', fanart=os.path.join(LOAD_LIVE,"dGhlYXRlci5qcGc=") , extra="", isPlayable=False, folder=True )
    plugintools.add_item( action="Radio", title='Radio' , url='', thumbnail='', plot='', fanart=os.path.join(LOAD_LIVE,"dGhlYXRlci5qcGc=") , extra="", isPlayable=False, folder=True )
    plugintools.add_item( action="TOOLS", title='Tools' , url='http://ovh.net/files/100Mio.dat', thumbnail='', plot='', fanart='' , extra="", isPlayable=False, folder=True )
    plugintools.log(pnimi+vod_channels("TWFpbiBNZW51")+repr(params))
    load_channels()
    if not lehekylg1:
       plugintools.open_settings_dialog()
    if uuendused == "true":
       updates(params)
    channels = kontroll()
    if channels == 1:
       plugintools.log(pnimi+vod_channels("TG9naW4gU3VjY2Vzcw=="))
       plugintools.add_item( action=vod_channels("ZXhlY3V0ZV9haW5mbw=="),   title=vod_channels("TXkgQWNjb3VudA==") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=True )
       plugintools.add_item( action=vod_channels("c2VjdXJpdHlfY2hlY2s="),  title=vod_channels("TGl2ZSBUVg==") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=True )
       plugintools.add_item( action=vod_channels("cnVubmVyMg=="),   title=vod_channels("VmlkZW8gT24gRGVtYW5k") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
       plugintools.add_item( action=vod_channels("bGljZW5zZV9jaGVjaw=="), title=vod_channels("U2V0dGluZ3M=") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=") ), folder=False )
       plugintools.set_view( plugintools.LIST )
    else:
       plugintools.log(pnimi+vod_channels("TG9naW4gZmFpbGVk"))
       plugintools.message(("Login failed"),("Possible reasons: Wrong host,port,username or pass.          Please reconfigure %s plugin with correct details!")%(pnimi))
       exit()  
    if plugintools.get_setting("improve")=="true":
        tseaded = xbmc.translatePath(sync_data("c3BlY2lhbDovL3VzZXJkYXRhL2FkdmFuY2Vkc2V0dGluZ3MueG1s"))
        tseaded = xbmc.translatePath(sync_data("c3BlY2lhbDovL3VzZXJkYXRhL2FkdmFuY2Vkc2V0dGluZ3MueG1s"))
        if not os.path.exists(tseaded):
            file = open( os.path.join(plugintools.get_runtime_path(),"resources",sync_data("YWR2YW5jZWRzZXR0aW5ncy54bWw=")) )
            data = file.read()
            file.close()
            file = open(tseaded,"w")
            file.write(data)
            file.close()
            plugintools.message(pnimi, "New advanced streaming settings added.")

def ovh(params):
    ret = dialog.select('Choose a Action', ['Canada Server','EU Server'])
    if ret == 0:
        DownloaderClass('http://ovh.net/files/10Mio.dat',addon_userdata+'pip.zip')

    if ret == 1:
        DownloaderClass('http://ovh.net/files/100Mb.dat',addon_userdata+'pip.zip')
def killxbmc(params):
    choice = xbmcgui.Dialog().yesno('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Pulling the power cable is the simplest method to force close.")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'           
def createini(params):
    u =  ADDON.getSetting('kasutajanimi')
    p =  ADDON.getSetting('salasona')
    dialog = xbmcgui.Dialog()
    with open(addonDir+"/DEXTER.ini", "w") as f:
        url = ('http://158.69.54.54:8000/panel_api.php?username=%s&password=%s'%(u,p))
        r = requests.get(url)
        match=re.compile('"name":"(.+?)".+?stream_id":"(.+?)"').findall(r.content)
        f.write('[plugin.video.dex]\n')
        for name,stream in match:
            f.write(name+'=http://158.69.54.54:8000/%s/%s/'%(u,p)+stream+'.m3u8\n')
        f.close()
        dialog.ok('All Done','This Feature Is Not Backed By Dexter And Will Not Offer Support Please Contact The Guide You Are Using For Help Questions On This Will Be Ignored')
    dialog.ok("Restart XBMC", "Please restart XBMC to rebuild thumbnail library")

def inifile(url):
        username =  ADDON.getSetting('kasutajanimi')
        password =  ADDON.getSetting('salasona')
        play=xbmc.Player(GetPlayerCore())
        dp = xbmcgui.DialogProgress()
        dp.create('Featching Your Video','g')
        dp.close()
        play.play('http://158.69.54.54:8000/live/%s/%s/%s.m3u8'%(username,password,url))
def license_check(params):
    plugintools.log(pnimi+get_live("U2V0dGluZ3MgbWVudQ==")+repr(params))
    plugintools.open_settings_dialog()
def security_check(params):
    plugintools.log(pnimi+sync_data("TGl2ZSBNZW51")+repr(params))
    request = urllib2.Request(televisioonilink, headers={"Accept" : "application/xml"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
        kanalinimi = channel.find(get_live("dGl0bGU=")).text
        kanalinimi = base64.b64decode(kanalinimi)
        kategoorialink = channel.find(vod_channels("cGxheWxpc3RfdXJs")).text
        if 'All' in kanalinimi:
            kanalinimi = '-- [COLOR deepskyblue][B]'+'ALL CHANNELS'+'[/B][/COLOR] --'
        plugintools.add_item( action=get_live("c3RyZWFtX3ZpZGVv"), title=kanalinimi , url=kategoorialink , thumbnail='' , fanart="" , folder=True )
    plugintools.set_view( plugintools.LIST )

def stream_video(params):
    if get_live("WHRyZWFtLUNvZGVz") not in open(addonDir+"/"+sync_data("YWRkb24ueG1s")).read():
       check_user(params)
    if vanemalukk == "true":
       pealkiri = params.get(sync_data("dGl0bGU="))
       vanema_lukk(pealkiri)
    url = params.get(get_live("dXJs"))
    request = urllib2.Request(url, headers={"Accept" : "application/xml"})
    u = urllib2.urlopen(request)
    tree = ElementTree.parse(u)
    rootElem = tree.getroot()
    for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
        kanalinimi = channel.find(get_live("dGl0bGU=")).text
        kanalinimi = base64.b64decode(kanalinimi)
        kanalinimi = kanalinimi.partition("[")
        striimilink = channel.find(get_live("c3RyZWFtX3VybA==")).text
        pilt = channel.find(vod_channels("ZGVzY19pbWFnZQ==")).text
        kava = kanalinimi[1]+kanalinimi[2]
        kava = kava.partition("]")
        kava = kava[2]
        kava = kava.partition("   ")
        kava = kava[2]
        shou = get_live("W0NPTE9SIHdoaXRlXVtCXSVzWy9CXSBbL0NPTE9SXQ==")%(kanalinimi[0])+'[COLOR gold]'+kava+'[/COLOR]'
        extras = kava
        kirjeldus = channel.find(sync_data("ZGVzY3JpcHRpb24=")).text
        if kirjeldus:
           kirjeldus = base64.b64decode(kirjeldus)
           nyyd = kirjeldus.partition("(")

           kokku = kirjeldus
        else:
           kokku = ""
        try:
                xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE )
                if pilt:
                    if showmenu == 'true':
                        plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=striimilink.replace('\.ts','\.m3u8'), thumbnail=pilt, plot='[B]'+kokku+'[/B]', fanart='http://localhost:52307/getpvrthumb&title=%s'%(kava), extra=kava, isPlayable=False, folder=False )
                    else:
                        plugintools.add_item( action=sync_data("cmVzdGFydF9zZXJ2aWNl"), title=shou , url=striimilink.replace('\.ts','\.m3u8'), thumbnail=pilt, plot='[B]'+kokku+'[/B]', fanart='http://localhost:52307/getpvrthumb&title=%s'%(kava), extra=kava, isPlayable=True, folder=False )
                else:
                    if showmenu == 'true':

                        plugintools.add_item( action=sync_data("cnVuX2Nyb25qb2I="), title=shou , url=striimilink.replace('\.ts','\.m3u8'), thumbnail=os.path.join(LOAD_LIVE,sync_data("ZGVmYXVsdGxvZ28ucG5n")) , plot='[B]'+kokku+'[/B]', fanart='http://localhost:52307/getpvrthumb&title=%s'%(kava) , extra=kava, isPlayable=False, folder=False )
                    else:
                        plugintools.add_item( action=sync_data("cmVzdGFydF9zZXJ2aWNl"), title=shou , url=striimilink.replace('\.ts','\.m3u8'), thumbnail=os.path.join(LOAD_LIVE,sync_data("ZGVmYXVsdGxvZ28ucG5n")) , plot='[B]'+kokku+'[/B]', fanart='http://localhost:52307/getpvrthumb&title=%s'%(kava) , extra=kava, isPlayable=True, folder=False )

        except:
            pass
    plugintools.set_view( plugintools.EPISODES )
    xbmc.executebuiltin(vod_channels("Q29udGFpbmVyLlNldFZpZXdNb2RlKDUwMyk="))
def get_myaccount(params):
        plugintools.log(pnimi+get_live("Vk9EIGNoYW5uZWxzIG1lbnUg")+repr(params))
        if vanemalukk == "true":
           pealkiri = params.get(sync_data("dGl0bGU="))
           vanema_lukk(pealkiri)
        purl = params.get(get_live("dXJs"))
        request = urllib2.Request(purl, headers={"Accept" : "application/xml"})
        u = urllib2.urlopen(request)
        tree = ElementTree.parse(u)
        rootElem = tree.getroot()
        for channel in tree.findall(sync_data("Y2hhbm5lbA==")):
            pealkiri = channel.find(get_live("dGl0bGU=")).text
            pealkiri = base64.b64decode(pealkiri)
            pealkiri = pealkiri.encode("utf-8")
            striimilink = channel.find("stream_url").text
            pilt = channel.find(sync_data("ZGVzY19pbWFnZQ==")).text 
            kirjeldus = channel.find(vod_channels("ZGVzY3JpcHRpb24=")).text
            if kirjeldus:
               kirjeldus = base64.b64decode(kirjeldus) 
            if pilt:
               plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=pilt, plot=kirjeldus, fanart=os.path.join(LOAD_LIVE,"theater.jpg") , extra="", isPlayable=True, folder=False )
            else:
               plugintools.add_item( action="restart_service", title=pealkiri , url=striimilink, thumbnail=os.path.join(LOAD_LIVE,"noposter.jpg"), plot=kirjeldus, fanart="" , extra="", isPlayable=True, folder=False )
        plugintools.set_view( plugintools.MOVIES )
        xbmc.executebuiltin('Container.SetViewMode(515)')
def runner(params):
    xbmc.executebuiltin("RunScript(script.matchcenter)")
def runner2(params):
    xbmc.executebuiltin("RunScript(script.extendedinfo)")
def runtest(params):
    DownloaderClass('http://ovh.net/files/100Mio.dat',HOME)

def deleteThumbnails(params):
    
    if os.path.exists(thumbnailPath)==True:  
            dialog = xbmcgui.Dialog()
            if dialog.yesno("Delete Thumbnails", "This option deletes all thumbnails", "Are you sure you want to do this?"):
                for root, dirs, files in os.walk(thumbnailPath):
                    file_count = 0
                    file_count += len(files)
                    if file_count > 0:                
                        for f in files:
                            try:
                                os.unlink(os.path.join(root, f))
                            except:
                                pass                
    else:
        pass
    
    text13 = os.path.join(databasePath,"Textures13.db")
    os.unlink(text13)
        
    dialog.ok("Restart XBMC", "Please restart XBMC to rebuild thumbnail library")
        
def clearCache(params):
    
    if os.path.exists(cachePath)==True:    
        for root, dirs, files in os.walk(cachePath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete XBMC Cache Files", str(file_count) + " files found", "Do you want to delete them?"):
                
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if os.path.exists(tempPath)==True:    
        for root, dirs, files in os.walk(tempPath):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete XBMC Temp Files", str(file_count) + " files found", "Do you want to delete them?"):
                    for f in files:
                        try:
                            if (f == "xbmc.log" or f == "xbmc.old.log"): continue
                            os.unlink(os.path.join(root, f))
                        except:
                            pass
                    for d in dirs:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass
                        
            else:
                pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'Other'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')
        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
        
            if file_count > 0:

                dialog = xbmcgui.Dialog()
                if dialog.yesno("Delete ATV2 Cache Files", str(file_count) + " files found in 'LocalAndRental'", "Do you want to delete them?"):
                
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))
                        
            else:
                pass    
                
    cacheEntries = setupCacheEntries()
                                         
    for entry in cacheEntries:
        clear_cache_path = xbmc.translatePath(entry.path)
        if os.path.exists(clear_cache_path)==True:    
            for root, dirs, files in os.walk(clear_cache_path):
                file_count = 0
                file_count += len(files)
                if file_count > 0:

                    dialog = xbmcgui.Dialog()
                    if dialog.yesno("Delete Cashe",str(file_count) + "%s cache files found"%(entry.name), "Do you want to delete them?"):
                        for f in files:
                            os.unlink(os.path.join(root, f))
                        for d in dirs:
                            shutil.rmtree(os.path.join(root, d))
                            
                else:
                    pass
                

    dialog = xbmcgui.Dialog()
    dialog.ok("DexterPro Tools", "Done Clearing Cache files")
    
    
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
def online(params):
    url = 'http://158.69.54.54/stream.php'
    r = requests.get(url)
    match = re.compile('<img src="(.+?)" width="73" height="78" />(.+?)&.+?fps"(.+?),.+?out_time":"(\d\d:\d\d:\d\d).+?".+?speed":"(.+?)x.+?>(.+?),',re.DOTALL).findall(r.content)
    for image,name,fps,uptime,speed,server in match:
        server = server.replace('14','US').replace('11','  -   EU').replace('10','  -   CA').replace('3','  -   EU').replace('9','  -   EU')
        if uptime < '00:30:00':
            uptime = '[COLOR red]'+uptime+'[/COLOR]'
        else:
            uptime = '[COLOR gold]'+uptime+'[/COLOR]'

        if speed < '1':
            if 'button-red' in image:
                addDir('[B]'+name+'[/B]  -   [COLOR orange][MAY BUFFER][/COLOR]'+' '+server+' - '+uptime,'','','http://www.clker.com/cliparts/W/i/K/w/1/D/glossy-orange-circle-icon-hi.png')
            else:
                addDir('[B]'+name+'[/B]  -   [COLOR red][Offline][/COLOR]'+' '+server+' - '+uptime,'','','http://www.iconattitude.com/icons/open_icon_library/others/png/256/button-red.png')

        elif speed >= '1':
            if 'button-red' in image:
                addDir('[B]'+name+'[/B]  -   [COLOR orange][MAY BUFFER][/COLOR]'+' '+server+' - '+uptime,'','','http://www.clker.com/cliparts/W/i/K/w/1/D/glossy-orange-circle-icon-hi.png')
            else:
                addDir('[B]'+name+'[/B]  -   [COLOR green][Healthy][/COLOR]'+' '+server+' - '+uptime,'','',image)
        else:
                addDir('[B]'+name+'[/B]  -   [COLOR orange][MAY BUFFER][/COLOR]'+' '+server+' - '+uptime,'','','http://www.clker.com/cliparts/W/i/K/w/1/D/glossy-orange-circle-icon-hi.png')
def upandcoming(params):
    url = 'http://www.wheresthematch.com/tv/home.asp'
    r = requests.get(url)
    match = re.compile('http://www\.wheresthematch\.com/fixtures/(.+?)\..+?channelid.+?">(.+?)<em class="livestream">Live Stream</em></a></span> <span class="ground">(.+?)</span>').findall(r.content)
    for game,image,name in match:
        addDir('[COLOR green]'+game+' [/COLOR]'+image+' '+'[COLOR yellow]'+name+'[/COLOR]','','','')


def run_cronjob(params):
    showmenu = ADDON.getSetting('showmenu')
    extent =  ADDON.getSetting('extention')
    lopplink = params.get(vod_channels("dXJs"))
    lopplink2 = params.get(vod_channels("dGl0bGU="))
    pealkiri = params.get(sync_data("ZXh0cmE="))
    lopplink = lopplink.replace('ts','%s'%(extent))
    if showmenu == 'true':
        dialog = xbmcgui.Dialog()
        ret = dialog.select('Choose a Action', ['[B]Play Live[/B]', '-------------[COLOR yellow][B]ONDEMAND[/B][/COLOR]----------','[COLOR gold]Movie[/COLOR] Search '+pealkiri+' On-Demand','[COLOR gold]TV Show[/COLOR] Search  '+pealkiri+' On-Demand'])
        if ret == 0:
            PLAYING(lopplink)
        if ret == 1:
            PLAYING(lopplink)
        if ret == 2:
            search(pealkiri)
        if ret == 3:
            search2(pealkiri)
        if ret == None:
            return
    
    else:
        PLAYING(lopplink)

def messages(params):
        l = []
        f = []
        u =  ADDON.getSetting('kasutajanimi')
        p =  ADDON.getSetting('salasona')
        r = requests.get('http://158.69.54.54/messages.php?username=%s&password=%s'%(u,p))
        b = re.compile('<p>(.+?)</p><p>(.+?)<p>(.+?)</p><p>(.+?)</p>').findall(r.content)
        for a,c,d,sby in b:
            k = l.append(a)
            g = f.append(c)
        dp = xbmcgui.Dialog()
        ret = dp.select('Message',l)
        if ret == ret:
			choice = xbmcgui.Dialog().yesno(l[ret],f[ret], '\n-----------[COLOR yellow][B]Date And Time[/B][/COLOR]-----------------------------[COLOR yellow][B]Sent By[/B][/COLOR]----------------\n------ %s ------------------ %s --------\n'%(d,sby), nolabel='Delete',yeslabel='Reply')
        if ret == None:
            return
def keyboard_input(default_text="", title="", hidden=False):
    keyboard = xbmc.Keyboard(default_text,title,hidden)
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        tecleado = keyboard.getText()
    else:
        tecleado = ""
    return tecleado
def setupCacheEntries():
    entries = 5 #make sure this refelcts the amount of entries you have
    dialogName = ["MP3 Streams", "4oD", "BBC iPlayer", "Simple Downloader", "ITV"]
    pathName = ["special://profile/addon_data/plugin.audio.mp3streams/temp_dl", "special://profile/addon_data/plugin.video.4od/cache",
					"special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache","special://profile/addon_data/script.module.simple.downloader",
                    "special://profile/addon_data/plugin.video.itv/Images"]
                    
    cacheEntries = []
    
    for x in range(entries):
        cacheEntries.append(cacheEntry(dialogName[x],pathName[x]))
    
    return cacheEntries


def TOOLS(params): 
    plugintools.add_item( action="ovh", title='SpeedTest' , url='http://ovh.net/files/100Mio.dat', thumbnail='', plot='', fanart='' , extra="", isPlayable=False, folder=False )
    plugintools.add_item( action="createini", title='Create INI' , url='', thumbnail='', plot='', fanart='' , extra="", isPlayable=False, folder=False )
    plugintools.add_item( action=vod_channels("b25saW5l"),   title=vod_channels("Q2hhbm5lbCBTdGF0dXM=") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=True )
    plugintools.add_item( action=vod_channels("YWR2YW5jZQ=="),   title=vod_channels("VXNlIEFkdmFuY2Vk") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("Y2xlYXJDYWNoZQ=="),   title=vod_channels("Q2xlYXIgQ2FzaGU=") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("ZGVsZXRlVGh1bWJuYWlscw=="),   title=vod_channels("RGVsZXRlIFRodW1ibmFpbHM=") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("Y2xlYXJwYWNrYWdl"),   title=vod_channels("UHVyZ2UgUGFja2FnZXM=") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("dXBkYXRlcw=="),   title="Update Current" , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("dXBkYXRlcw=="),   title=vod_channels("Rml4IERlcGVuZGVuY3lzIEVycm9y") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("cmVzZXQ="),   title=vod_channels("UmVzZXQ=") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action=vod_channels("a2lsbHhibWM="),   title=vod_channels("UmVzdGFydCBLb2Rp") , thumbnail="" , fanart=os.path.join(LOAD_LIVE,vod_channels("YmFja2dyb3VuZC5wbmc=")) , folder=False )
def advance(params):
            tseaded = xbmc.translatePath(sync_data("c3BlY2lhbDovL3VzZXJkYXRhL2FkdmFuY2Vkc2V0dGluZ3MueG1s"))
            file = open( os.path.join(plugintools.get_runtime_path(),"resources",sync_data("YWR2YW5jZWRzZXR0aW5ncy54bWw=")) )
            data = file.read()
            file.close()
            file = open(tseaded,"w")
            file.write(data)
            file.close()
            plugintools.message(pnimi, "New advanced streaming settings added.")
def reset(params):
            tseaded = xbmc.translatePath("special://userdata/addon_data/plugin.video.dex/settings.xml")
            file = open( os.path.join(plugintools.get_runtime_path(),"resources",("settings.xml")))
            data = file.read()
            file.close()
            file = open(tseaded,"w")
            file.write(data)
            file.close()
            plugintools.message(pnimi, "New advanced streaming settings added.")

def SPORTS(params): 
    plugintools.add_item( action="runner", title='Match Detail' , url='', thumbnail='', plot='', fanart='' , extra="", isPlayable=False, folder=False )
    plugintools.add_item( action="upandcoming", title='Wheres The Games' , url='', thumbnail='', plot='', fanart='' , extra="", isPlayable=False, folder=True )
def FETCHSHOW(url):
    season = 0
    r = requests.get(url)
    image = re.compile('<img src="(.+?)" width="158" border="0">').findall(r.content)
    match = re.compile('<div class=".+?"> <a href="(.+?)">(.+?)<span class=".+?">(.+?)</span>').findall(r.content)
    match2 = re.compile('<a href="\/go\.php\?gtfo=(.+?)" rel="nofollow" title=".+?" target="_blank">(.+?)</a>.+?</strong>(.+?)<',re.DOTALL).findall(r.content)
    for image in image:
        image = image
    for url,name1,name2 in match:
        name1 = name1.replace(' ','')
        if name1 == 'E1':
            season = season + 1
            addDir('[COLOR yellow]Season %s[/COLOR]'%season,'','','')
            addDir(name1+' '+name2,'http://www.watchfree.to/%s'%url,6,'http:%s'%image)
        else:
            addDir(name1+' '+name2,'http://www.watchfree.to/%s'%url,6,'http:%s'%image)
    for url,name,host in match2:
        url = base64.b64decode(url)
        addDir2(name+host,url,7,'')
def FETCHLINKS(url):
    r = requests.get(url)
    match = re.compile('<a href="\/go\.php\?gtfo=(.+?)" rel="nofollow" title=".+?" target="_blank">(.+?)</a>.+?</strong>(.+?)<',re.DOTALL).findall(r.content)
    for url,name,host in match:
        url = base64.b64decode(url)
        addDir2(name+host,url,7,'')    

def CATEGORIES():
    plugintools.add_item( action="keyboard_input", title='Search' , url='', thumbnail='', plot='', fanart=os.path.join(LOAD_LIVE,"dGhlYXRlci5qcGc=") , extra="", isPlayable=True, folder=False )
    url = ('http://watchfree.to?genres')
    r = requests.get(url)
    match = re.compile('<div class="genre_item"> <a href="(.+?)">(.+?)</a></div>').findall(r.content)
    for url2,name in match:
        plugintools.add_item( action="keyboard_input", title='Search' , url='', thumbnail='', plot='', fanart=os.path.join(LOAD_LIVE,"dGhlYXRlci5qcGc=") , extra="", isPlayable=True, folder=False )
def lists(url):
    r = requests.get(url)
    match = re.compile('<div class="item"><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"').findall(r.content)
    for url,name,image in match:
        addDir(name,'http://watchfree.to'+url,5,'http:'+image)
      
def PLAYING(lopplink):

    play=xbmc.Player(GetPlayerCore())
    play.play(lopplink)
    return
def PLAYING2(params):
        lopplink = params.get("url")
        play=xbmc.Player(GetPlayerCore())
        play.play(lopplink)
def PLAYING3(params):
    try:
        lopplink = params.get("url")
        play=xbmc.Player(GetPlayerCore())
        play.play(lopplink)
    except:
        pass
def GetPlayerCore(): 
    try: 
        PlayerMethod=getSet("core-player") 
        if   (PlayerMethod=='DVDPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_DVDPLAYER 
        elif (PlayerMethod=='MPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_MPLAYER 
        elif (PlayerMethod=='PAPLAYER'): PlayerMeth=xbmc.PLAYER_CORE_PAPLAYER 
        else: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    except: PlayerMeth=xbmc.PLAYER_CORE_AUTO 
    return PlayerMeth 
    return True
def search(name):
            menu = []
            urls = []
            menu2 = []
            dialog = xbmcgui.Dialog()
            url = ('http://www.watchfree.to/?keyword='+name)
            r = requests.get(url)
            match = re.compile('<div class="item"><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"').findall(r.content)
            for url,name,image in match:
                url = 'http://www.watchfree.to%s'%url
                    
                menu.append(name)
                urls.append(url)
            ret = dialog.select('Choose a Action', menu)
            url = urls[ret]
            if ret == None:
                return
            else:
                r = requests.get(url)
                match = re.compile('<div class=".+?"> <a href="(.+?)">(.+?)<span class=".+?">(.+?)</span>').findall(r.content)
                match = re.compile('<a href="\/go\.php\?gtfo=(.+?)" rel="nofollow" title=".+?" target="_blank">(.+?)</a>.+?</strong>(.+?)<',re.DOTALL).findall(r.content)
                for url,name,host in match:
                    url = base64.b64decode(url)
                    menu2.append(url)
                ret = dialog.select('Choose a Action', menu2)
                if ret < 0:
                    return
                else:
                    PLAYVIDEO3(menu2[ret])
def search2(name):
            menu = []
            urls = []
            urls2 = []
            urls3 = []
            menu2 = []
            urls4 = []
            dialog = xbmcgui.Dialog()
            url = ('http://www.watchfree.to/?search_section=2&keyword='+name)
            r = requests.get(url)
            match = re.compile('<div class="item"><a href="(.+?)" title="(.+?)">.+?<img src="(.+?)"').findall(r.content)
            for url,name,image in match:
                url = 'http://www.watchfree.to%s'%url
                menu.append(name)
                urls.append(url)
            ret = dialog.select('Choose a Action', menu)
            url = urls[ret]
            r = requests.get(url)
            match = re.compile('<a href="(.+?)">(.+?) <span class="tv_episode_name"> (.+?)</span>').findall(r.content)
            season=1
            for url,name,host in match:
                url = 'http://www.watchfree.to%s'%url
                if name == 'E1':
                    menu2.append('[COLOR yellow]Season %s[/COLOR]'%season)
                    menu2.append(name+' '+host)
                    season += 1
                    urls3.append(url)
                else:
                    menu2.append(name+' '+host)
                    urls3.append(url)
            ret = dialog.select('Choose a Action', menu2)
            if ret == ret:
                return
            elif ret == None:
                url = urls3[ret]
                r = requests.get(url)
                match = re.compile('<a href="\/go\.php\?gtfo=(.+?)" rel="nofollow" title=".+?" target="_blank">(.+?)</a>.+?</strong> - (.+?)<',re.DOTALL).findall(r.content)
                for url,name,host in match:
                    url = base64.b64decode(url)
                    urls2.append(url)
                    if 'vidzi' in url:
                        host = '[COLOR yellow]Recommended: [/COLOR]'+host+''
                        urls4.append(host)
                    if 'cloudzilla' in url:
                        host = '[COLOR yellow]Recommended: [/COLOR]'+host+''
                        urls4.append(host)
                    else:
                        urls4.append(host)
                    
                ret = dialog.select('Choose a Action', urls4)
                if ret < 0:
                    return
                else:
                    url=urls2[ret]
                    PLAYVIDEO3(url)

def PLAYVIDEO3(url):
    import urlresolver
    from urlresolver import common
    dp = xbmcgui.DialogProgress()
    dp.create('Grabbing Your Video','Opening Ready')
    play=xbmc.Player(GetPlayerCore())
    url=urlresolver.HostedMediaFile(url).resolve()
    play.play(url)           
           
def Radio(params):
    url='http://listenlive.eu/'
    r = requests.get(url)
    match=re.compile('<td><img width="8" height="8" alt="" src="b.gif" /> <a href="(.+?)">(.+?)</a></td></tr>').findall(r.content)
    for url2,name in match:
        plugintools.add_item( action='radio2', title=name , url=url+url2, thumbnail='', plot='', fanart=os.path.join(LOAD_LIVE,"theater.jpg") , extra="", isPlayable=False, folder=True )
def radio2(params):
    lopplink = params.get(vod_channels("dXJs"))
    r= requests.get(lopplink)
    match=re.compile('<b>(.+?)</b>.+?<a href="(.+?)">(.+?) Kbps', re.DOTALL).findall(r.content)
    for name,url2,hs in match:
        plugintools.add_item( action='PLAYING3', title=name+' '+hs , url=url2, thumbnail='', plot='', extra="", folder=False )
        
def sync_data(channel):
    video = base64.b64decode(channel)
    return video
def restart_service(params):
    if vanemalukk == "true":
       pealkiri = params.get(sync_data("dGl0bGU="))
       vanema_lukk(pealkiri)
    lopplink = params.get(vod_channels("dXJs"))
    plugintools.play_resolved_url( lopplink )
def grab_epg():
    req = urllib2.Request(andmelink)
    req.add_header(sync_data("VXNlci1BZ2VudA==") , vod_channels("S29kaSBwbHVnaW4gYnkgTWlra00="))
    response = urllib2.urlopen(req)
    link=response.read()
    jdata = json.loads(link.decode('utf8'))
    response.close()
    if jdata:
       plugintools.log(pnimi+sync_data("amRhdGEgbG9hZGVkIA=="))
       return jdata
def kontroll():
    randomstring = grab_epg()
    kasutajainfo = randomstring[sync_data("dXNlcl9pbmZv")]
    kontroll = kasutajainfo[get_live("YXV0aA==")]
    return kontroll
def get_live(channel):
    video = base64.b64decode(channel)
    return video
def execute_ainfo(params):
    plugintools.log(pnimi+get_live("TXkgYWNjb3VudCBNZW51IA==")+repr(params))
    andmed = grab_epg()
    kasutajaAndmed = andmed[sync_data("dXNlcl9pbmZv")]
    seis = kasutajaAndmed[get_live("c3RhdHVz")]
    aegub = kasutajaAndmed[sync_data("ZXhwX2RhdGU=")]
    if aegub:
       aegub = datetime.datetime.fromtimestamp(int(aegub)).strftime('%H:%M %d.%m.%Y')
    else:
       aegub = vod_channels("TmV2ZXI=") 
    rabbits = kasutajaAndmed[vod_channels("aXNfdHJpYWw=")]
    if rabbits == "0":
       rabbits = sync_data("Tm8=")
    else:
       rabbits = sync_data("WWVz")
    leavemealone = kasutajaAndmed[get_live("bWF4X2Nvbm5lY3Rpb25z")]
    polarbears = kasutajaAndmed[sync_data("dXNlcm5hbWU=")]
    plugintools.add_item( action="",   title=sync_data("W0NPTE9SID0gd2hpdGVdVXNlcjogWy9DT0xPUl0=")+polarbears , thumbnail="" , fanart=os.path.join(LOAD_LIVE,sync_data("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action="",   title=sync_data("W0NPTE9SID0gd2hpdGVdU3RhdHVzOiBbL0NPTE9SXQ==")+seis , thumbnail="" , fanart=os.path.join(LOAD_LIVE,sync_data("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action="",   title=get_live("W0NPTE9SID0gd2hpdGVdRXhwaXJlczogWy9DT0xPUl0=")+aegub , thumbnail="" , fanart=os.path.join(LOAD_LIVE,sync_data("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action="",   title=vod_channels("W0NPTE9SID0gd2hpdGVdVHJpYWwgYWNjb3VudDogWy9DT0xPUl0=")+rabbits , thumbnail="" , fanart=os.path.join(LOAD_LIVE,sync_data("YmFja2dyb3VuZC5wbmc=")) , folder=False )
    plugintools.add_item( action="",   title=vod_channels("W0NPTE9SID0gd2hpdGVdTWF4IGNvbm5lY3Rpb25zOiBbL0NPTE9SXQ==")+leavemealone , thumbnail="" , fanart=os.path.join(LOAD_LIVE,sync_data("aHR0cDovL2xvY2FsaG9zdDo1MjMwNy9nZXRwdnJ0aHVtYiZhbXA7dGl0bGU9JElORk9bTGlzdGl0ZW0uVGl0bGVdJmFtcDtjaGFubmVsPSVzJmFtcDt0eXBlPWZhbmFydA==")) , folder=False )
    plugintools.set_view( plugintools.LIST )
def vanema_lukk(name):
        plugintools.log(pnimi+sync_data("UGFyZW50YWwgbG9jayA="))
        a = 'XXX', 'Adult', 'Adults','ADULT','ADULTS','adult','adults','Porn','PORN','porn','Porn','xxx'
        if any(s in name for s in a):
           xbmc.executebuiltin((u'XBMC.Notification("Parental Lock", "Channels may contain adult content", 2000)'))
           text = plugintools.keyboard_input(default_text="", title=get_live("UGFyZW50YWwgbG9jaw=="))
           if text==plugintools.get_setting(sync_data("dmFuZW1ha29vZA==")):
              return
           else:
              exit()
        else:
           name = ""
def addDir(name,url,iconimage,urlType):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable','true')
        menu=[]
        menu.append(('Refresh', 'Container.Refresh'))        
        menu.append(('[COLOR red]Report Link[/COLOR]','Container.Update(%s?mode=14&name=%s&url=%s)'% (sys.argv[0],name,url)))
        liz.addContextMenuItems(items=menu, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
        return ok
def News(params):
    xbmc.executebuiltin("RunScript(script.dexnews)")
def runtest(params):
    DownloaderClass('http://ovh.net/files/100Mio.dat',addon_userdata+'pip.zip')
#-----------------------------------------------------------------------------------------------------------------
def DownloaderClass(url,dest,dp=None):
    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Status...","Downloading Content",' ', ' ')
    dp.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: _pbhook(nb, bs, fs, dp, start_time))

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled(): 
            dp.close()

#-----------------------------------------------------------------------------------------------------------------
def make_dir(mypath, dirname):
    ''' Creates sub-directories if they are not found. '''
    import xbmcvfs
    
    if not xbmcvfs.exists(mypath): 
        try:
            xbmcvfs.mkdirs(mypath)
        except:
            xbmcvfs.mkdir(mypath)
    
    subpath = os.path.join(mypath, dirname)
    
    if not xbmcvfs.exists(subpath): 
        try:
            xbmcvfs.mkdirs(subpath)
        except:
            xbmcvfs.mkdir(subpath)
            
    return subpath
#-----------------------------------------------------------------------------------------------------------------
def GetEpochStr():
    time_now  = datetime.datetime.now()
    epoch     = time.mktime(time_now.timetuple())+(time_now.microsecond/1000000.)
    epoch_str = str('%f' % epoch)
    epoch_str = epoch_str.replace('.','')
    epoch_str = epoch_str[:-3]
    return epoch_str
#-----------------------------------------------------------------------------------------------------------------
    dialog = xbmcgui.Dialog()
    with open(addonDir+"/DEXTER.ini", "w") as f:
        url = ('http://158.69.54.54:8000/panel_api.php?username=%s&password=%s'%(u,p))
        r = requests.get(url)
        match=re.compile('"name":"(.+?)".+?stream_id":"(.+?)"').findall(r.content)
        f.write('[plugin.video.dex]\n')
        for name,stream in match:
            f.write(name+'=http://158.69.54.54:8000/%s/%s/'%(u,p)+stream+'.m3u8\n')
        f.close()
        dialog.ok('All Done','This Feature Is Not Backed By Dexter And Will Not Offer Support Please Contact The Guide You Are Using For Help Questions On This Will Be Ignored')
    dialog.ok("Restart XBMC", "Please restart XBMC to rebuild thumbnail library")

def updates(params):
		dialog = xbmcgui.Dialog()
		version = ("3")
		url = ('http://158.69.54.54/version.txt')
		r = requests.get(url)
		match=re.compile('(\d)').findall(r.content)
		for d in match:
			if d > version:
				dialog.ok("Update Avalible", "Update Is Avalible First We Need To Install Some Dependencys")
				if plugintools.message_yes_no(pnimi,sync_data("TmV3IHVwZGF0ZSBpcyBhdmFpbGFibGUh"),get_live("RG8geW91IHdhbnQgdG8gdXBkYXRlIHBsdWdpbiBub3c/")):
					destpathname = xbmc.translatePath(os.path.join(sync_data("c3BlY2lhbDovLw=="),sync_data("aG9tZS9hZGRvbnMv")))
					local_file_name = os.path.join( plugintools.get_runtime_path() , get_live("cGx1Z2luLnZpZGVvLmRleC56aXA=") )
					urllib.urlretrieve('http://158.69.54.54/plugin.video.dex.zip',local_file_name )
					DownloaderClass('http://158.69.54.54/plugin.video.dex.zip',local_file_name)
					import ziptools
					unzipper = ziptools.ziptools()
					#destpathname = xbmc.translatePath(os.path.join('special://','home')) 
					unzipper.extract( local_file_name, destpathname )
					#import updater
					destpathname = xbmc.translatePath(os.path.join(sync_data("c3BlY2lhbDovLw=="),sync_data("aG9tZS9hZGRvbnMv")))
					local_file_name = os.path.join( plugintools.get_runtime_path() , get_live("ZGVwZW5kcy56aXA=") )
					urllib.urlretrieve('http://158.69.54.54/depends.zip',local_file_name )
					DownloaderClass('http://158.69.54.54/depends.zip',local_file_name)
					import ziptools
					unzipper = ziptools.ziptools()
					#destpathname = xbmc.translatePath(os.path.join('special://','home')) 
					unzipper.extract( local_file_name, destpathname )
					xbmc.executebuiltin((u'XBMC.Notification("Updated", "The add-on has been updated", 2000)'))
					#import updater
					xbmc.executebuiltin( "Container.Refresh" )


def check_user(params):
        m='s'

def load_channels():

    statinfo = os.stat(LOAD_LIVE+"/"+get_live("YmFja2dyb3VuZC5wbmc="))

       
    statinfo = os.stat(LOAD_LIVE+"/"+get_live("ZGVmYXVsdGxvZ28ucG5n"))
    statinfo = os.stat(LOAD_LIVE+"/"+get_live("aG9tZXRoZWF0ZXIuanBn"))
    statinfo = os.stat(LOAD_LIVE+"/"+get_live("bm9wb3N0ZXIuanBn"))
    statinfo = os.stat(LOAD_LIVE+"/"+get_live("dGhlYXRlci5qcGc="))

       
    statinfo = os.stat(addonDir+"/"+get_live("aW5pdC5weQ=="))
    statinfo = os.stat(addonDir+"/"+get_live("aWNvbi5wbmc="))
    statinfo = os.stat(addonDir+"/"+vod_channels("ZmFuYXJ0LnBuZw=="))
def addLink(name,url,iconimage,urlType):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('IsPlayable','true')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
         
def vod_channels(channel):
    video = base64.b64decode(channel)
    return video
active = xbmcplugin.getSetting(int(sys.argv[1]), 'active')
run()




