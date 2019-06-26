 #############Imports#############
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,xbmcvfs,base64,os,re,unicodedata,requests,time,string,sys,urllib,urllib2,json,urlparse,datetime,zipfile,shutil
from resources.modules import client,control,tools,user
from datetime import date
import xml.etree.ElementTree as ElementTree


#################################

#############Defined Strings#############
icon         = xbmc.translatePath(os.path.join('special://home/addons/' + user.id, 'icon.png'))
fanart       = xbmc.translatePath(os.path.join('special://home/addons/' + user.id , 'fanart.jpg'))

icon_set     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'icon_settings.png'))
icon_extr    = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'icon_extras.png'))
icon_help    = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'icon_help.png'))
icon_pvr     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'icon_pvr.png'))
icon_vod     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'icon_vod.png'))
icon_tool    = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'icon_tools.png'))

fan_set      = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'settings.jpg'))
fan_extr     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'addons.jpg'))
fan_help     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'help.jpg'))
fan_pvr      = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'pvr.jpg'))
fan_vod      = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'vod.jpg'))
fan_acct     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'account.jpg'))
fan_epg      = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'epg.jpg'))
fan_tv       = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'livetv.jpg'))
fan_srch     = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'search.jpg'))

help_set1    = xbmc.translatePath(os.path.join('special://home/addons/' + user.id + '/resources/images', 'set1.jpg'))

username     = control.setting('Username')
password     = control.setting('Password')
host         = control.setting('Server')


live_url     = '%s:%s/enigma2.php?username=%s&password=%s&type=get_live_categories'%(host,user.port,username,password)
vod_url      = '%s:%s/enigma2.php?username=%s&password=%s&type=get_vod_categories'%(host,user.port,username,password)
panel_api    = '%s:%s/panel_api.php?username=%s&password=%s'%(host,user.port,username,password)
player_api   = '%s:%s/player_api.php?username=%s&password=%s&action=get_live_streams'%(host,user.port,username,password)
play_url     = '%s:%s/live/%s/%s/'%(host,user.port,username,password)


basePath     = ('special://userdata/addon_data/'+user.id+'/')
basePath     = xbmc.translatePath(basePath)

strmPath = ('special://profile/addon_data/'+user.id+'/vodstrms/')
if not xbmcvfs.exists(strmPath):
    xbmcvfs.mkdir(strmPath)
strmPath = xbmc.translatePath(strmPath)

Guide = xbmc.translatePath(os.path.join('special://home/addons/addons/'+user.id+'/resources/catchup', 'guide.xml'))
GuideLoc = xbmc.translatePath(os.path.join('special://home/addons/addons/'+user.id+'/resources/catchup', 'g'))

advanced_settings           =  xbmc.translatePath('special://home/addons/'+user.id+'/resources/advanced_settings')
advanced_settings_target    =  xbmc.translatePath(os.path.join('special://home/userdata','advancedsettings.xml'))

KODIV        = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
#########################################

def buildcleanurl(url):
    url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
    return url
def start():
    addSrc()
    if username=="":
        usern = userpopup()
        passw = passpopup()
        portp = portpopup()
        control.setSetting('Username',usern)
        control.setSetting('Password',passw)
        control.setSetting('Server',portp)
        xbmc.executebuiltin('Container.Refresh')
        home()
    else:
        home()

def home():
    tools.addDir('Account Information','url',6,icon,fan_acct,'')
    tools.addDir('Live TV','live',1,icon,fan_tv,'')
    if xbmc.getCondVisibility('System.HasAddon(pvr.iptvsimple)'):
        tools.addDir('TV Guide','pvr',7,icon,fan_pvr,'')
    tools.addDir('VOD','vod',3,icon_vod,fan_vod,'')
    tools.addDir('Search','',5,icon,fan_srch,'')
    tools.addDir('IPTVXtra2 Settings','url',8,icon_set,fan_set,'')
    tools.addDir('PVR Setup & System Tools','url',16,icon_pvr,fan_pvr,'')
#    tools.addDir('Help','helptest',10,icon_help,fan_help,'')

def livecategory(url):
    
    open = tools.OPEN_URL(live_url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a,'<title>','</title>')
        name = base64.b64decode(name)
        cat = tools.regex_from_to(a,'<category_id>','</category_id>')
        url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
        if (xbmcaddon.Addon().getSetting('hidexxx')=='true') and (cat == '13') or (cat == '25'):
            continue
        else:
            tools.addDir('%s'%name,url1,2,icon,fan_tv,'')
        
