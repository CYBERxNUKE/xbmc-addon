# -*- coding: utf-8 -*-
import sys
l111llll1UK_Turk_No1 = sys.version_info [0] == 2
l1l1ll11lUK_Turk_No1 = 2048
l11l1111lUK_Turk_No1 = 7
def l11l1lUK_Turk_No1 (l1llll1lUK_Turk_No1):
    global l1l1lll11UK_Turk_No1
    l1l111111UK_Turk_No1 = ord (l1llll1lUK_Turk_No1 [-1])
    l11l11ll1UK_Turk_No1 = l1llll1lUK_Turk_No1 [:-1]
    l1lll1lllUK_Turk_No1 = l1l111111UK_Turk_No1 % len (l11l11ll1UK_Turk_No1)
    l1l1l1111UK_Turk_No1 = l11l11ll1UK_Turk_No1 [:l1lll1lllUK_Turk_No1] + l11l11ll1UK_Turk_No1 [l1lll1lllUK_Turk_No1:]
    if l111llll1UK_Turk_No1:
        l1ll1llUK_Turk_No1 = unicode () .join ([unichr (ord (char) - l1l1ll11lUK_Turk_No1 - (l11lllUK_Turk_No1 + l1l111111UK_Turk_No1) % l11l1111lUK_Turk_No1) for l11lllUK_Turk_No1, char in enumerate (l1l1l1111UK_Turk_No1)])
    else:
        l1ll1llUK_Turk_No1 = str () .join ([chr (ord (char) - l1l1ll11lUK_Turk_No1 - (l11lllUK_Turk_No1 + l1l111111UK_Turk_No1) % l11l1111lUK_Turk_No1) for l11lllUK_Turk_No1, char in enumerate (l1l1l1111UK_Turk_No1)])
    return eval (l1ll1llUK_Turk_No1)
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,os,re,sys,datetime,urlresolver,random,liveresolver,base64,pyxbmct,glob,net,json
from resources.lib.common_addon import Addon
from HTMLParser import HTMLParser
from metahandler import metahandlers
from resources.lib import scraper1
from resources.lib import scraper2
from resources.lib import scraper3
from resources.lib import l111111UK_Turk_No1
from resources.lib import l1111UK_Turk_No1
from resources.lib import l11lll1lUK_Turk_No1
from resources.lib import l11l1111UK_Turk_No1
from resources.lib import l1l11l1l1UK_Turk_No1
from resources.lib import l111l11l1UK_Turk_No1
from resources.lib import l11ll1lUK_Turk_No1
from resources.lib import l1l1l11llUK_Turk_No1
from resources.lib import l1l1111UK_Turk_No1
from resources.lib import l1l111l11UK_Turk_No1
from resources.lib import l1l1lll1lUK_Turk_No1
from resources.lib import wizard as l1l1l111UK_Turk_No1, downloader as l1l11lUK_Turk_No1, notify
import time;import ntpath;
import shutil;import zipfile;import hashlib;
import platform;
import subprocess
import xbmcvfs
import atexit
import cookielib
import uuid
import plugintools
import webbrowser as l1ll11l1UK_Turk_No1
from uuid import getnode as l11ll1UK_Turk_No1
mac = l11ll1UK_Turk_No1()
l11l1ll1lUK_Turk_No1   = xbmcaddon.Addon(l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡻ࡯ࡤࡦࡱ࠱ࡹࡰࡺࡵࡳ࡭ࠪࠀ"))
addon_id        = l11l1lUK_Turk_No1 (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡺࡱࡴࡶࡴ࡮ࠫࠁ")
DP              = xbmcgui.DialogProgress()
addon           = Addon(addon_id, sys.argv)
l1l1111lUK_Turk_No1       = xbmcaddon.Addon(id=addon_id)
l11l1l111UK_Turk_No1        = xbmc.translatePath(l1l1111lUK_Turk_No1.getAddonInfo(l11l1lUK_Turk_No1 (u"࠭ࡰࡳࡱࡩ࡭ࡱ࡫ࠧࠂ")))
DIALOG          = xbmcgui.Dialog()
l11l111llUK_Turk_No1      = xbmc.translatePath(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࠩࠃ"))+l11l1lUK_Turk_No1 (u"ࠨ࠱࠭࠲࠯࠭ࠄ")
l1l11l1UK_Turk_No1    = xbmc.translatePath(l11l1lUK_Turk_No1 (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࡥࡩࡪ࡯࡯ࡵ࠲ࠫࠅ"))
fanart          = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠪࡷࡵ࡫ࡣࡪࡣ࡯࠾࠴࠵ࡨࡰ࡯ࡨ࠳ࡦࡪࡤࡰࡰࡶ࠳ࠬࠆ") + addon_id, l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷ࠲࡯ࡶࡧࠨࠇ")))
l1l1111llUK_Turk_No1         = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࠧࠈ") + addon_id, l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡰࡤࡶࡹ࠴ࡪࡱࡩࠪࠉ")))
icon            = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࠩࠊ") + addon_id, l11l1lUK_Turk_No1 (u"ࠨ࡫ࡦࡳࡳ࠴ࡰ࡯ࡩࠪࠋ")))
HOME            = xbmc.translatePath(l11l1lUK_Turk_No1 (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࠫࠌ"))
ADDONS          = os.path.join(HOME,      l11l1lUK_Turk_No1 (u"ࠪࡥࡩࡪ࡯࡯ࡵࠪࠍ"))
PACKAGES        = os.path.join(ADDONS,    l11l1lUK_Turk_No1 (u"ࠫࡵࡧࡣ࡬ࡣࡪࡩࡸ࠭ࠎ"))
l11ll1l1lUK_Turk_No1        = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࠧࠏ") + addon_id, l11l1lUK_Turk_No1 (u"࠭࡮ࡦࡺࡷ࠲ࡵࡴࡧࠨࠐ")))
l11111lUK_Turk_No1        = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠧࡢࡦࡸࡰࡹ࠭ࠑ"))
l111l1lllUK_Turk_No1       = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪࠒ"))
l11111lUK_Turk_No1        = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡤࡨࡺࡲࡴࠨࠓ"))
l1ll1l1UK_Turk_No1         = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠪࡴ࡮ࡴࠧࠔ"))
count           = int(l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫࡨࡵࡵ࡯ࡶࠪࠕ")))
metaset         = l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡤࡳࡥࡵࡣࠪࠖ"))
l1lll1UK_Turk_No1        = xbmc.translatePath(l11l1lUK_Turk_No1 (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡶࡵࡨࡶࡩࡧࡴࡢ࠱ࡤࡨࡩࡵ࡮ࡠࡦࡤࡸࡦ࠵ࠧࠗ") + addon_id)
l1ll1ll1lUK_Turk_No1         = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡷࡶࡩࡷࡪࡡࡵࡣ࠲ࡈࡦࡺࡡࡣࡣࡶࡩࠬ࠘"), l11l1lUK_Turk_No1 (u"ࠨࡗࡎࡘࡺࡸ࡫࠯ࡦࡥࠫ࠙")))
l1ll1l1l1UK_Turk_No1      = l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡩࡪ࡯࡯ࡥ࡯ࡳࡺࡪ࠮ࡰࡴࡪ࠳ࡺࡱࡴࡶࡴ࡮࠳࡚ࡑࡔࡶࡴ࡮࠳ࡺࡱࡴࡶࡴ࡮࠽࠵࠸࠱࠱࠰࡭ࡴ࡬࠭ࠚ")
l1lll111UK_Turk_No1 =l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡼࡽࡷ࠯ࡩࡲࡳ࡬ࡲࡥࡢࡲ࡬ࡷ࠳ࡩ࡯࡮࠱ࡼࡳࡺࡺࡵࡣࡧ࠲ࡺ࠸࠵ࡳࡦࡣࡵࡧ࡭ࡅࡱ࠾ࠩࠛ")
l111l111lUK_Turk_No1 =l11l1lUK_Turk_No1 (u"ࠫࠫࡸࡥࡨ࡫ࡲࡲࡈࡵࡤࡦ࠿ࡘࡗࠫࡶࡡࡳࡶࡀࡷࡳ࡯ࡰࡱࡧࡷࠪ࡭ࡲ࠽ࡦࡰࡢ࡙ࡘࠬ࡫ࡦࡻࡀࡅࡎࢀࡡࡔࡻࡅ࡫࡝࡬ࡄ࠱ࡉࡻ࡭ࡸࡰࡖࡩ࡯࡙࠶࡯࠶ࡪࡣࡆ࡚ࡍ࡝ࡑࡷࡰ࠶ࡄࡧ࠽ࡽࡷࠧࡶࡼࡴࡪࡃࡶࡪࡦࡨࡳࠫࡳࡡࡹࡔࡨࡷࡺࡲࡴࡴ࠿࠸࠴ࠬࠜ")
l1111lll1UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡵࡧ࡭ࡧࡤࡴ࡮ࡹ࠮ࡤࡱࡰ࠳ࡾࡵࡵࡵࡷࡥࡩ࠴ࡼ࠳࠰ࡲ࡯ࡥࡾࡲࡩࡴࡶࡌࡸࡪࡳࡳࡀࡲࡤࡶࡹࡃࡳ࡯࡫ࡳࡴࡪࡺࠦࡱ࡮ࡤࡽࡱ࡯ࡳࡵࡋࡧࡁࠬࠝ")
l111l11UK_Turk_No1 = l11l1lUK_Turk_No1 (u"࠭ࠦ࡮ࡣࡻࡖࡪࡹࡵ࡭ࡶࡶࡁ࠺࠶ࠦ࡬ࡧࡼࡁࡆࡏࡺࡢࡕࡼࡆ࡬࡞ࡦࡅ࠲ࡊࡼ࡮ࡹࡪࡗࡪࡰ࡚࠷ࡰ࠰࡫ࡤࡇ࡛ࡎ࡞ࡋࡸࡱ࠷ࡅࡨ࠾ࡷࡸࠩࠞ")
l1l1lll1UK_Turk_No1 = open(l1ll1ll1lUK_Turk_No1,l11l1lUK_Turk_No1 (u"ࠧࡢࠩࠟ"))
l1l1lll1UK_Turk_No1.close()
net = net.Net()
l111l1111UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡨࡩࡵ࡮ࡤ࡮ࡲࡹࡩ࠴࡯ࡳࡩ࠲ࡻ࡮ࢀࡡࡳࡦ࠱ࡴ࡭ࡶࠧࠠ")
USER_AGENT   = l11l1lUK_Turk_No1 (u"ࠩࡐࡳࡿ࡯࡬࡭ࡣ࠲࠹࠳࠶࡙ࠠࠩ࡬ࡲࡩࡵࡷࡴࠢࡑࡘࠥ࠷࠰࠯࠲࠾ࠤ࡜ࡕࡗ࠷࠶ࠬࠤࡆࡶࡰ࡭ࡧ࡚ࡩࡧࡑࡩࡵ࠱࠸࠷࠼࠴࠳࠷ࠢࠫࡏࡍ࡚ࡍࡍ࠮ࠣࡰ࡮ࡱࡥࠡࡉࡨࡧࡰࡵࠩࠡࡅ࡫ࡶࡴࡳࡥ࠰࠶࠺࠲࠵࠴࠲࠶࠴࠹࠲࠼࠹ࠠࡔࡣࡩࡥࡷ࡯࠯࠶࠵࠺࠲࠸࠼ࠠࡓࡧࡳࡰ࡮ࡩࡡ࡯ࡶ࡚࡭ࡿࡧࡲࡥ࠱࠴࠲࠵࠴࠰ࠨࠡ")
l1lllllllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"࡙ࠥࡐ࡚ࡵࡳ࡭ࡶࠦࠢ")
P = plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠫࡵ࡯࡮ࠨࠣ"))
M = plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠬࡹࡵࡣ࡯ࡨࡷࡸࡧࡧࡦࠩࠤ"))
def l11lll11lUK_Turk_No1():
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡸࠪࠥ"),l11l1lUK_Turk_No1 (u"ࠧ࡯ࡱࠪࠦ"))
        if not os.path.exists(l1lll1UK_Turk_No1):
                os.mkdir(l1lll1UK_Turk_No1)
        link=l1llll111UK_Turk_No1(l1ll1l1l1UK_Turk_No1)
	l1l1l1l1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾࡬ࡲࡩ࡫ࡸ࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡱࡨࡪࡾ࠾ࠨࠧ")).findall(link)[0]
	link=l1llll111UK_Turk_No1(l1l1l1l1lUK_Turk_No1)
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠩࡱࡥࡲ࡫࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠯࠭ࡂࡶࡱࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠮ࠬࡁࡰ࡫ࡂࠨࠨ࠯࠭ࡂ࠭ࠧ࠭ࠨ"),re.DOTALL).findall(link)
	for name,url,l1l11l11UK_Turk_No1 in match:
		if not l11l1lUK_Turk_No1 (u"ࠪ࡜࡝࡞ࠧࠩ") in name:
			l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
		if l11l1lUK_Turk_No1 (u"ࠫ࡝࡞ࡘࠨࠪ") in name:
			if l11111lUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠬࡺࡲࡶࡧࠪࠫ"):
				if l111l1lllUK_Turk_No1 == l11l1lUK_Turk_No1 (u"࠭ࠧࠬ"):
				    dialog = xbmcgui.Dialog()
				    ret = dialog.yesno(l11l1lUK_Turk_No1 (u"ࠧࡂࡦࡸࡰࡹࠦࡃࡰࡰࡷࡩࡳࡺࠧ࠭"), l11l1lUK_Turk_No1 (u"ࠨ࡛ࡲࡹࠥ࡮ࡡࡷࡧࠣࡳࡵࡺࡥࡥࠢࡷࡳࠥࡹࡨࡰࡹࠣࡥࡩࡻ࡬ࡵࠢࡦࡳࡳࡺࡥ࡯ࡶࠪ࠮"),l11l1lUK_Turk_No1 (u"ࠩࠪ࠯"),l11l1lUK_Turk_No1 (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡷࡪࡺࠠࡢࠢࡳࡥࡸࡹࡷࡰࡴࡧࠤࡹࡵࠠࡱࡴࡨࡺࡪࡴࡴࠡࡣࡦࡧ࡮ࡪࡥ࡯ࡶࡤࡰࠥࡧࡣࡤࡧࡶࡷࠬ࠰"),l11l1lUK_Turk_No1 (u"ࠫࡈࡧ࡮ࡤࡧ࡯ࠫ࠱"),l11l1lUK_Turk_No1 (u"ࠬࡒࡥࡵࡵࠣࡋࡴ࠭࠲"))
				    if ret == 1:
					l1lll11l1UK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"࠭ࠧ࠳"), l11l1lUK_Turk_No1 (u"ࠧࡔࡧࡷࠤࡕࡧࡳࡴࡹࡲࡶࡩ࠭࠴"))
					l1lll11l1UK_Turk_No1.doModal()
					if (l1lll11l1UK_Turk_No1.isConfirmed()):
					    l1l1UK_Turk_No1 = l1lll11l1UK_Turk_No1.getText()
					    l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ࠵"),l1l1UK_Turk_No1)
					l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
			if l11111lUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠩࡷࡶࡺ࡫ࠧ࠶"):
				if l111l1lllUK_Turk_No1 <> l11l1lUK_Turk_No1 (u"ࠪࠫ࠷"):
					l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
	l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳࠨ࠸"),l1ll1ll1lUK_Turk_No1,15,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡧࡤࡥࡱࡱࡧࡱࡵࡵࡥ࠰ࡲࡶ࡬࠵ࡵ࡬ࡶࡸࡶࡰ࠵ࡕࡌࡖࡸࡶࡰ࠵ࡴࡩࡷࡰࡦࡸ࠵࡮ࡦࡹ࠲࡙ࡰࠫ࠲࠱ࡶࡸࡶࡰࠫ࠲࠱ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡷࠪ࠸࠰ࡧࡣࡹࡳࡺࡸࡩࡵࡧࡶ࠲࡯ࡶࡧࠨ࠹"),fanart)
	l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࠭ࡓࡦࡣࡵࡧ࡭࠭࠺"),l11l1lUK_Turk_No1 (u"ࠧࡶࡴ࡯ࠫ࠻"),5,l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡣࡧࡨࡴࡴࡣ࡭ࡱࡸࡨ࠳ࡵࡲࡨ࠱ࡸ࡯ࡹࡻࡲ࡬࠱ࡘࡏ࡙ࡻࡲ࡬࠱ࡷ࡬ࡺࡳࡢࡴ࠱ࡱࡩࡼ࠵ࡕ࡬ࠧ࠵࠴ࡹࡻࡲ࡬ࠧ࠵࠴ࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲࡳࠦ࠴࠳ࡷࡪࡧࡲࡤࡪ࠱࡮ࡵ࡭ࠧ࠼"),fanart)
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨ࠽"))
	l1l1l11l1UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪࡱࡴࡼࡩࡦࡵࠪ࠾"), l11l1lUK_Turk_No1 (u"ࠫࡒࡇࡉࡏࠩ࠿"),link)
def l11l1ll11UK_Turk_No1(url):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩࡀ"),l11l1lUK_Turk_No1 (u"࠭ࡹࡦࡵࠪࡁ"))
        l11111ll1UK_Turk_No1 = None
	file = open(l1ll1ll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡳࠩࡂ"))
	l11111ll1UK_Turk_No1 = file.read()
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠣ࠾࡬ࡸࡪࡳ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡪࡶࡨࡱࡃࠨࡃ"),re.DOTALL).findall(l11111ll1UK_Turk_No1)
	for item in match:
                data=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡮ࡺ࡬ࡦࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡭ࡹࡲࡥ࠿࠰࠮ࡃࡱ࡯࡮࡬ࡀࠫ࠲࠰ࡅࠩ࠽࠱࡯࡭ࡳࡱ࠾࠯࠭ࡂࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪࡄ"),re.DOTALL).findall(item)
                for name,url,l1l11l11UK_Turk_No1 in data:
                        if l11l1lUK_Turk_No1 (u"ࠪ࠲ࡹࡾࡴࠨࡅ") in url:
                                l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
                        else:
                                l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
def l1111ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
	url=url.replace(l11l1lUK_Turk_No1 (u"ࠫࠥ࠭ࡆ"),l11l1lUK_Turk_No1 (u"ࠬࠫ࠲࠱ࠩࡇ"))
	l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"࠭ࠠࠨࡈ"),l11l1lUK_Turk_No1 (u"ࠧࠦ࠴࠳ࠫࡉ"))
	string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡉࡅ࡛ࡄ࠼ࡪࡶࡨࡱࡃࡢ࡮࠽ࡶ࡬ࡸࡱ࡫࠾ࠨࡊ")+name+l11l1lUK_Turk_No1 (u"ࠩ࠿࠳ࡹ࡯ࡴ࡭ࡧࡁࡠࡳࡂ࡬ࡪࡰ࡮ࡂࠬࡋ")+url+l11l1lUK_Turk_No1 (u"ࠪࡀ࠴ࡲࡩ࡯࡭ࡁࡠࡳ࠭ࡌ")+l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩࡍ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂ࠯ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࡠࡳࡂ࠯ࡪࡶࡨࡱࡃࡂ࠯ࡇࡃ࡙ࡂࡡࡴࠧࡎ")
	l1l1lll1UK_Turk_No1 = open(l1ll1ll1lUK_Turk_No1,l11l1lUK_Turk_No1 (u"࠭ࡡࠨࡏ"))
	l1l1lll1UK_Turk_No1.write(string)
	l1l1lll1UK_Turk_No1.close()
def l11l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
	l11111ll1UK_Turk_No1 = None
	file = open(l1ll1ll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡳࠩࡐ"))
	l11111ll1UK_Turk_No1 = file.read()
	l11l1l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩࡑ")
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭ࡹ࡫࡭࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡷࡩࡲࡄࠧࡒ"),re.DOTALL).findall(l11111ll1UK_Turk_No1)
	for data in match:
		string=l11l1lUK_Turk_No1 (u"ࠪࡠࡳࡂࡆࡂࡘࡁࡀ࡮ࡺࡥ࡮ࡀ࡟ࡲࠬࡓ")+data+l11l1lUK_Turk_No1 (u"ࠫࡁ࠵ࡩࡵࡧࡰࡂࡡࡴࠧࡔ")
		if name in data:
			string=string.replace(l11l1lUK_Turk_No1 (u"ࠬ࡯ࡴࡦ࡯ࠪࡕ"),l11l1lUK_Turk_No1 (u"࠭ࠠࠨࡖ"))
		l11l1l11UK_Turk_No1=l11l1l11UK_Turk_No1+string
	file = open(l1ll1ll1lUK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧࡸࠩࡗ"))
	file.truncate()
	file.write(l11l1l11UK_Turk_No1)
	file.close()
	xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡗ࡫ࡦࡳࡧࡶ࡬ࠬࡘ"))
def l1lll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1,fanart):
        l1l1l11lUK_Turk_No1=l1llllUK_Turk_No1(name)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠩࡷࡺ࡙ࠬ"),l1l1l11lUK_Turk_No1)
        link=l1llll111UK_Turk_No1(url)
        if l11l1lUK_Turk_No1 (u"ࠪ࠳࡚ࡑࡔࡶࡴ࡮࠳࡙ࡻࡲ࡬࡫ࡶ࡬࡙࡜࠮ࡵࡺࡷ࡚ࠫ") in url: l1l11llllUK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠫ࠴࡛ࡋࡕࡷࡵ࡯࠴࡚ࡵࡳ࡭࡬ࡷ࡭࡚ࡖ࠯ࡶࡻࡸ࡛ࠬ") in url: KD()
        if l11l1lUK_Turk_No1 (u"ࠬ࠵ࡕࡌࡖࡸࡶࡰ࠵ࡔࡶࡴ࡮࡭ࡸ࡮ࡔࡗ࠰ࡷࡼࡹ࠭࡜") in url: l1l11l1llUK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"࠭࠯ࡖࡍࡗࡹࡷࡱ࠯ࡕࡷࡵ࡯࡮ࡹࡨࡕࡘ࠱ࡸࡽࡺࠧ࡝") in url: l11llll1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠧ࠰ࡗࡎࡘࡺࡸ࡫࠰ࡖࡸࡶࡰ࡯ࡳࡩࡖ࡙࠲ࡹࡾࡴࠨ࡞") in url: l1lll1ll1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠨ࠱ࡘࡏ࡙ࡻࡲ࡬࠱ࡷࡺࠪ࠸࠰ࡴࡪࡲࡻࡸ࠵ࡉ࡯ࡦࡨࡼ࠳ࡺࡸࡵࠩ࡟") in url: l1ll1ll11UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠩ࠲࡙ࡐ࡚ࡵࡳ࡭࠲ࡸࡻࠫ࠲࠱ࡵ࡫ࡳࡼࡹ࠯ࡊࡰࡧࡩࡽ࠴ࡴࡹࡶࠪࡠ") in url: l11ll11l1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠪ࠳࡚ࡑࡔࡶࡴ࡮࠳ࡘࡶ࡯ࡳࡶࡶࡐ࡮ࡹࡴ࠯ࡶࡻࡸࠬࡡ") in url: l1lll111lUK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠫ࠴࡛ࡋࡕࡷࡵ࡯࠴࡙ࡰࡰࡴࡷࡷࡑ࡯ࡳࡵ࠰ࡷࡼࡹ࠭ࡢ") in url: l111111l1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠬ࠵ࡕࡌࡖࡸࡶࡰ࠵࡭ࡰࡸ࡬ࡩࡸ࠵ࡉ࡯ࡦࡨࡼ࠳ࡺࡸࡵࠩࡣ") in url: l1l1111l1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"࠭࠯ࡖࡍࡗࡹࡷࡱ࠯ࡤࡣࡵࡸࡴࡵ࡮ࡴ࠱ࡌࡲࡩ࡫ࡸ࠯ࡶࡻࡸࠬࡤ") in url: l1ll111l1UK_Turk_No1()
        if l11l1lUK_Turk_No1 (u"ࠧࡊࡰࡧࡩࡽ࠭ࡥ") in url:
                l1lllll1lUK_Turk_No1(url)
        if l11l1lUK_Turk_No1 (u"ࠨ࡚࡛࡜ࠬࡦ") in name: l1l1ll1UK_Turk_No1(link)
        match= re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭ࡹ࡫࡭࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡷࡩࡲࡄࠧࡧ"),re.DOTALL).findall(link)
        count=str(len(match))
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡧࡴࡻ࡮ࡵࠩࡨ"),count)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧࡶࠨࡩ"),l11l1lUK_Turk_No1 (u"ࠬࡴ࡯ࠨࡪ"))
        for item in match:
                try:
                        if l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡲࡲࡶࡹࡹࡤࡦࡸ࡬ࡰࡃ࠭࡫") in item: l11111llUK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽࡫ࡳࡸࡻࡄࠧ࡬")in item: l11l11llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠨ࠾ࡌࡱࡦ࡭ࡥ࠿ࠩ࡭")in item: l11l1l11lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸࡪࡾࡴ࠿ࠩ࡮")in item: l1llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡩࡲࡢࡲࡨࡶࡃ࠭࡯") in item: l11l11lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠫࡁࡸࡥࡥ࡫ࡵࡩࡨࡺ࠾ࠨࡰ") in item: l111l1l11UK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠬࡂ࡯࡬ࡶ࡬ࡸࡱ࡫࠾ࠨࡱ") in item: OK(item)
                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡥ࡮ࡁࠫࡲ") in item: l111llllUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡦࡶࡦࡶࡥࡳࡀࠪࡳ") in item: l11l11lUK_Turk_No1(item)
                        else:l11l1UK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                except:pass
