import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os



ADDON = xbmcaddon.Addon(id='plugin.video.NUKE')
country=os.path.join(ADDON.getAddonInfo('path'),'resources','country')
print country
def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


if ADDON.getSetting('user')=='':
    dialog = xbmcgui.Dialog()
    dialog.ok("NUKE Streams", "You Now Need To Input", "Your [COLOR yellow]Username[/COLOR]")
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'NUKE Streams')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText() 
    ADDON.setSetting('user',search_entered)
    
if ADDON.getSetting('pass')=='':
    dialog = xbmcgui.Dialog()
    dialog.ok("NUKE Streams", "You Now Need To Input", "Your [COLOR yellow]Password[/COLOR]")
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'NUKE Streams')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText() 
    ADDON.setSetting('pass',search_entered)
    link=open(country).read()
    match=re.compile('name=(.+?)".+?"').findall(link)
    uniques=[]
    for name in match:
        if name not in uniques:
            uniques.append(name)
    dialog=xbmcgui.Dialog()
    name=uniques[xbmcgui.Dialog().select('Please Choose Your Region', uniques)]
    print name
    settimezone=[]
    regionselect=[]
    r='name=%s"(.+?)-(.+?)"'%name 
    print r
    link=open(country).read()
    match=re.compile(r).findall(link)  
    print match
    for country,region in match:
        regionselect.append(region)
        settimezone.append(country+'%2F'+region)
    region=settimezone[xbmcgui.Dialog().select('Please Select Closest City', regionselect)]
    ADDON.setSetting('timezone',region)
    ADDON.setSetting('firstrun','true')
    ADDON.setSetting('server',region)


