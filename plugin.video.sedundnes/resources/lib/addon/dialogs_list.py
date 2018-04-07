from threading import Thread, RLock

import xbmc,os
import xbmcaddon
import xbmcgui
from resources.lib.modules import control

import time

rt_timeout = 500

def select_ext(title, scraped_items):
    addonPath = xbmcaddon.Addon().getAddonInfo('path').decode('utf-8')
    dlg = SelectorDialog("DialogSelectList.xml", addonPath, title=title,
                         scraped_items=scraped_items)
    with ExtendedDialogHacks():
        dlg.doModal()
        selection = dlg.get_selection()
        del dlg
    return selection


class FanArtWindow(xbmcgui.WindowDialog):
    def __init__(self):
        control_background = xbmcgui.ControlImage(0, 0, 1280, 720, xbmcaddon.Addon().getAddonInfo('fanart'))
        self.addControl(control_background)
        fanart = xbmc.getInfoLabel('ListItem.Property(Fanart_Image)')
        if fanart and fanart != "Fanart_Image":
            control_fanart = xbmcgui.ControlImage(0, 0, 1280, 720, fanart)
            self.addControl(control_fanart)


class ExtendedDialogHacks(object):
    def __init__(self):
        self.active = False
        self.hide_progress = False
        self.hide_info = False
        self.autohidedialogs = False
        if self.autohidedialogs:
            self.hide_progress = False
            self.hide_info = False
        if not self.hide_progress and not self.hide_info:
            self.autohidedialogs = False

    def __enter__(self):
        self.active = True
        self.fanart_window = FanArtWindow()
        self.fanart_window.show()
        if self.autohidedialogs:
            Thread(target=self.background_task).start()

    def background_task(self):
        xbmc.sleep(1000)
        while not xbmc.abortRequested and self.active:
            if self.hide_progress:
                active_window = xbmcgui.getCurrentWindowDialogId()
                if active_window in [10101, 10151]:
                    xbmc.executebuiltin("Dialog.Close(%d, true)" % active_window)
            if self.hide_info:
                if xbmc.getCondVisibility("Window.IsActive(infodialog)"):
                    xbmc.executebuiltin('Dialog.Close(infodialog, true)')
            xbmc.sleep(100)

    def __exit__(self, exc_type, exc_value, traceback):
        self.active = False
        self.fanart_window.close()
        del self.fanart_window


class SelectorDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.title = kwargs['title']
        self.time_start = time.time()
        self.timer_active = True
        self.items = kwargs['scraped_items']
        self.selection = None
        self.insideIndex = -1
        self.completed_steps = 0
        self.selected = []
        self.thread = None
        self.lock = RLock()

    def get_selection(self):
        """ get final selection """
        self.timer_active = False
        return self.selected

    def onInit(self):
        self.label = self.getControl(1)
        self.label.setLabel(self.title)
        self.getControl(5).setVisible(False)
        try:
            self.list = self.getControl(6)
            self.list.controlLeft(self.list)
            self.list.controlRight(self.list)
            self.getControl(3).setVisible(False)
        except:
            self.list = self.getControl(6)
        self.thread = Thread(target=self._inside_root)
        self.thread.start()
        self.setFocus(self.list)

    def onAction(self, action):
        if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448,):
            if self.insideIndex == -1:
                self.timer_active = False
                self.close()
            else:
                self._inside_root(select=self.insideIndex)

    def onClick(self, controlID):

        if controlID == 6 or controlID == 3:
            num = self.list.getSelectedPosition()
            if num >= 0:
                if self.insideIndex == -1:
                    self._inside(num)
                else:
                    self.selection = self.items[self.insideIndex][1][num]
                    self.close()

    def onFocus(self, controlID):
        if controlID in (6, 61):
            self.setFocus(self.list)

    def _inside_root(self):
        with self.lock:
            self.setFocus(self.list)
            for links in self.items:
                self.providers_name = links['scraper']
                print ("Quality", links['quality'])
                quality = str(links['quality'])

                if "k" in quality.lower():  q_icon = "4k.png"
                if "1080" in quality:  q_icon = "1080.png"
                elif "HD" in quality: q_icon = "720.png"
                else: q_icon = "sd.png"

                if "torrent" in str(links['source']): q_icon = "torrent.png"
                if quality == '4k' or quality == '4K':  q_icon = "4k.png"
                try: info = links['info']
                except: info = ""
                if not info == "": info = " | %s" % info

                if links.get('debridonly', False) == True: label = '[I]DEB[/I] | %s | %s' % (quality, links['scraper'])
                else: label = '%s | %s' % (quality, links['scraper'])
                label2 = "[I]" + str(links['source']) + "[/I]"
                label = label + info
                listitem = xbmcgui.ListItem(label=label.upper(), label2=label2.upper())
                try:
                    pluginid = "plugin.video.sedundnes"
                    ARTDIR = xbmc.translatePath(os.path.join('special://home/addons/' + pluginid + '/resources/skins/icons' , ''))
                    icon = ARTDIR + q_icon
                    listitem.setIconImage(icon)
                except:
                    pass
                self.list.addItem(listitem)
            self.setFocus(self.list)

    def _inside(self, num):
        if num == -1:
            self._inside_root(select=self.insideIndex)
            return
        with self.lock:
            links = self.items[num]
            next = [y for x,y in enumerate(self.items) if x > num][:50]
            if len(links) >= 1:
                selected_link = links
                self.selected.append(selected_link)
                for next_scrape in next:
                                        self.selected.append(next_scrape)
                self.timer_active = False
                self.close()
                return
            self.insideIndex = num

    def step(self):
        self.completed_steps += 1
        progress = self.completed_steps * 100 / self.steps
        self.progress.setPercent(progress)
        self.label.setLabel(u"{0} - {1:d}% ({2}/{3})".format("Select Quality ", progress, self.completed_steps, self.steps))

    def _populate(self):
        selectedItem = None
        if self.insideIndex == -1:
            selectedIndex = self.list.getSelectedPosition()
        else:
            selectedIndex = self.insideIndex
        if selectedIndex >= 0:
            selectedItem = self.items[selectedIndex]

        self.items.extend(result)
        self.setFocus(self.list)


        if selectedItem is not None:
            selectedIndex = self.items.index(selectedItem)


            if self.insideIndex != -1:
                self.insideIndex = selectedIndex

        if self.insideIndex == -1:
            self._inside_root(select=selectedIndex)
            self.setFocus(self.list)
