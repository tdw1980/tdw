#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib
import os
import Cookie

import string, xbmc, xbmcgui, xbmcplugin, urllib, cookielib, xbmcaddon, urllib, urllib2, time
#-------------------------------


icon = ""
siteUrl = 'www.torrentino.me'
httpSiteUrl = 'http://' + siteUrl
addon = xbmcaddon.Addon(id='plugin.video.KinoPoisk.ru')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def debug(s):
	fl = open(ru(os.path.join( addon.getAddonInfo('path'),"test.txt")), "wb")
	fl.write(s)
	fl.close()


def GET(target, referer='http://www.torrentino.me', post=None):
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
		return ''


def upd(text, category):
	search=urllib.quote(text)
	url= 'http://www.torrentino.me/search?search='+search+category
	http = GET(url)
	if http == None:
		print 'torrentino: Сервер не отвечает'
		return None
	else:
		return http

def Parser_M(http, info):
	title=info['title']
	year1=str(info['year'])
	year2=str(info['year']+1)
	type =info['type']
	
	ss='<div class="tile"'
	es='</h2>'
	L=mfindal(http, ss,es)
	L2=[]
	for i in L:
		if title in i and (year1 in i or year2 in i or type != ""):
			ss='itemprop="name">'
			es='<span class="year"'
			i_title=mfindal(i,ss,es)[0][len(ss):]
			
			ss='href="'
			es='" title="'
			i_url='http://www.torrentino.me'+mfindal(i,ss,es)[0][len(ss):]
			
			#print i_title
			#print i_url
			L2.append(i_url)
	return L2
	
def Parser_S(http, info):
	title=info['title']
	year1=str(info['year'])
	year2=str(info['year']+1)
	type =info['type']
	
	ss='<div class="tile"'
	es='</h2>'
	L=mfindal(http, ss,es)
	L2=[]
	for i in L:
		if title in i and (year1 in i or year2 in i):
			ss='itemprop="name">'
			es='<span class="year"'
			i_title=mfindal(i,ss,es)[0][len(ss):]
			
			ss=' href="'
			es='" title="'
			i_url='http://www.torrentino.me'+mfindal(i,ss,es)[0][len(ss):]
			
			#print i_title
			#print i_url
			L2.append(i_url)
	return L2

def get_torrents_m(url, info):
	http=GET(url)
	
	ss='<div class="header-group">'
	es='<td class="value" itemprop="duration"'
	if es not in http: es='<meta itemprop="ratingValue"'
	nfo=mfindal(http,ss,es)[0]
	nfo=mfindal(http,ss,es)[0]
	
	Lnfo=nfo.splitlines()
	en_title="рус."
	ru_title=""
	year=""
	for i in Lnfo:
		if '<h1'           in i: ru_title=i[i.find('">')+2:i.find('</h1')]
		if '<h2'           in i: en_title=i[i.find('">')+2:i.find('</h2')]
		if 'copyrightYear' in i: year    =i[i.find('">')+2:i.find('</td')]
	
	if ru_title != info['title'] and ru_title !="" : return [] # Отсекает по русскому названию!
	
	ss='<tr data-group="group'
	es='href="javascript:void(0);" >Скачать</a>'
	L=mfindal(http,ss,es)
	Lout=[]
	for k in L:
		L2=k.splitlines()
		seed='0'
		size='0'
		quality=''
		quality2=''
		torrent=''
		for j in L2:
			if 'column size'  in j: size   =j[j.find('">')+2:j.find('</')]
			if 'class="seed"' in j: seed   =j[j.find('">')+2:j.find('</')]
			if 'data-torrent' in j: torrent=j[j.find('="')+2:-1]
			if 'title="'      in j: quality=j[j.find(' в  ')+3:j.find(' качестве"')].strip()
			if '1920x'        in j: quality2= ' 1080p'
			if '1280x'        in j: quality2= ' 720p'
		if 'class="label-3d"' in k: quality2 += ' 3D'
		if 'не установ' in quality: quality=""
		if size.find("М")>0: size=size[:size.find(".")]+" MB"
		size=size.replace('ГБ', "GB")
		title=ru_title+" / "+en_title+" ("+year+") "+quality+quality2
		if size!="0": Lout.append({"sids":seed, "size":size, "title":xt(title),"url":torrent, "quality": quality})
	return Lout