def apkInstaller(apk, url):
	ADDONTITLE=l11l1lUK_Turk_No1 (u"ࠨࡄࡵࡳࡼࡹࡥࡳࠢࡵࡩࡶࡻࡩࡳࡧࡧࠫࡴ")
	l1l1l111UK_Turk_No1.log(apk)
	l1l1l111UK_Turk_No1.log(url)
	if l1l1l111UK_Turk_No1.platform() == l11l1lUK_Turk_No1 (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪࡵ"):
		yes = DIALOG.yesno(ADDONTITLE, l11l1lUK_Turk_No1 (u"࡛ࠥࡴࡻ࡬ࡥࠢࡼࡳࡺࠦ࡬ࡪ࡭ࡨࠤࡹࡵࠠࡥࡱࡺࡲࡱࡵࡡࡥࠢࡤࡲࡩࠦࡩ࡯ࡵࡷࡥࡱࡲ࠺ࠣࡶ"), apk, yeslabel=l11l1lUK_Turk_No1 (u"ࠦࡉࡵࡷ࡯࡮ࡲࡥࡩࠨࡷ"), nolabel=l11l1lUK_Turk_No1 (u"ࠧࡉࡡ࡯ࡥࡨࡰࠧࡸ"))
		if not yes: l1l1l111UK_Turk_No1.LogNotify(ADDONTITLE, l11l1lUK_Turk_No1 (u"࠭ࡅࡓࡔࡒࡖ࠿ࠦࡉ࡯ࡵࡷࡥࡱࡲࠠࡄࡣࡱࡧࡪࡲ࡬ࡦࡦࠪࡹ")); return
		display = apk
		if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
		if not l1l1l111UK_Turk_No1.workingURL(url) == True: l1l1l111UK_Turk_No1.LogNotify(ADDONTITLE, l11l1lUK_Turk_No1 (u"ࠧࡂࡒࡎࠤࡎࡴࡳࡵࡣ࡯ࡰࡪࡸ࠺ࠡࡋࡱࡺࡦࡲࡩࡥࠢࡄࡴࡰࠦࡕࡳ࡮ࠤࠫࡺ") % COLOR2); return
		DP.create(l11l1lUK_Turk_No1 (u"ࠨࡅ࡫ࡶࡴࡳࡥࠨࡻ"),l11l1lUK_Turk_No1 (u"ࠩ࡞ࡆࡢࡊ࡯ࡸࡰ࡯ࡳࡦࡪࡩ࡯ࡩ࠽࡟࠴ࡈ࡝ࠡࡅ࡫ࡶࡴࡳࡥࠨࡼ"),l11l1lUK_Turk_No1 (u"ࠪࠫࡽ"), l11l1lUK_Turk_No1 (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡜ࡧࡩࡵࠩࡾ"))
		lib=os.path.join(PACKAGES, l11l1lUK_Turk_No1 (u"ࠧࠫࡳ࠯ࡣࡳ࡯ࠧࡿ") % apk.replace(l11l1lUK_Turk_No1 (u"࠭࡜࡝ࠩࢀ"), l11l1lUK_Turk_No1 (u"ࠧࠨࢁ")).replace(l11l1lUK_Turk_No1 (u"ࠨ࠱ࠪࢂ"), l11l1lUK_Turk_No1 (u"ࠩࠪࢃ")).replace(l11l1lUK_Turk_No1 (u"ࠪ࠾ࠬࢄ"), l11l1lUK_Turk_No1 (u"ࠫࠬࢅ")).replace(l11l1lUK_Turk_No1 (u"ࠬ࠰ࠧࢆ"), l11l1lUK_Turk_No1 (u"࠭ࠧࢇ")).replace(l11l1lUK_Turk_No1 (u"ࠧࡀࠩ࢈"), l11l1lUK_Turk_No1 (u"ࠨࠩࢉ")).replace(l11l1lUK_Turk_No1 (u"ࠩࠥࠫࢊ"), l11l1lUK_Turk_No1 (u"ࠪࠫࢋ")).replace(l11l1lUK_Turk_No1 (u"ࠫࡁ࠭ࢌ"), l11l1lUK_Turk_No1 (u"ࠬ࠭ࢍ")).replace(l11l1lUK_Turk_No1 (u"࠭࠾ࠨࢎ"), l11l1lUK_Turk_No1 (u"ࠧࠨ࢏")).replace(l11l1lUK_Turk_No1 (u"ࠨࡾࠪ࢐"), l11l1lUK_Turk_No1 (u"ࠩࠪ࢑")))
		try: os.remove(lib)
		except: pass
		l1l11lUK_Turk_No1.download(url, lib, DP)
		xbmc.sleep(100)
		DP.close()
		notify.apkInstaller(apk)
		l1l1l111UK_Turk_No1.ebi(l11l1lUK_Turk_No1 (u"ࠪࡗࡹࡧࡲࡵࡃࡱࡨࡷࡵࡩࡥࡃࡦࡸ࡮ࡼࡩࡵࡻࠫࠦࠧ࠲ࠢࡢࡰࡧࡶࡴ࡯ࡤ࠯࡫ࡱࡸࡪࡴࡴ࠯ࡣࡦࡸ࡮ࡵ࡮࠯ࡘࡌࡉ࡜ࠨࠬࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡶ࡯ࡦ࠱ࡥࡳࡪࡲࡰ࡫ࡧ࠲ࡵࡧࡣ࡬ࡣࡪࡩ࠲ࡧࡲࡤࡪ࡬ࡺࡪࠨࠬࠣࡨ࡬ࡰࡪࡀࠧ࢒")+lib+l11l1lUK_Turk_No1 (u"ࠫࠧ࠯ࠧ࢓"))
	else: l1l1l111UK_Turk_No1.LogNotify(ADDONTITLE, l11l1lUK_Turk_No1 (u"ࠬࡋࡒࡓࡑࡕ࠾ࠥࡔ࡯࡯ࡧࠣࡅࡳࡪࡲࡰ࡫ࡧࠤࡉ࡫ࡶࡪࡥࡨࠫ࢔"))
def l1ll1ll11UK_Turk_No1():
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡸࠪ࢕"),l11l1lUK_Turk_No1 (u"ࠧ࡯ࡱࠪ࢖"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡐࡨࡻࠥࡋࡰࡪࡵࡲࡨࡪࡹࠠࡰࡨࠣࡘ࡛ࠦࡓࡩࡱࡺࡷࠬࢗ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡻࡦࡺࡣࡩࡵࡨࡶ࡮࡫ࡳ࠮ࡱࡱࡰ࡮ࡴࡥ࠯ࡤࡨ࠳ࡱࡧࡳࡵ࠯࠶࠹࠵࠳ࡥࡱ࡫ࡶࡳࡩ࡫ࡳࠨ࢘"),23,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡥࡩࡪ࡯࡯ࡥ࡯ࡳࡺࡪ࠮ࡰࡴࡪ࠳ࡺࡱࡴࡶࡴ࡮࠳࡚ࡑࡔࡶࡴ࡮࠳ࡹࡼࠥ࠳࠲ࡶ࡬ࡴࡽࡳ࠰ࡗ࡮ࠤࡹࡻࡲ࡬ࠢࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡸࠦ࡮ࡦࡹࠣࡩࡵ࡯ࡳࡰࡦࡨࡷࠥࡺࡶࠡࡵ࡫ࡳࡼࡹ࠱࠯࡬ࡳ࡫࢙ࠬ"),fanart,description=l11l1lUK_Turk_No1 (u"࢚ࠫࠬ"))
def l1l1ll1llUK_Turk_No1(url):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷ࢛ࠩ"),l11l1lUK_Turk_No1 (u"࠭࡮ࡰࠩ࢜"))
        l111lUK_Turk_No1=l111l11l1UK_Turk_No1.l1ll11lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧ࢝")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
                l1111111UK_Turk_No1(name,url,24,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩ࢞"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠯ࠧ࢟"))
def l1l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡼࠧࢠ"),l11l1lUK_Turk_No1 (u"ࠫࡳࡵࠧࢡ"))
        l1l111UK_Turk_No1=[l11l1lUK_Turk_No1 (u"ࠬࡹࡴࡳࡧࡤࡱࡦࡴࡧࡰ࠰ࡦࡳࡲ࠭ࢢ"),l11l1lUK_Turk_No1 (u"࠭ࡶࡪࡦࡷࡳ࠳ࡳࡥࠨࢣ"),l11l1lUK_Turk_No1 (u"ࠧࡨࡱࡵ࡭ࡱࡲࡡࡷ࡫ࡧ࠲࡮ࡴࠧࢤ"),l11l1lUK_Turk_No1 (u"ࠨࡸ࡬ࡨࡿ࡯࠮ࡵࡸࠪࢥ"),l11l1lUK_Turk_No1 (u"ࠩࡵࡥࡵ࡯ࡤࡷ࡫ࡧࡩࡴ࠴ࡷࡴࠩࢦ")]
        count=[]
        l11llll1lUK_Turk_No1=[]
        l1l11ll1lUK_Turk_No1=l111l11l1UK_Turk_No1.l111l1l1UK_Turk_No1(url)
        i=1
        for link in l1l11ll1lUK_Turk_No1:
                if urlresolver.HostedMediaFile(link).valid_url():
                        for l11lll111UK_Turk_No1 in l1l111UK_Turk_No1:
                                if l11lll111UK_Turk_No1 in link:
                                        count.append(l11l1lUK_Turk_No1 (u"ࠪࡐ࡮ࡴ࡫ࠡࠩࢧ")+str(i))
                                        l11llll1lUK_Turk_No1.append(link)
                                        i=i+1
        dialog = xbmcgui.Dialog()
        select = dialog.select(l11l1lUK_Turk_No1 (u"ࠫࡈ࡮࡯ࡰࡵࡨࠤࡦࠦ࡬ࡪࡰ࡮࠲࠳࠭ࢨ"),count)
        if select < 0:quit()
        url = l11llll1lUK_Turk_No1[select]
	l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1ll111l1UK_Turk_No1():
     l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡑࡱࡳࡹࡱࡧࡲࠡࡅࡤࡶࡹࡵ࡯࡯ࡵ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠨࢩ"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱ࠲࡫ࡪࡴࡲࡦ࠱ࡤࡲ࡮ࡳࡡࡵ࡫ࡲࡲࡄࡹ࡯ࡳࡶࡀࡺ࡮࡫ࡷࡴࠨ࡮ࡩࡾࡽ࡯ࡳࡦࡀࠪࡹࡼ࠽ࠨࢪ"),27,l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫࠱࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡌࡆࡆࡰࡴ࠾ࡽ࠮࡫ࡲࡪࠫࢫ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩࢬ"))
def l11ll11l1UK_Turk_No1():
    l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡻ࠭ࢭ"),l11l1lUK_Turk_No1 (u"ࠪࡲࡴ࠭ࢮ"))
    l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡕࡵࡰࡶ࡮ࡤࡶ࡚ࠥࡖࠡࡕ࡫ࡳࡼࡹࠧࢯ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡪࡳࡼࡧࡴࡤࡪࡩࡶࡪ࡫࡭ࡰࡸ࡬ࡩࡸ࠴ࡴࡰ࠱ࡂࡷࡴࡸࡴ࠾ࡸ࡬ࡩࡼࡹࠦ࡬ࡧࡼࡻࡴࡸࡤ࠾ࠨࡷࡺࡂ࠭ࢰ"),27,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࡍࡽ࡮ࡴࡵࡇ࡝࠲࡯ࡶࡧࠨࢱ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨࢲ"))
    l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡐࡨࡻ࡚ࠥࡖࠡࡕ࡫ࡳࡼࡹࠧࢳ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡧࡰࡹࡤࡸࡨ࡮ࡦࡳࡧࡨࡱࡴࡼࡩࡦࡵ࠱ࡸࡴ࠵࠿ࡴࡱࡵࡸࡂࡸࡥ࡭ࡧࡤࡷࡪࠬ࡫ࡦࡻࡺࡳࡷࡪ࠽ࠧࡶࡹࡁࠬࢴ"),27,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࡪࡓࡴࡕࡉ࠷ࡴ࠯࡬ࡳ࡫ࠬࢵ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬࢶ"))
def l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩࢷ"),l11l1lUK_Turk_No1 (u"࠭࡮ࡰࠩࢸ"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢ࡙ࡅࡂࡔࡆࡌࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࢹ"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡭࡯ࡸࡣࡷࡧ࡭࡬ࡲࡦࡧࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳ࠴ࡅ࡫ࡦࡻࡺࡳࡷࡪ࠽ࠨࢺ"),35,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࡥࡤ࠸ࡘࡾ࠸ࡱ࠰࡭ࡴ࡬࠭ࢻ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫࢼ"))
        l111lUK_Turk_No1=l1l1111UK_Turk_No1.l1ll11lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂ࠭࠴ࠫࡀࠫ࠿ࡷࡪࡶ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧࢽ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1l11111UK_Turk_No1(name,url,28,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭ࢾ"))
        try:
                l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡯ࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡱࡴࡃ࠭ࢿ")).findall(str(l111lUK_Turk_No1))[0]
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡓ࡫ࡸࡵࠢࡓࡥ࡬࡫ࠠ࠿ࡀࡁ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࣀ"),l11l11l11UK_Turk_No1,27,l11ll1l1lUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩࣁ"))
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨࣂ"))
def l11ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡼࠧࣃ"),l11l1lUK_Turk_No1 (u"ࠫࡳࡵࠧࣄ"))
        l111lUK_Turk_No1=l1l1111UK_Turk_No1.l1ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡦࡰࡧࡂࠬࣅ")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
                l1l11111UK_Turk_No1(name,url,29,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧࣆ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠭ࠬࣇ"))
def l1ll1llllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬࣈ"),l11l1lUK_Turk_No1 (u"ࠩࡱࡳࠬࣉ"))
        l111lUK_Turk_No1=l1l1111UK_Turk_No1.l11lll1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡺࡡࡳࡶࡁࠬ࠳࠱࠿ࠪ࠾ࡶࡩࡵࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡧࡱࡨࡃ࠭࣊")).findall(str(l111lUK_Turk_No1))
        for l1l1llllUK_Turk_No1,l1l111llUK_Turk_No1,url in match:
                l1111111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡊࡶࡩࡴࡱࡧࡩࠥࠫࡳࠨ࣋")%l1l1llllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠬ࠳ࠠࠦࡵࠪ࣌")%l1l111llUK_Turk_No1,url,30,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ࣍"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠭ࠬ࣎"))
def l1lll1l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺ࣏ࠬ"),l11l1lUK_Turk_No1 (u"ࠩࡱࡳ࣐ࠬ"))
        link=l1llll111UK_Turk_No1(url)
        l111l1llUK_Turk_No1=[]
        l1111lllUK_Turk_No1=[]
        l11l11l1UK_Turk_No1=[]
        l1l111UK_Turk_No1=[l11l1lUK_Turk_No1 (u"ࠪࡷࡹࡸࡥࡢ࡯ࡤࡲ࡬ࡵ࠮ࡤࡱࡰ࣑ࠫ"),l11l1lUK_Turk_No1 (u"ࠫࡻ࡯ࡤࡵࡱ࠱ࡱࡪ࣒࠭"),l11l1lUK_Turk_No1 (u"ࠬ࡭࡯ࡳ࡫࡯ࡰࡦࡼࡩࡥ࠰࡬ࡲ࣓ࠬ"),l11l1lUK_Turk_No1 (u"࠭ࡶࡪࡦࡽ࡭࠳ࡺࡶࠨࣔ"),l11l1lUK_Turk_No1 (u"ࠧࡳࡣࡳ࡭ࡩࡼࡩࡥࡧࡲ࠲ࡼࡹࠧࣕ")]
        l11llll1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡶࡪࡲ࠽ࠣࡰࡲࡪࡴࡲ࡬ࡰࡹࠥࠤࡹ࡯ࡴ࡭ࡧࡀࠦ࠳࠱࠿ࠣࠢࡲࡲࡨࡲࡩࡤ࡭ࡀࠦ࠳࠱࠿ࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࡉ࡯ࡲࡦࡥࡷࠤࡑ࡯࡮࡬࠾࠲ࡥࡃ࠭ࣖ"),re.DOTALL).findall(link)
        i=1
        for l1lll1l1UK_Turk_No1 in l11llll1lUK_Turk_No1:
            l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠩ࠲࡫ࡴ࠴ࡰࡩࡲࡂ࡫ࡹ࡬࡯࠾ࠩࣗ"),l11l1lUK_Turk_No1 (u"ࠪࠫࣘ"))
            l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠫࠫࡺࡩࡵ࡮ࡨࡁࠬࣙ"))[0]
            if not l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧࣚ") in l1lll1l1UK_Turk_No1:
                l1lll1l1UK_Turk_No1=base64.b64decode(l1lll1l1UK_Turk_No1)
                l11l11lllUK_Turk_No1=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"࠭ࡳࡵࡴࡨࡥࡲࡧ࡮ࡨࡱࠪࣛ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠧࡷ࡫ࡧࡸࡴ࠭ࣜ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠨࡩࡲࡶ࡮ࡲ࡬ࡢࡸ࡬ࡨࠬࣝ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠩࡹ࡭ࡩࢀࡩࠨࣞ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠪࡳࡵ࡫࡮࡭ࡱࡤࡨࠬࣟ") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠫࡪࡹࡴࡳࡧࡤࡱࠬ࣠") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠬࡴ࡯ࡸࡸ࡬ࡨࡪࡵࠧ࣡") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"࠭ࡲࡢࡲ࡬ࡨࡻ࡯ࡤࡦࡱࠪ࣢") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠧࡍ࡫ࡱ࡯ࣣࠥ࠭")+str(i))
                    i=i+1
        dialog = xbmcgui.Dialog()
        select = dialog.select(name,l1111lllUK_Turk_No1)
        if select < 0:quit()
        else:
            url=l111l1llUK_Turk_No1[select]
            l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1111ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡩࡵࡧࡰࠦࡃࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠࡵ࡫ࡷࡰࡪࡃࠢ࠯࠭ࡂࠦࡃ࠴ࠫࡀ࠾࡬ࡱ࡬ࠦࡳࡳࡥࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡧࡵࡲࡥࡧࡵࡁࠧ࠴ࠫࡀࠤࠣࡻ࡮ࡪࡴࡩ࠿ࠥ࠲࠰ࡅࠢࠡࡪࡨ࡭࡬࡮ࡴ࠾ࠤ࠱࠯ࡄࠨࠠࡢ࡮ࡷࡁࠧ࡝ࡡࡵࡥ࡫ࠤ࠭࠴ࠫࡀࠫࠥࡂࡁ࠵ࡡ࠿࠾࠲ࡨ࡮ࡼ࠾ࠨࣤ"),re.DOTALL).findall(link)
        for url,l1l11l11UK_Turk_No1,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡧࡰࡹࡤࡸࡨ࡮ࡦࡳࡧࡨࡱࡴࡼࡩࡦࡵ࠱ࡸࡴ࠭ࣥ")+url
            l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻ࣦࠩ")+l1l11l11UK_Turk_No1
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠳࠺࠽ࠥࣧ"),l11l1lUK_Turk_No1 (u"ࠧ࠭ࠢࣨ")).replace(l11l1lUK_Turk_No1 (u"࠭ࠦࡢ࡯ࡳ࠿ࣩࠬ"),l11l1lUK_Turk_No1 (u"ࠧࠡࠨࠣࠫ࣪"))
            if l11l1lUK_Turk_No1 (u"ࠨࡶࡹ࠱ࡸ࡮࡯ࡸࠩ࣫") in url:
                l1l11111UK_Turk_No1(name,url,28,l1l11l11UK_Turk_No1,fanart)
