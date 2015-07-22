#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,sys,os,random
import xbmcplugin,xbmcgui,xbmcaddon
import time

addon = xbmcaddon.Addon(id='plugin.audio.kibergrad.com')
pluginhandle = int(sys.argv[1])
thumb = os.path.join( addon.getAddonInfo('path'), 'icon.png')
xbmcplugin.setContent(int(sys.argv[1]), 'songs')
__settings__ = xbmcaddon.Addon(id='plugin.audio.kibergrad.com')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


GenreList=[
("Jazz", "[COLOR F050F050]Джаз[/COLOR]"),
("Acid-Jazz", "Эйсид-джаз"),
("Contemporary-Jazz", "Современный Джаз"),
("Free-Jazz", "Фри Джаз"),
("Jazz-Metal", "Джаз Метал"),
("Jazz-Pop", "Джаз Поп"),
("Jazz-Rock", "Джаз Рок"),
("Lounge", "Гостиная"),
("Smooth-Jazz", "Smooth Jazz"),
("Swing", "Свинг"),
("Vocal-Jazz", "Вокал Джаз"),
("Metal", "[COLOR F050F050]Метал[/COLOR]"),
("Heavy-Metal", "Хэви-метал"),
("Death-Metal", "Дэт-метал"),
("Thrash-Metal", "Трэш-метал"),
("Nu-Metal", "Нюметал"),
("Doom-Metal", "Дум Метал"),
("Power-Metal", "Паувер Метал"),
("Alternative", "Альтернатива"),
("Black-Metal", "Блэк-метал"),
("Gothic", "Готика"),
("Post-Metal", "Пост Метал"),
("Melodic-Metalcore", "Мелодик Металкор"),
("Industrial", "Промышленные"),
("Melodic-Death", "Мелодик Дет"),
("Folk-Metal", "Фолк Метал"),
("Atmospheric-Black", "Атмосферик Блэк"),
("Avantgarde", "Авангард"),
("Avant-Metal", "Авант Метал"),
("Black-Doom", "Блэк Дум"),
("Blackened-Death", "Блэкенед Дет"),
("Brutal-Death", "Брутал Дэт"),
("Dark-Metal", "Дарк Метал"),
("Deathcore", "Дэткор"),
("Deathgrind", "Дэтграйнд"),
("Death-N-Roll", "Дэт Эн Ролл"),
("Depressive-Black", "Дипрессив Блэк"),
("Drone-Doom", "Дрон Дум"),
("Epic-Metal", "Эпик Метал"),
("Experimental-Metal", "Экспериментал Метал"),
("Funeral-Doom", "Фьюнерал Дум"),
("Groove-Metal", "Грув Метал"),
("Mathcore", "Маткор"),
("Melodic-Black", "Мелодик Блэк"),
("Modern-Metal", "Модерн Метал"),
("NS-Black-Metal", "НС Блэк Метал"),
("NWOBHM", "NWOBHM"),
("Pagan-Metal", "Паган Метал"),
("Post-Black-Metal", "Пост Блэк Метал"),
("Progressive-Death-Metal", "Прогрессив Дэт Метал"),
("Progressive-Metal", "Прогрессив Метал"),
("Raw-Black-Metal", "Рав Блэк Метал"),
("Sludge-Metal", "Сладж-метал"),
("Speed-Metal", "Спид Метал"),
("Stoner-Doom", "Стоунер Дум"),
("Stoner-Metal", "Стоунер Метал"),
("Symphonic-Metal", "Симфонический Метал"),
("TBM", "TBM"),
("Technical-Death", "Техничный Дэт"),
("Technical-Trash", "Техничный Трэш"),
("Thrash-n-Roll", "Thrash'n'Roll"),
("Viking-Metal", "Викинг Метал"),
("Pop", "[COLOR F050F050]Поп-музыка[/COLOR]"),
("Electro", "Электро"),
("Rock-And-Roll", "Рок & ролл"),
("Rock", "Рок"),
("Blues", "Блюз"),
("Rap", "[COLOR F050F050]Рэп[/COLOR]"),
("Chicano-Rap", "Чикано Рэп"),
("Crunk", "Кранк"),
("East-Coast-Rap", "Рэп Восточного Побережья"),
("Gangsta", "Гангста"),
("Hardcore-Rap", "Хардкор Рэп"),
("Pop-Rap", "Поп Рэп"),
("Rapcore", "Рэпкор"),
("Rap-Rock", "Рэп Рок"),
("Southern-Rap", "Южный рэп"),
("Texas-Rap", "Texas Rap"),
("Thug-Rap", "Thug Rap"),
("Underground-Rap", "Underground Rap"),
("West-Coast-Rap", "Рэп Западного побережья"),
("Reggae", "[COLOR F050F050]Регги[/COLOR]"),
("Raggamuffin", "Раггамаффин"),
("Reggaeton", "Реггетон"),
("Rock", "[COLOR F050F050]Рок[/COLOR]"),
("Alternative-Rock", "Альтернативный рок"),
("Indie-Rock", "Инди-рок"),
("Punk-Rock", "Панк-рок"),
("Hard-Rock", "Хард-рок"),
("Post-Rock", "Пост-рок"),
("Folk-Rock", "Фолк-рок"),
("Post-Grunge", "Пост Гранж"),
("Christian-Rock", "Христианский рок"),
("Britpop", "Брит-поп"),
("Progressive-Rock", "Прогрессивный рок"),
("Acid", "Кислота"),
("AOR", "АОР"),
("Art-Rock", "Арт-рок"),
("Avant-Rock", "Авант Рок"),
("Blues-Rock", "Блюз Рок"),
("Dark-Folk", "Дарк Фолк"),
("Experimental", "Экспериментальный"),
("Garage-Rock", "Гаражный рок"),
("Glam-Metal", "Глэм Метал"),
("Gothic-Rock", "Готик-рок"),
("J-Rock", "Джей Рок"),
("Krautrock", "Краут-рок"),
("Neofolk", "Неофолк"),
("New-Wave", "Новая волна"),
("Noise-Rock", "Ноиз рок"),
("Pornogrind", "Порнограйнд"),
("Classic-Rock", "Классический рок"),
("Post-Punk", "Пост-панк"),
("Psychobilly", "Сайкобилли"),
("Shoegaze", "Shoegaze"),
("Ska-Punk", "Ска Панк"),
("Skatepunk", "Скейт Панк"),
("Sleaze-Rock", "Слиз Рок"),
("Soft-Rock", "Софт Рок"),
("Space-Rock", "Спейс-рок"),
("Stoner-Rock", "Стоунер Рок"),
("Symphonic-Rock", "Симфонический рок"),
("Visual-Kei", "Visual Kei"),
("Zeuhl", "Zeuhl"),
("Soundtrack", "[COLOR F050F050]Саундтреки (OST)[/COLOR]"),
("Classical", "[COLOR F050F050]Классическая[/COLOR]"),
("Neoclassical", "Неоклассический"),
("Classical-Crossover", "Классикал Кроссовер"),
("Instrumental", "[COLOR F050F050]Инструментальная музыка[/COLOR]"),
("Acoustic", "Акустические"),
("Electronic", "[COLOR F050F050]Электронная[/COLOR]"),
("Club", "Танцевальная/Клубная"),
("Techno", "Техно"),
("8-bit", "8-бит"),
("Ambient", "Окружающая среда"),
("Breakbeat", "Брейкбит"),
("Chillout", "Chillout"),
("Chillwave", "Чиллвейв"),
("Chiptune", "Чиптюн"),
("Dark-Ambient", "Дарк-эмбиент"),
("Darkwave", "Дарквейв"),
("Digital-Hardcore", "Диджитал Хардкор"),
("Downtempo", "Даунтемпо"),
("Drone-Ambient", "Дрон Амбиент"),
("Dubstep", "Дабстеп"),
("Electro-Freestyle", "Электро Фристайл"),
("Electroclash", "Электроклэш"),
("Electropunk", "Электро Панк"),
("Euro-House", "Евро дом"),
("Futurepop", "Futurepop"),
("Glitch", "Глитч"),
("Goa", "Гоа"),
("Idm", "HD,"),
("Industrial-Rock", "Индастриал Рок"),
("Nu-Rave", "Ню Рэйв"),
("Power-Electronics", "Пауэр Электроникс"),
("Progressive-House", "Прогрессив Хаус"),
("Psytrance", "Psytrance"),
("Speedcore", "Спидкор"),
("Synthpop", "Синтипоп"),
("Tech-House", "Тек-хаус"),
("Tech-Trance", "Тек-транс"),
("Trance-Vocal", "Транс Вокал"),
("Trouse", "Trouse"),
("UK-Funky", "UK Funky"),
("UK-Garage", "UK Garage"),
("Chanson", "[COLOR F050F050]Шансон[/COLOR]"),
("Russkiy-Shanson", "Русский шансон"),
("Club", "[COLOR F050F050]Танцевальная/Клубная[/COLOR]"),
("Punk-Rock", "[COLOR F050F050]Панк-рок[/COLOR]"),
("Emo", "[COLOR F050F050]Эмо[/COLOR]"),
("Emo-Punk", "Эмо Панк"),
("Emo-Rock", "Эмо Рок"),
("Thematic", "[COLOR F050F050]Тематическая музыка[/COLOR]"),
("Hits", "[COLOR F050F050]Хиты[/COLOR]")
]


