"""
 WebcomicScrapper for Webcomic Menage a 3
 http://www.ma3comic.com/strips-ma3/
"""
import os.path
import urllib.parse
from datetime import datetime

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_MenageA3(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.ma3comic.com/strips-ma3/for_new_readers', imageFilesDestinationFolder='MenageA3', pageCountLimit=60 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgTitle = ''
		imgDate = ''
		imgArray = soup.select('#cc img')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
			self.logDebug( imgSrc, imgSrcExtension )
		
		# Get the title of the comic
		if not imgTitle:
			currentOption = soup.select_one('select#navjump option[value=""]')
			if currentOption:
				imgTitle = currentOption.get_text()
		
		# Get the date of the comic
		if not imgDate:
			fallbackDate = soup.select_one('#cndate')
			if fallbackDate and fallbackDate.get_text():
				self.logDebug("fallbackDate : ",str(fallbackDate))
				self.logDebug("fallbackDate.get_text() : ",str(fallbackDate.get_text()))
				imgDate = datetime.strptime( fallbackDate.get_text(), '%B %d, %Y' ).strftime('%Y-%m-%d')
		
		if not imgSrcExtension:
			self.logWarn('imgSrcExtension is incorrect')
		elif not imgTitle:
			self.logWarn('imgTitle is incorrect')
		elif not imgDate:
			self.logWarn('imgDate is incorrect')
		else:
			imageFileName = imgDate + '_-' + imgTitle + imgSrcExtension
			imageFileName = self.cleanStringForFolderName(imageFileName)
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug(imageFileName)
		
		aNavNext = soup.select_one('#cnav #cndnext')
		if aNavNext and aNavNext['href'] and aNavNext['href'] != '#':
			nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		return (nextUrl,imageFileName,imgSrc)
		
	def logDebug(self,*objects, end='\n'):
		# self.print_FileAndSysout(*objects, end)
		return


# Start scrapping webcomic
scrapper = WebcomicScrapper_MenageA3()

# scrapper.startComicUrl = 'http://www.ma3comic.com/strips-ma3/this_is_getting_unhealthy'
# scrapper.startComicUrl = 'http://www.ma3comic.com/strips-ma3/there_is_nothing_strange'
scrapper.pageCountLimit = 2000
scrapper.interRequestWaitingTime = 0;
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)





