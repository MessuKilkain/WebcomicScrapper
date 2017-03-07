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
				imgSrcPath = imgSrc = urllib.parse.urlparse(imgSrc).path
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrcPath)
				if imgSrcExtension:
					underscoreIndex = imgSrcExtension.find('_')
					if underscoreIndex != -1:
						imgSrcExtension = imgSrcExtension[:underscoreIndex]
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
			self.logDebug( imgSrc, imgSrcExtension )
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
		
		pagesArray = soup.select('form#top_bar div.r.m div select.m option')
		self.logDebug('pagesArray :',pagesArray)
		if pagesArray and len(pagesArray) > 0 :
			pagesArray.sort(key=lambda option: int(option['value']))
			self.logDebug('pagesArray sorted :',pagesArray)
			lastPageForChapterOption = pagesArray[len(pagesArray)-1]
			if lastPageForChapterOption and lastPageForChapterOption['value'] :
				lastPageForCurrentChapter = lastPageForChapterOption['value']
				self.logDebug( 'lastPageForCurrentChapter :',lastPageForCurrentChapter )
		# Get NextUrl
		if imageNumber and self.is_integer(imageNumber) and lastPageForCurrentChapter and self.is_integer(lastPageForCurrentChapter) :
			if lastPageForCurrentChapter == imageNumber :
				chapterNavigationDiv = soup.find('div',id='chnav')
				if chapterNavigationDiv:
					nextChapterSpanLabel = chapterNavigationDiv.find('span',string=re.compile('^Next.*'))
					if nextChapterSpanLabel and nextChapterSpanLabel.parent and nextChapterSpanLabel.parent.a and nextChapterSpanLabel.parent.a['href'] :
						nextUrl = nextChapterSpanLabel.parent.a['href']
			else:
				nextUrlArray = soup.select('#top_center_bar a.btn.next_page')
				self.logDebug('nextUrlArray :',nextUrlArray)
				if nextUrlArray and len(nextUrlArray) > 0 :
					nextUrlA = nextUrlArray[0]
					if nextUrlA and nextUrlA['href']:
						nextUrl = urllib.parse.urljoin(request.url,nextUrlA['href'])
		return (nextUrl,imageFileName,imgSrc)

# Start scrapping webcomic
scrapper = WebcomicScrapper_IDontWantThisKindOfHero()

scrapper.startComicUrl = 'http://mangafox.me/manga/i_don_t_want_this_kind_of_hero/c142/1.html'
scrapper.pageCountLimit = 1000
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)





