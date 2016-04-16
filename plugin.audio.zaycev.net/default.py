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




def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
def rt(x):
	L=[('&quot;','"'), ('&amp;','&'), ('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x

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
				uri = sys.argv[0] + '?mode=title'
				item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="История поиска"
				uri = sys.argv[0] + '?mode=history'
				item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)


				title="Жанры"
				uri = sys.argv[0] + '?mode=genres'
				item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="Новинки"
				uri = sys.argv[0] + '?mode=new'
				item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="Сборники"
				uri = sys.argv[0] + '?mode=sets'
				item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				xbmcplugin.endOfDirectory(pluginhandle)

def History(i=""):
	try:
		HL = eval(__settings__.getSetting("History"))
	except: 
		__settings__.setSetting(id="History", value="[]")
		HL = []
	if i=="":
		return HL
	else:
		n=len(HL)
		if n>30: n=30
		L=[i,]
		for j in range (0,n):
				L.append(HL[j])
		__settings__.setSetting(id="History", value=repr(L))
		return L

def HistoryList():
	L=History()
	for i in L:
				title=i.replace("+"," ")
				uri = sys.argv[0] + '?mode=title'
				uri += '&name='  + urllib.quote_plus(i)
				item = xbmcgui.ListItem(title, iconImage = thumb, thumbnailImage = thumb)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
	xbmcplugin.endOfDirectory(pluginhandle)

def New():
	url='http://zaycev.net/new/more.html?page='
	Songs(url)
	Songs(url,2)
	xbmcplugin.endOfDirectory(pluginhandle)


def Sets():
	url='http://zaycev.net/musicset/more.html?page='
	SetList(url,1)
	SetList(url,2)
	SetList(url,3)
	SetList(url,4)
	SetList(url,5)
	xbmcplugin.endOfDirectory(pluginhandle)


def SetList(url, n=1):
		url=url+str(n)
		http=getURL(url)
		try:
			ss='<div class="musicset-item__pic">'
			es='</p></div></div></li>'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
				ss='pic-link" href="'
				es='"><img height="122"'
				url="http://zaycev.net"+mfindal(i, ss, es)[0][len(ss):]
				
				ss='src="//cdnimg.zaycev.net'
				es='"/></a><a class="musicset-item-pic__shadow'
				img="http://cdnimg.zaycev.net"+mfindal(i, ss, es)[0][len(ss):]

				ss='class="musicset-item__pic-preview" alt="Музыкальная подборка: '
				es='" src="//cdnimg.zaycev.net'
				title=mfindal(i, ss, es)[0][len(ss):]

				uri = sys.argv[0] + '?mode=songs'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

def Title(q=""):
	if q=="": 
		q=inputbox().replace(" ","+")
		History(q)
		
	xbmc.executebuiltin('Container.Update("plugin://plugin.audio.zaycev.net/?mode=find&name='+urllib.quote_plus(q)+'")')

def Find(q):
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
				tmp=mfindal(i, ss, es)[0][len(ss):]
				k=tmp.find('">')
				url2="http://zaycev.net/artist/"+tmp[:k]
				
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
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.zaycev.net/?mode=save&url='+url+'&name='+title2+'")'),\
										('[COLOR F050F050] Исполнитель [/COLOR]', 'Container.Update("plugin://plugin.audio.zaycev.net/?mode=songs_of_artist&url='+url2+'&name='+title2+'")')])
				if url not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
					Lt.append(url)
	xbmcplugin.endOfDirectory(pluginhandle)

def Songs(url, n=1):
		Lt=[]
		if n>0: url=url+str(n)
		http=getURL(url)
		art=FindArt(http).replace("_top917","_square100")
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
				tmp=mfindal(i, ss, es)[0][len(ss):]
				k=tmp.find('">')
				url2="http://zaycev.net/artist/"+tmp[:k]
				
				ss='href="/artist/'
				es='</a></div><div class="musicset-track__track-dash'
				artist=mfindal(i, ss, es)[0]
				artist=rt(artist[artist.find('">')+2:])
				
				ss='target="_blank" >'
				es='</a></div></div><div class="musicset-track__duration'
				title=rt(mfindal(i, ss, es)[0][len(ss):])
				
				title2 = artist+" - "+title
				
				item = xbmcgui.ListItem(title2, iconImage = art, thumbnailImage = art)
				item.setInfo(type="Music", infoLabels={"Title": title, 'artist':artist})
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.zaycev.net/?mode=save&url='+url+'&name='+title2+'")'),\
										('[COLOR F050F050] Исполнитель [/COLOR]', 'Container.Update("plugin://plugin.audio.zaycev.net/?mode=songs_of_artist&url='+url2+'&name='+title2+'")')])
				if url not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
					Lt.append(url)

def FindArt(http):
	try:
		#http=getURL(url)
		ss='http://cdnimg.zaycev.net'
		es='" rel="image_src" id="social-share-image'
		img=ss+mfindal(http, ss, es)[0][len(ss):]
		return img
	except:
		return thumb


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
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.zaycev.net/?mode=save&url='+url+'&name='+title2+'")'),])
				if url not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False)
					Lt.append(url)

def Save(target, name):
	LstDir = __settings__.getSetting("DownloadDirectory")
	if LstDir == "":LstDir = os.path.join( addon.getAddonInfo('path'), "mp3" )
	referer=None
	post=None
	lfimg=os.listdir(ru(LstDir))
	nmi = ru(name)#os.path.basename(target)

	if nmi in lfimg and os.path.getsize(os.path.join(ru(LstDir),nmi))>0:
		return os.path.join( ru(LstDir),nmi)
	else:
		try:
			req = urllib2.Request(url = target, data = post)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(os.path.join( ru(LstDir),nmi+".mp3"), "wb")
			fl.write(resp.read())
		#resp.close()
			fl.close()
			return os.path.join( ru(LstDir),nmi)
		except Exception, e:
			#xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
			return target
			print 'HTTP ERROR ' + str(e)


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
elif mode == 'title':	Title(name)
elif mode == 'genres':	Genres()
elif mode == 'plot':	Plot()
elif mode == 'scene':	Scene()
elif mode == 'time':	Time()
elif mode == 'serch':	Serch(url)
elif mode == 'serchgenres':	SerchGenres(url)
elif mode == 'save':	Save(url, name)
elif mode == 'play':	Play(url)
elif mode == 'new':		New()
elif mode == 'sets':	Sets()
elif mode == 'history':	HistoryList()
elif mode == 'find':
	Find(name)
	if __settings__.getSetting("CL")=="1":
		xbmc.sleep(200)
		xbmc.executebuiltin("Container.SetViewMode(506)")

elif mode == 'songs':
	Songs(url,0)
	xbmcplugin.endOfDirectory(pluginhandle)
	if __settings__.getSetting("CL")=="1":
		xbmc.sleep(200)
		xbmc.executebuiltin("Container.SetViewMode(506)")

elif mode == 'songs_of_artist':
	for i in range(1,10):
		Songs(url+"?page=",i)
	xbmcplugin.endOfDirectory(pluginhandle)
	if __settings__.getSetting("CL")=="1":
		xbmc.sleep(200)
		xbmc.executebuiltin("Container.SetViewMode(506)")
