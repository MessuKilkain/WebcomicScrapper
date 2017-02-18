"""
 WebcomicScrapper for Webcomic Sinfest
"""
import os.path
import urllib.parse

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_Sinfest(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.sinfest.net/view.php?date=2000-01-17', imageFilesDestinationFolder='Sinfest', pageCountLimit=60 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgAlt = ''
		imgDate = ''
		imgArray = soup.select('table table img')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
			imgAlt = img['alt']
			self.logDebug( imgSrc, imgSrcExtension ,imgAlt )
		urlParsed = urllib.parse.urlparse(request.url)
		if urlParsed and urlParsed.query:
			self.logDebug(urlParsed,urlParsed.query)
			queryData = urllib.parse.parse_qs(urlParsed.query)
			if queryData:
				self.logDebug(queryData)
				self.logDebug(queryData['date'])
				imgDateList = queryData['date']
				if imgDateList and len(imgDateList) > 0:
					imgDate = imgDateList[0]
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
		nextUrl = ''
		if imgDate:
			nextUrlArray = soup.select('a img[src$="images/next.gif"]')
			self.logDebug('nextUrlArray :',nextUrlArray)
			if nextUrlArray and len(nextUrlArray) > 0 :
				nextUrlA = nextUrlArray[0].parent
				if nextUrlA and nextUrlA['href']:
					nextUrl = urllib.parse.urljoin(request.url,nextUrlA['href'])
		return (nextUrl,imageFileName,imgSrc)


# Start scrapping webcomic
scrapper = WebcomicScrapper_Sinfest()

scrapper.startComicUrl = 'http://www.sinfest.net/view.php?date=2017-02-01'
scrapper.pageCountLimit = 1000
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)





