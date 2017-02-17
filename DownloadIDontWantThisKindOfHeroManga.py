"""
 This script 
"""
from bs4 import BeautifulSoup
import re
import os
import os.path
import string
import requests
import urllib.parse
import datetime

# imageFilesDestinationFolder = cleanStringForFolderName('I_Don_t_Want_This_Kind_of_Hero_-_Manga')
imageFilesDestinationFolder = 'I_Don_t_Want_This_Kind_of_Hero_-_Manga'
pageCountLimit = 1000

firstCommicUrl = 'http://mangafox.me/manga/i_don_t_want_this_kind_of_hero/c142/1.html'

class WebcomicScrapper_IDontWantThisKindOfHero(object):

	def __init__(self):
		self._validCharsForFolderName = "-_.()%s%s" % (string.ascii_letters, string.digits)
		self._startComicUrl = ''
		self._imageFilesDestinationFolder = ''
		self._pageCountLimit = 1

	@property
	def validCharsForFolderName(self):
		"""List of characters accepted for folder name."""
		return self._validCharsForFolderName
	
	@property
	def startComicUrl(self):
		return self._startComicUrl
	@startComicUrl.setter
	def startComicUrl(self,value):
		if not isinstance(value, str):
			raise ValueError("startComicUrl is expected to be a string")
		else:
			self._startComicUrl = value
		return
	
	@property
	def imageFilesDestinationFolder(self):
		return self._imageFilesDestinationFolder
	@imageFilesDestinationFolder.setter
	def imageFilesDestinationFolder(self,value):
		if not isinstance(value, str):
			raise ValueError("imageFilesDestinationFolder is expected to be a string")
		else:
			self._imageFilesDestinationFolder = self.cleanStringForFolderName(value)
		return
	
	@property
	def pageCountLimit(self):
		return self._pageCountLimit
	@pageCountLimit.setter
	def pageCountLimit(self,value):
		if ( not isinstance(value, int) ) or value < -1 or value == 0:
			raise ValueError("pageCountLimit is expected to be a positive int or -1 for no limit")
		else:
			self._pageCountLimit = value
		return
	
	def is_integer(self,s):
		try:
			int(s)
			return True
		except ValueError:
			return False

	def print_FileAndSysout(self,*objects, end='\n'):
		print(*objects)
		if __file__:
			with open(os.path.basename(__file__)+'.log', 'a') as f:
				print(*objects, file=f)
	def logInfo(self,*objects, end='\n'):
		self.print_FileAndSysout(objects, end)
		return
	def logWarn(self,*objects, end='\n'):
		self.print_FileAndSysout(objects, end)
		return
	def logDebug(self,*objects, end='\n'):
		# self.print_FileAndSysout(objects, end)
		return
	
	def cleanStringForFolderName(self,stringToClean):
		if not isinstance(stringToClean, str):
			raise ValueError("stringToClean is expected to be a string")
			return
		temp = ''
		for c in stringToClean:
			if c in self.validCharsForFolderName:
				temp += str(c)
			else :
				temp += '_'
		return temp

	def start(self, shouldPauseAtEnd=True):
		self.logInfo("\nStar scrapping :",str(datetime.datetime.now()),'\n')

		nextUrl = self.startComicUrl
		pageCount = 0
		while ( self.pageCountLimit == -1 or pageCount < self.pageCountLimit) and nextUrl:
			self.logInfo('#'+str(pageCount),'Next Url :',nextUrl)
			r = requests.get(nextUrl)
			if r.status_code == 200 :
				soup = BeautifulSoup(r.text,'html.parser')
				imgSrc = ''
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
						imgSrc = urllib.parse.urljoin(r.url,imgSrc)
					self.logDebug( imgSrc, imgSrcExtension )
				urlParsed = urllib.parse.urlparse(r.url)
				if urlParsed and urlParsed.path:
					self.logDebug(urlParsed,urlParsed.path)
					(pathBeforePage,pageFileName) = os.path.split(urlParsed.path)
					if pageFileName:
						(imageNumber,tmpExtention) = os.path.splitext(pageFileName)
						self.logDebug( 'imageNumber :', imageNumber )
					if pathBeforePage :
						(nothingImportant,chapterNumber) = os.path.split(pathBeforePage)
						self.logDebug( 'chapterNumber :', chapterNumber )
				if not imgSrc:
					self.logWarn('imgSrc is incorrect')
				elif not imageNumber or not self.is_integer(imageNumber) :
					self.logWarn('imageNumber is incorrect')
				elif not chapterNumber:
					self.logWarn('chapterNumber is incorrect')
				elif not imgSrcExtension:
					self.logWarn('imgSrcExtension is incorrect')
				else:
					imageFileName = '%(chapter)s_-_%(number)03d%(ext)s' % {"chapter": chapterNumber, "number": int(imageNumber), 'ext': imgSrcExtension}
					imageFileName = self.cleanStringForFolderName( imageFileName )
					imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
					self.logDebug(imageFileName)
					if os.path.isfile( imageFileName ):
						self.logInfo('\tFile '+imageFileName+' already exists.')
					else:
						imageRequest = requests.get(imgSrc)
						if imageRequest.status_code != 200:
							self.logWarn('\tImage request failed :',r)
						else:
							with open(imageFileName, 'wb') as f:
								f.write(imageRequest.content)
								self.logInfo('\tImage saved as '+imageFileName)
				
				pagesArray = soup.select('form#top_bar div.r.m div select.m option')
				self.logDebug('pagesArray :',pagesArray)
				if pagesArray and len(pagesArray) > 0 :
					pagesArray.sort(key=lambda option: int(option['value']))
					self.logDebug('pagesArray sorted :',pagesArray)
					lastPageForChapterOption = pagesArray[len(pagesArray)-1]
					if lastPageForChapterOption and lastPageForChapterOption['value'] :
						lastPageForCurrentChapter = lastPageForChapterOption['value']
						self.logDebug( 'lastPageForCurrentChapter :',lastPageForCurrentChapter )
				
				nextUrl = ''
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
								nextUrl = urllib.parse.urljoin(r.url,nextUrlA['href'])
				if nextUrl :
					urlParsed = urllib.parse.urlparse(nextUrl)
					if not( urlParsed.scheme and urlParsed.netloc and urlParsed.path ):
						nextUrl = ''
				if nextUrl:
					pageCount += 1

		self.logInfo('Page Count :',pageCount)
		
		if shouldPauseAtEnd:
			os.system("pause")
		
		return pageCount

# Start scrapping webcomic
scrapper = WebcomicScrapper_IDontWantThisKindOfHero()

scrapper.startComicUrl = firstCommicUrl
scrapper.pageCountLimit = pageCountLimit
scrapper.imageFilesDestinationFolder = imageFilesDestinationFolder

scrapper.start(True)





