# -*- coding: utf-8 -*-
from datetime import datetime
from modules.kodi_utils import local_string as ls

years_movies = range(datetime.today().year, 1899, -1)

years_tvshows = range(datetime.today().year, 1941, -1)

decades_movies = [i for i in years_movies if not i % 10]

decades_tvshows = [i for i in years_tvshows if not i % 10] + ['1940']

oscar_winners = (
		[776503, 581734, 496243, 490132, 399055, 376867, 314365, 194662, 76203, 68734, 74643, 45269, 12162, 12405, 6977, 1422, 1640, 70, 122, 1574],
		[453, 98, 14, 1934, 597, 409, 197, 13, 424, 33, 274, 581, 403, 380, 746, 792, 606, 279, 11050, 783],
		[9443, 16619, 12102, 11778, 703, 1366, 510, 240, 9277, 238, 1051, 11202, 3116, 17917, 10633, 874, 15121, 11113, 5769, 947],
		[1725, 284, 665, 17281, 826, 2897, 15919, 654, 11426, 27191, 2769, 705, 25430, 23383, 33667, 887, 28580, 17661, 27367, 289],
		[43266, 223, 770, 34106, 43278, 43277, 12311, 3078, 56164, 33680, 42861, 143, 65203, 28966, 631]
	)

movie_certifications = (
		'G',
		'PG',
		'PG-13',
		'R',
		'NC-17',
		'NR'
	)

tvshow_certifications = (
		'tv-y',
		'tv-y7',
		'tv-g',
		'tv-pg',
		'tv-14',
		'tv-ma'
	)

languages = (
		(ls(32861), 'ar'), (ls(32862), 'bs'),   (ls(32863), 'bg'),   (ls(32864), 'zh'),   (ls(32865), 'hr'),   (ls(32866), 'nl'),   (ls(32867), 'en'),
		(ls(32868), 'fi'), (ls(32869), 'fr'),   (ls(32870), 'de'),   (ls(32871), 'el'),   (ls(32872), 'he'),   (ls(32873), 'hi'),   (ls(32874), 'hu'),
		(ls(32875), 'is'), (ls(32876), 'it'),   (ls(32877), 'ja'),   (ls(32878), 'ko'),   (ls(32879), 'mk'),   (ls(32880), 'no'),   (ls(32881), 'fa'),
		(ls(32882), 'pl'), (ls(32883), 'pt'),   (ls(32884), 'pa'),   (ls(32885), 'ro'),   (ls(32886), 'ru'),   (ls(32887), 'sr'),   (ls(32888), 'sl'),
		(ls(32889), 'es'), (ls(32890), 'sv'),   (ls(32891), 'tr'),   (ls(32892), 'uk')
	)
		

meta_languages = [
		{'iso': 'zh', 'name': 'Chinese'},          {'iso': 'hr', 'name': 'Croatian'},
		{'iso': 'cs', 'name': 'Czech'},            {'iso': 'da', 'name': 'Danish'},
		{'iso': 'nl', 'name': 'Dutch'},            {'iso': 'en', 'name': 'English'},
		{'iso': 'fi', 'name': 'Finnish'},          {'iso': 'fr', 'name': 'French'},
		{'iso': 'de', 'name': 'German'},           {'iso': 'el', 'name': 'Greek'},
		{'iso': 'he', 'name': 'Hebrew'},           {'iso': 'hu', 'name': 'Hungarian'},
		{'iso': 'it', 'name': 'Italian'},          {'iso': 'ja', 'name': 'Japanese'},
		{'iso': 'ko', 'name': 'Korean'},           {'iso': 'no', 'name': 'Norwegian'},
		{'iso': 'pl', 'name': 'Polish'},           {'iso': 'pt', 'name': 'Portuguese'},
		{'iso': 'ru', 'name': 'Russian'},          {'iso': 'sl', 'name': 'Slovenian'},
		{'iso': 'es', 'name': 'Spanish'},          {'iso': 'sv', 'name': 'Swedish'},
		{'iso': 'tr', 'name': 'Turkish'},          {'iso': 'ar-SA', 'name': 'Arabic Saudi Arabia'}
	]

regions = (
		{'code': 'AF', 'name': ls(32893)},   {'code': 'AL', 'name': ls(32894)},   {'code': 'DZ', 'name': ls(32895)},   {'code': 'AQ', 'name': ls(32896)},
		{'code': 'AR', 'name': ls(32897)},   {'code': 'AM', 'name': ls(32898)},   {'code': 'AU', 'name': ls(32899)},   {'code': 'AT', 'name': ls(32900)},
		{'code': 'BD', 'name': ls(32901)},   {'code': 'BY', 'name': ls(32902)},   {'code': 'BE', 'name': ls(32903)},   {'code': 'BR', 'name': ls(32904)},
		{'code': 'BG', 'name': ls(32905)},   {'code': 'KH', 'name': ls(32906)},   {'code': 'CA', 'name': ls(32907)},   {'code': 'CL', 'name': ls(32908)},
		{'code': 'CN', 'name': ls(32909)},   {'code': 'HR', 'name': ls(32910)},   {'code': 'CZ', 'name': ls(32911)},   {'code': 'DK', 'name': ls(32912)},
		{'code': 'EG', 'name': ls(32913)},   {'code': 'FI', 'name': ls(32914)},   {'code': 'FR', 'name': ls(32915)},   {'code': 'DE', 'name': ls(32916)},
		{'code': 'GR', 'name': ls(32917)},   {'code': 'HK', 'name': ls(32918)},   {'code': 'HU', 'name': ls(32919)},   {'code': 'IS', 'name': ls(32920)},
		{'code': 'IN', 'name': ls(32921)},   {'code': 'ID', 'name': ls(32922)},   {'code': 'IR', 'name': ls(32923)},   {'code': 'IQ', 'name': ls(32924)},
		{'code': 'IE', 'name': ls(32925)},   {'code': 'IL', 'name': ls(32926)},   {'code': 'IT', 'name': ls(32927)},   {'code': 'JP', 'name': ls(32928)},
		{'code': 'MY', 'name': ls(32929)},   {'code': 'NP', 'name': ls(32930)},   {'code': 'NL', 'name': ls(32931)},   {'code': 'NZ', 'name': ls(32932)},
		{'code': 'NO', 'name': ls(32933)},   {'code': 'PK', 'name': ls(32934)},   {'code': 'PY', 'name': ls(32935)},   {'code': 'PE', 'name': ls(32936)},
		{'code': 'PH', 'name': ls(32937)},   {'code': 'PL', 'name': ls(32938)},   {'code': 'PT', 'name': ls(32939)},   {'code': 'PR', 'name': ls(32940)},
		{'code': 'RO', 'name': ls(32941)},   {'code': 'RU', 'name': ls(32942)},   {'code': 'SA', 'name': ls(32943)},   {'code': 'RS', 'name': ls(32944)},
		{'code': 'SG', 'name': ls(32945)},   {'code': 'SK', 'name': ls(32946)},   {'code': 'SI', 'name': ls(32947)},   {'code': 'ZA', 'name': ls(32948)},
		{'code': 'ES', 'name': ls(32949)},   {'code': 'LK', 'name': ls(32950)},   {'code': 'SE', 'name': ls(32951)},   {'code': 'CH', 'name': ls(32952)},
		{'code': 'TH', 'name': ls(32953)},   {'code': 'TR', 'name': ls(32954)},   {'code': 'UA', 'name': ls(32955)},   {'code': 'AE', 'name': ls(32956)},
		{'code': 'GB', 'name': ls(32957)},   {'code': 'US', 'name': ls(32958)},   {'code': 'UY', 'name': ls(32959)},   {'code': 'VE', 'name': ls(32960)},
		{'code': 'VN', 'name': ls(32961)},   {'code': 'YE', 'name': ls(32962)},   {'code': 'ZW', 'name': ls(32963)}
	)

movie_genres = {
		ls(32548): ['28', 'genre_action'],                ls(32549): ['12', 'genre_adventure'],
		ls(32550): ['16', 'genre_animation'],             ls(32551): ['35', 'genre_comedy'],
		ls(32552): ['80', 'genre_crime'],                 ls(32553): ['99', 'genre_documentary'],
		ls(32554): ['18', 'genre_drama'],                 ls(32555): ['10751', 'genre_family'],
		ls(32558): ['14', 'genre_fantasy'],               ls(32559): ['36', 'genre_history'],
		ls(32560): ['27', 'genre_horror'],                ls(32561): ['10402', 'genre_music'],
		ls(32557): ['9648', 'genre_mystery'],             ls(32562): ['10749', 'genre_romance'],
		ls(32563): ['878', 'genre_scifi'],                ls(32564): ['10770', 'genre_soap'],
		ls(32565): ['53', 'genre_thriller'],              ls(32566): ['10752', 'genre_war'], 
		ls(32567): ['37', 'genre_western']
	}

