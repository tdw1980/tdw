#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,sys,os,random
import xbmcplugin,xbmcgui,xbmcaddon
import time

addon = xbmcaddon.Addon(id='plugin.audio.zaycev.net')
pluginhandle = int(sys.argv[1])
thumb = os.path.join( addon.getAddonInfo('path'), 'icon.png')
xbmcplugin.setContent(int(sys.argv[1]), 'songs')
__settings__ = xbmcaddon.Addon(id='plugin.audio.zaycev.net')

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



def getURL(url,Referer = 'http://www.mds-fm.ru/'):
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


def Format(t):
	title =t
	return title

def Root():
				title="Поиск"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=title'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="Жанры"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=genres'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)


				xbmcplugin.endOfDirectory(pluginhandle)

def Title():
	q=inputbox().replace(" ","+")
	Lt=[]
	for n in range (1,5):
		url='http://zaycev.net/search.html?query_search='+q
		if n>0: url=url+"&page="+str(n)
		http=getURL(url)
		try:
			ss='<div data-dkey='
			es='</i></span></a></div>'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
				ss='<div data-dkey="'
				es='.mp3" data-duration="'
				url="http://dl.zaycev.net"+mfindal(i, ss, es)[0][len(ss):]+"/play.mp3"
				
				ss='href="/artist/'
				es='</a></div><div class="musicset-track__track-dash'
				artist=mfindal(i, ss, es)[0]
				artist=artist[artist.find('">')+2:]
				
				ss='target="_blank" >'
				es='</a></div></div><div class="musicset-track__duration'
				title=mfindal(i, ss, es)[0][len(ss):]
				
				title2 = artist+" - "+title
				
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title, 'artist':artist})
				if url not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
					Lt.append(url)
				
	xbmcplugin.endOfDirectory(pluginhandle)



def Genres():
		L=[('pop', 'Поп'), ("rock", "Рок"), ("rap", "Рэп"), ("alternative", "Альтернатива"), ("electronic", "Электроника"), ("shanson", "Шансон"), ("soundtrack", "Саундтреки"), ("metal", "Метал"), ("classical", "Классика"), ("dance", "Танцевальная"), ("easy", "Легкая"), ("rnb", "R’n’B"), ("jazz", "Джаз"), ("reggae", "Регги"), ("other", "Другое")]
		for i in L:
			#for n in range (1,10):
				id, title=i
				url="http://zaycev.net/genres/"+id+"/index_"
				img=thumb
				uri = sys.argv[0] + '?mode=serchgenres'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
		xbmcplugin.endOfDirectory(pluginhandle)

def SerchGenres(url):
				title="[COLOR F050F050] [ Новинки ] [/COLOR]"
				img=thumb
				uri = sys.argv[0] + '?mode=serchgenres'
				uri += '&url='  + urllib.quote_plus(url.replace("index_","new_"))
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				if url.find("index_")>0: xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				for n in range (1,5):
					url2=url+str(n)+".html"
					Serch(url2.replace("index_1","index").replace("new_1","new"))
				xbmcplugin.endOfDirectory(pluginhandle)

def Plot():
		L=[('623','Бессмертие'), ('736','Вампиры'), ('741','Вторжение «Чужих»'), ('609','Генетические эксперименты, мутации'), ('702','Договор с нечистой силой'), ('686','Жизнь после смерти'), ('881','Звёздный ковчег'), ('616','Изобретения и научные исследования'), ('601','Искусственный интеллект'), ('658','Квест'), ('922','Клоны и клонирование'), ('590','Контакт'), ('593','Ксенофантастика'), ('939','Наши в другом мире'), ('761','Наши в прошлом'), ('993','Обмен разумов, перемещение разума'), ('786','Полая Земля, путешествия под землю'), ('738','Последний человек/люди на Земле'), ('1394','природные катаклизмы'), ('795','Прогрессорство'), ('898','Пророчество'), ('856','Реликты'), ('669','Робинзонада'), ('662','Роботы'), ('776','Сверхъестественные способности, супергерои'), ('685','Спасение мира'), ('743','Спецслужбы'), ('613','Становление/взросление героя'), ('1393','Стихийные бедствия'), ('747','Стихийные бедствия, природные катаклизмы'), ('894','Тёмный властелин'), ('788','Терраформирование'), ('651','Умирающая Земля')]
		for i in L:
				id, title=i
				url="http://mds-fm.ru/book?p="+id+"#"
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
		xbmcplugin.endOfDirectory(pluginhandle)

def Scene():
		L=[('656','Альтернативная история нашего мира/Земли'), ( '941','Виртуальная реальность'), ( '597','Вне Земли'), ( '721','Вторичный литературный мир'), ( '633','Другой мир, не связанный с нашим'), ( '724','Загробный мир'), ( '1398','Луна'), ( '584','Наш мир/Земля'), ( '1366','Открытый космос'), ( '847','Параллельный мир/вселенная'), ( '1367','Планеты других звездных систем'), ( '1420','спутники Юпитера'), ( '1419','Юпитер ')]
		for i in L:
				id, title=i
				url="http://mds-fm.ru/book?s="+id+"#"
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
		xbmcplugin.endOfDirectory(pluginhandle)



def Time():
		L=[('679','20 век'), ('589','21 век'), ('607','Близкое будущее'), ('598','Далёкое будущее'), ('1373','Дочеловеческие времена'), ('765','Древний мир'), ('831','Каменный век'), ('657','Неопределенное время действия'), ('829','Новое время (17-19 века)'), ('980','Очень далёкое будущее'), ('861','Позднее средневековье / Эпоха возрождения'), ('1159','Средние века'), ('897','Эпоха географических открытий (15-16 века)')]
		for i in L:
				id, title=i
				url="http://mds-fm.ru/book?t="+id+"#"
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
		xbmcplugin.endOfDirectory(pluginhandle)


def Serch(url):
		Lt=[]
		http=getURL(url)
		try:
			ss='<div data-dkey='
			es='</i></span></a></div>'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
				ss='<div data-dkey="'
				es='.mp3" data-duration="'
				url="http://dl.zaycev.net"+mfindal(i, ss, es)[0][len(ss):]+"/play.mp3"
				
				ss='href="/artist/'
				es='</a></div><div class="musicset-track__track-dash'
				artist=mfindal(i, ss, es)[0]
				artist=artist[artist.find('">')+2:]
				
				ss='target="_blank" >'
				es='</a></div></div><div class="musicset-track__duration'
				title=mfindal(i, ss, es)[0][len(ss):]
				
				title2 = artist+" - "+title
				
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title, 'artist':artist})
				if url not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
					Lt.append(url)


params = get_params()
url  =	'http://zaycev.net'
mode =	None
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



if   mode == None:		Root()
elif mode == 'title':	Title()
elif mode == 'genres':	Genres()
elif mode == 'plot':	Plot()
elif mode == 'scene':	Scene()
elif mode == 'time':	Time()
elif mode == 'serch':	Serch(url)
elif mode == 'serchgenres':	SerchGenres(url)

elif mode == 'play':	Play(url)

