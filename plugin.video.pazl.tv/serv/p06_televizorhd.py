#!/usr/bin/python
# -*- coding: utf-8 -*-

import string, xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os, sys, cookielib, urllib, urllib2, time
addon = xbmcaddon.Addon(id='plugin.video.pazl.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.pazl.tv')
#-----------------------------------------

icon = ""
serv_id = '6'
siteUrl = 'televizorhd.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), siteUrl+'.sid')

cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
def fs_enc(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
    sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
    return path.decode(sys_enc).encode('utf-8')

from xid import *

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

def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

def get_idx(name):
	name=lower(name).replace(" #1","").replace(" #2","").replace(" #3","").replace(" #4","")
	try:
		id="x"+xmlid[name]
	except: 
		id=''
	return id

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
			try:
					http=getURL(url)
					ss='http://content.asplaylist.net'
					es='.acelive'
					try:t1=mfindal(http,ss,es)[0]+es
					except:t1=""
					srv=__settings__.getSetting("p2p_serv")
					prt=__settings__.getSetting("p2p_port")
					if 'content.asplaylist.net' in t1: t=['http://'+srv+':'+prt+'/ace/getstream?url='+t1,]
					else: t=[]
					return t
			except:
				return []

	def Canals(self):
		Logo = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logo'))
		import logodb
		Ldb=logodb.ttvlogo
		LL=[]
		url='http://televizorhd.ru'
		#pref='http://1ttv.net/iframe.php?site=1714&channel='
		http=getURL(url)
			
		ss='<li>'
		es='</li>'
		L=mfindal(http,ss,es)
		fdbc=False
		no_err=True
		for i in L:
			try:
			#if '"><div class="openPart">' in i:
				ss='<a href="'
				es='"><div class="openPart">'
				url=mfindal(i,ss,es)[0][len(ss):]
				#print url
				
				ss='<div class="openPart">'
				es='</div></a>'
				title=mfindal(i,ss,es)[0][len(ss):]
				try:
					title=title.decode('windows-1251')
					title=title.encode('utf-8')
				except: pass
					
				id = get_idx(title)
				if id=="":
					try:
						#print "-=======================================================-"
						#print "-------------------- нет ID канала в БД -----------------------"
						#print lower(title)
						#print "-------------------- поиск ID на сайте  -----------------------"
						#print url
						h=getURL(url)
						ss='http://1ttv.net/iframe.php?site=1714&channel='
						es='" rel="nofollow" width="100%" height="570"'
						id=mfindal(h,ss,es)[0][len(ss):]
						#print '"'+lower(title)+'":"ttv'+id+'"'
					except:
						#print "-------------------- ID на сайте не найден -----------------------"
						id=""
				if id!="":
					try:
						#print "-------------------- Поиск логотипа в БД по ID -------------------"
						img=Ldb[id]
						#print img
					except:
						#try:
						#	#print "------------ Логотип отсутствует в БД > Грузим с 1ttv ------------"
						#	u2='http://1ttv.net/iframe.php?site=2252&channel='+id
						#	tmp=getURL(u2)
						#	ss='http://torrent-tv.ru/uploads/'
						#	es='.png" style="vertical-align'
						#	img=mfindal(tmp,ss,es)[0]+'.png'
						#	#print '"'+id+'":"'+img+'"'
						#	Ldb[id]=img
						#	fdbc=True
						#	#print "-------------------- Логотип сохранен в БД -------------------------"
						#except:
							#print "---------------------- Ошибка поиска на 1ttv > ищем локально -----------------------"
							path = fs_enc(os.path.join(Logo, id.replace("xttv","")+'.png'))
							try: sz=os.path.getsize(path)
							except: sz=0
							if sz >0:
								img=path
							else:
								#try:
								#	h=getURL(url)
								#	ss='http://televizorhd.ru/uploads/posts'
								#	es='_1.png'
								#	img=mfindal(h,ss,es)[0]+es
								#except:
									#print "------------------! Логотип незвестен !-------------------------"
									#print url
									#print id
									#print lower(title)
									img="http://televizorhd.ru/templates/Server-Torrent-TV/dleimages/no_image.jpg"
					
				else:
					#print " --------------- ОШИБКА ЗАГРУЗКИ КАНАЛА ----------------- "
					#print i
					no_err=False
				if no_err: LL.append({'url':url, 'img':img, 'title':title+' #'+serv_id})
			except: 
				#print " --------------- ОШИБКА  ----------------- "
				#print i
				pass
				
		if fdbc:
			fp=xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'logodb.py'))
			fl = open(fp, "w")
			fl.write('# -*- coding: utf-8 -*-\n')
			fl.write('ttvlogo={\n')
			for i in Ldb.items():
				fl.write('"'+i[0]+'":"'+i[1]+'",\n')
			fl.write('}')
			fl.close()

		if LL!=[]:save_channels(serv_id, LL)
		else: showMessage('televizorhd.ru', 'Не удалось загрузить каналы', 3000)
		return LL
