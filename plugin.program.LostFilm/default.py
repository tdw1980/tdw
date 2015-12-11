#!/usr/bin/python
# -*- coding: utf-8 -*-

# *      Copyright (C) 2011 TDW

import time
import httplib
import urllib
import urllib2
import re
import sys
import os
import Cookie


import string, xbmc, xbmcgui, xbmcplugin, os, urllib, cookielib, xbmcaddon, time, codecs

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import socket
socket.setdefaulttimeout(50)
try:
	import krasfs
	tft=krasfs.Tracker()
except: pass
	
siteUrl = 'www.lostfilm.tv'
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'plugin.video.LostFilm.cookies.sid')

#h = int(sys.argv[1])
#handle = int(sys.argv[1])

PLUGIN_NAME   = 'LostFilm'

addon = xbmcaddon.Addon(id='plugin.video.LostFilm')
__settings__ = xbmcaddon.Addon(id='plugin.video.LostFilm')
CT = __settings__.getSetting("ConType")
if CT=="0": httpSiteUrl = 'http://' + siteUrl
else:httpSiteUrl = 'https://' + siteUrl
#xbmcplugin.setContent(int(sys.argv[1]), 'movies')

icon = os.path.join(addon.getAddonInfo('path'), 'icon.png')
thumb = os.path.join( addon.getAddonInfo('path'), "icon.png" )
fanart = os.path.join( addon.getAddonInfo('path'), "fanart.jpg" )
LstDir = os.path.join( addon.getAddonInfo('path'), "playlists" )
dbDir = os.path.join( addon.getAddonInfo('path'), "db" )
ImgPath = os.path.join( addon.getAddonInfo('path'), "logo" )
playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)


headers  = {
	'User-Agent' : 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.7.62 Version/11.00',
	'Accept'     :' text/html, application/xml, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*',
	'Accept-Language':'ru-RU,ru;q=0.9,en;q=0.8',
	'Accept-Charset' :'utf-8, utf-16, *;q=0.1',
	'Accept-Encoding':'identity, *;q=0'
}

headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
	'Host' : 'vkontakte.ru',
	'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
	'Connection' : 'close',
}

def GET_off(target, referer, post=None):
	try:
		req = urllib2.Request(url = target, data = post)
		req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
		resp = urllib2.urlopen(req)
		http = resp.read()
		resp.close()
		return http
	except Exception, e:
		#xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
		showMessage('HTTP ERROR', e, 5000)


def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

import re, os, urllib, urllib2, cookielib, time, sys
from time import gmtime, strftime
import urlparse

fcookies = os.path.join(addon.getAddonInfo('path'), r'cookies.txt')

sys.path.append(os.path.join(addon.getAddonInfo('path'), r'resources', r'lib'))
from BeautifulSoup  import BeautifulSoup

import HTMLParser
hpar = HTMLParser.HTMLParser()

#---------- get web page -------------------------------------------------------
def get_HTML(url, post = None, ref = None, get_redirect = False):
    if url.find('http')<0 :
        if CT=="0": url='http:'+url
        else: url='https:'+url
    #url="http://translate.googleusercontent.com/translate_c?u="+url
    request = urllib2.Request(url, post)

    host = urlparse.urlsplit(url).hostname
    if ref==None:
        try:
           ref='http://'+host
        except:
            ref='localhost'

    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
    request.add_header('Host',   host)
    request.add_header('Accept', 'text/html, application/xhtml+xml, */*')
    request.add_header('Accept-Language', 'ru-RU')
    request.add_header('Referer',             ref)
    request.add_header('Content-Type','application/x-www-form-urlencoded')

    try:
        f = urllib2.urlopen(request)
    except IOError, e:
        if hasattr(e, 'reason'):
           print('We failed to reach a server.')
        elif hasattr(e, 'code'):
           print('The server couldn\'t fulfill the request.')
        return 'We failed to reach a server.'

    if get_redirect == True:
        html = f.geturl()
    else:
        html = f.read()

    return html

#-------------------------------------------------------------------------------
# get cookies from last session
cj = cookielib.FileCookieJar(fcookies)
hr  = urllib2.HTTPCookieProcessor(cj)
if __settings__.getSetting("immunicity") == "1": 
	import antizapret
	opener = urllib2.build_opener(antizapret.AntizapretProxyHandler(), hr)
	print "Immunicity"
