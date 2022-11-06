# -*- coding: utf-8 -*-
# modified by Venom for Fenomscrapers (updated 05-30-2022)
'''
	Fenomscrapers Project
'''

import re
from urllib.parse import quote_plus
from cocoscrapers.modules import client
from cocoscrapers.modules import source_utils


class source:
	priority = 22
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "http://get.myvideolinks.net"
		# self.search_link = "/search.php?keywords=%s"
		self.search_link = "/search.php?keywords=%s&terms=all&sk=t&sf=titleonly&sr=topics&submit=Search"

	def sources(self, data, hostDict):
		sources = []
		if not data: return sources
		sources_append = sources.append
		try:
			aliases = data['aliases']
			year = data['year']
			if 'tvshowtitle' in data:
				title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')
				episode_title = data['title']
				hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
			else:
				title = data['title'].replace('&', 'and').replace('/', ' ')
				episode_title = None
				hdlr = year
			query = '%s %s' % (re.sub(r'[^A-Za-z0-9\s\.-]+', '', title), hdlr)
			url = '%s%s' % (self.base_link, self.search_link % quote_plus(query))
			# log_utils.log('url = %s' % url, __name__)
			r = client.request(url, timeout=5)
			if not r or 'Error 404' in r: return sources
			r = client.parseDOM(r, 'ul', attrs={'class': 'topiclist topics'})
			r1= client.parseDOM(r, 'li')
			posts = zip(client.parseDOM(r1, 'a', attrs={'class': 'topictitle'}, ret='href'), client.parseDOM(r1, 'a'))
		except:
			source_utils.scraper_error('MYVIDEOLINK')
			return sources
		links = []
		for post in posts:
			try:
				name = source_utils.strip_non_ascii_and_unprintable(post[1])
				if '<' in name: name = re.sub(r'<.*?>', '', name)
				name = client.replaceHTMLCodes(name)
				name = source_utils.clean_name(name)

				if 'tvshowtitle' in data:
					if not source_utils.check_title(title, aliases, name, hdlr, year):
						if not source_utils.check_title(title, aliases, name, 'S%02d' % int(data['season']), year):
							if not source_utils.check_title(title, aliases, name, 'Season.%d' % int(data['season']), year):
								if not source_utils.check_title(title, aliases, name, 'S%d' % int(data['season']), year): continue
				else:
					if not source_utils.check_title(title, aliases, name, hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)

				link = post[0]
				link = '%s%s' % (self.base_link, link.lstrip('.'))
				results = client.request(link, timeout=5)
				results = client.parseDOM(results, 'div', attrs={'class': 'content'})[0]

				if 'tvshowtitle' in data:
					isSeasonList = False
					if 'Season' in name or 'S%02d' % int(data['season']) in name:
						isSeasonList = True
					results = re.sub(r'[\n\t]', '', results).replace('> <', '><')
					test = re.findall(r'<p><b>(.*?)</ul>', results, re.DOTALL) # parsing this site for episodes is a bitch, fuck it this is close as I'm doing
					for x in test:
						test2 = re.search(r'(.*?)</b>', x).group(1)
						if hdlr in test2:
							if isSeasonList:
								name = re.sub(r'\.Season\.\d+', '.%s.' % test2.replace(' ', '.'), name)
								name = re.sub(r'\.S\d+', '.%s' % test2.replace(' ', '.'), name)
							else: name = test2
							links = client.parseDOM(x, 'a', ret='href')
							break
						else:
							try: test3 = re.search(r'<p><b>(.*?)</b></p>', x).group(1)
							except: continue
							if hdlr in test3:
								if isSeasonList:
									name = re.sub(r'\.Season\.\d+', '.%s.' % test3.replace(' ', '.'), name)
									name = re.sub(r'\.S\d+', '.%s' % test3.replace(' ', '.'), name)
								else: name = test3
								links = client.parseDOM(x, 'a', ret='href')
								break
				else:
					links = client.parseDOM(results, 'a', attrs={'class': 'postlink'}, ret='href')

				for link in links:
					try:
						url = client.replaceHTMLCodes(str(link))
						if url in str(sources): continue

						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid: continue

						quality, info = source_utils.get_release_quality(name_info, url)
						try:
							size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', results).group(0)
							dsize, isize = source_utils._size(size)
							info.insert(0, isize)
						except: dsize = 0
						info = ' | '.join(info)

						sources_append({'provider': 'myvideolink', 'source': host, 'name': name, 'name_info': name_info, 'quality': quality,
													'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
					except:
						source_utils.scraper_error('MYVIDEOLINK')
			except:
				source_utils.scraper_error('MYVIDEOLINK')
		return sources