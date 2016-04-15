# -*- coding: utf-8 -*-

import os, sys, log

__DEBUG__ = False

class MakeCHDirException(Exception):
	def __init__(self, path):
		self.path = path

def get_filesystem_encoding():
	return sys.getfilesystemencoding() if os.name == 'nt' else 'utf-8'

def ensure_unicode(string, encoding=get_filesystem_encoding()):
	if isinstance(string, str):
		string = string.decode(encoding)
		
	if __DEBUG__:
		log.debug('\tensure_unicode(%s, encoding=%s)' % (string.encode('utf-8'), encoding))
		
	return string
	
def get_path(path):
	errors='strict'

	if path.startswith('smb://') and os.name == 'nt':
		path = path.replace('smb://', r'\\').replace('/', '\\')

	path = ensure_unicode(path)
	if os.name == 'nt':
		return path
	return path.encode(get_filesystem_encoding(), errors)

def exists(path):
	return os.path.exists(get_path(path))
	
def getcwd():
	return ensure_unicode(os.getcwd(), get_filesystem_encoding())
	
def makedirs(path):
	os.makedirs(get_path(path))
	
def chdir(path):
	os.chdir(get_path(path))
	
def save_make_chdir(new_path):
	current = getcwd()
	try:
		if not exists(new_path):
			makedirs(new_path)
		chdir(new_path)
	except BaseException as e:
		log.print_tb(e)
		raise MakeCHDirException(current)
	finally:
		return current

class save_make_chdir_context(object):

	def __init__(self, path):
		self.newPath = path

	# context management
	def __enter__(self):
		self.savePath = getcwd()
		if not exists(self.newPath):
			makedirs(self.newPath)
		chdir(self.newPath)
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		chdir(self.savePath)
		if exc_type:
			import traceback
			traceback.print_exception(exc_type, exc_val, exc_tb, limit=10, file=sys.stderr)
			log.debug("!!error!! " + str(exc_val))
			return True

def isfile(path):
	return os.path.isfile(get_path(path))
	
def abspath(path):
	return ensure_unicode(os.path.abspath(get_path(path)), get_filesystem_encoding())

def relpath(path, start=getcwd()):
	return ensure_unicode(os.path.relpath(get_path(path), get_path(start)), get_filesystem_encoding())

def normpath(path):
	return ensure_unicode(os.path.normpath(get_path(path)), get_filesystem_encoding())
	
def fopen(path, mode):
	return open(get_path(path), mode)
	
def join(path, *paths):
	path = get_path(path)
	fpaths = []
	for p in paths:
		fpaths.append( get_path(p) )
	return ensure_unicode(os.path.join(path, *tuple(fpaths)), get_filesystem_encoding())

def listdir(path):
	ld = []
	for p in os.listdir(get_path(path)):
		ld.append(ensure_unicode(p))
	return ld

def remove(path):
	os.remove(get_path(path))

def getmtime(path):
	return os.path.getmtime(get_path(path))

def getctime(path):
	return os.path.getctime(get_path(path))


def test():	
	log.debug('Filesystem encoding: %s' % get_filesystem_encoding())
	log.debug('getcwd(): %s' % getcwd().encode('utf-8'))
	log.debug('relpath(getcwd(), ".."): %s' % relpath(getcwd(), "..").encode('utf-8'))
	
	subpath = u'Подпапка'
	subpath2 = u'файл.ext'

	with save_make_chdir_context(join(getcwd(), subpath)):
		log.debug('aaaaa')
		raise Exception('save_make_chdir')
		log.debug('bbbbb')
	
	fullpath = join(getcwd(), subpath, subpath2)
	log.debug('subpath: %s' % subpath.encode('utf-8'))
	log.debug('subpath2: %s' % subpath2.encode('utf-8'))
	log.debug('join(getcwd(), subpath, subpath2): %s' % fullpath.encode('utf-8'))

	remote_file = u'smb://vd/Incoming/test.txt'
	if isfile(remote_file):
		with fopen(remote_file, "r") as f:
			log.debug(f.read())


if __name__ == '__main__':
	__DEBUG__ = True
	test()