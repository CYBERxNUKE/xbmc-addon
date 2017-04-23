import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc, xbmcaddon, os, sys
import downloader
import extract
import time
import shutil
from resources.modules import main
addon_id = 'plugin.video.nukewizard'
try: 		from t0mm0.common.addon import Addon
except: from t0mm0_common_addon import Addon
addon = main.addon
try: 		from t0mm0.common.net import Net
except: from t0mm0_common_net import Net
net = Net()
settings = xbmcaddon.Addon(id='plugin.video.nukewizard')

#==========================Help WIZARD=====================================================================================================
def HELPCATEGORIES():
    link=OPEN_URL('https://github.com/CYBERxNUKE/cputech/raw/master/help.txt').replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,filetype in match:
        #if 'status' in filetype:
            #main.addHELPDir(name,url,'wizardstatus',iconimage,fanart,description,filetype)
        #else:    
            main.addHELPDir(name,url,'helpwizard',iconimage,fanart,description,filetype)
            main.AUTO_VIEW('movies')

def OPEN_URL(url): req=urllib2.Request(url); req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'); response=urllib2.urlopen(req); link=response.read(); response.close(); return link

def HELPWIZARD(name,url,description,filetype):
    path=xbmc.translatePath(os.path.join('special://home/addons','packages'))
    confirm=xbmcgui.Dialog()
    if confirm.yesno("NUKECORP","Would you like me to ","customize your add-on selection? "," "):
        dp=xbmcgui.DialogProgress(); dp.create("NUKE WIZARD","Downloading ",'','Please Wait')
        lib=os.path.join(path,name+'.zip')
        try: os.remove(lib)
        except: pass
        downloader.download(url,lib,dp)
    #if filetype == 'addon':
        #addonfolder = xbmc.translatePath(os.path.join('special://','home/addons'))
    #elif filetype == 'media':
        #addonfolder = xbmc.translatePath(os.path.join('special://','home'))    
#attempt Shortcuts
    #elif filetype == 'main':
        addonfolder=xbmc.translatePath(os.path.join('special://','home'))
        time.sleep(2)
        dp.update(0,"","Extracting Zip Please Wait")
        print '======================================='; print addonfolder; print '======================================='
        extract.all(lib,addonfolder,dp)
        link=OPEN_URL('https://github.com/CYBERxNUKE/cputech/raw/master/homeshort.txt')
        proname=xbmc.getInfoLabel("System.ProfileName")
        shorts=re.compile('shortcut="(.+?)"').findall(link)
        for shortname in shorts: xbmc.executebuiltin("Skin.SetString(%s)" % shortname)
        time.sleep(2)
        xbmc.executebuiltin('UnloadSkin()'); xbmc.executebuiltin('ReloadSkin()'); xbmc.executebuiltin("LoadProfile(%s)" % proname)
        dialog=xbmcgui.Dialog(); dialog.ok("Success!","Please Reboot To Take","Effect   [COLOR gold]Brought To You By CYBERxNUKE[/COLOR]")

def WIZARDSTATUS(url):
    link=OPEN_URL(url).replace('\n','').replace('\r','')
    match=re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)".+?ype="(.+?)"').findall(link)
    for name,url,iconimage,fanart,description,filetype in match: header="[B][COLOR gold]"+name+"[/B][/COLOR]"; msg=(description); TextBoxes(header,msg)

def TextBoxes(heading,anounce):
        class TextBox():
            WINDOW=10147
            CONTROL_LABEL=1
            CONTROL_TEXTBOX=5
            def __init__(self,*args,**kwargs):
                xbmc.executebuiltin("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
                self.win=xbmcgui.Window(self.WINDOW) # get window
                xbmc.sleep(500) # give window time to initialize
                self.setControls()
            def setControls(self):
                self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
                try: f=open(anounce); text=f.read()
                except: text=anounce
                self.win.getControl( self.CONTROL_TEXTBOX ).setText (str(text))
                return
        TextBox()

#==========END HELP WIZARD==================================================================================================
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]; cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'): params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&'); param={}
                for i in range(len(pairsofparams)):
                        splitparams={}; splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2: param[splitparams[0]]=splitparams[1]
        return param

params=get_params(); url=None; name=None; mode=None; year=None; imdb_id=None

try:    fanart=urllib.unquote_plus(params["fanart"])
except: pass
try:    description=urllib.unquote_plus(params["description"])
except: pass
try:    filetype=urllib.unquote_plus(params["filetype"])
except: pass
try:		url=urllib.unquote_plus(params["url"])
except: pass
try:		name=urllib.unquote_plus(params["name"])
except: pass
try:		mode=urllib.unquote_plus(params["mode"])
except: pass
try:		year=urllib.unquote_plus(params["year"])
except: pass
print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name); print "Year: "+str(year)

if mode==None or url==None or len(url)<1: HELPCATEGORIES()
elif mode == "wizardstatus": print""+url; items = WIZARDSTATUS(url)
elif mode=='helpwizard': HELPWIZARD(name,url,description,filetype)
xbmcplugin.endOfDirectory(int(sys.argv[1]))        
