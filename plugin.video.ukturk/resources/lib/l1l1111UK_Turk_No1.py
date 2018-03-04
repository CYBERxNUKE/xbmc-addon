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
import urllib,urllib2,re,os,sys,base64
def l1ll11lUK_Turk_No1(url):
    print url
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪඒ")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡸࡶࡡ࡯ࠢࡦࡰࡦࡹࡳ࠾ࡥࡸࡶࡷ࡫࡮ࡵࡀ࠱࠯ࡄࡂ࠯ࡴࡲࡤࡲࡃࠦ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠰࠮ࡃࡁ࠵ࡡ࠿ࠩඓ")).findall(link)
        for l111lllllUK_Turk_No1 in l11l11l11UK_Turk_No1:
            l111lllllUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡩࡲࡻࡦࡺࡣࡩࡨࡵࡩࡪࡳ࡯ࡷ࡫ࡨࡷ࠳ࡺ࡯ࠨඔ")+l111lllllUK_Turk_No1
            l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠬࡂ࡮ࡱࡀࠪඕ")+l111lllllUK_Turk_No1+l11l1lUK_Turk_No1 (u"࠭࠼࡯ࡲࡁࠫඖ")
    except: pass
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠧ࠽ࡦ࡬ࡺࠥࡩ࡬ࡢࡵࡶࡁࠧ࡯ࡴࡦ࡯ࠥࡂࡁࡧࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࠦࡴࡪࡶ࡯ࡩࡂࠨ࠮ࠬࡁࠥࡂ࠳࠱࠿࠽࡫ࡰ࡫ࠥࡹࡲࡤ࠿ࠥࠬ࠳࠱࠿ࠪࠤࠣࡦࡴࡸࡤࡦࡴࡀࠦ࠳࠱࠿ࠣࠢࡺ࡭ࡩࡺࡨ࠾ࠤ࠱࠯ࡄࠨࠠࡩࡧ࡬࡫࡭ࡺ࠽ࠣ࠰࠮ࡃࠧࠦࡡ࡭ࡶࡀࠦ࡜ࡧࡴࡤࡪࠣࠬ࠳࠱࠿ࠪࠤࡁࡀ࠴ࡧ࠾࠽࠱ࡧ࡭ࡻࡄࠧ඗"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        url=l11l1lUK_Turk_No1 (u"ࠨࡪࡷࡸࡵࡀ࠯࠰ࡹࡺࡻ࠳࡭࡯ࡸࡣࡷࡧ࡭࡬ࡲࡦࡧࡰࡳࡻ࡯ࡥࡴ࠰ࡷࡳࠬ඘")+url
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩ࡫ࡸࡹࡶ࠺ࠨ඙")+l1l11l11UK_Turk_No1
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠹࠹࠼ࠤක"),l11l1lUK_Turk_No1 (u"ࠦࠬࠨඛ")).replace(l11l1lUK_Turk_No1 (u"ࠬࠬࡡ࡮ࡲ࠾ࠫග"),l11l1lUK_Turk_No1 (u"࠭ࠠࠧࠢࠪඝ"))
        string=l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠨඞ")+name+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡩࡵࡄࠧඟ")+url+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨච")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡪࡴࡤ࠿ࠩඡ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1ll111UK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠫࠬජ")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࠡࡦࡤࡸࡦ࠳ࡩࡥ࠿ࠥ࠲࠰ࡅࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡵࡨࡥࡸࡵ࡮࠮ࡶࡲ࡫࡬ࡲࡥࠣࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿ࠪ࠱࠯ࡄ࠯࠼ࡴࡲࡤࡲࠥࡹࡴࡺ࡮ࡨࡁࠧ࠴ࠫࡀࠤࡁࠫඣ"),re.DOTALL).findall(link)
        for url,name in match:
            url=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱࡫ࡴࡽࡡࡵࡥ࡫ࡪࡷ࡫ࡥ࡮ࡱࡹ࡭ࡪࡹ࠮ࡵࡱࠪඤ")+url
            string=l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠨඥ")+name+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡩࡵࡄࠧඦ")+url+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡩࡳࡪ࠾ࠨට")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l11lll1llUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
        l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪࠫඨ")
        link=l1llll111UK_Turk_No1(url)
        match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡷࡺࡤ࡫ࡰࡪࡵࡲࡨࡪࡥࡩࡵࡧࡰࠦࡃࠦ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿ࡇࠫ࠲࠰ࡅࠩ࠽ࡵࡳࡥࡳࠦࡣ࡭ࡣࡶࡷࡂࠨࡴࡷࡡࡨࡴ࡮ࡹ࡯ࡥࡧࡢࡲࡦࡳࡥࠣࡀࠣࠬ࠳࠱࠿ࠪ࠾࠲ࡷࡵࡧ࡮࠿࠰࠮ࡃࡁࡹࡰࡢࡰࠣࡧࡱࡧࡳࡴ࠿ࠥࡸࡻࡥࡥࡱ࡫ࡶࡳࡩ࡫࡟ࡢ࡫ࡵࡨࡦࡺࡥࠣࡀ࠱࠯ࡄࡂ࠯ࡴࡲࡤࡲࡃ࠭ඩ"),re.DOTALL).findall(link)
        for url,l1l1llllUK_Turk_No1,l1l111llUK_Turk_No1 in match:
            url=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡪࡳࡼࡧࡴࡤࡪࡩࡶࡪ࡫࡭ࡰࡸ࡬ࡩࡸ࠴ࡴࡰࠩඪ")+url
            string=l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠧණ")+l1l1llllUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭ඬ")+l1l111llUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡩࡵࡄࠧත")+url+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡩࡳࡪ࠾ࠨථ")
            l111lUK_Turk_No1=l111lUK_Turk_No1+string
        return l111lUK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧද"), l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩධ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠧࠬࠣࡹࠤන"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ඲"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ඳ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧප"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠩࡌࡗࡔ࠳࠸࠹࠷࠼࠱࠶࠭ඵ")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩබ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣභ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠧࡧࡳࡤ࡫࡬ࠦම"), l11l1lUK_Turk_No1 (u"ࠨࡩࡨࡰࡲࡶࡪࠨඹ")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ය")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩර")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠤࡂࡹࡷࡲ࠽ࠣ඼")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥල")+str(mode)+l11l1lUK_Turk_No1 (u"ࠦࠫࡴࡡ࡮ࡧࡀࠦ඾")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠧࠬࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࡁࠧ඿")+str(description)+l11l1lUK_Turk_No1 (u"ࠨࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠦව")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦශ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧෂ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠤࡌࡷࡕࡲࡡࡺࡣࡥࡰࡪࠨස"),l11l1lUK_Turk_No1 (u"ࠥࡸࡷࡻࡥࠣහ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok