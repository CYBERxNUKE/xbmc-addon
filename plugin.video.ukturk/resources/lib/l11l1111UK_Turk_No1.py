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
def l1ll11lUK_Turk_No1(url):
    l11llll1llUK_Turk_No1 = l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡻࡼࡽ࠮ࡥࡦ࡬ࡾ࡮࠷࠮ࡤࡱࡰࠫಬ")
    if url == l11l1lUK_Turk_No1 (u"ࠫ࠵࠭ಭ"):
        l11lllll11UK_Turk_No1 = 1
    else:
        l11lllll11UK_Turk_No1 = int(url) + 1
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠬ࠭ಮ")
    page = l11llll1llUK_Turk_No1 + l11l1lUK_Turk_No1 (u"࠭࠯࡭࠰ࡳ࡬ࡵࡅࡳࡢࡻࡩࡥࡂ࠭ಯ") + str(l11lllll11UK_Turk_No1)
    link=l1llll111UK_Turk_No1(page)
    try:
        l11lllll1lUK_Turk_No1 = int(l11lllll11UK_Turk_No1)+1
        l111lUK_Turk_No1=l111lUK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡰࡳࡂࠬರ")+str(l11lllll1lUK_Turk_No1)+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡱࡴࡃ࠭ಱ")
    except: pass
    l11llllll1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡥ࡫ࡽ࡭࠲ࡨ࡯ࡹࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧ࠮࠮ࠬࡁࠬࠦࠥࡺࡩࡵ࡮ࡨࡁࠧ࠴ࠫࡀࠤࡁࡀ࡮ࡳࡧࠡࡵࡵࡧࡂࠨࠨ࠯࠭ࡂ࠭ࠧࠦࡷࡪࡦࡷ࡬ࡂࠨ࠮ࠬࡁࠥࠤ࡭࡫ࡩࡨࡪࡷࡁࠧ࠴ࠫࡀࠤࠣࡥࡱࡺ࠽ࠣ࠰࠮ࡃࠧࠦ࠯࠿࠾ࡶࡴࡦࡴࠠࡤ࡮ࡤࡷࡸࡃࠢ࠯࠭ࡂࠦࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡹࡰࡢࡰࡁࡀ࠴ࡧ࠾࠽࠱ࡧ࡭ࡻࡄࠧಲ"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in l11llllll1UK_Turk_No1:
        name=name.split(l11l1lUK_Turk_No1 (u"ࠪ࠲ࠬಳ"))[0]
        url=url.replace(l11l1lUK_Turk_No1 (u"ࠫ࡭ࡺ࡭ࠨ಴"),l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴ࡮࠱࠳ࠫವ"))
        l1l11l11UK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱ࡨࡩ࡯ࡺࡪ࠳࠱ࡧࡴࡳ࠯ࠨಶ")+l1l11l11UK_Turk_No1
        string=l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡷࡥࡷࡺ࠾ࠨಷ")+name+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡶࡩࡵࡄࠧಸ")+url+l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡪࡶ࠾ࠨಹ")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠪࡀࡪࡴࡤ࠿ࠩ಺")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll1ll1UK_Turk_No1(url):
    parts=[]
    link=l1llll111UK_Turk_No1(url)
    parts.append(url)
    l1lll11llUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡧ࡭ࡿ࡯࠭ࡱࡣࡵࡸࡸࠨ࠾ࠩ࠰࠮ࡃ࠮ࡂࡤࡪࡸࠣࡧࡱࡧࡳࡴ࠿ࠥࡨ࡮ࢀࡩ࠮ࡸ࡬ࡨࡪࡵࠢ࠿ࠩ಻"),re.DOTALL).findall(link)[0]
    l1l11ll11UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࠡࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠾࠯࠭ࡂࡀ࠴ࡧ࠾࠽࠱࡯࡭ࡃ಼࠭")).findall(l1lll11llUK_Turk_No1)
    for page in l1l11ll11UK_Turk_No1:
        page=l11l1lUK_Turk_No1 (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡷࡸࡹ࠱ࡨࡩ࡯ࡺࡪ࠳࠱ࡧࡴࡳࠧಽ")+page
        parts.append(page)
    return parts
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllllllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠧࡴࡴࡦࡁࠧ࠮࠮ࠬࡁࠬࠦࠬಾ")).findall(link)
    print l11lllllllUK_Turk_No1
    for host in l11lllllllUK_Turk_No1:
        if l11l1lUK_Turk_No1 (u"ࠨࡦࡤ࡭ࡱࡿ࡭ࡰࡶ࡬ࡳࡳ࠭ಿ") in host or l11l1lUK_Turk_No1 (u"ࠩࡼࡳࡺࡺࡵࡣࡧࠪೀ") in host:
            return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧು"), l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩೂ"))
    response = urllib2.urlopen(req, timeout=30)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠧࠬࠣࡹࠤೃ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬೄ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭೅"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧೆ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠩࡌࡗࡔ࠳࠸࠹࠷࠼࠱࠶࠭ೇ")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩೈ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣ೉"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠧࡧࡳࡤ࡫࡬ࠦೊ"), l11l1lUK_Turk_No1 (u"ࠨࡩࡨࡰࡲࡶࡪࠨೋ")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ೌ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨ್ࠩ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠤࡂࡹࡷࡲ࠽ࠣ೎")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥ೏")+str(mode)+l11l1lUK_Turk_No1 (u"ࠦࠫࡴࡡ࡮ࡧࡀࠦ೐")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠧࠬࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࡁࠧ೑")+str(description)+l11l1lUK_Turk_No1 (u"ࠨࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠦ೒")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦ೓"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧ೔"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠤࡌࡷࡕࡲࡡࡺࡣࡥࡰࡪࠨೕ"),l11l1lUK_Turk_No1 (u"ࠥࡸࡷࡻࡥࠣೖ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok