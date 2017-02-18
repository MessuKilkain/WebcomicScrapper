"""
 WebcomicScrapper for Webcomic GamerCat
 http://www.thegamercat.com/comic/06102011/
"""
import os.path
import urllib.parse
from datetime import datetime

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_GamerCat(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.thegamercat.com/comic/06102011/', imageFilesDestinationFolder='GamerCat', pageCountLimit=60 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgTitle = ''
		imgDate = ''
		imgArray = soup.select('#comic img')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			try:
				imgTitle = img['title']
			except ValueError:
				self.logDebug( "No title for img" )
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
			self.logDebug( imgSrc, imgSrcExtension )
		
		# Get the title of the comic
		if not imgTitle:
			postTitle = soup.select_one('#content .post-content .post-title')
			if postTitle:
				imgTitle = postTitle.get_text()
		
		# Get the date of the comic
		if not imgDate:
			fallbackDate = soup.select_one('#content .post-content .post-text .post-date')
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
			imageFileName = imgDate + '_-_' + imgTitle + imgSrcExtension
			imageFileName = self.cleanStringForFolderName(imageFileName)
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug(imageFileName)
		
		aNavNext = soup.select_one('.comic-nav-container .comic-nav .comic-nav-base.comic-nav-next')
		if aNavNext and aNavNext['href'] and aNavNext['href'] != '#':
			nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		return (nextUrl,imageFileName,imgSrc)
		
	def logDebug(self,*objects, end='\n'):
		# self.print_FileAndSysout(*objects, end)
		return


# Start scrapping webcomic
scrapper = WebcomicScrapper_GamerCat()

# scrapper.startComicUrl = 'http://www.thegamercat.com/comic/generous-love/'
scrapper.pageCountLimit = 1000
# scrapper.interRequestWaitingTime = 0;
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)