elif __settings__.getSetting("immunicity") == "2": 
	prx=__settings__.getSetting("Proxy")
	if prx.find('http')<0 : prx="http://"+prx
	proxy_support = urllib2.ProxyHandler({"http" : prx})
	#proxy_support = urllib2.ProxyHandler({"http" : "http://n17-03-01.opera-mini.net:443"})
	opener = urllib2.build_opener(proxy_support, hr)
	print "Proxy "+__settings__.getSetting("Proxy")
else: 
	opener = urllib2.build_opener(hr)
	print "NO Proxy"
urllib2.install_opener(opener)

#----------- LOGIN to lostfilm.tv ----------------------------------------------
#-- step 1

url1 = 'http://login1.bogi.ru/login.php?referer=http%3A%2F%2Fwww.lostfilm.tv%2F'

#-- enter your login/pass
login = __settings__.getSetting("login")
passw = __settings__.getSetting("password")
if login =="" or passw == '': showMessage('lostfilm', "Проверьте логин и пароль", times = 50000)

values = {
				'login'     : login,
				'password'  : passw,
				'module'    : 1,
				'target'    : 'http://lostfilm.tv/',
				'repage'    : 'user',
				'act'       : 'login'
		}





def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def format_s(s):
	s=str(repr(s))[1:-1]
	s=s.replace('\\xb8','ё')
	s=s.replace('\\xe0','a')
	s=s.replace('\\xe1','б')
	s=s.replace('\\xe2','в')
	s=s.replace('\\xe3','г')
	s=s.replace('\\xe4','д')
	s=s.replace('\\xe5','е')
	s=s.replace('\\xe6','ж')
	s=s.replace('\\xe7','з')
	s=s.replace('\\xe8','и')
	s=s.replace('\\xe9','й')
	s=s.replace('\\xea','к')
	s=s.replace('\\xeb','л')
	s=s.replace('\\xec','м')
	s=s.replace('\\xed','н')
	s=s.replace('\\xee','о')
	s=s.replace('\\xef','п')
	s=s.replace('\\xf0','р')
	s=s.replace('\\xf1','с')
	s=s.replace('\\xf2','т')
	s=s.replace('\\xf3','у')
	s=s.replace('\\xf4','ф')
	s=s.replace('\\xf5','х')
	s=s.replace('\\xf6','ц')
	s=s.replace('\\xf7','ч')
	s=s.replace('\\xf8','ш')
	s=s.replace('\\xf9','щ')
	s=s.replace('\\xfa','ъ')
	s=s.replace('\\xfb','ы')
	s=s.replace('\\xfc','ь')
	s=s.replace('\\xfd','э')
	s=s.replace('\\xfe','ю')
	s=s.replace('\\xff','я')

	s=s.replace('\\xc0','А')
	s=s.replace('\\xc1','Б')
	s=s.replace('\\xc2','В')
	s=s.replace('\\xc3','Г')
	s=s.replace('\\xc4','Д')
	s=s.replace('\\xc5','Е')
	s=s.replace('\\xc6','Ж')
	s=s.replace('\\xc7','З')
	s=s.replace('\\xc8','И')
	s=s.replace('\\xc9','Й')
	s=s.replace('\\xca','К')
	s=s.replace('\\xcb','Л')
	s=s.replace('\\xcc','М')
	s=s.replace('\\xcd','Н')
	s=s.replace('\\xce','О')
	s=s.replace('\\xcf','П')
	s=s.replace('\\xd0','Р')
	s=s.replace('\\xd1','С')
	s=s.replace('\\xd2','Т')
	s=s.replace('\\xd3','У')
	s=s.replace('\\xd4','Ф')
	s=s.replace('\\xd5','Х')
	s=s.replace('\\xd6','Ц')
	s=s.replace('\\xd7','Ч')
	s=s.replace('\\xd8','Ш')
	s=s.replace('\\xd9','Щ')
	s=s.replace('\\xda','Ъ')
	s=s.replace('\\xdb','Ы')
	s=s.replace('\\xdc','Ь')
	s=s.replace('\\xdd','Э')
	s=s.replace('\\xde','Ю')
	s=s.replace('\\xdf','Я')
	
	s=s.replace('\\xab','"')
	s=s.replace('\\xbb','"')
	s=s.replace('\\r','')
	s=s.replace('\\n','\n')
	s=s.replace('\\t','\t')
	s=s.replace("\\x97",'-')
	
	return s