def Livelist(url):
    url  = buildcleanurl(url)
    open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        name = tools.regex_from_to(a,'<title>','</title>')
        name = base64.b64decode(name)
        xbmc.log(str(name))
        name = re.sub('\[.*?min ','-',name)
        thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
        cat = tools.regex_from_to(a,'<category_id>','</category_id>')
        url1  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
        desc = tools.regex_from_to(a,'<description>','</description>')
        if (xbmcaddon.Addon().getSetting('hidexxx')=='true') and (cat == '13') or (cat == '25'):
            continue
        else:
            tools.addDir(name,url1,4,thumb,fanart,base64.b64decode(desc))


def vod(url):

    if url =="vod":
        open = tools.OPEN_URL(vod_url)
    else:
        url  = buildcleanurl(url)
        open = tools.OPEN_URL(url)
    all_cats = tools.regex_get_all(open,'<channel>','</channel>')
    for a in all_cats:
        if '<playlist_url>' in open:
            name = tools.regex_from_to(a,'<title>','</title>')
            cat = tools.regex_from_to(a,'<category_id>','</category_id>')
            url1  = tools.regex_from_to(a,'<playlist_url>','</playlist_url>').replace('<![CDATA[','').replace(']]>','')
            if (xbmcaddon.Addon().getSetting('hidexxx')=='true') and (cat == '25'):
                continue
            tools.addDir(str(base64.b64decode(name)).replace('?',''),url1,3,icon,fan_vod,'')
        else:
            if xbmcaddon.Addon().getSetting('meta') == 'true':
                try:
                    name = tools.regex_from_to(a,'<title>','</title>')
                    name = base64.b64decode(name)
                    thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                    url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                    vodID = tools.regex_from_to(url,('movie/'+username+'/'+password+'/'),'.mp4')
                    desc = tools.regex_from_to(a,'<description>','</description>')
                    desc = base64.b64decode(desc)
                    cat = tools.regex_from_to(a,'<category_id>','</category_id>')
                    plot = tools.regex_from_to(desc,'PLOT: ','\n')
                    runt = tools.regex_from_to(desc,'DURATION: ','\n')
                    genre= tools.regex_from_to(desc,'GENRE: ','\n')
                    year = tools.regex_from_to(desc,'RELEASEDATE: ','\n')
                    year = re.findall("\d+", year)[0]
                    ratin= tools.regex_from_to(desc,'RATING: ','\n')
                    cast = tools.regex_from_to(desc,'CAST: ','\n')
                    dir  = tools.regex_from_to(desc,'DIRECTOR: ','\n')
                    tools.addDirMeta(str(name).replace('[/COLOR][/B].','.[/COLOR][/B]'),url,4,thumb,fanart,plot,int(year),cast.split(", "),ratin,runt,genre,dir)
                    if (xbmcaddon.Addon().getSetting('vodStrm')=='true'):
                        makeStrm(name,url)
                except:pass
                xbmcplugin.setContent(int(sys.argv[1]), 'movies')
            else:
                name = tools.regex_from_to(a,'<title>','</title>')
                name = base64.b64decode(name)
                thumb= tools.regex_from_to(a,'<desc_image>','</desc_image>').replace('<![CDATA[','').replace(']]>','')
                url  = tools.regex_from_to(a,'<stream_url>','</stream_url>').replace('<![CDATA[','').replace(']]>','')
                desc = tools.regex_from_to(a,'<description>','</description>')
                tools.addDir(name,url,4,thumb,fanart,base64.b64decode(desc))

def makeStrm(name,content):

    fileObj = open((strmPath + name.replace(':','-').replace('/','-').replace("'","").replace('&','and') +'.strm'),'w')
    # write file content
    fileObj.write(content)
    # close the file
    fileObj.close()

def saveFile(content):

    fileObject = open((basePath+'iptvxtra2.m3u'),'w')
    # write file content
    fileObject.write(content)
    # close the file
    fileObject.close()
    xbmc.executebuiltin("Notification(IPTVXtra II,[I][COLOR lime]   . . .*Custom PVR Playlist Created.[/COLOR][/I])")

def addSrc():
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')
    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if not'IPTVXtra II VOD' in str:
        if '</video>' in str:
            str = str.replace('</video>','    <source>\n            <name>IPTVXtra II VOD</name>\n            <path pathversion="1">special://profile/addon_data/plugin.video.iptvxtra2/vodstrms/</path>\n            <thumbnail pathversion="1">special://home/addons/plugin.video.iptvxtra2/icon.png</thumbnail>\n            <allowsharing>true</allowsharing>\n        </source>\n    </video>')
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','    <video>\n        <default pathversion="1"></default>\n        <source>\n            <name>IPTVXtra II VOD</name>\n            <path pathversion="1">special://profile/addon_data/plugin.video.iptvxtra2/vodstrms/</path>\n            <thumbnail pathversion="1">special://home/addons/plugin.video.iptvxtra2/icon.png</thumbnail>\n            <allowsharing>true</allowsharing>\n        </source>\n    </video>\n</sources>')
            f = open(path, mode='w')
            f.write(str)
            f.close() 

def m3uproc():
    xbmc.executebuiltin('Notification(IPTVXtra II,[I][COLOR yellow] . . . .Processing Channel Data  . . . . . . . . . . . . . . . . . . . . . . . . . . [/COLOR][/I],7000)')
    m3u = '#EXTM3U\n#EXTINF:-1 tvg-id="00411" tvg-chno="1" tvg-name="Information" tvg-logo="https://raw.githubusercontent.com/kens13/EPG/master/info.png" group-title="Information",Information \nhttps://raw.githubusercontent.com/kens13/EPG/master/test_pattern_1.mp4\n' 
    try: conv = json.loads(requests.get(user.ch_list).text)
    except: conv = {}

    open = tools.OPEN_URL(player_api)
    all_chans = tools.regex_get_all(open,'{"num":',':0},')
    for a in all_chans:
        name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
        url = tools.regex_from_to(a,'stream_id":','\,"')
        thumb = tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
        cat = tools.regex_from_to(a,'category_id":"','"')
        xml_id = tools.regex_from_to(a,'epg_channel_id":"','"')
        ds = tools.regex_from_to(a,'direct_source":"','"').replace('\/','/')
        if (xbmcaddon.Addon().getSetting('hidexxx')=='true') and (cat == '13') or (cat == '25'):
            continue

        cat = cat.replace('4', 'Sports')
        cat = cat.replace('5', 'Cinema')
        cat = cat.replace('6', 'Kids')
        cat = cat.replace('7', 'Internationals')
        cat = cat.replace('8', 'Information')
        cat = cat.replace('10', 'Entertainments')
        cat = cat.replace('11', 'Science')
        cat = cat.replace('12', 'Music')
        cat = cat.replace('13', 'For Adults')
        cat = cat.replace('14', 'Culture')
        cat = cat.replace('15', 'Business')

        try: chno_grp = conv[name]
        except: chno_grp = 'group-title="'+cat

        if (':' in ds.lower()):
            line = '#EXTINF:-1 tvg-id="'+xml_id+'" tvg-name="'+name+'" tvg-logo="'+thumb+'" '+chno_grp+'", '+name+'\n'+ds+'\n'
        else:
            line = '#EXTINF:-1 tvg-id="'+xml_id+'" tvg-name="'+name+'" tvg-logo="'+thumb+'" '+chno_grp+'", '+name+'\n'+play_url+url+'.ts\n'
        m3u += line

    saveFile(m3u)
    tvguidesetup()


def catchup():
    listcatchup()
        
def listcatchup():
    open = tools.OPEN_URL(panel_api)
    all  = tools.regex_get_all(open,'{"num','direct')
    for a in all:
        if '"tv_archive":1' in a:
            name = tools.regex_from_to(a,'"epg_channel_id":"','"').replace('\/','/')
            thumb= tools.regex_from_to(a,'"stream_icon":"','"').replace('\/','/')
            id   = tools.regex_from_to(a,'stream_id":"','"')
            if not name=="":
                tools.addDir(name,'url',13,thumb,fanart,id)
            

