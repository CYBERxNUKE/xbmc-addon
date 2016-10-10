# -*- coding: utf-8 -*-
'''
    script.matchcenter - Football information for Kodi
    A program addon that can be mapped to a key on your remote to display football information.
    Livescores, Event details, Line-ups, League tables, next and previous matches by team. Follow what
    others are saying about the match in twitter.
    Copyright (C) 2016 enen92

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import shutil
import xml.etree.ElementTree as ET
from xbmcgui import Dialog, WindowXMLDialog
from threading import Timer
from common_addon import *

default = xbmc.translatePath('special://xbmc/system/keymaps/keyboard.xml')
userdata = xbmc.translatePath('special://userdata/keymaps')
gen_file = os.path.join(userdata, 'gen.xml')

### Key mapp            
def run():
    ## load mappings ##
    try:
        setup_keymap_folder()
    except Exception:
        pass

    defaultkeymap = read_keymap(default)
    userkeymap = []
    if os.path.exists(gen_file):
        try:
            userkeymap = read_keymap(gen_file)
        except Exception:
            pass
    newkey = KeyListener.record_key()

    if newkey:
        if os.path.exists(gen_file):
            shutil.copyfile(gen_file, gen_file + ".old")
            
        new = ('global', u'RunScript(script.matchcenter)', newkey)
        
        done = False
        if len(userkeymap) !=0:
            _userkeymap = list(userkeymap)
            _u = []
            for u in _userkeymap:
                _u.append(list(u))
            for u in _u:
                if u[2] == newkey:
                    u[0] = new[0]
                    u[1] = new[1]
                    done = True
                    break
        if done: 
            final_userkeymap = []
            for u in _u:
                final_userkeymap.append(tuple(u))
            write_keymap(final_userkeymap, gen_file)
        else:
            userkeymap.append(new)
            write_keymap(userkeymap, gen_file)
        xbmc.executebuiltin("Action(reloadkeymaps)")
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % (translate(32048), translate(32049), 1,os.path.join(addon_path,'icon.png')))

class KeyListener(WindowXMLDialog):
    TIMEOUT = 5

    def __new__(cls):
        #Krypton and above
        if int(xbmc.getInfoLabel("System.BuildVersion")[0:2]) < 17:
            return super(KeyListener, cls).__new__(cls, "DialogKaiToast.xml", "")
        #Below Krypton
        else:
            return super(KeyListener, cls).__new__(cls, "DialogNotification.xml", "")

    def __init__(self):
        self.key = None

    def onInit(self):
        try:
            self.getControl(401).addLabel(translate(32000))
            self.getControl(402).addLabel('%s %.0f %s' % (translate(32050),self.TIMEOUT,translate(32051)))
        except AttributeError:
            self.getControl(401).setLabel(translate(32000))
            self.getControl(402).setLabel('%s %.0f %s' % (translate(32050),self.TIMEOUT,translate(32051)))

    def onAction(self, action):
        code = action.getButtonCode()
        self.key = None if code == 0 else str(code)
        self.close()

    @staticmethod
    def record_key():
        dialog = KeyListener()
        timeout = Timer(KeyListener.TIMEOUT, dialog.close)
        timeout.start()
        dialog.doModal()
        timeout.cancel()
        key = dialog.key
        del dialog
        return key
        
def read_keymap(filename):
    ret = []
    with open(filename, 'r') as xml:
        tree = ET.iterparse(xml)
        for _, keymap in tree:
            for context in keymap:
                for device in context:
                    for mapping in device:
                        key = mapping.get('id') or mapping.tag
                        action = mapping.text
                        if action:
                            ret.append((context.tag.lower(), action.lower(), key.lower()))
    return ret
    
def setup_keymap_folder():
    if not os.path.exists(userdata):
        os.makedirs(userdata)
    else:
        #make sure there are no user defined keymaps
        for name in os.listdir(userdata):
            if name.endswith('.xml') and name != os.path.basename(gen_file):
                src = os.path.join(userdata, name)
                for i in xrange(100):
                    dst = os.path.join(userdata, "%s.bak.%d" % (name, i))
                    if os.path.exists(dst):
                        continue
                    shutil.move(src, dst)
                    #successfully renamed
                    break
                    
def write_keymap(keymap, filename):
    contexts = list(set([c for c, a, k in keymap]))
    builder = ET.TreeBuilder()
    builder.start("keymap", {})
    for context in contexts:
        builder.start(context, {})
        builder.start("keyboard", {})
        for c, a, k in keymap:
            if c == context:
                builder.start("key", {"id":k})
                builder.data(a)
                builder.end("key")
        builder.end("keyboard")
        builder.end(context)
    builder.end("keymap")
    element = builder.close()
    ET.ElementTree(element).write(filename, 'utf-8')