def get_torrents_s(url, info):
	http=GET(url)
	
	ss='<tr class="item"'
	es='href="javascript:void(0);" >Скачать</a>'
	L=mfindal(http,ss,es)
	Lout=[]
	for k in L:
		L2=k.splitlines()
		seed='0'
		size='0'
		quality=''
		quality2=''
		torrent=''
		for j in L2:
			if 'column size'  in j: size   =j[j.find('">')+2:j.find('</')]
			if 'class="seed"' in j: seed   =j[j.find('">')+2:j.find('</')]
			if 'data-torrent' in j: torrent=j[j.find('="')+2:-1]
			if 'title="'      in j: title=j.replace('title="Скачать ',"").strip()[:-1]
			if '1920x'        in j: quality= ' 1080p'
			if '1280x'        in j: quality= ' 720p'
		if 'class="label-3d"' in k: quality += ' 3D'
		if size.find("М")>0: size=size[:size.find(".")]+" MB"
		size=size.replace('ГБ', "GB")
		title=title+" "+quality
		if size!="0" and info['title'] in title : Lout.append({"sids":seed, "size":size, "title":xt(title),"url":torrent, "quality": quality})
	return Lout

def get_torrents_s2(url, info):
	http=GET(url)
	
	ss='<tr class="item"'
	es='href="javascript:void(0);" >Скачать</a>'
	L=mfindal(http,ss,es)
	Lout=[]
	for k in L:
		L2=k.splitlines()
		seed='0'
		size='0'
		quality=''
		quality2=''
		torrent=''
		title=''
		title2=''
		for j in L2:
			if 'column size'  in j: size   =j[j.find('">')+2:j.find('</')]
			if 'class="seed"' in j: seed   =j[j.find('">')+2:j.find('</')]
			if 'data-torrent' in j: torrent=j[j.find('="')+2:-1]
			if 'title="'      in j: title=j[j.find('="')+2:j.find('сезон')+10].replace('Скачать ',"")
			if 'data-default' in j: title2=j[j.find('&dn=')+4:j.find('&tr=')]
			if '1920x'        in j: quality= ' 1080p'
			if '1280x'        in j: quality= ' 720p'
		if 'class="label-3d"' in k: quality += ' 3D'
		if size.find("М")>0: size=size[:size.find(".")]+" MB"
		size=size.replace('ГБ', "GB")
		title=title+"  /  "+urllib.unquote_plus(title2).replace(title,"")+" "+quality
		if size!="0": Lout.append({"sids":seed, "size":size, "title":xt(title),"url":torrent, "quality": quality})
	return Lout

def get_sz(url):
	http=GET(url)
	L=[25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
	for i in L:
		if 'season-'+str(i) in http: return i
	return 0

def Storr(info):
	Lout=[]
	
	if info['type']=="": 
		text=info['originaltitle']
		category = '&type=movies'
		http=upd(text, category)
		RL=Parser_M(http, info)
		if len(RL)==0:
			http=upd(info['title'], category)
			RL=Parser_M(http, info)
		for i in RL:
			Lout.extend(get_torrents_m(i, info))
	else: 
		text=info['title']
		
		category = '&type=shows'
		http=upd(text, category)
		RL=Parser_S(http, info)
		for i in RL:
			n=get_sz(i)
			for sz in range(1,n+1):
				url2= i+'/season-'+str(sz)+'/episode-1'
				
				Lout.extend(get_torrents_s2(url2, info))
		
		if len(Lout)<20:
			category = '&type=torrents'
			
			for i in [1,2,3,4]:
				page="&page="+str(i)
				url= 'http://www.torrentino.me/search?search='+text+category+page
				Lout.extend(get_torrents_s(url, info))

	return Lout



class Tracker:
	def __init__(self):
		pass

	def Search(self, info):
		Lout=Storr(info)
		return Lout