# -*- coding: cp1252 -*-
# Main Module by: Blazetamer
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,os,xbmcaddon
try: 		from t0mm0.common.addon import Addon
except: from t0mm0_common_addon import Addon
try: 		from t0mm0.common.net import Net
except: from t0mm0_common_net import Net
#Define common.addon
addon_id='plugin.video.nukewizard'
addon=Addon(addon_id, sys.argv)
# Global Stuff
settings=xbmcaddon.Addon(id=addon_id)
net=Net()

# HELPDIR
def addHELPDir(name,url,mode,iconimage,fanart,description,filetype): u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)+"&filetype="+urllib.quote_plus(filetype); ok=True; liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage); liz.setInfo(type="Video",infoLabels={"title":name,"Plot":description}); liz.setProperty("Fanart_Image",fanart); ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False); return ok
# Standard addDir
def addDir(name,url,mode,thumb,labels,favtype):
	contextMenuItems=[]; sitethumb=thumb; sitename=name
	try: name=data['title']; thumb=data['cover_url']; fanart=data['backdrop_url']
	except: name=sitename
	if thumb=='': thumb=sitethumb
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True; liz=xbmcgui.ListItem(name,iconImage="DefaultFolder.png",thumbnailImage=thumb); liz.setInfo(type="Video",infoLabels=labels)
	if favtype == 'movie':     contextMenuItems.append(('Movie Information','XBMC.Action(Info)'))
	elif favtype == 'tvshow':  contextMenuItems.append(('TV Show  Information','XBMC.Action(Info)'))
	elif favtype == 'episode': contextMenuItems.append(('TV Show  Information','XBMC.Action(Info)'))       
	liz.addContextMenuItems(contextMenuItems, replaceItems=False)
	try: liz.setProperty("Fanart_Image",labels['backdrop_url'])
	except: pass
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True); return ok
# Set View
def doSetView(s): xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting(s))
# AutoView
def AUTO_VIEW(content):
	if content:
		xbmcplugin.setContent(int(sys.argv[1]),content)
		if settings.getSetting('auto-view')=='true':
			if content=='movies': doSetView('movies-view')
			elif content=='list': doSetView('default-view')
			else: doSetView('default-view')
		else: doSetView('default-view')
