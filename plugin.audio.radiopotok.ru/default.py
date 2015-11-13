#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,sys,os,random
import xbmcplugin,xbmcgui,xbmcaddon
import time

pluginhandle = int(sys.argv[1])
xbmcplugin.setContent(int(sys.argv[1]), 'music')
__settings__ = xbmcaddon.Addon(id='plugin.audio.radiopotok.ru')
thumb = os.path.join( __settings__.getAddonInfo('path'), 'icon.png')

def showMessage(heading, message, times = 3000):
	heading = heading.encode('utf-8')
	message = message.encode('utf-8')
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, thumb))


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



def getURL(url,Referer = 'http://www.radiopotok.ru/'):
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
		#sn=http[s:]
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L


def Root(url="http://radiopotok.ru/radiostations/"):
	title="[COLOR F050F050][B]ПОИСК[/B][/COLOR]"
	uri = sys.argv[0] + '?mode=Category'
	item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
	xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
	
	title="[COLOR F050F050][B]ИЗБРАННОЕ[/B][/COLOR]"
	uri = sys.argv[0] + '?mode=Favorites'
	item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
	xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

	if url=="":url="http://radiopotok.ru/radio/774/"
	http = getURL(url)
	http = http.replace(chr(10),"").replace(chr(13),"").replace('	',"")
	#print http
	ss = 'div class="item-image col'
	es = '<div class="clearfix"></div></div><br>'
	L1=mfindal(http, ss, es)
	if len (L1)==0: 
		es = '<div class="clearfix"></div><br>'
		L1=mfindal(http, ss, es)
	#print L1
	for i in L1:
			#print i
			ss = '.jpg" alt="'
			es = '"></a></div><div'
			try:title=mfindal(i, ss, es)[0][len(ss):]
			except:
				es = '"></div><div class="item-body col-xs-9'
				try:title=mfindal(i, ss, es)[0][len(ss):]
				except:title="err"
				
			#ss = 'class="item-text">'
			#es = '</p></div>'
			#text=mfindal(i, ss, es)[0][len(ss):].replace('&#8230;',"...")
			try:
				ss = 'data-id="'
				es = '" data-tagstate'
				id=mfindal(i, ss, es)[0][len(ss):]

				url = "http://radiopotok.ru/f/m3u/station_"+id+".m3u"
				img = "http://radiopotok.ru/f/station/s_"+id+".jpg"
				#title=dbr+Li[5]+" FM"+"  -  [B]"+Li[4] +"[/B]"
				uri = sys.argv[0] + '?mode=PlayStation'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				
				urc1 = sys.argv[0] + '?mode=add'
				urc1 += '&url='  + urllib.quote_plus(id)
				urc1 += '&name='  + urllib.quote_plus(title)
				item.addContextMenuItems([('[COLOR F050F050] Добавить в избранное [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/'+urc1+'")'),('[COLOR F050F050] Избранное [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/?mode=Favorites")')])
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
			except:
				print "err: " +i
	xbmcplugin.endOfDirectory(pluginhandle)

def dir(url="http://radiopotok.ru/radiostations/"):
	http = getURL(url)
	http = http.replace(chr(10),"").replace(chr(13),"").replace('	',"")
	#print http
	ss = 'div class="item-image col'
	es = '<div class="clearfix"></div></div><br>'
	L1=mfindal(http, ss, es)
	if len (L1)==0: 
		es = '<div class="clearfix"></div><br>'
		L1=mfindal(http, ss, es)
	#print L1
	for i in L1:
			#print i
			ss = '.jpg" alt="'
			es = '"></a></div><div'
			try:title=mfindal(i, ss, es)[0][len(ss):]
			except:
				es = '"></div><div class="item-body col-xs-9'
				try:title=mfindal(i, ss, es)[0][len(ss):]
				except:title="err"
				
			#ss = 'class="item-text">'
			#es = '</p></div>'
			#text=mfindal(i, ss, es)[0][len(ss):].replace('&#8230;',"...")
			try:
				ss = 'data-id="'
				es = '" data-tagstate'
				id=mfindal(i, ss, es)[0][len(ss):]

				url = "http://radiopotok.ru/f/m3u/station_"+id+".m3u"
				img = "http://radiopotok.ru/f/station/s_"+id+".jpg"
				#title=dbr+Li[5]+" FM"+"  -  [B]"+Li[4] +"[/B]"
				uri = sys.argv[0] + '?mode=PlayStation'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				
				urc1 = sys.argv[0] + '?mode=add'
				urc1 += '&url='  + urllib.quote_plus(id)
				urc1 += '&name='  + urllib.quote_plus(title)
				item.addContextMenuItems([('[COLOR F050F050] Добавить в избранное [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/'+urc1+'")'),('[COLOR F050F050] Избранное [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/?mode=Favorites")')])
				if title!="":xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
			except:
				print "err: " +i
	xbmcplugin.endOfDirectory(pluginhandle)

def PlayStation(url,name,img):
	http = getURL(url)
	L=http.splitlines()
	for i in L:
		if i[:4]=="http": url=i
		if i[:4]=="rtmp": url=i
	item = xbmcgui.ListItem(name, iconImage = img, thumbnailImage = img)
	item.setInfo(type="Music", infoLabels={"Title": name})
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(url, item)

def add(id, name):
	try:L=eval(__settings__.getSetting("Favorites"))
	except:L=[]
	L.append((id,name))
	__settings__.setSetting("Favorites",repr(L))


def rem(id):
	try:L=eval(__settings__.getSetting("Favorites"))
	except:L=[]
	L2=[]
	for i in L:
		if i[0] != id: L2.append(i)
	__settings__.setSetting("Favorites",repr(L2))


def Favorites():
	L=eval(__settings__.getSetting("Favorites"))
	if len(L)==0 and __settings__.getSetting("FP")=="1":
		title="[COLOR F050F050][B]ПОИСК[/B][/COLOR]"
		uri = sys.argv[0] + '?mode=Category'
		item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
		xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

	for i in L:
			title=i[1]
			id  = i[0]
			url = "http://radiopotok.ru/f/m3u/station_"+id+".m3u"
			img = "http://radiopotok.ru/f/station/s_"+id+".jpg"
			
			uri = sys.argv[0] + '?mode=PlayStation'
			uri += '&url='  + urllib.quote_plus(url)
			uri += '&name='  + urllib.quote_plus(title)
			uri += '&img='  + urllib.quote_plus(img)
			item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
			item.setInfo(type="Music", infoLabels={"Title": title})
			
			urc1 = sys.argv[0] + '?mode=rem'
			urc1 += '&url='  + urllib.quote_plus(id)
			urc1 += '&name='  + urllib.quote_plus(title)

			item.addContextMenuItems([('[COLOR F050F050] Удалить [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/'+urc1+'")'),('[COLOR F050F050] Поиск станций [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/?mode=Category")')])

			xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
	xbmcplugin.endOfDirectory(pluginhandle)


GenreList=[
("http://radiopotok.ru/catalog/radio/classic-music/","[COLOR F050F050][B]--------   Жанры   -------[/B][/COLOR]"),
("http://radiopotok.ru/catalog/radio/classic-music/","Классика"),
("http://radiopotok.ru/rating/radio/radio_jazz/","Джаз"),
("http://radiopotok.ru/rating/radio/classic_rock/","Рок"),
("http://radiopotok.ru/radio/91/","Поп"),
("http://radiopotok.ru/radio/100/","Клубная"),
("http://radiopotok.ru/radio/178/","Хип Хоп"),
("http://radiopotok.ru/radio/499/","Чилаут"),
("http://radiopotok.ru/radio/107/","Детское"),
("http://radiopotok.ru/radio/774/", "[COLOR F050F050][B]--------  Города  -------[/B][/COLOR]"),
("http://radiopotok.ru/radio/847/", "Барнаул"), 
("http://radiopotok.ru/radio/839/", "Воронеж"), 
("http://radiopotok.ru/radio/751/", "Екатеринбург"), 
("http://radiopotok.ru/radio/818/", "Иркутск"), 
("http://radiopotok.ru/radio/843/", "Казань"), 
("http://radiopotok.ru/radio/835/", "Кемерово"), 
("http://radiopotok.ru/radio/783/", "Краснодар"), 
("http://radiopotok.ru/radio/742/", "Красноярск"), 
("http://radiopotok.ru/radio/774/", "Москва"), 
("http://radiopotok.ru/radio/786/", "Нижний Новгород"), 
("http://radiopotok.ru/radio/760/", "Новосибирск"), 
("http://radiopotok.ru/radio/855/", "Оренбург"), 
("http://radiopotok.ru/radio/820/", "Пермь"), 
("http://radiopotok.ru/radio/811/", "Ростов-На-Дону"), 
("http://radiopotok.ru/radio/792/", "Самара"), 
("http://radiopotok.ru/radio/765/", "Санкт-Петербург"), 
("http://radiopotok.ru/radio/850/", "Саратов"), 
("http://radiopotok.ru/radio/853/", "Ставрополь"), 
("http://radiopotok.ru/radio/806/", "Уфа"), 
("http://radiopotok.ru/radio/797/", "Челябинск")
]