tvshow_genres = {
		'%s & %s' % (ls(32548), ls(32549)): ['10759', 'genre_action'],         ls(32550): ['16', 'genre_animation'],
		ls(32551): ['35', 'genre_comedy'],                                     ls(32552): ['80', 'genre_crime'],
		ls(32553): ['99', 'genre_documentary'],                                ls(32554): ['18', 'genre_drama'],
		ls(32555): ['10751', 'genre_family'],                                  ls(32556): ['10762', 'genre_kids'],
		ls(32557): ['9648', 'genre_mystery'],                                  ls(32568):['10763', 'genre_news'],
		ls(32569): ['10764', 'genre_reality'],                                 ls(33057): ['10765', 'genre_scifi'],
		ls(32570): ['10766', 'genre_soap'],                                    ls(32570): ['10767', 'genre_talk'],
		ls(32572): ['10768', 'genre_war'],                                     ls(32567): ['37', 'genre_western']
	}

networks = (
		{'id':54,'name':'Disney Channel','logo': 'network_disney'},                   {'id':44,'name':'Disney XD','logo': 'network_disneyxd'},
		{'id':2,'name':'ABC','logo': 'network_abc'},                                  {'id':493,'name':'BBC America','logo': 'network_bbcamerica'},
		{'id':6,'name':'NBC','logo': 'network_nbc'},                                  {'id':13,'name':'Nickelodeon','logo': 'network_nickelodeon'},
		{'id':14,'name':'PBS','logo': 'network_pbs'},                                 {'id':16,'name':'CBS','logo': 'network_cbs'},
		{'id':19,'name':'FOX','logo': 'network_fox'},                                 {'id':21,'name':'The WB','logo': 'network_thewb'},
		{'id':24,'name':'BET','logo': 'network_bet'},                                 {'id':30,'name':'USA Network','logo': 'network_usanetwork'},
		{'id':32,'name':'CBC','logo': 'network_cbc'},                                 {'id':173,'name':'AT-X','logo': 'network_atx'},
		{'id':33,'name':'MTV','logo': 'network_mtv'},                                 {'id':34,'name':'Lifetime','logo': 'network_lifetime'},
		{'id':35,'name':'Nick Junior','logo': 'network_nickjr'},                      {'id':41,'name':'TNT','logo': 'network_tnt'},
		{'id':43,'name':'National Geographic','logo': 'network_natgeo'},              {'id':47,'name':'Comedy Central','logo': 'network_comedycentral'},
		{'id':49,'name':'HBO','logo': 'network_hbo'},                                 {'id':55,'name':'Spike','logo': 'network_spike'},
		{'id':67,'name':'Showtime','logo': 'network_showtime'},                       {'id':56,'name':'Cartoon Network','logo': 'network_cartoonnetwork'},
		{'id':65,'name':'History Channel','logo': 'network_history'},                 {'id':84,'name':'TLC','logo': 'network_tlc'},
		{'id':68,'name':'TBS','logo': 'network_tbs'},                                 {'id':71,'name':'The CW','logo': 'network_thecw'},
		{'id':74,'name':'Bravo','logo': 'network_bravo'},                             {'id':76,'name':'E!','logo': 'network_e'},
		{'id':77,'name':'Syfy','logo': 'network_syfy'},                               {'id':80,'name':'Adult Swim','logo': 'network_adultswim'},
		{'id':91,'name':'Animal Planet','logo': 'network_animalplanet'},              {'id':110,'name':'CTV','logo': 'network_ctv'},
		{'id':129,'name':'A&E','logo': 'network_ane'},                                {'id':158,'name':'VH1','logo': 'network_vh1'},
		{'id':174,'name':'AMC','logo': 'network_amc'},                                {'id':928,'name':'Crackle','logo': 'network_crackle'},
		{'id':202,'name':'WGN America','logo': 'network_wgnamerica'},                 {'id':209,'name':'Travel Channel','logo': 'network_travel'},
		{'id':213, 'name':'Netflix','logo': 'network_netflix'},                       {'id':251,'name':'Audience','logo': 'network_audience'},
		{'id':270,'name':'SundanceTV','logo': 'network_sundancetv'},                  {'id':318,'name':'Starz','logo': 'network_starz'},
		{'id':359,'name':'Cinemax','logo': 'network_cinemax'},                        {'id':364,'name':'truTV','logo': 'network_trutv'},
		{'id':384,'name':'Hallmark Channel','logo': 'network_hallmark'},              {'id':397,'name':'TV Land','logo': 'network_tvland'},
		{'id':1024,'name':'Amazon','logo': 'network_amazon'},                         {'id':1267,'name':'Freeform','logo': 'network_freeform'},
		{'id':4,'name':'BBC 1','logo': 'network_bbc1'},                               {'id':332,'name':'BBC 2','logo': 'network_bbc2'},
		{'id':3,'name':'BBC 3','logo': 'network_bbc3'},                               {'id':100,'name':'BBC 4','logo': 'network_bbc4'},
		{'id':214,'name':'Sky 1','logo': 'network_sky1'},                             {'id':9,'name':'ITV','logo': 'network_itv'},
		{'id':26,'name':'Channel 4','logo': 'network_channel4'},                      {'id':99,'name':'Channel 5','logo': 'network_channel5'},
		{'id':136,'name':'E4','logo': 'network_e4'},                                  {'id':210,'name':'HGTV','logo': 'network_hgtv'},
		{'id':453,'name':'Hulu','logo': 'network_hulu'},                              {'id':1436,'name':'YouTube Red','logo': 'network_youtubered'},
		{'id':64,'name':'Discovery Channel','logo': 'network_discovery'},             {'id':2739,'name':'Disney+','logo': 'network_disneyplus'},
		{'id':2552,'name':'Apple TV +','logo': 'network_appletvplus'},                {'id':2697,'name':'Acorn TV','logo': 'network_acorntv'},
		{'id':1709,'name':'CBS All Access','logo': 'network_cbsallaccess'},           {'id':3186,'name':'HBO Max','logo': 'network_hbomax'},
		{'id':2243,'name':'DC Universe','logo': 'network_dcuniverse'},                {'id':2076,'name':'Paramount Network','logo': 'network_paramount'},
		{'id':4330,'name':'Paramount+','logo': 'network_paramountplus'},              {'id': 3353, 'name': 'Peacock', 'logo': 'network_peacock'},
		{'id':4353,'name':'Discovery+','logo': 'network_discoveryplus'}
	)

