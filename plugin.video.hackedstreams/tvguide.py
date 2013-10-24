import urllib,urllib2,sys,re,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os,time,datetime



ADDON = xbmcaddon.Addon(id='plugin.video.offside')
baseurl='http://www.bleb.org/tv/data/listings/0/'

    
def OPEN_URL(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"}) 
    con = urllib2.urlopen( req )
    link= con.read()
    return link


    
def offset_time():
    quality = ADDON.getSetting('timefrom')
    if quality == '0':
        return '-12'
    elif quality == '1':
        return '-11'
    elif quality == '2':
        return '-10'
    elif quality == '3':
        return '-9'
    elif quality == '4':
        return '-8'
    elif quality == '5':
        return '-7'
    elif quality == '6':
        return '-6'
    elif quality == '7':
        return '-5'
    elif quality == '8':
        return '-4'
    elif quality == '9':
        return '-3'
    elif quality == '10':
        return '-2'
    elif quality == '11':
        return '-1'
    elif quality == '12':
        return '0'
    elif quality == '13':
        return '+1'
    elif quality == '14':
        return '+2'
    elif quality == '15':
        return '+3'
    elif quality == '16':
        return '+4'
    elif quality == '17':
        return '+5'
    elif quality == '18':
        return '+6'
    elif quality == '19':
        return '+7'
    elif quality == '20':
        return '+8'
    elif quality == '21':
        return '+9'
    elif quality == '22':
        return '+10'
    elif quality == '23':
        return '+11'
    elif quality == '24':
        return '+12'
        
        
        
def offset_gmt():
    quality = ADDON.getSetting('gmtfrom')
    if quality == '0':
        return '-12'
    elif quality == '1':
        return '-11'
    elif quality == '2':
        return '-10'
    elif quality == '3':
        return '-9'
    elif quality == '4':
        return '-8'
    elif quality == '5':
        return '-7'
    elif quality == '6':
        return '-6'
    elif quality == '7':
        return '-5'
    elif quality == '8':
        return '-4'
    elif quality == '9':
        return '-3'
    elif quality == '10':
        return '-2'
    elif quality == '11':
        return '-1'
    elif quality == '12':
        return '0'
    elif quality == '13':
        return '+1'
    elif quality == '14':
        return '+2'
    elif quality == '15':
        return '+3'
    elif quality == '16':
        return '+4'
    elif quality == '17':
        return '+5'
    elif quality == '18':
        return '+6'
    elif quality == '19':
        return '+7'
    elif quality == '20':
        return '+8'
    elif quality == '21':
        return '+9'
    elif quality == '22':
        return '+10'
    elif quality == '23':
        return '+11'
    elif quality == '24':
        return '+12'
        
    


def return_url(name):
    if 'Sky Action' in name:
        url=baseurl+'sky_movies_action_thriller.xml'	
    elif 'Sky Comedy' in name:
        url=baseurl+'sky_movies_comedy.xml'	
    elif 'Sky Drama' in name:
        url=baseurl+'sky_movies_drama.xml'	
    elif 'Sky Family' in name:
        url=baseurl+'sky_movies_family.xml'	
    elif 'Sky Modern Greats' in name:
        url=baseurl+'sky_movies_modern_greats.xml'	
    elif 'Sky Premiere' in name:
        url=baseurl+'sky_movies_premiere.xml'	
    elif 'Sky SciFi/Horror' in name:
        url=baseurl+'sky_movies_sci-fi_horror.xml'	
    elif 'Sky Sports 1' in name:
        url=baseurl+'sky_sports1.xml'	
    elif 'Sky Sports 2' in name:
        url=baseurl+'sky_sports2.xml'	
    elif 'Sky Sports 3' in name:
        url=baseurl+'sky_sports3.xml'	
    elif 'Sky Sports F1' in name:
        url=baseurl+'sky_sports_f1.xml'	
    elif 'Sky Sports News' in name:
        url=baseurl+'sky_sports_news.xml'	
    elif 'Sky Thriller' in name:
        url=baseurl+'sky_movies_crime_thriller.xml'
    else:
        url='None Found'
    return url

    


def tvguide(name):
    url=return_url(name)
    if 'Al Jazeera' in name:
	    For_Name=name
	    url    =  'http://www.en.aljazeerasport.tv/fragment/aljazeera/fragments/components/ajax/channelList/channel/plus%s/maxRecords/0'%(name.split('+')[1])	
	    link   =  OPEN_URL(url).replace('\n','').replace('  ','')
	    link   =  link.split('<h')[1]
	    pattern='<td class="eventsCell hardAlign">(.+?)</td'
	    match = re.compile(pattern, re.M|re.DOTALL).findall(link)
	    return ' - '+match[0]
	        
    elif not 'None Found' in url:
    
        forOffset_gmt=offset_gmt()
        if '+' in forOffset_gmt:
        
            Z       =   forOffset_gmt.split('+')[1]
            t       =   datetime.datetime.today()- datetime.timedelta(hours = int(Z))
            t_hour  =   t - datetime.timedelta(hours = 1)
            
        elif '-' in forOffset_gmt:
        
            Z       =   forOffset_gmt.split('-')[1]
            t       =   datetime.datetime.today()+ datetime.timedelta(hours = int(Z))
            t_hour  =   t - datetime.timedelta(hours = 1)
             
        elif '-' in forOffset_gmt:
            t   =   datetime.datetime.today()+ datetime.timedelta(hours = int(Z))
            t_hour =   t - datetime.timedelta(hours = 1)
            
        else:
            t = datetime.datetime.today()
            t_hour =   datetime.datetime.today() - datetime.timedelta(hours = 1)
            
        link=OPEN_URL(url)
        link=link.split('<programme>')
        name ='<start>'+t.strftime('%H')
        _name ='<start>'+t_hour.strftime('%H')
        for p in link:
            if _name in p:
                match=re.compile('<title>(.+?)</title>').findall(p)
                return ' - '+match[0].replace('amp;','').strip()
            else:
                if name in p:
                    match=re.compile('<title>(.+?)</title>').findall(p)
                    return ' - '+match[0].replace('amp;','').strip()
    else:
        return ''

        
def fulltvguide(name):
    url=return_url(name)
    if not 'None Found' in url:
        return url
    else:
        return ''
        

            
