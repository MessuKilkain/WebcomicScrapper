"""
 WebcomicScrapper for website www.webtoons.com
"""
import os.path
import urllib.parse
import re

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_WebToons(WebcomicScrapper):

	# return (nextUrl,imageFileNameArray,imgSrcArray)
	def getValuesFromPage(self,soup,request):
		imgSrcArray = list()
		imageFileNameArray = list()
		nextUrl = ''
		
		imgSrcExtension = ''
		chapterNumber = ''
		imageNumber = ''
		lastPageForCurrentChapter = ''
		
		chapterNumber = soup.select_one('#toolbar .paginate.v2 > span._btnOpenEpisodeList').string.replace('#','')
		self.logDebug('chapterNumber :',chapterNumber)
		
		urlParsed = urllib.parse.urlparse(request.url)
		urlScheme = None
		self.logDebug( u'urlParsed', urlParsed )
		
		imgArray = soup.select('#_imageList img._images')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			imageNumberIndex = 0
			for img in imgArray:
				imageNumberIndex = imageNumberIndex + 1
				imageNumber = str(imageNumberIndex)
				# imgSrc = img['src']
				imgSrc = img['data-url']
				imageFileName = ''
				if imgSrc:
					imgSrcPath = urllib.parse.urlparse(imgSrc).path
					(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrcPath)
					if imgSrcExtension:
						underscoreIndex = imgSrcExtension.find('_')
						if underscoreIndex != -1:
							imgSrcExtension = imgSrcExtension[:underscoreIndex]
				self.logDebug( imgSrc, imgSrcExtension )
				if urlParsed:
					if imgSrc:
						imgSrcParsed = urllib.parse.urlparse(imgSrc)
						if imgSrcParsed:
							self.logDebug( u'imgSrcParsed', imgSrcParsed )
							if not imgSrcParsed.scheme:
								imgSrcParsed.scheme = urlParsed.scheme
							if not imgSrcParsed.netloc:
								imgSrcParsed.netloc = urlParsed.netloc
							imgSrc = urllib.parse.urlunparse(imgSrcParsed)
							self.logDebug( u'New imgSrc', imgSrc )
					if urlParsed.scheme:
						urlScheme = urlParsed.scheme
				if not imageNumber or not self.is_integer(imageNumber) :
					self.logWarn('imageNumber is incorrect')
				elif not chapterNumber:
					self.logWarn('chapterNumber is incorrect')
				elif not imgSrcExtension:
					self.logWarn('imgSrcExtension is incorrect')
				else:
					imageFileName = 'c%(chapter)03d_-_%(number)03d%(ext)s' % {"chapter": int(chapterNumber), "number": int(imageNumber), 'ext': imgSrcExtension}
					imageFileName = self.cleanStringForFolderName( imageFileName )
					imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
					self.logDebug( 'imageFileName :', imageFileName)
				if imgSrc and imageFileName:
					imgSrcArray.append(imgSrc)
					imageFileNameArray.append(imageFileName)
		
		self.logDebug('imageFileNameArray :',imageFileNameArray)
		self.logDebug('imgSrcArray :',imgSrcArray)
		
		# Get NextUrl
		self.logDebug( 'imageNumber :',imageNumber )
		nextUrlLinkElement = soup.select_one('#toolbar .paginate.v2 > a.pg_next')
		if nextUrlLinkElement and len(nextUrlLinkElement) > 0:
			nextUrl = nextUrlLinkElement['href']
		
		if nextUrl and urlScheme:
			urlParsed = urllib.parse.urlparse(nextUrl)
			if urlParsed:
				if not urlParsed.scheme:
					nextUrl = urlScheme + u':' + nextUrl
				self.logDebug( 'nextUrl with scheme :', nextUrl )
		return (nextUrl,imageFileNameArray,imgSrcArray)
	





