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

def get_ttv(url):
		#print url
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

def dload_epg_xml():
	#try:
			target='http://api.torrent-tv.ru/ttv.xmltv.xml.gz'
			#print "-==-=-=-=-=-=-=- download =-=-=-=-=-=-=-=-=-=-"
			fp = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'tmp.zip'))
			
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			#print "-==-=-=-=-=-=-=- unpak =-=-=-=-=-=-=-=-=-=-"
			xml=ungz(fp)
			#print "-==-=-=-=-=-=-=- unpak ok =-=-=-=-=-=-=-=-=-=-"
			#os.remove(fp)
			return xml[:120000]
	#except Exception, e:
	#		print 'HTTP ERROR ' + str(e)
	#		return ''

def ungz(filename):
	import gzip
	with gzip.open(filename, 'rb') as f:
		file_content = f.read()
		return file_content

def save_channels(ns, L):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'Channels'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('Channels=[\n')
		for i in L:
			fl.write(repr(i)+',\n')
		fl.write(']\n')
		fl.close()

def save_aid(ns, d):
		fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'aid'+ns+'.py'))
		fl = open(fp, "w")
		fl.write('# -*- coding: utf-8 -*-\n')
		fl.write('n2id=')
		fl.write(repr(d))
		fl.close()


class PZL:
	def __init__(self):
		pass

	def Streams(self, url):
		try:
			trst=get_ttv(url)
			if trst=="":return []
			else:return [trst,]
		except:
			return []

	def Canals(self):
		import cnl
		import logodb
		Ldb=logodb.ttvlogo
		LL=[]
		Lu=[]
		for i in cnl.ttvcnl:
			LL.append({'url':i['url'], 'img':i['img'], 'title':i['title']+" #"+serv_id})
			Lu.append(i['url'])
		pref='http://1ttv.net/iframe.php?site=1714&channel='
		xml=dload_epg_xml()
		n=xml.find('<channel id')
		k=xml.find('<programme ')
		xml=xml[n:k]
		xml=xml.replace(chr(10),"").replace(chr(13),"").replace("<channel id", "\n<channel id")
		L=xml.splitlines()
		#debug (xml)
		#LL=[]
		fdbc=False
		for i in L:
			if 'id="ttv' in i:
				try:
					ss='id="ttv'
					es='"><display-name lang="ru">'
					id=mfindal(i,ss,es)[0][len(ss):]
					url=pref+id
					if url not in Lu:
						Lu.append(url)
						#print url
						ss='<display-name lang="ru">'
						es='</display-name>'
						title=mfindal(i,ss,es)[0][len(ss):]
						#print title
						
						try:
							img=Ldb[id]
						except:
							print "################ Логотип отсутствует в БД #################"
							print url
							tmp=getURL(url)
							ss='http://torrent-tv.ru/uploads/'
							es='.png" style="vertical-align'
							img=mfindal(tmp,ss,es)[0]+'.png'
							print '"'+id+'":"'+img+'"'
							Ldb[id]=img
							fdbc=True
							print "################ Логотип сохранен в БД #################"
						
						LL.append({'url':url, 'img':img, 'title':title+" #"+serv_id})
				except:
						pass
						print "!_!_!_!_!_!_!_!_ Ошибка получения канала TTB !_!_!_!_!_!_!_!_"
						print i
						print "!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_!_"
		if fdbc:
			fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logodb.py'))
			fl = open(fp, "w")
			fl.write('# -*- coding: utf-8 -*-\n')
			fl.write('ttvlogo={\n')
			for i in Ldb.items():
				fl.write('"'+i[0]+'":"'+i[1]+'",\n')
			fl.write('}')
			fl.close()

		if LL!=[]: save_channels(serv_id, LL)
		else: showMessage('torrent-tv.ru', 'Не удалось загрузить каналы', times = 3000)

		return LL

	def Archive(self, id, dt):
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
				#print tm
				
				ss='">'
				es='</a></p>'
				title=mfindal(i,ss,es)[0][len(ss):].strip()
				#print title
				
				ss='href="'
				es='">'
				uri='http://torrent-tv.ru/'+mfindal(i,ss,es)[0][len(ss):]+'&noflash'
				#print uri
				
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