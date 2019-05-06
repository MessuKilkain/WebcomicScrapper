"""
 WebcomicScrapper for _Seed
"""
import os.path
import urllib.parse
import re

from WebcomicScrapper_WebToons import WebcomicScrapper_WebToons

class WebcomicScrapper_Seed(WebcomicScrapper_WebToons):

	def __init__(self):
		WebcomicScrapper_WebToons.__init__(self, startComicUrl='https://www.webtoons.com/en/sf/seed/prologue/viewer?title_no=1480&episode_no=1', imageFilesDestinationFolder='Seed_-_Manga', pageCountLimit=1000 )

if __name__ == '__main__':
	# Start scrapping webcomic
	scrapper = WebcomicScrapper_Seed()
	scrapper.pageCountLimit = 1000
	# scrapper.pageCountLimit = 1
	scrapper.logFileName = os.path.basename(__file__)+'.log'
	# scrapper.interRequestWaitingTime = 2

	scrapper.start(True)





