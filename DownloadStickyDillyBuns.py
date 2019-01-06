"""
 WebcomicScrapper for Webcomic Menage a 3
 http://www.stickydillybuns.com/strips-sdb/
"""
import os.path
import urllib.parse
from datetime import datetime

from WebcomicScrapper import WebcomicScrapper

class WebcomicScrapper_StickyDillyBuns(WebcomicScrapper):

	def __init__(self):
		WebcomicScrapper.__init__(self, startComicUrl='http://www.stickydillybuns.com/strips-sdb/awesome_leading_man', imageFilesDestinationFolder='StickyDillyBuns', pageCountLimit=60 )

	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		
		imgSrcExtension = ''
		imgTitle = ''
		imgDate = ''
		imgArray = soup.select('#comic img')
		self.logDebug('imgArray :',imgArray)
		if imgArray and len(imgArray) > 0 :
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
			self.logDebug( imgSrc, imgSrcExtension )
		if not imgArray or len(imgArray) == 0 :
			imgArray = soup.select('#cc-comic')
			img = imgArray[0]
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(request.url,imgSrc)
			self.logDebug( imgSrc, imgSrcExtension )
		
		# Get the title of the comic
		if not imgTitle:
			currentOption = soup.select_one('select#navjump option[value=""]')
			if currentOption:
				imgTitle = currentOption.get_text()
		if not imgTitle:
			currentOption = soup.select_one('#fold2b h3')
			if currentOption:
				imgTitle = currentOption.get_text()
		
		# Get the date of the comic
		if not imgDate:
			fallbackDate = soup.select_one('#date')
			if fallbackDate and fallbackDate.get_text():
				self.logDebug("fallbackDate : ",str(fallbackDate))
				self.logDebug("fallbackDate.get_text() : ",str(fallbackDate.get_text()))
				imgDate = datetime.strptime( fallbackDate.get_text(), '%B %d, %Y' ).strftime('%Y-%m-%d')
		
		#imgDate fallback
		if not imgDate:
			fallbackDate = soup.select_one('#fold2b')
			self.logDebug("fallbackDate : ",str(fallbackDate))
			self.logDebug("fallbackDate.contents : ",str(fallbackDate.contents))
			for child in fallbackDate.children:
				child = child.string
				self.logDebug("fallbackDate.child : ",str(child))
				if child and child.startswith("Published on"):
					imgDate = datetime.strptime( child, 'Published on : %B %d, %Y' ).strftime('%Y-%m-%d')
					break
		
		if not imgSrcExtension:
			self.logWarn('imgSrcExtension is incorrect')
		elif not imgTitle:
			self.logWarn('imgTitle is incorrect')
		elif not imgDate:
			self.logWarn('imgDate is incorrect')
		else:
			imageFileName = imgDate + '_-' + imgTitle + imgSrcExtension
			imageFileName = self.cleanStringForFolderName(imageFileName)
			imageFileName = os.path.join(self.imageFilesDestinationFolder,imageFileName)
			self.logDebug(imageFileName)
		
		aNavNext = soup.select_one('#cnav #cndnext')
		if aNavNext and aNavNext['href'] and aNavNext['href'] != '#':
			nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		if not nextUrl:
			aNavNext = soup.select_one('#cnav .nav .next')
			if aNavNext and aNavNext['href'] and aNavNext['href'] != '#':
				nextUrl = urllib.parse.urljoin(request.url,aNavNext['href'])
		return (nextUrl,imageFileName,imgSrc)
		

if __name__ == '__main__':
	# Start scrapping webcomic
	scrapper = WebcomicScrapper_StickyDillyBuns()

	# scrapper.startComicUrl = 'http://www.stickydillybuns.com/strips-sdb/sticky_dilly_buns_status_update'
	# scrapper.startComicUrl = 'http://www.stickydillybuns.com/strips-sdb/to_the_next_level'
	scrapper.pageCountLimit = 1000
	# scrapper.interRequestWaitingTime = 0;
	scrapper.logFileName = os.path.basename(__file__)+'.log'

	scrapper.start(True)