def l11ll11lUK_Turk_No1(url):
    string =l11l1lUK_Turk_No1 (u"ࠩࠪ࣬")
    keyboard = xbmc.Keyboard(string, l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡈࡲࡹ࡫ࡲࠡࡕࡨࡥࡷࡩࡨࠡࡖࡨࡶࡲࡡ࠯ࡄࡑࡏࡓࡗࡣ࣭ࠧ"))
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(l11l1lUK_Turk_No1 (u"࣮ࠫࠥ࠭"),l11l1lUK_Turk_No1 (u"ࠬ࠱࣯ࠧ"))
        if len(string)>1:
            url = l11l1lUK_Turk_No1 (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱ࠲ࡃࡰ࡫ࡹࡸࡱࡵࡨࡂࠨࣰ") + string
            l1111ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        else: quit()
def l11llll1UK_Turk_No1():
        url = l11l1lUK_Turk_No1 (u"ࠧ࠱ࣱࠩ")
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࠪࠫࠬ࠭ࠤ࡞࡫ࡲ࡭࡫ࠣ࡝ࡪࡴࡩࠡࡇ࡮ࡰࡪࡴࡥ࡯࡮ࡨࡶࠥࡊࡩࡻ࡫࡯ࡩࡷࠦ࠱ࠡࠬ࠭࠮࠯ࡡ࠯ࡄࡑࡏࡓࡗࡣࣲࠧ"),url,25,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡳࡔࡵࡲࡺ࡬ࡑ࠮࡫ࡲࡪࠫࣳ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫࣴ"))
def l1ll1l11lUK_Turk_No1(url):
        l111lUK_Turk_No1=l11l1111UK_Turk_No1.l1ll11lUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂ࠭࠴ࠫࡀࠫ࠿ࡷࡪࡶ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧࣵ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,26,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࣶࠬ࠭"))
        try:
                l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡯ࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡱࡴࡃ࠭ࣷ")).findall(str(l111lUK_Turk_No1))[0]
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡓ࡫ࡸࡵࠢࡓࡥ࡬࡫ࠠ࠿ࡀࡁ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࣸ"),l11l11l11UK_Turk_No1,25,l11ll1l1lUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࣹࠩ"))
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠯ࣺࠧ"))
def l11lllll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lll11UK_Turk_No1=l11l1111UK_Turk_No1.l11ll1ll1UK_Turk_No1(url)
        l111lll11UK_Turk_No1 = l111lll11UK_Turk_No1[1:]
        l1l11lllUK_Turk_No1=len(l111lll11UK_Turk_No1)
        if l1l11lllUK_Turk_No1 > 1:
                count=[]
                i=1
                for part in l111lll11UK_Turk_No1:
                        count.append(l11l1lUK_Turk_No1 (u"ࠪࡔࡦࡸࡴࠡࠩࣻ")+str(i))
                        i=i+1
                        dialog = xbmcgui.Dialog()
                select = dialog.select(l11l1lUK_Turk_No1 (u"ࠫࡈ࡮࡯ࡰࡵࡨࠤࡦࠦࡐࡢࡴࡷ࠲࠳࠭ࣼ"),count)
                if select < 0:quit()
                url = l111lll11UK_Turk_No1[select]
	l1llll1llUK_Turk_No1=l11l1111UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1llUK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def l1lll1ll1UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠ࠮࠯࠰࡛ࠪࠡࡨࡶࡱ࡯࡚ࠠࡧࡱ࡭ࠥࡋ࡫࡭ࡧࡱࡩࡳࡲࡥࡳࠢࡇ࡭ࡿ࡯࡬ࡦࡴࠣ࠶ࠥ࠰ࠪࠫࠬ࡞࠳ࡈࡕࡌࡐࡔࡠࠫࣽ"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱ࡧࡦࡴ࡬ࡪࡦ࡬ࡾ࡮࡮ࡤ࠷࠰ࡦࡳࡲ࠵ࠧࣾ"),36,l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࡸ࡙ࡳࡰࡸࡪࡏ࠳ࡰࡰࡨࠩࣿ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩऀ"))
def l11ll11llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l1l11l1l1UK_Turk_No1.l1ll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠫ࠲࠰ࡅࠩ࠽ࡵࡨࡴࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡦࡰࡧࡂࠬँ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,37,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫं"))
        try:
                l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠪ࠱࠯ࡄ࠯࠼࡯ࡲࡁࠫः")).findall(str(l111lUK_Turk_No1))[0]
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟ࡑࡩࡽࡺࠠࡑࡣࡪࡩࠥࡄ࠾࠿࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪऄ"),l11l11l11UK_Turk_No1,36,l11ll1l1lUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧअ"))
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠭ࠬआ"))
def l1ll111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lll11UK_Turk_No1=l1l11l1l1UK_Turk_No1.l11ll1ll1UK_Turk_No1(url)
        l1l11lllUK_Turk_No1=len(l111lll11UK_Turk_No1)
        if l1l11lllUK_Turk_No1 > 1:
                count=[]
                i=1
                for part in l111lll11UK_Turk_No1:
                        count.append(l11l1lUK_Turk_No1 (u"ࠨࡒࡤࡶࡹࠦࠧइ")+str(i))
                        i=i+1
                        dialog = xbmcgui.Dialog()
                select = dialog.select(l11l1lUK_Turk_No1 (u"ࠩࡆ࡬ࡴࡵࡳࡦࠢࡤࠤࡕࡧࡲࡵ࠰࠱ࠫई"),count)
                if select < 0:quit()
                url = l111lll11UK_Turk_No1[select]
	l1llll1llUK_Turk_No1=l1l11l1l1UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1llUK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def l1l11llllUK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࠬ࠭࠮࠯ࠦࡔࡓࡖࠣ࡝ࡪࡸ࡬ࡪࠢ࡜ࡩࡳ࡯ࠠࡆ࡭࡯ࡩࡳ࡫࡮࡭ࡧࡵࠤࡉ࡯ࡺࡪ࡮ࡨࡶࠥ࠰ࠪࠫࠬ࡞࠳ࡈࡕࡌࡐࡔࡠࠫउ"),url,45,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࠮ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࡥ࡯࠸ࡱࡘ࡫ࡰ࠲࡯ࡶࡧࠨऊ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭ऋ"))
def l1ll1lUK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࡉࡏ࡚ࡊ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪऌ"),l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡺࡲࡵ࠰ࡷࡺ࠴࠸࠯ࡥ࡫ࡽ࡭ࡱ࡫ࡲࠨऍ"),21,l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡬࠲࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࡪࡒ࡜ࡸࡊࡽ࠳࠯࡬ࡳ࡫ࠬऎ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪए"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࡒࡕࡓࡌࡘࡁࡎ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪऐ"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡽࡷࡸ࠰ࡷࡶࡹ࠴ࡴࡷ࠱࠵࠴࠶࠺࠹࠰ࡲࡵࡳ࡬ࡸࡡ࡮࡮ࡤࡶࠬऑ"),21,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࠯࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳࠹࡛ࡱࡖࡗࡌ࡫࠳ࡰࡰࡨࠩऒ"),fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧओ"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࡈࡅࡍࡉࡈࡗࡊࡒ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨऔ"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡴࡳࡶ࠱ࡸࡻ࠵࠲࠱࠳࠸࠷࠴ࡨࡥ࡭ࡩࡨࡷࡪࡲࠧक"),21,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࡊࡈࡍ࠽ࡉࡴࡵ࠰࡭ࡴ࡬࠭ख"),fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫग"))
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤ࡬ࡵ࡬ࡥ࡟ࡆࡓࡈ࡛ࡋ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩघ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡸࡷࡺ࠮ࡵࡸ࠲࠶࠵࠷࠵࠸࠱ࡦࡳࡨࡻ࡫ࠨङ"),21,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࠰࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴ࡠࡗ࠶ࡧࡒ࡫ࡱ࠴ࡪࡱࡩࠪच"),fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨछ"))
def l1ll1111UK_Turk_No1(url):
        l111lUK_Turk_No1=l111111UK_Turk_No1.l11l1lll1UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ࠪ࠱࠯ࡄ࠯࠼ࡴࡧࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡷࡪࡶ࠾ࠩ࠰࠮ࡃ࠮ࡂࡥ࡯ࡦࡁࠫज")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
            l1111111UK_Turk_No1(name,url,22,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪझ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠪࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶࠰ࠪࠩञ"))
def l1111l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l11l11l1lUK_Turk_No1=[]
        l1l111llUK_Turk_No1=[]
        l1l1l111lUK_Turk_No1=[]
        link=l1llll111UK_Turk_No1(url)
        l1l11ll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤ࡬ࡸࡪࡳ࡟ࡩࡧ࡬࡫࡭ࡺࠠࡤࡱ࡯࠱ࡱ࡭࠭࠳ࠢࡦࡳࡱ࠳࡭ࡥ࠯࠵ࠤࡨࡵ࡬࠮ࡵࡰ࠱࠸ࠦࡣࡰ࡮࠰ࡼࡸ࠳࠴ࠡࡥࡲࡰ࠲ࡾࡸࡴ࠯࠹ࠦࠥࡺࡩࡵ࡮ࡨࡁࠧࠨ࠾࠯࠭ࡂࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࡃ࠴ࠫࡀ࠾࡬ࡱ࡬ࠦࡳࡳࡥࡀࠦ࠳࠱࠿ࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡳࡰࡦࡿࠢࠡࡣ࡯ࡸࡂࠨࡩࡻ࡮ࡨࠦࠥ࠵࠾࠯࠭ࡂࡀ࡮ࡳࡧࠡࡵࡵࡧࡂࠨࠨ࠯࠭ࡂ࠭ࡄࡼ࠽࠯࠭ࡂࠦࠥࡧ࡬ࡵ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡧࡱࡧࡳࡴ࠿ࠥ࡭ࡲ࡭࠭ࡳࡧࡶࡴࡴࡴࡳࡪࡸࡨࠤ࡭ࡧࡳࡠࡶࡲࡳࡱࡺࡩࡱࠤࠣ࠳ࡃ࠭ट"),re.DOTALL).findall(link)
        for url,l1l11l11UK_Turk_No1,name in l1l11ll11UK_Turk_No1:
            url=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡷࡸࡹ࠱ࡸࡷࡺ࠮ࡵࡸࠪठ")+url
            name=name.replace(l11l1lUK_Turk_No1 (u"࠭ࠦࡲࡷࡲࡸࡀ࠭ड"),l11l1lUK_Turk_No1 (u"ࠧࠣࠩढ")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠸࠷࠻ࠣण"),l11l1lUK_Turk_No1 (u"ࠤࡦࠦत")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠷࠹࠺࠽ࠥथ"),l11l1lUK_Turk_No1 (u"ࠦࡈࠨद")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠷࠵࠿ࠧध"),l11l1lUK_Turk_No1 (u"ࠨࡵࠣन")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠶࠵ࡁࠢऩ"),l11l1lUK_Turk_No1 (u"ࠣࡗࠥप")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠷࠷࠴࠼ࠤफ"),l11l1lUK_Turk_No1 (u"ࠥࡓࠧब")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠵࠸࠾ࠦभ"),l11l1lUK_Turk_No1 (u"ࠧࡵࠢम")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠵࠼࠿ࠧय"),l11l1lUK_Turk_No1 (u"ࠢࠨࠤर"))
            l1l111llUK_Turk_No1.append(name)
            l11l11l1lUK_Turk_No1.append(url)
        dialog = xbmcgui.Dialog()
        select = dialog.select(l11l1lUK_Turk_No1 (u"ࠨࡄࡲࡰࡺࡳ࡬ࡦࡴࠪऱ"),l1l111llUK_Turk_No1)
        if select < 0:quit()
	l1llll1llUK_Turk_No1=l111111UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1llUK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def KD():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡪࡳࡱࡪ࡝ࠫࠬ࠭࠮ࠥࡑࡁࡏࡃࡏࠤࡉ࡙ࠦࡦࡴ࡯࡭ࠥ࡟ࡥ࡯࡫ࠣࡉࡰࡲࡥ࡯ࡧࡱࡰࡪࡸࠠࡅ࡫ࡽ࡭ࡱ࡫ࡲࠡࠬ࠭࠮࠯ࡡ࠯ࡄࡑࡏࡓࡗࡣࠧल"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡩࡳ࡭ࡥ࡭ࡵ࡬ࡾ࠳ࡱࡡ࡯ࡣ࡯ࡨ࠳ࡩ࡯࡮࠰ࡷࡶ࠴࠭ळ"),46,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࠮ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࡨࡾ࡞ࡴࡪࡕࡲ࠲࡯ࡶࡧࠨऴ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭व"))
def l11llllUK_Turk_No1(url):
        l111lUK_Turk_No1=l1111UK_Turk_No1.l11l1lll1UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡵࡨࡴࡃ࠮࠮ࠬࡁࠬࡀࡪࡴࡤ࠿ࠩश")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
            l1111111UK_Turk_No1(name,url,47,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨष"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠴࠵࠯ࠧस"))
def l11llll11UK_Turk_No1(name,url):
        l11l11l1lUK_Turk_No1=[]
        l1l111llUK_Turk_No1=[]
        link=l1llll111UK_Turk_No1(url)
        l1lll11llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢ࡭࡫ࡶࡸࠧࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡦ࡮ࡨࡧࡹࡄࠧह"),re.DOTALL).findall(link)[0]
        l1l11ll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡴࡶࡴࡪࡱࡱࠤࡻࡧ࡬ࡶࡧࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡵࡰࡵ࡫ࡲࡲࡃ࠭ऺ")).findall(l1lll11llUK_Turk_No1)
        for url,name in l1l11ll11UK_Turk_No1:
            url=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡪࡴࡧࡦ࡮ࡶ࡭ࡿ࠴࡫ࡢࡰࡤࡰࡩ࠴ࡣࡰ࡯࠱ࡸࡷ࠵ࡖࡪࡦࡨࡳ࠴ࡊࡥࡵࡣ࡬ࡰ࠴࠭ऻ")+url
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠬࠬࡱࡶࡱࡷ࠿़ࠬ"),l11l1lUK_Turk_No1 (u"࠭ࠢࠨऽ")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠷࠶ࡁࠢा"),l11l1lUK_Turk_No1 (u"ࠣࡥࠥि")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠶࠿࠹࠼ࠤी"),l11l1lUK_Turk_No1 (u"ࠥࡇࠧु")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠶࠴࠾ࠦू"),l11l1lUK_Turk_No1 (u"ࠧࡻࠢृ")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠴࠵࠴ࡀࠨॄ"),l11l1lUK_Turk_No1 (u"ࠢࡖࠤॅ")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠶࠺࠻ࠣॆ"),l11l1lUK_Turk_No1 (u"ࠤࡒࠦे")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠴࠷࠽ࠥै"),l11l1lUK_Turk_No1 (u"ࠦࡴࠨॉ")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠴࠻࠾ࠦॊ"),l11l1lUK_Turk_No1 (u"ࠨࠧࠣो"))
            l1l111llUK_Turk_No1.append(name)
            l11l11l1lUK_Turk_No1.append(url)
        dialog = xbmcgui.Dialog()
        select = dialog.select(l11l1lUK_Turk_No1 (u"ࠧࡃࡱ࡯ࡹࡲࡲࡥࡳࠩौ"),l1l111llUK_Turk_No1)
        if select < 0:quit()
	l1llll1llUK_Turk_No1=l1111UK_Turk_No1.l111l1l1UK_Turk_No1(url)
	l1ll1l1llUK_Turk_No1(name,l1llll1llUK_Turk_No1,l1l11l11UK_Turk_No1)
def l1l11l1llUK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࠪࠫࠬ࠭ࠤࡘࡎࡏࡘࡖ࡙ࠤ࡞࡫ࡲ࡭࡫ࠣ࡝ࡪࡴࡩࠡࡇ࡮ࡰࡪࡴࡥ࡯࡮ࡨࡶࠥࡊࡩࡻ࡫࡯ࡩࡷࠦࠪࠫࠬ࠭࡟࠴ࡉࡏࡍࡑࡕࡡ्ࠬ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡳࡩࡱࡺࡸࡺࡸ࡫࠯ࡥࡲࡱ࠳ࡺࡲ࠰ࡦ࡬ࡾ࡮ࡲࡥࡳ࠱ࡤࡶࡸ࡯ࡶࡥࡧ࡮࡭࠲ࡪࡩࡻ࡫࡯ࡩࡷ࠭ॎ"),48,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮࠴ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱࡬ࡲ࠽ࡴࡃࡃ࠻࠱࡮ࡵ࡭ࠧॏ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬॐ"))
def l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11lll1lUK_Turk_No1.l11l1llllUK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡴࡧࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡩࡳࡪ࠾ࠨ॑")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
            l1l11111UK_Turk_No1(name,url,49,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"॒࠭ࠧ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩ࠷࠳࠴࠮࠭॓"))
def l11l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11lll1lUK_Turk_No1.l11ll1l1UK_Turk_No1(name,url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ࠪ࠱࠯ࡄ࠯࠼ࡴࡧࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡩࡳࡪ࠾ࠨ॔")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
            l1l11111UK_Turk_No1(name,url,50,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪॕ"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠪࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡓࡦࡶ࡙࡭ࡪࡽࡍࡰࡦࡨࠬ࠺࠶ࠩࠨॖ"))
def l1llllll1UK_Turk_No1(url):
    parts=[]
    link=l1llll111UK_Turk_No1(url)
    parts.append(url)
    l1lll11llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡻ࡬ࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡸ࡬ࡨࡪࡵ࠭ࡱࡣࡵࡸ࠲ࡴࡵ࡮ࡤࡨࡶࠧࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡵ࡭ࡀࠪॗ"),re.DOTALL).findall(link)[0]
    l1l11ll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡢࡀ࠿࠳ࡱ࡯࠾ࠨक़")).findall(l1lll11llUK_Turk_No1)
    for page,name in l1l11ll11UK_Turk_No1:
        page=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱ࡷ࡭ࡵࡷࡵࡸ࠱ࡧࡴࡳ࠮ࡵࡴࠪख़")+page
        parts.append(page)
        l1111111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧࡑࡣࡵࡧࡦࠦࠥࡴࠩग़")%name,page,51,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩज़"))
def l11ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡱࡪࡺࡡࠡࡰࡤࡱࡪࡃࠢࡱࡱࡳࡧࡴࡸ࡮࠻ࡵࡷࡶࡪࡧ࡭ࠣࠢࡦࡳࡳࡺࡥ࡯ࡶࡀࠦ࠭࠴ࠫࡀࠫࠥࠤ࠴ࡄࠧड़"),re.DOTALL).findall(link)
        for url in match:
            l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1lll111lUK_Turk_No1():
    l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡷ࡫ࡥ࡯࡟࠰࠱࠲࠳࠭ࠡࡕࡳࡳࡷࡺࡳࠡࡊ࡬࡫࡭ࡲࡩࡨࡪࡷࡷࠥ࠳࠭࠮࠯࠰࡟࠴ࡉࡏࡍࡑࡕࡡࠬढ़"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡰࡪࡳࡱࡵࡳ࠯ࡥࡲࡱ࠴࠭फ़"),52,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࠯࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࡳ࡭ࡅࡧࡊ࡛࠷࠳ࡰࡰࡨࠩय़"),fanart)
def l1ll1l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l1l1l11llUK_Turk_No1.l1ll11l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡥࡱࡀࠫ࠲࠰ࡅࠩ࠽ࡧࡱࡨࡃ࠭ॠ")).findall(str(l111lUK_Turk_No1))
        for name,url in match:
            l1l11111UK_Turk_No1(name,url,53,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨॡ"))
def l1l1ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨ࡭ࡢࡶࡦ࡬ࠧࡄ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠾࡬ࡱ࡬ࠦࡳࡳࡥࡀࠦ࠳࠱࠿ࠣࠢ࠲ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡦࡄ࠼࠰ࡦ࡬ࡺࡃ࠭ॢ"),re.DOTALL).findall(link)
        for url,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴࡮ࡨࡱ࡯ࡳࡸ࠴ࡣࡰ࡯ࠪॣ")+url
            l1111111UK_Turk_No1(name,url,54,l1l11l11UK_Turk_No1,fanart)
        try:
            l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀ࠴ࡹࡰࡢࡰࡁࠤࡁࡧࠠࡤ࡮ࡤࡷࡸࡃࠢࡤࡰ࠰ࡴࡦ࡭ࡥ࠮ࡰࡨࡻࡸࠨࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠮ࠬࡁ࠿࠳ࡦࡄࠧ।"),re.DOTALL).findall(link)
            for l111lllllUK_Turk_No1 in l11l11l11UK_Turk_No1:
                url=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡰࡪࡳࡱࡵࡳ࠯ࡥࡲࡱࠬ॥")+l111lllllUK_Turk_No1
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟ࡑࡉ࡝࡚ࠠࡑࡃࡊࡉࠥࡄ࠾࠿࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ०"),url,53,l11ll1l1lUK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ१"))
        except:pass
def llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
            link=l1llll111UK_Turk_No1(url)
            l111l1llUK_Turk_No1=[]
            l1111lllUK_Turk_No1=[]
            l11l11l1UK_Turk_No1=[]
            match=re.compile(l11l1lUK_Turk_No1 (u"ࠧࡢࡦࡧࡸ࡭࡯ࡳࡠ࡫ࡱࡰ࡮ࡴࡥࡠࡵ࡫ࡥࡷ࡫࡟ࡵࡱࡲࡰࡧࡵࡸࠩ࠰࠮ࡃ࠮ࠫ࠲ࡇࡵࡷࡶࡴࡴࡧࠦ࠵ࡈࠩ࠷࠶ࠧ२"),re.DOTALL).findall(link)[0]
            l11llll1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨࡵࡵࡧࠪ࠹ࡄࠦ࠴࠵ࠬ࠳࠱࠿ࠪࠧ࠵࠶ࠬ३"),re.DOTALL).findall(match)
            i=1
            for l1lll1l1UK_Turk_No1 in l11llll1lUK_Turk_No1:
                l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠩࠨ࠷ࡆ࠭४"),l11l1lUK_Turk_No1 (u"ࠪ࠾ࠬ५")).replace(l11l1lUK_Turk_No1 (u"ࠫࠪ࠸ࡆࠨ६"),l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧ७"))
                l11l11lllUK_Turk_No1=l1lll1l1UK_Turk_No1
                domain=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"࠭࡯࡬࠰ࡵࡹࠬ८") in l1lll1l1UK_Turk_No1:
                    l1lll1l1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠭९")+l1lll1l1UK_Turk_No1
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠨࡊ࡬࡫࡭ࡲࡩࡨࡪࡷࡷࠬ॰"))
                elif l11l1lUK_Turk_No1 (u"ࠩࡶࡸࡷ࡫ࡡ࡮ࡣࡥࡰࡪ࠭ॱ") in l1lll1l1UK_Turk_No1:
                    l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠪ࠳ࡪ࠵ࠧॲ"),l11l1lUK_Turk_No1 (u"ࠫ࠴࠭ॳ"))
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠬࡎࡩࡨࡪ࡯࡭࡬࡮ࡴࡴࠩॴ"))
                elif l11l1lUK_Turk_No1 (u"࠭ࡩ࡮ࡩࡷࡧࠬॵ") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠧࡈࡱࡤࡰࡸ࠭ॶ"))
                elif l11l1lUK_Turk_No1 (u"ࠨ࡯࡬ࡼࡹࡧࡰࡦࠩॷ") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠩࡋ࡭࡬࡮࡬ࡪࡩ࡫ࡸࡸ࠭ॸ"))
                elif l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨࠫॹ") in l1lll1l1UK_Turk_No1:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠫࡍ࡯ࡧࡩ࡮࡬࡫࡭ࡺࡳࠨॺ"))
                else:
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(domain)
                i=i+1
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,l1111lllUK_Turk_No1)
            if select < 0:quit()
            else:
                url=l111l1llUK_Turk_No1[select]
                l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l111111l1UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭ࡲࡦࡧࡱࡡ࠲࠳࠭࠮࠯ࠣࡊࡴࡵࡴࡣࡣ࡯ࡰࠥࡎࡩࡨࡪ࡯࡭࡬࡮ࡴࡴࠢ࠰࠱࠲࠳࠭࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩॻ"),url,32,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲࠴ࡺ࡮ࡢ࠸ࡇࡅ࠲࡯ࡶࡧࠨॼ"),fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨॽ"))