language_choices =  {
		'None': None,              'Afrikaans': 'afr',            'Albanian': 'alb',             'Arabic': 'ara',
		'Armenian': 'arm',         'Basque': 'baq',               'Bengali': 'ben',              'Bosnian': 'bos',
		'Breton': 'bre',           'Bulgarian': 'bul',            'Burmese': 'bur',              'Catalan': 'cat',
		'Chinese': 'chi',          'Croatian': 'hrv',             'Czech': 'cze',                'Danish': 'dan',
		'Dutch': 'dut',            'English': 'eng',              'Esperanto': 'epo',            'Estonian': 'est',
		'Finnish': 'fin',          'French': 'fre',               'Galician': 'glg',             'Georgian': 'geo',
		'German': 'ger',           'Greek': 'ell',                'Hebrew': 'heb',               'Hindi': 'hin',
		'Hungarian': 'hun',        'Icelandic': 'ice',            'Indonesian': 'ind',           'Italian': 'ita',
		'Japanese': 'jpn',         'Kazakh': 'kaz',               'Khmer': 'khm',                'Korean': 'kor',
		'Latvian': 'lav',          'Lithuanian': 'lit',           'Luxembourgish': 'ltz',        'Macedonian': 'mac',
		'Malay': 'may',            'Malayalam': 'mal',            'Manipuri': 'mni',             'Mongolian': 'mon',
		'Montenegrin': 'mne',      'Norwegian': 'nor',            'Occitan': 'oci',              'Persian': 'per',
		'Polish': 'pol',           'Portuguese': 'por',           'Portuguese(Brazil)': 'pob',   'Romanian': 'rum',
		'Russian': 'rus',          'Serbian': 'scc',              'Sinhalese': 'sin',            'Slovak': 'slo',
		'Slovenian': 'slv',        'Spanish': 'spa',              'Swahili': 'swa',              'Swedish': 'swe',
		'Syriac': 'syr',           'Tagalog': 'tgl',              'Tamil': 'tam',                'Telugu': 'tel',
		'Thai': 'tha',             'Turkish': 'tur',              'Ukrainian': 'ukr',            'Urdu': 'urd',
		'Vietnamese': 'vie'
	}

