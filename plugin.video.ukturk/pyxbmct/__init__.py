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
l11l1lUK_Turk_No1 (u"ࠥࠦࠧࠓࠊࡑࡻ࡛ࡆࡒࡉࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡲࡵࡤࡶ࡮ࡨࠑࠏࠓࠊࡑࡻ࡛ࡆࡒࡉࡴࠡ࡫ࡶࠤࡦࠦ࡭ࡪࡰ࡬࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡧࡱࡵࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡋࡰࡦ࡬ࠤ࠭࡞ࡂࡎࡅࠬࠤࡕࡿࡴࡩࡱࡱࠤࡦࡪࡤࡰࡰࡶࠑࠏࡽࡩࡵࡪࠣࡥࡷࡨࡩࡵࡴࡤࡶࡾࠦࡕࡊࠢࡰࡥࡩ࡫ࠠࡰࡨࠣࡇࡴࡴࡴࡳࡱ࡯ࡷࠥ࠳ࠠࡥࡧࡦࡩࡳࡪࡡ࡯ࡶࡶࠤࡴ࡬ࠠࡹࡤࡰࡧ࡬ࡻࡩ࠯ࡅࡲࡲࡹࡸ࡯࡭ࠢࡦࡰࡦࡹࡳ࠯ࠏࠍࡘ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡹࡸ࡫ࡳࠡ࡫ࡰࡥ࡬࡫ࠠࡵࡧࡻࡸࡺࡸࡥࡴࠢࡩࡶࡴࡳࠠࡌࡱࡧ࡭ࠥࡉ࡯࡯ࡨ࡯ࡹࡪࡴࡣࡦࠢࡶ࡯࡮ࡴ࠮ࠎࠌࠐࠎࡑ࡯ࡣࡦࡰࡦࡩ࠿ࠦࡇࡑࡎࠣࡺ࠳࠹ࠠࡩࡶࡷࡴ࠿࠵࠯ࡸࡹࡺ࠲࡬ࡴࡵ࠯ࡱࡵ࡫࠴ࡲࡩࡤࡧࡱࡷࡪࡹ࠯ࡨࡲ࡯࠲࡭ࡺ࡭࡭ࠏࠍࠦࠧࠨౘ")
from addonwindow import (AddonWindowError, Label, FadeLabel, TextBox, Image, Button, RadioButton, Edit, List, Slider,
                         BlankFullWindow, BlankDialogWindow, AddonDialogWindow, AddonFullWindow)