try:
	from xbmc import log
except:
	def log(s):
		print s

import inspect

prefix = 'script.media.aggregator'

def debug(s, line = None):

	if isinstance(s, BaseException):
		print_tb(s)
	elif isinstance(s, unicode):
		s = s.encode('utf-8')
	elif not isinstance(s, str):
		s = str(s)

	if prefix:
		if line:
			message = '[%s: %s] %s' % (prefix, str(line), s)
		else:
			message = '[%s]  %s' % (prefix, s)
	else:
		if line:
			message = '[%s]  %s' % (line, s)
		else:
			message = s
			
	log(message)
	

def print_tb(e=None):
	import sys
	exc_type, exc_val, exc_tb = sys.exc_info()
	import traceback
	traceback.print_exception(exc_type, exc_val, exc_tb, limit=10, file=sys.stderr)

	if e:
		debug(str(e))

def lineno():
	"""Returns the current line number in our program."""
	return inspect.currentframe().f_back.f_lineno
