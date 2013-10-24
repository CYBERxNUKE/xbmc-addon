import urllib , urllib2 , sys , re , xbmcplugin , xbmcgui , xbmcaddon , xbmc , os
import datetime
import time
if 64 - 64: i11iIiiIii
if 65 - 65: O0 / iIii1I11I1II1 % OoooooooOO - i1IIi
if 73 - 73: II111iiii

OO0oIIIii = 'plugin.video.footballreplays'
IiII1IiiIiI1 = xbmcaddon . Addon ( id = 'plugin.video.footballreplays' )
iIiiiI1IiI1I1 = IiII1IiiIiI1 . getSetting ( "maxVideoQuality" )
o0OoOoOO00 = [ "480p" , "720p" , "1080p" ]
iIiiiI1IiI1I1 = o0OoOoOO00 [ int ( iIiiiI1IiI1I1 ) ]
if 27 - 27: OOOo0 / Oo - Ooo00oOo00o . I1IiI
if IiII1IiiIiI1 . getSetting ( 'visitor_ga' ) == '' :
 from random import randint
 IiII1IiiIiI1 . setSetting ( 'visitor_ga' , str ( randint ( 0 , 0x7fffffff ) ) )
 if 73 - 73: OOooOOo / ii11ii1ii
O00ooOO = "1.0.2"
I1iII1iiII = "Football Replays"
iI1Ii11111iIi = "UA-35537758-1"
if 41 - 41: I1II1
if 100 - 100: iII1iII1i1iiI % iiIIIII1i1iI % iiI11iii111 % i1I1Ii1iI1ii
def II1iI ( ) :
 i1iIii1Ii1II ( 'Full Matches' , 'url' , 3 , '' , '1' )
 i1iIii1Ii1II ( 'Search Team' , 'url' , 4 , '' , '1' )
 i1iIii1Ii1II ( 'Highlights' , 'url' , 5 , '' , '1' )
 i1I1Iiii1111 ( 'movies' , 'main' )
 #setView is setting the automatic view.....first is what section "movies"......second is what you called it in the settings xml  
 if 22 - 22: OOo000 . O0I11i1i11i1I
 if 31 - 31: i11iI / i11iI + O0I11i1i11i1I - i11iI . OoooooooOO
def oO0 ( ) :
 IIIi1i1I = OOoOoo00oo ( 'http://livefootballvideo.com/fullmatch' )
 iiI11 = 'rel="bookmark".+?img src="(.+?)".+?<a href="(.+?)" title=".+?">(.+?)</a></h2><p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 print OOooO
 for OOoO00o , II111iiiiII , oOoOo00oOo , Ooo00O00O0O0O , OooO0OO , iiiIi in OOooO :
  IiIIIiI1I1 = '%s/%s/%s' % ( OooO0OO , Ooo00O00O0O0O , iiiIi )
  OoO000 = '%s-[COLOR yellow][%s][/COLOR]' % ( oOoOo00oOo , IiIIIiI1I1 )
  i1iIii1Ii1II ( OoO000 , II111iiiiII , 1 , OOoO00o , '' )
 i1iIii1Ii1II ( 'Next Page >>' , 'url' , 2 , '' , '1' )
 i1I1Iiii1111 ( 'movies' , 'main' )
 if 42 - 42: I1II1 - i1IIi / i11iIiiIii + iII1iII1i1iiI + Ooo00oOo00o
 if 17 - 17: I1II1 . Oo . ii11ii1ii
def IIi ( page ) :
 i1I11 = int ( page ) + 1
 IIIi1i1I = OOoOoo00oo ( 'http://livefootballvideo.com/fullmatch/page/' + str ( i1I11 ) )
 iiI11 = 'rel="bookmark".+?img src="(.+?)".+?<a href="(.+?)" title=".+?">(.+?)</a></h2><p class="postmetadata longdate" rel=".+?">(.+?)/(.+?)/(.+?)</p>'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 print OOooO
 for OOoO00o , II111iiiiII , oOoOo00oOo , Ooo00O00O0O0O , OooO0OO , iiiIi in OOooO :
  IiIIIiI1I1 = '%s/%s/%s' % ( OooO0OO , Ooo00O00O0O0O , iiiIi )
  OoO000 = '%s-[COLOR yellow][%s][/COLOR]' % ( oOoOo00oOo , IiIIIiI1I1 )
  i1iIii1Ii1II ( OoO000 , II111iiiiII , 1 , OOoO00o , '' )
 i1iIii1Ii1II ( 'Next Page >>' , 'url' , 2 , '' , i1I11 )
 i1I1Iiii1111 ( 'movies' , 'default' )
 if 26 - 26: i11iIiiIii