def l111ll111UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨࡊ࡬࡫࡭ࡲࡩࡨࡪࡷࡷࠬॾ"),l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡦࡶ࡮࡯ࡱࡦࡺࡣࡩࡧࡶࡥࡳࡪࡳࡩࡱࡺࡷ࠳ࡩ࡯࡮࠱ࡦࡥࡹ࡫ࡧࡰࡴࡼ࠳࡭࡯ࡧࡩ࡮࡬࡫࡭ࡺࡳ࠰ࠩॿ"),33,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࡃࡲࡖࡘ࡬࠸ࡕ࠯࡬ࡳ࡫ࠬঀ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡲࡦࠢࡋ࡭࡬࡮࡬ࡪࡩ࡫ࡸࡸ࠭ঁ"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡩࡹࡱࡲ࡭ࡢࡶࡦ࡬ࡪࡹࡡ࡯ࡦࡶ࡬ࡴࡽࡳ࠯ࡥࡲࡱ࠴ࡩࡡࡵࡧࡪࡳࡷࡿ࠯ࡧࡷ࡯ࡰ࠲ࡳࡡࡵࡥ࡫࠳ࠬং"),33,l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡪ࠰࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴ࡉ࠹ࡻ࡛࠹ࡻࡹ࠴ࡪࡱࡩࠪঃ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧࡑࡴࡨࡱ࡮࡫ࡲࠡࡎࡨࡥ࡬ࡻࡥࠨ঄"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡬ࡵ࡭࡮ࡰࡥࡹࡩࡨࡦࡵࡤࡲࡩࡹࡨࡰࡹࡶ࠲ࡨࡵ࡭࠰ࡥࡤࡸࡪ࡭࡯ࡳࡻ࠲ࡴࡷ࡫࡭ࡪࡧࡵ࠱ࡱ࡫ࡡࡨࡷࡨ࠳ࠬঅ"),33,l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࡇࡅ࡯ࡩࡕ࡝ࡊ࠮࡫ࡲࡪࠫআ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠪࡉࡳ࡭࡬ࡢࡰࡧࠫই"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡨࡸࡰࡱࡳࡡࡵࡥ࡫ࡩࡸࡧ࡮ࡥࡵ࡫ࡳࡼࡹ࠮ࡤࡱࡰ࠳ࡨࡧࡴࡦࡩࡲࡶࡾ࠵ࡥ࡯ࡩ࡯ࡥࡳࡪ࠯ࠨঈ"),33,l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱ࡅࡶࡎ࡮࠷ࡃࡍ࠱࡮ࡵ࡭ࠧউ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࠭ࡓࡱࡣ࡬ࡲࠬঊ"),l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡸࡹࡺ࠲࡫ࡻ࡬࡭࡯ࡤࡸࡨ࡮ࡥࡴࡣࡱࡨࡸ࡮࡯ࡸࡵ࠱ࡧࡴࡳ࠯ࡤࡣࡷࡩ࡬ࡵࡲࡺ࠱ࡶࡴࡦ࡯࡮࠰ࠩঋ"),33,l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴ࡉࡪࡨ࡜࡝࡭࠾࠴ࡪࡱࡩࠪঌ"),fanart)
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩࡌࡸࡦࡲࡹࠨ঍"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡧࡷ࡯ࡰࡲࡧࡴࡤࡪࡨࡷࡦࡴࡤࡴࡪࡲࡻࡸ࠴ࡣࡰ࡯࠲ࡧࡦࡺࡥࡨࡱࡵࡽ࠴࡯ࡴࡢ࡮ࡼࠫ঎"),33,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࡊ࡭࠼ࡖ࡬ࡶ࡚࠰࡭ࡴ࡬࠭এ"),fanart)
def l1l1l1lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11ll1lUK_Turk_No1.l111lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠮࠮ࠬࡁࠬࡀࡸ࡫ࡰ࠿ࠪ࠱࠯ࡄ࠯࠼ࡴࡧࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡩࡳࡪ࠾ࠨঐ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,34,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ঑"))
        try:
            l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂ࠭࠴ࠫࡀࠫ࠿ࡲࡵࡄࠧ঒")).findall(str(l111lUK_Turk_No1))
            for url in l11l11l11UK_Turk_No1:
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡔࡥࡹࡶࠣࡔࡦ࡭ࡥࠡࡀࡁࡂࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ও"),url,mode,l11ll1l1lUK_Turk_No1,fanart)
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠩࡆࡳࡳࡺࡡࡪࡰࡨࡶ࠳࡙ࡥࡵࡘ࡬ࡩࡼࡓ࡯ࡥࡧࠫ࠹࠵࠶ࠩࠨঔ"))
def l1ll1111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
            link=l1llll111UK_Turk_No1(url)
            l111l1llUK_Turk_No1=[]
            l1111lllUK_Turk_No1=[]
            l11l11l1UK_Turk_No1=[]
            l11llll1lUK_Turk_No1=l11ll1lUK_Turk_No1.l1lll1l1lUK_Turk_No1(url)
            i=1
            for l1lll1l1UK_Turk_No1 in l11llll1lUK_Turk_No1:
                l11l11lllUK_Turk_No1=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠪࡳࡰ࠴ࡲࡶࠩক") in l1lll1l1UK_Turk_No1:
                    l1lll1l1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼ࠪখ")+l1lll1l1UK_Turk_No1
                    domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧগ"))[2].replace(l11l1lUK_Turk_No1 (u"࠭ࡷࡸࡹ࠱ࠫঘ"),l11l1lUK_Turk_No1 (u"ࠧࠨঙ"))
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠨࡎ࡬ࡲࡰࠦࠧচ")+str(i))
                else:
                    domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠩ࠲ࠫছ"))[2].replace(l11l1lUK_Turk_No1 (u"ࠪࡻࡼࡽ࠮ࠨজ"),l11l1lUK_Turk_No1 (u"ࠫࠬঝ"))
                    l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                    l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠬࡒࡩ࡯࡭ࠣࠫঞ")+str(i))
                i=i+1
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,l1111lllUK_Turk_No1)
            if select < 0:quit()
            else:
                url=l111l1llUK_Turk_No1[select]
                l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1l1111l1UK_Turk_No1():
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"࠭ࡁ࠮࡜ࠣࡑࡴࡼࡩࡦࡵࠪট"),l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰࡯ࡲࡺ࡮࡫࠴ࡶ࠰ࡦ࡬ࠬঠ"),39,l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡬࠲࡮ࡳࡧࡶࡴ࠱ࡧࡴࡳ࠯ࡕ࠹ࡽࡘ࠸ࡶࡉ࠯࡬ࡳ࡫ࠬড"),fanart)
def l1l1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡥࡰࡺ࡫࡝ࡔࡇࡄࡖࡈࡎࠠࡂ࠯࡝࡟࠴ࡉࡏࡍࡑࡕࡡࠬঢ"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡲࡵࡶࡪࡧ࠷ࡹ࠳ࡩࡨࠨণ"),42,l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴࡯࠮ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࡧࡦ࠺ࡓࡹ࠺ࡳ࠲࡯ࡶࡧࠨত"),fanart)
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂ࡬ࡪࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡧ࠾࠽࠱࡯࡭ࡃ࠭থ")).findall(link)
        for url,name in match:
            name=name.replace(l11l1lUK_Turk_No1 (u"࠭ࠣࠨদ"),l11l1lUK_Turk_No1 (u"ࠧ࠱࠯࠼ࠫধ"))
            if l11l1lUK_Turk_No1 (u"ࠨ࠱ࡂࡰࡪࡺࡴࡦࡴࡀࠫন") in url:
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠩ࡞ࡆࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠬ঩") %name,url,40,l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳࡮࠴ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱࠸ࡪ࡚ࡠࡵ࡬ࡨ࠱࡮ࡵ࡭ࠧপ"),fanart)
def l111llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l1l1lll1lUK_Turk_No1.l11ll1lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂ࠭࠴ࠫࡀࠫ࠿ࡷࡪࡶ࠾ࠩ࠰࠮ࡃ࠮ࡂࡳࡦࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡨࡲࡩࡄࠧফ")).findall(str(l111lUK_Turk_No1))
        for name,url,l1l11l11UK_Turk_No1 in match:
                l1111111UK_Turk_No1(name,url,41,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠬ࠭ব"))
        try:
            l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡯ࡲࡁࠬ࠳࠱࠿ࠪ࠾ࡱࡴࡃ࠮࠮ࠬࡁࠬࡀࡳࡶ࠾ࠨভ")).findall(str(l111lUK_Turk_No1))
            for l111ll1l1UK_Turk_No1,url in l11l11l11UK_Turk_No1:
                l1l11111UK_Turk_No1(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨম")%l111ll1l1UK_Turk_No1,url,40,l11ll1l1lUK_Turk_No1,fanart)
        except:pass
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡅࡲࡲࡹࡧࡩ࡯ࡧࡵ࠲ࡘ࡫ࡴࡗ࡫ࡨࡻࡒࡵࡤࡦࠪ࠸࠴࠵࠯ࠧয"))
def l111ll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
            link=l1llll111UK_Turk_No1(url)
            l111l1llUK_Turk_No1=[]
            l1111lllUK_Turk_No1=[]
            l11l11l1UK_Turk_No1=[]
            l11llll1lUK_Turk_No1=l1l1lll1lUK_Turk_No1.l111l1l1UK_Turk_No1(url)
            i=1
            for l1lll1l1UK_Turk_No1 in l11llll1lUK_Turk_No1:
                l11l11lllUK_Turk_No1=l1lll1l1UK_Turk_No1
                domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠩ࠲ࠫর"))[2].replace(l11l1lUK_Turk_No1 (u"ࠪࡻࡼࡽ࠮ࠨ঱"),l11l1lUK_Turk_No1 (u"ࠫࠬল"))
                l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠬࡒࡩ࡯࡭ࠣࠫ঳")+str(i))
                i=i+1
            dialog = xbmcgui.Dialog()
            select = dialog.select(name,l1111lllUK_Turk_No1)
            if select < 0:quit()
            else:
                url=l111l1llUK_Turk_No1[select]
                l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    string =l11l1lUK_Turk_No1 (u"࠭ࠧ঴")
    keyboard = xbmc.Keyboard(string, l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡅ࡯ࡶࡨࡶ࡙ࠥࡥࡢࡴࡦ࡬࡚ࠥࡥࡳ࡯࡞࠳ࡈࡕࡌࡐࡔࡠࠫ঵"))
    keyboard.doModal()
    if keyboard.isConfirmed():
        string = keyboard.getText().replace(l11l1lUK_Turk_No1 (u"ࠨࠢࠪশ"),l11l1lUK_Turk_No1 (u"ࠩ࠮ࠫষ"))
        if len(string)>1:
            url = l11l1lUK_Turk_No1 (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡲࡵࡶࡪࡧ࠷ࡹ࠳ࡩࡨ࠰ࡁࡶࡁࠧস") + string
            l1111l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        else: quit()
def l1111l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        link=l1llll111UK_Turk_No1(url)
        l11lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࠥࡧ࡮ࡪ࡯ࡤࡸ࡮ࡵ࡮࠮࠴ࠥࡂ࠳࠱࠿࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠰ࡅࠩࠣࡀ࠱࠯ࡄࡂࡩ࡮ࡩࠣࡷࡷࡩ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡣ࡯ࡸࡂࠨࠨ࠯࠭ࡂ࠭ࠧࠦ࠯࠿ࠩহ"),re.DOTALL).findall(link)
        for url,l1l11l11UK_Turk_No1,name in l11lUK_Turk_No1:
            name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠹࠴࠴࠻ࡀࠨ঺"),l11l1lUK_Turk_No1 (u"ࠨࠧࠣ঻")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠻࠶࠶࠷࠻়ࠣ"),l11l1lUK_Turk_No1 (u"ࠣ࠯ࠥঽ")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠵࠹࠸࠼ࠤা"),l11l1lUK_Turk_No1 (u"ࠥࠪࠧি"))
            l1111111UK_Turk_No1(name,url,41,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬী"))
def l11l11lUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡪࡶ࡯ࡩࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡩࡵ࡮ࡨࡂࠬু")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠧূ")).findall(item)[0]
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡦࡶࡦࡶࡥࡳࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡶࡧࡷࡧࡰࡦࡴࡁࠫৃ")).findall(item)[0]
        l1l11111UK_Turk_No1(name,url,20,l1l11l11UK_Turk_No1,fanart)
def l1lllll11UK_Turk_No1(url,l1l11l11UK_Turk_No1):
        string=url+l11l1lUK_Turk_No1 (u"ࠨ࠰ࡶࡧࡷࡧࡰࡦࠪࠬࠫৄ")
        link=eval(string)
        match= re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿࡭ࡹ࡫࡭࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡷࡩࡲࡄࠧ৅"),re.DOTALL).findall(link)
        count=str(len(match))
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠪࡧࡴࡻ࡮ࡵࠩ৆"),count)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧࡶࠨে"),l11l1lUK_Turk_No1 (u"ࠬࡴ࡯ࠨৈ"))
        for item in match:
                try:
                        if l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡲࡲࡶࡹࡹࡤࡦࡸ࡬ࡰࡃ࠭৉") in item: l11111llUK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽࡫ࡳࡸࡻࡄࠧ৊")in item: l11l11llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠨ࠾ࡌࡱࡦ࡭ࡥ࠿ࠩো")in item: l11l1l11lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸࡪࡾࡴ࠿ࠩৌ")in item: l1llUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡩࡲࡢࡲࡨࡶࡃ্࠭") in item: l11l11lUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠫࡁࡸࡥࡥ࡫ࡵࡩࡨࡺ࠾ࠨৎ") in item: l111l1l11UK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠬࡂ࡯࡬ࡶ࡬ࡸࡱ࡫࠾ࠨ৏") in item: OK(item)
                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡥ࡮ࡁࠫ৐") in item: l111llllUK_Turk_No1(item)
                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡦࡶࡦࡶࡥࡳࡀࠪ৑") in item: l11l11lUK_Turk_No1(item,l1l11l11UK_Turk_No1)
                        else:l11l1UK_Turk_No1(item,url,l1l11l11UK_Turk_No1)
                except:pass
def l111llllUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡭ࡹࡲࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡬ࡸࡱ࡫࠾ࠨ৒")).findall(item)[0]
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡤ࡭ࡀࠪ৓")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠫ৔")).findall(item)[0]
        l11l1llUK_Turk_No1(name,url,19,l1l11l11UK_Turk_No1,fanart)
