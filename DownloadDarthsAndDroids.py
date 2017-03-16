"""
 WebcomicScrapper for Webcomic Darths & Droids
 http://www.darthsanddroids.net/
"""
import os.path
import urllib.parse
import re
from datetime import datetime

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_DarthsAndDroids(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.darthsanddroids.net/episodes/0001.html', imageFilesDestinationFolder='DarthsAndDroids', pageCountLimit=60 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgTitle = ''
		imageNumber = ''
		divCenter = soup.select_one('body > div.center');
		if divCenter:
			imgArray = divCenter.select('> p:nth-of-type(2) img')
			self.logDebug('imgArray :',imgArray)
			if imgArray and len(imgArray) > 0 :
				img = imgArray[0]
				# try:
					# imgTitle = img['title']
				# except KeyError:
					# self.logDebug( "No title for img" )
				imgSrc = img['src']
				if imgSrc:
					(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
					imgSrc = urllib.parse.urljoin(request.url,imgSrc)
				self.logDebug( imgSrc, imgSrcExtension )
		
		# Get the title of the comic
		if not imgTitle:
			if divCenter:
				postTitle = divCenter.select_one('> p:nth-of-type(1) b')
				if postTitle:
					imgTitle = postTitle.get_text()
		
		# Get the number of the comic
		urlParsed = urllib.parse.urlparse(request.url)
		if urlParsed and urlParsed.path:
			self.logDebug(urlParsed,urlParsed.path)
			(pathBeforePage,pageFileName) = os.path.split(urlParsed.path)
			if pageFileName:
				(imageNumber,tmpExtention) = os.path.splitext(pageFileName)
				self.logDebug( 'imageNumber :', imageNumber )
			if pathBeforePage :
				(nothingImportant,chapterNumber) = os.path.split(pathBeforePage)
				self.logDebug( 'chapterNumber :', chapterNumber )
		
		if not imgSrcExtension:
			self.logWarn('imgSrcExtension is incorrect')
		elif not imgTitle:
			self.logWarn('imgTitle is incorrect')
		elif not imageNumber or not self.is_integer(imageNumber):
			self.logWarn('imageNumber is incorrect')
		else:
			imageFileName = ('%(number)04d' % {"number": int(imageNumber)}) + '_-_' + imgTitle + imgSrcExtension
			imageFileName = self.cleanStringForFolderName(imageFileName)
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug(imageFileName)
		
		if divCenter:
			aNavNext = divCenter.find('a',string=re.compile('NEXT'))
			if aNavNext:
				try:
					nextRelaviteUrl = aNavNext['href']
					if nextRelaviteUrl and nextRelaviteUrl != '#':
						nextUrl = urllib.parse.urljoin(request.url,nextRelaviteUrl)
				except KeyError:
					self.logDebug( "No nextRelaviteUrl for aNavNext" )
		return (nextUrl,imageFileName,imgSrc)
		
	def logDebug(self,*objects, end='\n'):
		# self.print_FileAndSysout(*objects, end)
		return


# Start scrapping webcomic
scrapper = WebcomicScrapper_DarthsAndDroids()

# scrapper.startComicUrl = 'http://www.darthsanddroids.net/episodes/1472.html'
scrapper.pageCountLimit = 2000
# scrapper.interRequestWaitingTime = 0;
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)





