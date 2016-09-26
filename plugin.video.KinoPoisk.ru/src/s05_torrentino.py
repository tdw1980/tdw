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


def upd(text, category):
	search=urllib.quote(text)
	url= 'http://www.torrentino.me/search?search='+search+category
	http = GET(url)
	if http == None:
		print 'torrentino: Сервер не отвечает'
		return None
	else:
		return http

def Parser(http, info):
	title=info['title']
	year1=str(info['year'])
	year2=str(info['year']+1)
	type =info['type']
	#debug (http)
	ss='<div class="tile"'
	es='</h2>'
	L=mfindal(http, ss,es)
	L2=[]
	for i in L:
		if title in i and (year1 in i or year2 in i or type != ""):
			ss='itemprop="name">'
			es='<span class="year"'
			i_title=mfindal(i,ss,es)[0][len(ss):]
			
			ss='<a href="'
			es='" title="'
			i_url='http://www.torrentino.me'+mfindal(i,ss,es)[0][len(ss):]
			
			#print i_title
			#print i_url
			L2.append(i_url)
	return L2

def get_torrents(url, info):
	http=GET(url)
	ss='<div class="header-group">'
	es='<meta itemprop="ratingValue"'
	if es not in http: es='<td class="value" itemprop="duration"'
	nfo=mfindal(http,ss,es)[0]
	Lnfo=nfo.splitlines()
	en_title="рус."
	for i in Lnfo:
		if '<h1'           in i: ru_title=i[i.find('">')+2:i.find('</h1')]
		if '<h2'           in i: en_title=i[i.find('">')+2:i.find('</h2')]
		if 'copyrightYear' in i: year    =i[i.find('">')+2:i.find('</td')]
	
	if ru_title != info['title']: return [] # Отсекает по русскому названию!
	
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



def Storr(info):
	text=info['originaltitle']
	if info['type']=="": category = '&type=movies'
	else: category = '&type=shows'
	http=upd(text, category)
	RL=Parser(http, info)
	if len(RL)==0:
		http=upd(info['title'], category)
		RL=Parser(http, info)
	Lout=[]
	for i in RL:
		Lout.extend(get_torrents(i, info))
	return Lout



class Tracker:
	def __init__(self):
		pass

	def Search(self, info):
		Lout=Storr(info)
		return Lout