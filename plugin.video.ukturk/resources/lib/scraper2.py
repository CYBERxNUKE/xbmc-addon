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
    string=l1l111UK_Turk_No1 (u"ࠨࠩ෗")
    link=l11111lUK_Turk_No1(l1l111UK_Turk_No1 (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࡦࡶ࡮ࡩࡦࡳࡧࡨ࠲ࡸࡩ࠯ࡧࡱࡲࡸࡧࡧ࡬࡭࠯࡯࡭ࡻ࡫࠭ࡴࡶࡵࡩࡦࡳࠢෘ"))
    events=re.compile(l1l111UK_Turk_No1 (u"ࠪࡀࡹࡪ࠾࠽ࡵࡳࡥࡳࠦࡣ࡭ࡣࡶࡷࡂࠨࡳࡱࡱࡵࡸ࠲࡯ࡣࡰࡰࠫ࠲࠰ࡅࠩ࠽࠱ࡷࡶࡃ࠭ෙ"),re.DOTALL).findall(link)
    for event in events:
        l1l11111l1UK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"ࠫࡁࡺࡤ࠿ࠪ࠱࠯ࡄ࠯࠼ࡣࡴࠫ࠲࠰ࡅࠩ࠽࠱ࡷࡨࡃ࠭ේ")).findall(event)
        for day,date in l1l11111l1UK_Turk_No1:
            day=l1l111UK_Turk_No1 (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠࠫෛ")+day+l1l111UK_Turk_No1 (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨො")
            date=date.replace(l1l111UK_Turk_No1 (u"ࠧ࠿ࠩෝ"),l1l111UK_Turk_No1 (u"ࠨࠩෞ"))
        time=re.compile(l1l111UK_Turk_No1 (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨ࡭ࡢࡶࡦ࡬ࡹ࡯࡭ࡦࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࠦ࠹࠹࠻࠴࠶࠶࠾ࡪࡴࡴࡴ࠮ࡹࡨ࡭࡬࡮ࡴ࠻ࡤࡲࡰࡩࡁࡦࡰࡰࡷ࠱ࡸ࡯ࡺࡦ࠼ࠣ࠽ࡵࡾࠢ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡶࡧࡂࠬෟ")).findall(event)[0]
        time=l1l111UK_Turk_No1 (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡦࡱࡻࡥ࡞ࠪࠪ෠")+time+l1l111UK_Turk_No1 (u"ࠫ࠮ࡡ࠯ࡄࡑࡏࡓࡗࡣࠧ෡")
        l1l1111l1lUK_Turk_No1=re.compile(l1l111UK_Turk_No1 (u"ࠬࡂࡡࠡࡵࡷࡽࡱ࡫࠽ࠣࡶࡨࡼࡹ࠳ࡤࡦࡥࡲࡶࡦࡺࡩࡰࡰ࠽ࡲࡴࡴࡥࠡࠣ࡬ࡱࡵࡵࡲࡵࡣࡱࡸࡀࡩ࡯࡭ࡱࡵ࠾ࠨ࠻࠴࠶࠶࠸࠸ࡀࠨࠠࡩࡴࡨࡪࡂࠨࠨ࠯࠭ࡂ࠭ࠧࠦࡴࡢࡴࡪࡩࡹࡃࠢࡠࡤ࡯ࡥࡳࡱࠢ࠿ࠪ࠱࠯ࡄ࠯࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࠩ෢")).findall(event)
        for url,l1l1111l11UK_Turk_No1 in l1l1111l1lUK_Turk_No1:
            url=url
            l1l1111l11UK_Turk_No1=l1l1111l11UK_Turk_No1
        string=string+l1l111UK_Turk_No1 (u"࠭࡜࡯࠾࡬ࡸࡪࡳ࠾࡝ࡰ࠿ࡸ࡮ࡺ࡬ࡦࡀࠨࡷࡁ࠵ࡴࡪࡶ࡯ࡩࡃࡢ࡮࠽ࡵࡳࡳࡷࡺࡳࡥࡧࡹ࡭ࡱࡄࠥࡴ࠾࠲ࡷࡵࡵࡲࡵࡵࡧࡩࡻ࡯࡬࠿࡞ࡱࠫ෣")%(day+l1l111UK_Turk_No1 (u"ࠧࠡࠩ෤")+time+l1l111UK_Turk_No1 (u"ࠨࠢ࠰ࠤࠬ෥")+l1l1111l11UK_Turk_No1,url)
        string=string+l1l111UK_Turk_No1 (u"ࠩ࠿ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄࡉ࡮ࡣࡪࡩࡍ࡫ࡲࡦ࠾࠲ࡸ࡭ࡻ࡭ࡣࡰࡤ࡭ࡱࡄ࡜࡯࠾ࡩࡥࡳࡧࡲࡵࡀࡩࡥࡳࡧࡲࡵ࠾࠲ࡪࡦࡴࡡࡳࡶࡁࡠࡳࡂ࠯ࡪࡶࡨࡱࡃࡢ࡮ࠨ෦")
    return string
def l11111lUK_Turk_No1(url):
    req = urllib2.Request(url)
    req.add_header(l1l111UK_Turk_No1 (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧ෧"), l1l111UK_Turk_No1 (u"ࠫࡒࡵࡺࡪ࡮࡯ࡥ࠴࠻࠮࠱࡛ࠢࠫ࡮ࡴࡤࡰࡹࡶࠤࡓ࡚ࠠ࠲࠲࠱࠴࠮ࠦࡁࡱࡲ࡯ࡩ࡜࡫ࡢࡌ࡫ࡷ࠳࠺࠹࠷࠯࠵࠹ࠤ࠭ࡑࡈࡕࡏࡏ࠰ࠥࡲࡩ࡬ࡧࠣࡋࡪࡩ࡫ࡰࠫࠣࡇ࡭ࡸ࡯࡮ࡧ࠲࠹࠹࠴࠰࠯࠴࠻࠸࠵࠴࠷࠲ࠢࡖࡥ࡫ࡧࡲࡪ࠱࠸࠷࠼࠴࠳࠷ࠩ෨"))
    response = urllib2.urlopen(req)
    link=response.read()
    return link