def tvarchive(name,description):
    days = 5
    
    now = str(datetime.datetime.now()).replace('-','').replace(':','').replace(' ','')
    date3 = datetime.datetime.now() - datetime.timedelta(days)
    date = str(date3)
    date = str(date).replace('-','').replace(':','').replace(' ','')
    APIv2 = base64.b64decode("JXM6JXMvcGxheWVyX2FwaS5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmYWN0aW9uPWdldF9zaW1wbGVfZGF0YV90YWJsZSZzdHJlYW1faWQ9JXM=")%(host,user.port,username,password,description)
    link=tools.OPEN_URL(APIv2)
    match = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(link)
    for ShowTitle,start,end,DesC in match:
        ShowTitle = base64.b64decode(ShowTitle)
        DesC = base64.b64decode(DesC)
        format = '%Y-%m-%d %H:%M:%S'
        try:
            modend = dtdeep.strptime(end, format)
            modstart = dtdeep.strptime(start, format)
        except:
            modend = datetime.datetime(*(time.strptime(end, format)[0:6]))
            modstart = datetime.datetime(*(time.strptime(start, format)[0:6]))
        StreamDuration = modend - modstart
        modend_ts = time.mktime(modend.timetuple())
        modstart_ts = time.mktime(modstart.timetuple())
        FinalDuration = int(modend_ts-modstart_ts) / 60
        strstart = start
        Realstart = str(strstart).replace('-','').replace(':','').replace(' ','')
        start2 = start[:-3]
        editstart = start2
        start2 = str(start2).replace(' ',' - ')
        start = str(editstart).replace(' ',':')
        Editstart = start[:13] + '-' + start[13:]
        Finalstart = Editstart.replace('-:','-')
        if Realstart > date:
            if Realstart < now:
                catchupURL = base64.b64decode("JXM6JXMvc3RyZWFtaW5nL3RpbWVzaGlmdC5waHA/dXNlcm5hbWU9JXMmcGFzc3dvcmQ9JXMmc3RyZWFtPSVzJnN0YXJ0PQ==")%(host,user.port,username,password,description)
                ResultURL = catchupURL + str(Finalstart) + "&duration=%s"%(FinalDuration)
                kanalinimi = "[B][COLOR purple]%s[/COLOR][/B] - %s"%(start2,ShowTitle)
                tools.addDir(kanalinimi,ResultURL,4,icon,fanart,DesC)

    
                    
def DownloaderClass(url, dest):
    dp = xbmcgui.DialogProgress()
    dp.create('Fetching latest Catch Up',"Fetching latest Catch Up...",' ', ' ')
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
            mbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '[B][COLOR purple]%.02f MB of less than 5MB[/COLOR][/B]' % (currently_downloaded)
            e = '[B][COLOR purple]Speed:  %.02f Mb/s ' % mbps_speed  + '[/COLOR][/B]'
            dp.update(percent, mbs, e)
        except: 
            percent = 100 
            dp.update(percent) 
        if dp.iscanceled():
            dialog = xbmcgui.Dialog()
            dialog.ok(user.name, 'The download was cancelled.')
                
            sys.exit()
            dp.close()
#####################################################################

def tvguide():
    xbmc.executebuiltin('ActivateWindow(TVGuide)')
def stream_video(url):
    url = buildcleanurl(url)
    url = str(url).replace('USERNAME',username).replace('PASSWORD',password)
    liz = xbmcgui.ListItem('', iconImage='DefaultVideo.png', thumbnailImage=icon)
    liz.setInfo(type='Video', infoLabels={'Title': '', 'Plot': ''})
    liz.setProperty('IsPlayable','true')
    liz.setPath(str(url))
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz)
    
    
def searchdialog():
    search = control.inputDialog(heading='Search '+user.name+':')
    if search=="":
        return
    else:
        return search

    
def search():
    if mode==3:
        return False
    text = searchdialog()
    if not text:
        xbmc.executebuiltin("XBMC.Notification([B][COLOR purple][B]Search is Empty[/B][/COLOR][/B],Aborting search,4000,"+icon+")")
        return
    xbmc.log(str(text))
    open = tools.OPEN_URL(panel_api)
    all_chans = tools.regex_get_all(open,'{"num":','epg')
    for a in all_chans:
        name = tools.regex_from_to(a,'name":"','"').replace('\/','/')
        url  = tools.regex_from_to(a,'"stream_id":"','"')
        thumb= tools.regex_from_to(a,'stream_icon":"','"').replace('\/','/')
        if text in name.lower():
            tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')
        elif text not in name.lower() and text in name:
            tools.addDir(name,play_url+url+'.ts',4,thumb,fanart,'')

    