ArtistList=[
("http://kibergrad.com/578/2517", "25/17"),
("http://kibergrad.com/63/acdc", "AC/DC"),
("http://kibergrad.com/7/beyonce", "Beyonce"),
("http://kibergrad.com/175/eminem", "Eminem"),
("http://kibergrad.com/191/enigma", "Enigma"),
("http://kibergrad.com/48/linkin-park", "Linkin Park"),
("http://kibergrad.com/58/metallica", "Metallica"),
("http://kibergrad.com/6123/mr-credo", "Mr. Credo"),
("http://kibergrad.com/28/rammstein", "Rammstein"),
("http://kibergrad.com/72/scorpions", "Scorpions"),
("http://kibergrad.com/397/skillet", "Skillet"),
("http://kibergrad.com/4768/skrillex", "Skrillex"),
("http://kibergrad.com/1537/ak-47", "АК-47"),
("http://kibergrad.com/1015/aleksandr-marshal", "Александр Маршал"),
("http://kibergrad.com/2138/ariya", "Ария"),
("http://kibergrad.com/13365/arkadiy-kobyakov", "Аркадий Кобяков"),
("http://kibergrad.com/13272/barbariki", "Барбарики"),
("http://kibergrad.com/13/basta", "Баста"),
("http://kibergrad.com/1230/butyrka", "Бутырка "),
("http://kibergrad.com/133/byanka", "Бьянка"),
("http://kibergrad.com/1886/viktor-petlyura", "Виктор Петлюра"),
("http://kibergrad.com/1228/viktor-coy", "Виктор Цой"),
("http://kibergrad.com/13288/gamora", "ГАМОРА"),
("http://kibergrad.com/9/grigoriy-leps", "Григорий Лепс"),
("http://kibergrad.com/2/guf", "Гуф"),
("http://kibergrad.com/3857/ddt", "ДДТ"),
("http://kibergrad.com/3492/denis-maydanov", "Денис Майданов"),
("http://kibergrad.com/147/irina-allegrova", "Ирина Аллегрова"),
("http://kibergrad.com/3981/irina-krug-i-aleksey-bryancev", "Ирина Круг и Алексей Брянцев"),
("http://kibergrad.com/1171/kino", "Кино"),
("http://kibergrad.com/19/kollekciya", "Коллекция"),
("http://kibergrad.com/120/korol-i-shut", "Король и Шут"),
("http://kibergrad.com/1461/leningrad", "Ленинград"),
("http://kibergrad.com/156/linda", "Линда"),
("http://kibergrad.com/125/lyube", "Любэ"),
("http://kibergrad.com/22/maksim", "Максим"),
("http://kibergrad.com/1615/mihail-krug", "Михаил Круг"),
("http://kibergrad.com/27/muzyka-iz-filma", "Музыка из фильма"),
("http://kibergrad.com/1901/nautilus-pompilius", "Наутилус Помпилиус"),
("http://kibergrad.com/1282/nyusha", "Нюша"),
("http://kibergrad.com/3785/piknik", "Пикник"),
("http://kibergrad.com/1273/polina-gagarina", "Полина Гагарина"),
("http://kibergrad.com/45/potap-i-nastya-kamenskih", "Потап и Настя Каменских"),
("http://kibergrad.com/3958/propaganda", "Пропаганда"),
("http://kibergrad.com/56/ruki-vverh", "Руки Вверх"),
("http://kibergrad.com/1625/sektor-gaza", "Сектор Газа "),
("http://kibergrad.com/3978/sergey-nagovicyn", "Сергей Наговицын"),
("http://kibergrad.com/98/stas-mihaylov", "Стас Михайлов"),
("http://kibergrad.com/23/timati", "Тимати"),
("http://kibergrad.com/13308/yarmak", "Ярмак")
]

