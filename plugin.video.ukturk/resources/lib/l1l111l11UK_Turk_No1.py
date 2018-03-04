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
import urllib,urllib2,re,os,sys
def l1ll11lUK_Turk_No1(url):
    print url
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࠨൟ")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡴࡦࡴࠠࡤ࡮ࡤࡷࡸࡃࡣࡶࡴࡵࡩࡳࡺ࠾࠯࠭ࡂࡀ࠴ࡹࡰࡢࡰࡁࠤࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠮ࠬࡁ࠿࠳ࡦࡄࠧൠ")).findall(link)
        for l111lllllUK_Turk_No1 in l11l11l11UK_Turk_No1:
            l111lllllUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡧࡰࡹࡤࡸࡨ࡮ࡦࡳࡧࡨࡱࡴࡼࡩࡦࡵ࠱ࡸࡴ࠭ൡ")+l111lllllUK_Turk_No1
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡳࡶ࠾ࠨൢ")+l111lllllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠩൣ")
    except: pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥ࡭ࡹ࡫࡭ࠣࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡹ࡯ࡴ࡭ࡧࡀࠦ࠳࠱࠿ࠣࡀ࠱࠯ࡄࡂࡩ࡮ࡩࠣࡷࡷࡩ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡤࡲࡶࡩ࡫ࡲ࠾ࠤ࠱࠯ࡄࠨࠠࡸ࡫ࡧࡸ࡭ࡃࠢ࠯࠭ࡂࠦࠥ࡮ࡥࡪࡩ࡫ࡸࡂࠨ࠮ࠬࡁࠥࠤࡦࡲࡴ࠾ࠤ࡚ࡥࡹࡩࡨࠡࠪ࠱࠯ࡄ࠯ࠢ࠿࠾࠲ࡥࡃࡂ࠯ࡥ࡫ࡹࡂࠬ൤"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        url=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱࠪ൥")+url
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࡩࡶࡷࡴ࠿࠭൦")+l1l11l11UK_Turk_No1
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠷࠾ࡁࠢ൧"),l11l1lUK_Turk_No1 (u"ࠤࠪࠦ൨")).replace(l11l1lUK_Turk_No1 (u"ࠪࠪࡦࡳࡰ࠼ࠩ൩"),l11l1lUK_Turk_No1 (u"ࠫࠥࠬࠠࠨ൪"))
        string=l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠭൫")+name+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬ൬")+url+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭൭")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡨࡲࡩࡄࠧ൮")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪ൯")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡦࠦࡤࡢࡶࡤ࠱࡮ࡪ࠽ࠣ࠰࠮ࡃࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡳࡦࡣࡶࡳࡳ࠳ࡴࡰࡩࡪࡰࡪࠨࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄࠨ࠯࠭ࡂ࠭ࡁࡹࡰࡢࡰࠣࡷࡹࡿ࡬ࡦ࠿ࠥ࠲࠰ࡅࠢ࠿ࠩ൰"),re.DOTALL).findall(link)
        for url,name in match:
            url=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡩࡲࡻࡦࡺࡣࡩࡨࡵࡩࡪࡳ࡯ࡷ࡫ࡨࡷ࠳ࡺ࡯ࠨ൱")+url
            string=l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠭൲")+name+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬ൳")+url+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡧࡱࡨࡃ࠭൴")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l11lll1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠨࠩ൵")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡵࡸࡢࡩࡵ࡯ࡳࡰࡦࡨࡣ࡮ࡺࡥ࡮ࠤࡁࠤࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄࡅࠩ࠰࠮ࡃ࠮ࡂࡳࡱࡣࡱࠤࡨࡲࡡࡴࡵࡀࠦࡹࡼ࡟ࡦࡲ࡬ࡷࡴࡪࡥࡠࡰࡤࡱࡪࠨ࠾ࠡࠪ࠱࠯ࡄ࠯࠼࠰ࡵࡳࡥࡳࡄ࠮ࠬࡁ࠿ࡷࡵࡧ࡮ࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡶࡹࡣࡪࡶࡩࡴࡱࡧࡩࡤࡧࡩࡳࡦࡤࡸࡪࠨ࠾࠯࠭ࡂࡀ࠴ࡹࡰࡢࡰࡁࠫ൶"),re.DOTALL).findall(link)
        for url,l1l1llllUK_Turk_No1,l1l111llUK_Turk_No1 in match:
            url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡨࡱࡺࡥࡹࡩࡨࡧࡴࡨࡩࡲࡵࡶࡪࡧࡶ࠲ࡹࡵࠧ൷")+url
            string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬ൸")+l1l1llllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫ൹")+l1l111llUK_Turk_No1+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬൺ")+url+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡧࡱࡨࡃ࠭ൻ")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬർ"), l11l1lUK_Turk_No1 (u"ࠩࡐࡳࡿ࡯࡬࡭ࡣ࠲࠹࠳࠶࡙ࠠࠩ࡬ࡲࡩࡵࡷࡴࠢࡑࡘࠥ࠷࠰࠯࠲ࠬࠤࡆࡶࡰ࡭ࡧ࡚ࡩࡧࡑࡩࡵ࠱࠸࠷࠼࠴࠳࠷ࠢࠫࡏࡍ࡚ࡍࡍ࠮ࠣࡰ࡮ࡱࡥࠡࡉࡨࡧࡰࡵࠩࠡࡅ࡫ࡶࡴࡳࡥ࠰࠷࠷࠲࠵࠴࠲࠹࠶࠳࠲࠼࠷ࠠࡔࡣࡩࡥࡷ࡯࠯࠶࠵࠺࠲࠸࠼ࠧൽ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠥࠪࠨࡾࠢൾ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪൿ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫ඀"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠨࠨࡀ࡫ࠬࠪࠨࡢࡷࠬ࠽ࠥඁ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠧࡊࡕࡒ࠱࠽࠾࠵࠺࠯࠴ࠫං")).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧඃ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠤࠫࡃ࡮࠯ࠦࠤ࡞ࡺ࠯ࡀࠨ඄"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠥࡥࡸࡩࡩࡪࠤඅ"), l11l1lUK_Turk_No1 (u"ࠦ࡮࡭࡮ࡰࡴࡨࠦආ")).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫඇ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"࠭ࠧඈ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠢࡀࡷࡵࡰࡂࠨඉ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠣࠨࡰࡳࡩ࡫࠽ࠣඊ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠤࠩࡲࡦࡳࡥ࠾ࠤඋ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠥࠪࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯࠿ࠥඌ")+str(description)+l11l1lUK_Turk_No1 (u"ࠦࠫ࡯ࡣࡰࡰ࡬ࡱࡦ࡭ࡥ࠾ࠤඍ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠧࡊࡥࡧࡣࡸࡰࡹࡌ࡯࡭ࡦࡨࡶ࠳ࡶ࡮ࡨࠤඎ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"࠭ࡦࡢࡰࡤࡶࡹࡥࡩ࡮ࡣࡪࡩࠬඏ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠢࡊࡵࡓࡰࡦࡿࡡࡣ࡮ࡨࠦඐ"),l11l1lUK_Turk_No1 (u"ࠣࡶࡵࡹࡪࠨඑ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok