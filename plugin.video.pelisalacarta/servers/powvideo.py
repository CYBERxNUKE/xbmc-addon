# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para powvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from core import httptools
from lib import jsunpack

headers = [['User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0']]
host = "http://powvideo.net/"


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "<title>watch </title>" in data.lower():
        return False, "[powvideo] El archivo no existe o  ha sido borrado"
    if "el archivo ha sido borrado por no respetar" in data.lower():
        return False, "[powvideo] El archivo no existe o ha sido borrado por no respetar los Terminos de uso"
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    url = page_url.replace(host, "http://powvideo.xyz/iframe-") + "-954x562.html"

    referer = {'Referer': url.replace("iframe","preview")}
    data = httptools.downloadpage(url, headers=referer).data

    jj_encode = scrapertools.find_single_match(data, "(\w+=~\[\];.*?\)\(\)\)\(\);)")
    jj_decode = None
    jj_patron = None
    reverse = False
    splice = False
    if jj_encode:
        jj_decode = jjdecode(jj_encode)
    if jj_decode:
        jj_patron = scrapertools.find_single_match(jj_decode, "/([^/]+)/")
        if "(" not in jj_patron: jj_patron = "(" + jj_patron
        if ")" not in jj_patron: jj_patron += ")"

        jhex_decode = jhexdecode(jj_decode)
        if "reverse" in jhex_decode: reverse = True
        if "splice" in jhex_decode: splice = True

    matches = scrapertools.find_single_match(data, "<script type=[\"']text/javascript[\"']>(eval.*?)</script>")
    data = jsunpack.unpack(matches).replace("\\", "")

    data = scrapertools.find_single_match(data.replace('"', "'"), "sources\s*=[^\[]*\[([^\]]+)\]")
    matches = scrapertools.find_multiple_matches(data, "[src|file]:'([^']+)'")
    video_urls = []
    for video_url in matches:
        _hash = scrapertools.find_single_match(video_url, '\w{40,}')
        if splice:
            splice = eval(scrapertools.find_single_match(jhex_decode, "splice\((\d[^,]*),\d\);"))
            if reverse:
                h = list(_hash)
                h.pop(-splice - 1)
                _hash = "".join(h)
            else:
                h = list(_hash)
                h.pop(splice)
                _hash = "".join(h)

        if reverse:
            video_url = re.sub(r'\w{40,}', _hash[::-1], video_url)
        filename = scrapertools.get_filename_from_url(video_url)[-4:]
        if video_url.startswith("rtmp"):
            rtmp, playpath = video_url.split("vod/", 1)
            video_url = "%s playpath=%s swfUrl=%splayer6/jwplayer.flash.swf pageUrl=%s" % \
                        (rtmp + "vod/", playpath, host, page_url)
            filename = "RTMP"
        elif video_url.endswith(".m3u8"):
            video_url += "|User-Agent=" + headers[0][1]
        elif video_url.endswith("/v.mp4"):
            video_url_flv = re.sub(r'/v.mp4$', '/v.flv', video_url)
            video_urls.append([".flv" + " [powvideo]", re.sub(r'%s' % jj_patron, r'\1', video_url_flv)])

        video_urls.append([filename + " [powvideo]", re.sub(r'%s' % jj_patron, r'\1', video_url)])

    video_urls.sort(key=lambda x: x[0], reverse=True)
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra videos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://powvideo.net/sbb9ptsfqca2
    # http://powvideo.net/embed-sbb9ptsfqca2
    # http://powvideo.net/iframe-sbb9ptsfqca2
    # http://powvideo.net/preview-sbb9ptsfqca2
    patronvideos = 'powvideo.net/(?:embed-|iframe-|preview-|)([a-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[powvideo]"
        url = "http://powvideo.net/" + match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'powvideo'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve


def jjdecode(t):
    x = '0123456789abcdef'
    j = scrapertools.get_match(t, '^([^=]+)=')
    t = t.replace(j + '.', 'j.')

    t = re.sub(r'^.*?"\\""\+(.*?)\+"\\"".*?$', r'\1', t.replace('\\\\', '\\')) + '+""'
    t = re.sub('(\(!\[\]\+""\)\[j\._\$_\])', '"l"', t)
    t = re.sub(r'j\._\$\+', '"o"+', t)
    t = re.sub(r'j\.__\+', '"t"+', t)
    t = re.sub(r'j\._\+', '"u"+', t)

    p = scrapertools.find_multiple_matches(t, '(j\.[^\+]+\+)')
    for c in p:
        t = t.replace(c, c.replace('_', '0').replace('$', '1'))

    p = scrapertools.find_multiple_matches(t, 'j\.(\d{4})')
    for c in p:
        t = re.sub(r'j\.%s' % c, '"' + x[int(c, 2)] + '"', t)

    p = scrapertools.find_multiple_matches(t, '\\"\+j\.(001)\+j\.(\d{3})\+j\.(\d{3})\+')
    for c in p:
        t = re.sub(r'\\"\+j\.%s\+j\.%s\+j\.%s\+' % (c[0], c[1], c[2]), chr(int("".join(c), 2)) + '"+', t)

    p = scrapertools.find_multiple_matches(t, '\\"\+j\.(\d{3})\+j\.(\d{3})\+')
    for c in p:
        t = re.sub(r'\\"\+j\.%s\+j\.%s\+' % (c[0], c[1]), chr(int("".join(c), 2)) + '"+', t)

    p = scrapertools.find_multiple_matches(t, 'j\.(\d{3})')
    for c in p:
        t = re.sub(r'j\.%s' % c, '"' + str(int(c, 2)) + '"', t)

    r = re.sub(r'"\+"|\\\\', '', t[1:-1])

    return r


def jhexdecode(t):
    r = re.sub(r'_\d+x\w+x(\d+)', 'var_' + r'\1', t)
    r = re.sub(r'_\d+x\w+', 'var_0', r)

    def to_hx(c):
        h = int("%s" % c.groups(0), 16)
        if 19 < h < 160:
            return chr(h)
        else:
            return ""

    r = re.sub(r'(?:\\|)x(\w{2})', to_hx, r).replace('var ', '')

    f = eval(scrapertools.find_single_match(r, '\s*var_0\s*=\s*([^;]+);'))
    for i, v in enumerate(f):
        r = r.replace('[var_0[%s]]' % i, "." + f[i])
        if v == "": r = r.replace('var_0[%s]' % i, '""')

    return r
