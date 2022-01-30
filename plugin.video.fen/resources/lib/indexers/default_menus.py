
class DefaultMenus:
	
	def RootList(self):
		return [
			{
				'iconImage': 'movies.png', 
				'mode': 'navigator.main',
				'action': 'MovieList',
				'name': 32028
			}, 
			{
				'iconImage': 'tv.png', 
				'mode': 'navigator.main',
				'action': 'TVShowList',
				'name': 32029
			}, 
			{
				'iconImage': 'search.png', 
				'mode': 'navigator.search', 
				'name': 32450
			}, 
			{
				'iconImage': 'discover.png', 
				'mode': 'navigator.discover_main', 
				'name': 32451
			}, 
			{
				'name': 32452, 
				'iconImage': 'genre_family.png', 
				'mode': 'build_popular_people',
			}, 
			{
				'iconImage': 'favourites.png', 
				'mode': 'navigator.favourites', 
				'name': 32453
			}, 
			{
				'iconImage': 'downloads.png', 
				'mode': 'navigator.downloads', 
				'name': 32107
			}, 
			{
				'iconImage': 'lists.png', 
				'mode': 'navigator.my_content', 
				'name': 32454
			}, 
			{
				'iconImage': 'premium.png', 
				'mode': 'navigator.premium', 
				'name': 32455
			}, 
			{
				'iconImage': 'settings2.png', 
				'mode': 'navigator.tools', 
				'name': 32456
			}, 
			{
				'iconImage': 'settings.png', 
				'mode': 'navigator.settings', 
				'name': 32247
			}
		]

	def MovieList(self):
		return [
			{
				'name': 32458, 
				'iconImage': 'trending.png', 
				'mode': 'build_movie_list', 
				'action': 'trakt_movies_trending'
			}, 
			{
				'name': 32459, 
				'iconImage': 'popular.png', 
				'mode': 'build_movie_list', 
				'action': 'tmdb_movies_popular'
			}, 
			{
				'action': 'tmdb_movies_premieres', 
				'iconImage': 'fresh.png', 
				'mode': 'build_movie_list', 
				'name': 32460
			}, 
			{
				'name': 32461, 
				'iconImage': 'dvd.png', 
				'mode': 'build_movie_list', 
				'action': 'tmdb_movies_latest_releases'
			}, 
			{
				'action': 'trakt_movies_top10_boxoffice', 
				'iconImage': 'box_office.png', 
				'mode': 'build_movie_list', 
				'name': 32462
			}, 
			{
				'name': 32463, 
				'iconImage': 'most_voted.png', 
				'mode': 'build_movie_list', 
				'action': 'tmdb_movies_blockbusters'
			}, 
			{
				'name': 32464, 
				'iconImage': 'intheatres.png', 
				'mode': 'build_movie_list', 
				'action': 'tmdb_movies_in_theaters'
			}, 
			{
				'name': 32465, 
				'iconImage': 'top_rated.png', 
				'mode': 'build_movie_list', 
				'action': 'tmdb_movies_top_rated'
			}, 
			{
				'name': 32466, 
				'iconImage': 'lists.png', 
				'mode': 'build_movie_list', 
				'action': 'tmdb_movies_upcoming'
			}, 
			{
				'name': 32467, 
				'iconImage': 'most_anticipated.png', 
				'mode': 'build_movie_list', 
				'action': 'trakt_movies_anticipated'
			}, 
			{
				'name': 32468, 
				'iconImage': 'oscar-winners.png', 
				'mode': 'build_movie_list', 
				'action': 'imdb_movies_oscar_winners'
			}, 
			{
				'name': 32469, 
				'menu_type': 'movie', 
				'iconImage': 'trakt.png', 
				'mode': 'navigator.trakt_mosts'
			}, 
			{
				'name': 32470, 
				'menu_type': 'movie', 
				'iconImage': 'genres.png', 
				'mode': 'navigator.genres'
			}, 
			{
				'name': 32471, 
				'menu_type': 'movie', 
				'iconImage': 'languages.png', 
				'mode': 'navigator.languages'
			}, 
			{
				'name': 32472, 
				'menu_type': 'movie', 
				'iconImage': 'calender.png', 
				'mode': 'navigator.years'
			}, 
			{
				'name': 32473, 
				'menu_type': 'movie', 
				'iconImage': 'certifications.png', 
				'mode': 'navigator.certifications'
			}, 
			{
				'name': 32474, 
				'iconImage': 'because_you_watched.png', 
				'mode': 'navigator.because_you_watched', 
				'menu_type': 'movie'
			}, 
			{
				'iconImage': 'watched_1.png', 
				'mode': 'build_movie_list',  
				'action': 'watched_movies', 
				'name': 32475
			}, 
			{
				'iconImage': 'player.png', 
				'mode': 'build_movie_list',  
				'action': 'in_progress_movies', 
				'name': 32476
			}, 
			{
				'name': 32477, 
				'iconImage': 'search.png', 
				'mode': 'get_search_term', 
				'db_type': 'movie', 
			}
		]
	
	def TVShowList(self):
		return [
			{
				'action': 'trakt_tv_trending', 
				'iconImage': 'trending.png', 
				'mode': 'build_tvshow_list', 
				'name': 32458
			}, 
			{
				'action': 'tmdb_tv_popular', 
				'iconImage': 'popular.png', 
				'mode': 'build_tvshow_list', 
				'name': 32459
			}, 
			{
				'action': 'tmdb_tv_premieres', 
				'iconImage': 'fresh.png', 
				'mode': 'build_tvshow_list', 
				'name': 32460
			}, 
			{
				'action': 'tmdb_tv_top_rated', 
				'iconImage': 'top_rated.png', 
				'mode': 'build_tvshow_list', 
				'name': 32465
			}, 
			{
				'action': 'tmdb_tv_airing_today', 
				'iconImage': 'live.png', 
				'mode': 'build_tvshow_list', 
				'name': 32478
			}, 
			{
				'action': 'tmdb_tv_on_the_air', 
				'iconImage': 'ontheair.png', 
				'mode': 'build_tvshow_list', 
				'name': 32479
			}, 
			{
				'name': 32466, 
				'iconImage': 'lists.png', 
				'mode': 'build_tvshow_list', 
				'action': 'tmdb_tv_upcoming'
			}, 
			{
				'action': 'trakt_tv_anticipated', 
				'iconImage': 'most_anticipated.png', 
				'mode': 'build_tvshow_list', 
				'name': 32467
			}, 
			{
				'menu_type': 'tvshow', 
				'iconImage': 'trakt.png', 
				'mode': 'navigator.trakt_mosts', 
				'name': 32469
			}, 
			{
				'menu_type': 'tvshow', 
				'iconImage': 'genres.png', 
				'mode': 'navigator.genres', 
				'name': 32470
			}, 
			{
				'menu_type': 'tvshow', 
				'iconImage': 'networks.png', 
				'mode': 'navigator.networks', 
				'name': 32480
			}, 
			{
				'menu_type': 'tvshow', 
				'iconImage': 'languages.png', 
				'mode': 'navigator.languages', 
				'name': 32471
			}, 
			{
				'name': 32472, 
				'menu_type': 'tvshow', 
				'iconImage': 'calender.png', 
				'mode': 'navigator.years'
			}, 
			{
				'menu_type': 'tvshow', 
				'iconImage': 'certifications.png', 
				'mode': 'navigator.certifications', 
				'name': 32473
			}, 
			{
				'name': 32474, 
				'iconImage': 'because_you_watched.png', 
				'mode': 'navigator.because_you_watched', 
				'menu_type': 'tvshow'
			}, 
			{
				'iconImage': 'watched_1.png', 
				'mode': 'build_tvshow_list',  
				'action': 'watched_tvshows', 
				'name': 32475
			}, 
			{
				'action': 'in_progress_tvshows', 
				'iconImage': 'in_progress_tvshow.png', 
				'mode': 'build_tvshow_list', 
				'name': 32481
			}, 
			{
				'iconImage': 'player.png', 
				'mode': 'build_in_progress_episode', 
				'name': 32482
			}, 
			{
				'iconImage': 'next_episodes.png', 
				'mode': 'build_next_episode', 
				'name': 32483
			}, 
			{
				'name': 32477, 
				'iconImage': 'search.png', 
				'mode': 'get_search_term', 
				'db_type': 'tv_show', 
			}
		]

	def DefaultMenuItems(self):
		return ['RootList', 'MovieList', 'TVShowList']






