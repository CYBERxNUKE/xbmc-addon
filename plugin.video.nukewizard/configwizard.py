# Config Wizard By: Blazetamer 2013-2016
import downloader
import extract
import os
import re
import sys
import urllib
import urllib2
import xbmc
import xbmcgui
import xbmcplugin

from libs import addon_able
from libs import kodi

AddonTitle = kodi.addon.getAddonInfo('name')
SiteDomain = 'TVADDONS.AG'
TeamName = 'Indigo'
wizlink = "http://indigo.tvaddons.ag/wizard/updates.txt"
cutslink = "http://indigo.tvaddons.ag/wizard/shortcuts.txt"


# ==========================Help WIZARD=====================================================================================================
def HELPCATEGORIES():
    filetype = 'main'
    link = OPEN_URL(wizlink).replace('\n', '').replace('\r', '').replace('\a', '').strip()
    HELPWIZARD('configwiz', link, '', 'main', )


## ### ##
def HELPWIZARD(name, url, description, filetype):
    path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
    confirm = xbmcgui.Dialog().yesno("Please Confirm",
                                     "                Please confirm that you wish to automatically                     ",
                                     "            configure Kodi with all the best addons and tweaks!",
                                     "              ", "Cancel", "Install")
    filetype = filetype.lower()
    if confirm:
        path = xbmc.translatePath(os.path.join('special://home', 'addons', 'packages'))
        dp = xbmcgui.DialogProgress()
        dp.create(AddonTitle, " ", 'Downloading and Configuring ', 'Please Wait')
        lib = os.path.join(path, name + '.zip')
        try:
            os.remove(lib)
        except:
            pass
        ### ## ... ##
        # kodi.log(url)
        if str(url).endswith('[error]'):
            print url
            dialog = xbmcgui.Dialog()
            dialog.ok("Error!", url)
            return
        if '[error]' in url:
            print url
            dialog = xbmcgui.Dialog()
            dialog.ok("Error!", url)
            return
        downloader.download(url, lib, dp)
        if filetype == 'main':
            addonfolder = xbmc.translatePath('special://home')
        elif filetype == 'addon':
            addonfolder = xbmc.translatePath(os.path.join('special://home', 'addons'))
        else:
            print {'filetype': filetype}
            dialog = xbmcgui.Dialog()
            dialog.ok("Error!", 'filetype: "%s"' % str(filetype))
            return
        xbmc.sleep(4000)
        extract.all(lib, addonfolder, dp)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        addon_able.setall_enable()
        try:
            os.remove(lib)
        except:
            pass
        if filetype == 'main':
            link = OPEN_URL(cutslink)
            shorts = re.compile('shortcut="(.+?)"').findall(link)
            for shortname in shorts:
                xEB('Skin.SetString(%s)' % shortname)
                enableBG16 = "UseCustomBackground,true"
                enableBG17 = "use_custom_bg,true"
                xEB('Skin.SetBool(%s)' % enableBG16)
                xEB('Skin.SetBool(%s)' % enableBG17)

        xbmc.sleep(4000)
        xbmc.executebuiltin('XBMC_UpdateLocalAddons()')
        addon_able.setall_enable()

        kodi.set_setting("wizardran", 'true')

        dialog = xbmcgui.Dialog()
        dialog.ok(TeamName, "Installation Complete!", "", "Click OK to exit Kodi and then restart to complete .")
        xbmc.executebuiltin('ShutDown')


def addHELPDir(name, url, mode, iconimage, fanart, description, filetype):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&iconimage=" + urllib.quote_plus(iconimage) + "&fanart=" + urllib.quote_plus(
        fanart) + "&description=" + urllib.quote_plus(description) + "&filetype=" + urllib.quote_plus(filetype)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"title": name, "Plot": description})
    liz.setProperty("Fanart_Image", fanart)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    return link


def xEB(t): xbmc.executebuiltin(t)