def OO0O00 ( name , url ) :
 IIIi1i1I = OOoOoo00oo ( url )
 if "www.youtube.com/embed/" in IIIi1i1I :
  iiI11 = 'youtube.com/embed/(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  ii1 = OOooO [ 0 ]
  OOoO00o = 'http://i.ytimg.com/vi/%s/0.jpg' % ii1 . replace ( '?rel=0' , '' )
  url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % ii1 . replace ( '?rel=0' , '' )
  i1iIii1Ii1II ( name + ' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , OOoO00o , '' )
 if "dailymotion.com" in IIIi1i1I :
  iiI11 = 'src="http://www.dailymotion.com/embed/video/(.+?)\?.+?"></iframe>'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , o0oO0o00oo ( url ) , '' )
 if "http://videa" in IIIi1i1I :
  iiI11 = 'http://videa.+?v=(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]VIDEA[/COLOR]' , url , 200 , '' , '' )
   if 32 - 32: Oo * O0 % I1II1 % iiI11iii111 . OOo000
 if "rutube.ru" in IIIi1i1I :
  iiI11 = 'ttp://rutube.ru/video/embed/(.+?)\?'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  print OOooO
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]RUTUBE[/COLOR]' , url , 200 , '' , '' )
 if "playwire" in IIIi1i1I :
  iiI11 = 'cdn.playwire.com.+?config=(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]PLAYWIRE[/COLOR]' , url , 200 , '' , '' )
 if "vk.com" in IIIi1i1I :
  iiI11 = '<iframe src="http://vk.com/(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]VK.COM[/COLOR]' , 'http://vk.com/' + url , 200 , '' , '' )
   if 61 - 61: i11iI
   if 79 - 79: Oo + OOOo0 - i1I1Ii1iI1ii
   
from xbmcads import ads
ads . ADDON_ADVERTISE ( OO0oIIIii )
   
def oO00O00o0OOO0 ( ) :
 IIIi1i1I = OOoOoo00oo ( 'http://livefootballvideo.com/highlights' )
 iiI11 = 'team home column">(.+?)&nbsp;.+?src="(.+?)"></div>.+?&nbsp;(.+?)</div>.+?"column"><a href="(.+?)"'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 for Ii1iIIIi1ii , o0oo0o0O00OO , o0oO , II111iiiiII in OOooO :
  oOoOo00oOo = '%s vs %s' % ( Ii1iIIIi1ii , o0oO )
  OOoO00o = 'http://livefootballvideo.com%s' % o0oo0o0O00OO
  i1iIii1Ii1II ( oOoOo00oOo , II111iiiiII , 7 , OOoO00o , '' )
 i1iIii1Ii1II ( 'Next Page >>' , 'url' , 6 , '' , '1' )
 i1I1Iiii1111 ( 'movies' , 'default' )
 if 48 - 48: iiIIIII1i1iI + iiIIIII1i1iI / II111iiii / iIii1I11I1II1
def i1iiI11I ( page ) :
 iiii = int ( page ) + 1
 IIIi1i1I = OOoOoo00oo ( 'http://livefootballvideo.com/highlights/page/' + str ( iiii ) )
 iiI11 = 'team home column">(.+?)&nbsp;.+?src="(.+?)"></div>.+?&nbsp;(.+?)</div>.+?"column"><a href="(.+?)"'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 for Ii1iIIIi1ii , o0oo0o0O00OO , o0oO , II111iiiiII in OOooO :
  oOoOo00oOo = '%s vs %s' % ( Ii1iIIIi1ii , o0oO )
  OOoO00o = 'http://livefootballvideo.com%s' % o0oo0o0O00OO
  i1iIii1Ii1II ( oOoOo00oOo , II111iiiiII , 7 , OOoO00o , '' )
 i1iIii1Ii1II ( 'Next Page >>' , 'url' , 6 , '' , iiii )
 i1I1Iiii1111 ( 'movies' , 'default' )
 if 54 - 54: ii11ii1ii * iII1iII1i1iiI
 if 13 - 13: OOo000 + I1IiI - OoooooooOO + O0I11i1i11i1I . i1I1Ii1iI1ii + Ooo00oOo00o
 if 8 - 8: iIii1I11I1II1 . OOOo0 - iIii1I11I1II1 * iiI11iii111
def OOOO ( name , url ) :
 IIIi1i1I = OOoOoo00oo ( url )
 if "www.youtube.com/embed/" in IIIi1i1I :
  iiI11 = 'youtube.com/embed/(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  ii1 = OOooO [ 0 ]
  OOoO00o = 'http://i.ytimg.com/vi/%s/0.jpg' % ii1 . replace ( '?rel=0' , '' )
  url = 'plugin://plugin.video.youtube/?path=root/video&action=play_video&videoid=%s' % ii1 . replace ( '?rel=0' , '' )
  i1iIii1Ii1II ( name + ' - [COLOR red]YOUTUBE[/COLOR]' , url , 200 , OOoO00o , '' )
 if "dailymotion.com" in IIIi1i1I :
  iiI11 = 'src="http://www.dailymotion.com/embed/video/(.+?)\?.+?"></iframe>'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]DAILYMOTION[/COLOR]' , url , 200 , o0oO0o00oo ( url ) , '' )
 if "http://videa" in IIIi1i1I :
  iiI11 = 'http://videa.+?v=(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]VIDEA[/COLOR]' , url , 200 , '' , '' )
   if 87 - 87: I1II1 / iiIIIII1i1iI - i1IIi * iII1iII1i1iiI / OoooooooOO . O0
 if "rutube.ru" in IIIi1i1I :
  iiI11 = 'rutube.ru/video/embed/(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]RUTUBE[/COLOR]' , url , 200 , '' , '' )
   if 1 - 1: II111iiii - iiIIIII1i1iI / iiIIIII1i1iI
 if "playwire" in IIIi1i1I :
  iiI11 = 'cdn.playwire.com.+?config=(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]PLAYWIRE[/COLOR]' , url , 200 , '' , '' )
 if "vk.com" in IIIi1i1I :
  iiI11 = '<iframe src="(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  for url in OOooO :
   i1iIii1Ii1II ( name + ' - [COLOR red]VK.COM[/COLOR]' , url , 200 , '' , '' )
   if 46 - 46: iiI11iii111 * iII1iII1i1iiI - Ooo00oOo00o * I1II1 - O0I11i1i11i1I
def oo0 ( ) :
 o00 = ''
 OooOooo = xbmc . Keyboard ( o00 , 'Search Football Replays' )
 OooOooo . doModal ( )
 if OooOooo . isConfirmed ( ) :
  o00 = OooOooo . getText ( ) . replace ( ' ' , '+' )
  if o00 == None :
   return False
 IIIi1i1I = O000oo0O ( 'http://www.google.com/cse?cx=partner-pub-9069051203647610:8413886168&ie=UTF-8&q=%s&sa=Search&ref=livefootballvideo.com/highlights' % o00 )
 OOooO = re . compile ( '" href="(.+?)" onmousedown=".+?">(.+?)</a>' ) . findall ( IIIi1i1I )
 for II111iiiiII , OOOOi11i1 in OOooO :
  import HTMLParser
  IIIii1II1II = HTMLParser . HTMLParser ( ) . unescape ( OOOOi11i1 )
  oOoOo00oOo = IIIii1II1II . replace ( '<b>' , '' ) . replace ( '</b>' , '' )
  i1iIii1Ii1II ( oOoOo00oOo , II111iiiiII , 1 , '' , '' )
 i1I1Iiii1111 ( 'movies' , 'default' )
 if 42 - 42: iiI11iii111 + I1II1
 if 76 - 76: O0I11i1i11i1I - Ooo00oOo00o
def o0oO0o00oo ( url ) :
 try :
  import json
  oOooOOo00Oo0O = OOoOoo00oo ( 'https://api.dailymotion.com/video/%s?fields=thumbnail_large_url' % url )
  O00oO = json . loads ( oOooOOo00Oo0O )
  I11i1I1I = O00oO [ 'thumbnail_large_url' ]
  return I11i1I1I
 except :
  return ''
  if 83 - 83: ii11ii1ii / i11iI
  if 49 - 49: OOooOOo
def IIii1Ii1 ( id ) :
 oOooOOo00Oo0O = OOoOoo00oo ( "http://www.dailymotion.com/embed/video/" + id )
 if oOooOOo00Oo0O . find ( '"statusCode":410' ) > 0 or oOooOOo00Oo0O . find ( '"statusCode":403' ) > 0 :
  xbmc . executebuiltin ( 'XBMC.Notification(Info:,Not Found (DailyMotion)!,5000)' )
  return ""
 else :
  I1II11IiII = re . compile ( '"stream_h264_hd1080_url":"(.+?)"' , re . DOTALL ) . findall ( oOooOOo00Oo0O )
  OOO0OOo = re . compile ( '"stream_h264_hd_url":"(.+?)"' , re . DOTALL ) . findall ( oOooOOo00Oo0O )
  I1I111 = re . compile ( '"stream_h264_hq_url":"(.+?)"' , re . DOTALL ) . findall ( oOooOOo00Oo0O )
  i11iiI111I = re . compile ( '"stream_h264_url":"(.+?)"' , re . DOTALL ) . findall ( oOooOOo00Oo0O )
  II11i1iIiII1 = re . compile ( '"stream_h264_ld_url":"(.+?)"' , re . DOTALL ) . findall ( oOooOOo00Oo0O )
  II111iiiiII = ""
  if I1II11IiII and iIiiiI1IiI1I1 == "1080p" :
   II111iiiiII = urllib . unquote_plus ( I1II11IiII [ 0 ] ) . replace ( "\\" , "" )
  elif OOO0OOo and ( iIiiiI1IiI1I1 == "720p" or iIiiiI1IiI1I1 == "1080p" ) :
   II111iiiiII = urllib . unquote_plus ( OOO0OOo [ 0 ] ) . replace ( "\\" , "" )
  elif I1I111 :
   II111iiiiII = urllib . unquote_plus ( I1I111 [ 0 ] ) . replace ( "\\" , "" )
  elif i11iiI111I :
   II111iiiiII = urllib . unquote_plus ( i11iiI111I [ 0 ] ) . replace ( "\\" , "" )
  elif II11i1iIiII1 :
   II111iiiiII = urllib . unquote_plus ( II11i1iIiII1 [ 0 ] ) . replace ( "\\" , "" )
  return II111iiiiII
  if 17 - 17: OOo000
  if 62 - 62: iIii1I11I1II1 * I1IiI
  if 26 - 26: i1I1Ii1iI1ii . O0I11i1i11i1I
