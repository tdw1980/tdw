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
siteUrl = 'dugtor.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'dugtor.cookies.sid')
 
cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def rulower(str):
	str=str.strip()
	str=xt(str).lower()
	str=str.replace('Й','й')
	str=str.replace('Ц','ц')
	str=str.replace('У','у')
	str=str.replace('К','к')
	str=str.replace('Е','е')
	str=str.replace('Н','н')
	str=str.replace('Г','г')
	str=str.replace('Ш','ш')
	str=str.replace('Щ','щ')
	str=str.replace('З','з')
	str=str.replace('Х','х')
	str=str.replace('Ъ','ъ')
	str=str.replace('Ф','ф')
	str=str.replace('Ы','ы')
	str=str.replace('В','в')
	str=str.replace('А','а')
	str=str.replace('П','п')
	str=str.replace('Р','р')
	str=str.replace('О','о')
	str=str.replace('Л','л')
	str=str.replace('Д','д')
	str=str.replace('Ж','ж')
	str=str.replace('Э','э')
	str=str.replace('Я','я')
	str=str.replace('Ч','ч')
	str=str.replace('С','с')
	str=str.replace('М','м')
	str=str.replace('И','и')
	str=str.replace('Т','т')
	str=str.replace('Ь','ь')
	str=str.replace('Б','б')
	str=str.replace('Ю','ю')
	return str


def GET(target, referer, post=None):
	#print target
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		print e



def upd(text):
	SUrl='http://dugtor.ru/engine/modules/search-torrents/search.php'
	Post='search_ok=go_search&static=off&fraza='+text#{"fraza":text, "search_ok":"go_search", "static":"off"}
	
	http = GET(SUrl, httpSiteUrl, Post)
	if http == None:
		print'dugtor.ru: Сервер не отвечает'
		return None
	else:
		LL=formtext(http)
		return LL

def cp1251(x):
	L=list(x)
	s=""
	for i in L:
		try:s+=i.decode('cp1251')
		except: pass
	return s

def mid1 (x):
	d=10-len(x)
	p=" "*d
	r= p+ x +p
	return r

def formtext(http):
	http=http.replace(chr(10),"").replace(chr(13),"").replace("\t","")
	ss="<td><b>"
	es="</tr><tr>"
	L=mfindal(http, ss, es)
	LL=[]
	for i in L:
		#print i
		ss="<td><b>"
		es="</b></td>"
		title=mfindal(i, ss, es)[0][len(ss):]
		#print title
		
		ss='</b></td><td style="text-align:center;">'
		es='<a href="/search-torrents'
		tmp=mfindal(i, ss, es)[0][len(ss):]
		
		tmp=tmp.replace('</td><td style="text-align:center;">', '","')
		l2=eval('["'+tmp+'0"]')
		size=l2[0].strip().center(11)
		sids=l2[1].strip().center(8-len(l2[1].strip()))
		
		ss='href="/search-torrents/download/'
		es='"><img src="/templates/primary/search-torrents/images/download'
		url='http://dugtor.ru/search-torrents/download/'+mfindal(i, ss, es)[0][len(ss):]+"/start"
		#print url
		try:LL.append([sids,size,title.decode('cp1251'),url])
		except:LL.append([sids,size,cp1251(title),url])
	return LL


class Tracker:
	def __init__(self):
		pass

	def Search(self, text="миля", category=0):
		Lout=upd(text)
		return Lout