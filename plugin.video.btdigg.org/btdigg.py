#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
#import re
#import sys
import os
import Cookie

import string, xbmc, xbmcgui, xbmcplugin, urllib, cookielib, xbmcaddon
#-------------------------------
import urllib, urllib2, time, random
#from time import gmtime, strftime 
#from urlparse import urlparse 

import HTMLParser 
hpar = HTMLParser.HTMLParser()
#-----------------------------------------
import socket
socket.setdefaulttimeout(50)

icon = ""
siteUrl = 'api.btdigg.org/api/private-c47ba652ee73735a/s02'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'btdigg.cookies.sid')#'plugin.video.krasfs.ru.cookies.sid'

#h = int(sys.argv[1])


#--------------- 
cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def unescape(text): 
    try: 
        text = hpar.unescape(text) 
    except: 
        text = hpar.unescape(text.decode('utf8')) 

    try: 
        text = unicode(text, 'utf-8') 
    except: 
        text = text 

    return text 
#--------------- 
url='http://www.btdigg.org/' 

#-- step 1 - get session cookies 
post = None 
request = urllib2.Request(url, post) 

request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)') 
request.add_header('Host',    'www.krasfs.ru') 
request.add_header('Accept', '*/*') 
request.add_header('Accept-Language', 'ru-RU') 
request.add_header('Referer',    'http://www.btdigg.org') 

try: 
    f = urllib2.urlopen(request) 
except IOError, e: 
    if hasattr(e, 'reason'): 
        xbmc.log('We failed to reach a server. Reason: '+ e.reason) 
    elif hasattr(e, 'code'): 
        xbmc.log('The server couldn\'t fulfill the request. Error code: '+ e.code)

# ---------------------------------------

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def inputbox():
	skbd = xbmc.Keyboard()
	skbd.setHeading('Поиск:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return ""


def upd(category, sort, s):
	Lout=[]
	for p in range (0,15):
		request = urllib2.Request('http://api.btdigg.org/api/private-c47ba652ee73735a/s02?q='+s.replace(" ","+")+"&p="+str(p)+"&order=1")
		
		request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)') 
		request.add_header('Accept', '*/*') 
		request.add_header('Accept-Language', 'ru-RU') 
		try: 
			f = urllib2.urlopen(request) 
			html = f.read()
			list=eval(html)
			for i in list:
				info_hash=i["info_hash"]
				name=eval('u"'+i["name"].replace('"','')+'"')
				files=i["files"]
				reqs=i["reqs"]
				magnet=i["magnet"]
				weight=i["weight"]
				size=i["size"]
				
				if size<1073741824:	s_size=str(float(size)/1024/1024)[:5]+" MB /"
				else:				s_size=str(float(size)/1024/1024/1024)[:5]+" GB /"
				
				if files<10:     s_files="   "+str(files)+"   "
				elif files<100:  s_files="  "+str(files)+"  "
				elif files<1000: s_files=" "+str(files)+" "
				
				srf=int(size/files/1024/1024)
				
				if reqs<10:		sids="   "+str(reqs)+"   "
				elif reqs<100:	sids="  "+str(reqs)+"  "
				elif reqs<1000:	sids=" "+str(reqs)+" "
				
				torrent='http://torcache.net/torrent/'+info_hash+".torrent"
				if srf>23: Lout.append([sids, s_size+s_files+" |", name, magnet])

		except IOError, e: 
			if hasattr(e, 'reason'): 
				print 'We failed to reach a server. Reason: '+ e.reason
			elif hasattr(e, 'code'): 
				print 'The server couldn\'t fulfill the request. Error code: '+ e.code
			return ""
	return Lout


def format(L):
		if L==None: 
			return ["","","","","","","","",""]
		else:
			Ln=[]
			i=0
			tmp1=''
			tmp2=''
			tmp3=''
			for itm in L:
				i+=1
				if len(itm)>6:
					if itm[:5]=="</out":
						i=0
						Ln.append([" -- ",tmp3,tmp2,tmp1])
					elif itm[:4]=="<has":
						tmp1='https://krasfs.ru/download.php?hash='+itm[6:-7]
					elif itm[:4]=="<alt":
						tmp2=itm[10:-11]
					elif itm[:6]=="<sizef":
						tmp3=itm[7:-8]
			return Ln
			
class Tracker:
	def __init__(self):
		pass

	def Search(self, text="matrix", category=4):
		sort='newest'
		L=upd(category, sort, xt(text))
		return L