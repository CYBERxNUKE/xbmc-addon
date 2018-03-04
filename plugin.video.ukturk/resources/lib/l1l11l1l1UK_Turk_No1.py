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
def l1ll11lUK_Turk_No1(name,url,l1l11l11UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬ࠭಄")
    link=l1llll111UK_Turk_No1(url)
    try:
        l11l11l11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"࠭࠼ࡢࠢࡦࡰࡦࡹࡳ࠾ࠤࡱࡩࡽࡺࡰࡰࡵࡷࡷࡱ࡯࡮࡬ࠤࠣࡶࡪࡲ࠽ࠣࡰࡨࡼࡹࠨࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄ࠮ࠬࡁ࠿࠳ࡦࡄࠧಅ")).findall(link)[0]
        l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂࠬಆ")+l11l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡱࡴࡃ࠭ಇ")
    except: pass
    l11llllll1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢ࡬ࡷࡷࡹ࠲ࡸࡥࡴ࡫ࡰࠦࡃࠦ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠡࡶ࡬ࡸࡱ࡫࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠾࡬ࡱ࡬ࠦࡳࡵࡻ࡯ࡩࡂࠨࡢࡰࡴࡧࡩࡷ࠳ࡷࡪࡦࡷ࡬࠿ࠦ࠰ࡱࡺ࠾ࠤ࡭࡫ࡩࡨࡪࡷ࠾ࠥ࠴ࠫࡀ࠽ࠣࡻ࡮ࡪࡴࡩ࠼ࠣ࠲࠰ࡅ࠻ࠣࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠠࡢ࡮ࡷࡁࠧ࠴ࠫࡀࠤࠣࡻ࡮ࡪࡴࡩ࠿ࠥ࠲࠰ࡅࠢࠡࡪࡨ࡭࡬࡮ࡴ࠾ࠤ࠱࠯ࡄࠨ࠯࠿ࠩಈ"),re.DOTALL).findall(link)
    for url,name,l1l11l11UK_Turk_No1 in l11llllll1UK_Turk_No1:
        name=name.split(l11l1lUK_Turk_No1 (u"ࠪ࠲ࠬಉ"))[0]
        string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬಊ")+name+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫಋ")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬಌ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡧࡱࡨࡃ࠭಍")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll1ll1UK_Turk_No1(url):
    parts=[]
    link=l1llll111UK_Turk_No1(url)
    parts.append(url)
    print parts
    l1lll11llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡩࡥ࠿ࠥࡴࡦࡸࡴࠣࡀࠫ࠲࠰ࡅࠩ࠽ࡦ࡬ࡺࠥࡩ࡬ࡢࡵࡶࡁࠧࡼࡩࡥࡧࡲࠦࡃ࠭ಎ"),re.DOTALL).findall(link)[0]
    l1l11ll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࡂࡁࡹࡰࡢࡰࡁࠫಏ")).findall(l1lll11llUK_Turk_No1)
    for page in l1l11ll11UK_Turk_No1:
        parts.append(page)
    return parts
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    link=l1llll111UK_Turk_No1(url)
    l11lllllllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡷࡷࡩ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠨಐ")).findall(link)
    print l11lllllllUK_Turk_No1
    for host in l11lllllllUK_Turk_No1:
        if l11l1lUK_Turk_No1 (u"ࠫࡩࡧࡩ࡭ࡻࡰࡳࡹ࡯࡯࡯ࠩ಑") in host or l11l1lUK_Turk_No1 (u"ࠬ࡮ࡱࡲࠩಒ") in host:
            return host
        elif l11l1lUK_Turk_No1 (u"࠭ࡣࡢࡰ࡯࡭ࡩ࡯ࡺࡪࡪࡧ࠺ࠬಓ") in host:
            link=l1llll111UK_Turk_No1(host)
            l11lllllllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠬಔ")).findall(link)
            for host in l11lllllllUK_Turk_No1:
                if l11l1lUK_Turk_No1 (u"ࠨࡦࡤ࡭ࡱࡿ࡭ࡰࡶ࡬ࡳࡳ࠭ಕ") in host:
                    return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠩࡘࡷࡪࡸ࠭ࡂࡩࡨࡲࡹ࠭ಖ"), l11l1lUK_Turk_No1 (u"ࠪࡑࡴࢀࡩ࡭࡮ࡤ࠳࠺࠴࠰࡚ࠡࠪ࡭ࡳࡪ࡯ࡸࡵࠣࡒ࡙ࠦ࠱࠱࠰࠳࠭ࠥࡇࡰࡱ࡮ࡨ࡛ࡪࡨࡋࡪࡶ࠲࠹࠸࠽࠮࠴࠸ࠣࠬࡐࡎࡔࡎࡎ࠯ࠤࡱ࡯࡫ࡦࠢࡊࡩࡨࡱ࡯ࠪࠢࡆ࡬ࡷࡵ࡭ࡦ࠱࠸࠸࠳࠶࠮࠳࠺࠷࠴࠳࠽࠱ࠡࡕࡤࡪࡦࡸࡩ࠰࠷࠶࠻࠳࠹࠶ࠨಗ"))
    response = urllib2.urlopen(req, timeout=30)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠦࠫࠩࡸࠣಘ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠬࡻࡴࡧ࠯࠻ࠫಙ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬಚ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦಛ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠨࡋࡖࡓ࠲࠾࠸࠶࠻࠰࠵ࠬಜ")).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨಝ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠥࠬࡄ࡯ࠩࠧࠥ࡟ࡻ࠰ࡁࠢಞ"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠦࡦࡹࡣࡪ࡫ࠥಟ"), l11l1lUK_Turk_No1 (u"ࠧ࡯ࡧ࡯ࡱࡵࡩࠧಠ")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬಡ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠧࠨಢ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠣࡁࡸࡶࡱࡃࠢಣ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠤࠩࡱࡴࡪࡥ࠾ࠤತ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠥࠪࡳࡧ࡭ࡦ࠿ࠥಥ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠦࠫࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࡀࠦದ")+str(description)+l11l1lUK_Turk_No1 (u"ࠧࠬࡩࡤࡱࡱ࡭ࡲࡧࡧࡦ࠿ࠥಧ")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠨࡄࡦࡨࡤࡹࡱࡺࡆࡰ࡮ࡧࡩࡷ࠴ࡰ࡯ࡩࠥನ"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡧࡣࡱࡥࡷࡺ࡟ࡪ࡯ࡤ࡫ࡪ࠭಩"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠣࡋࡶࡔࡱࡧࡹࡢࡤ࡯ࡩࠧಪ"),l11l1lUK_Turk_No1 (u"ࠤࡷࡶࡺ࡫ࠢಫ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok