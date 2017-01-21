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

imageFilesDestinationFolder = 'QuestionableContent'
pageCountLimit = 10000

#firstCommicUrl = 'http://www.questionablecontent.net/view.php?comic=1'
firstCommicUrl = 'http://www.questionablecontent.net/view.php?comic=3350'

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
		comicNumber = ''
		img = soup.find('img',id='strip')
		if img :
			imgSrc = img['src']
			if imgSrc:
				(tmpImgSrcRoot,imgSrcExtension) = os.path.splitext(imgSrc)
				imgSrc = urllib.parse.urljoin(r.url,imgSrc)
		# print_FileAndSysout( imgSrc, imgSrcExtension )
		urlParsed = urllib.parse.urlparse(r.url)
		if urlParsed and urlParsed.query:
			# print_FileAndSysout(urlParsed,urlParsed.query)
			queryData = urllib.parse.parse_qs(urlParsed.query)
			if queryData:
				# print_FileAndSysout(queryData)
				# print_FileAndSysout(queryData['comic'])
				comicNumberList = queryData['comic']
				if comicNumberList and len(comicNumberList) > 0 and is_integer(comicNumberList[0]):
					comicNumber = comicNumberList[0]
		if not imgSrc:
			print_FileAndSysout('imgSrc is incorrect')
		elif not imgSrcExtension:
			print_FileAndSysout('imgSrcExtension is incorrect')
		elif not comicNumber:
			print_FileAndSysout('comicNumber is incorrect')
		else:
			imageFileName = '%(comicNumber)04d%(ext)s' % {"comicNumber": int(comicNumber), 'ext': imgSrcExtension}
			imageFileName = cleanStringForFolderName(imageFileName)
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
		nextUrl = ''
		if img and img.parent and img.parent['href'] and img.parent['href'] != '#':
			nextUrl = urllib.parse.urljoin(r.url,img.parent['href'])
		if nextUrl :
			urlParsed = urllib.parse.urlparse(nextUrl)
			if not( urlParsed.scheme and urlParsed.netloc and urlParsed.path ):
				nextUrl = ''
		if nextUrl:
			pageCount += 1

print_FileAndSysout('Page Count :',pageCount)

os.system("pause")












