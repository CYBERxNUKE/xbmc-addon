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
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬว")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡴࡷࡵࡧࡳࡣࡰࡷࡤ࡯ࡴࡦ࡯ࠣࡧࡴࡲ࠭࡭ࡩ࠰࠷ࠥࡩ࡯࡭࠯ࡰࡨ࠲࠹ࠠࡤࡱ࡯࠱ࡸࡳ࠭࠵ࠢࡦࡳࡱ࠳ࡸࡴ࠯࠷ࠤࡨࡵ࡬࠮ࡺࡻࡷ࠲࠼ࠢ࠿࠰࠮ࡃࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠮ࠬࡁ࠿࡭ࡲ࡭ࠠࡤ࡮ࡤࡷࡸࡃࠢࡪ࡯ࡪ࠱ࡷ࡫ࡳࡱࡱࡱࡷ࡮ࡼࡥࠣࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠࡢ࡮ࡷࡁࠧ࠮࠮ࠬࡁࠬࠦࠥ࠵࠾ࠨศ"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        url=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡸࡹࡺ࠲ࡹࡸࡴ࠯ࡶࡹࠫษ")+url
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠧࡳࡸࡳࡹࡁࠧส"),l11l1lUK_Turk_No1 (u"ࠨࠤࠪห")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠷࠹࠱࠼ࠤฬ"),l11l1lUK_Turk_No1 (u"ࠥࡧࠧอ")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠱࠺࠻࠾ࠦฮ"),l11l1lUK_Turk_No1 (u"ࠧࡉࠢฯ")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠴࠸࠶ࡀࠨะ"),l11l1lUK_Turk_No1 (u"ࠢࡶࠤั")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠷࠶࠻ࠣา"),l11l1lUK_Turk_No1 (u"ࠤࡘࠦำ")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠱࠵࠽ࠥิ"),l11l1lUK_Turk_No1 (u"ࠦࡔࠨี")).replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠳࠶࠹࠿ࠧึ"),l11l1lUK_Turk_No1 (u"ࠨ࡯ࠣื")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠶࠽ࡀࠨุ"),l11l1lUK_Turk_No1 (u"ูࠣࠩࠥ"))
        l1l11l11UK_Turk_No1=l1l11l11UK_Turk_No1.replace(l11l1lUK_Turk_No1 (u"ฺࠩࠣࠫ"),l11l1lUK_Turk_No1 (u"ࠪࠩ࠷࠶ࠧ฻"))
        string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬ฼")+name+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫ฽")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬ฾")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡧࡱࡨࡃ࠭฿")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllllllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨࡷࡵࡰ࠿ࠦࠢࠩ࠰࠮ࡃ࠮ࡅ࠽࠯࠭ࡂࠦࠬเ")).findall(link)
    print l11lllllllUK_Turk_No1
    for host in l11lllllllUK_Turk_No1:
        return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭แ"), l11l1lUK_Turk_No1 (u"ࠪࡑࡴࢀࡩ࡭࡮ࡤ࠳࠺࠴࠰࡚ࠡࠪ࡭ࡳࡪ࡯ࡸࡵࠣࡒ࡙ࠦ࠱࠱࠰࠳࠭ࠥࡇࡰࡱ࡮ࡨ࡛ࡪࡨࡋࡪࡶ࠲࠹࠸࠽࠮࠴࠸ࠣࠬࡐࡎࡔࡎࡎ࠯ࠤࡱ࡯࡫ࡦࠢࡊࡩࡨࡱ࡯ࠪࠢࡆ࡬ࡷࡵ࡭ࡦ࠱࠸࠸࠳࠶࠮࠳࠺࠷࠴࠳࠽࠱ࠡࡕࡤࡪࡦࡸࡩ࠰࠷࠶࠻࠳࠹࠶ࠨโ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠦࠫࠩࡸࠣใ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫไ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬๅ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦๆ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠨࡋࡖࡓ࠲࠾࠸࠶࠻࠰࠵ࠬ็")).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨ่")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠥࠬࡄ࡯ࠩࠧࠥ࡟ࡻ࠰ࡁ้ࠢ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠦࡦࡹࡣࡪ࡫๊ࠥ"), l11l1lUK_Turk_No1 (u"ࠧ࡯ࡧ࡯ࡱࡵࡩ๋ࠧ")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ์")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨํ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠣࡁࡸࡶࡱࡃࠢ๎")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤ๏")+str(mode)+l11l1lUK_Turk_No1 (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥ๐")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠦࠫࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࡀࠦ๑")+str(description)+l11l1lUK_Turk_No1 (u"ࠧࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠥ๒")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠨࡄࡦࡨࡤࡹࡱࡺࡆࡰ࡮ࡧࡩࡷ࠴ࡰ࡯ࡩࠥ๓"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡧࡣࡱࡥࡷࡺ࡟ࡪ࡯ࡤ࡫ࡪ࠭๔"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠣࡋࡶࡔࡱࡧࡹࡢࡤ࡯ࡩࠧ๕"),l11l1lUK_Turk_No1 (u"ࠤࡷࡶࡺ࡫ࠢ๖"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok