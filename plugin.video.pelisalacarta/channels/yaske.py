# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para yaske
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re, sys, urllib, urlparse

from core import config
from core import logger
from core import httptools
from core import scrapertools
from core import servertools
from core import channeltools
from core import tmdb
from core.item import Item

HOST = 'http://www.yaske.ro'
parameters= channeltools.get_channel_parameters('yaske')
fanart_host= parameters['fanart']
thumbnail_host= parameters['thumbnail']
color1, color2, color3 = ['0xFFA5F6AF','0xFF5FDA6D','0xFF11811E']

def mainlist(item):
    logger.info()
    itemlist = []
    item.url = HOST
    item.text_color = color2
    item.fanart = fanart_host
    thumbnail = "https://raw.githubusercontent.com/master-1970/resources/master/images/genres/4/verdes/%s.png"

    itemlist.append(item.clone(title="Novedades", action="peliculas", text_blod= True, viewcontent='movies',
                                thumbnail= thumbnail % 'novedades', viewmode = "movie_with_plot"))
    itemlist.append(item.clone(title="Estrenos", action="peliculas", text_blod=True,
                                url= HOST + "/genero/premieres", thumbnail=thumbnail % 'estrenos'))
    itemlist.append(item.clone(title="", folder=False))

    itemlist.append(Item(channel=item.channel, title="Filtrar por:", fanart=fanart_host, folder=False,
                         text_color=color3, text_blod= True, thumbnail=thumbnail_host))
    itemlist.append(item.clone(title="    Género", action="menu_buscar_contenido", text_color=color1, text_italic=True,
                                extra="gender", thumbnail=thumbnail % 'generos', viewmode = "thumbnails" ))
    itemlist.append(item.clone(title="    Idioma", action="menu_buscar_contenido", text_color=color1, text_italic=True,
                                extra="language", thumbnail=thumbnail % 'idiomas'))
    itemlist.append(item.clone(title="    Calidad", action="menu_buscar_contenido", text_color=color1, text_italic=True,
                                extra="quality", thumbnail=thumbnail % 'calidad'))
    itemlist.append(item.clone(title="    Año", action="menu_buscar_contenido", text_color=color1, text_italic=True,
                                extra="year", thumbnail=thumbnail % 'year'))

    itemlist.append(item.clone(title="", folder=False))
    itemlist.append(item.clone(title="Buscar por título", action="search", thumbnail=thumbnail % 'buscar') )

    return itemlist


def search(item,texto):
    logger.info()
    itemlist = []

    try:
        item.url = HOST + "/search/%s" % texto.replace(' ', '+')
        item.extra = ""
        itemlist.extend(peliculas(item))
        if itemlist[-1].title == ">> Página siguiente":
            item_pag = itemlist[-1]
            itemlist = sorted(itemlist[:-1], key=lambda Item: Item.contentTitle)
            itemlist.append(item_pag)
        else:
            itemlist = sorted(itemlist, key=lambda Item: Item.contentTitle)


        return itemlist

    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []


def newest(categoria):
    logger.info()
    itemlist = []
    item = Item()
    try:
        if categoria == 'peliculas':
            item.url = HOST+"/"
        elif categoria == 'infantiles':
            item.url = HOST+"/custom/?gender=animation"
        else:
            return []

        itemlist = peliculas(item)
        if itemlist[-1].title == ">> Página siguiente":
            itemlist.pop()

    # Se captura la excepción, para no interrumpir al canal novedades si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error("{0}".format(line))
        return []

    return itemlist


def peliculas(item):
    logger.info()
    itemlist = []
    url_next_page = ""

    data = httptools.downloadpage(item.url).data
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    patron  = '<li class="item-movies.*?'
    patron += '<a class="image-block" href="([^"]+)" title="([^"]+)">'
    patron += '<img src="([^"]+).*?'
    patron += '<div class="moSinopsis">.*?</b>([^<]+).*?'
    patron += '<div class="moYear">.*?</b>([^<]+).*?'
    patron += '<ul class="bottombox">.*?<li>(<img.*?)</li>.*?</ul>'
    patron += '<div class="quality">([^<]+)</div>'
 
    matches = re.compile(patron,re.DOTALL).findall(data)

    # Paginacion
    if item.next_page != 'b':
        if len(matches) > 20:
            url_next_page = item.url
        matches = matches [:20]
        next_page = 'b'
    else:
        matches = matches[20:]
        next_page = 'a'
        patron_next_page = "<a href='([^']+)'>\&raquo\;</a>"
        matches_next_page = re.compile(patron_next_page, re.DOTALL).findall(data)
        if len(matches_next_page) > 0:
            url_next_page = urlparse.urljoin(item.url, matches_next_page[0])


    for scrapedurl, scrapedtitle, scrapedthumbnail, scrapedplot, year, idiomas, calidad in matches:
        patronidiomas = "<img src='[^']+' title='([^']+)'"
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(idiomas)

        idiomas_disponibles = ""
        if matchesidiomas:
            idiomas_disponibles = "[" + "/".join(matchesidiomas).strip() + "]"

        contentTitle = decodeHtmlentities(scrapedtitle.strip())
        title = "%s %s [%s]" %(contentTitle, idiomas_disponibles, calidad)
        plot = decodeHtmlentities(scrapedplot)

        itemlist.append(Item(channel=item.channel, action="findvideos", title=title, url=scrapedurl, contentQuality=calidad,
                                thumbnail=scrapedthumbnail, plot=plot, contentTitle=contentTitle,
                                infoLabels={"year":year}, text_color = color1))

    # Obtenemos los datos basicos de todas las peliculas mediante multihilos
    tmdb.set_infoLabels(itemlist)

    # Si es necesario añadir paginacion
    if url_next_page:
        itemlist.append(Item(channel=item.channel, action="peliculas", title=">> Página siguiente", thumbnail=thumbnail_host,
                              url=url_next_page, next_page=next_page, folder=True, text_color = color3, text_blod=True))

    return itemlist


def menu_buscar_contenido(item):
    logger.info()

    data = httptools.downloadpage(item.url).data
    data = scrapertools.get_match(data,'<select name="'+item.extra+'"(.*?)</select>')

    # Extrae las entradas
    patron  = "<option value='([^']+)'>([^<]+)</option>"
    matches = re.compile(patron,re.DOTALL).findall(data)

    itemlist = []
    adult_mode = config.get_setting("adult_mode")
    for scrapedurl,scrapedtitle in matches:
        thumbnail = ""
        
        if item.extra == 'gender':
            if scrapedtitle in ['Proximos', 'Series', 'Noticia'] or (scrapedtitle == 'Adultos' and adult_mode == "false"):
                continue

            url = HOST + "/genero/" + scrapedurl
            thumbnail = "https://raw.githubusercontent.com/master-1970/resources/master/images/genres/4/verdes/%s.png" \
                        % scrapedtitle.lower().replace(' ','%20')

        else:
            url = HOST+"/custom/?"+item.extra+"="+scrapedurl
            thumbnail = item.thumbnail

        itemlist.append( Item(channel=item.channel, action="peliculas", title=scrapedtitle, url=url, text_color = color1,
                              thumbnail=thumbnail, contentType='movie', folder=True, viewmode="movie_with_plot") )

    if item.extra in ['gender', 'language']:
        return sorted(itemlist, key=lambda i:  i.title.lower())
    else:
        return itemlist


def findvideos(item):
    logger.info()
    langdict = {}
    itemlist = []

    # Descarga la página
    data = httptools.downloadpage(item.url).data

    if not item.plot:
        item.plot = scrapertools.find_single_match(data,'<meta name="sinopsis" content="([^"]+)"')
        item.plot = decodeHtmlentities(item.plot)


    patron  = '<tr bgcolor=(.*?)</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for tr in matches:
        try:
            url = scrapertools.find_single_match(tr, '<a.*?href="([^"]+)"')
            if not url.startswith("http") or "olimpo.link" in url:
                continue

            title = scrapertools.find_single_match(tr,'<i class="icon-([^"]+)')
            server = scrapertools.find_single_match(tr,'"http\://www.google.com[^>]+>([^<]+)')
            idioma = scrapertools.find_single_match(tr,
                            '<img src="http://www.yaske.[a-z]+/theme/01/data/images/flags/([a-z_]+).png"[^>]+>[^<]*<')
            subtitulos = scrapertools.find_single_match(tr,
                            '<img src="http://www.yaske.[a-z]+/theme/01/data/images/flags/[^"]+"[^>]+>([^<]*)<')

            thumbnail = servertools.guess_server_thumbnail(server) # TODO: esto tarda un mundo, a ver si lo cambiamos
            if not thumbnail:
                thumbnail = thumbnail_host

            if title == 'play':
                title = "    Ver en %s" % server
            elif title == 'download':
                title = "    Descargar de %s" % server
            else:
                title = "    %s en %s" % (title, server)

            sublist = langdict.get(idioma, list())
            sublist.append(item.clone(action="play", title=title, url=url, server=server,
                                    thumbnail=thumbnail, folder=False, text_color=color1))
            langdict[idioma] = sublist

        except:
            import traceback
            logger.info("Excepcion: "+traceback.format_exc())

    # Añadir servidores encontrados, agrupandolos por idioma
    lang_trans = {"es_es": "Español:", "la_la": "Latino:", "en_es": "Subtitulado:", "en_en": "Ingles:"}
    for k in ["es_es", "la_la", "en_es", "en_en"]:
        if k in langdict:
            itemlist.append(Item(channel=item.channel, title=lang_trans[k], fanart=item.fanart, folder=False,
                                 text_color=color2, text_blod=True, thumbnail=thumbnail_host))
            itemlist.extend(langdict.pop(k))
    # Otros idiomas
    for k, v in  langdict.items():
        if subtitulos:
            title = "%s/s%:" % (k, subtitulos)
        else:
            title = "%s:" % k

        itemlist.append(Item(channel=item.channel, title=title, fanart=fanart_host, folder=False,
                             text_color=color2, text_blod=True, thumbnail=thumbnail_host))
        itemlist.extend(langdict.pop(k))

    # Insertar items "Buscar trailer" y "Añadir a la biblioteca"
    if itemlist and item.extra != "library":
        title = "%s [%s]" % (item.contentTitle, item.contentQuality)
        itemlist.insert(0, item.clone(channel = "trailertools", action="buscartrailer",
                                      text_color=color3, title=title, viewmode="list"))

        if config.get_library_support():
            itemlist.append(Item(channel=item.channel, title="Añadir película a la biblioteca",
                                 action="add_pelicula_to_library", url=item.url, text_color="green",
                                 contentTitle=item.contentTitle, extra="library", thumbnail=thumbnail_host))


    return itemlist


def play(item):
    logger.info("item.url="+item.url)
    itemlist=[]

    data = urllib.unquote(item.url)
    newdata = scrapertools.find_single_match(data,'olo.gg/s/[a-zA-Z0-9]+.s.(.*?)$')
    if newdata:
        data = urllib.unquote(newdata)

    logger.info("item.url=" + data)
    # Buscamos video por servidor ...
    devuelve = servertools.findvideosbyserver(data, item.server)
    if not devuelve:
        # ...sino lo encontramos buscamos en todos los servidores disponibles
        devuelve = servertools.findvideos(data)

    if devuelve:
        #logger.debug(devuelve)
        itemlist.append(Item(channel=item.channel, title=item.contentTitle, action="play", server=devuelve[0][2],
                             url=devuelve[0][1], thumbnail=item.thumbnail, folder=False))

    return itemlist


