#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, cookielib, urllib, urllib2, time
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')
#-----------------------------------------

icon = ""
serv_id = '1'
siteUrl = 'peers.tv'
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

def save_channels(n, L):
		ns=str(n)
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()

class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		if 'peers.tv' in url:
			try:
				url1=urllib.unquote_plus(url)+'|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0'
				url2=urllib.unquote_plus(url.replace('/126/','/16/'))+ '|User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:35.0) Gecko/20100101 Firefox/35.0'
				return [url1, url2]
			except:
				return []

	def Canals(self):
			LL=[]
			url='http://api.peers.tv/peerstv/2/'
			http=getURL(url)
			
			ss='<track>'
			es='</track>'
			L=mfindal(http,ss,es)
			
			for i in L:
				ss='<location>'
				es='</location>'
				url=mfindal(i,ss,es)[0][len(ss):]
				
				ss='<image>'
				es='</image>'
				img=mfindal(i,ss,es)[0][len(ss):]
				
				ss='<title>'
				es='</title>'
				title=mfindal(i,ss,es)[0][len(ss):]
				
				LL.append({'url':url, 'img':img, 'title':title+" #"+serv_id})
				
			if LL!=[]:save_channels(serv_id, LL)
			else:showMessage('peers.tv', 'Не удалось загрузить каналы', times = 3000)
			
			return LL
