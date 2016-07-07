#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, cookielib, urllib, urllib2, time
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')
#-----------------------------------------

icon = ""
serv_id = '7'
siteUrl = 'glaz.tv'
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
					L=[]
			#try:
					http=getURL(url)
					ss='param value="http://www.glaz.tv/uppod-hls2.swf?file='
					es='&aspect=" name='
					L1=mfindal(http,ss,es)
					for i in L1:
						uri=i[len(ss):]+"&aspect="
						if uri not in L: L.append(uri)
					
					#ss='<param value="http://www.glaz.tv/'
					#es='" name="movie"><embed height'
					#L1=mfindal(http,ss,es)
					#for i in L1:
						#print i
					#	if 'm3u8' in i:
					#		uri=i.replace('<param value="http://www.glaz.tv/','').replace('uppod-hls2.swf?file=','')
					#		if uri not in L: L.append(uri)
					#	else:
					#		ss='file='
					#		es='&type='
					#		cn=mfindal(i,ss,es)[0][len(ss):]
						
					#		ss='streamer='
					#		es='&autostart='
					#		urr=mfindal(i,ss,es)[0][len(ss):]
						
					#		uri=urr+cn
					#	if uri not in L: L.append(uri)
					
					ss='http://1ttv.net/'
					es="\\'  height=\\'"
					L1=mfindal(http,ss,es)
					for i in L1:
						uri=get_ttv(i)
						if uri not in L: L.append(uri)
					
					print L
					return L#['rtmp://stream.smcloud.net/live2/eskatv/eskatv_360p/playlist.m3u8',]
			#except:
			#	return []

	def Canals(self):
		LL=[]
		for n in range (1,9):
			url='http://www.glaz.tv/online-tv/'+str(n)+'/'
			http=getURL(url)
			ss='<td style="border-width:1px 0">'
			es='<strong>'
			L=mfindal(http,ss,es)
			
			for i in L:
				print i
				if "/online-tv/" in i and 'Вещание с других сайтов' not in i:
					
					ss='/online-tv/'
					es='"><img width="60"'
					url='http://www.glaz.tv'+mfindal(i,ss,es)[0]
					
					ss='src="'
					es='.gif'
					img='http://www.glaz.tv'+mfindal(i,ss,es)[0][len(ss):]+es
					
					ss='alt="'
					es='" style="'
					title=mfindal(i,ss,es)[0][len(ss):]
					
					LL.append({'url':url, 'img':img, 'title':title+" #"+serv_id})
					
		if LL!=[]:save_channels(serv_id, LL)
		else:showMessage('glaz.tv', 'Не удалось загрузить каналы', times = 3000)
				
		return LL