# TODO: Esto es temporal hasta q se modifique scrapertools
def decodeHtmlentities(data):
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8})(;?)")

    # maps the HTML5 named character references to the equivalent Unicode character(s)
    html5 = {'CupCap;': '\u224d', 'minusdu;': '\u2a2a', 'aring': '\xe5', 'Ubreve;': '\u016c', 'lcedil;': '\u013c',
             'Zacute;': '\u0179', 'NotVerticalBar;': '\u2224', 'bbrk;': '\u23b5', 'ThinSpace;': '\u2009',
             'nwarhk;': '\u2923', 'rlm;': '\u200f', 'DoubleDownArrow;': '\u21d3', 'RightDownVectorBar;': '\u2955',
             'jukcy;': '\u0454', 'frac12;': '\xbd', 'subrarr;': '\u2979', 'rsquo;': '\u2019', 'aacute;': '\xe1',
             'Integral;': '\u222b', 'oS;': '\u24c8', 'eqslantgtr;': '\u2a96', 'Uuml': '\xdc', 'piv;': '\u03d6',
             'iinfin;': '\u29dc', 'Ubrcy;': '\u040e', 'lhblk;': '\u2584', 'uml': '\xa8', 'backcong;': '\u224c',
             'capdot;': '\u2a40', 'harr;': '\u2194', 'lsquor;': '\u201a', 'iscr;': '\U0001d4be', 'Lsh;': '\u21b0',
             'Implies;': '\u21d2', 'Oacute': '\xd3', 'reg': '\xae', 'vsupnE;': '\u2acc\ufe00', 'Pcy;': '\u041f',
             'nang;': '\u2220\u20d2', 'Kcy;': '\u041a', 'GT': '>', 'eacute;': '\xe9', 'breve;': '\u02d8',
             'mfr;': '\U0001d52a', 'bnot;': '\u2310', 'racute;': '\u0155', 'dtrif;': '\u25be', 'cedil': '\xb8',
             'gesdotol;': '\u2a84', 'sc;': '\u227b', 'npreceq;': '\u2aaf\u0338', 'NotTildeTilde;': '\u2249',
             'nlE;': '\u2266\u0338', 'trianglerighteq;': '\u22b5', 'gfr;': '\U0001d524', 'odblac;': '\u0151',
             'wedge;': '\u2227', 'solb;': '\u29c4', 'isinE;': '\u22f9', 'middot;': '\xb7', 'nshortparallel;': '\u2226',
             'cudarrr;': '\u2935', 'loarr;': '\u21fd', 'UnderBar;': '_', 'mstpos;': '\u223e', 'Oacute;': '\xd3',
             'ltdot;': '\u22d6', 'gacute;': '\u01f5', 'Tcy;': '\u0422', 'Jcy;': '\u0419', 'wr;': '\u2240',
             'Amacr;': '\u0100', 'gtrdot;': '\u22d7', 'rarrap;': '\u2975', 'boxtimes;': '\u22a0', 'nearr;': '\u2197',
             'ecaron;': '\u011b', 'angmsdad;': '\u29ab', 'ropf;': '\U0001d563', 'uacute;': '\xfa', 'nsucc;': '\u2281',
             'nvap;': '\u224d\u20d2', 'udblac;': '\u0171', 'range;': '\u29a5', 'udhar;': '\u296e', 'nwarr;': '\u2196',
             'lneq;': '\u2a87', 'Uuml;': '\xdc', 'Tab;': '\t', 'Lmidot;': '\u013f', 'Tfr;': '\U0001d517',
             'TScy;': '\u0426', 'nvge;': '\u2265\u20d2', 'mp;': '\u2213', 'gl;': '\u2277', 'YAcy;': '\u042f',
             'CenterDot;': '\xb7', 'iopf;': '\U0001d55a', 'varsigma;': '\u03c2', 'lbrack;': '[', 'icy;': '\u0438',
             'boxDR;': '\u2554', 'nsubseteq;': '\u2288', 'Ocy;': '\u041e', 'integers;': '\u2124', 'THORN': '\xde',
             'cwint;': '\u2231', 'downharpoonright;': '\u21c2', 'capbrcup;': '\u2a49', 'nGtv;': '\u226b\u0338',
             'nge;': '\u2271', 'angmsdac;': '\u29aa', 'ropar;': '\u2986', 'boxdl;': '\u2510', 'bigcup;': '\u22c3',
             'lsim;': '\u2272', 'gtquest;': '\u2a7c', 'lrhar;': '\u21cb', 'Aring': '\xc5', 'Cap;': '\u22d2',
             'twoheadrightarrow;': '\u21a0', 'ngsim;': '\u2275', 'plus;': '+', 'LeftArrowBar;': '\u21e4',
             'lesseqqgtr;': '\u2a8b', 'softcy;': '\u044c', 'ne;': '\u2260', 'Agrave': '\xc0', 'SmallCircle;': '\u2218',
             'andd;': '\u2a5c', 'LeftArrow;': '\u2190', 'napE;': '\u2a70\u0338', 'iuml': '\xef', 'Lscr;': '\u2112',
             'gla;': '\u2aa5', 'yicy;': '\u0457', 'bsime;': '\u22cd', 'gtreqqless;': '\u2a8c', 'female;': '\u2640',
             'cupdot;': '\u228d', 'pound': '\xa3', 'yacy;': '\u044f', 'varkappa;': '\u03f0', 'lambda;': '\u03bb',
             'circledcirc;': '\u229a', 'circlearrowleft;': '\u21ba', 'Beta;': '\u0392', 'REG': '\xae',
             'drbkarow;': '\u2910', 'boxhu;': '\u2534', 'xvee;': '\u22c1', 'boxv;': '\u2502', 'igrave;': '\xec',
             'SquareSupersetEqual;': '\u2292', 'Afr;': '\U0001d504', 'lacute;': '\u013a', 'Yacute;': '\xdd',
             'xrArr;': '\u27f9', 'mnplus;': '\u2213', 'shchcy;': '\u0449', 'Hopf;': '\u210d', 'ucirc': '\xfb',
             'tau;': '\u03c4', 'TSHcy;': '\u040b', 'Icirc': '\xce', 'imath;': '\u0131', 'qprime;': '\u2057',
             'uhblk;': '\u2580', 'lbarr;': '\u290c', 'Hstrok;': '\u0126', 'NotLessGreater;': '\u2278',
             'vsubne;': '\u228a\ufe00', 'DoubleLeftRightArrow;': '\u21d4', 'larrtl;': '\u21a2',
             'LessEqualGreater;': '\u22da', 'boxVl;': '\u2562', 'csupe;': '\u2ad2', 'gesdoto;': '\u2a82',
             'lEg;': '\u2a8b', 'zhcy;': '\u0436', 'icirc': '\xee', 'rmoust;': '\u23b1', 'RoundImplies;': '\u2970',
             'subE;': '\u2ac5', 'zwj;': '\u200d', 'VerticalLine;': '|', 'ell;': '\u2113', 'larrbfs;': '\u291f',
             'OpenCurlyDoubleQuote;': '\u201c', 'Hfr;': '\u210c', 'ddotseq;': '\u2a77', 'orderof;': '\u2134',
             'Element;': '\u2208', 'circledast;': '\u229b', 'larrpl;': '\u2939', 'longmapsto;': '\u27fc',
             'lessapprox;': '\u2a85', 'nLtv;': '\u226a\u0338', 'ast;': '*', 'DiacriticalTilde;': '\u02dc',
             'lrm;': '\u200e', 'imagpart;': '\u2111', 'Ropf;': '\u211d', 'scE;': '\u2ab4', 'deg': '\xb0',
             'll;': '\u226a', 'mopf;': '\U0001d55e', 'ograve;': '\xf2', 'notnivc;': '\u22fd', 'prnap;': '\u2ab9',
             'CircleDot;': '\u2299', 'blank;': '\u2423', 'NotLeftTriangleEqual;': '\u22ec', 'num;': '#',
             'langle;': '\u27e8', 'scaron;': '\u0161', 'subne;': '\u228a', 'prE;': '\u2ab3', 'Tau;': '\u03a4',
             'trie;': '\u225c', 'times': '\xd7', 'eg;': '\u2a9a', 'rightharpoonup;': '\u21c0', 'nearhk;': '\u2924',
             'pointint;': '\u2a15', 'Pscr;': '\U0001d4ab', 'quot': '"', 'Iacute;': '\xcd', 'dcy;': '\u0434',
             'upsi;': '\u03c5', 'MediumSpace;': '\u205f', 'DownLeftVectorBar;': '\u2956', 'supdsub;': '\u2ad8',
             'Ccirc;': '\u0108', 'luruhar;': '\u2966', 'LT': '<', 'chcy;': '\u0447', 'lsimg;': '\u2a8f',
             'ljcy;': '\u0459', 'complexes;': '\u2102', 'dagger;': '\u2020', 'isinv;': '\u2208', 'PartialD;': '\u2202',
             'prod;': '\u220f', 'subplus;': '\u2abf', 'digamma;': '\u03dd', 'Ccedil': '\xc7', 'blacktriangle;': '\u25b4',
             'veeeq;': '\u225a', 'lesdotor;': '\u2a83', 'gcy;': '\u0433', 'ntgl;': '\u2279', 'Ouml': '\xd6',
             'eparsl;': '\u29e3', 'xsqcup;': '\u2a06', 'glE;': '\u2a92', 'bowtie;': '\u22c8',
             'SquareIntersection;': '\u2293', 'RightFloor;': '\u230b', 'Efr;': '\U0001d508',
             'DownLeftRightVector;': '\u2950', 'hercon;': '\u22b9', 'ecy;': '\u044d', 'DoubleDot;': '\xa8', 'rcub;': '}',
             'asympeq;': '\u224d', 'NotTildeFullEqual;': '\u2247', 'Gg;': '\u22d9', 'gtreqless;': '\u22db',
             'Sscr;': '\U0001d4ae', 'cularrp;': '\u293d', 'DoubleUpArrow;': '\u21d1', 'sect': '\xa7', 'map;': '\u21a6',
             'Del;': '\u2207', 'ctdot;': '\u22ef', 'Umacr;': '\u016a', 'copf;': '\U0001d554', 'minus;': '\u2212',
             'smte;': '\u2aac', 'zfr;': '\U0001d537', 'measuredangle;': '\u2221', 'male;': '\u2642',
             'angrtvbd;': '\u299d', 'NestedGreaterGreater;': '\u226b', 'uuml;': '\xfc', 'ograve': '\xf2',
             'Alpha;': '\u0391', 'QUOT;': '"', 'timesd;': '\u2a30', 'hyphen;': '\u2010', 'dopf;': '\U0001d555',
             'Backslash;': '\u2216', 'utrif;': '\u25b4', 'ntrianglerighteq;': '\u22ed', 'Hat;': '^', 'between;': '\u226c',
             'zacute;': '\u017a', 'geqslant;': '\u2a7e', 'elinters;': '\u23e7', 'lvertneqq;': '\u2268\ufe00',
             'Yscr;': '\U0001d4b4', 'NotPrecedesEqual;': '\u2aaf\u0338', 'otilde': '\xf5', 'rtriltri;': '\u29ce',
             'SucceedsSlantEqual;': '\u227d', 'bsim;': '\u223d', 'dscy;': '\u0455', 'cirmid;': '\u2aef',
             'gnapprox;': '\u2a8a', 'uharl;': '\u21bf', 'sqsube;': '\u2291', 'YIcy;': '\u0407', 'forall;': '\u2200',
             'ogt;': '\u29c1', 'Vopf;': '\U0001d54d', 'ffllig;': '\ufb04', 'loz;': '\u25ca', 'Atilde;': '\xc3',
             'ntlg;': '\u2278', 'vangrt;': '\u299c', 'it;': '\u2062', 'GreaterTilde;': '\u2273', 'rarrhk;': '\u21aa',
             'smid;': '\u2223', 'kappa;': '\u03ba', 'Diamond;': '\u22c4', 'ngeq;': '\u2271', 'DownArrowBar;': '\u2913',
             'expectation;': '\u2130', 'sup3': '\xb3', 'frasl;': '\u2044', 'Bscr;': '\u212c', 'geqq;': '\u2267',
             'lat;': '\u2aab', 'macr;': '\xaf', 'longrightarrow;': '\u27f6', 'Gcirc;': '\u011c', 'Wcirc;': '\u0174',
             'horbar;': '\u2015', 'dharr;': '\u21c2', 'DownRightTeeVector;': '\u295f', 'GreaterEqual;': '\u2265',
             'rBarr;': '\u290f', 'precsim;': '\u227e', 'iuml;': '\xef', 'ZHcy;': '\u0416', 'vnsub;': '\u2282\u20d2',
             'UnderParenthesis;': '\u23dd', 'RuleDelayed;': '\u29f4', 'bull;': '\u2022', 'swArr;': '\u21d9',
             'nrtri;': '\u22eb', 'apE;': '\u2a70', 'nLt;': '\u226a\u20d2', 'LeftDownVectorBar;': '\u2959',
             'succnapprox;': '\u2aba', 'szlig': '\xdf', 'vcy;': '\u0432', 'wcirc;': '\u0175', 'utri;': '\u25b5',
             'Zeta;': '\u0396', 'Hcirc;': '\u0124', 'NotRightTriangle;': '\u22eb', 'NotGreaterEqual;': '\u2271',
             'larrb;': '\u21e4', 'ecolon;': '\u2255', 'ascr;': '\U0001d4b6', 'RightUpVectorBar;': '\u2954',
             'divide': '\xf7', 'npolint;': '\u2a14', 'nexist;': '\u2204', 'plusb;': '\u229e', 'boxvl;': '\u2524',
             'searhk;': '\u2925', 'oror;': '\u2a56', 'tdot;': '\u20db', 'bigotimes;': '\u2a02', 'phone;': '\u260e',
             'Gscr;': '\U0001d4a2', 'bumpe;': '\u224f', 'ang;': '\u2220', 'ltquest;': '\u2a7b',
             'rightharpoondown;': '\u21c1', 'rdca;': '\u2937', 'cross;': '\u2717', 'Kopf;': '\U0001d542',
             'IEcy;': '\u0415', 'leq;': '\u2264', 'rarrw;': '\u219d', 'rcy;': '\u0440', 'Mu;': '\u039c',
             'nopf;': '\U0001d55f', 'Aopf;': '\U0001d538', 'CloseCurlyDoubleQuote;': '\u201d', 'lbrace;': '{',
             'triangleq;': '\u225c', 'curlyeqprec;': '\u22de', 'LeftDownTeeVector;': '\u2961', 'subset;': '\u2282',
             'xscr;': '\U0001d4cd', 'brvbar;': '\xa6', 'nles;': '\u2a7d\u0338', 'circeq;': '\u2257', 'boxVH;': '\u256c',
             'lE;': '\u2266', 'zeta;': '\u03b6', 'congdot;': '\u2a6d', 'emsp13;': '\u2004', 'uogon;': '\u0173',
             'xcap;': '\u22c2', 'eta;': '\u03b7', 'lAarr;': '\u21da', 'thicksim;': '\u223c', 'boxDl;': '\u2556',
             'rmoustache;': '\u23b1', 'Sopf;': '\U0001d54a', 'uarr;': '\u2191', 'Otimes;': '\u2a37', 'boxvH;': '\u256a',
             'lparlt;': '\u2993', 'nsime;': '\u2244', 'sqcaps;': '\u2293\ufe00', 'SquareUnion;': '\u2294',
             'Rsh;': '\u21b1', 'Zcy;': '\u0417', 'ycirc;': '\u0177', 'rbrkslu;': '\u2990', 'Proportional;': '\u221d',
             'Sup;': '\u22d1', 'curlyvee;': '\u22ce', 'rceil;': '\u2309', 'Xfr;': '\U0001d51b', 'minusd;': '\u2238',
             'angmsdab;': '\u29a9', 'DiacriticalDoubleAcute;': '\u02dd', 'par;': '\u2225', 'lpar;': '(', 'lcy;': '\u043b',
             'Nu;': '\u039d', 'euml;': '\xeb', 'CircleMinus;': '\u2296', 'lfloor;': '\u230a', 'Rightarrow;': '\u21d2',
             'rect;': '\u25ad', 'dzigrarr;': '\u27ff', 'tcy;': '\u0442', 'vartheta;': '\u03d1', 'Idot;': '\u0130',
             'Lleftarrow;': '\u21da', 'GT;': '>', 'emsp14;': '\u2005', 'vert;': '|', 'boxHu;': '\u2567',
             'Rarrtl;': '\u2916', 'nprcue;': '\u22e0', 'para': '\xb6', 'nsucceq;': '\u2ab0\u0338', 'nhArr;': '\u21ce',
             'ClockwiseContourIntegral;': '\u2232', 'Downarrow;': '\u21d3', 'Otilde': '\xd5', 'umacr;': '\u016b',
             'varsubsetneq;': '\u228a\ufe00', 'cup;': '\u222a', 'longleftrightarrow;': '\u27f7', 'gg;': '\u226b',
             'Barv;': '\u2ae7', 'Map;': '\u2905', 'Im;': '\u2111', 'ltcir;': '\u2a79', 'gdot;': '\u0121',
             'Cayleys;': '\u212d', 'timesbar;': '\u2a31', 'Gdot;': '\u0120', 'Ucirc': '\xdb', 'bigvee;': '\u22c1',
             'QUOT': '"', 'lang;': '\u27e8', 'Yfr;': '\U0001d51c', 'Larr;': '\u219e', 'leg;': '\u22da', 'cuesc;': '\u22df',
             'rArr;': '\u21d2', 'mumap;': '\u22b8', 'RightVector;': '\u21c0', 'nisd;': '\u22fa', 'crarr;': '\u21b5',
             'leftthreetimes;': '\u22cb', 'Fcy;': '\u0424', 'xotime;': '\u2a02', 'odash;': '\u229d', 'agrave;': '\xe0',
             'LeftFloor;': '\u230a', 'scpolint;': '\u2a13', 'Pfr;': '\U0001d513', 'nvHarr;': '\u2904', 'quot;': '"',
             'comp;': '\u2201', 'imagline;': '\u2110', 'telrec;': '\u2315', 'Sqrt;': '\u221a', 'supsub;': '\u2ad4',
             'rarr;': '\u2192', 'gvertneqq;': '\u2269\ufe00', 'nbumpe;': '\u224f\u0338', 'Uacute': '\xda',
             'gsim;': '\u2273', 'coprod;': '\u2210', 'ncongdot;': '\u2a6d\u0338', 'sscr;': '\U0001d4c8',
             'lstrok;': '\u0142', 'TripleDot;': '\u20db', 'topfork;': '\u2ada', 'yacute': '\xfd', 'nrightarrow;': '\u219b',
             'VerticalBar;': '\u2223', 'LeftDownVector;': '\u21c3', 'angzarr;': '\u237c', 'nsupset;': '\u2283\u20d2',
             'rdldhar;': '\u2969', 'deg;': '\xb0', 'DoubleRightArrow;': '\u21d2', 'macr': '\xaf', 'ldca;': '\u2936',
             'jcirc;': '\u0135', 'uml;': '\xa8', 'cupor;': '\u2a45', 'egrave': '\xe8', 'boxur;': '\u2514',
             'Esim;': '\u2a73', 'hybull;': '\u2043', 'DownBreve;': '\u0311', 'order;': '\u2134', 'Vscr;': '\U0001d4b1',
             'ApplyFunction;': '\u2061', 'Mellintrf;': '\u2133', 'ufisht;': '\u297e', 'Ycirc;': '\u0176',
             'nedot;': '\u2250\u0338', 'Ugrave;': '\xd9', 'npar;': '\u2226', 'RightArrowLeftArrow;': '\u21c4',
             'xnis;': '\u22fb', 'sharp;': '\u266f', 'twixt;': '\u226c', 'midcir;': '\u2af0', 'real;': '\u211c',
             'npr;': '\u2280', 'oopf;': '\U0001d560', 'Ouml;': '\xd6', 'urtri;': '\u25f9', 'SucceedsTilde;': '\u227f',
             'ngeqslant;': '\u2a7e\u0338', 'Eopf;': '\U0001d53c', 'LowerLeftArrow;': '\u2199', 'sqsubseteq;': '\u2291',
             'preccurlyeq;': '\u227c', 'RightTriangle;': '\u22b3', 'ReverseUpEquilibrium;': '\u296f',
             'simplus;': '\u2a24', 'Aogon;': '\u0104', 'NotGreater;': '\u226f', 'rpargt;': '\u2994', 'curarrm;': '\u293c',
             'THORN;': '\xde', 'smtes;': '\u2aac\ufe00', 'Ntilde': '\xd1', 'Zscr;': '\U0001d4b5', 'Nscr;': '\U0001d4a9',
             'sigma;': '\u03c3', 'Atilde': '\xc3', 'checkmark;': '\u2713', 'spades;': '\u2660', 'ycy;': '\u044b',
             'shortmid;': '\u2223', 'NotLeftTriangleBar;': '\u29cf\u0338', 'SuchThat;': '\u220b', 'amacr;': '\u0101',
             'bigcirc;': '\u25ef', 'Gt;': '\u226b', 'xopf;': '\U0001d569', 'puncsp;': '\u2008', 'Fscr;': '\u2131',
             'gel;': '\u22db', 'sect;': '\xa7', 'cudarrl;': '\u2938', 'Iuml': '\xcf', 'squarf;': '\u25aa',
             'seswar;': '\u2929', 'Eacute': '\xc9', 'scy;': '\u0441', 'subnE;': '\u2acb', 'Sacute;': '\u015a',
             'doublebarwedge;': '\u2306', 'rnmid;': '\u2aee', 'djcy;': '\u0452', 'Odblac;': '\u0150', 'duhar;': '\u296f',
             'nVDash;': '\u22af', 'NotPrecedes;': '\u2280', 'frac45;': '\u2158', 'ubrcy;': '\u045e', 'empty;': '\u2205',
             'nbsp;': '\xa0', 'comma;': ',', 'RightArrow;': '\u2192', 'notnivb;': '\u22fe', 'nrarrw;': '\u219d\u0338',
             'downdownarrows;': '\u21ca', 'ngE;': '\u2267\u0338', 'lcub;': '{', 'Kscr;': '\U0001d4a6', 'Utilde;': '\u0168',
             'pertenk;': '\u2031', 'sstarf;': '\u22c6', 'bdquo;': '\u201e', 'psi;': '\u03c8', 'NotLeftTriangle;': '\u22ea',
             'Jscr;': '\U0001d4a5', 'UpEquilibrium;': '\u296e', 'succneqq;': '\u2ab6', 'drcrop;': '\u230c',
             'csube;': '\u2ad1', 'plusdu;': '\u2a25', 'nvlArr;': '\u2902', 'RightTeeArrow;': '\u21a6', 'apos;': "'",
             'squf;': '\u25aa', 'blacktriangledown;': '\u25be', 'ShortDownArrow;': '\u2193', 'boxuL;': '\u255b',
             'Lambda;': '\u039b', 'Darr;': '\u21a1', 'sup3;': '\xb3', 'xcirc;': '\u25ef', 'nscr;': '\U0001d4c3',
             'UpArrowDownArrow;': '\u21c5', 'Auml': '\xc4', 'nrArr;': '\u21cf', 'nges;': '\u2a7e\u0338',
             'parallel;': '\u2225', 'LeftUpTeeVector;': '\u2960', 'uwangle;': '\u29a7', 'napprox;': '\u2249',
             'sol;': '/', 'nRightarrow;': '\u21cf', 'squ;': '\u25a1', 'natur;': '\u266e', 'Escr;': '\u2130',
             'nLl;': '\u22d8\u0338', 'DD;': '\u2145', 'Chi;': '\u03a7', 'lBarr;': '\u290e', 'emptyset;': '\u2205',
             'iexcl': '\xa1', 'rarrtl;': '\u21a3', 'gE;': '\u2267', 'LeftTeeVector;': '\u295a',
             'DoubleUpDownArrow;': '\u21d5', 'Icirc;': '\xce', 'Racute;': '\u0154', 'vee;': '\u2228', 'bot;': '\u22a5',
             'nleftrightarrow;': '\u21ae', 'atilde': '\xe3', 'frac35;': '\u2157', 'mDDot;': '\u223a', 'eqcolon;': '\u2255',
             'bsolb;': '\u29c5', 'lltri;': '\u25fa', 'bsemi;': '\u204f', 'because;': '\u2235', 'Oslash': '\xd8',
             'nu;': '\u03bd', 'rightarrow;': '\u2192', 'rangle;': '\u27e9', 'TRADE;': '\u2122', 'llhard;': '\u296b',
             'LeftAngleBracket;': '\u27e8', 'scnsim;': '\u22e9', 'ccirc;': '\u0109', 'Jsercy;': '\u0408',
             'nvsim;': '\u223c\u20d2', 'nleftarrow;': '\u219a', 'hopf;': '\U0001d559', 'Ccedil;': '\xc7',
             'rrarr;': '\u21c9', 'twoheadleftarrow;': '\u219e', 'erDot;': '\u2253', 'epsiv;': '\u03f5', 'xi;': '\u03be',
             'ring;': '\u02da', 'tscy;': '\u0446', 'mu;': '\u03bc', 'Uacute;': '\xda', 'Lang;': '\u27ea', 'ovbar;': '\u233d',
             'nleq;': '\u2270', 'gbreve;': '\u011f', 'cedil;': '\xb8', 'gneq;': '\u2a88', 'wopf;': '\U0001d568',
             'frac18;': '\u215b', 'Oscr;': '\U0001d4aa', 'Egrave': '\xc8', 'Igrave;': '\xcc', 'varnothing;': '\u2205',
             'divideontimes;': '\u22c7', 'dot;': '\u02d9', 'EqualTilde;': '\u2242', 'NotTilde;': '\u2241', 'els;': '\u2a95',
             'easter;': '\u2a6e', 'swarhk;': '\u2926', 'vnsup;': '\u2283\u20d2', 'ETH': '\xd0', 'blacksquare;': '\u25aa',
             'bcong;': '\u224c', 'ocy;': '\u043e', 'rbrksld;': '\u298e', 'lhard;': '\u21bd', 'gtrarr;': '\u2978',
             'nharr;': '\u21ae', 'rharu;': '\u21c0', 'Mfr;': '\U0001d510', 'npre;': '\u2aaf\u0338', 'oslash;': '\xf8',
             'GreaterSlantEqual;': '\u2a7e', 'Ifr;': '\u2111', 'Pi;': '\u03a0', 'lrarr;': '\u21c6', 'sce;': '\u2ab0',
             'NotSquareSubsetEqual;': '\u22e2', 'beta;': '\u03b2', 'tcedil;': '\u0163', 'Int;': '\u222c', 'Conint;': '\u222f',
             'kappav;': '\u03f0', 'varphi;': '\u03d5', 'subsim;': '\u2ac7', 'nGt;': '\u226b\u20d2', 'blk14;': '\u2591',
             'IJlig;': '\u0132', 'LeftUpVector;': '\u21bf', 'epsilon;': '\u03b5', 'ReverseElement;': '\u220b',
             'angmsdaa;': '\u29a8', 'starf;': '\u2605', 'sung;': '\u266a', 'udarr;': '\u21c5',
             'RightUpTeeVector;': '\u295c', 'gne;': '\u2a88', 'nlArr;': '\u21cd', 'Lcedil;': '\u013b', 'ccedil': '\xe7',
             'dtri;': '\u25bf', 'nap;': '\u2249', 'neArr;': '\u21d7', 'boxVR;': '\u2560', 'verbar;': '|', 'omicron;': '\u03bf',
             'precapprox;': '\u2ab7', 'Lcaron;': '\u013d', 'ugrave;': '\xf9', 'eDDot;': '\u2a77', 'NotTildeEqual;': '\u2244',
             'pitchfork;': '\u22d4', 'top;': '\u22a4', 'quaternions;': '\u210d', 'imped;': '\u01b5', 'SquareSubset;': '\u228f',
             'rarrbfs;': '\u2920', 'NotSquareSuperset;': '\u2290\u0338', 'boxvR;': '\u255e', 'ni;': '\u220b', 'gcirc;': '\u011d',
             'ffr;': '\U0001d523', 'numsp;': '\u2007', 'notinvb;': '\u22f7', 'MinusPlus;': '\u2213', 'preceq;': '\u2aaf',
             'boxH;': '\u2550', 'lsqb;': '[', 'lagran;': '\u2112', 'lnsim;': '\u22e6', 'triplus;': '\u2a39',
             'angmsdah;': '\u29af', 'iff;': '\u21d4', 'LT;': '<', 'amp;': '&', 'rightrightarrows;': '\u21c9',
             'operp;': '\u29b9', 'imacr;': '\u012b', 'frac38;': '\u215c', 'cent;': '\xa2', 'NotHumpEqual;': '\u224f\u0338',
             'zeetrf;': '\u2128', 'DownTee;': '\u22a4', 'Scedil;': '\u015e', 'ShortLeftArrow;': '\u2190',
             'Bernoullis;': '\u212c', 'prurel;': '\u22b0', 'gEl;': '\u2a8c', 'late;': '\u2aad', 'notniva;': '\u220c',
             'robrk;': '\u27e7', 'alefsym;': '\u2135', 'eng;': '\u014b', 'sext;': '\u2736', 'roang;': '\u27ed',
             'Tcedil;': '\u0162', 'NotLessLess;': '\u226a\u0338', 'efDot;': '\u2252', 'cscr;': '\U0001d4b8',
             'dashv;': '\u22a3', 'cularr;': '\u21b6', 'numero;': '\u2116', 'caron;': '\u02c7', 'suphsub;': '\u2ad7',
             'boxUr;': '\u2559', 'ncup;': '\u2a42', 'lozenge;': '\u25ca', 'lowast;': '\u2217', 'Ufr;': '\U0001d518',
             'Gcedil;': '\u0122', 'curren;': '\xa4', 'Ycy;': '\u042b', 'NegativeThickSpace;': '\u200b',
             'ulcorner;': '\u231c', 'sdotb;': '\u22a1', 'rdquor;': '\u201d', 'nvltrie;': '\u22b4\u20d2',
             'LeftUpDownVector;': '\u2951', 'cap;': '\u2229', 'PrecedesEqual;': '\u2aaf', 'Ecirc;': '\xca',
             'bscr;': '\U0001d4b7', 'UpArrow;': '\u2191', 'simg;': '\u2a9e', 'notin;': '\u2209',
             'RightDownTeeVector;': '\u295d', 'disin;': '\u22f2', 'oacute;': '\xf3', 'nsube;': '\u2288',
             'iquest': '\xbf', 'ltrif;': '\u25c2', 'ccups;': '\u2a4c', 'Because;': '\u2235', 'otimes;': '\u2297',
             'Zopf;': '\u2124', 'supedot;': '\u2ac4', 'ee;': '\u2147', 'NotSucceedsSlantEqual;': '\u22e1', 'scap;': '\u2ab8',
             'TildeEqual;': '\u2243', 'Colon;': '\u2237', 'rcaron;': '\u0159', 'GJcy;': '\u0403', 'curvearrowright;': '\u21b7',
             'Barwed;': '\u2306', 'scirc;': '\u015d', 'Lopf;': '\U0001d543', 'hoarr;': '\u21ff', 'NotLess;': '\u226e',
             'afr;': '\U0001d51e', 'homtht;': '\u223b', 'subsup;': '\u2ad3', 'NotRightTriangleEqual;': '\u22ed',
             'raemptyv;': '\u29b3', 'ltrPar;': '\u2996', 'upsih;': '\u03d2', 'ccupssm;': '\u2a50', 'Longrightarrow;': '\u27f9',
             'NotGreaterFullEqual;': '\u2267\u0338', 'bnequiv;': '\u2261\u20e5', 'lrtri;': '\u22bf', 'setminus;': '\u2216',
             'supplus;': '\u2ac0', 'Rscr;': '\u211b', 'Popf;': '\u2119', 'NotSuperset;': '\u2283\u20d2',
             'looparrowright;': '\u21ac', 'odot;': '\u2299', 'laquo': '\xab', 'sqcup;': '\u2294', 'hairsp;': '\u200a',
             'Gamma;': '\u0393', 'lbrksld;': '\u298f', 'uplus;': '\u228e', 'equivDD;': '\u2a78', 'el;': '\u2a99',
             'CHcy;': '\u0427', 'rarrsim;': '\u2974', 'ffilig;': '\ufb03', 'thorn;': '\xfe', 'ngtr;': '\u226f',
             'qopf;': '\U0001d562', 'nvle;': '\u2264\u20d2', 'omid;': '\u29b6', 'vrtri;': '\u22b3', 'curvearrowleft;': '\u21b6',
             'DownRightVector;': '\u21c1', 'frac58;': '\u215d', 'Uopf;': '\U0001d54c', 'AMP;': '&', 'equest;': '\u225f',
             'succapprox;': '\u2ab8', 'intercal;': '\u22ba', 'rthree;': '\u22cc', 'gimel;': '\u2137', 'Uparrow;': '\u21d1',
             'Ll;': '\u22d8', 'dzcy;': '\u045f', 'dfisht;': '\u297f', 'frac12': '\xbd', 'submult;': '\u2ac1', 'rang;': '\u27e9',
             'Wscr;': '\U0001d4b2', 'Kcedil;': '\u0136', 'leqslant;': '\u2a7d', 'urcrop;': '\u230e', 'SOFTcy;': '\u042c',
             'hamilt;': '\u210b', 'AMP': '&', 'pscr;': '\U0001d4c5', 'egs;': '\u2a96', 'supE;': '\u2ac6', 'searr;': '\u2198',
             'varpi;': '\u03d6', 'nlarr;': '\u219a', 'nearrow;': '\u2197', 'ldsh;': '\u21b2', 'gesl;': '\u22db\ufe00',
             'rarrfs;': '\u291e', 'LessTilde;': '\u2272', 'boxUL;': '\u255d', 'And;': '\u2a53', 'LeftDoubleBracket;': '\u27e6',
             'rAtail;': '\u291c', 'eogon;': '\u0119', 'bepsi;': '\u03f6', 'vDash;': '\u22a8', 'Coproduct;': '\u2210',
             'ngeqq;': '\u2267\u0338', 'supne;': '\u228b', 'REG;': '\xae', 'kopf;': '\U0001d55c', 'cire;': '\u2257',
             'boxhD;': '\u2565', 'cir;': '\u25cb', 'awconint;': '\u2233', 'LowerRightArrow;': '\u2198', 'Wfr;': '\U0001d51a',
             'ssmile;': '\u2323', 'ic;': '\u2063', 'boxHd;': '\u2564', 'Oopf;': '\U0001d546', 'trisb;': '\u29cd',
             'longleftarrow;': '\u27f5', 'vprop;': '\u221d', 'qfr;': '\U0001d52e', 'frac34;': '\xbe',
             'vsubnE;': '\u2acb\ufe00', 'odiv;': '\u2a38', 'nvinfin;': '\u29de', 'boxminus;': '\u229f', 'efr;': '\U0001d522',
             'ForAll;': '\u2200', 'lsaquo;': '\u2039', 'yen': '\xa5', 'lAtail;': '\u291b', 'tint;': '\u222d', 'ltri;': '\u25c3',
             'DownTeeArrow;': '\u21a7', 'Tilde;': '\u223c', 'nsce;': '\u2ab0\u0338', 'larr;': '\u2190', 'supsup;': '\u2ad6',
             'frac16;': '\u2159', 'eth;': '\xf0', 'acirc;': '\xe2', 'ddarr;': '\u21ca', 'Iscr;': '\u2110',
             'triangleright;': '\u25b9', 'capand;': '\u2a44', 'HARDcy;': '\u042a', 'sup;': '\u2283',
             'NotSubset;': '\u2282\u20d2', 'searrow;': '\u2198', 'nsc;': '\u2281', 'sup1': '\xb9', 'sup2': '\xb2',
             'Breve;': '\u02d8', 'epar;': '\u22d5', 'clubsuit;': '\u2663', 'approx;': '\u2248', 'NotGreaterLess;': '\u2279',
             'mapsto;': '\u21a6', 'scsim;': '\u227f', 'notinE;': '\u22f9\u0338', 'hcirc;': '\u0125',
             'rightthreetimes;': '\u22cc', 'geq;': '\u2265', 'Kappa;': '\u039a', 'vdash;': '\u22a2', 'Congruent;': '\u2261',
             'boxdr;': '\u250c', 'DoubleContourIntegral;': '\u222f', 'upuparrows;': '\u21c8', 'csub;': '\u2acf',
             'PrecedesSlantEqual;': '\u227c', 'boxbox;': '\u29c9', 'zdot;': '\u017c', 'sub;': '\u2282', 'andand;': '\u2a55',
             'laemptyv;': '\u29b4', 'dstrok;': '\u0111', 'perp;': '\u22a5', 'HumpDownHump;': '\u224e', 'int;': '\u222b',
             'RightUpDownVector;': '\u294f', 'LongRightArrow;': '\u27f6', 'hstrok;': '\u0127', 'ngt;': '\u226f',
             'lbrke;': '\u298b', 'Ograve': '\xd2', 'nvrtrie;': '\u22b5\u20d2', 'leqq;': '\u2266', 'intprod;': '\u2a3c',
             'centerdot;': '\xb7', 'emptyv;': '\u2205', 'infintie;': '\u29dd', 'lbbrk;': '\u2772', 'Cacute;': '\u0106',
             'rscr;': '\U0001d4c7', 'otilde;': '\xf5', 'DiacriticalGrave;': '`', 'supe;': '\u2287', 'rotimes;': '\u2a35',
             'die;': '\xa8', 'mapstodown;': '\u21a7', 'fjlig;': 'fj', 'SquareSuperset;': '\u2290', 'curren': '\xa4',
             'GreaterLess;': '\u2277', 'smile;': '\u2323', 'NotHumpDownHump;': '\u224e\u0338', 'ucirc;': '\xfb',
             'vArr;': '\u21d5', 'boxV;': '\u2551', 'Tcaron;': '\u0164', 'not;': '\xac', 'mho;': '\u2127', 'sfrown;': '\u2322',
             'ZeroWidthSpace;': '\u200b', 'Acirc': '\xc2', 'gneqq;': '\u2269', 'Euml': '\xcb', 'Ccaron;': '\u010c',
             'Iacute': '\xcd', 'Yopf;': '\U0001d550', 'aogon;': '\u0105', 'rationals;': '\u211a', 'Bopf;': '\U0001d539',
             'uopf;': '\U0001d566', 'acE;': '\u223e\u0333', 'ETH;': '\xd0', 'intcal;': '\u22ba', 'clubs;': '\u2663',
             'plussim;': '\u2a26', 'olt;': '\u29c0', 'tprime;': '\u2034', 'iogon;': '\u012f', 'diamondsuit;': '\u2666',
             'ltlarr;': '\u2976', 'frac14': '\xbc', 'fscr;': '\U0001d4bb', 'aacute': '\xe1', 'dollar;': '$', 'xmap;': '\u27fc',
             'vscr;': '\U0001d4cb', 'ShortRightArrow;': '\u2192', 'Square;': '\u25a1', 'blk12;': '\u2592', 'triangle;': '\u25b5',
             'eacute': '\xe9', 'angrt;': '\u221f', 'circlearrowright;': '\u21bb', 'UpTee;': '\u22a5', 'copy;': '\xa9',
             'scnE;': '\u2ab6', 'aelig;': '\xe6', 'doteq;': '\u2250', 'parsl;': '\u2afd', 'Ugrave': '\xd9',
             'lfr;': '\U0001d529', 'gvnE;': '\u2269\ufe00', 'rarrc;': '\u2933', 'Acy;': '\u0410', 'rbrace;': '}',
             'ccedil;': '\xe7', 'nwarrow;': '\u2196', 'njcy;': '\u045a', 'UpperRightArrow;': '\u2197', 'dHar;': '\u2965',
             'gt': '>', 'jscr;': '\U0001d4bf', 'rarrpl;': '\u2945', 'varrho;': '\u03f1', 'Ocirc;': '\xd4', 'lowbar;': '_',
             'Yacute': '\xdd', 'nsub;': '\u2284', 'lessdot;': '\u22d6', 'NotGreaterGreater;': '\u226b\u0338',
             'darr;': '\u2193', 'mcomma;': '\u2a29', 'Cedilla;': '\xb8', 'vartriangleright;': '\u22b3', 'vfr;': '\U0001d533',
             'rfisht;': '\u297d', 'PlusMinus;': '\xb1', 'planck;': '\u210f', 'NotPrecedesSlantEqual;': '\u22e0',
             'Egrave;': '\xc8', 'rightarrowtail;': '\u21a3', 'Prime;': '\u2033', 'gtrless;': '\u2277', 'thetasym;': '\u03d1',
             'bbrktbrk;': '\u23b6', 'nle;': '\u2270', 'mlcp;': '\u2adb', 'larrsim;': '\u2973', 'jcy;': '\u0439',
             'drcorn;': '\u231f', 'harrw;': '\u21ad', 'updownarrow;': '\u2195', 'ubreve;': '\u016d', 'pluse;': '\u2a72',
             'UpTeeArrow;': '\u21a5', 'prime;': '\u2032', 'COPY;': '\xa9', 'CirclePlus;': '\u2295', 'Longleftarrow;': '\u27f8',
             'dArr;': '\u21d3', 'xcup;': '\u22c3', 'AElig': '\xc6', 'leftharpoonup;': '\u21bc', 'Uarr;': '\u219f',
             'lsquo;': '\u2018', 'nVdash;': '\u22ae', 'nwnear;': '\u2927', 'gescc;': '\u2aa9', 'rdsh;': '\u21b3',
             'grave;': '`', 'blk34;': '\u2593', 'LeftVector;': '\u21bc', 'uharr;': '\u21be', 'isins;': '\u22f4',
             'lescc;': '\u2aa8', 'eplus;': '\u2a71', 'jmath;': '\u0237', 'kscr;': '\U0001d4c0', 'nsim;': '\u2241',
             'Aacute;': '\xc1', 'NotLessEqual;': '\u2270', 'tshcy;': '\u045b', 'plusmn': '\xb1', 'ecir;': '\u2256',
             'nsmid;': '\u2224', 'lesdoto;': '\u2a81', 'nvdash;': '\u22ac', 'Lt;': '\u226a', 'DownRightVectorBar;': '\u2957',
             'asymp;': '\u2248', 'ggg;': '\u22d9', 'szlig;': '\xdf', 'lneqq;': '\u2268', 'loplus;': '\u2a2d',
             'ExponentialE;': '\u2147', 'profline;': '\u2312', 'DDotrahd;': '\u2911', 'rarrlp;': '\u21ac', 'Scy;': '\u0421',
             'le;': '\u2264', 'auml;': '\xe4', 'roarr;': '\u21fe', 'fltns;': '\u25b1', 'vellip;': '\u22ee', 'apacir;': '\u2a6f',
             'circledS;': '\u24c8', 'rfloor;': '\u230b', 'Cross;': '\u2a2f', 'DoubleLeftTee;': '\u2ae4', 'subsetneqq;': '\u2acb',
             'ordf': '\xaa', 'rightleftharpoons;': '\u21cc', 'fllig;': '\ufb02', 'ntilde': '\xf1', 'emsp;': '\u2003',
             'iacute;': '\xed', 'xfr;': '\U0001d535', 'fflig;': '\ufb00', 'xlarr;': '\u27f5', 'leftarrow;': '\u2190',
             'urcorner;': '\u231d', 'dharl;': '\u21c3', 'reals;': '\u211d', 'Re;': '\u211c', 'bemptyv;': '\u29b0',
             'angrtvb;': '\u22be', 'mdash;': '\u2014', 'dotsquare;': '\u22a1', 'omacr;': '\u014d', 'Vvdash;': '\u22aa',
             'pm;': '\xb1', 'OverBar;': '\u203e', 'nldr;': '\u2025', 'target;': '\u2316', 'hksearow;': '\u2925',
             'ecirc': '\xea', 'swnwar;': '\u292a', 'nfr;': '\U0001d52b', 'Copf;': '\u2102', 'Rarr;': '\u21a0',
             'raquo;': '\xbb', 'oline;': '\u203e', 'utilde;': '\u0169', 'hookrightarrow;': '\u21aa', 'Or;': '\u2a54',
             'origof;': '\u22b6', 'Theta;': '\u0398', 'kfr;': '\U0001d528', 'Sfr;': '\U0001d516', 'aopf;': '\U0001d552',
             'lArr;': '\u21d0', 'equiv;': '\u2261', 'ord;': '\u2a5d', 'Sigma;': '\u03a3', 'DScy;': '\u0405',
             'PrecedesTilde;': '\u227e', 'gnsim;': '\u22e7', 'colone;': '\u2254', 'boxhU;': '\u2568', 'Ntilde;': '\xd1',
             'NotNestedGreaterGreater;': '\u2aa2\u0338', 'NotSucceeds;': '\u2281', 'larrfs;': '\u291d', 'models;': '\u22a7',
             'DifferentialD;': '\u2146', 'toea;': '\u2928', 'Zdot;': '\u017b', 'zscr;': '\U0001d4cf', 'gtlPar;': '\u2995',
             'ii;': '\u2148', 'Zcaron;': '\u017d', 'Leftarrow;': '\u21d0', 'ohbar;': '\u29b5', 'orv;': '\u2a5b',
             'OverParenthesis;': '\u23dc', 'Upsilon;': '\u03a5', 'plusdo;': '\u2214', 'nis;': '\u22fc',
             'Poincareplane;': '\u210c', 'tfr;': '\U0001d531', 'DownArrow;': '\u2193', 'Sub;': '\u22d0', 'Ncedil;': '\u0145',
             'Iota;': '\u0399', 'InvisibleComma;': '\u2063', 'Ucy;': '\u0423', 'lnap;': '\u2a89', 'angst;': '\xc5',
             'sube;': '\u2286', 'Gopf;': '\U0001d53e', 'Succeeds;': '\u227b', 'ap;': '\u2248', 'andv;': '\u2a5a',
             'eDot;': '\u2251', 'angsph;': '\u2222', 'Dscr;': '\U0001d49f', 'boxHD;': '\u2566', 'gamma;': '\u03b3',
             'RightTeeVector;': '\u295b', 'straightphi;': '\u03d5', 'ohm;': '\u03a9', 'frac15;': '\u2155',
             'itilde;': '\u0129', 'jfr;': '\U0001d527', 'NJcy;': '\u040a', 'notinva;': '\u2209', 'frac25;': '\u2156',
             'Epsilon;': '\u0395', 'xoplus;': '\u2a01', 'zcy;': '\u0437', 'Union;': '\u22c3', 'lesssim;': '\u2272',
             'trpezium;': '\u23e2', 'bcy;': '\u0431', 'succsim;': '\u227f', 'boxDr;': '\u2553', 'beth;': '\u2136',
             'prap;': '\u2ab7', 'bumpeq;': '\u224f', 'NotSquareSubset;': '\u228f\u0338', 'nhpar;': '\u2af2',
             'vBar;': '\u2ae8', 'rbrke;': '\u298c', 'Dot;': '\xa8', 'ENG;': '\u014a', 'and;': '\u2227',
             'nsupseteqq;': '\u2ac6\u0338', 'blacklozenge;': '\u29eb', 'boxdL;': '\u2555', 'odsold;': '\u29bc',
             'bigsqcup;': '\u2a06', 'trade;': '\u2122', 'half;': '\xbd', 'elsdot;': '\u2a97', 'iota;': '\u03b9',
             'diam;': '\u22c4', 'block;': '\u2588', 'parsim;': '\u2af3', 'KHcy;': '\u0425', 'Lstrok;': '\u0141',
             'lesseqgtr;': '\u22da', 'div;': '\xf7', 'planckh;': '\u210e', 'rfr;': '\U0001d52f', 'loang;': '\u27ec',
             'lnapprox;': '\u2a89', 'triangleleft;': '\u25c3', 'nvDash;': '\u22ad', 'oint;': '\u222e', 'ecirc;': '\xea',
             'Lfr;': '\U0001d50f', 'eqsim;': '\u2242', 'emacr;': '\u0113', 'DownLeftVector;': '\u21bd', 'succeq;': '\u2ab0',
             'yucy;': '\u044e', 'biguplus;': '\u2a04', 'plusmn;': '\xb1', 'smashp;': '\u2a33', 'cuvee;': '\u22ce',
             'prec;': '\u227a', 'chi;': '\u03c7', 'angmsdag;': '\u29ae', 'backprime;': '\u2035', 'nbump;': '\u224e\u0338',
             'Mcy;': '\u041c', 'subseteq;': '\u2286', 'gtrapprox;': '\u2a86', 'lmoustache;': '\u23b0', 'circledR;': '\xae',
             'gsiml;': '\u2a90', 'subseteqq;': '\u2ac5', 'rbbrk;': '\u2773', 'inodot;': '\u0131', 'fpartint;': '\u2a0d',
             'barvee;': '\u22bd', 'egsdot;': '\u2a98', 'fcy;': '\u0444', 'qint;': '\u2a0c', 'Gammad;': '\u03dc',
             'upharpoonright;': '\u21be', 'NotEqual;': '\u2260', 'boxVL;': '\u2563', 'dotminus;': '\u2238', 'esim;': '\u2242',
             'lotimes;': '\u2a34', 'Xopf;': '\U0001d54f', 'divide;': '\xf7', 'RightTriangleEqual;': '\u22b5', 'af;': '\u2061',
             'tridot;': '\u25ec', 'lvnE;': '\u2268\ufe00', 'multimap;': '\u22b8', 'rsh;': '\u21b1', 'Ascr;': '\U0001d49c',
             'hkswarow;': '\u2926', 'suplarr;': '\u297b', 'VDash;': '\u22ab', 'uscr;': '\U0001d4ca', 'sccue;': '\u227d',
             'SHcy;': '\u0428', 'ndash;': '\u2013', 'YUcy;': '\u042e', 'rppolint;': '\u2a12', 'Equilibrium;': '\u21cc',
             'boxvL;': '\u2561', 'nlt;': '\u226e', 'Euml;': '\xcb', 'IOcy;': '\u0401', 'times;': '\xd7', 'mapstoup;': '\u21a5',
             'epsi;': '\u03b5', 'xlArr;': '\u27f8', 'cacute;': '\u0107', 'capcap;': '\u2a4b', 'ntriangleleft;': '\u22ea',
             'sqsupseteq;': '\u2292', 'NotCupCap;': '\u226d', 'RightUpVector;': '\u21be', 'rpar;': ')', 'Xi;': '\u039e',
             'tilde;': '\u02dc', 'auml': '\xe4', 'esdot;': '\u2250', 'nleqslant;': '\u2a7d\u0338', 'rhard;': '\u21c1',
             'Delta;': '\u0394', 'gsime;': '\u2a8e', 'lt': '<', 'SHCHcy;': '\u0429', 'varsupsetneq;': '\u228b\ufe00',
             'LeftUpVectorBar;': '\u2958', 'simne;': '\u2246', 'lozf;': '\u29eb', 'LeftTeeArrow;': '\u21a4',
             'spadesuit;': '\u2660', 'Pr;': '\u2abb', 'Eacute;': '\xc9', 'boxVh;': '\u256b', 'Dashv;': '\u2ae4',
             'ccaron;': '\u010d', 'setmn;': '\u2216', 'Aring;': '\xc5', 'plustwo;': '\u2a27', 'Rcaron;': '\u0158',
             'sdote;': '\u2a66', 'ifr;': '\U0001d526', 'roplus;': '\u2a2e', 'qscr;': '\U0001d4c6', 'bernou;': '\u212c',
             'Dstrok;': '\u0110', 'not': '\xac', 'backepsilon;': '\u03f6', 'Otilde;': '\xd5', 'langd;': '\u2991',
             'lopf;': '\U0001d55d', 'KJcy;': '\u040c', 'infin;': '\u221e', 'uacute': '\xfa', 'Fopf;': '\U0001d53d',
             'backsim;': '\u223d', 'ape;': '\u224a', 'LeftArrowRightArrow;': '\u21c6', 'Wedge;': '\u22c0',
             'DownLeftTeeVector;': '\u295e', 'Ffr;': '\U0001d509', 'rtrif;': '\u25b8', 'gjcy;': '\u0453', 'supmult;': '\u2ac2',
             'gt;': '>', 'swarr;': '\u2199', 'amalg;': '\u2a3f', 'rho;': '\u03c1', 'triminus;': '\u2a3a', 'or;': '\u2228',
             'nesim;': '\u2242\u0338', 'sime;': '\u2243', 'larrlp;': '\u21ab', 'Sum;': '\u2211', 'khcy;': '\u0445',
             'wscr;': '\U0001d4cc', 'caret;': '\u2041', 'agrave': '\xe0', 'Ocirc': '\xd4', 'Iopf;': '\U0001d540',
             'bump;': '\u224e', 'ratail;': '\u291a', 'simgE;': '\u2aa0', 'precneqq;': '\u2ab5', 'varpropto;': '\u221d',
             'yuml;': '\xff', 'ntrianglelefteq;': '\u22ec', 'ouml': '\xf6', 'lt;': '<', 'alpha;': '\u03b1',
             'gopf;': '\U0001d558', 'smt;': '\u2aaa', 'doteqdot;': '\u2251', 'LessSlantEqual;': '\u2a7d', 'mid;': '\u2223',
             'simeq;': '\u2243', 'tstrok;': '\u0167', 'GreaterEqualLess;': '\u22db', 'escr;': '\u212f', 'Nfr;': '\U0001d511',
             'nGg;': '\u22d9\u0338', 'simlE;': '\u2a9f', 'apid;': '\u224b', 'nvrArr;': '\u2903', 'dotplus;': '\u2214',
             'cirscir;': '\u29c2', 'LeftTee;': '\u22a3', 'lnE;': '\u2268', 'topcir;': '\u2af1', 'egrave;': '\xe8',
             'demptyv;': '\u29b1', 'copysr;': '\u2117', 'Vdashl;': '\u2ae6', 'yen;': '\xa5', 'gap;': '\u2a86',
             'thetav;': '\u03d1', 'bumpE;': '\u2aae', 'Ncaron;': '\u0147', 'blacktriangleright;': '\u25b8',
             'olcir;': '\u29be', 'UnderBracket;': '\u23b5', 'nsimeq;': '\u2244', 'downarrow;': '\u2193', 'Assign;': '\u2254',
             'opar;': '\u29b7', 'diams;': '\u2666', 'jsercy;': '\u0458', 'SubsetEqual;': '\u2286', 'bkarow;': '\u290d',
             'square;': '\u25a1', 'ntriangleright;': '\u22eb', 'nrarr;': '\u219b', 'Udblac;': '\u0170', 'sqsubset;': '\u228f',
             'sup1;': '\xb9', 'ldrdhar;': '\u2967', 'erarr;': '\u2971', 'frown;': '\u2322', 'cemptyv;': '\u29b2',
             'rtri;': '\u25b9', 'Hscr;': '\u210b', 'Cconint;': '\u2230', 'Edot;': '\u0116', 'hardcy;': '\u044a',
             'there4;': '\u2234', 'frac56;': '\u215a', 'Gbreve;': '\u011e', 'ldquo;': '\u201c', 'wedgeq;': '\u2259',
             'ncong;': '\u2247', 'prop;': '\u221d', 'isinsv;': '\u22f3', 'hbar;': '\u210f', 'supseteq;': '\u2287',
             'Abreve;': '\u0102', 'swarrow;': '\u2199', 'lfisht;': '\u297c', 'siml;': '\u2a9d', 'equals;': '=',
             'lesges;': '\u2a93', 'phiv;': '\u03d5', 'Proportion;': '\u2237', 'Dcy;': '\u0414', 'edot;': '\u0117',
             'CounterClockwiseContourIntegral;': '\u2233', 'shortparallel;': '\u2225', 'frac34': '\xbe', 'solbar;': '\u233f',
             'sbquo;': '\u201a', 'LessLess;': '\u2aa1', 'harrcir;': '\u2948', 'Jfr;': '\U0001d50d', 'Xscr;': '\U0001d4b3',
             'NotNestedLessLess;': '\u2aa1\u0338', 'zcaron;': '\u017e', 'abreve;': '\u0103', 'nacute;': '\u0144',
             'ultri;': '\u25f8', 'Bcy;': '\u0411', 'ThickSpace;': '\u205f\u200a', 'questeq;': '\u225f',
             'DoubleLongLeftArrow;': '\u27f8', 'ccaps;': '\u2a4d', 'rHar;': '\u2964', 'upharpoonleft;': '\u21bf',
             'iacute': '\xed', 'cong;': '\u2245', 'yopf;': '\U0001d56a', 'nvlt;': '<\u20d2', 'bopf;': '\U0001d553',
             'Supset;': '\u22d1', 'Subset;': '\u22d0', 'varsubsetneqq;': '\u2acb\ufe00', 'Omega;': '\u03a9',
             'lsh;': '\u21b0', 'iiiint;': '\u2a0c', 'copy': '\xa9', 'gscr;': '\u210a', 'Star;': '\u22c6', 'boxHU;': '\u2569',
             'circ;': '\u02c6', 'lap;': '\u2a85', 'rlhar;': '\u21cc', 'percnt;': '%', 'NotLessSlantEqual;': '\u2a7d\u0338',
             'maltese;': '\u2720', 'looparrowleft;': '\u21ab', 'LeftVectorBar;': '\u2952', 'nLeftrightarrow;': '\u21ce',
             'bsolhsub;': '\u27c8', 'nsubseteqq;': '\u2ac5\u0338', 'Rfr;': '\u211c', 'lgE;': '\u2a91',
             'RightTriangleBar;': '\u29d0', 'Superset;': '\u2283', 'reg;': '\xae', 'frac14;': '\xbc', 'RBarr;': '\u2910',
             'realpart;': '\u211c', 'zwnj;': '\u200c', 'nrarrc;': '\u2933\u0338', 'pluscir;': '\u2a22', 'lharul;': '\u296a',
             'thickapprox;': '\u2248', 'lscr;': '\U0001d4c1', 'caps;': '\u2229\ufe00', 'supsim;': '\u2ac8',
             'cirfnint;': '\u2a10', 'boxvh;': '\u253c', 'therefore;': '\u2234', 'Verbar;': '\u2016', 'nsqsube;': '\u22e2',
             'latail;': '\u2919', 'propto;': '\u221d', 'boxuR;': '\u2558', 'Omacr;': '\u014c', 'ges;': '\u2a7e',
             'Scaron;': '\u0160', 'oslash': '\xf8', 'oast;': '\u229b', 'phi;': '\u03c6', 'cuwed;': '\u22cf',
             'oplus;': '\u2295', 'ncedil;': '\u0146', 'scnap;': '\u2aba', 'Iogon;': '\u012e', 'bne;': '=\u20e5',
             'Oslash;': '\xd8', 'xuplus;': '\u2a04', 'precnsim;': '\u22e8', 'bigtriangledown;': '\u25bd', 'iprod;': '\u2a3c',
             'ange;': '\u29a4', 'RightTee;': '\u22a2', 'tosa;': '\u2929', 'Iukcy;': '\u0406', 'leftrightarrows;': '\u21c6',
             'DoubleLeftArrow;': '\u21d0', 'COPY': '\xa9', 'frac13;': '\u2153', 'middot': '\xb7', 'pr;': '\u227a',
             'rhov;': '\u03f1', 'Qopf;': '\u211a', 'weierp;': '\u2118', 'ofr;': '\U0001d52c', 'lrhard;': '\u296d',
             'commat;': '@', 'nesear;': '\u2928', 'sopf;': '\U0001d564', 'raquo': '\xbb', 'malt;': '\u2720',
             'OElig;': '\u0152', 'Uscr;': '\U0001d4b0', 'eqslantless;': '\u2a95', 'LeftTriangleEqual;': '\u22b4',
             'oacute': '\xf3', 'andslope;': '\u2a58', 'yfr;': '\U0001d536', 'nsup;': '\u2285', 'NotElement;': '\u2209',
             'angmsdaf;': '\u29ad', 'nsccue;': '\u22e1', 'ge;': '\u2265', 'fallingdotseq;': '\u2252', 'rbarr;': '\u290d',
             'DoubleLongLeftRightArrow;': '\u27fa', 'uparrow;': '\u2191', 'orarr;': '\u21bb', 'Rcy;': '\u0420',
             'acute;': '\xb4', 'NewLine;': '\n', 'lmoust;': '\u23b0', 'NegativeMediumSpace;': '\u200b', 'Nacute;': '\u0143',
             'aelig': '\xe6', 'prcue;': '\u227c', 'ensp;': '\u2002', 'utdot;': '\u22f0', 'napos;': '\u0149',
             'DoubleLongRightArrow;': '\u27f9', 'Vfr;': '\U0001d519', 'xutri;': '\u25b3', 'awint;': '\u2a11',
             'leftrightsquigarrow;': '\u21ad', 'plusacir;': '\u2a23', 'FilledVerySmallSquare;': '\u25aa', 'Mscr;': '\u2133',
             'leftrightharpoons;': '\u21cb', 'sqcups;': '\u2294\ufe00', 'LJcy;': '\u0409', 'circleddash;': '\u229d',
             'NoBreak;': '\u2060', 'nlsim;': '\u2274', 'Uogon;': '\u0172', 'NotRightTriangleBar;': '\u29d0\u0338',
             'Ecy;': '\u042d', 'sdot;': '\u22c5', 'smeparsl;': '\u29e4', 'niv;': '\u220b', 'kcedil;': '\u0137',
             'xrarr;': '\u27f6', 'isindot;': '\u22f5', 'xodot;': '\u2a00', 'gtdot;': '\u22d7', 'natural;': '\u266e',
             'eqvparsl;': '\u29e5', 'gnap;': '\u2a8a', 'Psi;': '\u03a8', 'Rho;': '\u03a1', 'micro;': '\xb5',
             'cylcty;': '\u232d', 'gesles;': '\u2a94', 'uHar;': '\u2963', 'CircleTimes;': '\u2297', 'sqsub;': '\u228f',
             'ldrushar;': '\u294b', 'bsol;': '\\', 'rcedil;': '\u0157', 'nprec;': '\u2280', 'vltri;': '\u22b2',
             'atilde;': '\xe3', 'prsim;': '\u227e', 'primes;': '\u2119', 'Omicron;': '\u039f', 'ocirc;': '\xf4',
             'iiint;': '\u222d', 'quest;': '?', 'daleth;': '\u2138', 'nbsp': '\xa0', 'nwArr;': '\u21d6', 'gammad;': '\u03dd',
             'heartsuit;': '\u2665', 'wedbar;': '\u2a5f', 'OverBrace;': '\u23de', 'spar;': '\u2225', 'brvbar': '\xa6',
             'blacktriangleleft;': '\u25c2', 'lopar;': '\u2985', 'xwedge;': '\u22c0', 'iexcl;': '\xa1', 'boxul;': '\u2518',
             'Imacr;': '\u012a', 'ominus;': '\u2296', 'eopf;': '\U0001d556', 'DotDot;': '\u20dc', 'Scirc;': '\u015c',
             'succnsim;': '\u22e9', 'sigmaf;': '\u03c2', 'ReverseEquilibrium;': '\u21cb', 'DiacriticalDot;': '\u02d9',
             'AElig;': '\xc6', 'zigrarr;': '\u21dd', 'NegativeThinSpace;': '\u200b', 'approxeq;': '\u224a', 'Gcy;': '\u0413',
             'Vert;': '\u2016', 'NotSquareSupersetEqual;': '\u22e3', 'srarr;': '\u2192', 'rtrie;': '\u22b5',
             'VeryThinSpace;': '\u200a', 'RightDoubleBracket;': '\u27e7', 'dfr;': '\U0001d521', 'Eogon;': '\u0118',
             'Cscr;': '\U0001d49e', 'gnE;': '\u2269', 'nparallel;': '\u2226', 'lsime;': '\u2a8d', 'lceil;': '\u2308',
             'ijlig;': '\u0133', 'RightCeiling;': '\u2309', 'Icy;': '\u0418', 'yuml': '\xff', 'exist;': '\u2203',
             'DiacriticalAcute;': '\xb4', 'boxVr;': '\u255f', 'mscr;': '\U0001d4c2', 'NotGreaterSlantEqual;': '\u2a7e\u0338',
             'leftrightarrow;': '\u2194', 'Wopf;': '\U0001d54e', 'supset;': '\u2283', 'DownArrowUpArrow;': '\u21f5',
             'glj;': '\u2aa4', 'Colone;': '\u2a74', 'prnsim;': '\u22e8', 'Zfr;': '\u2128', 'lbrkslu;': '\u298d',
             'scedil;': '\u015f', 'Dcaron;': '\u010e', 'coloneq;': '\u2254', 'CapitalDifferentialD;': '\u2145',
             'nshortmid;': '\u2224', 'trianglelefteq;': '\u22b4', 'rarrb;': '\u21e5', 'ssetmn;': '\u2216', 'ufr;': '\U0001d532',
             'Acirc;': '\xc2', 'LeftRightArrow;': '\u2194', 'varr;': '\u2195', 'eth': '\xf0', 'varsupsetneqq;': '\u2acc\ufe00',
             'HilbertSpace;': '\u210b', 'diamond;': '\u22c4', 'npart;': '\u2202\u0338', 'Cfr;': '\u212d', 'slarr;': '\u2190',
             'cwconint;': '\u2232', 'ncaron;': '\u0148', 'theta;': '\u03b8', 'NotSupersetEqual;': '\u2289',
             'nsubset;': '\u2282\u20d2', 'EmptySmallSquare;': '\u25fb', 'Tstrok;': '\u0166', 'lg;': '\u2276', 'urcorn;': '\u231d',
             'acy;': '\u0430', 'DoubleVerticalBar;': '\u2225', 'Phi;': '\u03a6', 'imof;': '\u22b7', 'angle;': '\u2220',
             'supdot;': '\u2abe', 'timesb;': '\u22a0', 'bfr;': '\U0001d51f', 'dcaron;': '\u010f', 'Aacute': '\xc1',
             'cent': '\xa2', 'rdquo;': '\u201d', 'jopf;': '\U0001d55b', 'sup2;': '\xb2', 'triangledown;': '\u25bf',
             'lHar;': '\u2962', 'leftarrowtail;': '\u21a2', 'HorizontalLine;': '\u2500', 'duarr;': '\u21f5', 'cupcap;': '\u2a46',
             'euml': '\xeb', 'shy': '\xad', 'curarr;': '\u21b7', 'larrhk;': '\u21a9', 'Kfr;': '\U0001d50e', 'olarr;': '\u21ba',
             'nsupE;': '\u2ac6\u0338', 'colon;': ':', 'Eta;': '\u0397', 'dsol;': '\u29f6', 'LessGreater;': '\u2276',
             'dblac;': '\u02dd', 'vopf;': '\U0001d567', 'incare;': '\u2105', 'wreath;': '\u2240', 'NotSucceedsEqual;': '\u2ab0\u0338',
             'lcaron;': '\u013e', 'conint;': '\u222e', 'napid;': '\u224b\u0338', 'Equal;': '\u2a75', 'dscr;': '\U0001d4b9',
             'Itilde;': '\u0128', 'iiota;': '\u2129', 'UpDownArrow;': '\u2195', 'Vcy;': '\u0412', 'lobrk;': '\u27e6',
             'thksim;': '\u223c', 'Ucirc;': '\xdb', 'Rcedil;': '\u0156', 'tritime;': '\u2a3b', 'boxh;': '\u2500',
             'Fouriertrf;': '\u2131', 'realine;': '\u211b', 'rightleftarrows;': '\u21c4', 'wp;': '\u2118', 'thkap;': '\u2248',
             'sqsupset;': '\u2290', 'CloseCurlyQuote;': '\u2019', 'SquareSubsetEqual;': '\u2291', 'Iuml;': '\xcf',
             'sqsup;': '\u2290', 'NotDoubleVerticalBar;': '\u2226', 'ugrave': '\xf9', 'acd;': '\u223f', 'oscr;': '\u2134',
             'Qfr;': '\U0001d514', 'ncap;': '\u2a43', 'Vdash;': '\u22a9', 'nrtrie;': '\u22ed', 'lesdot;': '\u2a7f',
             'nltri;': '\u22ea', 'ncy;': '\u043d', 'Hacek;': '\u02c7', 'radic;': '\u221a', 'frac78;': '\u215e',
             'NotReverseElement;': '\u220c', 'Therefore;': '\u2234', 'lates;': '\u2aad\ufe00', 'varepsilon;': '\u03f5',
             'ruluhar;': '\u2968', 'rsaquo;': '\u203a', 'Tscr;': '\U0001d4af', 'subsetneq;': '\u228a', 'UnderBrace;': '\u23df',
             'Uring;': '\u016e', 'acirc': '\xe2', 'check;': '\u2713', 'rsquor;': '\u2019', 'tbrk;': '\u23b4',
             'NotLessTilde;': '\u2274', 'vsupne;': '\u228b\ufe00', 'wfr;': '\U0001d534', 'hellip;': '\u2026', 'nless;': '\u226e',
             'Yuml;': '\u0178', 'FilledSmallSquare;': '\u25fc', 'SucceedsEqual;': '\u2ab0', 'frac23;': '\u2154',
             'OverBracket;': '\u23b4', 'SupersetEqual;': '\u2287', 'gesdot;': '\u2a80', 'excl;': '!', 'UpArrowBar;': '\u2912',
             'barwed;': '\u2305', 'barwedge;': '\u2305', 'notinvc;': '\u22f6', 'uArr;': '\u21d1', 'lthree;': '\u22cb',
             'risingdotseq;': '\u2253', 'Mopf;': '\U0001d544', 'yacute;': '\xfd', 'otimesas;': '\u2a36', 'capcup;': '\u2a47',
             'ofcir;': '\u29bf', 'Upsi;': '\u03d2', 'Ecaron;': '\u011a', 'Qscr;': '\U0001d4ac', 'hookleftarrow;': '\u21a9',
             'Ograve;': '\xd2', 'precnapprox;': '\u2ab9', 'Uarrocir;': '\u2949', 'part;': '\u2202', 'subsub;': '\u2ad5',
             'lmidot;': '\u0140', 'DJcy;': '\u0402', 'nexists;': '\u2204', 'NotEqualTilde;': '\u2242\u0338',
             'profalar;': '\u232e', 'sum;': '\u2211', 'Precedes;': '\u227a', 'Ofr;': '\U0001d512', 'fopf;': '\U0001d557',
             'iecy;': '\u0435', 'ShortUpArrow;': '\u2191', 'nparsl;': '\u2afd\u20e5', 'boxUR;': '\u255a',
             'exponentiale;': '\u2147', 'upsilon;': '\u03c5', 'Jopf;': '\U0001d541', 'VerticalSeparator;': '\u2758',
             'Dfr;': '\U0001d507', 'NonBreakingSpace;': '\xa0', 'bottom;': '\u22a5', 'orslope;': '\u2a57', 'boxDL;': '\u2557',
             'bigcap;': '\u22c2', 'Vbar;': '\u2aeb', 'pound;': '\xa3', 'boxvr;': '\u251c', 'Cup;': '\u22d3',
             'bigtriangleup;': '\u25b3', 'RightAngleBracket;': '\u27e9', 'lesg;': '\u22da\ufe00', 'RightDownVector;': '\u21c2',
             'Gfr;': '\U0001d50a', 'shy;': '\xad', 'supnE;': '\u2acc', 'cirE;': '\u29c3', 'angmsdae;': '\u29ac',
             'Bumpeq;': '\u224e', 'delta;': '\u03b4', 'thinsp;': '\u2009', 'EmptyVerySmallSquare;': '\u25ab',
             'leftleftarrows;': '\u21c7', 'les;': '\u2a7d', 'ltcc;': '\u2aa6', 'TildeFullEqual;': '\u2245', 'iocy;': '\u0451',
             'supsetneqq;': '\u2acc', 'rharul;': '\u296c', 'hArr;': '\u21d4', 'amp': '&', 'Cdot;': '\u010a', 'rbrack;': ']',
             'nspar;': '\u2226', 'pcy;': '\u043f', 'NotSucceedsTilde;': '\u227f\u0338', 'acute': '\xb4', 'dlcrop;': '\u230d',
             'subdot;': '\u2abd', 'UnionPlus;': '\u228e', 'mapstoleft;': '\u21a4', 'DoubleRightTee;': '\u22a8',
             'sigmav;': '\u03c2', 'sfr;': '\U0001d530', 'Igrave': '\xcc', 'euro;': '\u20ac', 'complement;': '\u2201',
             'profsurf;': '\u2313', 'nabla;': '\u2207', 'para;': '\xb6', 'Dopf;': '\U0001d53b', 'cdot;': '\u010b',
             'sim;': '\u223c', 'popf;': '\U0001d561', 'ImaginaryI;': '\u2148', 'notni;': '\u220c', 'RightArrowBar;': '\u21e5',
             'intlarhk;': '\u2a17', 'gtcir;': '\u2a7a', 'llcorner;': '\u231e', 'Bfr;': '\U0001d505', 'Rang;': '\u27eb',
             'ddagger;': '\u2021', 'vBarv;': '\u2ae9', 'forkv;': '\u2ad9', 'angmsd;': '\u2221', 'ouml;': '\xf6',
             'nvgt;': '>\u20d2', 'Dagger;': '\u2021', 'lharu;': '\u21bc', 'Exists;': '\u2203', 'LeftTriangleBar;': '\u29cf',
             'ratio;': '\u2236', 'TildeTilde;': '\u2248', 'minusb;': '\u229f', 'race;': '\u223d\u0331', 'rAarr;': '\u21db',
             'bigoplus;': '\u2a01', 'rangd;': '\u2992', 'micro': '\xb5', 'osol;': '\u2298', 'strns;': '\xaf',
             'Longleftrightarrow;': '\u27fa', 'boxUl;': '\u255c', 'Sc;': '\u2abc', 'ocirc': '\xf4', 'ac;': '\u223e',
             'nsubE;': '\u2ac5\u0338', 'DotEqual;': '\u2250', 'zopf;': '\U0001d56b', 'llarr;': '\u21c7', 'permil;': '\u2030',
             'Topf;': '\U0001d54b', 'UpperLeftArrow;': '\u2196', 'ulcorn;': '\u231c', 'curlyeqsucc;': '\u22df',
             'aleph;': '\u2135', 'image;': '\u2111', 'igrave': '\xec', 'NestedLessLess;': '\u226a', 'LongLeftRightArrow;': '\u27f7',
             'sqsupe;': '\u2292', 'midast;': '*', 'dwangle;': '\u29a6', 'uring;': '\u016f', 'becaus;': '\u2235',
             'GreaterFullEqual;': '\u2267', 'dd;': '\u2146', 'kcy;': '\u043a', 'Laplacetrf;': '\u2112', 'marker;': '\u25ae',
             'simrarr;': '\u2972', 'Agrave;': '\xc0', 'bNot;': '\u2aed', 'ocir;': '\u229a', 'supsetneq;': '\u228b',
             'fork;': '\u22d4', 'pi;': '\u03c0', 'topbot;': '\u2336', 'xharr;': '\u27f7', 'Jukcy;': '\u0404',
             'naturals;': '\u2115', 'csup;': '\u2ad0', 'ltimes;': '\u22c9', 'mcy;': '\u043c', 'lessgtr;': '\u2276',
             'uuml': '\xfc', 'iquest;': '\xbf', 'boxhd;': '\u252c', 'nsupe;': '\u2289', 'leftharpoondown;': '\u21bd',
             'Lacute;': '\u0139', 'Emacr;': '\u0112', 'Vee;': '\u22c1', 'cupcup;': '\u2a4a', 'backsimeq;': '\u22cd',
             'dlcorn;': '\u231e', 'bprime;': '\u2035', 'HumpEqual;': '\u224f', 'simdot;': '\u2a6a', 'oelig;': '\u0153',
             'ntilde;': '\xf1', 'xdtri;': '\u25bd', 'hscr;': '\U0001d4bd', 'cups;': '\u222a\ufe00', 'pre;': '\u2aaf',
             'yscr;': '\U0001d4ce', 'boxplus;': '\u229e', 'Jcirc;': '\u0134', 'suphsol;': '\u27c9', 'Nopf;': '\u2115',
             'DZcy;': '\u040f', 'flat;': '\u266d', 'ldquor;': '\u201e', 'Leftrightarrow;': '\u21d4', 'veebar;': '\u22bb',
             'Rrightarrow;': '\u21db', 'compfn;': '\u2218', 'succ;': '\u227b', 'NegativeVeryThinSpace;': '\u200b',
             'cupbrcap;': '\u2a48', 'notindot;': '\u22f5\u0338', 'supseteqq;': '\u2ac6', 'plankv;': '\u210f', 'ordm': '\xba',
             'nsupseteq;': '\u2289', 'sacute;': '\u015b', 'ordm;': '\xba', 'dtdot;': '\u22f1', 'NotSubsetEqual;': '\u2288',
             'subedot;': '\u2ac3', 'curlywedge;': '\u22cf', 'GreaterGreater;': '\u2aa2', 'dbkarow;': '\u290f',
             'quatint;': '\u2a16', 'ContourIntegral;': '\u222e', 'LeftTriangle;': '\u22b2', 'lrcorner;': '\u231f',
             'RightVectorBar;': '\u2953', 'nequiv;': '\u2262', 'ltrie;': '\u22b4', 'divonx;': '\u22c7', 'topf;': '\U0001d565',
             'cuepr;': '\u22de', 'LeftRightVector;': '\u294e', 'rtimes;': '\u22ca', 'LeftCeiling;': '\u2308', 'iukcy;': '\u0456',
             'ordf;': '\xaa', 'OpenCurlyQuote;': '\u2018', 'fnof;': '\u0192', 'thorn': '\xfe', 'star;': '\u2606',
             'lne;': '\u2a87', 'hearts;': '\u2665', 'dash;': '\u2010', 'vartriangleleft;': '\u22b2', 'shcy;': '\u0448',
             'hfr;': '\U0001d525', 'uuarr;': '\u21c8', 'isin;': '\u2208', 'tcaron;': '\u0165', 'bigodot;': '\u2a00',
             'lurdshar;': '\u294a', 'ucy;': '\u0443', 'nmid;': '\u2224', 'semi;': ';', 'laquo;': '\xab', 'bullet;': '\u2022',
             'hslash;': '\u210f', 'gtrsim;': '\u2273', 'InvisibleTimes;': '\u2062', 'cfr;': '\U0001d520', 'tscr;': '\U0001d4c9',
             'nltrie;': '\u22ec', 'succcurlyeq;': '\u227d', 'ogon;': '\u02db', 'NotExists;': '\u2204', 'kgreen;': '\u0138',
             'seArr;': '\u21d8', 'Product;': '\u220f', 'sqcap;': '\u2293', 'rx;': '\u211e', 'nLeftarrow;': '\u21cd',
             'Updownarrow;': '\u21d5', 'Ecirc': '\xca', 'Lcy;': '\u041b', 'icirc;': '\xee', 'bigstar;': '\u2605',
             'gtcc;': '\u2aa7', 'olcross;': '\u29bb', 'in;': '\u2208', 'VerticalTilde;': '\u2240', 'filig;': '\ufb01',
             'rightsquigarrow;': '\u219d', 'pfr;': '\U0001d52d', 'Intersection;': '\u22c2', 'Not;': '\u2aec', 'rsqb;': ']',
             'Ncy;': '\u041d', 'period;': '.', 'xhArr;': '\u27fa', 'phmmat;': '\u2133', 'NotCongruent;': '\u2262',
             'boxdR;': '\u2552', 'kjcy;': '\u045c', 'bigwedge;': '\u22c0', 'NotGreaterTilde;': '\u2275', 'nsqsupe;': '\u22e3',
             'aring;': '\xe5', 'prnE;': '\u2ab5', 'LessFullEqual;': '\u2266', 'eqcirc;': '\u2256', 'downharpoonleft;': '\u21c3',
             'rlarr;': '\u21c4', 'smallsetminus;': '\u2216', 'omega;': '\u03c9', 'mldr;': '\u2026', 'vzigzag;': '\u299a',
             'nleqq;': '\u2266\u0338', 'ulcrop;': '\u230f', 'straightepsilon;': '\u03f5', 'Auml;': '\xc4', 'LongLeftArrow;': '\u27f5'}


    def substitute_entity(match):
        ent = match.group(2) + match.group(3)
        res = ""
        while not ent in html5 and not ent.endswith(";") and match.group(1) != "#":
            # Excepción para cuando '&' se usa como argumento en la urls contenidas en los datos
            try:
                res = ent[-1] + res
                ent = ent[:-1]
            except:
                break

        if match.group(1) == "#":
            ent = unichr(int(ent.replace(";","")))
            return ent.encode('utf-8')
        else:
            cp = html5.get(ent)
            if cp:
                return cp.decode("unicode-escape").encode('utf-8') + res
            else:
                return match.group()

    return entity_re.subn(substitute_entity, data)[0]

