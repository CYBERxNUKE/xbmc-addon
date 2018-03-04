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
def l111lllUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬ೗")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡱࡣࡱࠤࡨࡲࡡࡴࡵࡀࠦࡨࡻࡲࡳࡧࡱࡸࠧࡄ࠮ࠬࡁ࠿࠳ࡸࡶࡡ࡯ࡀ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡨࡲࡡࡴࡵࡀࠦࡵࡧࡧࡦࠤࠣࡸ࡮ࡺ࡬ࡦ࠿ࠥ࠲࠰ࡅࠢ࠿࠰࠮ࡃࡁ࠵ࡡ࠿ࠩ೘"),re.DOTALL).findall(link)
        for l111lllllUK_Turk_No1 in l11l11l11UK_Turk_No1:
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"࠭࠼࡯ࡲࡁࠫ೙")+l111lllllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂࠬ೚")
    except: pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡴࡥࡡࡰࡳࡩࡻ࡬ࡦࡡ࠴ࠤࡹࡪ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡸࡴࡤࡴࠥࡺࡤ࠮ࡣࡱ࡭ࡲࡧࡴࡪࡱࡱ࠱ࡸࡺࡡࡤ࡭ࠥࡂ࠳࠱࠿࠽ࡦ࡬ࡺࠥࡩ࡬ࡢࡵࡶࡁࠧࡺࡤ࠮࡯ࡲࡨࡺࡲࡥ࠮ࡶ࡫ࡹࡲࡨࠢ࠿࠾ࡤࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡶࡪࡲ࠽ࠣࡤࡲࡳࡰࡳࡡࡳ࡭ࠥࠤࡹ࡯ࡴ࡭ࡧࡀࠦ࠭࠴ࠫࡀࠫࠥࡂࡁ࡯࡭ࡨࠢࡺ࡭ࡩࡺࡨ࠾ࠤ࠱࠯ࡄࠨࠠࡩࡧ࡬࡫࡭ࡺ࠽ࠣ࠰࠮ࡃࠧࠦࡣ࡭ࡣࡶࡷࡂࠨࡥ࡯ࡶࡵࡽ࠲ࡺࡨࡶ࡯ࡥࠦࠥࡹࡲࡤ࠿ࠥࠬ࠳࠱࠿ࠪࡁࡵࡩࡸ࡯ࡺࡦ࠿࠱࠯ࡄࠨࠠࡢ࡮ࡷࡁࠧࠨࠠࡵ࡫ࡷࡰࡪࡃࠢ࠯࠭ࡂࠦࠥ࠵࠾࠽࠱ࡤࡂࡁ࠵ࡤࡪࡸࡁࠫ೛"),re.DOTALL).findall(link)
    for url,name,l1l11l11UK_Turk_No1 in match:
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠩࠩࠧ࠽࠸࠱࠲࠽ࠪ೜"),l11l1lUK_Turk_No1 (u"ࠪࠤ࠲ࠦࠧೝ")).replace(l11l1lUK_Turk_No1 (u"ࠫࠫࠩ࠰࠴࠺࠾ࠫೞ"),l11l1lUK_Turk_No1 (u"ࠬ࠭೟")).replace(l11l1lUK_Turk_No1 (u"࠭ࠠࡇࡷ࡯ࡰࠥࡓࡡࡵࡥ࡫ࠫೠ"),l11l1lUK_Turk_No1 (u"ࠧࠨೡ"))
        string=l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡸࡦࡸࡴ࠿ࠩೢ")+name+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨೣ")+url+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩ೤")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠫࡁ࡫࡮ࡥࡀࠪ೥")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1lll1l1lUK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l1l1111111UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡩࡧࡴࡤࡱࡪ࠴ࠫࡀࡵࡵࡧࡂࠨ࠮ࠬࡁࠥࠤࡩࡧࡴࡢ࠯࡯ࡥࡿࡿ࠭ࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠥ࡬ࡲࡢ࡯ࡨࡦࡴࡸࡤࡦࡴࡀࠫ೦"),re.DOTALL).findall(link)
    return l1l1111111UK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪ೧"), l11l1lUK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠵࠵࠴࠰ࠪࠢࡄࡴࡵࡲࡥࡘࡧࡥࡏ࡮ࡺ࠯࠶࠵࠺࠲࠸࠼ࠠࠩࡍࡋࡘࡒࡒࠬࠡ࡮࡬࡯ࡪࠦࡇࡦࡥ࡮ࡳ࠮ࠦࡃࡩࡴࡲࡱࡪ࠵࠵࠵࠰࠳࠲࠷࠾࠴࠱࠰࠺࠵࡙ࠥࡡࡧࡣࡵ࡭࠴࠻࠳࠸࠰࠶࠺ࠬ೨"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠣࠨࠦࡼࠧ೩"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨ೪"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩ೫"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣ೬"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠬࡏࡓࡐ࠯࠻࠼࠺࠿࠭࠲ࠩ೭")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ೮")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦ೯"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠣࡣࡶࡧ࡮࡯ࠢ೰"), l11l1lUK_Turk_No1 (u"ࠤ࡬࡫ࡳࡵࡲࡦࠤೱ")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩೲ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬೳ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠧࡅࡵࡳ࡮ࡀࠦ೴")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨ೵")+str(mode)+l11l1lUK_Turk_No1 (u"ࠢࠧࡰࡤࡱࡪࡃࠢ೶")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠣࠨࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴ࠽ࠣ೷")+str(description)+l11l1lUK_Turk_No1 (u"ࠤࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠢ೸")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠥࡈࡪ࡬ࡡࡶ࡮ࡷࡊࡴࡲࡤࡦࡴ࠱ࡴࡳ࡭ࠢ೹"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪ೺"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡏࡳࡑ࡮ࡤࡽࡦࡨ࡬ࡦࠤ೻"),l11l1lUK_Turk_No1 (u"ࠨࡴࡳࡷࡨࠦ೼"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok