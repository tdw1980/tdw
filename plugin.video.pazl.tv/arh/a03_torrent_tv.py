#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, cookielib, urllib, urllib2, time
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')
#-----------------------------------------

icon = ""
serv_id = '3'
siteUrl = 'Torrent-tv.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def unmark(nm):
	for i in range (0,20):
		nm=nm.replace(" #"+str(i),"")
	return nm

def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

def getURL(url, Referer = httpSiteUrl):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L


def save_aid(ns, d):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'aid'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('n2id=')
		fl.write(repr(d))
		fl.close()

def get_ttv(url):
		print url
		http=getURL(url)
		print http
		ss1='this.loadPlayer("'
		ss2='this.loadTorrent("'
		es='",{autoplay: true})'
		srv=__settings__.getSetting("p2p_serv")
		prt=__settings__.getSetting("p2p_port")
		
		try:
			if ss1 in http:
				CID=mfindal(http,ss1,es)[0][len(ss1):]
				lnk='http://'+srv+':'+prt+'/ace/getstream?id='+CID
				if len(CID)<30:lnk=''
				return lnk
			elif ss2 in http:
				AL=mfindal(http,ss2,es)[0][len(ss2):]
				lnk='http://'+srv+':'+prt+'/ace/getstream?url='+AL
				if len(AL)<30:lnk=''
				return lnk
			else: return ""
		except:
			return ""

class ARH:
	def __init__(self):
		pass

	def Streams(self, url):
		try:
			trst=get_ttv(url)
			if trst=="":return []
			else:return [trst,]
		except:
			return []

	def Archive(self, id, t):
		dt=time.strftime('-%d-%m-%Y',t).replace('-0','-')[1:]
		url='http://torrent-tv.ru/tv-archive-channel.php?channel='+id+'&data='+dt#12-7-2016
		http=getURL(url)
		ss='<p style="font: normal 12px sans-serif; line-height: 1;">'
		es='<br />'
		L=mfindal(http,ss,es)
		LL=[]
		for i in L:
			
			try:
				i=i.replace(chr(10),"").replace(chr(13),"").replace('<p style="font: normal 12px sans-serif; line-height: 1;">', '')
				#print i
				ss='<strong>'
				es=' &ndash;'
				tm=mfindal(i,ss,es)[0][len(ss):].strip()
				print tm
				
				ss='">'
				es='</a></p>'
				title=mfindal(i,ss,es)[0][len(ss):].strip()
				print title
				
				ss='href="'
				es='">'
				uri='http://torrent-tv.ru/'+mfindal(i,ss,es)[0][len(ss):]+'&noflash'
				print uri
				
				LL.append({'url':uri, 'title':title, 'time':tm})
			except: pass
		return LL

	def name2id(self):
		url='http://torrent-tv.ru/tv-archive.php'
		http=getURL(url)
		ss='<option value='
		es='</option>'
		L=mfindal(http,ss,es)
		d={}
		for i in L:
			#try:
				i=i.replace('<option value=','').replace(' disabled selected','')
				j = eval("("+i.replace('">', '", "')+'")')
				i1 = j[0]
				i2 = lower(unmark(j[1]))
				#print i
				d[i2] = i1
			#except: pass
		save_aid('3', d)
		return d