from libs import requests
import re


XHR = {'X-Requested-With': 'XMLHttpRequest'}
Default_Headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}#   <<<<<add HTTP headers to a request,

base_url = 'http://tvaddons.co/ad_api'
default_timeout = 10
special_path = 'http://indigo.tvaddons.co/installer/sources'

def search_addons(query):
    url = '/search_all'
    params = {'query': query}
    return _call(url, params=params)

def get_all_addons():
    url = '/show_all'
    return _call(url)

def get_types(query):
    url = '/addon_type'
    params = {'query': query}
    return _call(url, params=params)

def get_repos():
    url = '/repos'
    return _call(url)

def get_international():
    url = '/international'
    return _call(url)

def get_langs():
    url = '/lang_list'
    return _call(url)

def get_id(type):
    url = '/get_id'
    params = {'query': type}
    return _call(url, params=params)

# <<<<<<<<<<<Returns the Special Addon Ids<<<<<<<<<<<<<<<<
def special_addons(query):
    base = special_path
    if query == 'featured':
        area = '/featuredAddons.json'
    if query == 'live':
        area = '/livetvAddons.json'
    if query == 'playlists':
        area = '/playlistsAddons.json'
    if query == 'sports':
        area = '/sportsAddons.json'
    feat = []
    links = requests.get(base+area)
    link = links.json()
    for a in link['addons']:
        feat.append(a)
    return feat


def _call(url, params=None, headers=Default_Headers, verify_ssl=True, timeout=default_timeout):
    r = requests.get(base_url+url, params=params, headers=headers, verify=verify_ssl, allow_redirects=True, timeout=timeout)
    print '\t\tr = ' + str(r)
    print '\t\turl = ' + str(base_url+url)
    result = r.json()
    return result
