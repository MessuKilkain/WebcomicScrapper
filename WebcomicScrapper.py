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
import shelve

class WebcomicScrapper(object):

	def __init__(self,startComicUrl='',imageFilesDestinationFolder='',pageCountLimit=1,startWithLastValidUrlWithNext=True):
		self._validCharsForFolderName = "-_.()%s%s" % (string.ascii_letters, string.digits)
		self.startComicUrl = startComicUrl
		self.imageFilesDestinationFolder = imageFilesDestinationFolder
		self.logFileName = self.imageFilesDestinationFolder+'.log'
		self.shelveFileName = self.imageFilesDestinationFolder+'.shelve'
		if startWithLastValidUrlWithNext and self.lastValidUrlWithNext:
			self.startComicUrl = self.lastValidUrlWithNext
		self.pageCountLimit = pageCountLimit
		self.interRequestWaitingTime = 1
		self.numberOfFailureBeforeStop = -1

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
	def shelveFileName(self):
		return self._shelveFileName
	@shelveFileName.setter
	def shelveFileName(self,value):
		if not isinstance(value, str):
			raise ValueError("shelveFileName is expected to be a string")
		else:
			self._shelveFileName = value
		return
	
	@property
	def lastValidUrlWithNext(self):
		returnedValue = ''
		try:
			with shelve.open(self.shelveFileName, flag='r') as db:
				returnedValue = db['lastValidUrlWithNext']
		finally:
			return returnedValue
	@lastValidUrlWithNext.setter
	def lastValidUrlWithNext(self,value):
		if not isinstance(value, str):
			raise ValueError("lastValidUrlWithNext is expected to be a string")
		else:
			with shelve.open(self.shelveFileName) as db:
				db['lastValidUrlWithNext'] = value
				db.sync()
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
	
	@property
	def numberOfFailureBeforeStop(self):
		return self._numberOfFailureBeforeStop
	@numberOfFailureBeforeStop.setter
	def numberOfFailureBeforeStop(self,value):
		if ( not isinstance(value, int) ) or value < -1 or value == 0:
			raise ValueError("numberOfFailureBeforeStop is expected to be a positive int or null or -1 for no limit")
		else:
			self._numberOfFailureBeforeStop = value
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
		
		# Create the destination folder if it does not exist
		if self.imageFilesDestinationFolder and not os.path.exists(self.imageFilesDestinationFolder):
			os.makedirs(self.imageFilesDestinationFolder)

		nextUrl = self.startComicUrl
		pageCount = 0
		while ( self.pageCountLimit == -1 or pageCount < self.pageCountLimit) and nextUrl:
			currentUrl = nextUrl
			self.logInfo('#'+str(pageCount),'Url :',currentUrl)
			everythingWentWell = True
			try:
				r = requests.get(currentUrl)
				self.logDebug('r.status_code :',r.status_code)
				self.logDebug('r :',str(r))
				if r.status_code != 200:
					everythingWentWell = False
					self.logWarn('\tRequest failed :',r)
				elif r.status_code == 200 :
					soup = BeautifulSoup(r.text,'html.parser')
					
					(nextUrl,imageFileName,imgSrc) = self.getValuesFromPage( soup, r )
					
					if not imgSrc:
						everythingWentWell = False
						self.logWarn('imgSrc is incorrect')
					elif not imageFileName :
						everythingWentWell = False
						self.logWarn('imageFileName is incorrect')
					else:
						if os.path.isfile( imageFileName ):
							self.logInfo('\tFile '+imageFileName+' already exists.')
						else:
							imageRequest = requests.get(imgSrc)
							if imageRequest.status_code != 200:
								everythingWentWell = False
								self.logWarn('\tImage request failed :',r)
							else:
								with open(imageFileName, 'wb') as f:
									f.write(imageRequest.content)
									self.logInfo('\tImage saved as '+imageFileName)
					
					if currentUrl == nextUrl :
						# We prevent the loop to stay on the same url
						nextUrl = ''
					if nextUrl :
						urlParsed = urllib.parse.urlparse(nextUrl)
						if not( urlParsed.scheme and urlParsed.netloc and urlParsed.path ):
							nextUrl = ''
					if nextUrl:
						pageCount += 1
						if len(imagesFailuresUrls) == 0 and everythingWentWell:
							self.lastValidUrlWithNext = currentUrl
			except Exception as e:
				everythingWentWell = False
				self.logWarn('Request Error :',str(e))
				# We stop the loop since we are not able to get a nextUrl
				nextUrl = ''
			finally:
				if not everythingWentWell:
					imagesFailuresUrls.append(currentUrl)
				if self.interRequestWaitingTime > 0:
					time.sleep(self.interRequestWaitingTime)
				if self.numberOfFailureBeforeStop != -1 and self.numberOfFailureBeforeStop < len(imagesFailuresUrls):
					# We stop the loop since we encountered more than tolerated number of failure
					self.logWarn('Number of failure before stop(',str(self.numberOfFailureBeforeStop),') met')
					nextUrl = ''
			# While loop end

		self.logInfo('Page Count :',pageCount)
		
		if imagesFailuresUrls and len(imagesFailuresUrls) > 0:
			self.logWarn('Some image requests have failed :',str(imagesFailuresUrls))
		if self.lastValidUrlWithNext:
			self.logInfo('Last valid url saved :',self.lastValidUrlWithNext)
		
		if shouldPauseAtEnd:
			os.system("pause")
		
		return pageCount
	
	# return (nextUrl,imageFileName,imgSrc)
	def getValuesFromPage(self,soup,request):
		imgSrc = ''
		imageFileName = ''
		nextUrl = ''
		return (nextUrl,imageFileName,imgSrc)





