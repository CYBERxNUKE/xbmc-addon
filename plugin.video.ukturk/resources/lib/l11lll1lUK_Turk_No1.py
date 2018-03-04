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
def l11l1llllUK_Turk_No1(url):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠪࠫ෵")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡧ࡭ࡿ࡯ࠢࠡ࡫ࡧࡁࠧ࠴ࠫࡀࠤࡁ࠲࠰ࡅ࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠾࡬ࡱ࡬ࠦࡣ࡭ࡣࡶࡷࡂࠨࡤࡪࡼ࡬ࡍࡲࡧࡧࡦࠤࠣࡷࡷࡩ࠽ࠣࠪ࠱࠯ࡄ࠯࠿ࡷ࠿࠱࠯ࡄࠨࠠࡸ࡫ࡧࡸ࡭ࡃࠢ࠯࠭ࡂࠦࠥ࡮ࡥࡪࡩ࡫ࡸࡂࠨ࠮ࠬࡁࠥࡂ࠳࠱࠿࠽ࡷ࡯ࠤࡨࡲࡡࡴࡵࡀࠦࡩ࡯ࡺࡪࡄ࡬ࡰ࡬࡯ࠢ࠿࠰࠮ࡃࡁࡲࡩࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡦ࡬ࡾ࡮ࡥࡡࡥ࡫ࠥࡂ࠭࠴ࠫࡀࠫ࠿࠳ࡱ࡯࠾ࠨ෶"),re.DOTALL).findall(link)
    for url,l1l11l11UK_Turk_No1,name in match:
        name=name.replace(l11l1lUK_Turk_No1 (u"ࠧࠬࠣ࠴࠻࠾ࠦ෷"),l11l1lUK_Turk_No1 (u"ࠨࠧࠣ෸")).replace(l11l1lUK_Turk_No1 (u"ࠢࠧࠥ࠵࠷࠶ࡁࠢ෹"),l11l1lUK_Turk_No1 (u"ࠣࡥࠥ෺")).replace(l11l1lUK_Turk_No1 (u"ࠤࠩࠧ࠶࠿࠹࠼ࠤ෻"),l11l1lUK_Turk_No1 (u"ࠥࡇࠧ෼")).replace(l11l1lUK_Turk_No1 (u"ࠦࠫࠩ࠲࠶࠴࠾ࠦ෽"),l11l1lUK_Turk_No1 (u"ࠧࡻࠢ෾")).replace(l11l1lUK_Turk_No1 (u"ࠨࠦࠤ࠴࠵࠴ࡀࠨ෿"),l11l1lUK_Turk_No1 (u"ࠢࡖࠤ฀")).replace(l11l1lUK_Turk_No1 (u"ࠣࠨࠦ࠶࠶࠺࠻ࠣก"),l11l1lUK_Turk_No1 (u"ࠤࡒࠦข")).replace(l11l1lUK_Turk_No1 (u"ࠥࠪࠨ࠸࠴࠷࠽ࠥฃ"),l11l1lUK_Turk_No1 (u"ࠦࡴࠨค"))
        string=l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡵࡣࡵࡸࡃ࠭ฅ")+name+l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡧࡳࡂࠬฆ")+url+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭ง")+l1l11l11UK_Turk_No1+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡨࡲࡩࡄࠧจ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll1l1UK_Turk_No1(name,url):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠩࠪฉ")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠪࡀࡩ࡯ࡶࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡦࡵࡳࡵࡪ࡯ࡸࡰ࠰ࡧࡴࡴࡴࡦࡰࡷࠤࡩࡸ࡯ࡱࡦࡲࡻࡳ࠳ࡳࡤࡴࡲࡰࡱࠨ࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡥ࡫ࡹࡂࠬช"),re.DOTALL).findall(link)[0]
    l11ll11lllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠫࡁࡧࠠࡩࡴࡨࡪࡂࠨࡪࡢࡸࡤࡷࡨࡸࡩࡱࡶ࠽࠿ࠧࠦࡩࡥ࠿ࠥࠦࠥࡪࡡࡵࡣ࠰࡬ࡷ࡫ࡦ࠾ࠤࠫ࠲࠰ࡅࠩࠣࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡤࡂࠬซ")).findall(match)
    for url,name in l11ll11lllUK_Turk_No1:
        url=l11l1lUK_Turk_No1 (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡶ࡬ࡴࡽࡴࡷ࠰ࡦࡳࡲ࠴ࡴࡳࠩฌ")+url
        string=l11l1lUK_Turk_No1 (u"࠭࠼ࡴࡶࡤࡶࡹࡄࠧญ")+name+l11l1lUK_Turk_No1 (u"ࠧ࠽ࡵࡨࡴࡃ࠭ฎ")+url+l11l1lUK_Turk_No1 (u"ࠨ࠾ࡨࡲࡩࡄࠧฏ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l11ll11ll1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l11lllllllUK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡱࡪࡺࡡࠡࡰࡤࡱࡪࡃࠢࡱࡱࡳࡧࡴࡸ࡮࠻ࡵࡷࡶࡪࡧ࡭ࠣࠢࡦࡳࡳࡺࡥ࡯ࡶࡀࠦ࠭࠴ࠫࡀࠫࠥࠤ࠴ࡄࠧฐ"),re.DOTALL).findall(link)
    print l11lllllllUK_Turk_No1
    for host in l11lllllllUK_Turk_No1:
        return host
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧฑ"), l11l1lUK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩฒ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠧࠬࠣࡹࠤณ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬด"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ต"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠣࠪࡂ࡭࠮ࠬࠣ࡝ࡹ࠮࠿ࠧถ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠩࡌࡗࡔ࠳࠸࠹࠷࠼࠱࠶࠭ท")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩธ")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣน"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠧࡧࡳࡤ࡫࡬ࠦบ"), l11l1lUK_Turk_No1 (u"ࠨࡩࡨࡰࡲࡶࡪࠨป")).encode(l11l1lUK_Turk_No1 (u"ࠧࡶࡶࡩ࠱࠽࠭ผ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠨࠩฝ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠤࡂࡹࡷࡲ࠽ࠣพ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠥࠪࡲࡵࡤࡦ࠿ࠥฟ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠦࠫࡴࡡ࡮ࡧࡀࠦภ")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠧࠬࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࡁࠧม")+str(description)+l11l1lUK_Turk_No1 (u"ࠨࠦࡪࡥࡲࡲ࡮ࡳࡡࡨࡧࡀࠦย")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠢࡅࡧࡩࡥࡺࡲࡴࡇࡱ࡯ࡨࡪࡸ࠮ࡱࡰࡪࠦร"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠨࡨࡤࡲࡦࡸࡴࡠ࡫ࡰࡥ࡬࡫ࠧฤ"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠤࡌࡷࡕࡲࡡࡺࡣࡥࡰࡪࠨล"),l11l1lUK_Turk_No1 (u"ࠥࡸࡷࡻࡥࠣฦ"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok