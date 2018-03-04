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
def l11ll1lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬౙ")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡴࡦ࡭ࡩ࡯ࡣࡷ࡭ࡴࡴࠢ࠿ࠪ࠱࠯ࡄ࠯࠼ࡥ࡫ࡹࠤࡨࡲࡡࡴࡵࡀࠦࡸ࡯ࡤࡦࡤࡤࡶࠥࡹࡣࡳࡱ࡯ࡰ࡮ࡴࡧࠣࡀࠪౚ"),re.DOTALL).findall(link)
        for items in l11l11l11UK_Turk_No1:
            url=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡀࠪ౛")).findall(items)[-1]
            l111ll1l1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡳࡥࡳࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂࠬ౜")).findall(items)[0]
            url=url.replace(l11l1lUK_Turk_No1 (u"ࠨࠨࠦ࠴࠸࠾࠻ࠨౝ"),l11l1lUK_Turk_No1 (u"ࠩࠩࠫ౞"))
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡳࡶ࠾ࠨ౟")+l111ll1l1UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁࡴࡰ࠿ࠩౠ")+url+l11l1lUK_Turk_No1 (u"ࠬࡂ࡮ࡱࡀࠪౡ")
    except:pass
    match=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࡴࡷ࡭ࡨࡲࡥࠡ࡫ࡧࡁࠧ࠴ࠫࡀࠤࠣࡧࡱࡧࡳࡴ࠿ࠥ࡭ࡹ࡫࡭ࠡ࡯ࡲࡺ࡮࡫ࡳࠣࡀ࠱࠯ࡄࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡴࡴࡹࡴࡦࡴࠥࡂ࠳࠱࠿࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡥࡱࡺ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠰࠮ࡃࡁࡹࡰࡢࡰࠣࡧࡱࡧࡳࡴ࠿ࠥࡵࡺࡧ࡬ࡪࡶࡼࠦࡃ࠴ࠫࡀ࠾࠲ࡷࡵࡧ࡮࠿࠰࠮ࡃࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠼ࡥ࡫ࡹࠤࡨࡲࡡࡴࡵࡀࠦࡸ࡫ࡥࠣࡀࠪౢ"),re.DOTALL).findall(link)
    for l1l11l11UK_Turk_No1,name,url in match:
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠻࠶࠶࠽࠻ࠣౣ"),l11l1lUK_Turk_No1 (u"ࠣࠩࠥ౤")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠽࠸࠱࠲࠽ࠥ౥"),l11l1lUK_Turk_No1 (u"ࠥ࠱ࠧ౦")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠰࠴࠺࠾ࠦ౧"),l11l1lUK_Turk_No1 (u"ࠧࠬࠢ౨"))
        string=l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠧ౩")+name+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭౪")+url+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡩࡵࡄࠧ౫")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡩࡳࡪ࠾ࠨ౬")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l1l1111111UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀ࡮࡬ࡲࡢ࡯ࡨࠤࡨࡲࡡࡴࡵࡀࠦࡲ࡫ࡴࡢࡨࡵࡥࡲ࡫ࠠࡳࡲࡷࡷࡸࠨࠠࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠬ౭"),re.DOTALL).findall(link)
    return l1l1111111UK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡚ࠫࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠨ౮"), l11l1lUK_Turk_No1 (u"ࠬࡓ࡯ࡻ࡫࡯ࡰࡦ࠵࠵࠯࠲ࠣࠬ࡜࡯࡮ࡥࡱࡺࡷࠥࡔࡔࠡ࠳࠳࠲࠵࠯ࠠࡂࡲࡳࡰࡪ࡝ࡥࡣࡍ࡬ࡸ࠴࠻࠳࠸࠰࠶࠺ࠥ࠮ࡋࡉࡖࡐࡐ࠱ࠦ࡬ࡪ࡭ࡨࠤࡌ࡫ࡣ࡬ࡱࠬࠤࡈ࡮ࡲࡰ࡯ࡨ࠳࠺࠺࠮࠱࠰࠵࠼࠹࠶࠮࠸࠳ࠣࡗࡦ࡬ࡡࡳ࡫࠲࠹࠸࠽࠮࠴࠸ࠪ౯"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠨࠦࠤࡺࠥ౰"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭౱"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧ౲"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠤࠫࡃ࡮࠯ࠦࠤ࡞ࡺ࠯ࡀࠨ౳"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠪࡍࡘࡕ࠭࠹࠺࠸࠽࠲࠷ࠧ౴")).encode(l11l1lUK_Turk_No1 (u"ࠫࡺࡺࡦ࠮࠺ࠪ౵")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠧ࠮࠿ࡪࠫࠩࠧࡡࡽࠫ࠼ࠤ౶"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠨࡡࡴࡥ࡬࡭ࠧ౷"), l11l1lUK_Turk_No1 (u"ࠢࡪࡩࡱࡳࡷ࡫ࠢ౸")).encode(l11l1lUK_Turk_No1 (u"ࠨࡷࡷࡪ࠲࠾ࠧ౹")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠩࠪ౺")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠥࡃࡺࡸ࡬࠾ࠤ౻")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠦࠫࡳ࡯ࡥࡧࡀࠦ౼")+str(mode)+l11l1lUK_Turk_No1 (u"ࠧࠬ࡮ࡢ࡯ࡨࡁࠧ౽")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠨࠦࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࡂࠨ౾")+str(description)+l11l1lUK_Turk_No1 (u"ࠢࠧ࡫ࡦࡳࡳ࡯࡭ࡢࡩࡨࡁࠧ౿")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠣࡆࡨࡪࡦࡻ࡬ࡵࡈࡲࡰࡩ࡫ࡲ࠯ࡲࡱ࡫ࠧಀ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠩࡩࡥࡳࡧࡲࡵࡡ࡬ࡱࡦ࡭ࡥࠨಁ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠥࡍࡸࡖ࡬ࡢࡻࡤࡦࡱ࡫ࠢಂ"),l11l1lUK_Turk_No1 (u"ࠦࡹࡸࡵࡦࠤಃ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok