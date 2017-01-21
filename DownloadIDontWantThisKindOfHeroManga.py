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

firstCommicUrl = 'http://mangafox.me/manga/i_don_t_want_this_kind_of_hero/c137/1.html'

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

valid_chars = "-_.()%s%s" % (string.ascii_letters, string.digits)
def cleanStringForFolderName(stringToClean):
	temp = ''
	for c in stringToClean:
		if c in valid_chars:
			temp += str(c)
		else :
			temp += '_'
	return temp


print_FileAndSysout("\nStar scrapping :",str(datetime.datetime.now()),'\n')

nextUrl = firstCommicUrl
pageCount = 0
while pageCount < pageCountLimit and nextUrl:
	print_FileAndSysout('#'+str(pageCount),'Next Url :',nextUrl)
	r = requests.get(nextUrl)
	if r.status_code == 200 :
		soup = BeautifulSoup(r.text,'html.parser')
		imgSrc = ''
		imgSrcExtension = ''
		chapterNumber = ''
		imageNumber = ''
		lastPageForCurrentChapter = ''
		imgArray = soup.select('#viewer img#image')
		# print_FileAndSysout('imgArray :',imgArray)
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
			# print_FileAndSysout( imgSrc, imgSrcExtension )
		urlParsed = urllib.parse.urlparse(r.url)
		if urlParsed and urlParsed.path:
			# print_FileAndSysout(urlParsed,urlParsed.path)
			(pathBeforePage,pageFileName) = os.path.split(urlParsed.path)
			if pageFileName:
				(imageNumber,tmpExtention) = os.path.splitext(pageFileName)
				# print_FileAndSysout( 'imageNumber :', imageNumber )
			if pathBeforePage :
				(nothingImportant,chapterNumber) = os.path.split(pathBeforePage)
				# print_FileAndSysout( 'chapterNumber :', chapterNumber )
		if not imgSrc:
			print_FileAndSysout('imgSrc is incorrect')
		elif not imageNumber or not is_integer(imageNumber) :
			print_FileAndSysout('imageNumber is incorrect')
		elif not chapterNumber:
			print_FileAndSysout('chapterNumber is incorrect')
		elif not imgSrcExtension:
			print_FileAndSysout('imgSrcExtension is incorrect')
		else:
			imageFileName = '%(chapter)s_-_%(number)03d%(ext)s' % {"chapter": chapterNumber, "number": int(imageNumber), 'ext': imgSrcExtension}
			imageFileName = cleanStringForFolderName( imageFileName )
			imageFileName = os.path.join(imageFilesDestinationFolder,imageFileName)
			# print_FileAndSysout(imageFileName)
			if os.path.isfile( imageFileName ):
				print_FileAndSysout('\tFile '+imageFileName+' already exists.')
			else:
				imageRequest = requests.get(imgSrc)
				if imageRequest.status_code != 200:
					print_FileAndSysout('\tImage request failed :',r)
				else:
					with open(imageFileName, 'wb') as f:
						f.write(imageRequest.content)
						print_FileAndSysout('\tImage saved as '+imageFileName)
		
		pagesArray = soup.select('form#top_bar div.r.m div select.m option')
		# print_FileAndSysout('pagesArray :',pagesArray)
		if pagesArray and len(pagesArray) > 0 :
			pagesArray.sort(key=lambda option: int(option['value']))
			# print_FileAndSysout('pagesArray sorted :',pagesArray)
			lastPageForChapterOption = pagesArray[len(pagesArray)-1]
			if lastPageForChapterOption and lastPageForChapterOption['value'] :
				lastPageForCurrentChapter = lastPageForChapterOption['value']
				# print_FileAndSysout( 'lastPageForCurrentChapter :',lastPageForCurrentChapter )
		
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
				# print_FileAndSysout('nextUrlArray :',nextUrlArray)
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

print_FileAndSysout('Page Count :',pageCount)

os.system("pause")












