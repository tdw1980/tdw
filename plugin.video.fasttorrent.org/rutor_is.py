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
siteUrl = 'rutor.in'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'rutor.cookies.sid')
 
cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
import antizapret
#antizapret.config_add(siteUrl)
opener = urllib2.build_opener(antizapret.AntizapretProxyHandler(), hr)
urllib2.install_opener(opener) 


def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


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
	text=text.replace(" ", "%20")
	categoryUrl = 'http://rutor.in/search.php?sr=topics&sf=titleonly&fp=1&tracker_search=torrent&keywords='+text
	http = GET(categoryUrl, httpSiteUrl, None)
	if http == None:
		print'RuTor: Сервер не отвечает'
		return None
	else:
		
		LL=formtext(http)
		return LL

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def formtext(http):
	http=http.replace(chr(10),"").replace('\t',"")
	
	ss='<tr valign="middle" class="col_line">'
	es='span class="my_tt complet" title='
	L = mfindal(http, ss, es)
	Lout=[]
	for i in L:
		try:
			#print i
			ss='style="white-space:nowrap;width:100px;">'
			es='</td><td class="row'
			data=mfindal(i, ss, es)[0][len(ss):]
			#print data
		
			ss='href="./download/file.php?id='
			es='&amp;sid='
			id=mfindal(i, ss, es)[0][len(ss):]
			#print id
			url='http://rutor.in/download/file.php?id='+id
			
			ss='" class="topictitle">'
			es='</a> </td><td class="row'
			title=mfindal(i, ss, es)[0][len(ss):].replace("&quot;",'"')
			#print title
	
			ss='<span title="Размер">'
			es='</p></td><!--<td class'
			size=mfindal(i, ss, es)[0][len(ss):].replace('&nbsp;','')
			#print size
			nnn=size.find('.')
			if nnn>2:size=size[:nnn]+size[nnn+3:]
				
			if len(size)==4:size=size.center(14)
			elif len(size)==5:size=size.center(12)
			elif len(size)==6:size=size.center(10)
			elif len(size)==7:size=size.center(8)
			elif len(size)==8:size=size.center(6)
			elif len(size)==9:size=size.center(4)
			#size=size+" "+str(len(size))

			ss='title="Сидеров">'
			es='</span> | <span class="my_tt leech"'
			sids=mfindal(i, ss, es)[0][len(ss):]
			#print sids
			
			if len(sids)==1:sids=sids.center(9)
			elif len(sids)==2:sids=sids.center(8)
			elif len(sids)==3:sids=sids.center(7)
			elif len(sids)==4:sids=sids.center(6)

			
			UF=0
			Tresh=["Repack"," PC ","XBOX","RePack","FB2","TXT","DOC"," MP3"," JPG"," PNG"," SCR","CAMRip",") TS","CamRip"]
			for TRi in Tresh:
				if title.find(TRi)>=0:UF+=1
			if UF<1: Lout.append([sids,size,xt(title),url])
		except: pass
	return Lout


def Storr(text):
	HideScr = 'true'
	HideTSnd = 'true'
	TitleMode = 0
	EnabledFiltr = 'false'
	Filtr = ""

	RL=upd(text)
	RootList=format(RL)
	Lout=[]
	k=0
	TLD=[]
	defekt=0
	for tTitle in RootList:
		if len(tTitle)==9:
			tTitle.insert(6," ")
		
		if len(tTitle)==10 and int(tTitle[8])>0:
			
			size=tTitle[7]
			if size[-2:]=="MB":size=size[:-5]+"MB"
			
			if len(size)==3:size=size.center(10)
			elif len(size)==4:size=size.center(9)
			elif len(size)==5:size=size.center(8)
			elif len(size)==6:size=size.center(8)
			
			if len(tTitle[8])==1:sids=tTitle[8].center(9)
			elif len(tTitle[8])==2:sids=tTitle[8].center(8)
			elif len(tTitle[8])==3:sids=tTitle[8].center(7)
			elif len(tTitle[8])==4:sids=tTitle[8].center(6)
			else:sids=tTitle[8]
			
			#------------------------------------------------
			k+=1
			nnn=tTitle[1].rfind("/")+1
			ntor=xt(tTitle[1][nnn:])
			dict={}
			cover=""
			#-------------------------------------------------
			
			#Title = "|"+sids+"|"+size+"|  "+tTitle[5]
			Title = tTitle[5]
			UF=0
			if EnabledFiltr == 'true' and Filtr<>"":
				Fnu=Filtr.replace(",",'","')
				Fnu=Fnu.replace('" ','"')
				F1=eval('["'+Fnu+'", "4565646dsfs546546"]')
				Tlo=rulower(Title)
				try:Glo=rulower(dict['genre'])
				except: Glo="45664sdgd6546546"
				for Fi in F1:
					if Tlo.find(rulower(Fi))>=0:UF+=1
					if Glo.find(rulower(Fi))>=0:UF+=1
			Tresh=["Repack"," PC ","XBOX","RePack","FB2","TXT","DOC"," MP3"," JPG"," PNG"," SCR","CAMRip",") TS","CamRip"]
			for TRi in Tresh:
				if tTitle[5].find(TRi)>=0:UF+=1
					
			if HideScr == 'true':
				nH1=Title.find()
				nH2=Title.find()
				nH3=Title.find()
				nH4=Title.find(" DVDScr")
				nH=nH1+nH2+nH3+nH4
			else:
				nH=-1
				
			if HideTSnd == 'true':
				sH=Title.find("Звук с TS")
			else:
				sH=-1
				
			if TitleMode == '1': 
				k1=Title.find('/')
				if k1<0: k1=Title.find('(')
				tmp1=Title[:k1]
				n1=Title.find('(')
				k2=Title.find(' от ')
				if k2<0: k2=None
				tmp2=Title[n1:k2]
				Title = tmp1+tmp2
				Title = Title.replace("| Лицензия","")
				Title = Title.replace("| лицензия","")
				Title = Title.replace("| ЛицензиЯ","")
			
			dict['ntor']=ntor
			tTitle5=ru(tTitle[5].strip().replace("ё","е"))
			nc=tTitle5.find(") ")
			nc2=tTitle5.find("/ ")
			if nc2<nc and nc2 >0: nc=nc2
			CT=rulower(tTitle5[:nc].strip())
			#Title=CT
			if UF==0 and nH<0 and sH<0 and (CT not in TLD):
				#TLD.append(CT)
				if tTitle[1][:4]=="http":row_url = tTitle[1]
				else:row_url = "http://www.rutor.in"+tTitle[1]
				Title=Title.replace("&quot;",'"')
				Lout.append([sids,size,xt(Title),row_url])
				#print Title
				
#				listitem = xbmcgui.ListItem(Title, thumbnailImage=cover, iconImage=cover)
#				purl = sys.argv[0] + '?mode=OpenCat2'\
#					+ '&url=' + urllib.quote_plus(row_url)\
#					+ '&title=' + urllib.quote_plus(str(sids+"|"+size+"| "+tTitle[5]))\
#					+ '&info=' + urllib.quote_plus(repr(dict))
#				xbmcplugin.addDirectoryItem(handle, purl, listitem, True, totalItems=len(RootList)-defekt)
			else: defekt+=1
	return Lout



class Tracker:
	def __init__(self):
		pass

	def Search(self, text="миля", category=0):
		Lout=upd(text)
		return Lout