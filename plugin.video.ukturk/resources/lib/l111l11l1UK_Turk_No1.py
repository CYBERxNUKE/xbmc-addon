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
#import xbmc,xbmcaddon,xbmcgui,xbmcplugin
def l1ll11lUK_Turk_No1(url):
    print url
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"࠭ࠧഴ")
    l11llll11lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࠨവ")
    link=l1llll111UK_Turk_No1(url)
    l11llllll1UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠣ࠾࡯࡭ࠥࡩ࡬ࡢࡵࡶࡁࠬࡲࡩࡴࡶࡈࡴ࡮ࡹ࡯ࡥࡧࠪࠬ࠳࠱࠿ࠪ࠾࠲ࡰ࡮ࡄࠢശ"),re.DOTALL).findall(link)
    for show in l11llllll1UK_Turk_No1:
        name=re.compile(l11l1lUK_Turk_No1 (u"ࠤ࠿࠳ࡸࡶࡡ࡯ࡀࠫ࠲࠰ࡅࠩ࠽࠱ࡤࡂࠧഷ")).findall(show)[0]
        date=re.compile(l11l1lUK_Turk_No1 (u"ࠥࡠࡃ࠮࠮ࠬࡁࠬࠤࡡࡀࠠ࠽ࡣࠣࡸࡦࡸࡧࡦࡶࠥസ")).findall(show)[0].replace(l11l1lUK_Turk_No1 (u"ࠫࠥ࠭ഹ"),l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧഺ"))
        day=date.split(l11l1lUK_Turk_No1 (u"࠭࠯ࠨ഻"))[0]
        month=date.split(l11l1lUK_Turk_No1 (u"ࠧ࠰഼ࠩ"))[1]
        year=date.split(l11l1lUK_Turk_No1 (u"ࠨ࠱ࠪഽ"))[2]
        if len(day)==1:
            day=l11l1lUK_Turk_No1 (u"ࠩ࠳ࠫാ")+day
        date=l11l1lUK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣ࡫ࡴࡲࡤ࡞ࠩി")+day+l11l1lUK_Turk_No1 (u"ࠫ࠴࠭ീ")+month+l11l1lUK_Turk_No1 (u"ࠬ࠵ࠧു")+year+l11l1lUK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨൂ")
        name=date+l11l1lUK_Turk_No1 (u"ࠧࠡ࠯ࠣࠫൃ")+name
        url=re.compile(l11l1lUK_Turk_No1 (u"ࠨࡪࡵࡩ࡫ࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠾ࠨൄ")).findall(show)[0]
        string=l11l1lUK_Turk_No1 (u"ࠩ࠿ࡷࡹࡧࡲࡵࡀࠪ൅")+name+l11l1lUK_Turk_No1 (u"ࠪࡀࡸ࡫ࡰ࠿ࠩെ")+url+l11l1lUK_Turk_No1 (u"ࠫࡁ࡫࡮ࡥࡀࠪേ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l111l1l1UK_Turk_No1(url):
    link=l1llll111UK_Turk_No1(url)
    l1l1111111UK_Turk_No1=re.compile(l11l1lUK_Turk_No1 (u"ࠬࡂࡡࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤࡢࡦࡱࡧ࡮࡬ࠤࠣࡶࡪࡲ࠽ࠣࡰࡲࡪࡴࡲ࡬ࡰࡹࠥࠤ࡭ࡸࡥࡧ࠿ࠥࠬ࠳࠱࠿ࠪࠤࡁࡔࡱࡧࡹ࠽࠱ࡤࡂࠬൈ")).findall(link)
    return l1l1111111UK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪ൉"), l11l1lUK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠵࠵࠴࠰ࠪࠢࡄࡴࡵࡲࡥࡘࡧࡥࡏ࡮ࡺ࠯࠶࠵࠺࠲࠸࠼ࠠࠩࡍࡋࡘࡒࡒࠬࠡ࡮࡬࡯ࡪࠦࡇࡦࡥ࡮ࡳ࠮ࠦࡃࡩࡴࡲࡱࡪ࠵࠵࠵࠰࠳࠲࠷࠾࠴࠱࠰࠺࠵࡙ࠥࡡࡧࡣࡵ࡭࠴࠻࠳࠸࠰࠶࠺ࠬൊ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link
def l111ll1UK_Turk_No1(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == l11l1lUK_Turk_No1 (u"ࠣࠨࠦࡼࠧോ"): return unichr(int(text[3:-1], 16)).encode(l11l1lUK_Turk_No1 (u"ࠩࡸࡸ࡫࠳࠸ࠨൌ"))
        else: return unichr(int(text[2:-1])).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹്ࠩ"))
    try :return re.sub(l11l1lUK_Turk_No1 (u"ࠦ࠭ࡅࡩࠪࠨࠦࡠࡼ࠱࠻ࠣൎ"), fixup, text.decode(l11l1lUK_Turk_No1 (u"ࠬࡏࡓࡐ࠯࠻࠼࠺࠿࠭࠲ࠩ൏")).encode(l11l1lUK_Turk_No1 (u"࠭ࡵࡵࡨ࠰࠼ࠬ൐")))
    except:return re.sub(l11l1lUK_Turk_No1 (u"ࠢࠩࡁ࡬࠭ࠫࠩ࡜ࡸ࠭࠾ࠦ൑"), fixup, text.encode(l11l1lUK_Turk_No1 (u"ࠣࡣࡶࡧ࡮࡯ࠢ൒"), l11l1lUK_Turk_No1 (u"ࠤ࡬࡫ࡳࡵࡲࡦࠤ൓")).encode(l11l1lUK_Turk_No1 (u"ࠪࡹࡹ࡬࠭࠹ࠩൔ")))
def l1111111UK_Turk_No1(name,url,mode,l1l11l11UK_Turk_No1,fanart,description=l11l1lUK_Turk_No1 (u"ࠫࠬൕ")):
        u=sys.argv[0]+l11l1lUK_Turk_No1 (u"ࠧࡅࡵࡳ࡮ࡀࠦൖ")+urllib.quote_plus(url)+l11l1lUK_Turk_No1 (u"ࠨࠦ࡮ࡱࡧࡩࡂࠨൗ")+str(mode)+l11l1lUK_Turk_No1 (u"ࠢࠧࡰࡤࡱࡪࡃࠢ൘")+urllib.quote_plus(name)+l11l1lUK_Turk_No1 (u"ࠣࠨࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴ࠽ࠣ൙")+str(description)+l11l1lUK_Turk_No1 (u"ࠤࠩ࡭ࡨࡵ࡮ࡪ࡯ࡤ࡫ࡪࡃࠢ൚")+urllib.quote_plus(l1l11l11UK_Turk_No1)
        ok=True
        l111l1lUK_Turk_No1=xbmcgui.ListItem(name, iconImage=l11l1lUK_Turk_No1 (u"ࠥࡈࡪ࡬ࡡࡶ࡮ࡷࡊࡴࡲࡤࡦࡴ࠱ࡴࡳ࡭ࠢ൛"), thumbnailImage=l1l11l11UK_Turk_No1)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠫ࡫ࡧ࡮ࡢࡴࡷࡣ࡮ࡳࡡࡨࡧࠪ൜"), fanart)
        l111l1lUK_Turk_No1.setProperty(l11l1lUK_Turk_No1 (u"ࠧࡏࡳࡑ࡮ࡤࡽࡦࡨ࡬ࡦࠤ൝"),l11l1lUK_Turk_No1 (u"ࠨࡴࡳࡷࡨࠦ൞"))
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=l111l1lUK_Turk_No1,isFolder=False)
        return ok