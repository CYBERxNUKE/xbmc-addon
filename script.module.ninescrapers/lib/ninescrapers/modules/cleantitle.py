# -*- coding: utf-8 -*-

"""
    Exodus Add-on
    ///Updated for Nine///

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
"""

import re
import unicodedata
from six import ensure_str, ensure_text, PY2
from six.moves.urllib_parse import unquote
from ninescrapers.modules import client


def get(title):
    if not title: return
    title = unquote(title)
    title = client.replaceHTMLCodes(title)
    title = title.replace('&', 'and').replace('_', '')
    title = normalize(title)
    title = re.sub(r'<.*?>', '', title).lower()
    title = re.sub(r'\[.*?\]', '', title)
    # title = re.sub(r'\n|([[].+?[]])|([(].+?[)])|\s(vs[.]|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\+|\?)|\s', '', title) # fuck it
    title = re.sub(r'[^\w]+', '', title)
    return title


def get_title(title, sep='.'):
    if not title: return
    title = unquote(title)
    title = client.replaceHTMLCodes(title)
    title = title.replace('&', 'and').replace('.html', '').replace('_', sep)
    title = normalize(title)
    title = re.sub('[^\w\%s]+' % sep, sep, title)
    title = re.sub('\%s{2,}' % sep, sep, title)
    title = title.strip(sep)
    return title


def geturl(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.lower()
    title = title.rstrip()
    try: title = title.translate(None, ':*?"\'\.<>|&!,')
    except: title = title.translate(str.maketrans('', '', ':*?"\'\.<>|&!,'))
    title = title.replace('/', '-')
    title = title.replace(' ', '-')
    title = title.replace('--', '-')
    title = title.replace('–', '-')
    title = title.replace('!', '')
    return title


def get_url(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.replace(' ', '%20').replace('–', '-').replace('!', '')
    return title


def get_gan_url(title):
    if not title: return
    title = title.lower()
    title = title.replace('-','+')
    title = title.replace(' + ', '+-+')
    title = title.replace(' ', '%20')
    return title


def get_query_(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.replace(' ', '_').replace("'", "_").replace('-', '_').replace('–', '_').replace(':', '').replace(',', '').replace('!', '')
    return title.lower()


def get_simple(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.lower()
    title = re.sub('(\d{4})', '', title)
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&').replace('–', '-')
    title = re.sub('\n|\(|\)|\[|\]|\{|\}|\s(vs|v[.])\s|(:|;|-|–|"|,|\'|\_|\.|\?)|\s', '', title).lower()
    return title


def getsearch(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.lower()
    title = re.sub('&#(\d+);', '', title)
    title = re.sub('(&#[0-9]+)([^;^0-9]+)', '\\1;\\2', title)
    title = title.replace('&quot;', '\"').replace('&amp;', '&').replace('–', '-')
    title = re.sub('\\\|/|-|–|:|;|!|\*|\?|"|\'|<|>|\|', '', title).lower()
    return title


def query(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.replace('\'', '').rsplit(':', 1)[0].rsplit(' -', 1)[0].replace('-', ' ').replace('–', ' ').replace('!', '')
    return title


def get_query(title):
    if not title: return
    title = ensure_str(title, errors='ignore')
    title = title.replace(':', '').replace("'", "").lower()
    return title


def normalize(title):
    try:
        if PY2:
            try: return title.decode('ascii').encode("utf-8")
            except: pass
            return str(''.join(c for c in unicodedata.normalize('NFKD', title.decode('utf-8')) if not unicodedata.combining(c)))
        return u''.join(c for c in unicodedata.normalize('NFKD', ensure_text(title)) if not unicodedata.combining(c))
    except:
        return title


def clean_search_query(url):
    url = url.replace('-','+').replace(' ', '+').replace('–', '+').replace('!', '')
    return url


def scene_title(title, year):
    title = normalize(title)
    title = ensure_str(title, errors='ignore')
    title = title.replace('&', 'and').replace('-', ' ').replace('–', ' ').replace('_', ' ').replace('/', ' ').replace('*', ' ').replace('.', ' ')
    title = re.sub('[^\w\s]+', '', title)
    title = re.sub(' {2,}', ' ', title).strip()
    if title.startswith('Birdman or') and year == '2014': title = 'Birdman'
    if title == 'Birds of Prey and the Fantabulous Emancipation of One Harley Quinn' and year == '2020': title = 'Birds of Prey'
    if title == "Roald Dahls The Witches" and year == '2020': title = 'The Witches'
    return title, year


def scene_tvtitle(title, year, season, episode):
    title = normalize(title)
    title = ensure_str(title, errors='ignore')
    title = title.replace('&', 'and').replace('-', ' ').replace('–', ' ').replace('_', ' ').replace('/', ' ').replace('*', ' ').replace('.', ' ')
    title = re.sub('[^\w\s]+', '', title)
    title = re.sub(' {2,}', ' ', title).strip()
    if title in ['The Haunting', 'The Haunting of Bly Manor', 'The Haunting of Hill House'] and year == '2018':
        if season == '1': title = 'The Haunting of Hill House'
        elif season == '2': title = 'The Haunting of Bly Manor'; year = '2020'; season = '1'
    if title in ['Cosmos', 'Cosmos A Spacetime Odyssey', 'Cosmos Possible Worlds'] and year == '2014':
        if season == '1': title = 'Cosmos A Spacetime Odyssey'
        elif season == '2': title = 'Cosmos Possible Worlds'; year = '2020'; season = '1'
    if 'Special Victims Unit' in title: title = title.replace('Special Victims Unit', 'SVU')
    if title == 'Cobra Kai' and year == '1984': year = '2018'
    #if title == 'The Office' and year == '2001': title = 'The Office UK'
    if title == 'The End of the F ing World': title = 'The End of the Fucking World'
    if title == 'M A S H': title = 'MASH'
    if title == 'Lupin' and year == '2021':
        if season == '1' and int(episode) > 5: season = '2'; episode = str(int(episode) - 5)
    return title, year, season, episode