def Alln2(h):
	kc=h.find('span class="d_pages_link_selected"')
	nc=h.find('div class="content_head"')
	h=h[nc:kc].replace('\r','').replace('\n','').replace('\t','')
	s='font-size:18px;color:#000000'
	e='float:right;font-family:arial;'
	l=mfindal(h,s,e)[1:]
	LL=[]
	for i in l:
		s='//-->'
		e='</div>'
		n1=mfindal(i,s,e)[0][len(s):]
		
		s='font-size:14px;color:#000000">'
		e='</span>'
		n2=mfindal(i,s,e)[0][len(s):]
		
		s='<a href="/browse.php?cat='
		e='"><img src="/Static'
		n3=mfindal(i,s,e)[0][len(s):]
		
		s='<img src="/Static/icons/'
		e='" alt="'
		n4=mfindal(i,s,e)[0][len(s):]
		
		s='<span class="torrent_title"><b>'
		e='</b></span><br />'
		n5=mfindal(i,s,e)[0][len(s):]
		
		s='howAllReleases'
		e='"></a><br clear=both>'
		try:
			n6=mfindal(i,s,e)[0][len(s):]
		except:
			e='"></a></div><br clear=both>'
			n6=mfindal(i,s,e)[0][len(s):]
		#print n6
		LL.append([n1,n2,n3,n4,n5,n6])
	return LL

import SelectBox
def select(L):#,type, path
	addon.setSetting(id="id_params", value=repr(L))
	SelectBox.run("w1")
	#return addon.getSetting("w1")

def GET_N2():
	categoryUrl = xt(httpSiteUrl + '/browse.php')
	http =  get_HTML(categoryUrl)
	if http == None:
		showMessage('lostfilm:', 'Сервер не отвечает', 1000)
		return None
	else:
		
		L=Alln2(http)
		#debug(http)
		LN=[]
		for i in L:
			#nm=i[2].lower()
			Title = format_s(i[0]+" [B][COLOR FFFFFFFF]"+i[1]+":[/COLOR][/B] "+i[4])
			row_url = i[2]
			sn = i[5]
			dict=get_minfo(row_url)
			try:
				cover="http://www.lostfilm.tv/Static/icons/"+i[3]#dict["cover"]
				if CT=="1": cover.replace('http:','https:')
				if __settings__.getSetting("Picture") == "true": cover=GETimg(cover)
			except:cover=""
			
			try:
				if sn in eval(__settings__.getSetting("History")): 
					how=1
				else:
					how=0
			except:
				how=0
			
			purl = 'plugin://plugin.video.LostFilm/?mode=OpenRel'\
				+ '&url=' + urllib.quote_plus(sn)\
				+ '&title=' + urllib.quote_plus(Title)\
				+ '&text=' + urllib.quote_plus('0')
			LN.append([Title,cover, i[0],format_s(i[1]),format_s(i[4]), how, urllib.quote_plus(sn), purl])
			
	return LN

p = re.compile(r'<.*?>')

def clearinfo2(http):
	n=http.find("window.open('/rdr.php?c=")
	k=http.rfind('</span>\n</div>\n<div>')
	http=xt(http[n:k])
	s='Год выхода:'
	e='Страна: '
	l=mfindal(http, ss, es)
	