def l111l1l1lUK_Turk_No1(name,url):
        filename=url.split(l11l1lUK_Turk_No1 (u"ࠫ࠴࠭৕"))[-1]
        if filename==l11l1lUK_Turk_No1 (u"ࠬࡲࡡࡵࡧࡶࡸࠬ৖"):filename=l11l1lUK_Turk_No1 (u"࠭ࡁࡤࡧࡖࡸࡷ࡫ࡡ࡮ࡇࡱ࡫࡮ࡴࡥ࠯ࡣࡳ࡯ࠬৗ")
        import downloader
        dialog = xbmcgui.Dialog()
        dp = xbmcgui.DialogProgress()
        l11lll1UK_Turk_No1 = dialog.browse(0, l11l1lUK_Turk_No1 (u"ࠧࡔࡧ࡯ࡩࡨࡺࠠࡧࡱ࡯ࡨࡪࡸࠠࡵࡱࠣࡨࡴࡽ࡮࡭ࡱࡤࡨࠥࡺ࡯ࠨ৘"), l11l1lUK_Turk_No1 (u"ࠨ࡯ࡼࡴࡷࡵࡧࡳࡣࡰࡷࠬ৙"))
        lib=os.path.join(l11lll1UK_Turk_No1, filename)
        dp.create(l11l1lUK_Turk_No1 (u"ࠩࡇࡳࡼࡴ࡬ࡰࡣࡧ࡭ࡳ࡭ࠧ৚"),l11l1lUK_Turk_No1 (u"ࠪࠫ৛"),l11l1lUK_Turk_No1 (u"ࠫࠬড়"), l11l1lUK_Turk_No1 (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡝ࡡࡪࡶࠪঢ়"))
        downloader.download(url, lib, dp)
        dp.close()
        dialog = xbmcgui.Dialog()
        dialog.ok(l11l1lUK_Turk_No1 (u"࠭ࡄࡰࡹࡱࡰࡴࡧࡤࠡࡥࡲࡱࡵࡲࡥࡵࡧࠪ৞"),l11l1lUK_Turk_No1 (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡨࡵࡳࡲ࠴࠮ࠨয়"),l11lll1UK_Turk_No1)
def OK(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡭ࡹࡲࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡬ࡸࡱ࡫࠾ࠨৠ")).findall(item)[0]
        l1l1l1ll1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡳࡰࡺࡩࡵ࡮ࡨࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡴࡱࡴࡪࡶ࡯ࡩࡃ࠭ৡ")).findall(item)[0]
        line1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡱ࡯࡮ࡦ࠳ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡰ࡮ࡴࡥ࠲ࡀࠪৢ")).findall(item)[0]
        line2=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡲࡩ࡯ࡧ࠵ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡱ࡯࡮ࡦ࠴ࡁࠫৣ")).findall(item)[0]
        line3=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂ࡬ࡪࡰࡨ࠷ࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡲࡩ࡯ࡧ࠶ࡂࠬ৤")).findall(item)[0]
        text=l11l1lUK_Turk_No1 (u"࠭ࠣࠤࠩ৥")+l1l1l1ll1UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧࠤࠩ০")+line1+l11l1lUK_Turk_No1 (u"ࠨࠥࠪ১")+line2+l11l1lUK_Turk_No1 (u"ࠩࠦࠫ২")+line3+l11l1lUK_Turk_No1 (u"ࠪࠧࠨ࠭৩")
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡂࠬ৪")).findall(item)[0]
        l11l1llUK_Turk_No1(name,text,17,l1l11l11UK_Turk_No1,fanart)
def l111lll1UK_Turk_No1(name,url):
        lines=re.compile(l11l1lUK_Turk_No1 (u"ࠬࠩࠣࠩ࠰࠮ࡃ࠮ࠩࠣࠨ৫")).findall(url)[0].split(l11l1lUK_Turk_No1 (u"࠭ࠣࠨ৬"))
        dialog = xbmcgui.Dialog()
        dialog.ok(lines[0],lines[1],lines[2],lines[3])
def l1llUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵ࡫ࡷࡰࡪࡄࠧ৭")).findall(item)[0]
        text=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷࡩࡽࡺ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵࡧࡻࡸࡃ࠭৮")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪ৯")).findall(item)[0]
        l11l1llUK_Turk_No1(name,text,9,l1l11l11UK_Turk_No1,fanart)
def l11l1lllUK_Turk_No1(name,url):
        textfile=l1llll111UK_Turk_No1(url)
        l1111l11lUK_Turk_No1(name, textfile)
def l11l1l11lUK_Turk_No1(item):
        images=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡎࡳࡡࡨࡧࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡍࡲࡧࡧࡦࡀࠪৰ")).findall(item)
        if len(images)==1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡺࡩࡵ࡮ࡨࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡯ࡴ࡭ࡧࡁࠫৱ")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡬ࡺࡳࡢ࡯ࡣ࡬ࡰࡃ࠭৲")).findall(item)[0]
                image=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡊ࡯ࡤ࡫ࡪࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡉ࡮ࡣࡪࡩࡃ࠭৳")).findall(item)[0]
                l1l11l11UK_Turk_No1 = image.replace(l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡪ࡯ࡪࡹࡷ࠴ࡣࡰ࡯࠲ࠫ৴"),l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰࡫࠱࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࠧ৵"))+l11l1lUK_Turk_No1 (u"ࠩ࠱࡮ࡵ࡭ࠧ৶")
                image = image.replace(l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡭ࡲ࡭ࡵࡳ࠰ࡦࡳࡲ࠵ࠧ৷"),l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳࡮࠴ࡩ࡮ࡩࡸࡶ࠳ࡩ࡯࡮࠱ࠪ৸"))+l11l1lUK_Turk_No1 (u"ࠬ࠴ࡪࡱࡩࠪ৹")
                l11l1llUK_Turk_No1(name,image,7,l1l11l11UK_Turk_No1,fanart)
        elif len(images)>1:
                name=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵ࡫ࡷࡰࡪࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡪࡶ࡯ࡩࡃ࠭৺")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲ࠾ࠨ৻")).findall(item)[0]
                l1l1lllllUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩৼ")
                for image in images:
                        l1l11l11UK_Turk_No1 = image.replace(l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱࡬ࡱ࡬ࡻࡲ࠯ࡥࡲࡱ࠴࠭৽"),l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡭࠳࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࠩ৾"))+l11l1lUK_Turk_No1 (u"ࠫ࠳ࡰࡰࡨࠩ৿")
                        image = image.replace(l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡯࡭ࡨࡷࡵ࠲ࡨࡵ࡭࠰ࠩ਀"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡩ࠯࡫ࡰ࡫ࡺࡸ࠮ࡤࡱࡰ࠳ࠬਁ"))+l11l1lUK_Turk_No1 (u"ࠧ࠯࡬ࡳ࡫ࠬਂ")
                        l1l1lllllUK_Turk_No1=l1l1lllllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡌࡱࡦ࡭ࡥ࠿ࠩਃ")+image+l11l1lUK_Turk_No1 (u"ࠩ࠿࠳ࡎࡳࡡࡨࡧࡁࠫ਄")
                path = l1lll1UK_Turk_No1
                name=l1llllUK_Turk_No1(name)
                l1l1ll11UK_Turk_No1 = os.path.join(os.path.join(path,l11l1lUK_Turk_No1 (u"ࠪࠫਅ")), name+l11l1lUK_Turk_No1 (u"ࠫ࠳ࡺࡸࡵࠩਆ"))
                if not os.path.exists(l1l1ll11UK_Turk_No1):file(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠬࡽࠧਇ")).close()
                l111ll1llUK_Turk_No1 = open(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠨࡷࠣਈ"))
                l111ll1llUK_Turk_No1.write(l1l1lllllUK_Turk_No1)
                l111ll1llUK_Turk_No1.close()
                l11l1llUK_Turk_No1(name,l11l1lUK_Turk_No1 (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ਉ"),8,l1l11l11UK_Turk_No1,fanart)
def l11l11llUK_Turk_No1(item):
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡭ࡹࡲࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡬ࡸࡱ࡫࠾ࠨਊ")).findall(item)[0]
        l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪ਋")).findall(item)[0]
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀ࡮ࡶࡴࡷࡀࠫ࠲࠰ࡅࠩ࠽࠱࡬ࡴࡹࡼ࠾ࠨ਌")).findall(item)[0]
        l1l11111UK_Turk_No1(name,url,6,l1l11l11UK_Turk_No1,fanart)
def l1ll11lllUK_Turk_No1(url,l1l11l11UK_Turk_No1):
	link=l1llll111UK_Turk_No1(url)
	matches=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡣࠩ࠮ࠬࡁ࠽࠱ࡄࡡ࠰࠮࠻ࡠ࠮࠭࠴ࠪࡀࠫ࠯ࠬ࠳࠰࠿ࠪ࡞ࡱࠬ࠳࠰࠿ࠪࠦࠪ਍"),re.I+re.M+re.U+re.S).findall(link)
	l1l1l11UK_Turk_No1 = []
	for params, name, url in matches:
		l1ll1l11UK_Turk_No1 = {l11l1lUK_Turk_No1 (u"ࠧࡶࡡࡳࡣࡰࡷࠧ਎"): params, l11l1lUK_Turk_No1 (u"ࠨ࡮ࡢ࡯ࡨࠦਏ"): name, l11l1lUK_Turk_No1 (u"ࠢࡶࡴ࡯ࠦਐ"): url}
		l1l1l11UK_Turk_No1.append(l1ll1l11UK_Turk_No1)
	list = []
	for l11l11111UK_Turk_No1 in l1l1l11UK_Turk_No1:
		l1ll1l11UK_Turk_No1 = {l11l1lUK_Turk_No1 (u"ࠣࡰࡤࡱࡪࠨ਑"): l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠤࡱࡥࡲ࡫ࠢ਒")], l11l1lUK_Turk_No1 (u"ࠥࡹࡷࡲࠢਓ"): l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠦࡺࡸ࡬ࠣਔ")]}
		matches=re.compile(l11l1lUK_Turk_No1 (u"ࠬࠦࠨ࠯࠭ࡂ࠭ࡂࠨࠨ࠯࠭ࡂ࠭ࠧ࠭ਕ"),re.I+re.M+re.U+re.S).findall(l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠨࡰࡢࡴࡤࡱࡸࠨਖ")])
		for field, value in matches:
			l1ll1l11UK_Turk_No1[field.strip().lower().replace(l11l1lUK_Turk_No1 (u"ࠧ࠮ࠩਗ"), l11l1lUK_Turk_No1 (u"ࠨࡡࠪਘ"))] = value.strip()
		list.append(l1ll1l11UK_Turk_No1)
        for l11l11111UK_Turk_No1 in list:
                if l11l1lUK_Turk_No1 (u"ࠩ࠱ࡸࡸ࠭ਙ") in l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠥࡹࡷࡲࠢਚ")]:l11l1llUK_Turk_No1(l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠦࡳࡧ࡭ࡦࠤਛ")],l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠧࡻࡲ࡭ࠤਜ")],2,l1l11l11UK_Turk_No1,fanart)
                else:l1111111UK_Turk_No1(l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠨ࡮ࡢ࡯ࡨࠦਝ")],l11l11111UK_Turk_No1[l11l1lUK_Turk_No1 (u"ࠢࡶࡴ࡯ࠦਞ")],2,l1l11l11UK_Turk_No1,fanart)
def l11l1UK_Turk_No1(item,url,l1l11l11UK_Turk_No1):
        l11l1l1llUK_Turk_No1=l1l11l11UK_Turk_No1
        base=url
        l11llll1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾࡯࡭ࡳࡱ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯࡭࡫ࡱ࡯ࡃ࠭ਟ")).findall(item)
        data=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡮ࡺ࡬ࡦࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡷ࡭ࡹࡲࡥ࠿࠰࠮ࡃࡱ࡯࡮࡬ࡀࠫ࠲࠰ࡅࠩ࠽࠱࡯࡭ࡳࡱ࠾࠯࠭ࡂࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪਠ"),re.DOTALL).findall(item)
        for name,l11ll1111UK_Turk_No1,l1l11l11UK_Turk_No1 in data:
                if l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨ࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡲࡩࡴࡶࡂࠫਡ") in l11ll1111UK_Turk_No1:
                        l1111l111UK_Turk_No1 = l11ll1111UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠫࡱ࡯ࡳࡵ࠿ࠪਢ"))[1]
                        l1l11111UK_Turk_No1(name,l11ll1111UK_Turk_No1,mode,l1l11l11UK_Turk_No1,fanart,description=l1111l111UK_Turk_No1)
        if len(l11llll1lUK_Turk_No1)==1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡪࡶ࡯ࡩࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡩࡵ࡮ࡨࡂࠬਣ")).findall(item)[0]
                url=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼࡭࡫ࡱ࡯ࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡲࡩ࡯࡭ࡁࠫਤ")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲ࠾ࠨਥ")).findall(item)[0]
                print l1l11l11UK_Turk_No1
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠨࡋࡰࡥ࡬࡫ࡈࡦࡴࡨࠫਦ"):l1l11l11UK_Turk_No1=l11l1l1llUK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠩ࠱ࡸࡸ࠭ਧ") in url:l11l1llUK_Turk_No1(name,url,16,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫਨ"))
                elif l11l1lUK_Turk_No1 (u"ࠫࡲࡵࡶࡪࡧࡶࠫ਩") in base:
                        l1l11UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,int(count),isFolder=False)
                else:l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
        elif len(l11llll1lUK_Turk_No1)>1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡴࡪࡶ࡯ࡩࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡺࡩࡵ࡮ࡨࡂࠬਪ")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠧਫ")).findall(item)[0]
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠧࡊ࡯ࡤ࡫ࡪࡎࡥࡳࡧࠪਬ"):l1l11l11UK_Turk_No1=l11l1l1llUK_Turk_No1
                if l11l1lUK_Turk_No1 (u"ࠨ࠰ࡷࡷࠬਭ") in url:l11l1llUK_Turk_No1(name,url,16,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪਮ"))
                elif l11l1lUK_Turk_No1 (u"ࠪࡱࡴࡼࡩࡦࡵࠪਯ") in base:
                        l1l11UK_Turk_No1(name,url,3,l1l11l11UK_Turk_No1,int(count),isFolder=False)
                else:l1111111UK_Turk_No1(name,url,3,l1l11l11UK_Turk_No1,fanart)
def l1lllll1lUK_Turk_No1(url):
	link=l1llll111UK_Turk_No1(url)
	sort=False
	match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡳࡧ࡭ࡦ࠿ࠥࠬ࠳࠱࠿ࠪࠤ࠱࠯ࡄࡸ࡬࠾ࠤࠫ࠲࠰ࡅࠩࠣ࠰࠮ࡃࡲ࡭࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠨਰ"),re.DOTALL).findall(link)
	if l11l1lUK_Turk_No1 (u"ࠬࡺࡶࠦ࠴࠳ࡷ࡭ࡵࡷࡴࠩ਱") in url or l11l1lUK_Turk_No1 (u"࠭ࡣࡢࡴࡷࡳࡴࡴࡳࠨਲ") in url:
                match=sorted(match)
                sort=True
	for name,url,icon in match:
                        if name[0]==l11l1lUK_Turk_No1 (u"ࠧ࠱ࠩਲ਼"):
                                if sort==True:
                                        name=name[1:] + l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡩࡲࡰࡩࡣࠠࠡࠢࠫࡒࡪࡽࠩ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ਴")
                        if l11l1lUK_Turk_No1 (u"ࠩࡼࡳࡺࡺࡵࡣࡧ࠱ࡧࡴࡳ࠯ࡱ࡮ࡤࡽࡱ࡯ࡳࡵࡁ࡯࡭ࡸࡺ࠽ࠨਵ") in url:
                                l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                        elif l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨ࠲ࡨࡵ࡭࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡶࡩࡦࡸࡣࡩࡡࡴࡹࡪࡸࡹ࠾ࠩਸ਼") in url:
                                l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                        else:
                                l1l11111UK_Turk_No1(name,url,1,icon,fanart)
def l11111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        if l11l1lUK_Turk_No1 (u"ࠫࡾࡵࡵࡵࡷࡥࡩ࠳ࡩ࡯࡮࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡷࡪࡧࡲࡤࡪࡢࡵࡺ࡫ࡲࡺ࠿ࠪ਷") in url:
		l1111l111UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠬࡹࡥࡢࡴࡦ࡬ࡤࡷࡵࡦࡴࡼࡁࠬਸ"))[1]
		l111l1ll1UK_Turk_No1 = l1lll111UK_Turk_No1 + l1111l111UK_Turk_No1 + l111l111lUK_Turk_No1
		req = urllib2.Request(l111l1ll1UK_Turk_No1)
		req.add_header(l11l1lUK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪਹ"), l11l1lUK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹ࠻ࠡࡗ࠾ࠤ࡜࡯࡮ࡥࡱࡺࡷࠥࡔࡔࠡ࠷࠱࠵ࡀࠦࡥ࡯࠯ࡊࡆࡀࠦࡲࡷ࠼࠴࠲࠾࠴࠰࠯࠵ࠬࠤࡌ࡫ࡣ࡬ࡱ࠲࠶࠵࠶࠸࠱࠻࠵࠸࠶࠽ࠠࡇ࡫ࡵࡩ࡫ࡵࡸ࠰࠵࠱࠴࠳࠹ࠧ਺"))
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		link = link.replace(l11l1lUK_Turk_No1 (u"ࠨ࡞ࡵࠫ਻"),l11l1lUK_Turk_No1 (u"਼ࠩࠪ")).replace(l11l1lUK_Turk_No1 (u"ࠪࡠࡳ࠭਽"),l11l1lUK_Turk_No1 (u"ࠫࠬਾ")).replace(l11l1lUK_Turk_No1 (u"ࠬࠦࠠࠨਿ"),l11l1lUK_Turk_No1 (u"࠭ࠧੀ"))
		match=re.compile(l11l1lUK_Turk_No1 (u"ࠧࠣࡸ࡬ࡨࡪࡵࡉࡥࠤ࠽ࠤࠧ࠮࠮ࠬࡁࠬࠦ࠳࠱࠿ࠣࡶ࡬ࡸࡱ࡫ࠢ࠻ࠢࠥࠬ࠳࠱࠿ࠪࠤࠪੁ"),re.DOTALL).findall(link)
		for l1l111l1lUK_Turk_No1,name in match:
			url = l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡹࡰࡷࡷࡹࡧ࡫࠮ࡤࡱࡰ࠳ࡼࡧࡴࡤࡪࡂࡺࡂ࠭ੂ")+l1l111l1lUK_Turk_No1
			l1l11l11UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲࡭࠳ࡿࡴࡪ࡯ࡪ࠲ࡨࡵ࡭࠰ࡸ࡬࠳ࠪࡹ࠯ࡩࡳࡧࡩ࡫ࡧࡵ࡭ࡶ࠱࡮ࡵ࡭ࠧ੃")%l1l111l1lUK_Turk_No1
			l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
	elif l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨ࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡲࡩࡴࡶࡂࡰ࡮ࡹࡴ࠾ࠩ੄") in url:
		l1111l111UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡡࡺ࡮࡬ࡷࡹࡅ࡬ࡪࡵࡷࡁࠬ੅"))[1]
		l111l1ll1UK_Turk_No1 = l1111lll1UK_Turk_No1 + l1111l111UK_Turk_No1 + l111l11UK_Turk_No1
		req = urllib2.Request(l111l1ll1UK_Turk_No1)
		req.add_header(l11l1lUK_Turk_No1 (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩ੆"), l11l1lUK_Turk_No1 (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠤ࠭࡝ࡩ࡯ࡦࡲࡻࡸࡁࠠࡖ࠽࡛ࠣ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠶࠰࠴࠿ࠥ࡫࡮࠮ࡉࡅ࠿ࠥࡸࡶ࠻࠳࠱࠽࠳࠶࠮࠴ࠫࠣࡋࡪࡩ࡫ࡰ࠱࠵࠴࠵࠾࠰࠺࠴࠷࠵࠼ࠦࡆࡪࡴࡨࡪࡴࡾ࠯࠴࠰࠳࠲࠸࠭ੇ"))
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		link = link.replace(l11l1lUK_Turk_No1 (u"ࠧ࡝ࡴࠪੈ"),l11l1lUK_Turk_No1 (u"ࠨࠩ੉")).replace(l11l1lUK_Turk_No1 (u"ࠩ࡟ࡲࠬ੊"),l11l1lUK_Turk_No1 (u"ࠪࠫੋ")).replace(l11l1lUK_Turk_No1 (u"ࠫࠥࠦࠧੌ"),l11l1lUK_Turk_No1 (u"੍ࠬ࠭"))
		match=re.compile(l11l1lUK_Turk_No1 (u"࠭ࠢࡵ࡫ࡷࡰࡪࠨ࠺ࠡࠤࠫ࠲࠰ࡅࠩࠣ࠰࠮ࡃࠧࡼࡩࡥࡧࡲࡍࡩࠨ࠺ࠡࠤࠫ࠲࠰ࡅࠩࠣࠩ੎"),re.DOTALL).findall(link)
		for name,l1l111l1lUK_Turk_No1 in match:
			url = l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡹࡺࡻ࠳ࡿ࡯ࡶࡶࡸࡦࡪ࠴ࡣࡰ࡯࠲ࡻࡦࡺࡣࡩࡁࡹࡁࠬ੏")+l1l111l1lUK_Turk_No1
			l1l11l11UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱࡬࠲ࡾࡺࡩ࡮ࡩ࠱ࡧࡴࡳ࠯ࡷ࡫࠲ࠩࡸ࠵ࡨࡲࡦࡨࡪࡦࡻ࡬ࡵ࠰࡭ࡴ࡬࠭੐")%l1l111l1lUK_Turk_No1
			l1111111UK_Turk_No1(name,url,2,l1l11l11UK_Turk_No1,fanart)
def l1l111lllUK_Turk_No1(item):
        item=item.replace(l11l1lUK_Turk_No1 (u"ࠩ࡟ࡶࠬੑ"),l11l1lUK_Turk_No1 (u"ࠪࠫ੒")).replace(l11l1lUK_Turk_No1 (u"ࠫࡡࡺࠧ੓"),l11l1lUK_Turk_No1 (u"ࠬ࠭੔")).replace(l11l1lUK_Turk_No1 (u"࠭ࠦ࡯ࡤࡶࡴࡀ࠭੕"),l11l1lUK_Turk_No1 (u"ࠧࠨ੖")).replace(l11l1lUK_Turk_No1 (u"ࠨ࡞ࠪࠫ੗"),l11l1lUK_Turk_No1 (u"ࠩࠪ੘")).replace(l11l1lUK_Turk_No1 (u"ࠪࡠࡳ࠭ਖ਼"),l11l1lUK_Turk_No1 (u"ࠫࠬਗ਼"))
        data=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡴࡡ࡮ࡧࡀࠦ࠭࠴ࠫࡀࠫࠥ࠲࠰ࡅࡲ࡭࠿ࠥࠬ࠳࠱࠿ࠪࠤ࠱࠯ࡄࡳࡧ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠩਜ਼"),re.DOTALL).findall(item)
        for name,url,l1l11l11UK_Turk_No1 in data:
                if l11l1lUK_Turk_No1 (u"࠭ࡹࡰࡷࡷࡹࡧ࡫࠮ࡤࡱࡰ࠳ࡨ࡮ࡡ࡯ࡰࡨࡰ࠴࠭ੜ") in url:
                        l1111l111UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠧࡤࡪࡤࡲࡳ࡫࡬࠰ࠩ੝"))[1]
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l1111l111UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠨࡻࡲࡹࡹࡻࡢࡦ࠰ࡦࡳࡲ࠵ࡵࡴࡧࡵ࠳ࠬਫ਼") in url:
                        l1111l111UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠩࡸࡷࡪࡸ࠯ࠨ੟"))[1]
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l1111l111UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠪࡽࡴࡻࡴࡶࡤࡨ࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡲࡩࡴࡶࡂࠫ੠") in url:
                        l1111l111UK_Turk_No1 = url.split(l11l1lUK_Turk_No1 (u"ࠫࡱ࡯ࡳࡵ࠿ࠪ੡"))[1]
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l1111l111UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠿࠵࠯ࠨ੢") in url:
                        l1ll1l1lUK_Turk_No1 = HTMLParser()
                        url=l1ll1l1lUK_Turk_No1.unescape(url)
                        l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart)
                else:
                        l1l11111UK_Turk_No1(name,url,1,l1l11l11UK_Turk_No1,fanart)
def l11111llUK_Turk_No1(item,url,l1l11l11UK_Turk_No1):
        l11l1l1llUK_Turk_No1=l1l11l11UK_Turk_No1
        l11llll1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡲࡲࡶࡹࡹࡤࡦࡸ࡬ࡰࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡹࡰࡰࡴࡷࡷࡩ࡫ࡶࡪ࡮ࡁࠫ੣")).findall(item)
        l1l1ll111UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽࡮࡬ࡲࡰࡄࠨ࠯࠭ࡂ࠭ࡁ࠵࡬ࡪࡰ࡮ࡂࠬ੤")).findall(item)
        if len(l11llll1lUK_Turk_No1)+len(l1l1ll111UK_Turk_No1)==1:
                name=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡷ࡭ࡹࡲࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶ࡬ࡸࡱ࡫࠾ࠨ੥")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࠪ੦")).findall(item)[0]
                url=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡶ࡯ࡳࡶࡶࡨࡪࡼࡩ࡭ࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡶࡴࡴࡸࡴࡴࡦࡨࡺ࡮ࡲ࠾ࠨ੧")).findall(item)[0]
                url = l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠾࠴࠵ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳࡙ࡰࡰࡴࡷࡷࡉ࡫ࡶࡪ࡮࠲ࡃࡲࡵࡤࡦ࠿࠴ࠪࡦࡳࡰ࠼࡫ࡷࡩࡲࡃࡣࡢࡶࡦ࡬ࡪࡸࠥ࠴ࡦࡶࡸࡷ࡫ࡡ࡮ࡵࠨ࠶࠻ࡻࡲ࡭࠿ࠪ੨") +url
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠬࡏ࡭ࡢࡩࡨࡌࡪࡸࡥࠨ੩"):l1l11l11UK_Turk_No1=l11l1l1llUK_Turk_No1
                l11l1llUK_Turk_No1(name,url,16,l1l11l11UK_Turk_No1,fanart)
        elif len(l11llll1lUK_Turk_No1)+len(l1l1ll111UK_Turk_No1)>1:
                name=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵ࡫ࡷࡰࡪࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡴࡪࡶ࡯ࡩࡃ࠭੪")).findall(item)[0]
                l1l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡹ࡮ࡵ࡮ࡤࡱࡥ࡮ࡲ࠾ࠨ੫")).findall(item)[0]
                if l1l11l11UK_Turk_No1==l11l1lUK_Turk_No1 (u"ࠨࡋࡰࡥ࡬࡫ࡈࡦࡴࡨࠫ੬"):l1l11l11UK_Turk_No1=l11l1l1llUK_Turk_No1
                l11l1llUK_Turk_No1(name,url,3,l1l11l11UK_Turk_No1,fanart)
