"""

    Copyright (C) 2018, TonyH

    --June 16 2018, Added Hesgoal time to the top of the page.
    Added racing section--

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

    -------------------------------------------------------------

    Usage Examples:

<dir>
<title>HesGoal Games</title>
<hesgoal>games</hesgoal>
</dir>

"""    

import requests,re,json,os
import koding
import __builtin__
import xbmc,xbmcaddon
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode
from time import gmtime, strftime

CACHE_TIME = 3600  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class HesGoal(Plugin):
    name = "hesgoal"

    def process_item(self, item_xml):
        if "<hesgoal>" in item_xml:
            item = JenItem(item_xml)
            if "games" in item.get("hesgoal", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "get_hesgoal_games",
                    'url': item.get("hesgoal", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
                result_item["properties"] = {
                    'fanart_image': result_item["fanart"]
                }
                result_item['fanart_small'] = result_item["fanart"]
                return result_item


@route(mode='get_hesgoal_games', args=["url"])
def get_game(url):
    xml = ""
    try:    
        url = "http://www.hesgoal.com/"        
        headers = {'User_Agent':User_Agent}
        html = requests.get(url,headers=headers).content
        block1 = re.compile('<h2>Football News</h2>(.+?)<a href="http://www.hesgoal.com/league/11/Football_News">More Football News</a>',re.DOTALL).findall(html)
        site_hour = strftime("%H", gmtime())
        site_hour2 = int(site_hour)+2
        if site_hour2 == 25:
            site_hour2 = 1
        if site_hour2 == 26:
            site_hour2 = 2
        if site_hour2 == 27:
            site_hour2 = 3                         
        site_hour3 = str(site_hour2)
        site_minute = strftime("%M", gmtime())
        site_time = site_hour3+":"+site_minute
        xml += "<item>"\
               "<title>[COLOR blue]Hesgoal Time GMT+2 = (%s)[/COLOR]</title>"\
               "<thumbnail>http://www.logotypes101.com/logos/997/AD71A2CC84DD8DDE7932F9BC585926E1/Sports.png</thumbnail>"\
               "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
               "<link></link>"\
               "</item>" % (site_time)         
        match1 = re.compile('<a href="(.+?)".+?src="(.+?)".+?alt="(.+?)".+?href=.+?<p>(.+?)</p>',re.DOTALL).findall(str(block1))
        for link, image, name,time in match1:
            if "Djorkaeff" in name:
                break
            html2=requests.get(link,headers=headers).content
            match2 = re.compile('<center><iframe.+?src="(.+?)"',re.DOTALL).findall(html2)
            for url2 in match2:
                url2 = "http:"+url2
                url3 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url="+url2+"|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
                xml += "<plugin>"\
                       "<title>%s : %s</title>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link>%s</link>"\
                       "</plugin>" % (name,time,image,url3)
        block2 = re.compile('<h2>Racing News</h2>(.+?)<a href="http://www.hesgoal.com/league/12/Racing_News">More Racing News</a>',re.DOTALL).findall(html)
        match2 = re.compile('<a href="(.+?)".+?src="(.+?)".+?alt="(.+?)".+?href=.+?<p>(.+?)</p>',re.DOTALL).findall(str(block2))
        for link, image, name,time in match2:
            if "Hamilton leaves" in name:
                break
            html3=requests.get(link,headers=headers).content
            match3 = re.compile('<center><iframe.+?src="(.+?)"',re.DOTALL).findall(html3)
            for url4 in match3:
                url4 = "http:"+url4
                url5 = "plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url="+url4+"|User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
                xml += "<plugin>"\
                       "<title>%s : %s</title>"\
                       "<thumbnail>%s</thumbnail>"\
                       "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                       "<link>%s</link>"\
                       "</plugin>" % (name,time,image,url5)                                       
        if not xml:
            xml += "<item>"\
                   "<title>[B]----No Games at this time----[/B]</title>"\
                   "<thumbnail></thumbnail>"\
                   "<fanart>http://sportz4you.com/blog/wp-content/uploads/2016/01/0b46b20.jpg</fanart>"\
                   "<link></link>"\
                   "</item>"                                
    except:
        pass
    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type()) 
              

def remove_non_ascii(text):
    return unidecode(text)
           
            