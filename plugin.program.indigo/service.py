import xbmc
import os
import shutil
import re
import urllib2
import datetime
from libs import kodi
import support
import xbmcaddon
import common as Common
import base64

addon_id = kodi.addon_id
AddonTitle = kodi.addon.getAddonInfo('name')
kodi.log('STARTING ' + AddonTitle + ' SERVICE')


############################
# addonPath = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
# addonPath = xbmc.translatePath(addonPath)
# xbmcPath = os.path.join(addonPath, "..", "..")
# xbmcPath = os.path.abspath(xbmcPath)

# addonpath = xbmcPath+'/addons/'
# mediapath = xbmcPath+'/media/'
# systempath = xbmcPath+'/system/'
# userdatapath = xbmcPath+'/userdata/'
# indisettingspath = xbmcPath+'/userdata/addon_data/'+addon_id+'/settings.xml'
# packagepath = xbmcPath + '/addons/packages/'

##############################
oldinstaller = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.addoninstaller'))
oldnotify = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.program.xbmchub.notifications'))
oldmain = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.xbmchubmaintool'))
oldwiz = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubwizard'))
oldfresh = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.freshstart'))
oldmain2 = xbmc.translatePath(os.path.join('special://home', 'addons', 'plugin.video.hubmaintool'))
# #############################

# #############################
# check = plugintools.get_setting("checkupdates")
# addonupdate = plugintools.get_setting("updaterepos")
# autoclean = plugintools.get_setting("acstartup")
# size_check = plugintools.get_setting("startupsize")
# CLEAR_CACHE_SIZE = plugintools.get_setting("cachemb")
# CLEAR_PACKAGES_SIZE = plugintools.get_setting("packagesmb")
# CLEAR_THUMBS_SIZE = plugintools.get_setting("thumbsmb")

# Check for old maintenance tools and remove them
old_maintenance = (oldinstaller, oldnotify, oldmain, oldwiz, oldfresh)
for old_file in old_maintenance:
    if os.path.exists(old_file):
        try:
            shutil.rmtree(old_file)
        except OSError:
            pass

# #############################
if xbmc.getCondVisibility('System.HasAddon(script.service.twitter)'):
    search_string = xbmcaddon.Addon('script.service.twitter').getSetting('search_string')
    search_string = search_string.replace('from:@', 'from:')
    xbmcaddon.Addon('script.service.twitter').setSetting('search_string', search_string)
    xbmcaddon.Addon('script.service.twitter').setSetting('enable_service', 'false')

# Start of notifications
if kodi.get_setting('hasran') == 'true':
    # kodi.log(AddonTitle + ' has ran before')
    TypeOfMessage = "t"
    (NewImage, NewMessage) = Common.FetchNews()
    Common.CheckNews(TypeOfMessage, NewImage, NewMessage, True)
else:
    kodi.log(AddonTitle + ' has NOT ran before')
# ################################################## ##
# ################################################## ##

# Start of program
# support.service_checks()
# support.scriptblock_checks()

# ################################################## ##
# ################################################## ##

date = datetime.datetime.today().weekday()
if  (kodi.get_setting("clearday") == date) or kodi.get_setting("acstartup") == "true":
    import maintool
    maintool.auto_clean(True)


if __name__ == '__main__':
    monitor = xbmc.Monitor()

    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds 12 hours is 43200   1 hours is 3600
        if monitor.waitForAbort(1800):
            # Abort was requested while waiting. We should exit
            kodi.log('CLOSING ' + AddonTitle.upper() + ' SERVICES')
            break
        if kodi.get_setting('scriptblock') == 'true':
            kodi.log('Checking for Malicious scripts')
            BlocksUrl = base64.b64decode('aHR0cDovL2luZGlnby50dmFkZG9ucy5jby9ibG9ja2VyL2Jsb2NrZXIudHh0')
            BlocksUrl = 'http://indigo.tvaddons.co/blocker/blocker.txt'
            req = urllib2.Request(BlocksUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
            try:
                response = urllib2.urlopen(req)
                link = response.read()
                response.close()
            except:
                kodi.log('Could not perform blocked script. invalid URL')
                break
            #     continue
            link = link.replace('\n', '').replace('\r', '').replace('\a', '')

            match = re.compile('block="(.+?)"').findall(link)
            for blocked in match:
                    addonPath = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
                    addonPath = xbmc.translatePath(addonPath)
                    xbmcPath = os.path.join(addonPath, "..", "..")
                    xbmcPath = os.path.abspath(xbmcPath)

                    addonpath = xbmcPath + '/addons/'
                    try:
                        for root, dirs, files in os.walk(addonpath, topdown=False):
                            if root != addonpath:
                                if blocked in root:
                                    shutil.rmtree(root)
                    except:
                        kodi.log('Could not find blocked script')

                        # #### NOT NEEDED WITH DIFFERENT AUTO CLEAN METHOD #####

                        # if kodi.get_setting ('automain') == 'true':
                        # xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
                        # if os.path.exists(xbmc_cache_path)==True:
                        # for root, dirs, files in os.walk(xbmc_cache_path):
                        # file_count = 0
                        # file_count += len(files)
                        # if file_count > 0:

                        # for f in files:
                        # try:
                        # os.unlink(os.path.join(root, f))
                        # except:
                        # pass
                        # for d in dirs:
                        # try:
                        # shutil.rmtree(os.path.join(root, d))
                        # except:
                        # pass

                        # kodi.log('Service could not clear cache')

                        # #DO PURGE IS NEEDED
                        # kodi.log('Purging Packages')
                        # packages_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
                        # try:
                        # for root, dirs, files in os.walk(packages_path,topdown=False):
                        # for name in files :
                        # os.remove(os.path.join(root,name))
                        # #kodi.log('Packages Wiped by Service')
                        # except:
                        # kodi.log('Service could not purge packages')
                        # else:
                        # pass
