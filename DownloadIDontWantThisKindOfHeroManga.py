"""
 WebcomicScrapper for Manwa I don't want this kind of Hero
"""
import os.path
import urllib.parse
import re

from WebcomicScrapper_WebToons import WebcomicScrapper_WebToons

class WebcomicScrapper_IDontWantThisKindOfHero(WebcomicScrapper_WebToons):

	def __init__(self):
		WebcomicScrapper_WebToons.__init__(self, startComicUrl='https://www.webtoons.com/en/fantasy/i-dont-want-this-kind-of-hero/ep-140-i-still-havent-done-anything-wrong-today/viewer?title_no=98&episode_no=1', imageFilesDestinationFolder='I_Don_t_Want_This_Kind_of_Hero_-_Manga', pageCountLimit=50 )

if __name__ == '__main__':
	# Start scrapping webcomic
	scrapper = WebcomicScrapper_IDontWantThisKindOfHero()

	# scrapper.startComicUrl = 'http://mangafox.me/manga/i_don_t_want_this_kind_of_hero/c142/22.html'
	# scrapper.startComicUrl = 'http://www.mangatown.com/manga/i_don_t_want_this_kind_of_hero/c200/31.html'
	# scrapper.startComicUrl = 'https://www.webtoons.com/en/fantasy/i-dont-want-this-kind-of-hero/list?title_no=98'
	# scrapper.startComicUrl = 'https://www.webtoons.com/en/fantasy/i-dont-want-this-kind-of-hero/ep-140-i-still-havent-done-anything-wrong-today/viewer?title_no=98&episode_no=1'
	scrapper.pageCountLimit = 1000
	# scrapper.pageCountLimit = 1
	scrapper.logFileName = os.path.basename(__file__)+'.log'
	# scrapper.interRequestWaitingTime = 2

	scrapper.start(True)





