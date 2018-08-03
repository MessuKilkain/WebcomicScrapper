"""
 WebcomicScrapper for Manwa I don't want this kind of Hero
"""
import os.path
import urllib.parse
import re

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_IDontWantThisKindOfHero(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://mangafox.me/manga/i_don_t_want_this_kind_of_hero/c000/1.html', imageFilesDestinationFolder='I_Don_t_Want_This_Kind_of_Hero_-_Manga', pageCountLimit=50 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		chapterNumber = ''
		imageNumber = ''
		lastPageForCurrentChapter = ''
		imgArray = soup.select('#viewer img#image')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				imgSrcPath = urllib.parse.urlparse(imgSrc).path
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrcPath)
				if imgSrcExtension:
					underscoreIndex = imgSrcExtension.find('_')
					if underscoreIndex != -1:
						imgSrcExtension = imgSrcExtension[:underscoreIndex]
			self.logDebug( imgSrc, imgSrcExtension )
		urlParsed = urllib.parse.urlparse(request.url)
		urlScheme = None
		self.logDebug( u'urlParsed', urlParsed )
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
			if urlParsed.path:
				self.logDebug(urlParsed,urlParsed.path)
				(pathBeforePage,pageFileName) = os.path.split(urlParsed.path)
				if pageFileName:
					(imageNumber,tmpExtention) = os.path.splitext(pageFileName)
					self.logDebug( 'imageNumber :', imageNumber )
				elif pageFileName == '':
					imageNumber = '1'
					self.logDebug( 'imageNumber :', imageNumber )
				if pathBeforePage :
					(nothingImportant,chapterNumber) = os.path.split(pathBeforePage)
					self.logDebug( 'chapterNumber :', chapterNumber )
		if not imageNumber or not self.is_integer(imageNumber) :
			self.logWarn('imageNumber is incorrect')
		elif not chapterNumber:
			self.logWarn('chapterNumber is incorrect')
		elif not imgSrcExtension:
			self.logWarn('imgSrcExtension is incorrect')
		else:
			imageFileName = '%(chapter)s_-_%(number)03d%(ext)s' % {"chapter": chapterNumber, "number": int(imageNumber), 'ext': imgSrcExtension}
			imageFileName = self.cleanStringForFolderName( imageFileName )
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug( 'imageFileName :', imageFileName)
		
		pagesArray = soup.select('div.page_select select option')
		# self.logDebug('pagesArray :',pagesArray)
		if pagesArray and len(pagesArray) > 0 :
			pagesArray = [x for x in pagesArray if self.is_integer(x.string)]
			pagesArray.sort(key=lambda option: option.string)
			# self.logDebug('pagesArray sorted :',pagesArray)
			lastPageForChapterOption = pagesArray[len(pagesArray)-1]
			if lastPageForChapterOption and lastPageForChapterOption.string :
				lastPageForCurrentChapter = lastPageForChapterOption.string
				self.logDebug( 'lastPageForCurrentChapter :',lastPageForCurrentChapter )
		# Get NextUrl
		self.logDebug( 'imageNumber :',imageNumber )
		if imageNumber and self.is_integer(imageNumber) and lastPageForCurrentChapter and self.is_integer(lastPageForCurrentChapter) :
			if int(lastPageForCurrentChapter) == int(imageNumber) :
				nextUrlArray = soup.select('div.page_select select option')
				nextUrlArray = [x for x in nextUrlArray if x.string == '01']
				self.logDebug('nextUrlArray :',nextUrlArray)
				if nextUrlArray and len(nextUrlArray) > 0 :
					nextUrlA = nextUrlArray[0]
					if nextUrlA and nextUrlA['value']:
						nextUrl = urllib.parse.urljoin(request.url,nextUrlA['value'].replace(chapterNumber,u'c'+str(1+int(chapterNumber[1:]))))
						nextUrl = urllib.parse.urljoin(nextUrl,u'1.html')
			else:
				nextUrlArray = soup.select('div.page_select select option')
				nextUrlArray = [x for x in nextUrlArray if self.is_integer(x.string) and int(x.string) == 1+int(imageNumber)]
				self.logDebug('nextUrlArray :',nextUrlArray)
				if nextUrlArray and len(nextUrlArray) > 0 :
					nextUrlA = nextUrlArray[0]
					if nextUrlA and nextUrlA['value']:
						nextUrl = urllib.parse.urljoin(request.url,nextUrlA['value'])
		
		if nextUrl and urlScheme:
			urlParsed = urllib.parse.urlparse(nextUrl)
			if urlParsed:
				if not urlParsed.scheme:
					nextUrl = urlScheme + u':' + nextUrl
				self.logDebug( 'nextUrl with scheme :', nextUrl )
		return (nextUrl,imageFileName,imgSrc)

if __name__ == '__main__':
	# Start scrapping webcomic
	scrapper = WebcomicScrapper_IDontWantThisKindOfHero()

	# scrapper.startComicUrl = 'http://mangafox.me/manga/i_don_t_want_this_kind_of_hero/c142/22.html'
	# scrapper.startComicUrl = 'http://www.mangatown.com/manga/i_don_t_want_this_kind_of_hero/c200/31.html'
	scrapper.pageCountLimit = 1000
	scrapper.logFileName = os.path.basename(__file__)+'.log'

	scrapper.start(True)





