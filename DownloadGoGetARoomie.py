"""
 WebcomicScrapper for Webcomic Go Get a Roomie!
"""
import os.path
import urllib.parse

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_GoGetARoomie(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.gogetaroomie.com/comic/and-so-it-begins', imageFilesDestinationFolder='Go_Get_a_Roomie', pageCountLimit=50 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgAlt = ''
		imgDate = ''
		imgArray = soup.select('img#cc-comic')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
				# Get the date of the comic
				tmpImgSrcRoot = os.path.basename(tmpImgSrcRoot)
				imgNameParts = tmpImgSrcRoot.split('-')
				if imgNameParts and len(imgNameParts) > 3:
					imgDate = imgNameParts[1]+'-'+imgNameParts[2]+'-'+imgNameParts[3]
			# TODO : improve by adding try around get attribute with KeyError handling
			imgAlt = img['title']
			self.logDebug( imgSrc, imgSrcExtension ,imgAlt )
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
		
		navNextArray = soup.select('#comicwrap .nav a.next')
		self.logDebug('navNextArray :',navNextArray)
		if navNextArray and len(navNextArray) > 0 :
			aNavNext = navNextArray[0]
			if aNavNext['href'] and aNavNext['href'] != '#':
				nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		return (nextUrl,imageFileName,imgSrc)
		
	def logDebug(self,*objects, end='\n'):
		# self.print_FileAndSysout(*objects, end)
		return


# Start scrapping webcomic
scrapper = WebcomicScrapper_GoGetARoomie()

# scrapper.startComicUrl = 'http://www.gogetaroomie.com/comic/enough-kids-to-go-around'
scrapper.pageCountLimit = 1000
scrapper.logFileName = os.path.basename(__file__)+'.log'

scrapper.start(True)