def oOOOOo0 ( id ) :
 print id
 IIIi1i1I = OOoOoo00oo ( 'http://rutube.ru/api/play/trackinfo/%s/?format=xml' % str ( id ) )
 iiI11 = '<m3u8>(.+?)</m3u8>'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 return OOooO [ 0 ]
 if 20 - 20: i1IIi + ii11ii1ii - i11iI
def IiI11iII1 ( id ) :
 IIIi1i1I = OOoOoo00oo ( 'http://videa.hu/flvplayer_get_video_xml.php?v=%s&m=0' % str ( id ) )
 oOoOo00oOo = [ ]
 II111iiiiII = [ ]
 iiI11 = 'version quality="(.+?)" video_url="(.+?)"'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 for IIII11I1I , OOO0o in OOooO :
  oOoOo00oOo . append ( IIII11I1I . title ( ) )
  II111iiiiII . append ( OOO0o )
 return II111iiiiII [ xbmcgui . Dialog ( ) . select ( 'Please Select Resolution' , oOoOo00oOo ) ]
 if 30 - 30: iIii1I11I1II1 / i11iI - O0I11i1i11i1I - II111iiii % i1I1Ii1iI1ii
def IIi1i11111 ( url ) :
 print url
 IIIi1i1I = OOoOoo00oo ( url . replace ( 'amp;' , '' ) )
 print IIIi1i1I
 oOoOo00oOo = [ ]
 url = [ ]
 iiI11 = '"url(.+?)":"(.+?)"'
 OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
 for IIII11I1I , OOO0o in OOooO :
  oOoOo00oOo . append ( IIII11I1I + 'p' )
  url . append ( OOO0o . replace ( '\/' , '/' ) )
 return url [ xbmcgui . Dialog ( ) . select ( 'Please Select Resolution' , oOoOo00oOo ) ]
 if 81 - 81: i11iIiiIii % I1IiI - iII1iII1i1iiI
 if 68 - 68: O0I11i1i11i1I % i1IIi . OOo000 . ii11ii1ii
 if 92 - 92: i1I1Ii1iI1ii . O0I11i1i11i1I
def i1i ( name , url , iconimage ) :
 if 'YOUTUBE' in name :
  IIIi1i1I = str ( url )
 elif 'VIDEA' in name :
  IIIi1i1I = IiI11iII1 ( url )
 elif 'VK.COM' in name :
  IIIi1i1I = IIi1i11111 ( url )
  if 50 - 50: OOo000
 elif 'RUTUBE' in name :
  try :
   i11I1iIiII = 'http://rutube.ru/api/play/trackinfo/%s/?format=xml' % url . replace ( '_ru' , '' )
   print i11I1iIiII
   IIIi1i1I = OOoOoo00oo ( i11I1iIiII )
   iiI11 = '<m3u8>(.+?)</m3u8>'
   OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
   if OOooO :
    IIIi1i1I = OOooO [ 0 ]
   else :
    oO00o0 = xbmcgui . Dialog ( )
    oO00o0 . ok ( "Football Replays" , '' , 'Sorry Video Is Private' , '' )
    return
  except :
   oO00o0 = xbmcgui . Dialog ( )
   oO00o0 . ok ( "Football Replays" , '' , 'Sorry Video Is Private' , '' )
   return
 elif 'PLAYWIRE' in name :
  IIIi1i1I = OOoOoo00oo ( url )
  iiI11 = '"src":"(.+?)"'
  OOooO = re . compile ( iiI11 , re . DOTALL ) . findall ( IIIi1i1I )
  if OOooO :
   IIIi1i1I = OOooO [ 0 ]
 elif 'DAILYMOTION' in name :
  IIIi1i1I = IIii1Ii1 ( url )
 OOoo0O = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 OOoo0O . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 OOoo0O . setProperty ( "IsPlayable" , "true" )
 Oo0ooOo0o = xbmc . PlayList ( xbmc . PLAYLIST_VIDEO )
 Oo0ooOo0o . clear ( )
 Oo0ooOo0o . add ( IIIi1i1I , OOoo0O )
 xbmc . Player ( ) . play ( Oo0ooOo0o )
 if 22 - 22: iIii1I11I1II1 / i11iIiiIii * iIii1I11I1II1 * II111iiii . iII1iII1i1iiI / i11iIiiIii
 if 2 - 2: OOOo0 / O0 / OOooOOo % I1IiI % iiI11iii111
 if 52 - 52: OOooOOo
