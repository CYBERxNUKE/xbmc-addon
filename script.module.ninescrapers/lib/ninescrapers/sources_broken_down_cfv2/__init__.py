# -*- coding: UTF-8 -*-

import os
from six import iteritems
from . import en, en_Torrent, el


scraper_source = os.path.dirname(__file__)
__all__ = [x[1] for x in os.walk(os.path.dirname(__file__))][0]


##--en--##
hoster_source = en.sourcePath
hoster_providers = en.__all__


##--en_Torrent--##
torrent_source = en_Torrent.sourcePath
torrent_providers = en_Torrent.__all__


##--Foreign Providers--##
greek_providers = el.__all__


##--All Foreign Providers--##
foreign_providers = {'el': greek_providers}
all_foreign_providers = []
for key, value in iteritems(foreign_providers):
    all_foreign_providers += value


##--All Providers--##
total_providers = {'en': hoster_providers, 'en_Torrent': torrent_providers, 'el': greek_providers}
all_providers = []
for key, value in iteritems(total_providers):
    all_providers += value