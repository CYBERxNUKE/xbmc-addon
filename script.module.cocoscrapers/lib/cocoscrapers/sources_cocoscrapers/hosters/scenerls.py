# -*- coding: utf-8 -*-
# modified by Venom for Fenomscrapers (updated 7-30-2022)
'''
	Fenomscrapers Project
'''

import re
from urllib.parse import quote_plus
from cocoscrapers.modules import cfscrape
from cocoscrapers.modules import client
from cocoscrapers.modules import source_utils


class source:
	priority = 21
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "http://scene-rls.net"
		self.search_link = "/?s=%s"

	def sources(self, data, hostDict):
		sources = []
		if not data: return sources
		append = sources.append
		try:
			scraper = cfscrape.create_scraper()
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
			# log_utils.log('url = %s' % url)
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
			results = scraper.get(url, headers=headers, timeout=5).text
			if not results: return sources
			posts = client.parseDOM(results, "div", attrs={"class": "postContent"})
			if not posts: return sources
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('SCENERLS')
			return sources

		for post in posts:
			try:
				items = re.findall(r'<p style="text-align: center;">(.*?)</h2>', post, re.M | re.S | re.I)
			except: return sources

			for item in items:
				try:
					name = re.search(r'(.*?)<br', item).group(1).replace('.html', '')

					if not source_utils.check_title(title, aliases, name, hdlr, year): continue
					name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
					if source_utils.remove_lang(name_info, check_foreign_audio): continue
					if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

					# check year for reboot/remake show issues if year is available-crap shoot
					# if 'tvshowtitle' in data:
						# if re.search(r'([1-3][0-9]{3})', name):
							# if not any(value in name for value in (year, str(int(year)+1), str(int(year)-1))):
								# continue

					urls = client.parseDOM(item, "h2")
					urls = client.parseDOM(urls, 'a', ret='href')

					for url in urls:
						valid, host = source_utils.is_host_valid(url, hostDict)
						if not valid: continue
						quality, info = source_utils.get_release_quality(name_info, url)
						try:
							size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', item).group(0)
							dsize, isize = source_utils._size(size)
							info.insert(0, isize)
						except: dsize = 0
						info = ' | '.join(info)
						append({'provider': 'scenerls', 'source': host, 'name': name, 'name_info': name_info, 'quality': quality, 'language': 'en', 'url': url,
										'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
				except:
					source_utils.scraper_error('SCENERLS')

		return sources