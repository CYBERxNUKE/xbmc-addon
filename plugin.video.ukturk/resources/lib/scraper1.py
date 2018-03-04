# coding: UTF-8
import sys
l11l1l1l1UK_Turk_No1 = sys.version_info [0] == 2
l1ll11l1lUK_Turk_No1 = 2048
l11l1ll1lUK_Turk_No1 = 7
def l1l111UK_Turk_No1 (l1111llUK_Turk_No1):
    global l1ll1l111UK_Turk_No1
    l1l11lll1UK_Turk_No1 = ord (l1111llUK_Turk_No1 [-1])
    l11ll11l1UK_Turk_No1 = l1111llUK_Turk_No1 [:-1]
    l11111l1UK_Turk_No1 = l1l11lll1UK_Turk_No1 % len (l11ll11l1UK_Turk_No1)
    l1l1lll1lUK_Turk_No1 = l11ll11l1UK_Turk_No1 [:l11111l1UK_Turk_No1] + l11ll11l1UK_Turk_No1 [l11111l1UK_Turk_No1:]
    if l11l1l1l1UK_Turk_No1:
        l1lll1lUK_Turk_No1 = unicode () .join ([unichr (ord (char) - l1ll11l1lUK_Turk_No1 - (l1l11lUK_Turk_No1 + l1l11lll1UK_Turk_No1) % l11l1ll1lUK_Turk_No1) for l1l11lUK_Turk_No1, char in enumerate (l1l1lll1lUK_Turk_No1)])
    else:
        l1lll1lUK_Turk_No1 = str () .join ([chr (ord (char) - l1ll11l1lUK_Turk_No1 - (l1l11lUK_Turk_No1 + l1l11lll1UK_Turk_No1) % l11l1ll1lUK_Turk_No1) for l1l11lUK_Turk_No1, char in enumerate (l1l1lll1lUK_Turk_No1)])
    return eval (l1lll1lUK_Turk_No1)
import urllib,urllib2,re,os
def scrape():
    string=l1l111UK_Turk_No1 (u"ࠨࠩ෉")
    link=l11111lUK_Turk_No1(l1l111UK_Turk_No1 (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡺࡻࡼ࠴ࡳࡱࡱࡵࡸࡸ࠳ࡳࡵࡴࡨࡥࡲ࠴࡮ࡦࡶ࠲ࡷࡨ࡮ࡥࡥࡷ࡯ࡩ࠳࡮ࡴ࡮࡮්ࠥ"))
    events=re.compile(l1l111UK_Turk_No1 (u"ࠪࡀࡵࡄ࠼ࡴࡲࡤࡲࠥࡹࡴࡺ࡮ࡨࡁ࠭࠴ࠫࡀࠫ࠿࠳ࡵࡄࠧ෋"),re.DOTALL).findall(link)
    for event in events:
        time=re.compile(l1l111UK_Turk_No1 (u"ࠫࡁࡹࡰࡢࡰࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦࡊࡋ࠶࠰࠱࠲࠾ࠦࡃ࠮࠮ࠬࡁࠬࡀ࠴ࡹࡰࡢࡰࡁࠫ෌")).findall(event)[0]
        time=l1l111UK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡨ࡬ࡶࡧࡠࠫ෍")+time+l1l111UK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨ෎")
        l1l1111l1lUK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"ࠧ࠽࠱ࡶࡴࡦࡴ࠾ࠡࠪ࠱࠯ࡄ࠯ࠠ࠮ࠢ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࠤࡹࡧࡲࡨࡧࡷࡁࠧࡥࡢ࡭ࡣࡱ࡯ࠧࡄ࠮ࠬࡁ࠿࠳ࡦࡄࠧා")).findall(event)
        for l1l1111l11UK_Turk_No1,url in l1l1111l1lUK_Turk_No1:
            url=url
            l1l1111l11UK_Turk_No1=l1l1111l11UK_Turk_No1
            l1l1111l11UK_Turk_No1=l1l1111l11UK_Turk_No1.replace(l1l111UK_Turk_No1 (u"ࠨ࠯ࠪැ"),l1l111UK_Turk_No1 (u"ࠩࡹࡷࠬෑ"))
        string=string+l1l111UK_Turk_No1 (u"ࠪࡠࡳࡂࡩࡵࡧࡰࡂࡡࡴ࠼ࡵ࡫ࡷࡰࡪࡄࠥࡴ࠾࠲ࡸ࡮ࡺ࡬ࡦࡀ࡟ࡲࡁࡹࡰࡰࡴࡷࡷࡩ࡫ࡶࡪ࡮ࡁࠩࡸࡂ࠯ࡴࡲࡲࡶࡹࡹࡤࡦࡸ࡬ࡰࡃࡢ࡮ࠨි")%(time+l1l111UK_Turk_No1 (u"ࠫࠥ࠳ࠠࠨී")+l1l1111l11UK_Turk_No1,url)
        string=string+l1l111UK_Turk_No1 (u"ࠬࡂࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀࡌࡱࡦ࡭ࡥࡉࡧࡵࡩࡁ࠵ࡴࡩࡷࡰࡦࡳࡧࡩ࡭ࡀ࡟ࡲࡁ࡬ࡡ࡯ࡣࡵࡸࡃ࡬ࡡ࡯ࡣࡵࡸࡁ࠵ࡦࡢࡰࡤࡶࡹࡄ࡜࡯࠾࠲࡭ࡹ࡫࡭࠿࡞ࡱࠫු")
    return string
def l11111lUK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l1l111UK_Turk_No1 (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪ෕"), l1l111UK_Turk_No1 (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠵࠵࠴࠰ࠪࠢࡄࡴࡵࡲࡥࡘࡧࡥࡏ࡮ࡺ࠯࠶࠵࠺࠲࠸࠼ࠠࠩࡍࡋࡘࡒࡒࠬࠡ࡮࡬࡯ࡪࠦࡇࡦࡥ࡮ࡳ࠮ࠦࡃࡩࡴࡲࡱࡪ࠵࠵࠵࠰࠳࠲࠷࠾࠴࠱࠰࠺࠵࡙ࠥࡡࡧࡣࡵ࡭࠴࠻࠳࠸࠰࠶࠺ࠬූ"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link