from tagger import *
def retag(pt, info={}):
	#print "-=-=-= retag -=-=-=-=-"
	import mutagen
	from mutagen.mp3 import MP3
	from mutagen.id3 import ID3
	from mutagen.easyid3 import EasyID3

	try: ID3(pt).delete(delete_v1=True, delete_v2=False)
	except: pass

	mp3_tag = ID3v2(pt)
	#for frame in mp3_tag.frames:
		#print frame.fid
	title_frame = mp3_tag.new_frame('TIT2')
	title_frame.set_text(ru(info["title"].replace("? ","х ")))
	try:
		old_title_frame = [frame for frame in mp3_tag.frames if frame.fid == 'TIT2'][0]
		mp3_tag.frames.remove(old_title_frame)
	except: pass
	mp3_tag.frames.append(title_frame)
	
	a_frame = mp3_tag.new_frame('TPE1')
	a_frame.set_text(ru(info["artist"].replace("? ","х ")))
	try:
		old_a_frame = [frame for frame in mp3_tag.frames if frame.fid == 'TPE1'][0]
		mp3_tag.frames.remove(old_a_frame)
	except: pass
	mp3_tag.frames.append(a_frame)

	al_frame = mp3_tag.new_frame('TALB')
	al_frame.set_text(ru(info["album"].replace("? ","х ")))
	try:
		old_al_frame = [frame for frame in mp3_tag.frames if frame.fid == 'TALB'][0]
		mp3_tag.frames.remove(old_al_frame)
	except: pass
	mp3_tag.frames.append(al_frame)

	mp3_tag.commit()

	#audio = EasyID3(pt, ID3=EasyID3)
	#audio["title"]      = ru(info["title"].replace("? ","х "))
	#audio["artist"]     = ru(info["artist"].replace("? ","х "))
	#audio["performer"]  = info["artist"].replace("? ","х ")
	#audio["album"]      = ru(info["album"].replace("? ","х "))
	#audio["date"]       = "1980"
	#audio["tracknumber"]= "1/10"
	#print audio.pprint()
	#audio.save()

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
				title="[B][ Поиск ][/B]"
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

				title="Исполнители"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=artist'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				xbmcplugin.endOfDirectory(pluginhandle)


