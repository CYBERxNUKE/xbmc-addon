'''
    Ultimate Whitecream
    Copyright (C) 2015 Whitecream

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

import re

import xbmcplugin
from resources.lib import utils
 

@utils.url_dispatcher.register('150')
def HQMAIN():
    utils.addDir('[COLOR hotpink]Categories[/COLOR]','https://hqporner.com/porn-categories.php',153,'','')
    utils.addDir('[COLOR hotpink]Studios[/COLOR]','https://hqporner.com/porn-studios.php',153,'','')
    utils.addDir('[COLOR hotpink]Girls[/COLOR]','https://hqporner.com/porn-actress.php',153,'','')
    utils.addDir('[COLOR hotpink]Search[/COLOR]','https://hqporner.com/?s=',154,'','')
    HQLIST('https://hqporner.com/hdporn/1')
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('151', ['url'])
def HQLIST(url):
    try:
        link = utils.getHtml(url, '')
    except:
        return None
    match = re.compile('<a href="([^"]+)" class="image featured non-overlay".*?<img id="[^"]+" src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    for url, img, name in match:
        name = utils.cleantext(name)    
        videourl = "https://www.hqporner.com" + url
        if img.startswith('//'):
            img = 'https:' + img
        utils.addDownLink(name, videourl, 152, img, '')
    try:
        nextp=re.compile('<a href="([^"]+)"[^>]+>Next', re.DOTALL | re.IGNORECASE).findall(link)
        nextp = "https://www.hqporner.com" + nextp[0]
        utils.addDir('Next Page', nextp,151,'')
    except:
        pass
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('153', ['url'])
def HQCAT(url):
    link = utils.getHtml(url, '')
    tags = re.compile('<a href="([^"]+)"[^<]+<img src="([^"]+)" alt="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(link)
    tags = sorted(tags, key=lambda x: x[2])
    for caturl, catimg, catname in tags:
        caturl = "https://www.hqporner.com" + caturl
        catimg = "https://www.hqporner.com" + catimg        
        utils.addDir(catname,caturl,151,catimg)
    xbmcplugin.endOfDirectory(utils.addon_handle)


@utils.url_dispatcher.register('154', ['url'], ['keyword'])
def HQSEARCH(url, keyword=None):
    searchUrl = url
    if not keyword:
        utils.searchDir(url, 154)
    else:
        title = keyword.replace(' ','+')
        searchUrl = searchUrl + title
        print "Searching URL: " + searchUrl
        HQLIST(searchUrl)


@utils.url_dispatcher.register('152', ['url', 'name'], ['download'])
def HQPLAY(url, name, download=None):
    videopage = utils.getHtml(url, url)
    iframeurl = re.compile(r"nativeplayer\.php\?i=([^']+)", re.DOTALL | re.IGNORECASE).findall(videopage)[0]
    if iframeurl.startswith('//'):
        iframeurl = 'https:' + iframeurl
    if re.search('bemywife', iframeurl, re.DOTALL | re.IGNORECASE):
        videourl = getBMW(iframeurl)
    elif re.search('mydaddy', iframeurl, re.DOTALL | re.IGNORECASE):
        videourl = getBMW(iframeurl)        
    elif re.search('5\.79', iframeurl, re.DOTALL | re.IGNORECASE):
        videourl = getIP(iframeurl)
    elif re.search('flyflv', iframeurl, re.DOTALL | re.IGNORECASE):
        videourl = getFly(iframeurl)
    else:
        utils.notify('Oh oh','Couldn\'t find a supported videohost')
        return
    utils.playvid(videourl, name, download)


def getBMW(url):
    videopage = utils.getHtml(url, '')
    #redirecturl = utils.getVideoLink(url, '')
    #videodomain = re.compile("http://([^/]+)/", re.DOTALL | re.IGNORECASE).findall(redirecturl)[0]
    videos = re.compile(r'file: "([^"]+mp4)", label: "\d', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-2]
    if videourl.startswith('//'):
        videourl = 'https:' + videourl
    return videourl

def getIP(url):
    videopage = utils.getHtml(url, '')
    videos = re.compile('file": "([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-1]
    if videourl.startswith('//'):
        videourl = 'https:' + videourl
    return videourl

def getFly(url):
    videopage = utils.getHtml(url, '')
    videos = re.compile('fileUrl="([^"]+)"', re.DOTALL | re.IGNORECASE).findall(videopage)
    videourl = videos[-1]
    if videourl.startswith('//'):
        videourl = 'https:' + videourl
    return videourl
