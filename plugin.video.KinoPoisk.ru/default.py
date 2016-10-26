#!/usr/bin/python
# -*- coding: utf-8 -*-

# *  Copyright (C) 2016 TDW

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, urllib2, time, codecs, httplib

PLUGIN_NAME   = 'KinoPoisk-2.0'
siteUrl = 'www.KinoPoisk.ru'
httpSiteUrl = 'https://' + siteUrl
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.KinoPoisk.ru')
__settings__ = xbmcaddon.Addon(id='plugin.video.KinoPoisk.ru')
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

icon  = os.path.join( addon.getAddonInfo('path'), 'icon.png')
dbDir = os.path.join( addon.getAddonInfo('path'), "db" )
LstDir = addon.getAddonInfo('path')

#======================== стандартные функции ==========================
def fs_enc(path):
	sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
	return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
	sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
	return path.decode(sys_enc).encode('utf-8')

def fs(s):return s.decode('windows-1251').encode('utf-8')
def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
def rt(x):
	L=[('&#133;','…'),('&#34;','&'), ('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y'), ('&laquo;','"'), ('&raquo;','"'), ('&nbsp;',' ')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x

def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

def mid(s, n):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.center(n)
	try:s=s.encode('utf-8')
	except: pass
	return s

def mids(s, n):
	l="                                              "
	s=l[:n-len(s)]+s+l[:n-len(s)]
	return s

def FC(s, color="FFFFFF00"):
	s="[COLOR "+color+"]"+s+"[/COLOR]"
	return s

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

def inputbox():
	skbd = xbmc.Keyboard()
	skbd.setHeading('Поиск:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return ""

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

#====================== подготовка данных для интерфейса ================

from KPmenu import *

Category=[]
CategoryDict={}
for i in TypeList:
	Category.append(i[1])
	CategoryDict[i[1]]=i[0]

Genre=[]
GenreDict={}
for i in GenreList:
	Genre.append(i[1])
	GenreDict[i[1]]=i[0]

Cantry=[]
CantryDict={}
for i in CantryList:
	Cantry.append(i[1])
	CantryDict[i[1]]=i[0]

Year=[]
YearDict={}
for i in YearList:
	Year.append(i[1])
	YearDict[i[1]]=i[0]

Old=[]
OldDict={}
for i in OldList:
	Old.append(i[1])
	OldDict[i[1]]=i[0]

Sort=[]
SortDict={}
for i in SortList:
	Sort.append(i[1])
	SortDict[i[1]]=i[0]

Rating=[]
RatingDict={}
for i in RatingList:
	Rating.append(i[1])
	RatingDict[i[1]]=i[0]


#============================== основная часть ============================

def save_strm(url, ind=0, id='0'):
		info=get_info(str(id))
		SaveDirectory = __settings__.getSetting("SaveDirectory")
		if SaveDirectory=="":SaveDirectory=LstDir
		name = info['originaltitle'].replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		
		uri = sys.argv[0] + '?mode=PlayTorrent'
		uri = uri+ '&url='+urllib.quote_plus(url)
		uri = uri+ '&ind='+str(ind)
		uri = uri+ '&id='+str(id)
		
		fl = open(os.path.join(fs_enc(SaveDirectory),fs_enc(name+".strm")), "w")
		fl.write(uri)
		fl.close()
		
		xbmc.executebuiltin('UpdateLibrary("video", "", "false")')

def save_film_nfo(id):
		get_posters(id)
		info=get_info(str(id))
		title=info['title']
		fanart=info['fanart']
		cover=info['cover']
		try: fanarts=info["fanarts"]
		except: fanarts=[fanart,cover]
		posters=get_posters(id)
		fanarts.extend(posters)
		
		year=info['year']
		plot=info['plot']
		rating=info['rating']
		originaltitle=info['originaltitle']

		duration=info["duration"]
		genre=info["genre"].replace(', ', '</genre><genre>')
		studio=info["studio"]
		director=info["director"]
		cast=info["cast"]
		try: actors=info["actors"]
		except: actors={}
		
		name = info['originaltitle'].replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		cn=name.find(" (")
		#if cn>0:
		#	name=name[:cn]
		#	rus=1
		#else: rus=0
		
		#trailer=get_trailer(id)
		
		SaveDirectory = __settings__.getSetting("SaveDirectory")
		if SaveDirectory=="":SaveDirectory=LstDir
		
		nfo='<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'+chr(10)
		nfo+='<movie>'+chr(10)
		
		nfo+="	<title>"+title+"</title>"+chr(10)
		nfo+="	<originaltitle>"+originaltitle+"</originaltitle>"+chr(10)
		nfo+="	<genre>"+genre+"</genre>"+chr(10)
		nfo+="	<studio>"+studio+"</studio>"+chr(10)
		nfo+="	<director>"+director+"</director>"+chr(10)
		nfo+="	<year>"+str(year)+"</year>"+chr(10)
		nfo+="	<plot>"+plot+"</plot>"+chr(10)
		nfo+='	<rating>'+str(rating)+'</rating>'+chr(10)
		nfo+='	<runtime>'+duration+' min.</runtime>'+chr(10)
		
		nfo+="	<fanart>"+chr(10)
		for fan in fanarts:
			nfo+="		<thumb>"+fan+"</thumb>"+chr(10)
		nfo+="		<thumb>"+cover+"</thumb>"+chr(10)
		nfo+="	</fanart>"+chr(10)
		
		nfo+="	<thumb>"+cover+"</thumb>"+chr(10)
		
		for actor in cast:
			nfo+="	<actor>"+chr(10)
			nfo+="		<name>"+actor+"</name>"+chr(10)
			try:
				aid=actors[actor]
				actor_img="http://st.kp.yandex.net/images/actor_iphone/iphone360_"+aid+".jpg"
				nfo+="		<thumb>"+actor_img+"</thumb>"+chr(10)
			except: pass
			nfo+="	</actor>"+chr(10)
		
		nfo+="</movie>"+chr(10)
		
		fl = open(os.path.join(fs_enc(SaveDirectory),fs_enc(name+".nfo")), "w")
		fl.write(nfo)
		fl.close()

def get_posters(id):
	try:
		url='http://plus.kinopoisk.ru/film/'+id+'/details/art/poster/'
		http=GET(url)
		ss='src="//avatars.mds.yandex.net/get-kino-vod-films-gallery/'
		es='" data-bem'
		es='x538'
		L=mfindal(http,ss,es)
		L2=[]
		for i in L:
			if len(i)<120 and len(i)>80:
				img=i.replace('src="//', 'http://')+es#.replace('x80', 'x538').replace('x120', 'x538').replace('120x', 'x538').replace('x80', 'x538').replace('80x', 'x538')
				L2.append(img)
		return L2
	except: return []

def get_trailer(id):
	try:
		url='https://www.kinopoisk.ru/film/'+id+'/video/type/1/'
		http=GET(url)
		ss='kinoplayer-loader.swf?file='
		es='&amp;autostart=true&amp;link='
		link=urllib.unquote_plus(mfindal(http,ss,es)[0][len(ss):])
		return link
	except: return ""

def getList(id):
	try:L = eval(__settings__.getSetting(id))
	except:L =[]
	S=""
	for i in L:
		if i[:1]=="[": S=S+", "+i
	return S[1:]

def getList2(id):
	try:L = eval(__settings__.getSetting(id))
	except:L =[]
	S=[]
	for i in L:
		if i[:1]=="[": S.append(i.replace("[COLOR FFFFFF00]","").replace("[/COLOR]",""))
	return S


def setList(idw, L):
	__settings__.setSetting(id=idw, value=repr(L))

def play(url, ind=0, id='0'):
	#print url
	engine=__settings__.getSetting("Engine")
	if engine=="0": 
		if play_ace (url, ind) != 'Ok':
			if ind == 0: 
				if play_ace (alter (id, url), 0) != 'Ok': xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.KinoPoisk.ru/?mode=Torrents&id='+id+'", return)')
			else: xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.KinoPoisk.ru/?mode=Torrents&id='+id+'", return)')
	if engine=="1": play_t2h (url, ind, __settings__.getSetting("DownloadDirectory"))
	if engine=="2": play_yatp(url, ind)

def play_ace(torr_link, ind=0):
	title=get_item_name(torr_link, ind)
	from TSCore import TSengine as tsengine
	TSplayer=tsengine()
	out=TSplayer.load_torrent(torr_link,'TORRENT')
	#print out
	if out=='Ok': TSplayer.play_url_ind(int(ind),title, icon, icon, True)
	TSplayer.end()
	return out

def play_t2h(uri, file_id=0, DDir=""):
	try:
		sys.path.append(os.path.join(xbmc.translatePath("special://home/"),"addons","script.module.torrent2http","lib"))
		from torrent2http import State, Engine, MediaType
		progressBar = xbmcgui.DialogProgress()
		from contextlib import closing
		if DDir=="": DDir=os.path.join(xbmc.translatePath("special://home/"),"userdata")
		progressBar.create('Torrent2Http', 'Запуск')
		# XBMC addon handle
		# handle = ...
		# Playable list item
		# listitem = ...
		# We can know file_id of needed video file on this step, if no, we'll try to detect one.
		# file_id = None
		# Flag will set to True when engine is ready to resolve URL to XBMC
		ready = False
		# Set pre-buffer size to 15Mb. This is a size of file that need to be downloaded before we resolve URL to XMBC 
		pre_buffer_bytes = 15*1024*1024
		engine = Engine(uri, download_path=DDir)
		with closing(engine):
			# Start engine and instruct torrent2http to begin download first file, 
			# so it can start searching and connecting to peers  
			engine.start(file_id)
			progressBar.update(0, 'Torrent2Http', 'Загрузка торрента', "")
			while not xbmc.abortRequested and not ready:
				xbmc.sleep(500)
				status = engine.status()
				# Check if there is loading torrent error and raise exception 
				engine.check_torrent_error(status)
				# Trying to detect file_id
				if file_id is None:
					# Get torrent files list, filtered by video file type only
					files = engine.list(media_types=[MediaType.VIDEO])
					# If torrent metadata is not loaded yet then continue
					if files is None:
						continue
					# Torrent has no video files
					if not files:
						break
						progressBar.close()
					# Select first matching file                    
					file_id = files[0].index
					file_status = files[0]
				else:
					# If we've got file_id already, get file status
					file_status = engine.file_status(file_id)
					# If torrent metadata is not loaded yet then continue
					if not file_status:
						continue
				if status.state == State.DOWNLOADING:
					# Wait until minimum pre_buffer_bytes downloaded before we resolve URL to XBMC
					if file_status.download >= pre_buffer_bytes:
						ready = True
						break
					#print file_status
					progressBar.update(100*file_status.download/pre_buffer_bytes, 'Torrent2Http', xt('Предварительная буферизация: '+str(file_status.download/1024/1024)+" MB"), "")
					
				elif status.state in [State.FINISHED, State.SEEDING]:
					#progressBar.update(0, 'T2Http', 'We have already downloaded file', "")
					# We have already downloaded file
					ready = True
					break
				
				if progressBar.iscanceled():
					progressBar.update(0)
					progressBar.close()
					break
				# Here you can update pre-buffer progress dialog, for example.
				# Note that State.CHECKING also need waiting until fully finished, so it better to use resume_file option
				# for engine to avoid CHECKING state if possible.
				# ...
			progressBar.update(0)
			progressBar.close()
			if ready:
				# Resolve URL to XBMC
				item = xbmcgui.ListItem(path=file_status.url)
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
				xbmc.sleep(3000)
				# Wait until playing finished or abort requested
				while not xbmc.abortRequested and xbmc.Player().isPlaying():
					xbmc.sleep(500)
	except: pass


def play_yatp(url, ind):
	purl ="plugin://plugin.video.yatp/?action=play&torrent="+ urllib.quote_plus(url)+"&file_index="+str(ind)
	item = xbmcgui.ListItem(path=purl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def GET(url,Referer = 'http://www.KinoPoisk.ru/'):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
		req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
		req.add_header('Accept-Language', 'ru,en;q=0.9')
		req.add_header('Referer', Referer)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except:
		import requests
		s = requests.session()
		r=s.get(url).text
		rd=r.encode('windows-1251')
		return rd

def GETtorr(target):
	try:
			req = urllib2.Request(url = target)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			return resp.read()
	except Exception, e:
			print 'HTTP ERROR ' + str(e)
			return None

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param



import sqlite3 as db
db_name = os.path.join( addon.getAddonInfo('path'), "move_info.db" )
c = db.connect(database=db_name)
cu = c.cursor()
def add_to_db(n, item):
		item=item.replace("'","XXCC").replace('"',"XXDD")
		err=0
		tor_id="n"+n
		litm=str(len(item))
		try:
			cu.execute("CREATE TABLE "+tor_id+" (db_item VARCHAR("+litm+"), i VARCHAR(1));")
			c.commit()
		except: 
			err=1
			print "Ошибка БД"
		if err==0:
			cu.execute('INSERT INTO '+tor_id+' (db_item, i) VALUES ("'+item+'", "1");')
			c.commit()
			#c.close()

def get_inf_db(n):
		tor_id="n"+n
		cu.execute(str('SELECT db_item FROM '+tor_id+';'))
		c.commit()
		Linfo = cu.fetchall()
		info=Linfo[0][0].replace("XXCC","'").replace("XXDD",'"')
		return info

def rem_inf_db(n):
		tor_id="n"+n
		try:
			cu.execute("DROP TABLE "+tor_id+";")
			c.commit()
		except: pass

def get_labels(info):
	Linf=['genre', 'year', 'rating', 'cast', 'director', 'plot', 'title', 'originaltitle', 'studio']
	Labels={}
	for inf in Linf:
		try:Labels[inf] = info[inf]
		except: pass
	try:Labels['duration'] = str(int(info['duration'])*60)
	except: pass
	return Labels


def AddItem(Title = "", mode = "", id='0', url='', total=100):
			if id !='0':
				if mode=="PersonFilm":
					cover='https://st.kp.yandex.net/images/actor_iphone/iphone360_'+id+".jpg"
					fanart = ''
					info={"cover":cover, "title":Title, "id":id}
				else:
					info=get_info(id)
					try:    cover = info["cover"]
					except: cover = icon
					try:    fanart = info["fanart"]
					except: fanart = ''
			else:
				cover = icon
				fanart = ''
				info={}
			listitem = xbmcgui.ListItem(Title, iconImage=cover, thumbnailImage=cover)
			listitem.setInfo(type = "Video", infoLabels = get_labels(info))
			try: listitem.setArt({ 'poster': cover, 'fanart' : fanart})
			except: pass
			listitem.setProperty('fanart_image', fanart)
			
			purl = sys.argv[0] + '?mode='+mode+'&id='+id
			if url !="": purl = purl +'&url='+urllib.quote_plus(url)
			
			if mode=="Torrents":
				listitem.addContextMenuItems([('[B]Hайти похожие[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Recomend&id='+id+'")'), ('[B]Персоны[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Person&id='+id+'")'), ('[B]Трейлер[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=PlayTrailer&id='+id+'")'), ('[B]Рецензии[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Review&id='+id+'")'), ('[B]Буду смотреть[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Add2List&id='+id+'")'), ('[B]Список раздач[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Torrents2&id='+id+'")')])
			if mode=="PlayTorrent":
				listitem.addContextMenuItems([('[B]Сохранить фильм(STRM)[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=save_strm&id='+id+'&url='+urllib.quote_plus(url)+'")'),])
			if mode=="OpenTorrent":
				try:type=info["type"]
				except:type=''
				if type != '': listitem.addContextMenuItems([('[B]Сохранить сериал[/B]', 'Container.Update("plugin://plugin.video.torrent.checker/?mode=save_episodes_api&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(info['originaltitle'])+ '&info=' + urllib.quote_plus(repr(info))+'")'),])
				else: listitem.addContextMenuItems([('[B]Сохранить фильм(STRM)[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Save_strm&id='+id+'&url='+urllib.quote_plus(url)+'")'),])
				
			if mode=="PersonFilm":
				listitem.addContextMenuItems([('[B]Добавить в Персоны[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=AddPerson&info='+urllib.quote_plus(repr(info))+'")'), ('[B]Удалить из Персоны[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=RemovePerson&info='+urllib.quote_plus(repr(info))+'")')])
			if mode=="Wish":
				listitem.addContextMenuItems([('[B]Удалить задание[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=RemItem&&id='+id+'")'),])
			
			try:type=info["type"]
			except:type=''
			if __settings__.getSetting("Autoplay") == 'true' and mode=="Torrents" and type=="":
				listitem.setProperty('IsPlayable', 'true')
				purl = sys.argv[0] + '?mode=Autoplay&id='+id
				xbmcplugin.addDirectoryItem(handle, purl, listitem, False, total)
			else:
				xbmcplugin.addDirectoryItem(handle, purl, listitem, True, total)

def AddPerson(info):
		try:PL=eval(__settings__.getSetting("PersonLst"))
		except: PL=[]
		if info not in PL: 
			PL.append(info)
			__settings__.setSetting(id="PersonLst", value=repr(PL))

def RemovePerson(info):
		try:PL=eval(__settings__.getSetting("PersonLst"))
		except: PL=[]
		NL=[]
		for i in PL:
				if i!=info: NL.append(i)
		__settings__.setSetting(id="PersonLst", value=repr(NL))

def PersonList():
		try:PL=eval(__settings__.getSetting("PersonLst"))
		except: PL=[]
		for i in PL:
			id = i['id']
			AddItem(i["title"], "PersonFilm", id, '',len(PL))

def Person():
	try:id = urllib.unquote_plus(get_params()["id"])
	except: id = ''
	link="http://m.kinopoisk.ru/cast/"+id+"/"
	#print link
	ss='<dt>'
	se='</dd><dt>'
	http = GET (link, httpSiteUrl)
	L=mfindal(http, ss, se)
	
	for i in L:
		
		ss='<dt>'
		se='</dt><dd>'
		tb=mfindal(i, ss, se)[0][4:]
		AddItem(FC(fs(tb)), "", '0', '', len(L))
		
		ss='/person/'
		se='</a>'
		L2=mfindal(i, ss, se)
		for j in L2:
			n=j.find('/">')
			nm=j[n+3:]
			id=j[8:n]
			#cover="http://st.kp.yandex.net/images/sm_actor/"+id+".jpg"
			cover="http://st.kp.yandex.net/images/actor_iphone/iphone360_"+id+".jpg"
			#.replace('sm_film/','film_iphone/iphone360_')+'.jpg'
			#info={"cover":cover, "title":nm, "id":id}
			#print info
			AddItem(fs(nm), "PersonFilm", id, '', len(L))



def SrcNavi(md="Navigator"):
	#ss="/level/1/film/"
	ss='id="film_eye_'
	#se='/">'
	se='"></div>'

	if md =="Navigator":
		Cats=getList("CutList")
		#Genres=getList("GenreList")
		Cantrys=getList("CantryList")
		Years=__settings__.getSetting("YearList")
		Old=__settings__.getSetting("OldList")
		Sort=__settings__.getSetting("SortList")
		Rating=__settings__.getSetting("RatingList")

		Cat=getList2("CatList")
		sCat=""
		for i in Cat:
			sCat=sCat+"m_act%5B"+str(CategoryDict[i])+"%5D/on/"
		if sCat == "m_act%5B%5D/on/" or sCat == "m_act%5Ball%5D/on/": sCat =""
	
		Cantry=getList2("CantryList")
		Cantrys=""
		for i in Cantry:
			Cantrys=Cantrys+","+str(CantryDict[i])
		Cantrys=Cantrys[1:]
		if Cantrys == "" or Cantrys == "0": sCantry =""
		else: sCantry = "m_act%5Bcountry%5D/"+ Cantrys+"/"

		Genre=getList2("GenreList")
		Genres=""
		for i in Genre:
			Genres=Genres+","+str(GenreDict[i])
		Genres=Genres[1:]
		if Genres == "" or Genres == "0": sGenre =""
		else: sGenre = "m_act%5Bgenre%5D/"+ Genres+"/"

		try:YearId = YearDict[Years]
		except:YearId="0"
		if YearId == "0": sYear = ""
		else: sYear = "m_act%5Bdecade%5D/"+ YearId+"/"
	
		try:OldId = OldDict[Old]
		except:OldId=""
		if OldId == "": sOld = ""
		else: sOld = "m_act%5Brestriction%5D/"+ OldId+"/"
	
		try:RatingId = RatingDict[Rating]
		except:RatingId=""
		if RatingId == "": sRating = ""
		else: sRating = "m_act%5Brating%5D/"+ RatingId+":/"
	
		try:sSort = SortDict[Sort]
		except:sSort = "order/rating"
		
		if sCat.find("is_serial%5D/on")<0 and sCat!="": sGenre=sGenre+"m_act%5Begenre%5D/999/"
		#print sCat
		#print sGenre
		link=httpSiteUrl+"/top/navigator/"+sGenre+sCantry+sYear+sRating+sOld+sCat+sSort+"/perpage/100/#results"
		
		if link=="http://www.KinoPoisk.ru/top/navigator/order/rating/perpage/100/#results": 
			link="http://www.KinoPoisk.ru/top/navigator/m_act%5Brating%5D/7:/order/rating/perpage/100/#results"
			
			
	elif md=="Popular": link="http://www.kinopoisk.ru/top/lists/186/filtr/all/sort/order/perpage/200/"
	elif md=="New": link="http://www.kinopoisk.ru/top/lists/222/"
	elif md=="Future": 
		#link="http://www.kinopoisk.ru/top/lists/220/"
		link="http://www.kinopoisk.ru/comingsoon/sex/all/sort/date/period/halfyear/"
		ss='id="top_film_'
		se='" class="item" style="z'
	elif md=="Recomend": 
		try:id = urllib.unquote_plus(get_params()["id"])
		except: id = ''
		link="http://www.kinopoisk.ru/film/"+id+"/like/"
		#print link
	elif md=="PersonFilm":
		id = get_params()["id"]
		#try:id = eval(urllib.unquote_plus(get_params()["info"]))["id"]
		#except: id = ''
		link="http://m.kinopoisk.ru/person/"+id+"/"
		ss="m.kinopoisk.ru/movie/"
		se='/">'
		#print link

	else: 
		link='http://www.kinopoisk.ru/index.php?first=no&what=&kp_query='+urllib.quote(md)
		ss="/level/1/film/"
		se='/sr/1/"'
	
	http = GET (link, httpSiteUrl)
	L=mfindal(http, ss, se)
	L2=[]
	for i in L:
		if i not in L2 and i<>"": L2.append(i)
	for i in L2:#[:-1]
		id = i[len(ss):]
		info = get_info(id)
		rating_kp = info['rating']
		if rating_kp>0: rkp = str(rating_kp)[:3]
		else: rkp= " - - "
		nru = info['title']
		
		if info['type'] !="": type = " ("+info['type']+")"
		else: type = ''
		
		if md=="Future":
			try:rkp=info['premiered'][:-5]
			except: rkp= " __.__ "
		
		try: AddItem("[ "+rkp+" ] "+nru+type, "Torrents", id, total=len(L2)-2)
		except: pass

def get_info(ID):
	try:
			if __settings__.getSetting('UpdLib')=='true': rem_inf_db(ID)
			info=eval(xt(get_inf_db(ID)))
			return info
	except:
			url="http://m.kinopoisk.ru/movie/"+ID
			http = GET (url, httpSiteUrl)
			try:http = rt(http)
			except: pass
			#debug(http)
			# ------------- ищем описание -----------------
			s='<div id="content">'
			e='<br><div class="city">'
			try: Info=mfindal(http, s, e)[0]
			except: Info=""
			#debug (Info)
			# ------------- название -----------------
			s='<p class="title">'
			e='<img src="http://m.kinopoisk.ru/images/star'
			if Info.find(e)<0: e='<div class="block film">'
			try: 
				nbl=mfindal(Info, s, e)[0][len(s):]
			except:
				nbl=""
			if nbl <> "":
				# ---------------- ru -------------------
				s='<b>'
				e='</b>'
				nru=mfindal(nbl, s, e)[0][len(s):]
				
				# ------------- en year time ------------
				s='<span>'
				e='</span>'
				nen=mfindal(nbl, s, e)[0][len(s):]
				vrn=nen.replace("'","#^").replace(",", "','")
				tmps="['"+vrn+"']"
				Lt=eval(tmps)
				n=len(Lt)
				year=0
				duration=""
				for i in Lt:
					try: year=int(i)
					except: pass
					if i[-1:]==".": duration=i
				if year>0: n2= nen.find(str(year))
				else: n2=-1
				if duration<>"":n3=nen.find(duration)
				else: n3=-1
				if n3>0 and n3<n2: n2=n3
				if n2>1: nen=nen[:n2-2]
				else: nen=nru
				
				# --------------- rus eng ----------
				rus = fs(nru)
				eng = fs(nen).replace(' (сериал)', '').replace(' (мини-сериал)', '').replace(' (ТВ)', '').replace(' (видео)', '')
				
				# ------------------ тип ----------
				type = ''
				if ' (сериал)' in rus: 
					type='сериал'
					rus = rus.replace(' (сериал)', '')
				
				if ' (мини-сериал)' in rus: 
					type='мини-сериал'
					rus = rus.replace(' (мини-сериал)', '')
				
				if ' (ТВ)' in rus:
					type='ТВ'
					rus = rus.replace(' (ТВ)', '')
				
				if ' (видео)' in rus:
					type='видео'
					rus = rus.replace(' (видео)', '')

				# ---------------- жанр  страна ----------
				s='<div class="block film">'
				e='<span class="clear"'
				try:
					b2=mfindal(Info, s, e)[0][len(s):]
					s='<span>'
					e='</span>'
					genre=mfindal(b2, s, e)[0][len(s):]
					studio=mfindal(b2, s, e)[1][len(s):]
				except:
					genre=""
					studio=""
				# ---------------- режисер ----------
				s='<span class="clear">'
				e='</a></span>'
				try:
					directors=mfindal(Info, s, e)[0][len(s):]
					s='/">'
					e='</a>'
					try: 
						director1=mfindal(directors, s, e)[0][len(s):]
						nn=directors.rfind('/">')
						director=director1+", "+directors[nn+3:]
					except:
						nn=directors.rfind('/">')
						director=directors[nn+3:]
				except:
					director=""
					
				# --------------- актеры ------------
				if director!="":
					s=directors#'<span class="clear">'
					e='<p class="descr">'
					if Info.find(e)<0:e='">...</a>'
					
					try:bcast=mfindal(Info, s, e)[0][len(s):]
					except: bcast=""
					s='/">'
					s2='/person/'
					e='</a>,'
					#lcast=mfindal(bcast, s, e)
					lactors=mfindal(bcast, s2, e)
					cast=[]
					actors={}
					for a in lactors:
						sep=a.find('/">')
						actor_name=fs(a[sep+3:])
						actor_id=fs(a[len(s2):sep])
						
						cast.append(actor_name)
						actors[actor_name]= actor_id
					
					#for i in lcast:
					#	cast.append(fs(i[3:]))
				else:
					cast=[]
					actors={}
				# ----------------  описание ----------
				s='<p class="descr">'
				e='<span class="link">'
				if Info.find(e)<0: e='<p class="margin"'
				#debug (Info)
				try:plotand=mfindal(Info, s, e)[0][len(s):]
				except:plotand=""# -----------------------------------------------------------  доделать ----------
				nn=plotand.find("</p>")
				plot=plotand[:nn].replace("<br>","").replace("<br />","")
				# ----------------- оценки ------------
				tale=plotand[nn:]
				s='</b> <i>'
				e='</i> ('
				ratings=mfindal(Info, s, e)
				try:rating_kp=float(ratings[0][len(s):])
				except:rating_kp=0
				try:rating_IMDB=float(ratings[1][len(s):])
				except: rating_IMDB=0
				
				
				# ------------------ обложка ----------
				s='//st.kp.yandex.net/images/sm_'
				e='.jpg" width="'
				try:cover='http:'+mfindal(Info, s, e)[0].replace('sm_film/','film_iphone/iphone360_')+'.jpg'
				except:cover="http://st.kp.yandex.net/images/image_none_no_border.gif"
				# ------------------ фанарт ----------
				s='//st.kp.yandex.net/images/kadr'
				e='.jpg"/></div>'
				try:fanart='http:'+mfindal(Info, s, e)[0].replace('sm_','')+'.jpg'
				except:fanart=""
				try:
					F1=mfindal(Info, s, e)
					fanarts=[]
					for fnr in F1:
						fanarts.append('http:'+fnr.replace('sm_','')+'.jpg')
				except:fanarts=[]
				
				# ---------------- премьера  ------
				s='):</b> '
				e=' ('
				nc=fs(Info).find(s)
				if nc>0:
					tmp=fs(Info)[nc : nc+90]
					if e not in tmp: e='<br>'
					nc2=tmp.find(e)
					try:
						premiered=mont2num(tmp[len(s):nc2])
						if premiered[1]==".": premiered="0"+premiered
					except: 
						premiered=" __.__.____ "
				else:
						premiered=" __.__.____ "
				#--------------
				
				info = {"title": rus, 
						"originaltitle":eng,
						"year":year, 
						"duration":duration[:-5],
						"genre":fs(genre),
						"studio":fs(studio),
						"director":fs(director),
						"cast":cast,
						"actors":actors,
						"rating":rating_kp,
						"cover":cover,
						"fanart":fanart,
						"fanarts":fanarts,
						"plot":fs(plot),
						"type":type,
						"premiered":premiered,
						"id":ID
						}
				if rating_kp>0: rkp=str(rating_kp)[:3]
				else: rkp= " - - "
				nru=fs(nru)
				#AddItem("[ "+rkp+" ] "+fs(nru), "Torrents", info, len(L2)-2)
				try:
					if rating_kp>0: add_to_db(ID, repr(info))
					#print "ADD: " + FilmID
				except:
					print "ERR: " + ID
					#print repr(info)
				return info

def mont2num(dt):
	L1=[' января ',' февраля ',' марта ',' апреля ',' мая ',' июня ',' июля ',' августа ',' сентября ',' октября ',' ноября ',' декабря ']
	L2=['.01.','.02.','.03.','.04.','.05.','.06.','.07.','.08.','.09.','.10.','.11.','.12.']
	for i in range (0,12):
		dt=dt.replace(L1[i], L2[i])
	return dt

#==============  Menu  ====================
def Root():
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	AddItem("Поиск", "Search")
	AddItem("Навигатор", "Navigator")
	AddItem("Популярные", "Popular")
	AddItem("Недавние премьеры", "New")
	AddItem("Самые ожидаемые", "Future")
	AddItem("Персоны", "PersonList")
	if len(L)>0: AddItem("Буду смотреть", "Wish_list")
	#AddItem("check", "check")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

def Search():
	SrcNavi(inputbox())

def PersonSearch():
	PS=inputbox()
	link='https://www.kinopoisk.ru/index.php?first=no&what=&kp_query='+urllib.quote(PS)
	http = GET (link, httpSiteUrl)
	ss='https://st.kp.yandex.net/images/sm_actor/'
	es='" title="'
	l1=mfindal(http,ss,es)
	for i in l1:
		if len(i) > 45 and len(i)< 550:
			n=i.find('.jpg" alt="')
			id=i[len(ss):n]
			nm=i[n+11:]
			#cover='https://st.kp.yandex.net/images/actor_iphone/iphone360_'+id+".jpg"
			#info={"cover":cover, "title":nm, "id":id}
			if len(nm)>0 and len(id)>0 :AddItem(fs(nm), "PersonFilm", id,'', len(l1))
	#debug (http)

def Navigator():
	Cats=getList("CatList")
	Genres=getList("GenreList")
	Cantrys=getList("CantryList")
	Years=__settings__.getSetting("YearList")
	Old=__settings__.getSetting("OldList")
	Sort=__settings__.getSetting("SortList")
	Rating=__settings__.getSetting("RatingList")
	
	if Cats=="": Cats="[COLOR FFFFFF00] --[/COLOR]"
	if Genres=="": Genres="[COLOR FFFFFF00]  --[/COLOR]"
	if Cantrys=="": Cantrys="[COLOR FFFFFF00] --[/COLOR]"
	if Years=="": Years="--"
	if Old=="": Old="--"
	if Rating=="": Rating="> 7"
	if Sort=="": Sort="рейтингу Кинопоиска"
	
	AddItem("Категории: " +Cats,    "SelCat")
	AddItem("Жанры:      " +Genres,  "SelGenre")
	AddItem("Страны:      " +Cantrys, "SelCantry")
	AddItem("Год:             [COLOR FFFFFF00]" +Years+"[/COLOR]",   "SelYear")
	AddItem("Возраст:      [COLOR FFFFFF00]" +Old+"[/COLOR]",     "SelOld")
	AddItem("Рейтинг:      [COLOR FFFFFF00]" +Rating+"[/COLOR]",  "SelRating")
	AddItem("Порядок:      [COLOR FFFFFF00]по " +Sort+"[/COLOR]",    "SelSort")
	
	AddItem("[B][COLOR FF00FF00][ Искать ][/COLOR][/B]", "SrcNavi")

def Torrents(id, additm=True):
	info=get_info(id)
	sys.path.append(os.path.join(addon.getAddonInfo('path'),"src"))
	ld=os.listdir(os.path.join(addon.getAddonInfo('path'),"src"))
	L2=[]
	Lz=[]
	for i in ld:
		if i[-3:]=='.py': 
			try:
				exec ("import "+i[:-3]+"; skp="+i[:-3]+".Tracker()")
				L = skp.Search(info)
			except: L=[]
			for D in L:
				url = D['url']
				try:    tor_title=D['title'].encode('utf-8').replace("«",'').replace("»",'').replace('"', '')
				except: tor_title=D['title'].replace("«",'').replace("»",'').replace('"', '')
				#print tor_title
				ru_title=info['title'].replace("«",'').replace("»",'').replace('"', '')
				#print ru_title
				en_title=info['originaltitle'].replace("«",'').replace("»",'').replace('"', '')
				year=str(info['year'])
				year2=str(info['year']+1)
				
				if (ru_title in tor_title or ru_title in tor_title) and (year in tor_title or year2 in tor_title or info['type']!=''):
					size = D['size']
					if 'MB' in size and '.' in size: size=size[:size.find('.')]
					size = size.replace('GB','').replace('MB','').strip()
					if size not in Lz or __settings__.getSetting("CutSize") == 'false':
						Lz.append(size)
						Z=D['size']
						if 'GB' in Z and Z.find('.') == 2: Z=Z[:3]+Z[4:]
						title=xt(mid(Z, 10))+" | "+xt(mids(D['sids'], 6))+" | "+xt(D['title'])
						title=get_label(xt(D['title']))+" "+title
						if additm:
							if __settings__.getSetting("SortLst") == 'true' and info['type']=='':
								pr=fnd(D)
								#ratio=str(get_rang(D))+" "
								if pr: title=FC(title, 'FEFFFFFF')
								else:  title=FC(title.replace("[COLOR F", "[COLOR 7"), 'FF777777')
							AddItem(title, "OpenTorrent", id, url)
						L2.append(D)
				#print D
	return L2
def get_label(text):
	text=lower(text)#.lower()
	#print text
	if 'трейлер'  in text: return FC('[ Трейл.]',    'FF999999')
	if ' кпк'     in text: return FC('[   КПК  ]',   'FFF8888F')
	if 'telesyn'  in text: return FC('[    TS    ]', 'FFFF2222')
	if 'telecin'  in text: return FC('[    TS    ]', 'FFFF2222')
	if 'camrip'   in text: return FC('[    TS    ]', 'FFFF2222')
	if ' ts'      in text: return FC('[    TS    ]', 'FFFF2222')
	if 'dvdscr'   in text: return FC('[    Scr   ]', 'FFFF2222')
	if ' 3d'      in text: return FC('[    3D    ]', 'FC45FF45')
	if '720'      in text: return FC('[  720p  ]',   'FBFFFF55')
	if '1080'     in text: return FC('[ 1080p ]',    'FAFF9535')
	if 'blu-ray'  in text: return FC('[  BRay  ]',   'FF5555FF')
	if 'bdremux'  in text: return FC('[    BD    ]', 'FF5555FF')
	if ' 4k'      in text: return FC('[    4K    ]', 'FF5555FF')
	if 'bdrip'    in text: return FC('[ BDRip ]',    'FE98FF98')
	if 'drip'     in text: return FC('[ BDRip ]',    'FE98FF98')
	if 'hdrip'    in text: return FC('[ HDRip ]',    'FE98FF98')
	if 'webrip'   in text: return FC('[  WEB   ]',   'FEFF88FF')
	if 'WEB'      in text: return FC('[  WEB   ]',   'FEFF88FF')
	if 'web-dl'   in text: return FC('[  WEB   ]',   'FEFF88FF')
	if 'hdtv'     in text: return FC('[ HDTV ]',     'FEFFFF88')
	if 'tvrip'    in text: return FC('[    TV    ]', 'FEFFFF88')
	if 'satrip'   in text: return FC('[    TV    ]', 'FEFFFF88')
	if 'dvb '     in text: return FC('[    TV    ]', 'FEFFFF88')
	if 'dvdrip'   in text: return FC('[DVDRip]',     'FE88FFFF')
	if 'dvd5'     in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'xdvd'     in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'dvd-5'    in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'dvd-9'    in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'dvd9'     in text: return FC('[  DVD   ]',   'FE88FFFF')
	return FC('[   ????  ]', 'FFFFFFFF')

def OpenTorrent(url, id):
	#print url
	torrent_data = GETtorr(url)
	if torrent_data != None:
		import bencode
		torrent = bencode.bdecode(torrent_data)
		cover = get_info(id)['cover']
		try:
			L = torrent['info']['files']
			ind=0
			for i in L:
				name=ru(i['path'][-1])
				#size=i['length']
				listitem = xbmcgui.ListItem(name, iconImage=cover, thumbnailImage=cover)
				listitem.setProperty('IsPlayable', 'true')
				uri = sys.argv[0]+'?mode=PlayTorrent&id='+id+'&ind='+str(ind)+'&url='+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle, uri, listitem)
				ind+=1
		except:
				ind=0
				name=torrent['info']['name']
				listitem = xbmcgui.ListItem(name, iconImage=cover, thumbnailImage=cover)
				listitem.setProperty('IsPlayable', 'true')
				listitem.addContextMenuItems([('[B]Сохранить фильм(STRM)[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Save_strm&id='+id+'&url='+urllib.quote_plus(url)+'")'),])
				uri =sys.argv[0]+'?mode=PlayTorrent&id='+id+'&ind='+str(ind)+'&url='+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle, uri, listitem)

def get_item_name(url, ind):
	torrent_data = GETtorr(url)
	if torrent_data != None:
		import bencode
		torrent = bencode.bdecode(torrent_data)
		try:
			L = torrent['info']['files']
			name=L[ind]['path'][-1]
		except:
			name=torrent['info']['name']
		return name
	else:
		return ' '

def check():
	print "check"
	SaveDirectory = __settings__.getSetting("SaveDirectory")
	if SaveDirectory=="":SaveDirectory=LstDir
	
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	for id in L:
		info=get_info(id)
		year=info["year"]
		name = info['originaltitle'].replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		if os.path.isfile(os.path.join(fs_enc(SaveDirectory),fs_enc(name+".strm")))==False:
			L=Torrents(id, False)
			url=''
			rang=0
			for i in L:
				if fnd(i):
					rang_i=get_rang(i)
					if rang_i>rang:
						rang=rang_i
						url=i['url']
			
			if url != "":
					if __settings__.getSetting("NFO2")=='true': save_film_nfo(id)
					save_strm (i['url'], 0, id)


def alter(id, url=''):
		SaveDirectory = __settings__.getSetting("SaveDirectory")
		if SaveDirectory=="":SaveDirectory=LstDir
		info=get_info(id)
		year=info["year"]
		name = info['originaltitle'].replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		L=Torrents(id, False)
		try:W_list=eval(__settings__.getSetting("W_list"))
		except: W_list=[]
		for i in L:
			newurl=i['url'].replace('new-ru.org','').replace('open-tor.org','')
			oldurl=url.replace('new-ru.org','').replace('open-tor.org','')
			if fnd(i) and newurl!=oldurl:
				if id in W_list:
					if __settings__.getSetting("NFO2")=='true': save_film_nfo(id)
					save_strm (i['url'], 0, id)
				return i['url']

def autoplay(id):
		L=Torrents(id, False)
		url=''
		for i in L:
			if fnd(i): 
				url=i['url']
				break
		if url !='': play(url,0,id)
		else: 
			if len(L)== 0: showMessage("Кинопоиск", "Фильм не найден")
			else: showMessage("Кинопоиск", "Нет нужного качества")

def review(id):
	url='https://m.kinopoisk.ru/reviews/'+id
	http=GET(url)
	ss='<span class="bold">'
	es='&raquo;</a></p>'
	L=mfindal(http,ss,es)
	#debug(L[0])
	Lt=[]
	Lu=[]
	for i in L:
		if "hand_good.gif" in i: rating = FC('+', 'FF33FF33')
		elif "hand_bad.gif" in i: rating = FC(' - ', 'FFFF3333')
		else: rating = FC(' - ', '01003333')
		ss='<i>'
		es='&nbsp;'
		if rating == FC(' - ', '01003333'): es='</i></span>'
		date=mfindal(i,ss,es)[0][3:]
		
		ss='<p class="head">'
		es='</p>'
		head=mfindal(i,ss,es)[0][len(ss):]
		
		ss='review/'
		es='/">'
		url='https://m.kinopoisk.ru/review/'+mfindal(i,ss,es)[0][len(ss):]
		
		Lt.append('['+rating+'] '+ date+" - "+rt(fs(head)))
		Lu.append(url)
	sel = xbmcgui.Dialog()
	r = sel.select("Рецензии:", Lt)
	if r >=0:
		http2=GET(Lu[r])
		#debug (http2)
		n=http2.find('</p><br>')
		k=http2.find('<div id="bottom">')
		text=http2[n:k].replace('<b>','').replace('</b>','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','').replace('<br>','').replace('<br />','').replace('</div>','')
		text=rt(fs(text))
		heading=Lt[r]
		showText(heading, text)

def showText(heading, text):
	id = 10147
	xbmc.executebuiltin('ActivateWindow(%d)' % id)
	xbmc.sleep(500)
	win = xbmcgui.Window(id)
	retry = 50
	while (retry > 0):
		try:
			xbmc.sleep(10)
			retry -= 1
			win.getControl(1).setLabel(heading)
			win.getControl(5).setText(text)
			return
		except:
			pass

def fnd(D):
	BL=['Трейлер', "Тизер"]
	if __settings__.getSetting("F_Qual") != "0":BL.extend([' TS','TeleSyn','TeleCin','TELECIN',' CAM',' CamRip','screen','Screen'])
	WL=[]
	if __settings__.getSetting("F_Qual1") == 'true': WL.append("dvdrip")
	if __settings__.getSetting("F_Qual2") == 'true': WL.append("webrip")
	if __settings__.getSetting("F_Qual3") == 'true': WL.append("web-dl")
	if __settings__.getSetting("F_Qual4") == 'true': WL.append("bdrip")
	if __settings__.getSetting("F_Qual5") == 'true': WL.append("hdrip")
	if __settings__.getSetting("F_Qual6") == 'true': WL.append("tvrip")
	if __settings__.getSetting("F_Qual7") == 'true': WL.append("hdtv")
	if __settings__.getSetting("F_Qual8") == 'true': WL.append("blu-ray")
	if __settings__.getSetting("F_Qual9") == 'true': WL.append("720p")
	if __settings__.getSetting("F_Qual10")== 'true': WL.append("1080p")
	if __settings__.getSetting("F_Qual") == '0': WL=[]

	size1 = int(__settings__.getSetting("F_Size1"))
	size2 = int(__settings__.getSetting("F_Size2"))
	if size2 == 0: size2 = 999
	
	b=0
	q=0
	z=0
	Title = D['title']
	try:Title=Title+' '+D['quality']
	except:pass
	
	try:Title=Title.encode('utf-8')
	except: Title=xt(Title)
	
	for i in BL:
		if Title.find(i)>0:b+=1
	
	if __settings__.getSetting("F_Qual") == "0":
		q=1
	else:
		for i in WL:
			if Title.lower().find(i)>0:q+=1
		
	if 'ГБ' in xt(D['size']) or 'GB' in xt(D['size']):
			szs=xt(D['size']).replace('ГБ','').replace('GB','').replace('|','').strip()
			sz=float(szs)
			if sz>size1 and sz<size2 : z=1
	else: z=0
	
	#print Title
	#if b <> 0: print 'Попал в Черный список'
	#if q == 0: print 'Низкое Качество'
	#if z == 0: print 'Не тот Размер'
	
	if b == 0 and q > 0 and z > 0:
	#	print 'Файл найден'
		return True
	else: 
		return False

def get_rang(D):
	Title = D['title']
	try:Title=Title+' '+D['quality']
	except:pass
	try:Title=Title.encode('utf-8')
	except: Title=xt(Title)
	Title=Title.lower()
	ratio=0
	WL=[]
	if __settings__.getSetting("F_Qual1") == 'true' and "dvdrip"  in Title:   ratio+=40
	if __settings__.getSetting("F_Qual2") == 'true' and "webrip"  in Title:   ratio+=30
	if __settings__.getSetting("F_Qual3") == 'true' and "web-dl"  in Title:   ratio+=30
	if __settings__.getSetting("F_Qual4") == 'true' and "bdrip"   in Title:   ratio+=80
	if __settings__.getSetting("F_Qual5") == 'true' and "hdrip"   in Title:   ratio+=80
	if __settings__.getSetting("F_Qual6") == 'true' and "tvrip"   in Title:   ratio+=20
	if __settings__.getSetting("F_Qual7") == 'true' and "hdtv"    in Title:   ratio+=70
	if __settings__.getSetting("F_Qual8") == 'true' and "blu-ray" in Title:   ratio+=20
	
	if __settings__.getSetting("F_Qual9") == 'true' and '720p'    in Title:   ratio+=1000
	if __settings__.getSetting("F_Qual10")== 'true' and "1080p"   in Title:   ratio+=2000
	
	size1 = int(__settings__.getSetting("F_Size1"))
	size2 = int(__settings__.getSetting("F_Size2"))
	if size2 == 0: size2 = 10
	size=(size2-size1)/2+size1
	
	if 'ГБ' in xt(D['size']) or 'GB' in xt(D['size']):
			szs=xt(D['size']).replace('ГБ','').replace('GB','').replace('|','').strip()
			sz=float(szs)
			#print size
			#print sz
			#print abs(sz-size)
			#print '----'
			if   abs(sz-size)<1 : ratio+=900
			elif abs(sz-size)<2 : ratio+=800
			elif abs(sz-size)<3 : ratio+=700
			elif abs(sz-size)<4 : ratio+=600
			elif abs(sz-size)<5 : ratio+=500
			elif abs(sz-size)<6 : ratio+=400
			elif abs(sz-size)<7 : ratio+=300
			elif abs(sz-size)<8 : ratio+=200
			elif abs(sz-size)<9 : ratio+=100
	
	sids=D['sids']
	if len(sids)==1: ratio+=11
	if len(sids)==2: ratio+=44
	if len(sids)==3: ratio+=66
	if len(sids)==4: ratio+=88
	if len(sids)==5: ratio+=99
	if sids =='0': ratio-=500
	if sids =='1': ratio-=100
	if sids =='2': ratio-=50
	return ratio


try:    mode = urllib.unquote_plus(get_params()["mode"])
except: mode = None
try:    url = urllib.unquote_plus(get_params()["url"])
except: url = None
try:    info = eval(urllib.unquote_plus(get_params()["info"]))
except: info = {}
try:    id = str(get_params()["id"])
except: id = '0'
try:    ind = int(get_params()["ind"])
except: ind = 0


if mode == None:
	setList("CatList", Category)
	setList("GenreList", Genre)
	setList("CantryList", Cantry)
	__settings__.setSetting(id="YearList", value="")
	__settings__.setSetting(id="OldList", value="")
	__settings__.setSetting(id="SortList", value="")
	__settings__.setSetting(id="RatingList", value="")
	Root()

if mode == "Search":
	Search()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Navigator":
	Navigator()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Popular":
	SrcNavi("Popular")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "New":
	SrcNavi("New")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Future":
	SrcNavi("Future")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Recomend":
	SrcNavi("Recomend")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PersonFilm":
	SrcNavi("PersonFilm")#+PeID
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Person":
	Person()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PersonList":
	AddItem("[ Поиск ]", "PersonSearch")
	PersonList()
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PersonSearch": 
	PersonSearch()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "AddPerson": 
	AddPerson(info)

if mode == "RemovePerson": 
	RemovePerson(info)
	xbmc.executebuiltin("Container.Refresh()")
	
if mode == "SrcNavi":
	SrcNavi()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "SelCat":
	import SelectBox
	SelectBox.run("CatList")

if mode == "SelGenre":
	import SelectBox
	SelectBox.run("GenreList")

if mode == "SelCantry":
	import SelectBox
	SelectBox.run("CantryList")
	
if mode == "SelYear":
	sel = xbmcgui.Dialog()
	r = sel.select("Десятилетие:", Year)
	__settings__.setSetting(id="YearList", value=Year[r])

if mode == "SelOld":
	sel = xbmcgui.Dialog()
	r = sel.select("Возраст:", Old)
	__settings__.setSetting(id="OldList", value=Old[r])

if mode == "SelSort":
	sel = xbmcgui.Dialog()
	r = sel.select("Десятилетие:", Sort)
	__settings__.setSetting(id="SortList", value=Sort[r])

if mode == "SelRating":
	sel = xbmcgui.Dialog()
	r = sel.select("Десятилетие:", Rating)
	__settings__.setSetting(id="RatingList", value=Rating[r])

if mode == "Torrents" or mode == "Torrents2":
	Torrents(id)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.endOfDirectory(handle)
	xbmc.sleep(300)
	xbmc.executebuiltin("Container.SetViewMode(51)")

if mode == "OpenTorrent":
	OpenTorrent(url, id)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PlayTorrent":
	play(url, ind, id)

if mode == "play_url2": #совместимость с 1.0
	url = urllib.unquote_plus(get_params()["torr_url"])
	play(url, ind, id)

if mode == "Add2List":
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	L.append(id)
	__settings__.setSetting("W_list", repr(L))

if mode == "RemItem":
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	L.remove(id)
	__settings__.setSetting("W_list", repr(L))
	xbmc.executebuiltin("Container.Refresh()")

if mode == "Wish_list":
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	for id in L:
		info=get_info(str(id))
		rus=info["title"]
		AddItem(rus, 'Wish', id)
	xbmcplugin.endOfDirectory(handle)

if mode == "Wish":
	Torrents(id)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PlayTrailer":
	trailer=get_trailer(id)
	if trailer!='':
		info=get_info(str(id))
		cover=info['cover']
		title=info['title']
		listitem = xbmcgui.ListItem("trailer", path=trailer,iconImage=cover, thumbnailImage=cover)
		listitem.setInfo(type = "Video", infoLabels = get_labels(info))
		xbmc.Player().play(trailer, listitem)
		xbmcplugin.endOfDirectory(handle, False, False)

if mode == "Save_strm":
	if __settings__.getSetting("NFO2")=='true': save_film_nfo(id)
	save_strm (url, 0, id)

if mode == "check":
	check()

if mode == "Review":
	review(id)

if mode == "Autoplay":
	autoplay(id)

c.close()