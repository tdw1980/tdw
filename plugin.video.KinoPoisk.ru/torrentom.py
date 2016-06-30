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
siteUrl = 'torrentom.com'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'torrentom.cookies.sid')
 
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

def formatKP(str):
	str=str.strip()
	str=str.replace('%','%25')
	str=str.replace('&','%26')
	str=str.replace('?','%3F')
	str=str.replace('&','%26')
	str=str.replace('!','%21')
	str=str.replace(':','%3A')
	str=str.replace('#','%23')
	str=str.replace(',','%2C')
	str=str.replace(';','%3B')
	str=str.replace('@','%40')
	str=str.replace('(','%28')
	str=str.replace(')','%29')
	str=str.replace('"','%22')
	
	str=str.replace('а','%E0')
	str=str.replace('б','%E1')
	str=str.replace('в','%E2')
	str=str.replace('г','%E3')
	str=str.replace('д','%E4')
	str=str.replace('е','%E5')
	str=str.replace('ё','%b8')
	str=str.replace('ж','%E6')
	str=str.replace('з','%E7')
	str=str.replace('и','%E8')
	str=str.replace('й','%E9')
	str=str.replace('к','%EA')
	str=str.replace('л','%EB')
	str=str.replace('м','%EC')
	str=str.replace('н','%ED')
	str=str.replace('о','%EE')
	str=str.replace('п','%EF')
	str=str.replace('р','%F0')
	str=str.replace('с','%F1')
	str=str.replace('т','%F2')
	str=str.replace('у','%F3')
	str=str.replace('ф','%F4')
	str=str.replace('х','%F5')
	str=str.replace('ц','%F6')
	str=str.replace('ч','%F7')
	str=str.replace('ш','%F8')
	str=str.replace('щ','%F9')
	str=str.replace('ъ','%FA')
	str=str.replace('ы','%FB')
	str=str.replace('ь','%FC')
	str=str.replace('э','%FD')
	str=str.replace('ю','%FE')
	str=str.replace('я','%FF')
	
	str=str.replace('А','%C0')
	str=str.replace('Б','%C1')
	str=str.replace('В','%C2')
	str=str.replace('Г','%C3')
	str=str.replace('Д','%C4')
	str=str.replace('Е','%C5')
	str=str.replace('Ё','%A8')
	str=str.replace('Ж','%C6')
	str=str.replace('З','%C7')
	str=str.replace('И','%C8')
	str=str.replace('Й','%C9')
	str=str.replace('К','%CA')
	str=str.replace('Л','%CB')
	str=str.replace('М','%CC')
	str=str.replace('Н','%CD')
	str=str.replace('О','%CE')
	str=str.replace('П','%CF')
	str=str.replace('Р','%D0')
	str=str.replace('С','%D1')
	str=str.replace('Т','%D2')
	str=str.replace('У','%D3')
	str=str.replace('Ф','%D4')
	str=str.replace('Х','%D5')
	str=str.replace('Ц','%D6')
	str=str.replace('Ч','%D7')
	str=str.replace('Ш','%D8')
	str=str.replace('Щ','%D9')
	str=str.replace('Ь','%DA')
	str=str.replace('Ы','%DB')
	str=str.replace('Ъ','%DC')
	str=str.replace('Э','%DD')
	str=str.replace('Ю','%DE')
	str=str.replace('Я','%DF')

	str=str.replace(' ','+')
	return str

def upd(text):
	#SUrl='http://dugtor.ru/engine/modules/search-torrents/search.php'
	#Post='search_ok=go_search&static=off&fraza='+text#{"fraza":text, "search_ok":"go_search", "static":"off"}
	SUrl='http://torrentom.com/torrentz/search/'+formatKP(text)+"/"#'%D2%E5%F0%EC%E8%ED%E0%F2%EE%F0'
	print SUrl
	http = GET(SUrl, httpSiteUrl)#, Post)
	if http == None:
		print 'torrentom: Сервер не отвечает'
		return []
	else:
		L=formtext(http)
		i=L[0]
		#for i in L:
		http2 = GET(i[1], httpSiteUrl)
		LL=formtext2(http2, i[0])
		#print LL
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
	#print http
	http=http.replace(chr(10),"").replace(chr(13),"").replace("\t","")
	ss='<td class="colhead" colspan="2" align="center">'
	es='class="rate_widget">'
	L=mfindal(http, ss, es)
	
	LL=[]
	for i in L:
		print i
		ss=' href="'
		es='.htm" alt="'
		url='http://torrentom.com'+mfindal(i, ss, es)[0][len(ss):]+".htm"
		print url
		
		ss='"><b>'
		es='</b></a>'
		title=mfindal(i, ss, es)[0][len(ss):]
		print title
		LL.append([title.decode('cp1251'),url])
	return LL

def formtext2(http, title):
	#print http
	http=http.replace(chr(10),"").replace(chr(13),"").replace("\t","")
	ss='width=12 height=12 align=absmiddle src="/pic/arrow_right.png"'
	es='border="0" align=center cellspacing=0 cellpadding=6>'
	L=mfindal(http, ss, es)
	
	LL=[]
	for i in L:
		#print i
		#ss="<strong>"
		#es="</strong>"
		#title=mfindal(i, ss, es)[0][len(ss):]
		#print title
		
		ss='<td>'
		es='<td align=center>'
		size=mfindal(i, ss, es)[0][len(ss):].replace('</td>','')
		size=size.strip().center(11)
		
		ss='" />'
		es='</span><br>'
		sids=mfindal(i, ss, es)[0][len(ss):].strip()
		sids=sids.decode('cp1251')
		sids=sids.center(18-len(sids))
		#tmp=tmp.replace('</td><td style="text-align:center;">', '","')
		#l2=eval('["'+tmp+'0"]')
		#size='l2[0].strip().center(11)'
		#sids='l2[1].strip().center(8-len(l2[1].strip()))'
		
		ss='<a rel="nofollow" href="'
		es='"><img align=absmiddle border=0'
		url='http://torrentom.com'+mfindal(i, ss, es)[0][len(ss):]#+"/start"
		#print url
		LL.append([sids,size,title,url])
	return LL


class Tracker:
	def __init__(self):
		pass

	def Search(self, text="миля", category=0):
		Lout=upd(text)
		return Lout