def OOoOoo00oo ( url ) :
 o0OO0oOO0O0 = urllib2 . Request ( url )
 o0OO0oOO0O0 . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 iiiIIi1II = urllib2 . urlopen ( o0OO0oOO0O0 )
 IIIi1i1I = iiiIIi1II . read ( )
 iiiIIi1II . close ( )
 return IIIi1i1I
 if 61 - 61: iiIIIII1i1iI
 if 86 - 86: iiIIIII1i1iI % I1IiI / OOOo0 / I1IiI
def O000oo0O ( url ) :
 o0OO0oOO0O0 = urllib2 . Request ( url )
 o0OO0oOO0O0 . add_header ( 'User-Agent' , "Magic Browser" )
 iiiIIi1II = urllib2 . urlopen ( o0OO0oOO0O0 )
 IIIi1i1I = iiiIIi1II . read ( )
 iiiIIi1II . close ( )
 return IIIi1i1I
 if 42 - 42: Ooo00oOo00o
 if 67 - 67: O0I11i1i11i1I . i1I1Ii1iI1ii . O0
 if 10 - 10: ii11ii1ii % ii11ii1ii - iIii1I11I1II1 / iII1iII1i1iiI + iiI11iii111
def OOOOoOoo0O0O0 ( ) :
 OOOo00oo0oO = [ ]
 IIiIi1iI = sys . argv [ 2 ]
 if len ( IIiIi1iI ) >= 2 :
  i1IiiiI1iI = sys . argv [ 2 ]
  i1iIi = i1IiiiI1iI . replace ( '?' , '' )
  if ( i1IiiiI1iI [ len ( i1IiiiI1iI ) - 1 ] == '/' ) :
   i1IiiiI1iI = i1IiiiI1iI [ 0 : len ( i1IiiiI1iI ) - 2 ]
  ooOOoooooo = i1iIi . split ( '&' )
  OOOo00oo0oO = { }
  for II1I in range ( len ( ooOOoooooo ) ) :
   O0i1II1Iiii1I11 = { }
   O0i1II1Iiii1I11 = ooOOoooooo [ II1I ] . split ( '=' )
   if ( len ( O0i1II1Iiii1I11 ) ) == 2 :
    OOOo00oo0oO [ O0i1II1Iiii1I11 [ 0 ] ] = O0i1II1Iiii1I11 [ 1 ]
    if 9 - 9: ii11ii1ii / Oo - OOOo0 / OoooooooOO / iIii1I11I1II1 - OOooOOo
 return OOOo00oo0oO
 if 91 - 91: i1I1Ii1iI1ii % i1IIi % iIii1I11I1II1
 if 20 - 20: iII1iII1i1iiI % iiI11iii111 / iiI11iii111 + iiI11iii111
def III1IiiI ( dateString ) :
 try :
  return datetime . datetime . fromtimestamp ( time . mktime ( time . strptime ( dateString . encode ( 'utf-8' , 'replace' ) , "%Y-%m-%d %H:%M:%S" ) ) )
 except :
  return datetime . datetime . today ( ) - datetime . timedelta ( days = 1 )
  if 31 - 31: OOooOOo . OOOo0
  if 46 - 46: i1I1Ii1iI1ii
def IIIII11I1IiI ( ) :
 if 16 - 16: iIii1I11I1II1
 oOooOOOoOo = 60 * 60
 i1Iii1i1I = 2 * oOooOOOoOo
 if 91 - 91: ii11ii1ii + OOOo0 . iII1iII1i1iiI * ii11ii1ii + OOOo0 * Oo
 O000OOOOOo = datetime . datetime . today ( )
 Iiii1i1 = III1IiiI ( IiII1IiiIiI1 . getSetting ( 'ga_time' ) )
 OO = O000OOOOOo - Iiii1i1
 oo000o = OO . days
 iiIi1IIi1I = OO . seconds
 if 84 - 84: i11iI * II111iiii + Oo
 O0ooO0Oo00o = ( oo000o > 0 ) or ( iiIi1IIi1I > i1Iii1i1I )
 if not O0ooO0Oo00o :
  return
  if 77 - 77: iIii1I11I1II1 * Ooo00oOo00o
 IiII1IiiIiI1 . setSetting ( 'ga_time' , str ( O000OOOOOo ) . split ( '.' ) [ 0 ] )
 oOooOo0 ( )
 if 38 - 38: O0I11i1i11i1I
 if 84 - 84: iIii1I11I1II1 % i1I1Ii1iI1ii / iIii1I11I1II1 % iiIIIII1i1iI
def ii ( utm_url ) :
 OOooooO0Oo = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
 import urllib2
 try :
  o0OO0oOO0O0 = urllib2 . Request ( utm_url , None ,
 { 'User-Agent' : OOooooO0Oo }
 )
  iiiIIi1II = urllib2 . urlopen ( o0OO0oOO0O0 ) . read ( )
 except :
  print ( "GA fail: %s" % utm_url )
 return iiiIIi1II
 if 91 - 91: OOooOOo . iIii1I11I1II1 / I1II1 + i1IIi
