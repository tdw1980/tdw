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
siteUrl = 'fileek.com'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'fileek.com.sid')#'plugin.video.krasfs.ru.cookies.sid'

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
url='http://www.KinoPoisk.ru/' 


def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

headers  = {
	'User-Agent' : 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.7.62 Version/11.00',
	'Accept'     :' text/html, application/xml, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*',
	'Accept-Language':'ru-RU,ru;q=0.9,en;q=0.8',
	'Accept-Charset' :'utf-8, utf-16, *;q=0.1',
	'Accept-Encoding':'identity, *;q=0'
}

def get_HTML(url, post = None, ref = None, get_redirect = False):
	request = urllib2.Request(url, post)
	import urlparse
	#import HTMLParser
	#hpar = HTMLParser.HTMLParser()
	host = urlparse.urlsplit(url).hostname
	if ref==None:
		try:   ref='http://'+host
		except:ref='localhost'

	request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
	request.add_header('Host',   host)
	request.add_header('Accept', 'text/html, application/xhtml+xml, */*')
	request.add_header('Accept-Language', 'ru-RU')
	request.add_header('Referer',             ref)
	request.add_header('Content-Type','application/x-www-form-urlencoded')
	request.add_header('cache-control','no-cache')
	request.add_header('pragma','no-cache')
	try:
		f = urllib2.urlopen(request)
	except IOError, e:
		if hasattr(e, 'reason'):
			print('We failed to reach a server.')
		elif hasattr(e, 'code'):
			print('The server couldn\'t fulfill the request.')
		return None
	if get_redirect == True:
		html = f.geturl()
	else:
		html = f.read()
	return html

			

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def csr(http):
	ss='<div id="item_'
	es='<a id="magnetbtn_'
	LT=mfindal(http, ss, es)
	L=[]
	for i in LT:
		ss='href="#">'
		es="</a></div>"
		title=mfindal(i, ss, es)[0][len(ss):]
		
		ss='<div class="size">'
		es='<div class="magnet-btn">'
		size=mfindal(i, ss, es)[0][len(ss):].replace("</div>","").replace(chr(10),"").replace(chr(13),"").replace("\t","").replace(" ","").replace(".00"," ")
		if len(size)==4: size="     "+size+"     "
		if len(size)==5: size="    "+size+"    "
		if len(size)==6: size="   "+size+"   "
		if len(size)==7: size="  "+size+"  "
		if len(size)==8: size=" "+size+" "

		ss='<strong>'
		es='</strong>'
		seeds=mfindal(i, ss, es)[0][len(ss):]#.replace("</span></td>","").replace(chr(10),"").replace(chr(13),"").replace("\t","").replace(" ","")
		if len(seeds)==0: seeds="     ---    "
		if len(seeds)==1: seeds="      "+seeds+"     "
		if len(seeds)==2: seeds="     "+seeds+"    "
		if len(seeds)==3: seeds="    "+seeds+"   "
		if len(seeds)==4: seeds="   "+seeds+"   "
		if len(seeds)==5: seeds="   "+seeds+"   "
		if len(seeds)==6: seeds="   "+seeds+"  "
		seeds=seeds.replace('avi',' avi ')
		
		ss='checkLink('
		es=', &quot;/search&quot;)'
		try: link=mfindal(i, ss, es)[0][len(ss):]
		except: link=""
		
		if link<>"": 
			html=get_HTML('http://fileek.com/index.php?r=download/ajaxlinkcheck&id='+link+'&action=%2Fsearch&ismagnet=0')
			flink=eval(html.replace("\\/","/"))['link']
			L.append([seeds, size, title, flink])
			
	return L


class Tracker:
	def __init__(self):
		pass

	def Search(self, qury):
		q=qury.replace(" ","+")
		RL=[]
		for p in range (1,10):
			html=get_HTML('http://fileek.com/search/?q='+q+"&ft%5B%5D=movies&page="+str(p))
			L=csr(html)
			for i in L:
				if i not in RL: RL.append(i)
		return RL 