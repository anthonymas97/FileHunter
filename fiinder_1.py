import os
import re
import sys
import glob
from os import walk
import mmap
from threading import  Thread
from datetime import datetime
from events import Events
from time import sleep


class Search:
	keyword = ""
	extension_List = [".txt", ".ppt", ".doc",".xls", ".csv"]
	searchList = []
	drivesList = []
	
	events = 0
	indexing = False
	totalIndexThreads = 0
	killSearch = False

	t1 = datetime.now()

	def __init__(self):
    	# body of the constructor
		self.events = Events()
		self.indexing = True
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
			elif line == 'K:':
				continue
			else:
				list1.append(line)
		return list1

	def searchFile(self, filename, dirname):
		for extension in self.extension_List:
			if filename.lower().endswith(extension):
				cwd = os.getcwd()
				fullPath = os.path.join(dirname,filename)
				if os.path.isfile(fullPath): #and searchFileContents(fullPath, keyword):
					#print(fullPath)
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
						if (result != -1 and result not in self.searchList):
							self.searchList.append(result)
		if self.indexing and self.totalIndexThreads > 0:
			self.totalIndexThreads -= 1
		else:
			self.indexing = False

	os.chdir('/')
	def spider(self, drivesList):
		for drive in self.drivesList:
			if (os.path.isdir(drive)):
				#print('DRIVE', drive)
				thread = Thread(target=self.threadedWalk, args=(drive,))
				thread.start()
				self.totalIndexThreads += 1

	def startSearch(self):
		self.spider(self.drivesList)

	def search(self, keyword):
		self.keyword = keyword
		localList = []

		if self.indexing:
			Exception('INDEXING')
		
		for file in self.searchList:
			if (self.killSearch):
				self.killSearch = False
				break
			if self.searchFileContents(file, keyword):
				localList.append(file)
				self.events.newFileList(localList, self.keyword)
		return localList

	def stopSearch(self):
		self.killSearch = True

	def isIndexing(self):
		return self.indexing