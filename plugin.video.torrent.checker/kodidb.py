import log

import xbmc, filesystem, xbmcvfs, os, time
import xml.etree.ElementTree as ET


class AdvancedSettingsReader(object):
	dict = {}
	def LOG(self, s):
		log.debug('[AdvancedSettingsReader]: ' + s)
	
	def __init__(self):
		self.use_mysql = False
		self.dict.clear()
	
		path = xbmc.translatePath('special://profile/advancedsettings.xml').decode('utf-8')
		self.LOG(path)
		if not filesystem.exists(path):
			return

		try:
			with filesystem.fopen(path, 'r') as f:
				content = f.read()
				log.debug(content)
				root = ET.fromstring(content)
		except IOError as e:
			self.LOG("I/O error({0}): {1}".format(e.errno, e.strerror))
			return
		except BaseException as e:
			self.LOG("error: " + str(e))
			return

		for section in root:
			if section.tag == 'videodatabase':
				for child in section:
					if child.tag in ['type', 'host', 'port', 'user', 'pass', 'name']:
						self.dict[child.tag] = child.text
						log.debug(child.text)
				self.LOG('<videodatabase> found')
				return
				
		self.LOG('<videodatabase> not found')
		
	def __getitem__(self, key):
		return self.dict.get(key, None)

reader = AdvancedSettingsReader()

DB_VERSIONS = {
	'10': '37',
	'11': '60',
	'12': '75',
	'13': '78',
	'14': '90',
	'15': '93',
	'16': '99'
}

BASE_PATH = 'special://database'		
class VideoDatabase(object):
	@staticmethod
	def find_last_version(name, path=BASE_PATH):
		import re
		try:
			dirs, files = xbmcvfs.listdir(path)
			matched_files = [f for f in files if bool(re.match(name, f, re.I))]  #f.startswith(name)]
			versions = [int(os.path.splitext(f[len(name):])[0]) for f in matched_files]
			if not versions:
				return 0
			return max(versions)
		except BaseException as e:
			log.debug(e, log.lineno())
			return 0

	@staticmethod
	def get_db_version(name=None):
		major = xbmc.getInfoLabel("System.BuildVersion").split(".")[0]
		ver = DB_VERSIONS.get(major)
		if ver:
			return ver

		return VideoDatabase.find_last_version(name, 'special://home/dbversions')

	def __init__(self):
		try:
			
			self.DB_NAME = reader['name'] if reader['name'] is not None else 'myvideos'
			self.DB_NAME += self.get_db_version(self.DB_NAME)
			xbmc.log('kodidb: DB name is ' + self.DB_NAME )

			self.DB_USER = reader['user']
			self.DB_PASS = reader['pass']
			self.DB_ADDRESS = reader['host']
			self.DB_PORT=reader['port']
		  
			if reader['type'] == 'mysql' and \
							self.DB_ADDRESS is not None and \
							self.DB_USER is not None and \
							self.DB_PASS is not None and \
							self.DB_NAME is not None:

				xbmc.log('kodidb: Service: Loading MySQL as DB engine')
				self.DB = 'mysql'
			else:
				xbmc.log('kodidb: Service: MySQL not enabled or not setup correctly')
				raise ValueError('MySQL not enabled or not setup correctly')
		except:
			self.DB = 'sqlite'
			self.db_dir = os.path.join(xbmc.translatePath(BASE_PATH), 'MyVideos%s.db' % VideoDatabase.find_last_version('MyVideos'))
			
	def create_connection(self):
		if self.DB == 'mysql':
			import mysql.connector
			return mysql.connector.connect(	database=self.DB_NAME,
											user=self.DB_USER,
											password=self.DB_PASS,
											host=self.DB_ADDRESS,
											port=self.DB_PORT,
											buffered=True)
		else:
			from sqlite3 import dbapi2 as db_sqlite
			return db_sqlite.connect(self.db_dir)
			
	def sql_request(self, req):
		if self.DB == 'mysql':
			return req.replace('?', '%s')
		else:
			return req.replace('%s', '?')
	
class KodiDB(object):
	
	def debug(self, msg, line=0):
		if isinstance(msg, unicode):
			msg = msg.encode('utf-8')
		#line = inspect.currentframe().f_back.f_back.f_lineno
		log.debug('[KodiDB:%d] %s' % (line, msg))
	
	def __init__(self, strmName, strmPath, pluginUrl):
		
		self.debug('strmName: ' + strmName, log.lineno())
		self.debug('strmPath: ' + strmPath, log.lineno())
		self.debug('pluginUrl: ' + pluginUrl, log.lineno())
		
		self.timeOffset	= 0
		
		self.strmName 	= strmName
		self.strmPath 	= strmPath
		self.pluginUrl 	= pluginUrl
		
		self.videoDB = VideoDatabase()
	
	def PlayerPreProccessing(self):
		xbmc.sleep(1000)
		self.db = self.videoDB.create_connection()
		try:
			self.debug('PlayerPreProccessing: ', log.lineno())
			strmItem = self.getFileItem(self.strmName, self.strmPath)
			if not strmItem is None:
				self.debug('\tstrmItem = ' + str(strmItem), log.lineno())
				bookmarkItem = self.getBookmarkItem(strmItem['idFile'])
				self.debug('\tbookmarkItem = ' + str(bookmarkItem), log.lineno())
				self.timeOffset = bookmarkItem['timeInSeconds'] if bookmarkItem != None else 0
				self.debug('\ttimeOffset: ' + str(self.timeOffset / 60) , log.lineno())
			else:
				self.debug('\tstrmItem is None', log.lineno())
		finally:
			self.db.close()
	
	def PlayerPostProccessing(self):
		self.db = self.videoDB.create_connection()
		try:
			self.debug('PlayerPostProccessing: ', log.lineno())

			for cnt in range(3):
				pluginItem = self.getFileItem(self.pluginUrl)
				self.debug('\tpluginItem = ' + str(pluginItem), log.lineno())

				if pluginItem:
					break

				self.debug('Try again #' + str(cnt + 2))
				time.sleep(2)

			strmItem = self.getFileItem(self.strmName, self.strmPath)
			self.debug('\tstrmItem = ' + str(strmItem), log.lineno())
			
			self.CopyWatchedStatus(pluginItem, strmItem)
			self.ChangeBookmarkId(pluginItem, strmItem)

		finally:
			self.db.close()
		
		
	def CopyWatchedStatus(self, pluginItem, strmItem ):
	
		if pluginItem is None or strmItem is None:
			return

		if pluginItem['playCount'] is None or strmItem['idFile'] is None:
			return
		
		cur = self.db.cursor()

		sql = 	'UPDATE files'
		sql += 	' SET playCount=' + str(pluginItem['playCount'])
		sql += 	' WHERE idFile = ' + str(strmItem['idFile'])
		
		self.debug('CopyWatchedStatus: ' + sql, log.lineno())
		
		cur.execute(sql)
		self.db.commit()
		
	def ChangeBookmarkId(self, pluginItem, strmItem ):
		if pluginItem is None or strmItem is None:
			return
			
		if strmItem['idFile'] is None or pluginItem['idFile'] is None:
			return
	
		cur = self.db.cursor()
		
		#delete previous
		sql = "DELETE FROM bookmark WHERE idFile=" + str(strmItem['idFile'])
		self.debug('ChangeBookmarkId: ' + sql, log.lineno())
		cur.execute(sql)
		self.db.commit()
		

		#set new
		sql =  'UPDATE bookmark SET idFile=' + str(strmItem['idFile'])
		sql += ' WHERE idFile = ' +  str(pluginItem['idFile'])
		self.debug('ChangeBookmarkId: ' + sql, log.lineno())
		
		cur.execute(sql)
		self.db.commit()
		
	def getBookmarkItem(self, idFile):
		cur = self.db.cursor()
		sql =	"SELECT idBookmark, idFile, timeInSeconds, totalTimeInSeconds " + \
				"FROM bookmark WHERE idFile = " + str(idFile)
		cur.execute(sql)
		bookmarks = cur.fetchall()
		for item in bookmarks:
			self.debug('Bookmark: ' + item.__repr__(), log.lineno())
			return { 'idBookmark': item[0], 'idFile': item[1], 'timeInSeconds': item[2], 'totalTimeInSeconds': item[3] }
			
		return None
		
	def getFileItem(self, strFilename, strPath = None):
		cur = self.db.cursor()
		
		sql = 	"SELECT idFile, idPath, strFilename, playCount, lastPlayed " + \
				"FROM files WHERE strFilename" + \
				"='" + strFilename.replace("'", "''")	+ "'" #.split('&nfo=')[0] + "%'"
		self.debug(sql, log.lineno())
		cur.execute(sql)
		files = cur.fetchall()
		
		if len(files) == 0:
			self.debug('getFileItem: len(files) == 0', log.lineno())
			return None

		if strPath is None:
			for item in files:
				self.debug('File: ' + item.__repr__(), log.lineno())
				return { 'idFile': item[0], 'idPath': item[1], 'strFilename': item[2], 'playCount': item[3], 'lastPlayed': item[4] }
		else:
			if strPath.endswith('\\') or strPath.endswith('/'):
				strPath = strPath[:-1]
			
			self.debug(strPath, log.lineno())
			sql = 'SELECT idPath, strPath FROM path WHERE idPath IN ( '
			ids = []
			for item in files:
				ids.append( str( item[1]))
			sql += ', '.join(ids) + ' )'
			self.debug(sql, log.lineno())
			cur.execute(sql)
			paths = cur.fetchall()
			for path in paths:
				self.debug(path, log.lineno())
				#pattern = path[1].replace('\\', '/').replace('[', '\\[').replace(']', '\\]')
				if path[1].replace('\\', '/').endswith(strPath + '/') or path[1].replace('/', '\\').endswith(strPath + '\\'):
					for item in files:
						self.debug(item, log.lineno())
						if path[0] == item[1]:
							self.debug('File: ' + item.__repr__(), log.lineno())
							return { 'idFile': item[0], 'idPath': item[1], 'strFilename': item[2], 'playCount': item[3], 'lastPlayed': item[4] }
		
		self.debug('return None', log.lineno())
		return None
		
	def getPathId(self, strPath):
		cur = self.db.cursor()
		
		sql = 	"SELECT idPath, strPath FROM path " + \
				"WHERE strPath LIKE '%" + strPath.encode('utf-8').replace("'", "''") + "%'"
		self.debug(sql, log.lineno())
		cur.execute(sql)
		return cur.fetchall()
		
	def getFileDataById(self, fileId):
		return