def l1l1ll1UK_Turk_No1(link):
	if l111l1lllUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠩࠪ੭"):
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(l11l1lUK_Turk_No1 (u"ࠪࡅࡩࡻ࡬ࡵࠢࡆࡳࡳࡺࡥ࡯ࡶࠪ੮"), l11l1lUK_Turk_No1 (u"ࠫ࡞ࡵࡵࠡࡪࡤࡺࡪࠦ࡯ࡱࡶࡨࡨࠥࡺ࡯ࠡࡵ࡫ࡳࡼࠦࡡࡥࡷ࡯ࡸࠥࡩ࡯࡯ࡶࡨࡲࡹ࠭੯"),l11l1lUK_Turk_No1 (u"ࠬ࠭ੰ"),l11l1lUK_Turk_No1 (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡳࡦࡶࠣࡥࠥࡶࡡࡴࡵࡺࡳࡷࡪࠠࡵࡱࠣࡴࡷ࡫ࡶࡦࡰࡷࠤࡦࡩࡣࡪࡦࡨࡲࡹࡧ࡬ࠡࡣࡦࡧࡪࡹࡳࠨੱ"),l11l1lUK_Turk_No1 (u"ࠧࡄࡣࡱࡧࡪࡲࠧੲ"),l11l1lUK_Turk_No1 (u"ࠨࡑࡎࠫੳ"))
		if ret == 1:
                        l1lll11l1UK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠩࠪੴ"), l11l1lUK_Turk_No1 (u"ࠪࡗࡪࡺࠠࡑࡣࡶࡷࡼࡵࡲࡥࠩੵ"))
			l1lll11l1UK_Turk_No1.doModal()
			if (l1lll11l1UK_Turk_No1.isConfirmed()):
			    l1l1UK_Turk_No1 = l1lll11l1UK_Turk_No1.getText()
			    l11l1ll1lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭੶"),l1l1UK_Turk_No1)
                else:quit()
	elif l111l1lllUK_Turk_No1 <> l11l1lUK_Turk_No1 (u"ࠬ࠭੷"):
		dialog = xbmcgui.Dialog()
		ret = dialog.yesno(l11l1lUK_Turk_No1 (u"࠭ࡁࡥࡷ࡯ࡸࠥࡉ࡯࡯ࡶࡨࡲࡹ࠭੸"), l11l1lUK_Turk_No1 (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡦࡰࡷࡩࡷࠦࡴࡩࡧࠣࡴࡦࡹࡳࡸࡱࡵࡨࠥࡿ࡯ࡶࠢࡶࡩࡹ࠭੹"),l11l1lUK_Turk_No1 (u"ࠨࡶࡲࠤࡨࡵ࡮ࡵ࡫ࡱࡹࡪ࠭੺"),l11l1lUK_Turk_No1 (u"ࠩࠪ੻"),l11l1lUK_Turk_No1 (u"ࠪࡇࡦࡴࡣࡦ࡮ࠪ੼"),l11l1lUK_Turk_No1 (u"ࠫࡔࡑࠧ੽"))
		if ret == 1:
			l1lll11l1UK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠬ࠭੾"), l11l1lUK_Turk_No1 (u"࠭ࡅ࡯ࡶࡨࡶࠥࡖࡡࡴࡵࡺࡳࡷࡪࠧ੿"))
			l1lll11l1UK_Turk_No1.doModal()
			if (l1lll11l1UK_Turk_No1.isConfirmed()):
				l1l1UK_Turk_No1 = l1lll11l1UK_Turk_No1.getText()
			if l1l1UK_Turk_No1 <> l111l1lllUK_Turk_No1:
				quit()
		else:quit()
def l1l1l1l1UK_Turk_No1():
        link=l1llll111UK_Turk_No1(l1ll1l1l1UK_Turk_No1)
        l1ll11111UK_Turk_No1=[l11l1lUK_Turk_No1 (u"ࠧࡍ࡫ࡹࡩ࡚ࠥࡖࠨ઀"),l11l1lUK_Turk_No1 (u"ࠨࡕࡳࡳࡷࡺࡳࠨઁ"),l11l1lUK_Turk_No1 (u"ࠩࡐࡳࡻ࡯ࡥࡴࠩં"),l11l1lUK_Turk_No1 (u"ࠪࡘ࡛ࠦࡓࡩࡱࡺࡷࠬઃ"),l11l1lUK_Turk_No1 (u"ࠫࡈࡧࡲࡵࡱࡲࡲࡸ࠭઄"),l11l1lUK_Turk_No1 (u"ࠬࡊ࡯ࡤࡷࡰࡩࡳࡺࡡࡳ࡫ࡨࡷࠬઅ"),l11l1lUK_Turk_No1 (u"࠭ࡓࡵࡣࡱࡨࡺࡶࠧઆ"),l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡧࡪࡸࡴࡴࠩઇ"),l11l1lUK_Turk_No1 (u"ࠨࡔࡤࡨ࡮ࡵࠧઈ"),l11l1lUK_Turk_No1 (u"ࠩࡆࡇ࡙࡜ࠧઉ"),l11l1lUK_Turk_No1 (u"ࠪࡘࡺࡸ࡫ࡪࡵ࡫ࠤ࡙࡜ࠧઊ"),l11l1lUK_Turk_No1 (u"࡙ࠫࡻࡲ࡬࡫ࡶ࡬ࠥࡓ࡯ࡷ࡫ࡨࡷࠬઋ"),l11l1lUK_Turk_No1 (u"ࠬࡌࡩࡵࡰࡨࡷࡸ࠭ઌ"),l11l1lUK_Turk_No1 (u"࠭ࡆࡰࡱࡧࠤࡕࡵࡲ࡯ࠩઍ")]
        l1lll11l1UK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠧࠨ઎"), l11l1lUK_Turk_No1 (u"ࠨࡕࡨࡥࡷࡩࡨࠨએ"))
	l1lll11l1UK_Turk_No1.doModal()
	if (l1lll11l1UK_Turk_No1.isConfirmed()):
		l1111l111UK_Turk_No1=l1lll11l1UK_Turk_No1.getText()
		l1111l111UK_Turk_No1=l1111l111UK_Turk_No1.upper()
	else:quit()
        l1llll1l1UK_Turk_No1=[]
        l11llUK_Turk_No1=[]
        link=l1llll111UK_Turk_No1(l1ll1l1l1UK_Turk_No1)
        dialog = xbmcgui.Dialog()
	ret = dialog.multiselect(l11l1lUK_Turk_No1 (u"ࠤࡖࡩࡱ࡫ࡣࡵࠢࡺ࡬࡮ࡩࡨࠡࡥࡤࡸࡪ࡭࡯ࡳ࡫ࡨࡷࠥࡺ࡯ࠡࡵࡨࡥࡷࡩࡨࠣઐ"), l1ll11111UK_Turk_No1)
	for num in ret:
                l1llll1l1UK_Turk_No1.append(l1ll11111UK_Turk_No1[num])
        for l1ll11ll1UK_Turk_No1 in l1llll1l1UK_Turk_No1:
                string=l11l1lUK_Turk_No1 (u"ࠪࡀࠬઑ")+l1ll11ll1UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡃ࠮࠮ࠬࡁࠬࡀ࠴࠭઒")+l1ll11ll1UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡄࠧઓ")
                match=re.compile(string,re.DOTALL).findall(link)
                for data in match:
                        match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡤࡣࡷࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡨࡧࡴ࠿ࠩઔ")).findall(data)
                        print match
                        for data in match:
                                l11llUK_Turk_No1.append(data)
        for l11lllllUK_Turk_No1 in l11llUK_Turk_No1:
                try:
                        link=l1llll111UK_Turk_No1(l11lllllUK_Turk_No1)
                        l1l1l11l1UK_Turk_No1(content, l11111l1lUK_Turk_No1,link)
                        if l11l1lUK_Turk_No1 (u"ࠧࡊࡰࡧࡩࡽ࠭ક") in l11lllllUK_Turk_No1:
                                sort=False
                                match=re.compile(l11l1lUK_Turk_No1 (u"ࠨࡰࡤࡱࡪࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠮ࠬࡁࡵࡰࡂࠨࠨ࠯࠭ࡂ࠭ࠧ࠴ࠫࡀ࡯ࡪࡁࠧ࠮࠮ࠬࡁࠬࠦࠬખ"),re.DOTALL).findall(link)
                                for name,url,icon in match:
                                        if l1111l111UK_Turk_No1 in name.upper():
                                                if name[0]==l11l1lUK_Turk_No1 (u"ࠩ࠳ࠫગ"):
                                                        name=name[1:] + l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࠢࠣࠤ࠭ࡔࡥࡸࠫ࡞࠳ࡈࡕࡌࡐࡔࡠࠫઘ")
                                                if l11l1lUK_Turk_No1 (u"ࠫࡾࡵࡵࡵࡷࡥࡩ࠳ࡩ࡯࡮࠱ࡳࡰࡦࡿ࡬ࡪࡵࡷࡃࡱ࡯ࡳࡵ࠿ࠪઙ") in url:
                                                        l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                                                elif l11l1lUK_Turk_No1 (u"ࠬࡿ࡯ࡶࡶࡸࡦࡪ࠴ࡣࡰ࡯࠲ࡶࡪࡹࡵ࡭ࡶࡶࡃࡸ࡫ࡡࡳࡥ࡫ࡣࡶࡻࡥࡳࡻࡀࠫચ") in url:
                                                        l1l11111UK_Turk_No1(name,url,18,icon,fanart)
                                                else:
                                                        l1l11111UK_Turk_No1(name,url,1,icon,fanart)
                        else:
                                match= re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡪࡶࡨࡱࡃ࠮࠮ࠬࡁࠬࡀ࠴࡯ࡴࡦ࡯ࡁࠫછ"),re.DOTALL).findall(link)
                                count=str(len(match))
                                l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠧࡤࡱࡸࡲࡹ࠭જ"),count)
                                l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬઝ"),l11l1lUK_Turk_No1 (u"ࠩࡱࡳࠬઞ"))
                                for item in match:
                                        title= re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡹ࡯ࡴ࡭ࡧࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡸ࡮ࡺ࡬ࡦࡀࠪટ")).findall(item)[0]
                                        if l1111l111UK_Turk_No1 in title.upper():
                                                try:
                                                        if l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡰࡰࡴࡷࡷࡩ࡫ࡶࡪ࡮ࡁࠫઠ") in item: l11111llUK_Turk_No1(item,l11lllllUK_Turk_No1,l1l11l11UK_Turk_No1)
                                                        elif l11l1lUK_Turk_No1 (u"ࠬࡂࡩࡱࡶࡹࡂࠬડ")in item: l11l11llUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"࠭࠼ࡊ࡯ࡤ࡫ࡪࡄࠧઢ")in item: l11l1l11lUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶࡨࡼࡹࡄࠧણ")in item: l1llUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡧࡷࡧࡰࡦࡴࡁࠫત") in item: l11l11lUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠩ࠿ࡶࡪࡪࡩࡳࡧࡦࡸࡃ࠭થ") in item: l111l1l11UK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠪࡀࡴࡱࡴࡪࡶ࡯ࡩࡃ࠭દ") in item: OK(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠫࡁࡪ࡬࠿ࠩધ") in item: l111llllUK_Turk_No1(item)
                                                        elif l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡤࡴࡤࡴࡪࡸ࠾ࠨન") in item: l11l11lUK_Turk_No1(item)
                                                        else:l11l1UK_Turk_No1(item,l11lllllUK_Turk_No1,l1l11l11UK_Turk_No1)
                                                except:pass
                except:pass
def l1ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l11l1l1llUK_Turk_No1=l1l11l11UK_Turk_No1
	l111l1llUK_Turk_No1=[]
	l1111lllUK_Turk_No1=[]
	l11l11l1UK_Turk_No1=[]
	link=l1llll111UK_Turk_No1(url)
	urls=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡵ࡫ࡷࡰࡪࡄࠧ઩")+re.escape(name)+l11l1lUK_Turk_No1 (u"ࠧ࠽࠱ࡷ࡭ࡹࡲࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡷࡩࡲࡄࠧપ"),re.DOTALL).findall(link)[0]
        l11llll1lUK_Turk_No1=[]
	if l11l1lUK_Turk_No1 (u"ࠨ࠾࡯࡭ࡳࡱ࠾ࠨફ") in urls:
                l11111l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡰ࡮ࡴ࡫࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡮࡬ࡲࡰࡄࠧબ")).findall(urls)
                for l1l1lllUK_Turk_No1 in l11111l1UK_Turk_No1:
                        l11llll1lUK_Turk_No1.append(l1l1lllUK_Turk_No1)
        if l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡶ࡯ࡳࡶࡶࡨࡪࡼࡩ࡭ࡀࠪભ") in urls:
                l1l1l1l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡰࡰࡴࡷࡷࡩ࡫ࡶࡪ࡮ࡁࠬ࠳࠱࠿ࠪ࠾࠲ࡷࡵࡵࡲࡵࡵࡧࡩࡻ࡯࡬࠿ࠩમ")).findall(urls)
                for l11ll1llUK_Turk_No1 in l1l1l1l11UK_Turk_No1:
                        l11ll1llUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠿࠵࠯ࡱ࡮ࡸ࡫࡮ࡴ࠮ࡷ࡫ࡧࡩࡴ࠴ࡓࡱࡱࡵࡸࡸࡊࡥࡷ࡫࡯࠳ࡄࡳ࡯ࡥࡧࡀ࠵ࠫࡧ࡭ࡱ࠽࡬ࡸࡪࡳ࠽ࡤࡣࡷࡧ࡭࡫ࡲࠦ࠵ࡧࡷࡹࡸࡥࡢ࡯ࡶࠩ࠷࠼ࡵࡳ࡮ࡀࠫય") +l11ll1llUK_Turk_No1
                        l11llll1lUK_Turk_No1.append(l11ll1llUK_Turk_No1)
	i=1
	for l1lll1l1UK_Turk_No1 in l11llll1lUK_Turk_No1:
                l11l11lllUK_Turk_No1=l1lll1l1UK_Turk_No1
                if l11l1lUK_Turk_No1 (u"࠭ࡡࡤࡧࡶࡸࡷ࡫ࡡ࡮࠼࠲࠳ࠬર") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠧ࠯ࡣࡦࡩࡱ࡯ࡶࡦࠩ઱") in l1lll1l1UK_Turk_No1 or l11l1lUK_Turk_No1 (u"ࠨࡵࡲࡴ࠿࠵࠯ࠨલ")in l1lll1l1UK_Turk_No1:l1l11l11lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠣࠬࡆࡩࡥࡴࡶࡵࡩࡦࡳࡳࠪࠩળ")
                else:l1l11l11lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪࠫ઴")
                if l11l1lUK_Turk_No1 (u"ࠫ࠭࠭વ") in l1lll1l1UK_Turk_No1:
                        l1lll1l1UK_Turk_No1=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠬ࠮ࠧશ"))[0]
                        l1111l1lUK_Turk_No1=str(l11l11lllUK_Turk_No1.split(l11l1lUK_Turk_No1 (u"࠭ࠨࠨષ"))[1].replace(l11l1lUK_Turk_No1 (u"ࠧࠪࠩસ"),l11l1lUK_Turk_No1 (u"ࠨࠩહ"))+l1l11l11lUK_Turk_No1)
                        l111l1llUK_Turk_No1.append(l1lll1l1UK_Turk_No1)
                        l1111lllUK_Turk_No1.append(l1111l1lUK_Turk_No1)
                else:
                        domain=l1lll1l1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠩ࠲ࠫ઺"))[2].replace(l11l1lUK_Turk_No1 (u"ࠪࡻࡼࡽ࠮ࠨ઻"),l11l1lUK_Turk_No1 (u"઼ࠫࠬ"))
                        l111l1llUK_Turk_No1.append( l1lll1l1UK_Turk_No1 )
                        l1111lllUK_Turk_No1.append(l11l1lUK_Turk_No1 (u"ࠬࡒࡩ࡯࡭ࠣࠫઽ")+str(i)+l1l11l11lUK_Turk_No1)#+ l11l1lUK_Turk_No1 (u"࠭ࠠࡽࠢࠪા") +domain)
                i=i+1
	dialog = xbmcgui.Dialog()
	select = dialog.select(l11l1lUK_Turk_No1 (u"ࠧࡄࡪࡲࡳࡸ࡫ࠠࡢࠢ࡯࡭ࡳࡱ࠮࠯ࠩિ"),l1111lllUK_Turk_No1)
	if select < 0:quit()
	else:
		url = l111l1llUK_Turk_No1[select]
		l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
def l1ll11llUK_Turk_No1(url):
    string = l11l1lUK_Turk_No1 (u"ࠣࡕ࡫ࡳࡼࡖࡩࡤࡶࡸࡶࡪ࠮ࠥࡴࠫࠥી") %url
    xbmc.executebuiltin(string)
def l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        try:
                if l11l1lUK_Turk_No1 (u"ࠩࡶࡳࡵࡀ࠯࠰ࠩુ")in url:
                        url = urllib.quote(url)
                        url=l11l1lUK_Turk_No1 (u"ࠪࡴࡱࡻࡧࡪࡰ࠽࠳࠴ࡶࡲࡰࡩࡵࡥࡲ࠴ࡰ࡭ࡧࡻࡹࡸ࠵࠿࡮ࡱࡧࡩࡂ࠸ࠦࡶࡴ࡯ࡁࠪࡹࠦ࡯ࡣࡰࡩࡂࠫࡳࠨૂ")%(url,name.replace(l11l1lUK_Turk_No1 (u"ࠫࠥ࠭ૃ"),l11l1lUK_Turk_No1 (u"ࠬ࠱ࠧૄ")))
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"࠭ࡡࡤࡧࡶࡸࡷ࡫ࡡ࡮࠼࠲࠳ࠬૅ") in url or l11l1lUK_Turk_No1 (u"ࠧ࠯ࡣࡦࡩࡱ࡯ࡶࡦࠩ૆") in url:
                        url = urllib.quote(url)
                        url=l11l1lUK_Turk_No1 (u"ࠨࡲ࡯ࡹ࡬࡯࡮࠻࠱࠲ࡴࡷࡵࡧࡳࡣࡰ࠲ࡵࡲࡥࡹࡷࡶ࠳ࡄࡳ࡯ࡥࡧࡀ࠵ࠫࡻࡲ࡭࠿ࠨࡷࠫࡴࡡ࡮ࡧࡀࠩࡸ࠭ે")%(url,name.replace(l11l1lUK_Turk_No1 (u"ࠩࠣࠫૈ"),l11l1lUK_Turk_No1 (u"ࠪ࠯ࠬૉ")))
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠾࠴࠵ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳࡙ࡰࡰࡴࡷࡷࡉ࡫ࡶࡪ࡮࠲ࠫ૊") in url:
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif l11l1lUK_Turk_No1 (u"ࠬ࠴ࡴࡴࠩો")in url:
                        url = l11l1lUK_Turk_No1 (u"࠭ࡰ࡭ࡷࡪ࡭ࡳࡀ࠯࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡸ࡬ࡨࡪࡵ࠮ࡧ࠶ࡰࡘࡪࡹࡴࡦࡴ࠲ࡃࡸࡺࡲࡦࡣࡰࡸࡾࡶࡥ࠾ࡖࡖࡈࡔ࡝ࡎࡍࡑࡄࡈࡊࡘࠦࡢ࡯ࡳ࠿ࡳࡧ࡭ࡦ࠿ࠪૌ")+name+l11l1lUK_Turk_No1 (u"ࠧࠧࡣࡰࡴࡀࡻࡲ࡭࠿્ࠪ")+url
                        l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif urlresolver.HostedMediaFile(url).valid_url():
                        url = urlresolver.HostedMediaFile(url).resolve()
                        l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                elif liveresolver.isValid(url)==True:
                        url=liveresolver.resolve(url)
                        l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
                else:l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
        except:
                notification(l11l1lUK_Turk_No1 (u"ࠨࡗࡎࡘࡺࡸ࡫ࠨ૎"),l11l1lUK_Turk_No1 (u"ࠩࡖࡸࡷ࡫ࡡ࡮ࠢࡘࡲࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠧ૏"), l11l1lUK_Turk_No1 (u"ࠪ࠷࠵࠶࠰ࠨૐ"), icon)
def l11111l11UK_Turk_No1(url):
        if urlresolver.HostedMediaFile(url).valid_url():
                url = urlresolver.HostedMediaFile(url).resolve()
        xbmc.Player ().play(url)
def l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l1l11l11UK_Turk_No1,thumbnailImage=l1l11l11UK_Turk_No1); l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"࡛ࠦ࡯ࡤࡦࡱࠥ૑"), infoLabels={ l11l1lUK_Turk_No1 (u"࡚ࠧࡩࡵ࡮ࡨࠦ૒"): name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l111l1lUK_Turk_No1)
        l111l1lUK_Turk_No1.setPath(str(url))
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, l111l1lUK_Turk_No1)
def l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"࠭ࡄࡪࡣ࡯ࡳ࡬࠴ࡃ࡭ࡱࡶࡩ࠭ࡧ࡬࡭࠮ࡗࡶࡺ࡫ࠩࠨ૓"))
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦ૔"), thumbnailImage=l1l11l11UK_Turk_No1); l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"ࠣࡘ࡬ࡨࡪࡵࠢ૕"), infoLabels={ l11l1lUK_Turk_No1 (u"ࠤࡗ࡭ࡹࡲࡥࠣ૖"): name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=l111l1lUK_Turk_No1)
        xbmc.Player ().play(url, l111l1lUK_Turk_No1, False)
def l111ll1lUK_Turk_No1(url):
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠥࡔࡱࡧࡹࡎࡧࡧ࡭ࡦ࠮ࠥࡴࠫࠥ૗")%url)
def l1llll1UK_Turk_No1(url):
        display=l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠫࡱࡧࡹࡰࡷࡷࠫ૘"))
        if display==l11l1lUK_Turk_No1 (u"ࠬࡒࡩࡴࡶࡨࡶࡸ࠭૙"):l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭࡬ࡢࡻࡲࡹࡹ࠭૚"),l11l1lUK_Turk_No1 (u"ࠧࡄࡣࡷࡩ࡬ࡵࡲࡺࠩ૛"))
        else:l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠨ࡮ࡤࡽࡴࡻࡴࠨ૜"),l11l1lUK_Turk_No1 (u"ࠩࡏ࡭ࡸࡺࡥࡳࡵࠪ૝"))
        xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠪࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡒࡦࡨࡵࡩࡸ࡮ࠧ૞"))
