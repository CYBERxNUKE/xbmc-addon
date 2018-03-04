# coding: UTF-8
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
import xbmc,xbmcaddon,xbmcgui,xbmcplugin,urllib,urllib2,re,os,sys
def l11l1lll1UK_Turk_No1(url):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪആ")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡱ࡯࠾࠽ࡣࠣ࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠰ࡅࠩࠣࠢࡷ࡭ࡹࡲࡥ࠾ࠤࠫ࠲࠰ࡅࠩࠣࡀ࠱࠯ࡄࡂࡩ࡮ࡩࠣࡷࡷࡩ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡹ࡬ࡨࡹ࡮࠽ࠣ࠰࠮ࡃࠧࠦࡨࡦ࡫ࡪ࡬ࡹࡃࠢ࠯࠭ࡂࠦࠥࡧ࡬ࡵ࠿ࠥ࠲࠰ࡅࠢࠡ࠱ࡁࡀ࠴ࡧ࠾࠽࠱࡯࡭ࡃ࠭ഇ"),re.DOTALL).findall(link)
    for url,name,l1l11l11UK_Turk_No1 in match:
        url=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡪࡴࡧࡦ࡮ࡶ࡭ࡿ࠴࡫ࡢࡰࡤࡰࡩ࠴ࡣࡰ࡯࠱ࡸࡷ࠵ࠧഈ")+url
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠴࠻࠾ࠦഉ"),l11l1lUK_Turk_No1 (u"ࠨࠧࠣഊ")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠷࠶ࡁࠢഋ"),l11l1lUK_Turk_No1 (u"ࠣࡥࠥഌ")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠶࠿࠹࠼ࠤ഍"),l11l1lUK_Turk_No1 (u"ࠥࡇࠧഎ")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠶࠴࠾ࠦഏ"),l11l1lUK_Turk_No1 (u"ࠧࡻࠢഐ")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠴࠵࠴ࡀࠨ഑"),l11l1lUK_Turk_No1 (u"ࠢࡖࠤഒ")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠶࠺࠻ࠣഓ"),l11l1lUK_Turk_No1 (u"ࠤࡒࠦഔ")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠴࠷࠽ࠥക"),l11l1lUK_Turk_No1 (u"ࠦࡴࠨഖ"))
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡫࡮ࡨࡧ࡯ࡷ࡮ࢀ࠮࡬ࡣࡱࡥࡱࡪ࠮ࡤࡱࡰ࠲ࡹࡸ࠯ࠨഗ")+l1l11l11UK_Turk_No1
        string=l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠧഘ")+name+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭ങ")+url+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡩࡵࡄࠧച")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡩࡳࡪ࠾ࠨഛ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllllllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠥࡹࡷࡲ࠺ࠡࠩࡰࡴ࠹ࡀࡥ࡯ࡩࡨࡰࡸ࡯ࡺ࠰ࠪ࠱࠯ࡄ࠯ࠧࠣജ")).findall(link)
    print l11lllllllUK_Turk_No1
    for host in l11lllllllUK_Turk_No1:
        host=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡨࡪ࡮࠷࠰࡮ࡥࡳࡧ࡬ࡥ࠰ࡦࡳࡲ࠴ࡴࡳ࠱ࠪഝ")+host
        return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩഞ"), l11l1lUK_Turk_No1 (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠤ࠭࡝ࡩ࡯ࡦࡲࡻࡸࠦࡎࡕࠢ࠴࠴࠳࠶ࠩࠡࡃࡳࡴࡱ࡫ࡗࡦࡤࡎ࡭ࡹ࠵࠵࠴࠹࠱࠷࠻ࠦࠨࡌࡊࡗࡑࡑ࠲ࠠ࡭࡫࡮ࡩࠥࡍࡥࡤ࡭ࡲ࠭ࠥࡉࡨࡳࡱࡰࡩ࠴࠻࠴࠯࠲࠱࠶࠽࠺࠰࠯࠹࠴ࠤࡘࡧࡦࡢࡴ࡬࠳࠺࠹࠷࠯࠵࠹ࠫട"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠢࠧࠥࡻࠦഠ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧഡ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨഢ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠥࠬࡄ࡯ࠩࠧࠥ࡟ࡻ࠰ࡁࠢണ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠫࡎ࡙ࡏ࠮࠺࠻࠹࠾࠳࠱ࠨത")).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫഥ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠨࠨࡀ࡫ࠬࠪࠨࡢࡷࠬ࠽ࠥദ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠢࡢࡵࡦ࡭࡮ࠨധ"), l11l1lUK_Turk_No1 (u"ࠣ࡫ࡪࡲࡴࡸࡥࠣന")).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨഩ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠪࠫപ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠦࡄࡻࡲ࡭࠿ࠥഫ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠧࠬ࡭ࡰࡦࡨࡁࠧബ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡯ࡣࡰࡩࡂࠨഭ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠢࠧࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳࡃࠢമ")+str(description)+l11l1lUK_Turk_No1 (u"ࠣࠨ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࡂࠨയ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠤࡇࡩ࡫ࡧࡵ࡭ࡶࡉࡳࡱࡪࡥࡳ࠰ࡳࡲ࡬ࠨര"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠪࡪࡦࡴࡡࡳࡶࡢ࡭ࡲࡧࡧࡦࠩറ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠦࡎࡹࡐ࡭ࡣࡼࡥࡧࡲࡥࠣല"),l11l1lUK_Turk_No1 (u"ࠧࡺࡲࡶࡧࠥള"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok