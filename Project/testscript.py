import os

dirPath = "/var/lib/motion"
fileList = os.listdir(dirPath)
for fileName in fileList:
	os.remove(dirPath+"/"+fileName)
	
dirPath = "/home/Project/wav"
fileList = os.listdir(dirPath)
for fileName in fileList:
	filedirList = os.listdir(dirPath+"/"+fileName)
	for files in filedirList:
		os.remove(dirPath+"/"+fileName+"/"+files)
	os.rmdir(dirPath+"/"+fileName)
	
dirPath = "/home/Project/split"
fileList = os.listdir(dirPath)
for fileName in fileList:
	filedirList = os.listdir(dirPath+"/"+fileName)
	for files in filedirList:
		os.remove(dirPath+"/"+fileName+"/"+files)
	os.rmdir(dirPath+"/"+fileName)

#with open('classifer', 'r') as myfile:
#    data=myfile.read()
	
#print(data)