import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os
import datetime
import time
from t0mm0.common.net import Net



PLUGIN='plugin.video.nhlstreams'
ADDON = xbmcaddon.Addon(id=PLUGIN)
deletepy = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'),ADDON.getSetting('delete')))

print '####################################'

    
net=Net()



def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


if ADDON.getSetting('firstrun')=='':
	if ADDON.getSetting('user')=='':
	    dialog = xbmcgui.Dialog()
	    dialog.ok("NHL Streams", "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
	    search_entered = ''
	    keyboard = xbmc.Keyboard(search_entered, 'NHL Streams')
	    keyboard.doModal()
	    if keyboard.isConfirmed():
	        search_entered = keyboard.getText() 
	    ADDON.setSetting('user',search_entered)
	    
	if ADDON.getSetting('pass')=='':
	    dialog = xbmcgui.Dialog()
	    dialog.ok("NHL Streams", "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
	    search_entered = ''
	    keyboard = xbmc.Keyboard(search_entered, 'NHL Streams')
	    keyboard.doModal()
	    if keyboard.isConfirmed():
	        search_entered = keyboard.getText() 
	    ADDON.setSetting('pass',search_entered)
	    ADDON.setSetting('firstrun','true')
    
    
    
        
    
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
cookie_path = os.path.join(datapath, 'cookies')
cookie_jar = os.path.join(cookie_path, "kickoff_new.lwp")
site='http://nhlstreams.com/live-nhl-streams/'

    

def LOGIN():
    try:
        os.remove(cookie_jar)
    except:
        pass
    loginurl = 'http://nhlstreams.com/wp-login.php'
    username    =ADDON.getSetting('user')
    password =ADDON.getSetting('pass')
    
    data     = {'pwd': password,
                                            'log': username,
                                            'wp-submit': 'Log In','testcookie':'1'}
    headers  = {'Host':'nhlstreams.com',
                                            'Origin':'http://nhlstreams.com',
                                            'Referer':'http://nhlstreams.com/wp-login.php',
                                                    'X-Requested-With':'XMLHttpRequest'}
    html = net.http_POST(loginurl, data, headers)
    
    if os.path.exists(cookie_path) == False:
            os.makedirs(cookie_path)
    net.save_cookies(cookie_jar)
	
	
if os.path.exists(cookie_jar) == False:
        LOGIN()



def CATEGORIES():
    net.set_cookies(cookie_jar)
    link = net.http_GET('http://nhlstreams.com/chan.js').content
    match = re.findall('"title": "(.+?)".+?"file": "(.+?)",',link,re.M|re.DOTALL)
    for name,url in match:
        addDir(name,url,2,'','False','','')
        
        
        
def PLAYSTREAM(name,url):
    try:
        net.set_cookies(cookie_jar)
        html = net.http_GET(site).content
        var = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
        stream_url='%s swfUrl=http://p.jwpcdn.com/6/6/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10'%(url.replace('" + urlkey1 + "',var[0]),var[0],site)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": description} )
        liz.setProperty("IsPlayable","true")
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(stream_url, liz)
        xbmc.Player().play(pl)
    except:
        LOGIN()
        net.set_cookies(cookie_jar)
        html = net.http_GET(site).content
        var = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
        stream_url='%s swfUrl=http://p.jwpcdn.com/6/6/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10'%(url.replace('" + urlkey1 + "',var[0]),var[0],site)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": description} )
        liz.setProperty("IsPlayable","true")
        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        pl.clear()
        pl.add(stream_url, liz)
        xbmc.Player().play(pl)
        
        
 
    
def OPEN_MAGIC(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent' , "Magic Browser")
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
        
        
        
        
        
    
def fullguide(name,url,iconimage,description):
    description=description.split('[COLOR yellow]')[0]
    url=tvguide.fulltvguide(description)
    link=OPEN_URL(url)
    match=re.findall('<title>(.+?)</title>.+?<start>(.+?)</start>',link,re.M|re.DOTALL)
    for _name,start in match:
        hours=start[0:2]+':'+start[2:4]
        name_='[COLOR white][%s]-[/COLOR][COLOR yellow][B]%s[/B][/COLOR]'%(hours,_name)
        addDir(name_,url,2,iconimage.replace(' ','%20').replace('i/H','i-H'),'True','',description)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE)      
        
        
def Grab_Day(date):
    year, month, day = (int(x) for x in date.split('-'))    
    ans=datetime.date(year,month,day)
    return (ans.strftime("%a"))
        
    
def PLAY_STREAM(name,url,iconimage,play,description):
    if play=='True':
        desc=description.replace('%20',' ').replace('i-H','i/H').replace('  ',' +')
        link = OPEN_URL(server())
        link = link.split('"title": "')
        r='"file": "(.+?)",'
        for p in link:
            if desc in p:
                match = re.findall(r,p,re.M|re.DOTALL)
                rtmp=match[0]
                try:
                        net.set_cookies(cookie_jar)
                        html = net.http_GET(site).content
                        var = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
                        liz=xbmcgui.ListItem(description, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                        stream_url='%s swfUrl=http://p.jwpcdn.com/6/5/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10'%(rtmp.replace('" + urlkey1 + "',var[0]),var[0],site)
                        liz.setInfo( type="Video", infoLabels={ "Title": name} )
                        liz.setProperty("IsPlayable","true")
                        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                        pl.clear()
                        pl.add(stream_url, liz)
                        xbmc.Player().play(pl)
                except:
                        LOGIN()
                        net.set_cookies(cookie_jar)
                        html = net.http_GET(site).content
                        var = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
                        liz=xbmcgui.ListItem(description, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
                        stream_url='%s swfUrl=http://p.jwpcdn.com/6/5/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10'%(rtmp.replace('" + urlkey1 + "',var[0]),var[0],site)
                        liz.setInfo( type="Video", infoLabels={ "Title": name} )
                        liz.setProperty("IsPlayable","true")
                        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
                        pl.clear()
                        pl.add(stream_url, liz)
                        xbmc.Player().play(pl)
    else:
        try:
	        net.set_cookies(cookie_jar)
	        html = net.http_GET(site).content
	        var = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
	        stream_url='%s swfUrl=http://p.jwpcdn.com/6/5/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10'%(url.replace('" + urlkey1 + "',var[0]),var[0],site)
	        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	        liz.setInfo( type="Video", infoLabels={ "Title": description} )
	        liz.setProperty("IsPlayable","true")
	        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	        pl.clear()
	        pl.add(stream_url, liz)
	        xbmc.Player().play(pl)
        except:
	        LOGIN()
	        net.set_cookies(cookie_jar)
	        html = net.http_GET(site).content
	        var = re.findall('urlkey1 = "(.+?)"',html,re.M|re.DOTALL)
	        stream_url='%s swfUrl=http://p.jwpcdn.com/6/5/jwplayer.flash.swf app=liveedge?wmsAuthSign=%s pageUrl=%s timeout=10'%(url.replace('" + urlkey1 + "',var[0]),var[0],site)
	        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	        liz.setInfo( type="Video", infoLabels={ "Title": description} )
	        liz.setProperty("IsPlayable","true")
	        pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
	        pl.clear()
	        pl.add(stream_url, liz)
	        xbmc.Player().play(pl)
	        
        
def EXIT():
        xbmc.executebuiltin("XBMC.Container.Update(path,replace)")
        xbmc.executebuiltin("XBMC.ActivateWindow(Home)")
        
        
    
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

def addDir(name,url,mode,iconimage,play,date,description,page=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&play="+urllib.quote_plus(play)+"&date="+urllib.quote_plus(date)+"&description="+urllib.quote_plus(description)+"&page="+str(page)
        
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Premiered":date,"Plot":description} )
        menu=[]
        menu.append(('[COLOR yellow]Schedule[/COLOR]','XBMC.Container.Update(%s?mode=200&url=None&description=%s&name=%s&play=False&iconimage=%s)'% (sys.argv[0],description,name,iconimage)))
        liz.addContextMenuItems(items=menu, replaceItems=False)
        if mode == 2000 or mode==2:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
date=None
description=None
page=None

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
try:
        play=urllib.unquote_plus(params["play"])
except:
        pass
try:
        date=urllib.unquote_plus(params["date"])
except:
        pass
try:
        description=urllib.unquote_plus(params["description"])
except:
        pass
try:        
        page=int(params["page"])
except:
        pass
   
        
#these are the modes which tells the plugin where to go
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
               
elif mode==2:
        PLAYSTREAM(name,url)
        
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))

