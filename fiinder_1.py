import os
import re
import sys
import glob
from os import walk
import mmap
from threading import  Thread
from datetime import datetime

keyword = "trademark"
extension_List = [".txt", ".ppt", ".doc",".xls", ".csv"]
searchList = []

t1 = datetime.now()

def get_drives():
	response = os.popen("wmic logicaldisk get caption")
	list1 = []
	total_file = []

	for line in response.readlines():
		line = line.strip("\n")
		line = line.strip("\r")
		line = line.strip(" ")
		if (line == "Caption" or line == ""):
			continue
		if (line == 'C:'):
			#print('LINE', line)
			for (dirname) in os.listdir(line + '\\'):
				if (dirname != 'Windows' and 
					dirname != 'Program Files (x86)' and 
					dirname != 'Program Files' and not 
					dirname.startswith('C:\\$')):
					list1.append('C:\\' + dirname)
		else:
			list1.append(line)
	return list1

drivesList = get_drives()
print(drivesList)

def searchFile(filename, dirname):
	for extension in extension_List:
		if filename.lower().endswith(extension):
			cwd = os.getcwd()
			fullPath = os.path.join(dirname,filename)
			if os.path.isfile(fullPath): #and searchFileContents(fullPath, keyword):
				#print(fullPath)
				return fullPath
	return -1

def searchFileContents(sourceFile, keyword):
	try:
		a = sourceFile.replace(r'\t', r'\\t').replace(r'\a', r'\\a')
		f = open(a, 'r')
		contents = f.read()
		if (contents.find(keyword) >= 0):
			print('FOUND: ', sourceFile)
			return True
		else:
			return False
	except:
		return False

def threadedWalk(directory):
	#print('THREADED WALK')
	global searchList
	if (os.path.isdir(directory)):
		for (dirname,dirs,files) in os.walk(directory):
				for filename in files:
					result = searchFile(filename, dirname)
					if (result != -1):
						searchList.append(result)

os.chdir('/')
def spider(drivesList):
	#print('THREADING')
	for drive in drivesList:
		# if drive.startswith('C:\\$'):
		# 	continue
		if (os.path.isdir(drive)):
			print('DRIVE', drive)
			thread = Thread(target=threadedWalk, args=(drive,))
			thread.start()

#file1 = r"C:\Users\grena_000\Documents\test.txt"

def startSearch():
	spider(drivesList)

def search(keyword):
	localList = []
	for file in searchList:
		if searchFileContents(file, keyword):
			localList.append(file)
	return localList

t2 = datetime.now()
totalTime = t2-t1
print('Total Time', totalTime)