def SerchTitle():
		q=inputbox().replace(" ","+")
		Lt=[]
		url='http://kibergrad.com/search?q='+q
		http=getURL(url)
		try:
			ss='<li class="view clearit">'
			es='<a class="icon icon-list-download download-btn'
			L=mfindal(http, ss, es)
		except:
			L=[]
		Lt=[]
		for n in range (1,10):
					if n>1: url2=url+"?page="+str(n)
					else: url2=url
					Lt=Serch(url2, Lt)
		xbmcplugin.endOfDirectory(pluginhandle)


def SrcArtist():
		q=inputbox().replace(" ","+")
		Lt=[]
		url='http://kibergrad.com/search?q='+q+"&p=artists"
		http=getURL(url)
		try:
			ss='<h3>'
			es='</h3>'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
			n=eval(i.replace("<a href=","(").replace("</a>",'")').replace('">','", "').replace('<h3>','').replace(chr(10), "").strip())
			Lt.append(n)
		Artist(Lt)


def Genres():
		for i in GenreList:
			#for n in range (1,10):
				id, title=i
				url="http://kibergrad.com/tag/"+id
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
				Lt=[]
				for n in range (1,20):
					if n>1: url2=url+"?page="+str(n)
					else: url2=url
					Lt=Album(url2, Lt)
				xbmcplugin.endOfDirectory(pluginhandle)


def Artist(L=[]):
		if L==[]:
				title="[COLOR F06060F0][B][ Поиск ][/B][/COLOR]"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=srcartist'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

		if L==[]:AL=ArtistList
		else: AL=L
			
		for i in AL:
				url, title=i
				img=thumb
				uri = sys.argv[0] + '?mode=serchartists'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
		xbmcplugin.endOfDirectory(pluginhandle)