def settingsmenu():
    if xbmcaddon.Addon().getSetting('meta')=='true':
        META = '[B][COLOR lime]ON[/COLOR][/B]'
    else:
        META = '[B][COLOR red]OFF[/COLOR][/B]'
    if xbmcaddon.Addon().getSetting('hidexxx')=='true':
        XXX = '[B][COLOR lime]ON[/COLOR][/B]'
    else:
        XXX = '[B][COLOR red]OFF[/COLOR][/B]'
    if xbmcaddon.Addon().getSetting('epgx')=='true':
        EPG = '[B][COLOR lime]Alternate Enabled[/COLOR][/B] / Provider EPG'
    else:
        EPG = 'Alternate Disabled/ [B][COLOR lime]Provider EPG[/COLOR][/B]'
    tools.addDir('Edit Advanced Settings','ADS',10,icon,fanart,'')
    tools.addDir('META for VOD is %s'%META,'META',10,icon,fanart,META)
    tools.addDir('Hide XXX Channels is %s'%XXX,'XXX',10,icon,fanart,XXX)
    tools.addDir('EPG Source-> %s'%EPG,'EPG',10,icon,fanart,EPG)
    tools.addDir('Logout/Reset User ID','LO',10,icon,fanart,'')
    

def addonsettings(url,description):
    url  = buildcleanurl(url)
    if   url =="CC":
        tools.clear_cache()
    elif url =="AS":
        xbmc.executebuiltin('Addon.OpenSettings(%s)'%user.id)
    elif url =="ADS":
        dialog = xbmcgui.Dialog().select('Edit Advanced Settings', ['Enable Fire TV Stick AS','Enable Fire TV AS','Enable 1GB Ram or Lower AS','Enable 2GB Ram or Higher AS','Enable Nvidia Shield AS','Disable AS'])
        if dialog==0:
            advancedsettings('stick')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==1:
            advancedsettings('firetv')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==2:
            advancedsettings('lessthan')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==3:
            advancedsettings('morethan')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==4:
            advancedsettings('shield')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==5:
            advancedsettings('remove')
            xbmcgui.Dialog().ok(user.name, 'Advanced Settings Removed')
    elif url =="ADS2":
        dialog = xbmcgui.Dialog().select('Select Your Device Or Closest To', ['Fire TV Stick ','Fire TV','1GB Ram or Lower','2GB Ram or Higher','Nvidia Shield'])
        if dialog==0:
            advancedsettings('stick')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==1:
            advancedsettings('firetv')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==2:
            advancedsettings('lessthan')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==3:
            advancedsettings('morethan')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
        elif dialog==4:
            advancedsettings('shield')
            xbmcgui.Dialog().ok(user.name, 'Set Advanced Settings')
    elif url =="tv":
        dialog = xbmcgui.Dialog().yesno(user.name,'Would You like us to Setup the TV Guide for You?')
        if dialog:
            pvrsetup()
            xbmcgui.Dialog().ok(user.name, 'PVR Integration Complete, Restart Kodi For Changes To Take Effect')
    elif url =="ST":
        xbmc.executebuiltin('Runscript("special://home/addons/'+user.id+'/resources/modules/speedtest.py")')
    elif url =="helptest":
        xbmc.executebuiltin('ShowPicture('+help_set1+')')

    elif url =="META":
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('meta','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('meta','true')
            xbmc.executebuiltin('Container.Refresh')
    elif url =="EPG":
        if 'Enabled' in description:
            xbmcaddon.Addon().setSetting('epgx','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('epgx','true')
            xbmc.executebuiltin('Container.Refresh')
    elif url =="XXX":
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('hidexxx','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('hidexxx','true')
            xbmc.executebuiltin('Container.Refresh')
    elif url =="LO":
        xbmcaddon.Addon().setSetting('Username','')
        xbmcaddon.Addon().setSetting('Password','')
        xbmcaddon.Addon().setSetting('Server','')
        xbmc.executebuiltin('XBMC.ActivateWindow(Videos,addons://sources/video/)')
        xbmc.executebuiltin('Container.Refresh')
    elif url =="UPDATE":
        if 'ON' in description:
            xbmcaddon.Addon().setSetting('update','false')
            xbmc.executebuiltin('Container.Refresh')
        else:
            xbmcaddon.Addon().setSetting('update','true')
            xbmc.executebuiltin('Container.Refresh')
    
        
def advancedsettings(device):
    if device == 'stick':
        file = open(os.path.join(advanced_settings, 'stick.xml'))
    elif device == 'firetv':
        file = open(os.path.join(advanced_settings, 'firetv.xml'))
    elif device == 'lessthan':
        file = open(os.path.join(advanced_settings, 'lessthan1GB.xml'))
    elif device == 'morethan':
        file = open(os.path.join(advanced_settings, 'morethan1GB.xml'))
    elif device == 'shield':
        file = open(os.path.join(advanced_settings, 'shield.xml'))
    elif device == 'remove':
        os.remove(advanced_settings_target)
    
    try:
        read = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(read)
        f.close()
    except:
        pass
        
    
def pvrsetup():
    correctPVR()
    return
        
        
def asettings():
    choice = xbmcgui.Dialog().yesno(user.name, 'Please Select The RAM Size of Your Device', yeslabel='Less than 1GB RAM', nolabel='More than 1GB RAM')
    if choice:
        lessthan()
    else:
        morethan()
    

def morethan():
        file = open(os.path.join(advanced_settings, 'morethan.xml'))
        a = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(a)
        f.close()

        
def lessthan():
        file = open(os.path.join(advanced_settings, 'lessthan.xml'))
        a = file.read()
        f = open(advanced_settings_target, mode='w+')
        f.write(a)
        f.close()
        
        
def userpopup():
    kb =xbmc.Keyboard ('', 'heading', True)
    kb.setHeading('Enter Username')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        text = kb.getText()
        return text
    else:
        return False

        
def passpopup():
    kb =xbmc.Keyboard ('', 'heading', True)
    kb.setHeading('Enter Password')
    kb.setHiddenInput(False)
    kb.doModal()
    if (kb.isConfirmed()):
        text = kb.getText()
        return text
    else:
        return False

def portpopup():
    dialog = xbmcgui.Dialog()
    entries = ["http://p1.iptvrocket.tv", "http://p2.iptvrocket.tv", "http://s1.iptv66.tv", "http://s2.iptv66.tv", "http://p1.iptvprivateserver.tv", "http://p2.iptvprivateserver.tv", "http://p3.iptvprivateserver.tv", "http://p4.iptvprivateserver.tv", "http://p5.iptvprivateserver.tv"]
    nr = dialog.select("Select your Server/ Portal", entries)
    if nr>=0:
        text = entries[nr]
        return text
    else:
        return False

def accountinfo():
    try:
        open = tools.OPEN_URL(panel_api)
        useracct = tools.regex_from_to(open,'"username":"','"')
        passacct = tools.regex_from_to(open,'"password":"','"')
        status = tools.regex_from_to(open,'"status":"','"')
        connects = tools.regex_from_to(open,'"max_connections":"','"')
        active = tools.regex_from_to(open,'"active_cons":"','"')
        serverurl = tools.regex_from_to(open,'"url":"','"')
        expiry = tools.regex_from_to(open,'"exp_date":"','"')
        if not expiry=="":
            expiry = datetime.datetime.fromtimestamp(int(expiry)).strftime('%d/%m/%Y - %H:%M')
            expreg = re.compile('^(.*?)/(.*?)/(.*?)$',re.DOTALL).findall(expiry)
            for day,month,year in expreg:
                month = tools.MonthNumToName(month)
                year = re.sub(' -.*?$','',year)
                expiry = month+' '+day+' - '+year
        else:
            expiry = 'Unlimited'
        ip = tools.getlocalip()
        extip = tools.getexternalip()
        tools.addDir('[B][COLOR purple]Username :[/COLOR][/B] '+useracct,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Password :[/COLOR][/B] '+passacct,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Server URL :[/COLOR][/B] '+serverurl,'','',icon,fanart,'')
        tools.addDir('[B][COLOR yellow]Expiry Date:[/COLOR][/B] '+expiry,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Account Status :[/COLOR][/B] %s'%status,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Current Connections:[/COLOR][/B] '+ active,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Allowed Connections:[/COLOR][/B] '+connects,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Local IP Address:[/COLOR][/B] '+ip,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]External IP Address:[/COLOR][/B] '+extip,'','',icon,fanart,'')
        tools.addDir('[B][COLOR purple]Kodi Version:[/COLOR][/B] '+str(KODIV),'','',icon,fanart,'')
    except:
        pass
 
def correctPVR():

    addon = xbmcaddon.Addon(user.id)
    username_text = addon.getSetting(id='Username')
    password_text = addon.getSetting(id='Password')
    xEPGurl       = addon.getSetting(id='xepgurl')
    jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'
    IPTVon = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
    IPTVoff = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}'
    loginurl = host+':'+user.port+"/get.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"
    PEPGurl  = host+':'+user.port+"/xmltv.php?username=" + username_text + "&password=" + password_text + "&type=m3u_plus&output=ts"

    xbmc.executeJSONRPC(jsonSetPVR)
    xbmc.executeJSONRPC(IPTVon)

    moist = xbmcaddon.Addon('pvr.iptvsimple')
    moist.setSetting(id='m3uPathType', value="0")
    moist.setSetting(id='m3uPath', value=(basePath+'iptvxtra2.m3u'))
#    moist.setSetting(id='m3uUrl', value=loginurl)
    if xbmcaddon.Addon(user.id).getSetting('epgx')=='true':
        EPGurl = xEPGurl
    else:
        EPGurl = PEPGurl
    moist.setSetting(id='epgUrl', value=EPGurl)
#    moist.setSetting(id='m3uCache', value="false")
#    moist.setSetting(id='epgCache', value="false")
    xbmc.executebuiltin("Container.Refresh")

def tvguidesetup():
        dialog = xbmcgui.Dialog().yesno(user.name,'Would You like to load the PVR settings now?')
        if dialog:
            pvrsetup()
            dialog = xbmcgui.Dialog().yesno(user.name, 'PVR Integration Complete.  Restart Kodi Now For Changes To Take Effect?')
            if dialog:
                xbmc.executebuiltin('ActivateWindow(shutdownmenu)')
        else:
            return



def num2day(num):
    if num =="0":
        day = 'monday'
    elif num=="1":
        day = 'tuesday'
    elif num=="2":
        day = 'wednesday'
    elif num=="3":
        day = 'thursday'
    elif num=="4":
        day = 'friday'
    elif num=="5":
        day = 'saturday'
    elif num=="6":
        day = 'sunday'
    return day
    
def extras():
    tools.addDir('Create IPTVXtra2 custom PVR M3U','url',17,icon,fanart,'')
    tools.addDir('Setup PVR Guide','tv',10,icon,fanart,'')
    tools.addDir('Run a Speed Test','ST',10,icon,fanart,'')
    tools.addDir('Clear Cache','CC',10,icon,fanart,'')
    

params=tools.get_params()
url=None
name=None
mode=None
iconimage=None
description=None
query=None
type=None

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
    description=urllib.unquote_plus(params["description"])
except:
    pass
try:
    query=urllib.unquote_plus(params["query"])
except:
    pass
try:
    type=urllib.unquote_plus(params["type"])
except:
    pass

if mode==None or url==None or len(url)<1:
    start()

elif mode==1:
    livecategory(url)
    
elif mode==2:
    Livelist(url)
    
elif mode==3:
    vod(url)
    
elif mode==4:
    stream_video(url)
    
elif mode==5:
    search()
    
elif mode==6:
    accountinfo()
    
elif mode==7:
    tvguide()
    
elif mode==8:
#    settingsmenu()
    xbmcaddon.Addon(user.id).openSettings()
elif mode==9:
    xbmc.executebuiltin('ActivateWindow(busydialog)')
    tools.Trailer().play(url) 
    xbmc.executebuiltin('Dialog.Close(busydialog)')
    
elif mode==10:
    addonsettings(url,description)
    
elif mode==11:
    pvrsetup()
    
elif mode==12:
    catchup()

elif mode==13:
    tvarchive(name,description)
    
elif mode==14:
    listcatchup2()
    
#elif mode==15:
#    showhelp(url)
    
elif mode==16:
    extras()
    
elif mode==17:
    m3uproc()

elif mode==18:
    makeStrm(name,url)
    xbmc.executebuiltin('Notification(IPTVXtra II,[B][COLOR lime]*'+name+'.strm created.[/COLOR][/B],5000,'+icon+')')
    xbmc.executebuiltin('updatelibrary(video)')

elif mode==9999:
    xbmcgui.Dialog().ok('ADDON','This Category Will Be Available Soon!')
    livecategory('url')

xbmcplugin.endOfDirectory(int(sys.argv[1]))