def I1i ( group , name ) :
 try :
  try :
   from hashlib import md5
  except :
   from md5 import md5
  from random import randint
  import time
  from urllib import unquote , quote
  from os import environ
  from hashlib import sha1
  OOOOO0oo0O0O0 = IiII1IiiIiI1 . getSetting ( 'visitor_ga' )
  oO = "http://www.google-analytics.com/__utm.gif"
  if not group == "None" :
   oO0O0o0Oooo = oO + "?" + "utmwv=" + O00ooOO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmt=" + "event" + "&utme=" + quote ( "5(" + I1iII1iiII + "*" + group + "*" + name + ")" ) + "&utmp=" + quote ( I1iII1iiII ) + "&utmac=" + iI1Ii11111iIi + "&utmcc=__utma=%s" % "." . join ( [ "1" , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , "2" ] )
   if 5 - 5: i11iI - II111iiii - OoooooooOO % iiI11iii111 + OOOo0 * iIii1I11I1II1
   if 37 - 37: OOo000 % i11iI + I1IiI + OOooOOo * iiIIIII1i1iI % O0
   if 61 - 61: OOOo0 - iII1iII1i1iiI . I1II1 / iII1iII1i1iiI + Oo
   if 5 - 5: i11iI + i11iI / O0 * Oo - iII1iII1i1iiI % i11iI
   if 15 - 15: i11iIiiIii % iiI11iii111 . Oo + ii11ii1ii
   if 61 - 61: Oo * ii11ii1ii % Oo - i1IIi - iIii1I11I1II1
   if 74 - 74: ii11ii1ii + II111iiii / Ooo00oOo00o
   try :
    print "============================ POSTING TRACK EVENT ============================"
    ii ( oO0O0o0Oooo )
   except :
    print "============================  CANNOT POST TRACK EVENT ============================"
  if name == "None" :
   oOo0O0Oo00oO = oO + "?" + "utmwv=" + O00ooOO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( I1iII1iiII ) + "&utmac=" + iI1Ii11111iIi + "&utmcc=__utma=%s" % "." . join ( [ "1" , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , "2" ] )
   if 7 - 7: OOo000 * O0I11i1i11i1I % iiI11iii111 - OOooOOo
   if 13 - 13: iiI11iii111 . i11iIiiIii
   if 56 - 56: ii11ii1ii % O0 - OOOo0
   if 100 - 100: iiI11iii111 - O0 % I1II1 * iII1iII1i1iiI + OOOo0
   if 88 - 88: OoooooooOO - Ooo00oOo00o * O0 * OoooooooOO . OoooooooOO
  else :
   if group == "None" :
    oOo0O0Oo00oO = oO + "?" + "utmwv=" + O00ooOO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( I1iII1iiII + "/" + name ) + "&utmac=" + iI1Ii11111iIi + "&utmcc=__utma=%s" % "." . join ( [ "1" , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , "2" ] )
    if 33 - 33: O0I11i1i11i1I + i1I1Ii1iI1ii * I1II1 / iIii1I11I1II1 - OOOo0
    if 54 - 54: O0I11i1i11i1I / iII1iII1i1iiI . I1II1 % i1I1Ii1iI1ii
    if 57 - 57: i11iIiiIii . ii11ii1ii - iiI11iii111 - I1II1 + I1IiI
    if 63 - 63: I1IiI * i1I1Ii1iI1ii
    if 69 - 69: O0 . Ooo00oOo00o
   else :
    oOo0O0Oo00oO = oO + "?" + "utmwv=" + O00ooOO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( I1iII1iiII + "/" + group + "/" + name ) + "&utmac=" + iI1Ii11111iIi + "&utmcc=__utma=%s" % "." . join ( [ "1" , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , "2" ] )
    if 49 - 49: OOOo0 - iiIIIII1i1iI
    if 74 - 74: iIii1I11I1II1 * ii11ii1ii + I1IiI / i1IIi / II111iiii . Oo
    if 62 - 62: OoooooooOO * OOOo0
    if 58 - 58: I1IiI % OOooOOo
    if 50 - 50: O0I11i1i11i1I . OOooOOo
    if 97 - 97: O0 + I1IiI
  print "============================ POSTING ANALYTICS ============================"
  ii ( oOo0O0Oo00oO )
  if 89 - 89: OOooOOo + Ooo00oOo00o * iiIIIII1i1iI * iiI11iii111
 except :
  print "================  CANNOT POST TO ANALYTICS  ================"
  if 37 - 37: OoooooooOO - O0 - OOooOOo
  if 77 - 77: iII1iII1i1iiI * iIii1I11I1II1