def Category():
		title="[COLOR F050F050][B]ВСЕ СТАНЦИИ[/B][/COLOR]"
		img=thumb
		uri = sys.argv[0] + '?mode=all'
		uri += '&url='  + urllib.quote_plus("0")
		item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
		xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

		for i in GenreList:
			title=i[1]
			url=i[0]
			img=thumb
			uri = sys.argv[0] + '?mode=dir'
			uri += '&url='  + urllib.quote_plus(url)
			uri += '&name='  + urllib.quote_plus(title)
			uri += '&img='  + urllib.quote_plus(img)
			item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
			xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
		xbmcplugin.endOfDirectory(pluginhandle)

def Stations(url="http://radiopotok.ru/radiostations/"):
	http = getURL(url)
	http = http.replace(chr(10),"").replace(chr(13),"").replace('	',"")
	#print http
	ss = 'div class="item-image col'
	es = '<div class="clearfix"></div></div><br>'
	L1=mfindal(http, ss, es)
	if len (L1)==0: 
		es = '<div class="clearfix"></div><br>'
		L1=mfindal(http, ss, es)
	#print L1
	for i in L1:
			#print i
			ss = '.jpg" alt="'
			es = '"></a></div><div'
			try:title=mfindal(i, ss, es)[0][len(ss):]
			except:
				es = '"></div><div class="item-body col-xs-9'
				try:title=mfindal(i, ss, es)[0][len(ss):]
				except:title="err"
				
			#ss = 'class="item-text">'
			#es = '</p></div>'
			#text=mfindal(i, ss, es)[0][len(ss):].replace('&#8230;',"...")
			try:
				ss = 'data-id="'
				es = '" data-tagstate'
				id=mfindal(i, ss, es)[0][len(ss):]

				url = "http://radiopotok.ru/f/m3u/station_"+id+".m3u"
				img = "http://radiopotok.ru/f/station/s_"+id+".jpg"
				#title=dbr+Li[5]+" FM"+"  -  [B]"+Li[4] +"[/B]"
				uri = sys.argv[0] + '?mode=PlayStation'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				
				urc1 = sys.argv[0] + '?mode=add'
				urc1 += '&url='  + urllib.quote_plus(id)
				urc1 += '&name='  + urllib.quote_plus(title)
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/'+urc1+'")'),('[COLOR F050F050] Избранное [/COLOR]', 'Container.Update("plugin://plugin.audio.radiopotok.ru/?mode=Favorites")')])
				if title!="":xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True,100)
			except:
				print "err: " +i

def all(d=""):
	if d=="0": d=""
	for n in range(0,9):
		url="http://radiopotok.ru/radiostations/page-"+d+str(n+1)+".html"
		print url
		Stations(url)
		
	if d=="": d="1"
	else: d=str(int(d)+1)
	
	title="[COLOR F050F050][B]"+d+" Далее >[/B][/COLOR]"
	uri = sys.argv[0] + '?mode=all'
	uri += '&url='  + urllib.quote_plus(d)
	item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
	xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
	
	xbmcplugin.endOfDirectory(pluginhandle)



params = get_params()
url  =	''
mode =	"Root"
name =	''
img =	' '

try: url = urllib.unquote_plus(params["url"])
except: pass
try: mode = urllib.unquote_plus(params["mode"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: img = urllib.unquote_plus(params["img"])
except: pass


if   mode == "Root":
	if __settings__.getSetting("FP")=="1" and url=="":Favorites()
	else:Root(url)
elif mode == 'PlayStation':	PlayStation(url,name,img)
elif mode == 'add':			add(url,name)
elif mode == 'rem':			rem(url)
elif mode == 'Favorites':	Favorites()
elif mode == 'Category':	Category()
elif mode == 'all':			all(url)
elif mode == 'dir':			dir(url)