"""
 WebcomicScrapper class
"""
from bs4 import BeautifulSoup
import os.path
import string
import requests
import urllib.parse
import datetime
import time

class WebcomicScrapper(object):

	def __init__(self,startComicUrl='',imageFilesDestinationFolder='',pageCountLimit=1):
		self._validCharsForFolderName = "-_.()%s%s" % (string.ascii_letters, string.digits)
		self.startComicUrl = startComicUrl
		self.imageFilesDestinationFolder = imageFilesDestinationFolder
		self.logFileName = self.imageFilesDestinationFolder+'.log'
		self.pageCountLimit = pageCountLimit
		self.interRequestWaitingTime = 1

	@property
	def validCharsForFolderName(self):
		"""List of characters accepted for folder name."""
		return self._validCharsForFolderName
	
	@property
	def interRequestWaitingTime(self):
		return self._interRequestWaitingTime
	@interRequestWaitingTime.setter
	def interRequestWaitingTime(self,value):
		if ( not isinstance(value, float) and not isinstance(value, int) ) or value < 0.0 :
			raise ValueError("interRequestWaitingTime is expected to be a positive number (int or float)")
		else:
			self._interRequestWaitingTime = value
		return
	
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
	def logFileName(self):
		return self._logFileName
	@logFileName.setter
	def logFileName(self,value):
		if not isinstance(value, str):
			raise ValueError("logFileName is expected to be a string")
		else:
			self._logFileName = value
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
			with open(self.logFileName, 'a') as f:
				print(*objects, file=f)
		return
	def logInfo(self,*objects, end='\n'):
		self.print_FileAndSysout(*objects, end)
		return
	def logWarn(self,*objects, end='\n'):
		self.print_FileAndSysout(*objects, end)
		return
	def logDebug(self,*objects, end='\n'):
		# self.print_FileAndSysout(*objects, end)
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
		imagesFailuresUrls = []
		# TODO : improve by creating the destination folder if it does not exist

		nextUrl = self.startComicUrl
		pageCount = 0
		while ( self.pageCountLimit == -1 or pageCount < self.pageCountLimit) and nextUrl:
			self.logInfo('#'+str(pageCount),'Next Url :',nextUrl)
			r = requests.get(nextUrl)
			self.logDebug('r.status_code :',r.status_code)
			if r.status_code == 200 :
				soup = BeautifulSoup(r.text,'html.parser')
				
				(nextUrl,imageFileName,imgSrc) = self.getValuesFromPage( soup, r )
				
				if not imgSrc:
					self.logWarn('imgSrc is incorrect')
				elif not imageFileName :
					self.logWarn('imageFileName is incorrect')
				else:
					if os.path.isfile( imageFileName ):
						self.logInfo('\tFile '+imageFileName+' already exists.')
					else:
						imageRequest = requests.get(imgSrc)
						if imageRequest.status_code != 200:
							self.logWarn('\tImage request failed :',r)
							imagesFailuresUrls.append(r.url)
						else:
							with open(imageFileName, 'wb') as f:
								f.write(imageRequest.content)
								self.logInfo('\tImage saved as '+imageFileName)
				
				if nextUrl :
					urlParsed = urllib.parse.urlparse(nextUrl)
					if not( urlParsed.scheme and urlParsed.netloc and urlParsed.path ):
						nextUrl = ''
				if nextUrl:
					pageCount += 1
			if self.interRequestWaitingTime > 0:
				time.sleep(self.interRequestWaitingTime)
			# While loop end

		self.logInfo('Page Count :',pageCount)
		
		if imagesFailuresUrls and len(imagesFailuresUrls) > 0:
			self.logWarn('Some image requests have failed :',str(imagesFailuresUrls))
		
		if shouldPauseAtEnd:
			os.system("pause")
		
		return pageCount
	
	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		return (nextUrl,imageFileName,imgSrc)





