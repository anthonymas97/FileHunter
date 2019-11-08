import os
import re
import sys
import glob
from os import walk
import mmap
from threading import  Thread
from datetime import datetime


class Search:
	keyword = "trademark"
	extension_List = [".txt", ".ppt", ".doc",".xls", ".csv"]
	searchList = []
	drivesList = []

	t1 = datetime.now()

	def __init__(self):
    	# body of the constructor
		self.drivesList = self.get_drives()
		self.startSearch()
		print(self.drivesList)

	def get_drives(self):
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

	def searchFile(self, filename, dirname):
		for extension in self.extension_List:
			if filename.lower().endswith(extension):
				cwd = os.getcwd()
				fullPath = os.path.join(dirname,filename)
				if os.path.isfile(fullPath): #and searchFileContents(fullPath, keyword):
					print(fullPath)
					return fullPath
		return -1

	def searchFileContents(self, sourceFile, keyword):
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

	def threadedWalk(self, directory):
		#print('THREADED WALK')
		global searchList
		if (os.path.isdir(directory)):
			for (dirname,dirs,files) in os.walk(directory):
					for filename in files:
						result = self.searchFile(filename, dirname)
						if (result != -1):
							self.searchList.append(result)

	os.chdir('/')
	def spider(self, drivesList):
		#print('THREADING')
		for drive in self.drivesList:
			# if drive.startswith('C:\\$'):
			# 	continue
			if (os.path.isdir(drive)):
				print('DRIVE', drive)
				thread = Thread(target=self.threadedWalk, args=(drive,))
				thread.start()

	#file1 = r"C:\Users\grena_000\Documents\test.txt"

	def startSearch(self):
		self.spider(self.drivesList)

	def search(self, keyword):
		localList = []
		for file in self.searchList:
			if self.searchFileContents(file, keyword):
				localList.append(file)
		return localList

	t2 = datetime.now()
	totalTime = t2-t1
	print('Total Time', totalTime)