# -*- coding: utf-8 -*-

from resources.lib.modules import control

NETFLIX_ENABLED = (control.condVisibility('System.HasAddon(plugin.video.netflix)') == True and control.setting('netflix') == 'true')
PRIME_ENABLED = (control.condVisibility('System.HasAddon(plugin.video.amazon-test)') == True and control.setting('prime') == 'true')
HBO_ENABLED = (control.condVisibility('System.HasAddon(slyguy.hbo.max)') == True and control.setting('hbo.max') == 'true')
DISNEY_ENABLED = (control.condVisibility('System.HasAddon(slyguy.disney.plus)') == True and control.setting('disney.plus') == 'true')
IPLAYER_ENABLED = (control.condVisibility('System.HasAddon(plugin.video.iplayerwww)') == True and control.setting('iplayer') == 'true')
CURSTREAM_ENABLED = (control.condVisibility('System.HasAddon(slyguy.curiositystream)') == True and control.setting('curstream') == 'true')
HULU_ENABLED = (control.condVisibility('System.HasAddon(slyguy.hulu)') == True and control.setting('hulu') == 'true')
PARAMOUNT_ENABLED = (control.condVisibility('System.HasAddon(slyguy.paramount.plus)') == True and control.setting('paramount') == 'true')
CRACKLE_ENABLED = (control.condVisibility('System.HasAddon(plugin.video.crackle)') == True and control.setting('crackle') == 'true')

SCRAPER_INIT = any(e for e in [NETFLIX_ENABLED, PRIME_ENABLED, HBO_ENABLED, DISNEY_ENABLED, IPLAYER_ENABLED, CURSTREAM_ENABLED, HULU_ENABLED, PARAMOUNT_ENABLED, CRACKLE_ENABLED])
