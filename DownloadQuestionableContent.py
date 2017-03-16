"""
 WebcomicScrapper for Webcomic Questionnable Content
"""
import os.path
import urllib.parse

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_QuestionableContent(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.questionablecontent.net/view.php?comic=1', imageFilesDestinationFolder='QuestionableContent', pageCountLimit=60 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		comicNumber = ''
		img = soup.find('img',id='strip')
		if img :
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
		self.logDebug( imgSrc, imgSrcExtension )
		urlParsed = urllib.parse.urlparse(request.url)
		if urlParsed and urlParsed.query:
			self.logDebug(urlParsed,urlParsed.query)
			queryData = urllib.parse.parse_qs(urlParsed.query)
			if queryData:
				self.logDebug(queryData)
				self.logDebug(queryData['comic'])
				comicNumberList = queryData['comic']
				if comicNumberList and len(comicNumberList) > 0 and self.is_integer(comicNumberList[0]):
					comicNumber = comicNumberList[0]
		if not imgSrcExtension:
			self.logWarn('imgSrcExtension is incorrect')
		elif not comicNumber:
			self.logWarn('comicNumber is incorrect')
		else:
			imageFileName = '%(comicNumber)04d%(ext)s' % {"comicNumber": int(comicNumber), 'ext': imgSrcExtension}
			imageFileName = self.cleanStringForFolderName(imageFileName)
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug(imageFileName)
		if img and img.parent and img.parent['href'] and img.parent['href'] != '#':
			nextUrl = urllib.parse.urljoin(request.url,img.parent['href'])
		return (nextUrl,imageFileName,imgSrc)

# Start scrapping webcomic
scrapper = WebcomicScrapper_QuestionableContent()

# scrapper.startComicUrl = 'http://www.questionablecontent.net/view.php?comic=3420'
scrapper.pageCountLimit = 10000
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)




