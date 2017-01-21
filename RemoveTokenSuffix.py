from os import walk
import os.path

mypath="./I_Don_t_Want_This_Kind_of_Hero_-_Manga"

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
	f.extend(filenames)
	break

# print(f)
for filename in f:
	(imgSrcRoot,imgSrcExtension) = os.path.splitext(filename)
	if imgSrcExtension:
		# print(imgSrcExtension)
		underscoreIndex=imgSrcExtension.find('_')
		if underscoreIndex!=-1:
			imgSrcExtension=imgSrcExtension[:underscoreIndex]
			# print(imgSrcExtension)
			originalFilePath = os.path.join(mypath,filename)
			newFilePath = os.path.join(mypath,imgSrcRoot+imgSrcExtension)
			print("originalFilePath : "+originalFilePath)
			print("newFilePath : "+newFilePath)
			os.rename(originalFilePath, newFilePath)