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
def l1ll11l1lUK_Turk_No1(name,url,l11llll1l1UK_Turk_No1):
    l111lUK_Turk_No1=l11l1lUK_Turk_No1 (u"ࠧࠨ೽")
    link=l1llll111UK_Turk_No1(url)
    match=re.compile(l11l1lUK_Turk_No1 (u"ࠨ࠾ࡧ࡭ࡻࠦࡣ࡭ࡣࡶࡷࡂࠨࡦ࡭ࡣࡪࡷࠧࡄࠨ࠯࠭ࡂ࠭ࡁࡪࡩࡷࠢࡦࡰࡦࡹࡳ࠾ࠤࡤࡨࡤࡺ࡯ࡱࠤࡁࠫ೾"),re.DOTALL).findall(link)[0]
    cat=re.compile(l11l1lUK_Turk_No1 (u"ࠩ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࡂࡁࡲࡩ࠿࠾࡬ࠤࡹ࡯ࡴ࡭ࡧࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡨࡲࡡࡴࡵࡀࠦ࠳࠱࠿ࠣࡀ࠿࠳࡮ࡄࠧ೿")).findall(match)
    for url,name in cat:
        url=l11l1lUK_Turk_No1 (u"ࠪ࡬ࡹࡺࡰ࠻ࠩഀ")+url
        string=l11l1lUK_Turk_No1 (u"ࠫࡁࡹࡴࡢࡴࡷࡂࠬഁ")+name+l11l1lUK_Turk_No1 (u"ࠬࡂࡳࡦࡲࡁࠫം")+url+l11l1lUK_Turk_No1 (u"࠭࠼ࡦࡰࡧࡂࠬഃ")
        l111lUK_Turk_No1=l111lUK_Turk_No1+string
    return l111lUK_Turk_No1
def l1llll111UK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l11l1lUK_Turk_No1 (u"ࠧࡖࡵࡨࡶ࠲ࡇࡧࡦࡰࡷࠫഄ"), l11l1lUK_Turk_No1 (u"ࠨࡏࡲࡾ࡮ࡲ࡬ࡢ࠱࠸࠲࠵ࠦࠨࡘ࡫ࡱࡨࡴࡽࡳࠡࡐࡗࠤ࠶࠶࠮࠱ࠫࠣࡅࡵࡶ࡬ࡦ࡙ࡨࡦࡐ࡯ࡴ࠰࠷࠶࠻࠳࠹࠶ࠡࠪࡎࡌ࡙ࡓࡌ࠭ࠢ࡯࡭ࡰ࡫ࠠࡈࡧࡦ࡯ࡴ࠯ࠠࡄࡪࡵࡳࡲ࡫࠯࠶࠶࠱࠴࠳࠸࠸࠵࠲࠱࠻࠶ࠦࡓࡢࡨࡤࡶ࡮࠵࠵࠴࠹࠱࠷࠻࠭അ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link