def SerchArtists(url):
				title="[COLOR F06060F0][B][ Альбомы ] [/B][/COLOR]"
				img=thumb
				uri = sys.argv[0] + '?mode=serchalbums'
				uri += '&url='  + urllib.quote_plus(url+'?p=albums')
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				Lt=[]
				for n in range (1,20):
					if n>1: url2=url+"?page="+str(n)
					else: url2=url
					Lt=Serch(url2, Lt)
				xbmcplugin.endOfDirectory(pluginhandle)

def SerchAlbums(url):
				Lt=[]
				for n in range (1,5):
					if n>1: url2=url+"&FAlbum_page="+str(n)
					else: url2=url
					Lt=Album(url2, Lt)
				xbmcplugin.endOfDirectory(pluginhandle)

def SerchTracs(url):
				Lt=Serch(url)
				xbmcplugin.endOfDirectory(pluginhandle)


def Serch(url, Lt=[]):
		http=getURL(url)
		try:
			ss='<li class="view clearit">'
			es='<a class="icon icon-list-download download-btn'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
				k=i.find("data-play-src=")
				i=i[k:]
				i=i.replace('  ','')
				i=i.replace(chr(10),'').replace(chr(13),'')
				i=i.replace('" data-','", "')
				i=i.replace('="','": "')
				i=i.replace('></a>','')
				i=i.replace('-name','')
				#i=i.replace('album-name','album')
				#i=i.replace('artist-name','artist')
				i=i.replace('name','title')
				i=i.replace('data-play-src','url')
				i=i.replace('download-src','dlurl')
				i='{"'+i+"}"
				dict=eval(i)
				#print i
				
				album	=dict["album"].replace("? ","х ")
				artist	=dict["artist"].replace("? ","х ")
				title	=dict["title"].replace("? ","х ")
				img		=dict["cover"]
				url		=dict["url"]
				
				trk='[COLOR F050F050][T] [/COLOR]'
				title2 = artist+" - [B]"+title+"[/B]"
				item = xbmcgui.ListItem(trk+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist, "album":album})
				
				uri = sys.argv[0] + '?mode=save'
				uri += '&info='  + urllib.quote_plus(i)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.kibergrad.com/'+uri+'")'),])
				
				if title2 not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, url, item, False,500)
					Lt.append(title2)
		return Lt

def Album(url, Lt=[]):
		http=getURL(url)
		try:
			ss='<div class="album-item clearfix">'
			es='<div class="clear"></div>'
			L=mfindal(http, ss, es)
		except:
			L=[]
		#print L
		for i in L:
			if len(i)>10:
				ss='<div class="album-cover">'
				es='<div class="album-info">'
				it=mfindal(i, ss, es)[0][len(ss):]
				it=it.replace('><img src=',', "cover": ')
				it=it.replace('alt=',', "alt": ')
				it=it.replace('title=',', "title": ')
				it=it.replace('<a href=','{"url": ')
				it=it.replace('/></a>    </div>','}')
				it=it.strip()
				#print it
				dict=eval(it)
				
				
				ss='<h3>'
				es='</h3>'
				it=mfindal(i, ss, es)[0][len(ss):]
				ss='">'
				es='</a>'
				
				artist=mfindal(it, ss, es)[0][len(ss):].replace("? ","х ")
				dict["artist"] = artist
				title2	=dict["title"].replace("? ","х ")
				img		=dict["cover"]
				url		=dict["url"]
				title=title2.replace(" - ", '').replace(artist, '').replace("? ","х ")
				title2=title2.replace(" - ", ' - [B]')+"[/B]"
				album	=title
				alb='[COLOR F07070F0][А] [/COLOR]'
				item = xbmcgui.ListItem(alb+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist, "album":album})
				
				uri = sys.argv[0] + '?mode=save_all'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)
				item.addContextMenuItems([('[COLOR F050F050] Сохранить альбом [/COLOR]', 'Container.Update("plugin://plugin.audio.kibergrad.com/'+uri+'")'),])
				
				uri = sys.argv[0] + '?mode=serchtracs'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)

				if title2 not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True,50)
					Lt.append(title2)
		return Lt


