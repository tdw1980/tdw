#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,sys,os,random
import xbmcplugin,xbmcgui,xbmcaddon
import time

addon = xbmcaddon.Addon(id='plugin.audio.mds-fm.ru')
pluginhandle = int(sys.argv[1])
thumb = os.path.join( addon.getAddonInfo('path'), 'icon.png')
xbmcplugin.setContent(int(sys.argv[1]), 'artists')
__settings__ = xbmcaddon.Addon(id='plugin.audio.mds-fm.ru')

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
	try:
		author, title = eval("('"+t.replace(". ","','")+"')")
		title = "[COLOR F050F050]"+t.replace(". ","[/COLOR]  ")
	except:
		print t
		try: 
			t=t.replace("-","— ")
			t=t.replace("«","— «")
			author, title = eval("('"+t.replace("— ","','")+"')")
			title = "[COLOR F050F050]"+t.replace("— ","[/COLOR]  ")
		except: 
			title =t

	#nt= "[COLOR F050F050]"+"[--------------  «Fileek.com»  "+qury+" --------------]"+"[/COLOR]"
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
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				title="Автор"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=author'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
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
				
				title="Сюжетные ходы"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=plot'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				title="Место действия"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=scene'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				title="Время действия"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=time'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				xbmcplugin.endOfDirectory(pluginhandle)


def Title():
	q=inputbox().replace(" ","%20")
	Lt=[]
	for n in range (1,5):
		url='http://mds-fm.ru/search/node/'+q
		if n>0: url=url+"?page="+str(n)
		http=getURL(url)
		ss='<li class="search-result">'
		es='</ol>'
		try:
			c1=mfindal(http, ss, es)[0]
			ss='<a href="'
			es='</a>'
			L=mfindal(c1, ss, es)
		except:
			L=[]
		for i in L:
				url, title = eval(i.replace('<a href="','("').replace('">','", "')+'")')
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(Format(title), iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				if url not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
					Lt.append(url)
				
	xbmcplugin.endOfDirectory(pluginhandle)



def Genres():
		L=[('632', 'Dark Fantasy '),  ('582', 'Science Fantasy'), ('836', '«Дотолкиновское» фэнтези '),  ('745', 'Авантюрно-плутовское'), ('1148', 'Анималистическое '),  ('717', 'Антивоенное'), ('621', 'Антиутопия '),  ('944', 'Античность'), ('1054', 'Боевик '),  ('839', 'Буддизм'), ('730', 'Военное '),  ('631', 'Героическое фэнтези'), ('841', 'Городское фэнтези '),  ('588', 'Гуманитарная (социальная) фантастика'), ('615', 'Детектив '),  ('1408', 'дизельпанк'), ('1169', 'Европейское средневековье '),  ('876', 'Египетская'), ('1144', 'Инков/майя/ацтеков '),  ('592', 'Ирония'), ('825', 'Ислам '),  ('853', 'Исторический роман'), ('649', 'Католичество '),  ('756', 'Киберпанк'), ('1122', 'Классический детектив '),  ('852', 'Классический латино-американский'), ('683', 'Космоопера '),  ('1280', 'Лавкрафтианский хоррор'), ('778', 'Любовный роман '),  ('700', 'Магический реализм'), ('610', 'Мистика '),  ('1395', 'мистический реализм'), ('697', 'Мифология '),  ('1071', 'Мифы Народов Междуречья'), ('694', 'На основе игровой вселенной '),  ('990', 'Народов Африки'), ('666', 'Научная фантастика '),  ('1243', 'Нуар'), ('1063', 'Пародия '),  ('750', 'Планетарная фантастика'), ('1002', 'Полицейский детектив '),  ('647', 'Постапокалиптика'), ('723', 'Постмодернизм '),  ('802', 'Православие'), ('595', 'Приключения '),  ('603', 'Производственная'), ('650', 'Протестантизм '),  ('774', 'Психоделика'), ('596', 'Психологическое '),  ('936', 'Разработанная автором оригинальная мифологическая система'), ('645', 'Реализм '),  ('642', 'Религия'), ('654', 'Роман-катастрофа '),  ('1296', 'Русская/Славянская мифология'), ('875', 'С использованием мифологии '),  ('684', 'С множеством интриг'), ('606', 'Сатира '),  ('639', 'Сказка/Притча'), ('989', 'Скандинавская мифология '),  ('701', 'Современный'), ('605', 'Социальная '),  ('1185', 'Стимпанк/паропанк'), ('692', 'Сюрреализм '),  ('884', 'Таймпанк'), ('935', 'Технофэнтези '),  ('627', 'Утопия'), ('587', 'Фантастика '),  ('764', 'Феминистское'), ('622', 'Философское '),  ('581', 'Фэнтези'), ('677', 'Хоррор/Ужасы '),  ('648', 'Христианство'), ('714', 'Хроноопера '),  ('1205', 'Эпическое фэнтези'), ('817', 'Эротика '),  ('583', 'Юмор'), ('997', 'Язычество ')]
		
		for i in L:
				id, title=i
				url="http://mds-fm.ru/book?g="+id+"#"
				img=thumb
				uri = sys.argv[0] + '?mode=serch'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
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


def Serch(url, title=""):
		print url
		http=getURL(url)
		#ss="<li class = 'playlist'>"
		#es="Setup the player to autoplay"
		#cut1='		|'+mfindal(http, ss, es)[0].replace("'#' data-src=", "")
		#http=http.replace("<li class='playlist'>","<li class = 'playlist'>")
		ss="<li class = 'playlist'"#"<li class = 'playlist'>"
		es='data("object").audioRun'#'</a><hr/></li>'
		L1=mfindal(http, ss, es)
		fl=0
		#if len(L1)==0:
		#	ss="<li class='playlist'>"
		#	es='</a></li></ol>'
		#	L1=mfindal(http, ss, es)
		#	fl=1
			
		for i in L1:
			print i
			ss='http://d.mds-fm.ru'
			es='.mp3'
			L2=mfindal(i, ss, es)
			
			ss="data-title='"
			es="' data-album"
			try:title=mfindal(i, ss, es)[0][len(ss):]
			except: title=" ??? "
			
			ss='</h3><p>'
			es='..</p>'
			try:plot=mfindal(i, ss, es)[0][len(ss):]
			except: plot=""
			
			ss="data-image='"
			es='.jpg'
			try:img=mfindal(i, ss, es)[0][len(ss):]+'.jpg'
			except: img=thumb
			
			if len(L2)>1:
				k=0
				for j in L2:
					k+=1
					url=j+".mp3"
					#img=thumb
					title2=Format(title)+" ч. "+str(k)
					item = xbmcgui.ListItem(title2, iconImage = img, thumbnailImage = img)
					item.setInfo(type="music", infoLabels={"Title": title.replace(".","\n"), "Comment":plot, "album":plot})
					item.setProperty('IsPlayable', 'true')
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
			else:
					url=L2[0]+".mp3"
					#img=thumb
					item = xbmcgui.ListItem(Format(title), iconImage = img, thumbnailImage = img)
					item.setInfo(type="music", infoLabels={"Title": title.replace(".","\n"), "album":plot, "Comment":plot})
					item.setProperty('IsPlayable', 'true')
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
					
		if fl==1 and len(L2)==1: xbmc.Player().play(url)
		else:xbmcplugin.endOfDirectory(pluginhandle)
			
			

params = get_params()
url  =	'http://www.moskva.fm/rss/onair.xml'
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
elif mode == 'serch':	Serch(url, name)
elif mode == 'play':	Play(url)