def oOooOo0 ( ) :
 oO00oOOoooO = int ( xbmc . getInfoLabel ( "System.BuildVersion" ) [ 0 : 2 ] )
 if oO00oOOoooO < 12 :
  if xbmc . getCondVisibility ( 'system.platform.osx' ) :
   if xbmc . getCondVisibility ( 'system.platform.atv2' ) :
    IiIi11iI = '/var/mobile/Library/Preferences'
   else :
    IiIi11iI = os . path . join ( os . path . expanduser ( '~' ) , 'Library/Logs' )
  elif xbmc . getCondVisibility ( 'system.platform.ios' ) :
   IiIi11iI = '/var/mobile/Library/Preferences'
  elif xbmc . getCondVisibility ( 'system.platform.windows' ) :
   IiIi11iI = xbmc . translatePath ( 'special://home' )
   Oo0O00O000 = os . path . join ( IiIi11iI , 'xbmc.log' )
   i11I1IiII1i1i = open ( Oo0O00O000 , 'r' ) . read ( )
  elif xbmc . getCondVisibility ( 'system.platform.linux' ) :
   IiIi11iI = xbmc . translatePath ( 'special://home/temp' )
  else :
   IiIi11iI = xbmc . translatePath ( 'special://logpath' )
  Oo0O00O000 = os . path . join ( IiIi11iI , 'xbmc.log' )
  i11I1IiII1i1i = open ( Oo0O00O000 , 'r' ) . read ( )
  OOooO = re . compile ( 'Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?' ) . findall ( i11I1IiII1i1i )
 elif oO00oOOoooO > 11 :
  print '======================= more than ===================='
  IiIi11iI = xbmc . translatePath ( 'special://logpath' )
  Oo0O00O000 = os . path . join ( IiIi11iI , 'xbmc.log' )
  i11I1IiII1i1i = open ( Oo0O00O000 , 'r' ) . read ( )
  OOooO = re . compile ( 'Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?' ) . findall ( i11I1IiII1i1i )
 else :
  i11I1IiII1i1i = 'Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
  OOooO = re . compile ( 'Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?' ) . findall ( i11I1IiII1i1i )
 print '==========================   ' + I1iII1iiII + ' ' + O00ooOO + '  =========================='
 try :
  from hashlib import md5
 except :
  from md5 import md5
 from random import randint
 import time
 from urllib import unquote , quote
 from os import environ
 from hashlib import sha1
 import platform
 OOOOO0oo0O0O0 = IiII1IiiIiI1 . getSetting ( 'visitor_ga' )
 for oo , I1111i in OOooO :
  if re . search ( '12' , oo [ 0 : 2 ] , re . IGNORECASE ) :
   oo = "Frodo"
  if re . search ( '11' , oo [ 0 : 2 ] , re . IGNORECASE ) :
   oo = "Eden"
  if re . search ( '13' , oo [ 0 : 2 ] , re . IGNORECASE ) :
   oo = "Gotham"
  print oo
  print I1111i
  oO = "http://www.google-analytics.com/__utm.gif"
  oO0O0o0Oooo = oO + "?" + "utmwv=" + O00ooOO + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmt=" + "event" + "&utme=" + quote ( "5(APP LAUNCH*" + oo + "*" + I1111i + ")" ) + "&utmp=" + quote ( I1iII1iiII ) + "&utmac=" + iI1Ii11111iIi + "&utmcc=__utma=%s" % "." . join ( [ "1" , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , OOOOO0oo0O0O0 , "2" ] )
  if 14 - 14: iII1iII1i1iiI / OOooOOo
  if 32 - 32: OOOo0 * Oo
  if 78 - 78: iII1iII1i1iiI - OoooooooOO - ii11ii1ii / i11iI / II111iiii
  if 29 - 29: OOOo0 % OOOo0
  if 94 - 94: iIii1I11I1II1 / Oo % i1I1Ii1iI1ii * i1I1Ii1iI1ii * II111iiii
  if 29 - 29: Ooo00oOo00o + I1IiI / OOooOOo / iII1iII1i1iiI * iIii1I11I1II1
  if 62 - 62: iII1iII1i1iiI / I1II1 - Ooo00oOo00o . iiIIIII1i1iI
  try :
   print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
   ii ( oO0O0o0Oooo )
  except :
   print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================"
   if 11 - 11: ii11ii1ii . Ooo00oOo00o * OOo000 * OoooooooOO + i11iI
   if 33 - 33: O0 * OOooOOo - O0I11i1i11i1I % O0I11i1i11i1I
   if 18 - 18: O0I11i1i11i1I / Oo * O0I11i1i11i1I + O0I11i1i11i1I * i11iIiiIii * ii11ii1ii
IIIII11I1IiI ( )
if 11 - 11: i11iI / I1IiI - OOo000 * OoooooooOO + OoooooooOO . I1IiI
if 26 - 26: iiI11iii111 % ii11ii1ii
def i1iIii1Ii1II ( name , url , mode , iconimage , page ) :
 o00Oo0oooooo = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&iconimage=" + urllib . quote_plus ( iconimage ) + "&page=" + str ( page )
 O0oO0 = True
 OOoo0O = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 OOoo0O . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 if mode == 200 :
  O0oO0 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o00Oo0oooooo , listitem = OOoo0O , isFolder = False )
 else :
  O0oO0 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = o00Oo0oooooo , listitem = OOoo0O , isFolder = True )
 return O0oO0
 if 7 - 7: OOOo0
