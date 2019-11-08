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
	_keyword = ""
	_extension_List = [".txt", ".ppt", ".doc",".xls", ".csv"]
	_searchList = []
	_drivesList = []
	_timer = None
	
	events = None
	_indexing = False
	_killSearch = False

	def __init__(self):
    	# body of the constructor
		self.events = Events()
		self._indexing = True
		self._drivesList = self._get_drives()
		self._startSearch()
		print(self._drivesList)

	def _startSearchTimer(self):
		self._timer = Timer(60.0, self._startSearch)
		self._timer.start()

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
		for extension in self._extension_List:
			if filename.lower().endswith(extension):
				cwd = os.getcwd()
				fullPath = os.path.join(dirname,filename)
				if os.path.isfile(fullPath):
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
						if (result != -1 and result not in self._searchList):
							self._searchList.append(result)

	os.chdir('/')
	def _spider(self, drivesList):
		for drive in drivesList:
			if (os.path.isdir(drive)):
				#print('DRIVE', drive)
				thread = Thread(target=self._threadedWalk, args=(drive,))
				thread.start()

	def _startSearch(self):
		print('CACHING STARTED')
		self._spider(self._drivesList)
		self._startSearchTimer()

	def search(self, keyword):
		"""
		Start a new search\n
		Callback made to `events.newFileList` with real-time results\n
		Returns list of results
		"""
		self._keyword = keyword
		self._killSearch = False
		localList = []
		if self._indexing:
			self._indexing = False
			sleep(5)
		
		initalSearchListCount = -1
		while(initalSearchListCount != len(self._searchList)):
			initalSearchListCount = len(self._searchList)
			for file in self._searchList:
				if (self._killSearch):
					self._killSearch = False
					break
				if self._searchFileContents(file, keyword) and file not in localList:
					localList.append(file)
					self.events.newFileList(localList, self._keyword, False)
		
		self.events.newFileList(localList, self._keyword, True)
		return localList

	def stopSearch(self):
		"""Stop the current search"""
		self._killSearch = True