colors = [
		'black', 'white', 'whitesmoke', 'gainsboro', 'lightgray', 'silver', 'darkgray', 'gray', 'dimgray', 'snow', 'floralwhite', 'ivory', 'beige', 'cornsilk', 'antiquewhite',
		'bisque', 'blanchedalmond', 'burlywood', 'darkgoldenrod', 'ghostwhite', 'azure', 'lightsaltegray', 'lightsteelblue', 'powderblue', 'lightblue', 'skyblue', 'lightskyblue',
		'deepskyblue', 'dodgerblue', 'royalblue', 'blue', 'mediumblue', 'midnightblue', 'navy', 'darkblue', 'cornflowerblue', 'slateblue', 'slategray', 'yellowgreen', 'springgreen',
		'seagreen', 'steelblue', 'teal', 'fuchsia', 'deeppink', 'darkmagenta', 'blueviolet', 'darkviolet', 'darkorchid', 'darkslateblue', 'darkslategray', 'indigo', 'cadetblue',
		'darkcyan', 'darkturquoise', 'turquoise', 'cyan', 'paleturquoise', 'lightcyan', 'mintcream', 'honeydew', 'aqua', 'aquamarine', 'chartreuse', 'greenyellow', 'palegreen',
		'lawngreen', 'lightgreen', 'lime', 'mediumspringgreen', 'mediumturquoise', 'lightseagreen', 'mediumaquamarine', 'mediumseagreen', 'limegreen', 'darkseagreen', 'forestgreen',
		'green', 'darkgreen', 'darkolivegreen', 'olive', 'olivedab', 'darkkhaki', 'khaki', 'gold', 'goldenrod', 'lightyellow', 'lightgoldenrodyellow', 'lemonchiffon', 'yellow',
		'seashell', 'lavenderblush', 'lavender', 'lightcoral', 'indianred', 'darksalmon', 'lightsalmon', 'pink', 'lightpink', 'hotpink', 'magenta', 'plum', 'violet', 'orchid',
		'palevioletred', 'mediumvioletred', 'purple', 'maroon', 'mediumorchid', 'mediumpurple', 'mediumslateblue', 'thistle', 'linen', 'mistyrose', 'palegoldenrod', 'oldlace',
		'papayawhip', 'moccasin', 'navajowhite', 'peachpuff', 'sandybrown', 'peru', 'chocolate', 'orange', 'darkorange', 'tomato', 'orangered', 'red', 'crimson', 'salmon', 'coral',
		'firebrick', 'brown', 'darkred', 'tan', 'rosybrown', 'sienna', 'saddlebrown'
	]

media_lists = (
		"'tmdb_movies%'",
		"'tmdb_tv%'",
		"'tmdb_popular_people%'",
		"'tmdb_images_person%'",
		"'tmdb_popular_people%'",
		"'tmdb_media%'",
		"'trakt_movies%'",
		"'trakt_tv%'",
		"'trakt_trending_user_lists%'",
		"'trakt_popular_user_lists%'",
		"'imdb_movies%'",
		"'imdb_tv%'",
		"'imdb_people%'",
		"'imdb_reviews%'",
		"'imdb_trivia%'",
		"'imdb_images%'",
		"'imdb_videos%'",
		"'imdb_parentsguide%'",
		"'imdb_watchlist%'",
		"'tmdb_people%'",
		"'imdb_keyword%'",
		"'imdb_blunders%'",
		"'fen_FURK_T_FILE%'",
		"'fen_pm_instant_transfer%'",
		"'fen_rd_check_hash%'",
		"'FEN_AD_%'",
		"'FEN_RD_%'",
		"'FEN_FOLDER_%'",
		"'https%'"
	)