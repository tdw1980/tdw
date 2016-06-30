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
			Title =Title[:20]
			if len(Title)==10:   Title="          "+Title+"          "
			elif len(Title)==11: Title="         "+Title+"         "
			elif len(Title)==12: Title="        "+Title+"        "
			elif len(Title)==13: Title="       "+Title+"       "
			elif len(Title)==14: Title="      "+Title+"      "
			elif len(Title)==15: Title="     "+Title+"     "
			elif len(Title)==16: Title="    "+Title+"    "
			elif len(Title)==17: Title="   "+Title+"  "
			elif len(Title)==18: Title="  "+Title+"  "
			elif len(Title)==19: Title=" "+Title+" "
			elif len(Title)==20: Title=""+Title+""
			else: Title = ""
			
		Lang = Li[0].strip()
		Lang=Lang.replace(' (',"(")
		Lang=Lang.replace('многоголосный',"мн-гол")
		Lang=Lang.replace('двухголосный',"2-гол.")
		Lang=Lang.replace('одноголосный',"1-гол.")
		Lang=Lang.replace('дублирование',"дубл.")
		Lang=Lang.replace('закадровый',"закадр.")
		Lang=Lang.replace('полное',"полн.")
		nl=str(len(Lang))
		Lang=Lang[:40]
		if len(Lang)==3:    Lang="                   "+Lang+"                   "
		elif len(Lang)==9:  Lang="                "+Lang+"                 "
		elif len(Lang)==10: Lang="               "+Lang+"                 "
		elif len(Lang)==11: Lang="               "+Lang+"                "
		elif len(Lang)==12: Lang="              "+Lang+"                "
		elif len(Lang)==13: Lang="              "+Lang+"               "
		elif len(Lang)==14: Lang="             "+Lang+"               "
		elif len(Lang)==15: Lang="             "+Lang+"              "
		elif len(Lang)==16: Lang="             "+Lang+"             "
		elif len(Lang)==17: Lang="            "+Lang+"            "
		elif len(Lang)==18: Lang="           "+Lang+"            "
		elif len(Lang)==19: Lang="           "+Lang+"           "
		elif len(Lang)==20: Lang="          "+Lang+"           "
		elif len(Lang)==21: Lang="          "+Lang+"          "
		elif len(Lang)==22: Lang="         "+Lang+"          "
		elif len(Lang)==23: Lang="         "+Lang+"         "
		elif len(Lang)==24: Lang="        "+Lang+"         "
		elif len(Lang)==25: Lang="        "+Lang+"        "
		elif len(Lang)==26: Lang="       "+Lang+"        "
		elif len(Lang)==27: Lang="       "+Lang+"       "
		elif len(Lang)==28: Lang="      "+Lang+"       "
		elif len(Lang)==29: Lang="      "+Lang+"      "
		elif len(Lang)==30: Lang="     "+Lang+"      "
		elif len(Lang)==31: Lang="     "+Lang+"     "
		elif len(Lang)==32: Lang="    "+Lang+"     "
		elif len(Lang)==33: Lang="    "+Lang+"    "
		elif len(Lang)==34: Lang="   "+Lang+"    "
		elif len(Lang)==35: Lang="   "+Lang+"   "
		elif len(Lang)==36: Lang="  "+Lang+"   "
		elif len(Lang)==37: Lang="  "+Lang+"  "
		elif len(Lang)==38: Lang=" "+Lang+"  "
		elif len(Lang)==39: Lang=" "+Lang+" "
		elif len(Lang)==40: Lang=""+Lang+" "
		#Lang=nl+Lang
		Size = Li[1]
		Size=Size[:10]
		if Size.find("М")>0: Size=chr(2)+"  "+Size[:Size.find(".")]+" MБ [COLOR 00FFF000].[/COLOR]"
		if len(Size)==8: Size="  "+Size+"   "
		if len(Size)==9: Size="  "+Size+"  "
		if len(Size)==10: Size=" "+Size+" "
		if len(Size)==11: Size=" "+Size+" "



		Sids = Li[4]
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
		Qual=Qual.replace('КПК',"    КПК     ")
		Qual=Qual.replace('Blu-Ray',  " Blu-Ray  ")
		Qual=Qual.replace('WebRip HD',"  WR HD   ")
		
		if len(Qual)==3:    Qual="    "+Qual+"    "
		elif len(Qual)==4:  Qual="    "+Qual+"   "
		elif len(Qual)==5:  Qual="   "+Qual+"   "
		elif len(Qual)==6:  Qual="  "+Qual+"  "
		elif len(Qual)==7:  Qual=" "+Qual+" "
		elif len(Qual)==8:  Qual=" "+Qual+" "
		elif len(Qual)==9:  Qual=""+Qual+" "
		elif len(Qual)==10: Qual=""+Qual+""
		
		if Title=="": Title = title
		row_name = Qual+"|"+Title+"|"+Lang+"|"
		
		row_url = Urlt
		#try:cover=dict["cover"]
		#except:cover=""
		if SL!='': LL.append([SL,Size,row_name,row_url])
	return LL


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
	stext=text.replace(" ", "%20")
	categoryUrl = 'http://www.fast-torrent.ru/search/'+stext+'/1.html'#search/
	#print categoryUrl
	#post={"sort":"8","search_pages":"50"}#13
	#http = GET(categoryUrl, httpSiteUrl, post)
	post = "search_pages=50&sort=8"
	http = get_HTML(categoryUrl, post)
	if http == None:
		showMessage('fast-torrent:', 'Сервер не отвечает', 1000)
		return None
	else:
		LL=formtext_n(http)
		#LL=http.splitlines()
		return LL

def Search2(text):
	#print text
	RootList=upd(text)
	for t in RootList:
				#print t
				dict=t
				title=t['title']
				row_url = t['url']
				LL=OpenList(row_url, dict, title)
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

	def Search(self, text="миля", category=0):
		#print '=================================='
		Lout=Search2(text)
		return Lout