def l1llll111UK_Turk_No1(url):
        link = net.http_GET(url).content
        link=link.replace(l11l1lUK_Turk_No1 (u"ࠫࡁ࠵ࡦࡢࡰࡤࡶࡹࡄࠧ૟"),l11l1lUK_Turk_No1 (u"ࠬࡂࡦࡢࡰࡤࡶࡹࡄࡸ࠽࠱ࡩࡥࡳࡧࡲࡵࡀࠪૠ")).replace(l11l1lUK_Turk_No1 (u"࠭࠼ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࡀ࠴ࡺࡨࡶ࡯ࡥࡲࡦ࡯࡬࠿ࠩૡ"),l11l1lUK_Turk_No1 (u"ࠧ࠽ࡶ࡫ࡹࡲࡨ࡮ࡢ࡫࡯ࡂࡽࡂ࠯ࡵࡪࡸࡱࡧࡴࡡࡪ࡮ࡁࠫૢ")).replace(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡸࡸࡺࡨࡥ࠿ࠩૣ"),l11l1lUK_Turk_No1 (u"ࠩ࠿ࡰ࡮ࡴ࡫࠿ࡪࡷࡸࡵࡹ࠺࠰࠱ࡺࡻࡼ࠴ࡹࡰࡷࡷࡹࡧ࡫࠮ࡤࡱࡰ࠳ࡼࡧࡴࡤࡪࡂࡺࡂ࠭૤")).replace(l11l1lUK_Turk_No1 (u"ࠪࡀ࠴ࡻࡴࡶࡤࡨࡂࠬ૥"),l11l1lUK_Turk_No1 (u"ࠫࡁ࠵࡬ࡪࡰ࡮ࡂࠬ૦"))#.replace(l11l1lUK_Turk_No1 (u"ࠬࡄ࠼࠰ࠩ૧"),l11l1lUK_Turk_No1 (u"࠭࠾ࡹ࠾࠲ࠫ૨"))
        if l11l1lUK_Turk_No1 (u"ࠧ࠱࠸࠳࠵࠵࠻ࠧ૩") in link:link=decode(link)
        return link
def l1ll111llUK_Turk_No1():
        param=[]
        l1ll1lll1UK_Turk_No1=sys.argv[2]
        if len(l1ll1lll1UK_Turk_No1)>=2:
                params=sys.argv[2]
                l1111ll1UK_Turk_No1=params.replace(l11l1lUK_Turk_No1 (u"ࠨࡁࠪ૪"),l11l1lUK_Turk_No1 (u"ࠩࠪ૫"))
                if (params[len(params)-1]==l11l1lUK_Turk_No1 (u"ࠪ࠳ࠬ૬")):
                        params=params[0:len(params)-2]
                l11UK_Turk_No1=l1111ll1UK_Turk_No1.split(l11l1lUK_Turk_No1 (u"ࠫࠫ࠭૭"))
                param={}
                for i in range(len(l11UK_Turk_No1)):
                        l11l11UK_Turk_No1={}
                        l11l11UK_Turk_No1=l11UK_Turk_No1[i].split(l11l1lUK_Turk_No1 (u"ࠬࡃࠧ૮"))
                        if (len(l11l11UK_Turk_No1))==2:
                                param[l11l11UK_Turk_No1[0]]=l11l11UK_Turk_No1[1]
        return param
params=l1ll111llUK_Turk_No1(); url=None; name=None; mode=None; l11lll1l1UK_Turk_No1=None; l1l11l11UK_Turk_No1=None
try: l11lll1l1UK_Turk_No1=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠨࡳࡪࡶࡨࠦ૯")])
except: pass
try: url=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠢࡶࡴ࡯ࠦ૰")])
except: pass
try: name=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠣࡰࡤࡱࡪࠨ૱")])
except: pass
try: mode=int(params[l11l1lUK_Turk_No1 (u"ࠤࡰࡳࡩ࡫ࠢ૲")])
except: pass
try: l1l11l11UK_Turk_No1=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠥ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࠨ૳")])
except: pass
try: fanart=urllib.unquote_plus(params[l11l1lUK_Turk_No1 (u"ࠦ࡫ࡧ࡮ࡢࡴࡷࠦ૴")])
except: pass
try: description=urllib.unquote_plus([l11l1lUK_Turk_No1 (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥ૵")])
except: pass
def notification(title, message, l1l11l111UK_Turk_No1, l11l1l1l1UK_Turk_No1):
    xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡘࡃࡏࡆ࠲ࡳࡵࡴࡪࡨ࡬ࡧࡦࡺࡩࡰࡰࠫࠦ૶") + title + l11l1lUK_Turk_No1 (u"ࠢ࠭ࠤ૷") + message + l11l1lUK_Turk_No1 (u"ࠣ࠮ࠥ૸") + l1l11l111UK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠤ࠯ࠦૹ") + l11l1l1l1UK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠥ࠭ࠧૺ"))
def l1llllUK_Turk_No1(string):
        l11l1l1lUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡡࡡࠨ࠯࠭ࡂ࠭ࡡࡣࠧૻ")).findall(string)
        for tag in l11l1l1lUK_Turk_No1:string=string.replace(tag,l11l1lUK_Turk_No1 (u"ࠬ࠭ૼ")).replace(l11l1lUK_Turk_No1 (u"࡛࠭࠰࡟ࠪ૽"),l11l1lUK_Turk_No1 (u"ࠧࠨ૾")).replace(l11l1lUK_Turk_No1 (u"ࠨ࡝ࡠࠫ૿"),l11l1lUK_Turk_No1 (u"ࠩࠪ଀"))
        return string
def l1l11lll1UK_Turk_No1(string):
        string=string.split(l11l1lUK_Turk_No1 (u"ࠪࠤࠬଁ"))
        final=l11l1lUK_Turk_No1 (u"ࠫࠬଂ")
        for l1111llllUK_Turk_No1 in string:
            l1111l1l1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢ࠭ଃ")+l1111llllUK_Turk_No1[0].upper()+l11l1lUK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠧ଄")+l1111llllUK_Turk_No1[1:]+l11l1lUK_Turk_No1 (u"ࠧ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࠦࠧଅ")
            final=final+l1111l1l1UK_Turk_No1
        return final
def l1l11UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,l11lll11UK_Turk_No1,isFolder=False):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠨࠢࠪଆ"),l11l1lUK_Turk_No1 (u"ࠩࠨ࠶࠵࠭ଇ"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠪࠤࠬଈ"),l11l1lUK_Turk_No1 (u"ࠫࠪ࠸࠰ࠨଉ"))
	if metaset==l11l1lUK_Turk_No1 (u"ࠬࡺࡲࡶࡧࠪଊ"):
	  if not l11l1lUK_Turk_No1 (u"࠭ࡃࡐࡎࡒࡖࠬଋ") in name:
	    l111l11llUK_Turk_No1=name.partition(l11l1lUK_Turk_No1 (u"ࠧࠩࠩଌ"))
	    l1ll1UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠣࠤ଍")
	    l1l1l1lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠤࠥ଎")
	    if len(l111l11llUK_Turk_No1)>0:
		l1ll1UK_Turk_No1=l111l11llUK_Turk_No1[0]
		l1l1l1lUK_Turk_No1=l111l11llUK_Turk_No1[2].partition(l11l1lUK_Turk_No1 (u"ࠪ࠭ࠬଏ"))
	    if len(l1l1l1lUK_Turk_No1)>0:
		l1l1l1lUK_Turk_No1=l1l1l1lUK_Turk_No1[0]
            mg = eval(base64.b64decode(l11l1lUK_Turk_No1 (u"ࠫࡧ࡝ࡖ࠱࡛࡚࡬࡭ࡨ࡭ࡓࡵ࡝࡜ࡏࢀࡌ࡬࠳࡯ࡨࡌࡌࡅ࡚࡚ࡕ࡬ࡐࡎࡒࡵ࡜ࡊࡎ࡫࡟ࡘࡃࡲ࡛࠶ࡹࡲࡥࡕ࠲࡬࡞࡜ࡔࡩ࡚ࡼࡪ࠶࡞ࢀ࡫ࡺ࡜ࡊࡉࡾࡓࡺࡥ࡬࡜࡮ࡱࡳ࡙ࡘ࡜ࡰࡒࡲࡗࡺ࡛ࡉࡕ࡮ࡓࡍࡊ࡭ࡐࡰࡕ࡮ࡑࡑ࠾࠿ࠪଐ")))
	    meta = mg.get_meta(l11l1lUK_Turk_No1 (u"ࠬࡳ࡯ࡷ࡫ࡨࠫ଑"), name=l1ll1UK_Turk_No1 ,year=l1l1l1lUK_Turk_No1)
	    u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠨ࠿ࡶࡴ࡯ࡁࠧ଒")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠢࠧࡵ࡬ࡸࡪࡃࠢଓ")+str(l11lll1l1UK_Turk_No1)+l11l1lUK_Turk_No1 (u"ࠣࠨࡰࡳࡩ࡫࠽ࠣଔ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤକ")+urllib.quote_plus(name)
	    ok=True
	    l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=meta[l11l1lUK_Turk_No1 (u"ࠪࡧࡴࡼࡥࡳࡡࡸࡶࡱ࠭ଖ")], thumbnailImage=meta[l11l1lUK_Turk_No1 (u"ࠫࡨࡵࡶࡦࡴࡢࡹࡷࡲࠧଗ")])
	    l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"ࠧ࡜ࡩࡥࡧࡲࠦଘ"), infoLabels= meta )
	    l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡉࡴࡒ࡯ࡥࡾࡧࡢ࡭ࡧࠥଙ"),l11l1lUK_Turk_No1 (u"ࠢࡵࡴࡸࡩࠧଚ"))
	    l1l11llUK_Turk_No1=[]
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡺࠬଛ"))==l11l1lUK_Turk_No1 (u"ࠩࡼࡩࡸ࠭ଜ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝ࡓࡧࡰࡳࡻ࡫ࠠࡧࡴࡲࡱ࡛ࠥࡋࠡࡖࡸࡶࡰࠦࡆࡢࡸࡲࡹࡷ࡯ࡴࡦࡵ࡞࠳ࡈࡕࡌࡐࡔࡠࠫଝ"),l11l1lUK_Turk_No1 (u"ࠫ࡝ࡈࡍࡄ࠰ࡕࡹࡳࡖ࡬ࡶࡩ࡬ࡲ࠭ࠫࡳࡀ࡯ࡲࡨࡪࡃ࠱࠵ࠨࡱࡥࡲ࡫࠽ࠦࡵࠩࡹࡷࡲ࠽ࠦࡵࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠥࡴࠫࠪଞ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩଟ"))==l11l1lUK_Turk_No1 (u"࠭࡮ࡰࠩଠ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࡁࡥࡦࠣࡸࡴࠦࡕࡌࠢࡗࡹࡷࡱࠠࡇࡣࡹࡳࡺࡸࡩࡵࡧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࠬଡ"),l11l1lUK_Turk_No1 (u"ࠨ࡚ࡅࡑࡈ࠴ࡒࡶࡰࡓࡰࡺ࡭ࡩ࡯ࠪࠨࡷࡄࡳ࡯ࡥࡧࡀ࠵࠷ࠬ࡮ࡢ࡯ࡨࡁࠪࡹࠦࡶࡴ࡯ࡁࠪࡹࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠩࡸ࠯ࠧଢ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
	    if not meta[l11l1lUK_Turk_No1 (u"ࠩࡥࡥࡨࡱࡤࡳࡱࡳࡣࡺࡸ࡬ࠨଣ")] == l11l1lUK_Turk_No1 (u"ࠪࠫତ"): l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪଥ"), meta[l11l1lUK_Turk_No1 (u"ࠬࡨࡡࡤ࡭ࡧࡶࡴࡶ࡟ࡶࡴ࡯ࠫଦ")])
	    else: l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬଧ"), fanart)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=isFolder,totalItems=l11lll11UK_Turk_No1)
	    return ok
	else:
	    u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠢࡀࡷࡵࡰࡂࠨନ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠣࠨࡶ࡭ࡹ࡫࠽ࠣ଩")+str(l11lll1l1UK_Turk_No1)+l11l1lUK_Turk_No1 (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤପ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥଫ")+urllib.quote_plus(name)
	    ok=True
	    l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l1l11l11UK_Turk_No1, thumbnailImage=l1l11l11UK_Turk_No1)
	    l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"࡛ࠦ࡯ࡤࡦࡱࠥବ"), infoLabels={ l11l1lUK_Turk_No1 (u"࡚ࠧࡩࡵ࡮ࡨࠦଭ"): name } )
	    l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬମ"), fanart)
	    l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠢࡊࡵࡓࡰࡦࡿࡡࡣ࡮ࡨࠦଯ"),l11l1lUK_Turk_No1 (u"ࠣࡶࡵࡹࡪࠨର"))
	    l1l11llUK_Turk_No1=[]
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡻ࠭଱"))==l11l1lUK_Turk_No1 (u"ࠪࡽࡪࡹࠧଲ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡔࡨࡱࡴࡼࡥࠡࡨࡵࡳࡲࠦࡕࡌࠢࡗࡹࡷࡱࠠࡇࡣࡹࡳࡺࡸࡩࡵࡧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࠬଳ"),l11l1lUK_Turk_No1 (u"ࠬ࡞ࡂࡎࡅ࠱ࡖࡺࡴࡐ࡭ࡷࡪ࡭ࡳ࠮ࠥࡴࡁࡰࡳࡩ࡫࠽࠲࠶ࠩࡲࡦࡳࡥ࠾ࠧࡶࠪࡺࡸ࡬࠾ࠧࡶࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠦࡵࠬࠫ଴")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡸࠪଵ"))==l11l1lUK_Turk_No1 (u"ࠧ࡯ࡱࠪଶ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࡂࡦࡧࠤࡹࡵࠠࡖࡍࠣࡘࡺࡸ࡫ࠡࡈࡤࡺࡴࡻࡲࡪࡶࡨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ଷ"),l11l1lUK_Turk_No1 (u"࡛ࠩࡆࡒࡉ࠮ࡓࡷࡱࡔࡱࡻࡧࡪࡰࠫࠩࡸࡅ࡭ࡰࡦࡨࡁ࠶࠸ࠦ࡯ࡣࡰࡩࡂࠫࡳࠧࡷࡵࡰࡂࠫࡳࠧ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࡁࠪࡹࠩࠨସ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
            l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
	    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=isFolder)
	    return ok
def l1l11111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫହ")):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠫࠥ࠭଺"),l11l1lUK_Turk_No1 (u"ࠬࠫ࠲࠱ࠩ଻"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"࠭ࠠࠨ଼"),l11l1lUK_Turk_No1 (u"ࠧࠦ࠴࠳ࠫଽ"))
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠣࡁࡸࡶࡱࡃࠢା")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤି")+str(mode)+l11l1lUK_Turk_No1 (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥୀ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠦࠫࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࡀࠦୁ")+str(description)+l11l1lUK_Turk_No1 (u"ࠧࠬࡦࡢࡰࡤࡶࡹࡃࠢୂ")+urllib.quote_plus(fanart)+l11l1lUK_Turk_No1 (u"ࠨࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠦୃ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦୄ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setInfo( type=l11l1lUK_Turk_No1 (u"ࠣࡘ࡬ࡨࡪࡵࠢ୅"), infoLabels={ l11l1lUK_Turk_No1 (u"ࠤࡗ࡭ࡹࡲࡥࠣ୆"): name, l11l1lUK_Turk_No1 (u"ࠪࡴࡱࡵࡴࠨେ"): description } )
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪୈ"), fanart)
        l1l11llUK_Turk_No1=[]
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩ୉"))==l11l1lUK_Turk_No1 (u"࠭ࡹࡦࡵࠪ୊"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡗ࡫࡭ࡰࡸࡨࠤ࡫ࡸ࡯࡮ࠢࡘࡏ࡚ࠥࡵࡳ࡭ࠣࡊࡦࡼ࡯ࡶࡴ࡬ࡸࡪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨୋ"),l11l1lUK_Turk_No1 (u"ࠨ࡚ࡅࡑࡈ࠴ࡒࡶࡰࡓࡰࡺ࡭ࡩ࡯ࠪࠨࡷࡄࡳ࡯ࡥࡧࡀ࠵࠹ࠬ࡮ࡢ࡯ࡨࡁࠪࡹࠦࡶࡴ࡯ࡁࠪࡹࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠩࡸ࠯ࠧୌ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡻ୍࠭"))==l11l1lUK_Turk_No1 (u"ࠪࡲࡴ࠭୎"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡅࡩࡪࠠࡵࡱ࡙ࠣࡐࠦࡔࡶࡴ࡮ࠤࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ୏"),l11l1lUK_Turk_No1 (u"ࠬ࡞ࡂࡎࡅ࠱ࡖࡺࡴࡐ࡭ࡷࡪ࡭ࡳ࠮ࠥࡴࡁࡰࡳࡩ࡫࠽࠲࠴ࠩࡲࡦࡳࡥ࠾ࠧࡶࠪࡺࡸ࡬࠾ࠧࡶࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠦࡵࠬࠫ୐")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
        if l11l1lUK_Turk_No1 (u"࠭ࡰ࡭ࡷࡪ࡭ࡳࡀ࠯࠰ࠩ୑") in url:
                u=url
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=True)
        return ok
