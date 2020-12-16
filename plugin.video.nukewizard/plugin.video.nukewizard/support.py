import base64
import os
import re
import shutil
import urllib2
import xbmc
import xbmcaddon

from libs import kodi

addon_id = kodi.addon_id

BlocksUrl = base64.b64decode('aHR0cDovL2luZGlnby50dmFkZG9ucy5hZy9ibG9ja2VyL2Jsb2NrZXIudHh0')


def service_checks():
    if kodi.get_setting('automain') == 'true':
        clear_cache()
        purge_packages()
    else:
        kodi.log('Auto Main Turned off')


def scriptblock_checks():
    if kodi.get_setting('scriptblock') == 'true':
        kodi.log('SCRIPT BLOCKER ON')

        req = urllib2.Request(BlocksUrl)
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Linux; U; Android 4.2.2; en-us; AFTB Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
        response = urllib2.urlopen(req)
        link = response.read()
        response.close()
        link = link.replace('\n', '').replace('\r', '').replace('\a', '')

        match = re.compile('block="(.+?)"').findall(link)
        for blocked in match:
            kodi.log('Checking for Malicious scripts')

            addonPath = xbmcaddon.Addon(id=addon_id).getAddonInfo('path')
            addonPath = xbmc.translatePath(addonPath)
            xbmcPath = os.path.join(addonPath, "..", "..")
            xbmcPath = os.path.abspath(xbmcPath);

            addonpath = xbmcPath + '/addons/'
            try:
                for root, dirs, files in os.walk(addonpath, topdown=False):
                    if root != addonpath:
                        if blocked in root:
                            shutil.rmtree(root)
            except:
                kodi.log('Could not find blocked script')


def clear_cache():
    kodi.log('STARTUP CLEAR CACHE ACTIVATED')
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    if os.path.exists(xbmc_cache_path) == True:
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:

                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    if 'archive_cache' not in d:
                        try:
                            shutil.rmtree(os.path.join(root, d))
                        except:
                            pass

        kodi.log('Startup Service could not clear cache')


def purge_packages():
    kodi.log('STARTUP PURGE PACKAGES ACTIVATED')
    packages_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
    try:
        for root, dirs, files in os.walk(packages_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            # kodi.log('Packages Wiped by Service')
            # dialog = xbmcgui.Dialog()
            # dialog.ok(AddonTitle, "                     Packages Folder Wiped Successfully!")


    except:
        kodi.log('Startup Service could not purge packages')
