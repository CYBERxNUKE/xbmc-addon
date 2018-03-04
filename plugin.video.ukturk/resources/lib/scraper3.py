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
    string=l1l111UK_Turk_No1 (u"ࠬ࠭෩")
    print l1l111UK_Turk_No1 (u"࠭ࡸࡹࡺࡻࡼࡽࡾࡸࡹࡺࡻࡼࡽࡾࡸࡹࡺࡻࡼࠬ෪")
    link=l11111lUK_Turk_No1(l1l111UK_Turk_No1 (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰࡯ࡤࡱࡦ࡮ࡤ࠯ࡶࡹ࠳ࠧ෫")).replace(l1l111UK_Turk_No1 (u"ࠨ࡞ࡱࠫ෬"),l1l111UK_Turk_No1 (u"ࠩࠪ෭")).replace(l1l111UK_Turk_No1 (u"ࠪࡠࡹ࠭෮"),l1l111UK_Turk_No1 (u"ࠫࠬ෯"))
    l11lllll1lUK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"ࠬࡂࡴࡩࠢࡦࡰࡦࡹࡳ࠾ࠤ࡫ࡳࡲ࡫࠭ࡴࡶࡵࡩࡦࡳࡳࠣࡀࠫ࠲࠰ࡅࠩࡸ࡫ࡧ࡫ࡪࡺ࠭ࡤࡱࡱࡸࡪࡴࡴࠡࡵࡷࡽࡱ࡫࠱ࠣࡀࠪ෰")).findall(link)[0]
    #l11llll111UK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"࠭࠼ࡢࠢ࡫ࡶࡪ࡬࠽ࠣࠪ࠱࠯ࡄ࠯ࠢ࠿࠰࠮ࡃࡁ࡯࡭ࡨࠢࡶࡶࡨࡃࠢࠩ࠰࠮ࡃ࠮ࠨ࠮ࠬࡁ࠿ࡨ࡮ࡼࠠࡤ࡮ࡤࡷࡸࡃࠢࡩࡱࡰࡩࠥࡩࡥ࡭࡮ࠥࡂ࠳࠱࠿࠽ࡵࡳࡥࡳࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂ࠳࠱࠿࠽ࡵࡳࡥࡳࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂ࠳࠱࠿࠽࠱ࡤࡂࠬ෱")).findall(l11lllll1lUK_Turk_No1)
    l11lllllllUK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦ࡭ࡵ࡭ࡦ࠯ࡷ࡭ࡲ࡫ࠢ࠿ࠪ࠱࠯ࡄ࠯࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥ࡬ࡴࡳࡥ࠮ࡵࡷࡥࡹࡻࡳࠣࡀࠪෲ"),re.DOTALL).findall(l11lllll1lUK_Turk_No1)
    print l11lllllllUK_Turk_No1[0]
    for l11lllll11UK_Turk_No1 in l11lllllllUK_Turk_No1:
            date=re.compile(l1l111UK_Turk_No1 (u"ࠨ࠾ࡶࡴࡦࡴࠠࡤ࡮ࡤࡷࡸࡃࠢࡥࡣࡷࡩࠧࡄࠨ࠯࠭ࡂ࠭ࡁ࠵ࡳࡱࡣࡱࡂࠬෳ"),re.DOTALL).findall(l11lllll11UK_Turk_No1)[0]
            print date
            url=re.compile(l1l111UK_Turk_No1 (u"ࠩ࠿ࡥࠥ࡮ࡲࡦࡨࡀࠦ࠭࠴ࠫࡀࠫࠥࡂࠬ෴")).findall(l11lllll11UK_Turk_No1)[0]
            print url
            l1l1l1llUK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"ࠪࡀ࡮ࡳࡧࠡࡵࡵࡧࡂࠨࠨ࠯࠭ࡂ࠭ࠧࡄࠧ෵")).findall(l11lllll11UK_Turk_No1)[0]
            print l1l1l1llUK_Turk_No1
            home=url.split(l1l111UK_Turk_No1 (u"ࠫ࠲࠭෶"))[0]
            print home
    #https://l11llll11lUK_Turk_No1.tv/4657-l11llll1l1UK_Turk_No1-l11lll1l1lUK_Turk_No1-l11llll1llUK_Turk_No1-l11lll1ll1UK_Turk_No1-l1l111111lUK_Turk_No1-l1l1111111UK_Turk_No1-l11llllll1UK_Turk_No1-stream.html
    #for url,l1l1l1llUK_Turk_No1,home,l11lll1lllUK_Turk_No1 in l11llll111UK_Turk_No1:
    #return string
def l11111lUK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l1l111UK_Turk_No1 (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩ෷"), l1l111UK_Turk_No1 (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠤ࠭࡝ࡩ࡯ࡦࡲࡻࡸࠦࡎࡕࠢ࠴࠴࠳࠶ࠩࠡࡃࡳࡴࡱ࡫ࡗࡦࡤࡎ࡭ࡹ࠵࠵࠴࠹࠱࠷࠻ࠦࠨࡌࡊࡗࡑࡑ࠲ࠠ࡭࡫࡮ࡩࠥࡍࡥࡤ࡭ࡲ࠭ࠥࡉࡨࡳࡱࡰࡩ࠴࠻࠴࠯࠲࠱࠶࠽࠺࠰࠯࠹࠴ࠤࡘࡧࡦࡢࡴ࡬࠳࠺࠹࠷࠯࠵࠹ࠫ෸"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link