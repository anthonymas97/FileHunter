import os
import re
import sys
import glob
from os import walk
import mmap
from threading import  Thread, Timer
from datetime import datetime
from events import Events
from time import sleep


class Search:
	keyword = ""
	extension_List = [".txt", ".ppt", ".doc",".xls", ".csv"]
	searchList = []
	drivesList = []
	timer = None
	
	events = None
	indexing = False
	killSearch = False

	def __init__(self):
    	# body of the constructor
		self.events = Events()
		self.indexing = True
		self.drivesList = self._get_drives()
		self._startSearch()
		print(self.drivesList)

	def _startSearchTimer(self):
		self.timer = Timer(60.0, self._startSearch)
		self.timer.start()

	def _get_drives(self):
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

	def _searchFile(self, filename, dirname):
		for extension in self.extension_List:
			if filename.lower().endswith(extension):
				cwd = os.getcwd()
				fullPath = os.path.join(dirname,filename)
				if os.path.isfile(fullPath): #and searchFileContents(fullPath, keyword):
					#print(fullPath)
					return fullPath
		return -1

	def _searchFileContents(self, sourceFile, keyword):
		try:
			a = sourceFile.replace(r'\t', r'\\t').replace(r'\a', r'\\a')
			f = open(a, 'r')
			contents = f.read()
			if (contents.find(keyword) >= 0):
				#print('FOUND: ', sourceFile)
				return True
			else:
				return False
		except:
			return False

	def _threadedWalk(self, directory):
		#print('THREADED WALK')
		global searchList
		if (os.path.isdir(directory)):
			for (dirname,dirs,files) in os.walk(directory):
					for filename in files:
						result = self._searchFile(filename, dirname)
						if (result != -1 and result not in self.searchList):
							self.searchList.append(result)

	os.chdir('/')
	def _spider(self, drivesList):
		for drive in self.drivesList:
			if (os.path.isdir(drive)):
				#print('DRIVE', drive)
				thread = Thread(target=self._threadedWalk, args=(drive,))
				thread.start()

	def _startSearch(self):
		print('SEARCH STARTED')
		self._spider(self.drivesList)
		self._startSearchTimer()

	def search(self, keyword):
		self.keyword = keyword
		self.killSearch = False
		localList = []
		if self.indexing:
			self.indexing = False
			sleep(5)
		
		for file in self.searchList:
			if (self.killSearch):
				self.killSearch = False
				break
			if self._searchFileContents(file, keyword):
				localList.append(file)
				self.events.newFileList(localList, self.keyword, False)
		self.events.newFileList(localList, self.keyword, True)
		return localList

	def stopSearch(self):
		self.killSearch = True

	def isIndexing(self):
		return self.indexing