def clearinfo(str):
	n=str.find("window.open('/rdr.php?c=")
	k=str.rfind('t_row even')
	k=str.rfind('</span>\n</div>\n<div>')
	str=xt(str[n:k])
	str=format_s(str)
	
	#str=str.replace(chr(13)+chr(10),chr(10))
	#str=str.replace(chr(10)+chr(13),chr(10))
	str=str.replace(chr(13),chr(10))
	str=str.replace(chr(10),'')
	str=str.replace('\t','')
	str=str.replace("'",'"')
	str=str.replace('" alt="" title',chr(10))
	str=str.replace('Год выходa:',chr(10)+"Год выхода:")
	str=str.replace('О сериале ( About',"")
	str=str.replace('О сериaле',chr(10)+"Описание:")
	str=str.replace('</h1><br /><img src="',chr(10)+"Обложка:")
	str=str.replace('<span>',"")
	str=str.replace('</span>',"")
	str=str.replace("<br />",chr(10))
	str=str.replace("</h2></div></div>"," ")
	
	str=str.replace('</script><div><h1>',chr(10)+"Название:")
	str=str.replace('Жaнр:',chr(10)+"Жанр:")
	str=str.replace('Режиссер:',chr(10)+"Режиссер:")
	str=str.replace('Страна:',chr(10)+"Страна:")
	
	str=p.sub('', str)
	
	str=str.replace(chr(10)+chr(10)+chr(10),chr(10))
	str=str.replace(chr(10)+chr(10),chr(10))
	str=str.replace('   ',' ')
	str=str.replace('  ',' ')
	str=str.replace('О фильме:'+chr(10), chr(10)+'О фильме: ')
	str=str.replace('О фильме: '+chr(10), chr(10)+'О фильме: ')
	str=str.replace('Описание:'+chr(10), chr(10)+'Описание: ')
	str=str.replace('Описание: '+chr(10), chr(10)+'Описание: ')
	str=str.replace('Оценка',chr(10)+"Оценка: ")
	str=str.replace('.jpg', ".jpg"+chr(10))
	str=str.replace('.jpeg', ".jpeg"+chr(10))
	str=str.replace('.png', ".png"+chr(10))
	#debug(str)
	return str


import sqlite3 as db
db_name = os.path.join( addon.getAddonInfo('path').replace("plugin.program.LostFilm","plugin.video.LostFilm"), "move_info.db" )
c = db.connect(database=db_name)
cu = c.cursor()

def get_minfo(ntor):
			
			try: dict=eval(xt(get_inf_db(ntor)[0][0]))#dbi = move_info_db[ntor]
			except: #dbi = None
				#print get_inf_db(ntor)
				#debug (eval(get_inf_db(ntor)[0][0]))
			#if dbi == None:
				hp =  get_HTML(httpSiteUrl + '/browse.php?cat='+ntor)
				
				hp=clearinfo(hp)
				#if ntor=="119":print hp
				LI=hp.splitlines()
				
				
				dict={}
				cover=''
				jjk=""
				for itm in LI:
					#print itm
					nc=itm.find(':')
					flag=itm[:nc]
					if flag=='Обложка': 
						cvr=itm.strip()
						cover=httpSiteUrl + itm[nc+1:].strip()
						dict['cover']=cover
						#print cover
					elif flag=='Название': dict['title']=itm[nc+1:].strip().replace("&#960;",'п').replace('\\"','`').replace("'",'`').replace('"',"``").replace('\\x96',"-").replace('\\x85',"...")
					elif flag=='Оценка': 
						nr=itm.find('из')
						try:
							dict['rating']=float(itm[nc+2:nr])
							#dict['votes']=str(int(int(itm[nc+2:nr])/2))
						except: pass
					elif flag=='Год выхода':
						try:dict['year']=int(itm.strip()[nc+1:])
						except: 
							try:dict['year']=int(itm.strip()[nc+1:nc+6])
							except: pass
					elif flag=='Жанр': dict['genre']=xt(itm[nc+1:].strip())
					#elif flag=='Режиссер': dict['director']=itm[nc+1:].strip()
					#elif flag=='В ролях': 
					#	dict['cast']=itm[nc+1:].split(",")[:6]
					elif flag=='О фильме' or flag=='Описание':
						if jjk=="": jjk=itm[nc+1:].strip().replace('\\"','`').replace("'",'`').replace('"',"``").replace('\\x96',"-").replace("&#960;",'п').replace('\\x85',"...")
						#debug (jjk)#[:10]
						
						dict['plot']=jjk#[1:-1]
						
				#move_info_db[ntor]=dict
				#add_to_db(ntor, repr(dict))
				try: 
					if cover <> "": #
						add_to_db(ntor, repr(dict))
						#print dict
				except: pass
					#try:add_to_db(ntor, repr(dict).replace('"',"'"))
					#except: pass

			return dict


select(GET_N2())

c.close()