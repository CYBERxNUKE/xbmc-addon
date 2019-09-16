'''
    Ultimate Whitecream
    Copyright (C) 2016 Whitecream

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import urllib
import re
import os.path
import sys
import socket

import xbmc
import xbmcplugin
import xbmcaddon
from resources.lib import utils
from resources.lib import favorites
from resources.lib.sites import *

socket.setdefaulttimeout(60)

xbmcplugin.setContent(utils.addon_handle, 'movies')
addon = xbmcaddon.Addon(id=utils.__scriptid__)

progress = utils.progress
dialog = utils.dialog

imgDir = utils.imgDir
rootDir = utils.rootDir

@utils.url_dispatcher.register('0')
def INDEX():
    utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Scenes[/COLOR]','',1,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Movies[/COLOR]','',2,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Hentai[/COLOR]','',3,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Tubes[/COLOR]','',6,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Webcams & Streams[/COLOR]','',7,os.path.join(rootDir, 'icon.png'),'')
    utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Favorites[/COLOR]','',901,os.path.join(rootDir, 'icon.png'),'')
    download_path = addon.getSetting('download_path')
    if download_path != '' and os.path.exists(download_path):
        utils.addDir('[COLOR hotpink]Whitecream[/COLOR] [COLOR white]Download Folder[/COLOR]',download_path,4,os.path.join(rootDir, 'icon.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)

@utils.url_dispatcher.register('1')
def INDEXS():
    if sys.version_info >= (2, 7, 9):
        utils.addDir('[COLOR hotpink]WatchXXXFree[/COLOR]','http://www.watchxxxfree.com/page/1/',10,os.path.join(imgDir, 'wxf.png'),'')
        utils.addDir('[COLOR hotpink]PornTrex[/COLOR]','https://www.porntrex.com/videos?o=mr&page=1',50,os.path.join(imgDir, 'pt.png'),'')
    utils.addDir('[COLOR hotpink]PornAQ[/COLOR]','http://www.pornaq.com/page/1/',60,os.path.join(imgDir, 'paq.png'),'')
    utils.addDir('[COLOR hotpink]Porn00[/COLOR]','http://www.porn00.com/page/1/',64,os.path.join(imgDir, 'p00.png'),'')
    utils.addDir('[COLOR hotpink]Beeg[/COLOR]','http://beeg.com/page-1',80,os.path.join(imgDir, 'bg.png'),'')
    utils.addDir('[COLOR hotpink]ElReyX[/COLOR]','http://elreyx.com/index1.html',110,os.path.join(imgDir, 'elreyx.png'),'')
    utils.addDir('[COLOR hotpink]XvideoSpanish[/COLOR]','http://www.xvideospanish.net/',130,os.path.join(imgDir, 'xvideospanish.png'),'')
    utils.addDir('[COLOR hotpink]HQPorner[/COLOR]','http://hqporner.com/hdporn/1',150,os.path.join(imgDir, 'hqporner.png'),'')
    utils.addDir('[COLOR hotpink]VideoMegaPorn[/COLOR]','http://www.videomegaporn.com/index.html',160,os.path.join(imgDir, 'videomegaporn.png'),'')
    utils.addDir('[COLOR hotpink]StreamXXX[/COLOR]','http://streamxxx.tv/category/clips/',170,os.path.join(imgDir, 'streamxxx.png'),'')
    utils.addDir('[COLOR hotpink]JustPorn[/COLOR]','http://justporn.to/category/scenes/',240,os.path.join(imgDir, 'justporn.png'),'')
    utils.addDir('[COLOR hotpink]YourFreeTube[/COLOR]','http://www.yourfreetube.net/newvideos.html',190,'','')
    utils.addDir('[COLOR hotpink]Xtasie[/COLOR]','http://xtasie.com/porn-video-list/page/1/',200,os.path.join(imgDir, 'xtasie.png'),'')
    utils.addDir('[COLOR hotpink]HD Zog[/COLOR]','http://www.hdzog.com/new/',340,os.path.join(imgDir, 'hdzog.png'),'')    
    utils.addDir('[COLOR hotpink]Mr Sexe[/COLOR]','http://www.mrsexe.com/',400,os.path.join(imgDir, 'mrsexe.png'),'')
    utils.addDir('[COLOR hotpink]Ero-tik[/COLOR]','http://www.ero-tik.com/',260,os.path.join(imgDir, 'erotik.png'),'')
    utils.addDir('[COLOR hotpink]Czech3x[/COLOR]','http://czech3x.net/',310,os.path.join(imgDir, 'czechhd.png'),'')     
    utils.addDir('[COLOR hotpink]XXX Streams (eu)[/COLOR]','http://xxxstreams.eu/',410,os.path.join(imgDir, 'xxxstreams.png'),'')
    utils.addDir('[COLOR hotpink]XXX Streams (org)[/COLOR]','http://xxxstreams.org/',420,os.path.join(imgDir, 'xxxsorg.png'),'')
    utils.addDir('[COLOR hotpink]K18[/COLOR]','http://k18.co/',230,os.path.join(imgDir, 'k18.png'),'')
    utils.addDir('[COLOR hotpink]DaftSex[/COLOR]','https://daftsex.com/',610,os.path.join(imgDir, 'daftsex.png'),'')
    utils.addDir('[COLOR hotpink]PornsLand[/COLOR]','https://porns.land/recent-porns/',620,os.path.join(imgDir, 'pl.png'),'')
    utils.addDir('[COLOR hotpink]Vidz7[/COLOR]','http://www.vidz7.com/',640,'','')
    utils.addDir('[COLOR hotpink]YourPorn[/COLOR]','https://yourporn.sexy/',650,os.path.join(imgDir, 'yourpornsexy.png'),'')
    utils.addDir('[COLOR hotpink]JavWhores[/COLOR]','https://www.javwhores.com/',55,os.path.join(imgDir, 'javwhores.png'),'')
    utils.addDir('[COLOR hotpink]DatoPorn[/COLOR]','http://datoporn.co/',670,os.path.join(imgDir, 'datoporn.png'),'')
    utils.addDir('[COLOR hotpink]Pornvibe[/COLOR]','https://pornvibe.org/',680,os.path.join(imgDir, 'pornvibe.png'),'')
    utils.addDir('[COLOR hotpink]YesPornPlease[/COLOR]','https://yespornplease.com/',690,'','')

    utils.addDir('[COLOR hotpink]One list, to watch them all[/COLOR]','',5,'',1)
    xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)

@utils.url_dispatcher.register('2')
def INDEXM():
    if sys.version_info >= (2, 7, 9):
        utils.addDir('[COLOR hotpink]Xtheatre[/COLOR]','http://xtheatre.net/page/1/',20,os.path.join(imgDir, 'xt.png'),'')
    utils.addDir('[COLOR hotpink]PornHive[/COLOR]','http://www.pornhive.tv/en/movies/all',70,os.path.join(imgDir, 'ph.png'),'')
    utils.addDir('[COLOR hotpink]JustPorn[/COLOR]','http://justporn.to/category/dvdrips-full-movies/',245,os.path.join(imgDir, 'justporn.png'),'')
    utils.addDir('[COLOR hotpink]ElReyX[/COLOR]','http://elreyx.com/index1.html',116,os.path.join(imgDir, 'elreyx.png'),'')
    utils.addDir('[COLOR hotpink]PelisxPorno[/COLOR]','http://www.pelisxporno.com/',140,os.path.join(imgDir, 'pelisxporno.png'),'')
    utils.addDir('[COLOR hotpink]StreamXXX[/COLOR]','http://streamxxx.tv/category/movies/',175,os.path.join(imgDir, 'streamxxx.png'),'')
    utils.addDir('[COLOR hotpink]Cat3Movie[/COLOR]','http://cat3movie.us',350,os.path.join(imgDir, 'cat3movie.png'),'')
    utils.addDir('[COLOR hotpink]ParadiseHill[/COLOR]','http://www.paradisehill.tv/en/',250,os.path.join(imgDir, 'paradisehill.png'),'')
    utils.addDir('[COLOR hotpink]FreeOMovie[/COLOR]','http://www.freeomovie.com/',370,os.path.join(imgDir, 'freeomovie.png'),'')
    utils.addDir('[COLOR hotpink]Eroticage[/COLOR]','http://www.eroticage.net/',430,'','')
    xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)

@utils.url_dispatcher.register('6')
def INDEXT():
    utils.addDir('[COLOR hotpink]BubbaPorn[/COLOR]','http://www.bubbaporn.com/page1.html',90,os.path.join(imgDir, 'bubba.png'),'')
    utils.addDir('[COLOR hotpink]Poldertube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]','http://www.poldertube.nl/pornofilms/nieuw',100,os.path.join(imgDir, 'poldertube.png'),0)
    utils.addDir('[COLOR hotpink]Milf.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]','http://www.milf.nl/videos/nieuw',100,os.path.join(imgDir, 'milfnl.png'),1)
    utils.addDir('[COLOR hotpink]Sextube.nl[/COLOR] [COLOR orange](Dutch)[/COLOR]','http://www.sextube.nl/videos/nieuw',100,os.path.join(imgDir, 'sextube.png'),2)
    utils.addDir('[COLOR hotpink]TubePornClassic[/COLOR]','http://www.tubepornclassic.com/latest-updates/',360,os.path.join(imgDir, 'tubepornclassic.png'),'')
    utils.addDir('[COLOR hotpink]HClips[/COLOR]','http://www.hclips.com/latest-updates/',380,os.path.join(imgDir, 'hclips.png'),'')
    utils.addDir('[COLOR hotpink]PornHub[/COLOR]','https://www.pornhub.com/newest.html',390,os.path.join(imgDir, 'pornhub.png'),'')
    utils.addDir('[COLOR hotpink]Porndig[/COLOR] [COLOR white]Professional[/COLOR]','http://www.porndig.com',290,os.path.join(imgDir, 'porndig.png'),'')
    utils.addDir('[COLOR hotpink]Porndig[/COLOR] [COLOR white]Amateurs[/COLOR]','http://www.porndig.com',290,os.path.join(imgDir, 'porndig.png'),'')
    utils.addDir('[COLOR hotpink]AbsoluPorn[/COLOR]','http://www.absoluporn.com/en/',300,os.path.join(imgDir, 'absoluporn.gif'),'')
    utils.addDir('[COLOR hotpink]Anybunny[/COLOR]','http://anybunny.com/',320,os.path.join(imgDir, 'anybunny.png'),'')    
    utils.addDir('[COLOR hotpink]SpankBang[/COLOR]','http://spankbang.com/new_videos/',440,os.path.join(imgDir, 'spankbang.png'),'')	
    utils.addDir('[COLOR hotpink]Amateur Cool[/COLOR]','http://www.amateurcool.com/most-recent/',490,os.path.join(imgDir, 'amateurcool.png'),'')	
    utils.addDir('[COLOR hotpink]Vporn[/COLOR]','https://www.vporn.com/newest/',500,os.path.join(imgDir, 'vporn.png'),'')
    utils.addDir('[COLOR hotpink]xHamster[/COLOR]','https://xhamster.com/',505,os.path.join(imgDir, 'xhamster.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)

@utils.url_dispatcher.register('7')
def INDEXW():
    utils.addDir('[COLOR hotpink]Chaturbate[/COLOR] [COLOR white]- webcams[/COLOR]','https://chaturbate.com/?page=1',220,os.path.join(imgDir, 'chaturbate.png'),'')
    utils.addDir('[COLOR hotpink]MyFreeCams[/COLOR] [COLOR white]- webcams[/COLOR]','https://www.myfreecams.com',270,os.path.join(imgDir, 'myfreecams.jpg'),'')
    utils.addDir('[COLOR hotpink]Cam4[/COLOR] [COLOR white]- webcams[/COLOR]','http://www.cam4.com',280,os.path.join(imgDir, 'cam4.png'),'')    
    utils.addDir('[COLOR hotpink]Camsoda[/COLOR] [COLOR white]- webcams[/COLOR]','http://www.camsoda.com',475,os.path.join(imgDir, 'camsoda.png'),'')    
    utils.addDir('[COLOR hotpink]naked.com[/COLOR] [COLOR white]- webcams[/COLOR]','http://www.naked.com',480,os.path.join(imgDir, 'naked.png'),'')
    if sys.version_info >= (2, 7, 9):
        utils.addDir('[COLOR hotpink]streamate.com[/COLOR] [COLOR white]- webcams[/COLOR]','http://www.streammate.com',515,os.path.join(imgDir, 'streamate.png'),'')
    utils.addDir('[COLOR hotpink]bongacams.com[/COLOR] [COLOR white]- webcams[/COLOR]','http://www.bongacams.com',520,os.path.join(imgDir, 'bongacams.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)

@utils.url_dispatcher.register('3')
def INDEXH():
    utils.addDir('[COLOR hotpink]Hentaihaven[/COLOR]','http://hentaihaven.org/?sort=date',460,os.path.join(imgDir, 'hh.png'),'')
    utils.addDir('[COLOR hotpink]Animeid Hentai[/COLOR]','https://animeidhentai.com/hentai',660,os.path.join(imgDir, 'ah.png'),'')
    xbmcplugin.endOfDirectory(utils.addon_handle, cacheToDisc=False)    

@utils.url_dispatcher.register('5', ['page'])
def ONELIST(page=1):
    watchxxxfree.WXFList('http://www.watchxxxfree.com/page/1/',page, True)
    hdporn.PAQList('http://www.pornaq.com/page/1/',page, True)
    hdporn.PAQList('http://www.porn00.org/page/1/',page, True)
    porntrex.PTList('http://www.porntrex.com/videos?o=mr&page=1',page, True)
    npage = page + 1
    utils.addDir('[COLOR hotpink]Next page ('+ str(npage) +')[/COLOR]','',5,'',npage)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('4', ['url'])
def OpenDownloadFolder(url):
    xbmc.executebuiltin('ActivateWindow(Videos, ' + url + ')')


@utils.url_dispatcher.register('8')
def smrSettings():
    utils.resolveurl.display_settings()


def change():
    if addon.getSetting('changelog_seen_version') == utils.__version__ or not os.path.isfile(utils.changelog):
        return
    addon.setSetting('changelog_seen_version', utils.__version__)
    heading = '[B][COLOR hotpink]Whitecream[/COLOR] [COLOR white]Changelog[/COLOR][/B]'
    with open(utils.changelog) as f:
        cl_lines = f.readlines()
    announce = ''
    for line in cl_lines:
        if not line.strip():
            break
        announce += line
    utils.textBox(heading, announce)
    

if not addon.getSetting('uwcage') == 'true':
    age = dialog.yesno('WARNING: This addon contains adult material.','You may enter only if you are at least 18 years of age.', nolabel='Exit', yeslabel='Enter')
    if age:
        addon.setSetting('uwcage','true')
else:
    age = True


def main(argv=None):
    if sys.argv: argv = sys.argv
    queries = utils.parse_query(sys.argv[2])
    mode = queries.get('mode', None)
    utils.url_dispatcher.dispatch(mode, queries)


if __name__ == '__main__':
    if age:
        change()
        sys.exit(main())