def l11l1llUK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨ୒")):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠨࠢࠪ୓"),l11l1lUK_Turk_No1 (u"ࠩࠨ࠶࠵࠭୔"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠪࠤࠬ୕"),l11l1lUK_Turk_No1 (u"ࠫࠪ࠸࠰ࠨୖ"))
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠧࡅࡵࡳ࡮ࡀࠦୗ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨ୘")+str(mode)+l11l1lUK_Turk_No1 (u"ࠢࠧࡰࡤࡱࡪࡃࠢ୙")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠣࠨࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴ࠽ࠣ୚")+str(description)+l11l1lUK_Turk_No1 (u"ࠤࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠢ୛")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠥࡈࡪ࡬ࡡࡶ࡮ࡷࡊࡴࡲࡤࡦࡴ࠱ࡴࡳ࡭ࠢଡ଼"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪଢ଼"), fanart)
        l1l11llUK_Turk_No1=[]
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬ࡬ࡡࡷࠩ୞"))==l11l1lUK_Turk_No1 (u"࠭ࡹࡦࡵࠪୟ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡗ࡫࡭ࡰࡸࡨࠤ࡫ࡸ࡯࡮ࠢࡘࡏ࡚ࠥࡵࡳ࡭ࠣࡊࡦࡼ࡯ࡶࡴ࡬ࡸࡪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨୠ"),l11l1lUK_Turk_No1 (u"ࠨ࡚ࡅࡑࡈ࠴ࡒࡶࡰࡓࡰࡺ࡭ࡩ࡯ࠪࠨࡷࡄࡳ࡯ࡥࡧࡀ࠵࠹ࠬ࡮ࡢ࡯ࡨࡁࠪࡹࠦࡶࡴ࡯ࡁࠪࡹࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠩࡸ࠯ࠧୡ")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡻ࠭ୢ"))==l11l1lUK_Turk_No1 (u"ࠪࡲࡴ࠭ୣ"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡅࡩࡪࠠࡵࡱ࡙ࠣࡐࠦࡔࡶࡴ࡮ࠤࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ୤"),l11l1lUK_Turk_No1 (u"ࠬ࡞ࡂࡎࡅ࠱ࡖࡺࡴࡐ࡭ࡷࡪ࡭ࡳ࠮ࠥࡴࡁࡰࡳࡩ࡫࠽࠲࠴ࠩࡲࡦࡳࡥ࠾ࠧࡶࠪࡺࡸ࡬࠾ࠧࡶࠪ࡮ࡩ࡯࡯࡫ࡰࡥ࡬࡫࠽ࠦࡵࠬࠫ୥")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧ୦")):
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠧࠡࠩ୧"),l11l1lUK_Turk_No1 (u"ࠨࠧ࠵࠴ࠬ୨"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ࠩࠣࠫ୩"),l11l1lUK_Turk_No1 (u"ࠪࠩ࠷࠶ࠧ୪"))
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠦࡄࡻࡲ࡭࠿ࠥ୫")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠧࠬ࡭ࡰࡦࡨࡁࠧ୬")+str(mode)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡯ࡣࡰࡩࡂࠨ୭")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠢࠧࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࡃࠢ୮")+str(description)+l11l1lUK_Turk_No1 (u"ࠣࠨ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࡂࠨ୯")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠤࡇࡩ࡫ࡧࡵ࡭ࡶࡉࡳࡱࡪࡥࡳ࠰ࡳࡲ࡬ࠨ୰"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡴࡡࡳࡶࡢ࡭ࡲࡧࡧࡦࠩୱ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠦࡎࡹࡐ࡭ࡣࡼࡥࡧࡲࡥࠣ୲"),l11l1lUK_Turk_No1 (u"ࠧࡺࡲࡶࡧࠥ୳"))
        l1l11llUK_Turk_No1=[]
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡸࠪ୴"))==l11l1lUK_Turk_No1 (u"ࠧࡺࡧࡶࠫ୵"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡘࡥ࡮ࡱࡹࡩࠥ࡬ࡲࡰ࡯࡙ࠣࡐࠦࡔࡶࡴ࡮ࠤࡋࡧࡶࡰࡷࡵ࡭ࡹ࡫ࡳ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩ୶"),l11l1lUK_Turk_No1 (u"࡛ࠩࡆࡒࡉ࠮ࡓࡷࡱࡔࡱࡻࡧࡪࡰࠫࠩࡸࡅ࡭ࡰࡦࡨࡁ࠶࠺ࠦ࡯ࡣࡰࡩࡂࠫࡳࠧࡷࡵࡰࡂࠫࡳࠧ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࡁࠪࡹࠩࠨ୷")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        if l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡼࠧ୸"))==l11l1lUK_Turk_No1 (u"ࠫࡳࡵࠧ୹"):l1l11llUK_Turk_No1.append((l11l1lUK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࡆࡪࡤࠡࡶࡲࠤ࡚ࡑࠠࡕࡷࡵ࡯ࠥࡌࡡࡷࡱࡸࡶ࡮ࡺࡥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ୺"),l11l1lUK_Turk_No1 (u"࠭ࡘࡃࡏࡆ࠲ࡗࡻ࡮ࡑ࡮ࡸ࡫࡮ࡴࠨࠦࡵࡂࡱࡴࡪࡥ࠾࠳࠵ࠪࡳࡧ࡭ࡦ࠿ࠨࡷࠫࡻࡲ࡭࠿ࠨࡷࠫ࡯ࡣࡰࡰ࡬ࡱࡦ࡭ࡥ࠾ࠧࡶ࠭ࠬ୻")% (sys.argv[0],name,url,l1l11l11UK_Turk_No1)))
        l111l1lUK_Turk_No1.addContextMenuItems(l1l11llUK_Turk_No1, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok
def popup(url,name):
        message=l1llll111UK_Turk_No1(url)
        if len(message)>1:
                path = l1lll1UK_Turk_No1
                l1l1ll11UK_Turk_No1 = os.path.join(os.path.join(path,l11l1lUK_Turk_No1 (u"ࠧࠨ୼")), name+l11l1lUK_Turk_No1 (u"ࠨ࠰ࡷࡼࡹ࠭୽"))
                if not os.path.exists(l1l1ll11UK_Turk_No1):
                    file(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠩࡺࠫ୾")).close()
                r = open(l1l1ll11UK_Turk_No1)
                l1lll1111UK_Turk_No1 = r.read()
                if l1lll1111UK_Turk_No1 == message:pass
                else:
                        l1111l11lUK_Turk_No1(l11l1lUK_Turk_No1 (u"࡙ࠪࡐ࡚ࡵࡳ࡭ࠪ୿"), message)
                        l111ll1llUK_Turk_No1 = open(l1l1ll11UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠦࡼࠨ஀"))
                        l111ll1llUK_Turk_No1.write(message)
                        l111ll1llUK_Turk_No1.close()
def l1111l11lUK_Turk_No1(heading, text):
    id = 10147
    xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠬࡇࡣࡵ࡫ࡹࡥࡹ࡫ࡗࡪࡰࡧࡳࡼ࠮ࠥࡥࠫࠪ஁") % id)
    xbmc.sleep(500)
    win = xbmcgui.Window(id)
    retry = 50
    while (retry > 0):
	try:
	    xbmc.sleep(10)
	    retry -= 1
	    win.getControl(1).setLabel(heading)
	    win.getControl(5).setText(text)
	    return
	except:
	    pass
def l11ll111lUK_Turk_No1(name):
        global l1111lUK_Turk_No1
        global l1ll1ll1UK_Turk_No1
        global l1lllll1UK_Turk_No1
        global window
        global l1llll11UK_Turk_No1
        global images
        l1l1ll11UK_Turk_No1 = os.path.join(os.path.join(l1lll1UK_Turk_No1,l11l1lUK_Turk_No1 (u"࠭ࠧஂ")), name+l11l1lUK_Turk_No1 (u"ࠧ࠯ࡶࡻࡸࠬஃ"))
        r = open(l1l1ll11UK_Turk_No1)
        l1lll1111UK_Turk_No1 = r.read()
        images=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾࡬ࡱࡦ࡭ࡥ࠿ࠪ࠱࠯ࡄ࠯࠼࠰࡫ࡰࡥ࡬࡫࠾ࠨ஄")).findall(l1lll1111UK_Turk_No1)
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠩࡳࡳࡸ࠭அ"),l11l1lUK_Turk_No1 (u"ࠪ࠴ࠬஆ"))
	window= pyxbmct.AddonDialogWindow(l11l1lUK_Turk_No1 (u"ࠫࠬஇ"))
        l1l1llll1UK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠬ࠵ࡲࡦࡵࡲࡹࡷࡩࡥࡴ࠱ࡤࡶࡹ࠭ஈ")
        l1lllUK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"࠭ࡳࡱࡧࡦ࡭ࡦࡲ࠺࠰࠱࡫ࡳࡲ࡫࠯ࡢࡦࡧࡳࡳࡹ࠯ࠨஉ") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠧ࡯ࡧࡻࡸࡤ࡬࡯ࡤࡷࡶ࠲ࡵࡴࡧࠨஊ")))
        l11l111UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠨࡵࡳࡩࡨ࡯ࡡ࡭࠼࠲࠳࡭ࡵ࡭ࡦ࠱ࡤࡨࡩࡵ࡮ࡴ࠱ࠪ஋") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠩࡱࡩࡽࡺ࠱࠯ࡲࡱ࡫ࠬ஌")))
        l1UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠪࡷࡵ࡫ࡣࡪࡣ࡯࠾࠴࠵ࡨࡰ࡯ࡨ࠳ࡦࡪࡤࡰࡰࡶ࠳ࠬ஍") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠫࡵࡸࡥࡷ࡫ࡲࡹࡸࡥࡦࡰࡥࡸࡷ࠳ࡶ࡮ࡨࠩஎ")))
        l1lll11UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠬࡹࡰࡦࡥ࡬ࡥࡱࡀ࠯࠰ࡪࡲࡱࡪ࠵ࡡࡥࡦࡲࡲࡸ࠵ࠧஏ") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"࠭ࡰࡳࡧࡹ࡭ࡴࡻࡳ࠯ࡲࡱ࡫ࠬஐ")))
        l1ll1lllUK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠧࡴࡲࡨࡧ࡮ࡧ࡬࠻࠱࠲࡬ࡴࡳࡥ࠰ࡣࡧࡨࡴࡴࡳ࠰ࠩ஑") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠨࡥ࡯ࡳࡸ࡫࡟ࡧࡱࡦࡹࡸ࠴ࡰ࡯ࡩࠪஒ")))
        l111l11lUK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠩࡶࡴࡪࡩࡩࡢ࡮࠽࠳࠴࡮࡯࡮ࡧ࠲ࡥࡩࡪ࡯࡯ࡵ࠲ࠫஓ") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠪࡧࡱࡵࡳࡦ࠰ࡳࡲ࡬࠭ஔ")))
        l11ll1l11UK_Turk_No1 = xbmc.translatePath(os.path.join(l11l1lUK_Turk_No1 (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷ࠴࠭க") + addon_id + l1l1llll1UK_Turk_No1, l11l1lUK_Turk_No1 (u"ࠬࡳࡡࡪࡰ࠰ࡦ࡬࠷࠮ࡱࡰࡪࠫ஖")))
        window.setGeometry(1300, 720, 100, 50)
        background=pyxbmct.Image(l11ll1l11UK_Turk_No1)
        window.placeControl(background, -10, -10, 130, 70)
        text = l11l1lUK_Turk_No1 (u"࠭࠰ࡹࡈࡉ࠴࠵࠶࠰࠱࠲ࠪ஗")
	l1lllll1UK_Turk_No1 = pyxbmct.Button(l11l1lUK_Turk_No1 (u"ࠧࠨ஘"),focusTexture=l1UK_Turk_No1,noFocusTexture=l1lll11UK_Turk_No1,textColor=text,focusedColor=text)
	l1ll1ll1UK_Turk_No1 = pyxbmct.Button(l11l1lUK_Turk_No1 (u"ࠨࠩங"),focusTexture=l1lllUK_Turk_No1,noFocusTexture=l11l111UK_Turk_No1,textColor=text,focusedColor=text)
	l1llll11UK_Turk_No1 = pyxbmct.Button(l11l1lUK_Turk_No1 (u"ࠩࠪச"),focusTexture=l1ll1lllUK_Turk_No1,noFocusTexture=l111l11lUK_Turk_No1,textColor=text,focusedColor=text)
	l1111lUK_Turk_No1=pyxbmct.Image(images[0], aspectRatio=1)
	window.placeControl(l1lllll1UK_Turk_No1 ,102, 1,  10, 10)
	window.placeControl(l1ll1ll1UK_Turk_No1 ,102, 40, 10, 10)
	window.placeControl(l1llll11UK_Turk_No1 ,102, 21, 10, 10)
	window.placeControl(l1111lUK_Turk_No1, 0, 0, 100, 50)
	l1lllll1UK_Turk_No1.controlRight(l1ll1ll1UK_Turk_No1)
	l1lllll1UK_Turk_No1.controlUp(l1llll11UK_Turk_No1)
	window.connect(l1lllll1UK_Turk_No1,l1llllllUK_Turk_No1)
	window.connect(l1ll1ll1UK_Turk_No1,l1l1ll1l1UK_Turk_No1)
	l1lllll1UK_Turk_No1.l111l111UK_Turk_No1(False)
        window.setFocus(l1llll11UK_Turk_No1)
        l1lllll1UK_Turk_No1.controlRight(l1llll11UK_Turk_No1)
        l1llll11UK_Turk_No1.controlLeft(l1lllll1UK_Turk_No1)
        l1llll11UK_Turk_No1.controlRight(l1ll1ll1UK_Turk_No1)
        l1ll1ll1UK_Turk_No1.controlLeft(l1llll11UK_Turk_No1)
	window.connect(l1llll11UK_Turk_No1, window.close)
	window.doModal()
	del window
def l1l1ll1l1UK_Turk_No1():
        l1l1l1UK_Turk_No1=int(l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠪࡴࡴࡹࠧ஛")))
        l1l11111lUK_Turk_No1=int(l1l1l1UK_Turk_No1)+1
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠫࡵࡵࡳࠨஜ"),str(l1l11111lUK_Turk_No1))
        l111111llUK_Turk_No1=len(images)
        l1111lUK_Turk_No1.setImage(images[int(l1l11111lUK_Turk_No1)])
        l1lllll1UK_Turk_No1.l111l111UK_Turk_No1(True)
        if int(l1l11111lUK_Turk_No1) ==int(l111111llUK_Turk_No1)-1:
                l1ll1ll1UK_Turk_No1.l111l111UK_Turk_No1(False)
def l1llllllUK_Turk_No1():
        l1l1l1UK_Turk_No1=int(l1l1111lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬࡶ࡯ࡴࠩ஝")))
        l11l1l1UK_Turk_No1=int(l1l1l1UK_Turk_No1)-1
        l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"࠭ࡰࡰࡵࠪஞ"),str(l11l1l1UK_Turk_No1))
        l1111lUK_Turk_No1.setImage(images[int(l11l1l1UK_Turk_No1)])
        l1ll1ll1UK_Turk_No1.l111l111UK_Turk_No1(True)
        if int(l11l1l1UK_Turk_No1) ==0:
                l1lllll1UK_Turk_No1.l111l111UK_Turk_No1(False)
def decode(s):
    l1llll11lUK_Turk_No1 = [ s[ i : i + 3] for i in range(0, len(s), 3) ]
    return l11l1lUK_Turk_No1 (u"ࠧࠨட").join( chr(int(val)) for val in l1llll11lUK_Turk_No1 )
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠣࠨࠦࡼࠧ஠"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨ஡"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩ஢"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣண"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠬࡏࡓࡐ࠯࠻࠼࠺࠿࠭࠲ࠩத")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ஥")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦ஦"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠣࡣࡶࡧ࡮࡯ࠢ஧"), l11l1lUK_Turk_No1 (u"ࠤ࡬࡫ࡳࡵࡲࡦࠤந")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩன")))
def l111lll1lUK_Turk_No1():
	if xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠫࡸࡿࡳࡵࡧࡰ࠲ࡵࡲࡡࡵࡨࡲࡶࡲ࠴ࡡ࡯ࡦࡵࡳ࡮ࡪࠧப")):
		return l11l1lUK_Turk_No1 (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭஫")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"࠭ࡳࡺࡵࡷࡩࡲ࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠯࡮࡬ࡲࡺࡾࠧ஬")):
		return l11l1lUK_Turk_No1 (u"ࠧ࡭࡫ࡱࡹࡽ࠭஭")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠨࡵࡼࡷࡹ࡫࡭࠯ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࠱ࡻ࡮ࡴࡤࡰࡹࡶࠫம")):
		return l11l1lUK_Turk_No1 (u"ࠩࡺ࡭ࡳࡪ࡯ࡸࡵࠪய")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠪࡷࡾࡹࡴࡦ࡯࠱ࡴࡱࡧࡴࡧࡱࡵࡱ࠳ࡵࡳࡹࠩர")):
		return l11l1lUK_Turk_No1 (u"ࠫࡴࡹࡸࠨற")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠬࡹࡹࡴࡶࡨࡱ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠮ࡢࡶࡹ࠶ࠬல")):
		return l11l1lUK_Turk_No1 (u"࠭ࡡࡵࡸ࠵ࠫள")
	elif xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠧࡴࡻࡶࡸࡪࡳ࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠰࡬ࡳࡸ࠭ழ")):
		return l11l1lUK_Turk_No1 (u"ࠨ࡫ࡲࡷࠬவ")
	else:
		return l11l1lUK_Turk_No1 (u"ࠩࡒࡸ࡭࡫ࡲࠨஶ")
def l11llllllUK_Turk_No1(url):
	request  = urllib2.Request(url)
	request.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧஷ"), USER_AGENT)
	response = urllib2.urlopen(request)
	link = response.read()
	response.close()
	return link
def l1ll1l1UK_Turk_No1():
	url=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡧࡤࡥࡱࡱࡧࡱࡵࡵࡥ࠰ࡲࡶ࡬࠵ࡰࡪࡰ࠱ࡴ࡭ࡶࠧஸ")
	l111ll11UK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠬࡹࡹࡴࡶࡨࡱ࠳ࡶ࡬ࡢࡶࡩࡳࡷࡳ࠮ࡸ࡫ࡱࡨࡴࡽࡳࠨஹ"))
	l1111l1UK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"࠭ࡳࡺࡵࡷࡩࡲ࠴ࡰ࡭ࡣࡷࡪࡴࡸ࡭࠯ࡱࡶࡼࠬ஺"))
	l1111llUK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠧࡴࡻࡶࡸࡪࡳ࠮ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮࠰࡯࡭ࡳࡻࡸࠨ஻"))
	l1l11l1lUK_Turk_No1 = xbmc.getCondVisibility(l11l1lUK_Turk_No1 (u"ࠨࡕࡼࡷࡹ࡫࡭࠯ࡒ࡯ࡥࡹ࡬࡯ࡳ࡯࠱ࡅࡳࡪࡲࡰ࡫ࡧࠫ஼"))
	if l1111l1UK_Turk_No1:
		# _ l11111lllUK_Turk_No1 the url with the default l11l111lUK_Turk_No1 browser
		xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠤࡖࡽࡸࡺࡥ࡮࠰ࡈࡼࡪࡩࠨࡰࡲࡨࡲࠥࠨ஽")+url+l11l1lUK_Turk_No1 (u"ࠥ࠭ࠧா"))
	elif l111ll11UK_Turk_No1:
		# _ l11111lllUK_Turk_No1 the url with the default l11l111lUK_Turk_No1 browser
		xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠦࡘࡿࡳࡵࡧࡰ࠲ࡊࡾࡥࡤࠪࡦࡱࡩ࠴ࡥࡹࡧࠣ࠳ࡨࠦࡳࡵࡣࡵࡸࠥࠨி")+url+l11l1lUK_Turk_No1 (u"ࠧ࠯ࠢீ"))
	elif l1l11l1lUK_Turk_No1:
		try:
			xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠨࡓࡵࡣࡵࡸࡆࡴࡤࡳࡱ࡬ࡨࡆࡩࡴࡪࡸ࡬ࡸࡾ࠮ࡣࡰ࡯࠱ࡥࡳࡪࡲࡰ࡫ࡧ࠲ࡨ࡮ࡲࡰ࡯ࡨ࠰ࡦࡴࡤࡳࡱ࡬ࡨ࠳࡯࡮ࡵࡧࡱࡸ࠳ࡧࡣࡵ࡫ࡲࡲ࠳࡜ࡉࡆ࡙࠯࠰ࠧு")+url+l11l1lUK_Turk_No1 (u"ࠢࠪࠤூ"))
		except:
			xbmcgui.Dialog().ok( l11l1lUK_Turk_No1 (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࠧࠡࠢࠣࠣࡅࡑࡋࡒࡕࠢࠤ࡛ࠥࠦࠧ࠰ࡅࡒࡐࡔࡘ࡝ࠨ௃"),l11l1lUK_Turk_No1 (u"ࠤ࡜ࡳࡺࡸࠠࡥࡧࡹ࡭ࡨ࡫ࠠࡥࡱࡨࡷࡳ࠭ࡴࠡࡪࡤࡺࡪࠦࡡࠡࡤࡵࡳࡼࡹࡥࡳ࠰ࠣࡔࡱ࡫ࡡࡴࡧࠣ࡭ࡳࡹࡴࡢ࡮࡯ࠤࡦࠦࡢࡳࡱࡺࡷࡪࡸࠠࡵࡪࡨࡲࠥࡻࡳࡦࠢࡷ࡬࡮ࡹࠠࡢࡦࡧࡳࡳࠨ௄"))
def l111111lUK_Turk_No1(P):
	global l1l1llUK_Turk_No1
	global l1l111lUK_Turk_No1
	if P == l11l1lUK_Turk_No1 (u"ࠥࠦ௅") :
		l1lllllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠦ࡞ࡵࡵࠡࡐࡨࡩࡩࠦࡡࠡ࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝࡜ࡄࡠࡔࡎࡔ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠥࡺ࡯ࠡࡃࡦࡧࡪࡹࡳࠡࡗࡎࠤ࡙ࡻࡲ࡬ࡵࠤࠦெ")
		msg2 = l11l1lUK_Turk_No1 (u"ࠧࡍ࡯ࠡࡶࡲࠤࡠࡉࡏࡍࡑࡕࠤࡧࡲࡵࡦ࡟࡞ࡆࡢ࡛ࡔࡑࡋࡑ࠲ࡈࡕࡍ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢࠦ࡯࡯ࠢࡼࡳࡺࡸࠠࡎࡱࡥ࡭ࡱ࡫࠯ࡑࡅࠣࡸࡴࠦࡧࡦࡶࠣࡽࡴࡻࡲࠡࡒࡌࡒࠥࡴࡵ࡮ࡤࡨࡶࠥࡺࡨࡦࡰࠣࡧࡱ࡯ࡣ࡬ࠢࡲࡲࠥࡿࡥࡴࠢࡷࡳࠥ࡯࡮ࡱࡷࡷࠤࡾࡵࡵࡳࠢࡳ࡭ࡳࠦ࡯ࡳࠢࡦࡰ࡮ࡩ࡫ࠡࡱࡱࠤࡓࡵࠠࡵࡱࠣࡩࡽ࡯ࡴࠣே")
		if l1l1l111UK_Turk_No1.platform() == l11l1lUK_Turk_No1 (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧை"):
			yes = DIALOG.yesno(l11l1lUK_Turk_No1 (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࠦࠧࡃࡩࡴࡲࡱࡪࠦࡂࡳࡱࡺࡷࡪࡸࠠࡓࡧࡴࡹ࡮ࡸࡥࡥࠣࠤ࡟࠴ࡉࡏࡍࡑࡕࡡࠬ௉"), l11l1lUK_Turk_No1 (u"ࠣࡋࡩࠤࡾࡵࡵࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡻ࡫ࠠࡄࡪࡵࡳࡲ࡫ࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠣࡸ࡭࡫࡮ࠡࡥ࡯࡭ࡨࡱࠠ࡜ࡅࡒࡐࡔࡘࠠࡨࡴࡨࡩࡳࡣࡃࡰࡰࡷ࡭ࡳࡻࡥ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤொ"), l11l1lUK_Turk_No1 (u"ࠤࡇࡳࡳ࠭ࡴࠡࡪࡤࡺࡪࠦࡃࡩࡴࡲࡱࡪࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࡁࠣࡧࡱ࡯ࡣ࡬ࠢ࡞ࡇࡔࡒࡏࡓࠢࡦࡽࡦࡴ࡝ࡅࡱࡺࡲࡱࡵࡡࡥ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠥோ"), yeslabel=l11l1lUK_Turk_No1 (u"ࠥ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡣࡺࡣࡱࡡࡉࡵࡷ࡯࡮ࡲࡥࡩࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛࠰ࡄࡠࠦௌ"), nolabel=l11l1lUK_Turk_No1 (u"ࠦࡠࡈ࡝࡜ࡅࡒࡐࡔࡘࠠࡨࡴࡨࡩࡳࡣࡃࡰࡰࡷ࡭ࡳࡻࡥ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝࠲ࡆࡢࠨ்"))
			if yes:
				apkInstaller(l11l1lUK_Turk_No1 (u"ࠬࡩࡨࡳࡱࡰࡩࠬ௎"),l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡦࡧࡳࡳࡩ࡬ࡰࡷࡧ࠲ࡴࡸࡧ࠰ࡷ࡮ࡸࡺࡸ࡫࠰ࡨ࡬ࡰࡪࡹ࠯ࡤࡪࡵࡳࡲ࡫࡟ࡷ࠸࠴࠲࠵࠴࠳࠲࠸࠶࠲࠾࠾࠮ࡢࡲ࡮ࠫ௏"))
			else:
				pass
		yes_pressed = plugintools.message_yes_no(l1lllllllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠢࠡࠢࡓ࡭ࡳࠦࡁࡤࡥࡨࡷࡸࠦࡓࡺࡵࡷࡩࡲࠨௐ"), l1lllllUK_Turk_No1, msg2)
		if yes_pressed:
			l1ll1l1UK_Turk_No1()
			l1ll11l11UK_Turk_No1()
		else:
			sys.exit()
	else:
		link  = l11llllllUK_Turk_No1(l111l1111UK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠨࡁࡳ࡭ࡳࡃࠧ௑") + plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠩࡳ࡭ࡳ࠭௒")) ).replace(l11l1lUK_Turk_No1 (u"ࠪࡠࡳ࠭௓"), l11l1lUK_Turk_No1 (u"ࠫࠬ௔")).replace(l11l1lUK_Turk_No1 (u"ࠬࡢࡲࠨ௕"), l11l1lUK_Turk_No1 (u"࠭ࠧ௖"))
		total = re.compile(l11l1lUK_Turk_No1 (u"ࠧࡪࡰࡶࡸࡦࡲ࡬࠾ࠤࠫࡠࡩ࠯ࠢࠨௗ")).findall(link)
		try:
			if (str(total[0]) == l11l1lUK_Turk_No1 (u"ࠨ࠳ࠪ௘")):
				pass
		except:
			l1lllllUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡔࡎࡔࠬࠣ௙")
			msg2 = l11l1lUK_Turk_No1 (u"ࠥࡔࡷ࡫ࡳࡴࠢࡼࡩࡸࠦࡴࡰࠢࡨࡲࡹ࡫ࡲࠡࡒࡌࡒࠥࡧࡧࡢ࡫ࡱࠤࡴࡸࠠࡏࡱࠣࡸࡴࠦࡥࡹ࡫ࡷ࠲ࠧ௚")
			yes_pressed = plugintools.message_yes_no(l1lllllllUK_Turk_No1 + l11l1lUK_Turk_No1 (u"ࠦࠥࠦࡐࡪࡰࠣࡅࡨࡩࡥࡴࡵࠣࡗࡾࡹࡴࡦ࡯ࠥ௛"), l1lllllUK_Turk_No1, msg2)
			if yes_pressed:
				l1ll1l1UK_Turk_No1()
				l1ll11l11UK_Turk_No1()
			else:
				sys.exit()
def l1ll11l11UK_Turk_No1():
	l1l111ll1UK_Turk_No1()
	global P
	P = plugintools.get_setting(l11l1lUK_Turk_No1 (u"ࠬࡶࡩ࡯ࠩ௜"))
	l111111lUK_Turk_No1(P)
def l1l111ll1UK_Turk_No1():
	try:
		l1l1llUK_Turk_No1 = l1lll1llUK_Turk_No1()
		if l1l1llUK_Turk_No1 == l11l1lUK_Turk_No1 (u"ࠨࠢ௝"):
			plugintools.message(l1lllllllUK_Turk_No1, l11l1lUK_Turk_No1 (u"࡚ࠢࡱࡸࡶࠥࡶࡩ࡯ࠢࡦࡥࡳࡴ࡯ࡵࠢࡥࡩࠥ࡫࡭ࡱࡶࡼࠦ௞"))
			l1l111ll1UK_Turk_No1()
		else:
			plugintools.set_setting(l11l1lUK_Turk_No1 (u"ࠣࡲ࡬ࡲࠧ௟"), l1l1llUK_Turk_No1)
			return
	except:
		l1l111ll1UK_Turk_No1()
def l1lll1llUK_Turk_No1():
        l1lll11l1UK_Turk_No1 = xbmc.Keyboard(l11l1lUK_Turk_No1 (u"ࠩࠪ௠"), l11l1lUK_Turk_No1 (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡩࡳࡺࡥࡳࠢࡼࡳࡺࡸࠠࡱ࡫ࡱࠤ࡭࡫ࡲࡦࠩ௡"))
        l1lll11l1UK_Turk_No1.doModal()
        if (l1lll11l1UK_Turk_No1.isConfirmed()):
            l1l1UK_Turk_No1 = l1lll11l1UK_Turk_No1.getText()
            l1l1111lUK_Turk_No1.setSetting(l11l1lUK_Turk_No1 (u"ࠫࡵ࡯࡮ࠨ௢"),l1l1UK_Turk_No1)
        return l1l1UK_Turk_No1
def l1l1l11l1UK_Turk_No1(content, l11111l1lUK_Turk_No1,link):
	try:
		if (content):
			xbmcplugin.setContent(int(sys.argv[1]), content)
		if (l11l1ll1lUK_Turk_No1.getSetting(l11l1lUK_Turk_No1 (u"ࠬࡧࡵࡵࡱ࠰ࡺ࡮࡫ࡷࠨ௣")) == l11l1lUK_Turk_No1 (u"࠭ࡴࡳࡷࡨࠫ௤")):
			xbmc.executebuiltin(l11l1lUK_Turk_No1 (u"ࠧࡄࡱࡱࡸࡦ࡯࡮ࡦࡴ࠱ࡗࡪࡺࡖࡪࡧࡺࡑࡴࡪࡥࠩࠧࡶ࠭ࠬ௥") % l11l1ll1lUK_Turk_No1.getSetting(l11111l1lUK_Turk_No1))
	except:pass
if ((mode == None) or (url == None) or len(url) < 1):
	l111111lUK_Turk_No1(P)
	l11lll11lUK_Turk_No1()
elif mode==1:l1lll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1,fanart)
elif mode==2:l1ll1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==3:l1ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==4:l1l11ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==5:l1l1l1l1UK_Turk_No1()
elif mode==6:l1ll11lllUK_Turk_No1(url,l1l11l11UK_Turk_No1)
elif mode==7:l1ll11llUK_Turk_No1(url)
elif mode==8:l11ll111lUK_Turk_No1(name)
elif mode==9:l11l1lllUK_Turk_No1(name,url)
elif mode==10:l1lll11lUK_Turk_No1(name,url)
elif mode==11:l111ll1lUK_Turk_No1(url)
elif mode==12:l1111ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==13:l1llll1UK_Turk_No1(url)
elif mode==14:l11l1ll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==15:l11l1ll11UK_Turk_No1(url)
elif mode==16:l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==17:l111lll1UK_Turk_No1(name,url)
elif mode==18:l11111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==19:l111l1l1lUK_Turk_No1(name,url)
elif mode==20:l1lllll11UK_Turk_No1(url,l1l11l11UK_Turk_No1)
elif mode==21:l1ll1111UK_Turk_No1(url)
elif mode==22:l1111l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==23:l1l1ll1llUK_Turk_No1(url)
elif mode==24:l1l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==25:l1ll1l11lUK_Turk_No1(url)
elif mode==26:l11lllll1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==27:l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==28:l11ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==29:l1ll1llllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==30:l1lll1l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==31:l111111l1UK_Turk_No1()
elif mode==32:l111ll111UK_Turk_No1()
elif mode==33:l1l1l1lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==34:l1ll1111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==35:l11ll11lUK_Turk_No1(url)
elif mode==36:l11ll11llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==37:l1ll111lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==38:l1l1111l1UK_Turk_No1()
elif mode==39:l1l1l1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==40:l111llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==41:l111ll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==42:l1l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==43:l1111l11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==44:l1111ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==45:l1ll1lUK_Turk_No1()
elif mode==46:l11llllUK_Turk_No1(url)
elif mode==47:l11llll11UK_Turk_No1(name,url)
elif mode==48:l1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==49:l11l111l1UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==50:l1llllll1UK_Turk_No1(url)
elif mode==51:l11ll11UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==52:l1ll1l111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==53:l1l1ll1lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
elif mode==54:llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1)
xbmcplugin.endOfDirectory(int(sys.argv[1]))