def SaveAll(url):
		http=getURL(url)
		try:
			ss='<li class="view clearit">'
			es='<a class="icon icon-list-download download-btn'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
				k=i.find("data-play-src=")
				i=i[k:]
				i=i.replace('  ','')
				i=i.replace(chr(10),'').replace(chr(13),'')
				i=i.replace('" data-','", "')
				i=i.replace('="','": "')
				i=i.replace('></a>','')
				i=i.replace('-name','')
				#i=i.replace('album-name','album')
				#i=i.replace('artist-name','artist')
				i=i.replace('name','title')
				i=i.replace('data-play-src','url')
				i=i.replace('download-src','dlurl')
				i='{"'+i+"}"
				dict=eval(i)
				#print i
				
				album	=dict["album"].replace("? ","х ")
				artist	=dict["artist"].replace("? ","х ")
				title	=dict["title"].replace("? ","х ")
				img		=dict["cover"]
				url		=dict["url"]
				
				trk='[COLOR F050F050][T] [/COLOR]'
				title2 = artist+" - [B]"+title+"[/B]"
				item = xbmcgui.ListItem(trk+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist, "album":album})
				
				Save(dict, title2, update=0)
				xbmcplugin.addDirectoryItem(pluginhandle, url, item, False,len(L))
		xbmc.executebuiltin('UpdateLibrary("music")')
		xbmcplugin.endOfDirectory(pluginhandle)



def Save2(dict, name):
	target=dict["dlurl"]
	LstDir = __settings__.getSetting("DownloadDirectory")
	if LstDir == "":LstDir = os.path.join( addon.getAddonInfo('path'), "mp3" )
	referer=None
	post=None
	lfimg=os.listdir(ru(LstDir))
	nmi = ru(name)#os.path.basename(target)

	if nmi in lfimg and os.path.getsize(os.path.join(ru(LstDir),nmi))>0:
		return os.path.join(ru(LstDir),nmi)
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

def Save(dict, name, update=1):
	target	=dict["dlurl"]
	artist	=dict["artist"].replace("? ","х ")
	title	=dict["title"].replace("? ","х ")
	img		=dict["cover"]
	album	=dict["album"].replace("? ","х ")

	Dldir = __settings__.getSetting("DownloadDirectory")
	if Dldir == "":Dldir = os.path.join( addon.getAddonInfo('path'), "mp3" )
	
	fp = os.path.join(ru(Dldir), ru(artist))
	fp = os.path.join(fp, ru(album))
	if os.path.exists(fp)== False: os.makedirs(fp)
	cp=os.path.join(fp, "cover.jpg")
	fp = os.path.join(fp, ru(title+".mp3"))
	
	try:
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			if os.path.exists(cp)== False:
				req = urllib2.Request(url = img, data = None)
				req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
				resp = urllib2.urlopen(req)
				fl = open(cp, "wb")
				fl.write(resp.read())
				fl.close()
			
			retag(fp, dict)
			#print "Update"
			if update==1: xbmc.executebuiltin('UpdateLibrary("music")')
			
			return os.path.join( ru(LstDir),nmi)
	except Exception, e:
			#xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
			return target
			print 'HTTP ERROR ' + str(e)

params = get_params()
url  =	'http://kibergrad.com'
mode =	None
name =	''
img =	' '
info =	{}

try: url = urllib.unquote_plus(params["url"])
except: pass
try: mode = urllib.unquote_plus(params["mode"])
except: pass
try: name = urllib.unquote_plus(params["name"])
except: pass
try: img = urllib.unquote_plus(params["img"])
except: pass
try: info = eval(urllib.unquote_plus(params["info"]))
except: pass



if   mode == None:		Root()
elif mode == 'title':	SerchTitle()
elif mode == 'genres':	Genres()
elif mode == 'artist':	Artist()
elif mode == 'scene':	Scene()
elif mode == 'time':	Time()
elif mode == 'serch':	Serch(url)
elif mode == 'serchgenres':		SerchGenres(url)
elif mode == 'serchartists':	SerchArtists(url)
elif mode == 'serchalbums':	SerchAlbums(url)
elif mode == 'serchtracs':	SerchTracs(url)
elif mode == 'save':	Save(info, name)
elif mode == 'save_all':	SaveAll(url)
elif mode == 'srcartist':	SrcArtist()

