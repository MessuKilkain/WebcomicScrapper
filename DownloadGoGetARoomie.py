"""
 WebcomicScrapper for Webcomic Go Get a Roomie!
"""
import os.path
import urllib.parse
from datetime import datetime

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_GoGetARoomie(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.gogetaroomie.com/comic/and-so-it-begins', imageFilesDestinationFolder='Go_Get_a_Roomie', pageCountLimit=50 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgAlt = ''
		imgDate = ''
		imgArray = soup.select('img#cc-comic')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
				# Get the date of the comic
				tmpImgSrcRoot = os.path.basename(tmpImgSrcRoot)
				imgNameParts = tmpImgSrcRoot.split('-')
				if imgNameParts and len(imgNameParts) > 3 and self.is_integer(imgNameParts[1]) and self.is_integer(imgNameParts[2]) and self.is_integer(imgNameParts[3]):
					imgDate = imgNameParts[1]+'-'+imgNameParts[2]+'-'+imgNameParts[3]
			# TODO : improve by adding try around get attribute with KeyError handling
			imgAlt = img['title']
			self.logDebug( imgSrc, imgSrcExtension ,imgAlt )
		
		#imgDate fallback
		if not imgDate:
			fallbackDate = soup.select_one('.cc-publishtime')
			self.logDebug("fallbackDate : ",str(fallbackDate))
			self.logDebug("fallbackDate.get_text() : ",str(fallbackDate.get_text()))
			if fallbackDate and fallbackDate.get_text():
				fallbackDateParts = fallbackDate.get_text().split()
				self.logDebug("fallbackDateParts : ",str(fallbackDateParts))
				if fallbackDateParts and len(fallbackDateParts) > 1:
					if not imgDate:
						try:
							# imgDate = '-'.join( fallbackDateParts[1].split('.') )
							imgDate = datetime.strptime( fallbackDateParts[1], '%b.%d.%y' ).strftime('%Y-%m-%d')
						except Exception as e:
							self.logDebug("e : ",str(e))
							imgDate = None
					if not imgDate:
						try:
							imgDate = datetime.strptime( fallbackDate.get_text(), 'Posted %B %d, %Y at %I:%M %p' ).strftime('%Y-%m-%d')
						except Exception as e:
							self.logDebug("e : ",str(e))
							imgDate = None
		
		if not imgSrcExtension:
			self.logWarn('imgSrcExtension is incorrect')
		elif not imgAlt:
			self.logWarn('imgAlt is incorrect')
		elif not imgDate:
			self.logWarn('imgDate is incorrect')
		else:
			imageFileName = imgDate + '_-_' + imgAlt + imgSrcExtension
			imageFileName = self.cleanStringForFolderName(imageFileName)
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug(imageFileName)
		
		if not nextUrl:
			navNextArray = soup.select('#comicwrap .nav a.next')
			self.logDebug('navNextArray :',navNextArray)
			if navNextArray and len(navNextArray) > 0 :
				aNavNext = navNextArray[0]
				if aNavNext['href'] and aNavNext['href'] != '#':
					nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		if not nextUrl:
			navNextArray = soup.select('#comicwrap .cc-nav a.cc-next')
			self.logDebug('navNextArray :',navNextArray)
			if navNextArray and len(navNextArray) > 0 :
				aNavNext = navNextArray[0]
				if aNavNext['href'] and aNavNext['href'] != '#':
					nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		return (nextUrl,imageFileName,imgSrc)
		

if __name__ == '__main__':
	# Start scrapping webcomic
	scrapper = WebcomicScrapper_GoGetARoomie()

	# scrapper.startComicUrl = 'http://www.gogetaroomie.com/comic/enough-kids-to-go-around'
	scrapper.pageCountLimit = 1000
	# scrapper.interRequestWaitingTime = 0;
	scrapper.logFileName = os.path.basename(__file__)+'.log'

	scrapper.start(True)