def I1ii1iIiii1I ( name , url , iconimage , description ) :
 O0oO0 = True
 OOoo0O = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 OOoo0O . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description } )
 OOoo0O . setProperty ( "IsPlayable" , "true" )
 O0oO0 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = OOoo0O , isFolder = False )
 return O0oO0
 if 42 - 42: OOooOOo + i1IIi - iiI11iii111 / OOo000
 if 9 - 9: O0 % O0 - OOooOOo
 if 51 - 51: OOOo0 . iIii1I11I1II1 - ii11ii1ii / O0
def i1I1Iiii1111 ( content , viewType ) :
 if 52 - 52: OOooOOo + O0 + i1I1Ii1iI1ii + Oo % i1I1Ii1iI1ii
 if content :
  xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , content )
 if IiII1IiiIiI1 . getSetting ( 'auto-view' ) == 'true' :
  xbmc . executebuiltin ( "Container.SetViewMode(%s)" % IiII1IiiIiI1 . getSetting ( viewType ) )
  if 75 - 75: OOOo0 . i11iI . O0 * O0I11i1i11i1I
  if 4 - 4: iiI11iii111 % I1II1 * Ooo00oOo00o
i1IiiiI1iI = OOOOoOoo0O0O0 ( )
II111iiiiII = None
oOoOo00oOo = None
o0O0OOOOoOO0 = None
OOoO00o = None
iiO0oOo00o = None
if 81 - 81: OOo000 % i1IIi . iIii1I11I1II1
if 4 - 4: i11iIiiIii % Ooo00oOo00o % i1IIi / OOo000
try :
 II111iiiiII = urllib . unquote_plus ( i1IiiiI1iI [ "url" ] )
except :
 pass
try :
 oOoOo00oOo = urllib . unquote_plus ( i1IiiiI1iI [ "name" ] )
except :
 pass
try :
 OOoO00o = urllib . unquote_plus ( i1IiiiI1iI [ "iconimage" ] )
except :
 pass
try :
 o0O0OOOOoOO0 = int ( i1IiiiI1iI [ "mode" ] )
except :
 pass
try :
 iiO0oOo00o = int ( i1IiiiI1iI [ "page" ] )
except :
 pass
 if 6 - 6: i1I1Ii1iI1ii / OOOo0 % iII1iII1i1iiI - OOOo0
print "Mode: " + str ( o0O0OOOOoOO0 )
print "URL: " + str ( II111iiiiII )
print "Name: " + str ( oOoOo00oOo )
print "IconImage: " + str ( OOoO00o )
if 31 - 31: iII1iII1i1iiI
if 23 - 23: O0I11i1i11i1I . OOo000
if 92 - 92: I1IiI + O0I11i1i11i1I * iiI11iii111 % OOOo0
if o0O0OOOOoOO0 == None or II111iiiiII == None or len ( II111iiiiII ) < 1 :
 print ""
 II1iI ( )
 if 42 - 42: Oo
elif o0O0OOOOoOO0 == 1 :
 OO0O00 ( oOoOo00oOo , II111iiiiII )
 if 76 - 76: OOOo0 * i1I1Ii1iI1ii % O0I11i1i11i1I
elif o0O0OOOOoOO0 == 2 :
 IIi ( iiO0oOo00o )
 if 57 - 57: iIii1I11I1II1 - i1IIi / O0I11i1i11i1I - O0 * OoooooooOO % II111iiii
elif o0O0OOOOoOO0 == 3 :
 oO0 ( )
 if 68 - 68: OoooooooOO * iiIIIII1i1iI % I1IiI - OOo000
elif o0O0OOOOoOO0 == 4 :
 oo0 ( )
 if 34 - 34: O0I11i1i11i1I . iIii1I11I1II1 * I1IiI * I1II1 / O0I11i1i11i1I / ii11ii1ii
elif o0O0OOOOoOO0 == 5 :
 oO00O00o0OOO0 ( )
 if 78 - 78: Oo - OOooOOo / I1IiI
elif o0O0OOOOoOO0 == 6 :
 i1iiI11I ( iiO0oOo00o )
 if 10 - 10: i1I1Ii1iI1ii + Oo * ii11ii1ii + iIii1I11I1II1 / O0I11i1i11i1I / ii11ii1ii
elif o0O0OOOOoOO0 == 7 :
 OOOO ( oOoOo00oOo , II111iiiiII )
 if 42 - 42: OOOo0
elif o0O0OOOOoOO0 == 200 :
 i1i ( oOoOo00oOo , II111iiiiII , OOoO00o )
 if 38 - 38: iII1iII1i1iiI + II111iiii % i11iI % I1IiI - iiI11iii111 / OoooooooOO
 if 73 - 73: OOooOOo * O0 - i11iIiiIii
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
