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
	
	@property
	def validCharsForFolderName(self):
		"""List of characters accepted for folder name."""
		if !self._validCharsForFolderName
			self._validCharsForFolderName = "-_.()%s%s" % (string.ascii_letters, string.digits)
		return self._validCharsForFolderName
	
	@property
	def startComicUrl(self):
		return self._startComicUrl
	@startComicUrl.setter
	def startComicUrl(self,value):
		if !isinstance(value, str)
			raise ValueError("startComicUrl is expected to be a string")
		else
			self._startComicUrl = value
		return
	
	@property
	def imageFilesDestinationFolder(self):
		return self._imageFilesDestinationFolder
	@imageFilesDestinationFolder.setter
	def imageFilesDestinationFolder(self,value):
		if !isinstance(value, str)
			raise ValueError("imageFilesDestinationFolder is expected to be a string")
		else
			self._imageFilesDestinationFolder = self.cleanStringForFolderName(value)
		return
	
	@property
	def pageCountLimit(self):
		return self._pageCountLimit
	@pageCountLimit.setter
	def pageCountLimit(self,value):
		if !isinstance(value, int) or value < -1 or value == 0:
			raise ValueError("pageCountLimit is expected to be a positive int or -1 for no limit")
		else
			self._pageCountLimit = value
		return
	
	def is_integer(s):
		try:
			int(s)
			return True
		except ValueError:
			return False

	def print_FileAndSysout(*objects, end='\n'):
		print(*objects)
		if __file__:
			with open(os.path.basename(__file__)+'.log', 'a') as f:
				print(*objects, file=f)
	
	def cleanStringForFolderName(stringToClean):
		if !isinstance(stringToClean, str)
			raise ValueError("stringToClean is expected to be a string")
			return
		temp = ''
		for c in stringToClean:
			if c in self.validCharsForFolderName:
				temp += str(c)
			else :
				temp += '_'
		return temp

	def start(self, shouldPauseAtEnd):
		self.print_FileAndSysout("\nStar scrapping :",str(datetime.datetime.now()),'\n')

		nextUrl = self.startComicUrl
		pageCount = 0
		while ( self.pageCountLimit == -1 or pageCount < self.pageCountLimit) and nextUrl:
			self.print_FileAndSysout('#'+str(pageCount),'Next Url :',nextUrl)
			r = requests.get(nextUrl)
			if r.status_code == 200 :
				soup = BeautifulSoup(r.text,'html.parser')
				imgSrc = ''
				imgSrcExtension = ''
				chapterNumber = ''
				imageNumber = ''
				lastPageForCurrentChapter = ''
				imgArray = soup.select('#viewer img#image')
				# self.print_FileAndSysout('imgArray :',imgArray)
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
					# self.print_FileAndSysout( imgSrc, imgSrcExtension )
				urlParsed = urllib.parse.urlparse(r.url)
				if urlParsed and urlParsed.path:
					# self.print_FileAndSysout(urlParsed,urlParsed.path)
					(pathBeforePage,pageFileName) = os.path.split(urlParsed.path)
					if pageFileName:
						(imageNumber,tmpExtention) = os.path.splitext(pageFileName)
						# self.print_FileAndSysout( 'imageNumber :', imageNumber )
					if pathBeforePage :
						(nothingImportant,chapterNumber) = os.path.split(pathBeforePage)
						# self.print_FileAndSysout( 'chapterNumber :', chapterNumber )
				if not imgSrc:
					self.print_FileAndSysout('imgSrc is incorrect')
				elif not imageNumber or not is_integer(imageNumber) :
					self.print_FileAndSysout('imageNumber is incorrect')
				elif not chapterNumber:
					self.print_FileAndSysout('chapterNumber is incorrect')
				elif not imgSrcExtension:
					self.print_FileAndSysout('imgSrcExtension is incorrect')
				else:
					imageFileName = '%(chapter)s_-_%(number)03d%(ext)s' % {"chapter": chapterNumber, "number": int(imageNumber), 'ext': imgSrcExtension}
					imageFileName = self.cleanStringForFolderName( imageFileName )
					imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
					# self.print_FileAndSysout(imageFileName)
					if os.path.isfile( imageFileName ):
						self.print_FileAndSysout('\tFile '+imageFileName+' already exists.')
					else:
						imageRequest = requests.get(imgSrc)
						if imageRequest.status_code != 200:
							self.print_FileAndSysout('\tImage request failed :',r)
						else:
							with open(imageFileName, 'wb') as f:
								f.write(imageRequest.content)
								self.print_FileAndSysout('\tImage saved as '+imageFileName)
				
				pagesArray = soup.select('form#top_bar div.r.m div select.m option')
				# self.print_FileAndSysout('pagesArray :',pagesArray)
				if pagesArray and len(pagesArray) > 0 :
					pagesArray.sort(key=lambda option: int(option['value']))
					# self.print_FileAndSysout('pagesArray sorted :',pagesArray)
					lastPageForChapterOption = pagesArray[len(pagesArray)-1]
					if lastPageForChapterOption and lastPageForChapterOption['value'] :
						lastPageForCurrentChapter = lastPageForChapterOption['value']
						# self.print_FileAndSysout( 'lastPageForCurrentChapter :',lastPageForCurrentChapter )
				
				nextUrl = ''
				if imageNumber and is_integer(imageNumber) and lastPageForCurrentChapter and is_integer(lastPageForCurrentChapter) :
					if lastPageForCurrentChapter == imageNumber :
						chapterNavigationDiv = soup.find('div',id='chnav')
						if chapterNavigationDiv:
							nextChapterSpanLabel = chapterNavigationDiv.find('span',string=re.compile('^Next.*'))
							if nextChapterSpanLabel and nextChapterSpanLabel.parent and nextChapterSpanLabel.parent.a and nextChapterSpanLabel.parent.a['href'] :
								nextUrl = nextChapterSpanLabel.parent.a['href']
					else:
						nextUrlArray = soup.select('#top_center_bar a.btn.next_page')
						# self.print_FileAndSysout('nextUrlArray :',nextUrlArray)
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

		self.print_FileAndSysout('Page Count :',pageCount)
		
		if shouldPauseAtEnd:
			os.system("pause")
		
		return pageCount












