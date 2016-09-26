#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import re
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
siteUrl = 'www.fast-torrent.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'fasttor.cookies.sid')
 
cj = cookielib.FileCookieJar(sid_file) 
hr  = urllib2.HTTPCookieProcessor(cj) 
opener = urllib2.build_opener(hr) 
urllib2.install_opener(opener) 

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
def rt(x):
	L=[('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x

p = re.compile(r'<.*?>')

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


def GET(target, post=None):
	referer=target
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

def get_HTML(url, post = None, ref = None, get_redirect = False):
	request = urllib2.Request(url, post)
	import urlparse
	#import HTMLParser
	#hpar = HTMLParser.HTMLParser()
	host = urlparse.urlsplit(url).hostname
	if ref==None:
		try:   ref='http://'+host
		except:ref='localhost'

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
		return None
	if get_redirect == True:
		html = f.geturl()
	else:
		html = f.read()
	return html


def format2(L):
	if L==None: 
		return ["","","","","","","","",""]
	else:
		Li=[]
		Ln=[]
		L1=[]
		qual=""
		i=0
		for itm in L:
			i+=1
			if len(itm)>6:
				if itm[:4]=="flag":
					if itm[:5]=="flag2":
						qual=itm[6:]
					if itm[:5]=="flag1":
						#try:
							L1=eval(itm[6:])
							L1.append(qual)
							qual=""
							Ln.append(L1)
						#except: 
						#	qual=""
					
		return Ln


def gettorlist(str):
	#gettorlist_n(str)
	str=str.replace(chr(13)+chr(10),chr(10))
	str=str.replace(chr(10)+chr(13),chr(10))
	str=str.replace(chr(10),"")
	str=str.replace("\t","")
	str=str.replace("&nbsp;"," ")
	
	n=str.find('<div class="ordering">')
	if n<100: n=str.find('>Как скачать фильм?<')
	if n<1000:n=1000
	k=str.rfind('Сообщить о появлении в хорошем качестве')
	str=str[n:k]
	
	str=str.replace("'",'"')
	#str=str.replace("[",'(')
	#str=str.replace("]",')')
	
	str=str.replace('use_tooltip" title="',chr(10)+"flag2:")
	str=str.replace('::',chr(10))

	str=str.replace('Подробнее</a></td><td ><b>',chr(10)+"flag1:['")
	str=str.replace('Подробнее</a></td><td > ',chr(10)+"flag1:['")
	str=str.replace('Подробнее</a>',chr(10)+"flag1:['")
	str=str.replace('</div><div class="c2">',"")
	str=str.replace('</div><div class="c3">',"', '")
	str=str.replace('</div><div class="c4">',"', '")
	str=str.replace('</div><div class="c5">',"', '")
	str=str.replace('</div><div class="c6">',"', '")
	str=str.replace('</div><div class="c7">',"', '")
	str=str.replace('<font color="green" nowrap="nowrap" title="Раздают">', '')
	str=str.replace('</font><br/><font color="red" title="Качают" nowrap="nowrap">', "', '")
	
	str=str.replace('</td><td title="Открыть подробное описание торрента">',"', '")
	str=str.replace('<font color="green" nowrap="nowrap" title="Раздают">',"")
	str=str.replace('</font><br/><font color="red" title="Качают" nowrap="nowrap">',"', '")
	str=str.replace('</font></td><td class="right"><a href="',"', '")
	str=str.replace('.torrent"><img alt="Скачать"',".torrent']"+chr(10))
	str=str.replace('.torrent"><em class="download-button">',".torrent']"+chr(10))
	str=str.replace('.torrent"',".torrent']"+chr(10))
	#print str
	#debug(str)
	str=p.sub('', str)
	
	#fl = open(os.path.join( ru(LstDir),"test.txt"), "w")
	#fl.write(str)
	#fl.close()
	
	L=str.splitlines()
	Ln=format2(L)
	return Ln

def OpenList(url, dict,title):
	#print 'http://www.fast-torrent.ru/'+url.replace(".html", "/torrents.html")
	hp = GET('http://www.fast-torrent.ru'+url.replace(".html", "/torrents.html"))
	#print url
	L=gettorlist(hp)
	LL=[]
	#print L
	for Li in L:
		#print Li
		if len(Li)!=8: Li=["","","","","","","","",""]
		if Li[0]!="": 
			Title = ""#Li[0].strip()
			
		Lang = Li[0].strip()
		Lang=Lang.replace(' (',"(")
		Lang=Lang.replace('многоголосный',"мн-гол")
		Lang=Lang.replace('двухголосный',"2-гол.")
		Lang=Lang.replace('одноголосный',"1-гол.")
		Lang=Lang.replace('дублирование',"дубл.")
		Lang=Lang.replace('закадровый',"закадр.")
		Lang=Lang.replace('полное',"полн.")
		nl=str(len(Lang))
		#Lang=Lang[:40]
		Size = Li[1]
		Size=Size[:10]
		if Size.find("М")>0: Size=Size[:Size.find(".")]+" MB"
		Size=Size.replace('ГБ', "GB")
		#if len(Size)==8: Size="  "+Size+"   "
		#if len(Size)==9: Size="  "+Size+"  "
		#if len(Size)==10: Size=" "+Size+" "
		#if len(Size)==11: Size=" "+Size+" "



		Sids = Li[4].replace("▲ ", "").strip()
		Lich = Li[5]
		SL=Sids+Lich
		#if len(SL)==9:  SL=" "+Sids+"       "+Lich+" "
		if len(SL)==10: SL=" "+Sids+"          "+Lich+" "
		if len(SL)==11: SL=" "+Sids+"        "+Lich+" "
		if len(SL)==12: SL=" "+Sids+"      "+Lich+" "
		if len(SL)==13: SL=" "+Sids+"    "+Lich+" "
		if len(SL)==14: SL=" "+Sids+"  "+Lich+" "
		if len(SL)==15: SL=" "+Sids+""+Lich+" "
		if len(SL)==16: SL=""+Sids+""+Lich+""
			
		Urlt = Li[6].replace('<a href="', httpSiteUrl)
		Qual = Li[7].strip()
		
		#if Title=="": 
		Title = rt(title)
		row_name = Title+"  "+Qual+" | "+Lang
		
		row_url = Urlt
		#try:cover=dict["cover"]
		#except:cover=""
		if SL!='': LL.append({'sids':Sids, 'size':Size, 'title':row_name, 'url':row_url, 'quality':Qual})#LL.append([SL,Size,row_name,row_url])
	return LL


def formatKP(s):
	return urllib.quote(s)


def upd(text):
	stext=text.replace(" ", "%20")
	categoryUrl = 'http://www.fast-torrent.ru/search/'+stext+'/1.html'#search/
	#print categoryUrl
	#post={"sort":"8","search_pages":"50"}#13
	#http = GET(categoryUrl, httpSiteUrl, post)
	post = "search_pages=50&sort=8"
	http = get_HTML(categoryUrl, post)
	if http == None:
		print 'fast-torrent: Сервер не отвечает'
		return None
	else:
		LL=formtext_n(http)
		#LL=http.splitlines()
		return LL

def Search2(text):
	#print text
	RootList=upd(text)
	L=[]
	n=0
	for t in RootList:
				n+=1
				#print t
				dict=t
				title=t['title']
				row_url = t['url']
				LL=OpenList(row_url, dict, title)
				L.extend(LL)
				if n>5: return L
	return L


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

def formtext_n(http):
	#n=http.find('end Пустой баннер')
	#http=http[n:]
	http=http.replace(chr(13),chr(10))
	http=http.replace(chr(10)+chr(10),chr(10))
	http=http.replace(chr(10)+chr(10),chr(10))
	http=http.replace("\t","")
	http=http.replace("'",'"')
	ss='<div class="film-item'
	ss='<div class="film-wrap'
	es='<em class="download-button">'#'<tr><td colspan="4"'
	#debug (http)
	L=mfindal(http, ss, es)
	#debug (L[3])
	RL=[]
	for i in L:
		try:
			dict={}
		#------------------- ищем ссылку ----------------
		#for i in L:
			ss='</div><div class="film-foot"><a href="'
			es='" target="_blank"'
			#if i.find(ss)<0:ss='<span style="header">Режиссер</span>'
			L2=mfindal(i, ss, es)
			nm=L2[1][len(ss):]
			#print("URL: "+nm)
			dict['url']=nm
			
		#------------------- ищем обложку ----------------
		#for i in L:
			ss='style="background: url('
			es=')"></a></div><div class="film-info">'
			#if i.find(ss)<0:ss='<span style="header">Режиссер</span>'
			L2=mfindal(i, ss, es)
			nm=L2[0][len(ss):]
			#print("IMG: "+nm)
			dict['cover']=nm
		#------------------- ищем название ----------------
		#for i in L:</li></ul></span></div><h2>
			ss='><span itemprop="name">'#</ul></span>
			es='</h2><div class="film-genre'
			#if i.find(ss)<0:ss='</h2><div class="genre_list'
			L2=mfindal(i, ss, es)
			try:nm=L2[0][len(ss):].replace("<br/>",'').replace("</span>",'').replace('<span itemprop="alternativeHeadline">','').strip()
			except: nm="НАЗВАНИЕ"
			#print("НАЗВАНИЕ: "+nm)
			#print nm.find("(")
			dict['title']=nm#[:nm.find("(")]
			
			try:dict['year']=int(mfindal(nm, "(", ")")[0][1:])
			except:
				try:dict['year']=int(mfindal(nm, "(", ")")[1][1:])
				except:pass
			RL.append(dict)
		except: pass
	return RL



class Tracker:
	def __init__(self):
		pass

	def Search(self, info):
		text=info['title']
		Lout=Search2(text)
		return Lout