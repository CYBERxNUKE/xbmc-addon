import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
from t0mm0.common.net import Net
ADDON = xbmcaddon.Addon(id='plugin.video.gta')
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
net=Net()
loginurl = 'http://gtastreams.com/wp-login.php'
username = ADDON.getSetting("user")
password = ADDON.getSetting("pass")

data     = {'pwd': password,
                                        'log': username,
                                        'wp-submit': 'Log In'}
headers  = {'Host':'gtastreams.com',
                                        'Origin':'http://gtastreams.com',
                                        'Referer':'http://gtastreams.com/wp-login.php',
                                                'X-Requested-With':'XMLHttpRequest'}
html = net.http_POST(loginurl, data, headers)
cookie_jar = os.path.join(cookie_path, "gtastreams.lwp")
if os.path.exists(cookie_path) == False:
        os.makedirs(cookie_path)
net.save_cookies(cookie_jar)

image='http://offsidestreams.com/site/wp-content/uploads/2013/06/'
site='http://gtastreams.com/?page_id=8'




def CATEGORIES():
    try:
	    net.set_cookies(cookie_jar)
	    html = net.http_GET(site).content
	    getkey = re.findall('urlkey = "(.+?)"</script>',html,re.M|re.DOTALL)
	    key = getkey[0]
	    js=re.compile('src="(.+?)/vai/(.+?)"></script').findall(html)
	    link = OPEN_URL(js[0][0]+'/vai/'+js[0][1])
	    link = link.split('window.channels =')[1]
	    match = re.findall('"title": "(.+?)".+?"file": "(.+?)",',link,re.M|re.DOTALL)
	    for name,url in match:
	        addDir(name,url,2,image+name.replace(' ','%20')+'.png')
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok("[COLOR yellow]LiveStreaming4U [/COLOR]","[COLOR red]Login ERROR! [/COLOR]", "Do You Have An Account Set Up ?")
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
	        

def PLAY_STREAM(name,url,iconimage):
    net.set_cookies(cookie_jar)
    html = net.http_GET(site).content
    key = re.findall('urlkey = "(.+?)"',html,re.M|re.DOTALL)
    dp = xbmcgui.DialogProgress()
    dp.create("LiveStreaming4U","",'Please Wait While We Grab The Stream')
    url='%s swfUrl=http://p.jwpcdn.com/6/4/jwplayer.flash.swf timeout=15 swfVfy=true live=true pageUrl=%s'%(url.replace('" + urlkey + "',key[0]),site)
    liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name} )
    liz.setProperty("IsPlayable","true")
    pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    pl.clear()
    pl.add(url, liz)
    xbmc.Player().play(pl)
    dp.close()
        
        
 
def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link
    
                
    
    
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

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
 
        
#below tells plugin about the views                
def setView(content, viewType):
        # set content type so library shows more views and info
        if content:
                xbmcplugin.setContent(int(sys.argv[1]), content)
        if ADDON.getSetting('auto-view') == 'true':#<<<----see here if auto-view is enabled(true) 
                xbmc.executebuiltin("Container.SetViewMode(%s)" % ADDON.getSetting(viewType) )#<<<-----then get the view type
                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
               
elif mode==2:
        print ""+url
        PLAY_STREAM(name,url,iconimage)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))


