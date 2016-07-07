#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, cookielib, urllib, urllib2, time
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')
#-----------------------------------------

icon = ""
serv_id = '5'
siteUrl = 'ok-tv.org'
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

def get_ttv(url):
		http=getURL(url)
		#print http
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
		try:
			L=[]
			try:
				
				http=getURL(url)
				#print http
				ss='frameborder="0" scrolling="no" src="'
				es='" bgcolor="#000000" allowtransparency="true"'
				pl=mfindal(http,ss,es)[0][len(ss):]
				#print pl
				
				http2=getURL(pl)
				#print http2
				ss='file='
				es='"></object>'
				st=mfindal(http2,ss,es)[0][len(ss):]
				#print st
				L=[st,]
			except: pass
				
			if True:#__settings__.getSetting("p2p-2")=='true':
				try:
					ss='http://1ttv.net'
					es='" width="660" height="450" bgcolor="#000000"'
					Lt=mfindal(http,ss,es)#[0]
					Lp2=[]
					for t in Lt:
						t=t.replace('site=1906','site=1714')
						trst=get_ttv(t)
						#print trst
						Lp2.append(trst)
					L.extend(Lp2)
				except: pass

			return L
				
		except:
			return []

	def Canals(self):
		LL=[]
		url='http://ok-tv.org'
		http=getURL(url)
		
		ss='<a target="_blank"'
		es='style="width:100px;"'
		L=mfindal(http,ss,es)
		
		for i in L:
			ss='href="'
			es='.html'
			url='http://ok-tv.org'+mfindal(i,ss,es)[0][len(ss):]+es
		
			ss='src="'
			es='" alt="'
			img='http://ok-tv.org'+mfindal(i,ss,es)[0][len(ss):]

			ss='title="'
			es='" href'
			title=mfindal(i,ss,es)[0][len(ss):]
			#try: title=title.decode('windows-1251')
			#except:pass
			try: title=title.encode('utf-8')
			except:pass
			#print title
			title=title.replace('смотреть','').replace('Cмотреть','').replace('онлайн','').replace('прямой эфир','').replace('прямо эфир','').replace('прямую трансляцию','').replace('бесплатно','').strip()
			title=title.replace('\xd0\xa1\xd0\xbc\xd0\xbe\xd1\x82\xd1\x80\xd0\xb5\xd1\x82\xd1\x8c','').strip()
			
			LL.append({'url':url, 'img':img, 'title':title+" #"+serv_id})
			
		if LL!=[]:save_channels(serv_id, LL)
		else:showMessage('ok-tv.org', 'Не удалось загрузить каналы', times = 3000)
		
		return LL
