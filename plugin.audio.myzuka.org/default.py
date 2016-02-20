#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,re,sys,os,random
import xbmcplugin,xbmcgui,xbmcaddon
import time

addon = xbmcaddon.Addon(id='plugin.audio.myzuka.org')
pluginhandle = int(sys.argv[1])
thumb = os.path.join( addon.getAddonInfo('path'), 'icon.png')
xbmcplugin.setContent(int(sys.argv[1]), 'songs')
__settings__ = xbmcaddon.Addon(id='plugin.audio.myzuka.org')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


GenreList=[
("/Genre/11/Pop","Pop"),
("/Genre/25/Disco","Disco"),
("/Genre/28/Hard-Rock","Hard Rock"),
("/Genre/234/Eurodance","Eurodance"),
("/Genre/1/Rock","Rock"),
("/Genre/30/Heavy-Metal","Heavy Metal"),
("/Genre/158/Blues-Rock","Blues Rock"),
("/Genre/8/Rap","Rap"),
("/Genre/12/Trance","Trance"),
("/Genre/229/Ost","OST"),
("/Genre/21/Synthpop","Synthpop"),
("/Genre/67/Thrash-Metal","Thrash Metal")
]

ArtistList=[
("/Artist/96002/Imany","Imany"),
("/Artist/124788/Lana-Del-Rey","Lana Del Rey"),
("/Artist/5/Linkin-Park","Linkin Park"),
("/Artist/11659/Calvin-Harris","Calvin Harris"),
("/Artist/76588/%D0%9A%D0%BE%D1%80%D0%BE%D0%BB%D1%8C-%D0%98-%D0%A8%D1%83%D1%82","Король и Шут"),
("/Artist/30/Eminem","Eminem"),
("/Artist/937/Rammstein","Rammstein"),
("/Artist/29/Shakira","Shakira"),
("/Artist/278404/Robin-Schulz","Robin Schulz"),
("/Artist/1268/Pharrell-Williams","Pharrell Williams"),
("/Artist/923/Metallica","Metallica"),
("/Artist/271/Hans-Zimmer","Hans Zimmer"),
("/Artist/85569/%D0%9D%D1%8E%D1%88%D0%B0","Нюша"),
("/Artist/228/Rihanna","Rihanna"),
("/Artist/179673/Lilly-Wood-And-The-Prick","Lilly Wood &amp; The Prick"),
("/Artist/272494/Faul","Faul"),
("/Artist/235/Pink-Floyd","Pink Floyd"),
("/Artist/134/Scorpions","Scorpions"),
("/Artist/35084/Ellie-Goulding","Ellie Goulding"),
("/Artist/3827/Enrique-Iglesias","Enrique Iglesias"),
("/Artist/27233/The-Prodigy","The Prodigy"),
("/Artist/8380/Pnau","PNAU"),
("/Artist/82883/%D0%9A%D1%80%D0%B0%D1%81%D0%BD%D0%B0%D1%8F-%D0%9F%D0%BB%D0%B5%D1%81%D0%B5%D0%BD%D1%8C","Красная Плесень"),
("/Artist/272495/Wad-Ad","Wad Ad"),
("/Artist/20851/Ac-Dc","AC/DC"),
("/Artist/71003/%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4","Ленинград"),
("/Artist/1867/Michael-Jackson","Michael Jackson"),
("/Artist/84647/%D0%95%D0%BB%D0%BA%D0%B0","Ёлка"),
("/Artist/326640/The-Avener","The Avener"),
("/Artist/25537/%D0%9A%D0%B8%D0%BD%D0%BE","Кино"),
("/Artist/246/Within-Temptation","Within Temptation"),
("/Artist/31142/Serebro","Serebro"),
("/Artist/26/The-Beatles","The Beatles"),
("/Artist/15369/Sia","Sia"),
("/Artist/86143/%D0%92%D0%B8%D0%BD%D1%82%D0%B0%D0%B6","Винтаж"),
("/Artist/282015/Kadebostany","Kadebostany"),
("/Artist/1190/Deep-Purple","Deep Purple"),
("/Artist/60659/%D0%91%D0%B0%D1%81%D1%82%D0%B0","Баста"),
("/Artist/40/Daft-Punk","Daft Punk"),
("/Artist/287375/Dj-Snake","Dj Snake"),
("/Artist/161/Queen","Queen"),
("/Artist/139152/Imagine-Dragons","Imagine Dragons"),
("/Artist/71089/%D0%9B%D1%8F%D0%BF%D0%B8%D1%81-%D0%A2%D1%80%D1%83%D0%B1%D0%B5%D1%86%D0%BA%D0%BE%D0%B8","Ляпис Трубецкой"),
("/Artist/70285/%D0%90%D1%80%D0%B8%D1%8F","Ария"),
("/Artist/133/Coldplay","Coldplay"),
("/Artist/308532/Kiesza","Kiesza"),
("/Artist/1002/Armin-Van-Buuren","Armin van Buuren"),
("/Artist/175/Marilyn-Manson","Marilyn Manson"),
("/Artist/1447/Pitbull","Pitbull"),
("/Artist/68/Beyonce","Beyonce"),
("/Artist/70669/%D0%A1%D0%B5%D0%BA%D1%82%D0%BE%D1%80-%D0%93%D0%B0%D0%B7%D0%B0","Сектор Газа"),
("/Artist/247/Modern-Talking","Modern Talking"),
("/Artist/67529/%D0%9E%D0%BA%D0%B5%D0%B0%D0%BD-%D0%95%D0%BB%D1%8C%D0%B7%D0%B8","Океан Ельзи"),
("/Artist/17227/Wiz-Khalifa","Wiz Khalifa"),
("/Artist/4/Limp-Bizkit","Limp Bizkit"),
("/Artist/314289/Sam-Martin","Sam Martin"),
("/Artist/920/Maroon-5","Maroon 5"),
("/Artist/43/2Pac","2Pac"),
("/Artist/31620/Major-Lazer","Major Lazer"),
("/Artist/15/Madonna","Madonna"),
("/Artist/127799/%D0%90%D0%BD%D0%B8-%D0%9B%D0%BE%D1%80%D0%B0%D0%BA","Ани Лорак"),
("/Artist/90531/%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80-%D0%92%D1%8B%D1%81%D0%BE%D1%86%D0%BA%D0%B8%D0%B8","Владимир Высоцкий"),
("/Artist/76577/%D0%90%D0%BB%D0%B8%D1%81%D0%B0","Алиса"),
("/Artist/121/Enigma","Enigma"),
("/Artist/41792/Mr-Probz","Mr. Probz"),
("/Artist/76573/%D0%91%D0%B8-2","БИ-2"),
("/Artist/201572/Sam-Smith","Sam Smith"),
("/Artist/414/30-Seconds-To-Mars","30 Seconds To Mars"),
("/Artist/89199/%D0%9D%D0%B0%D1%82%D0%B0%D0%BB%D0%B8","Натали"),
("/Artist/282572/Mo","M&#216;"),
("/Artist/323098/Nico-And-Vinz","Nico &amp; Vinz"),
("/Artist/48742/Avicii","Avicii"),
("/Artist/10/Nickelback","Nickelback"),
("/Artist/42/Nightwish","Nightwish"),
("/Artist/237/Led-Zeppelin","Led Zeppelin"),
("/Artist/3758/Nazareth","Nazareth"),
("/Artist/2172/Dr-Alban","Dr. Alban"),
("/Artist/89213/%D0%92%D0%B8%D0%B0-%D0%93%D1%80%D0%B0","ВИА Гра"),
("/Artist/220774/Martin-Garrix","Martin Garrix"),
("/Artist/142/Muse","Muse"),
("/Artist/19/Three-Days-Grace","Three Days Grace"),
("/Artist/26919/Hurts","Hurts"),
("/Artist/12646/Katy-Perry","Katy Perry"),
("/Artist/37/Snoop-Dogg","Snoop Dogg"),
("/Artist/70474/%D0%A1%D0%BF%D0%BB%D0%B8%D0%BD","Сплин"),
("/Artist/1138/Accept","Accept"),
("/Artist/1589/Skillet","Skillet"),
("/Artist/82786/%D0%A0%D1%83%D0%BA%D0%B8-%D0%92%D0%B2%D0%B5%D1%80%D1%85","Руки Вверх!"),
("/Artist/171/Nirvana","Nirvana"),
("/Artist/2312/Bad-Boys-Blue","Bad Boys Blue"),
("/Artist/1294/Black-Sabbath","Black Sabbath"),
("/Artist/126/Slipknot","Slipknot"),
("/Artist/7/Scooter","Scooter"),
("/Artist/316248/%D0%95%D0%B3%D0%BE%D1%80-%D0%9A%D1%80%D0%B8%D0%B4","Егор Крид"),
("/Artist/186530/Iowa","Iowa"),
("/Artist/14950/Lady-Gaga","Lady GaGa"),
("/Artist/59649/Skrillex","Skrillex"),
("/Artist/18958/Jason-Derulo","Jason Derulo"),
("/Artist/171114/The-Rolling-Stones","The Rolling Stones"),
("/Artist/21/50-Cent","50 Cent"),
("/Artist/292011/%D0%91%D1%83%D1%80%D0%B8%D1%82%D0%BE","Бурито"),
("/Artist/5553/Onerepublic","OneRepublic"),
("/Artist/693/Brian-Tyler","Brian Tyler"),
("/Artist/386/Britney-Spears","Britney Spears"),
("/Artist/339/Fall-Out-Boy","Fall Out Boy"),
("/Artist/86684/%D0%93%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%D1%81%D0%BA%D0%B0%D1%8F-%D0%9E%D0%B1%D0%BE%D1%80%D0%BE%D0%BD%D0%B0","Гражданская Оборона"),
("/Artist/76601/%D0%90%D0%B3%D0%B0%D1%82%D0%B0-%D0%9A%D1%80%D0%B8%D1%81%D1%82%D0%B8","Агата Кристи"),
("/Artist/70894/%D0%AE%D0%BB%D0%B8%D1%8F-%D0%A1%D0%B0%D0%B2%D0%B8%D1%87%D0%B5%D0%B2%D0%B0","Юлия Савичева"),
("/Artist/366/Iron-Maiden","Iron Maiden"),
("/Artist/10513/Flo-Rida","Flo Rida"),
("/Artist/76605/%D0%9F%D0%B8%D0%BA%D0%BD%D0%B8%D0%BA","Пикник"),
("/Artist/1916/Judas-Priest","Judas Priest"),
("/Artist/311914/Zhu","ZHU"),
("/Artist/10934/Hollywood-Undead","Hollywood Undead"),
("/Artist/46875/Two-Steps-From-Hell","Two Steps from Hell"),
("/Artist/194/Moby","Moby"),
("/Artist/197/Arash","Arash"),
("/Artist/2566/Sandra","Sandra"),
("/Artist/98053/%D0%94%D0%B4%D1%82","ДДТ"),
("/Artist/1116/Lil-Jon","Lil Jon"),
("/Artist/285354/Indila","Indila"),
("/Artist/23/System-Of-A-Down","System Of A Down"),
("/Artist/36/Korn","Korn"),
("/Artist/68148/%D0%92%D0%B5%D1%80%D0%B0-%D0%91%D1%80%D0%B5%D0%B6%D0%BD%D0%B5%D0%B2%D0%B0","Вера Брежнева"),
("/Artist/68349/%D0%A2%D0%B8%D0%BC%D0%B0%D1%82%D0%B8","Тимати"),
("/Artist/51/Disturbed","Disturbed"),
("/Artist/87472/%D0%94%D0%B8%D0%BC%D0%B0-%D0%91%D0%B8%D0%BB%D0%B0%D0%BD","Дима Билан"),
("/Artist/80104/%D0%A1%D1%82%D0%B0%D1%81-%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB%D0%BE%D0%B2","Стас Михайлов"),
("/Artist/6760/Uriah-Heep","Uriah Heep"),
("/Artist/480/Paul-Mccartney","Paul McCartney"),
("/Artist/57521/Nautilus-Pompilius","Nautilus Pompilius"),
("/Artist/156/Atb","ATB"),
("/Artist/311913/Steve-James","Steve James"),
("/Artist/926/Mylene-Farmer","Mylene Farmer"),
("/Artist/141605/Zedd","Zedd"),
("/Artist/7790/Taylor-Swift","Taylor Swift"),
("/Artist/121788/One-Direction","One Direction"),
("/Artist/8/Ozzy-Osbourne","Ozzy Osbourne"),
("/Artist/170092/Dvbbs","DVBBS"),
("/Artist/192/Placebo","Placebo"),
("/Artist/408/Jay-Z","Jay-Z"),
("/Artist/17694/Selena-Gomez","Selena Gomez"),
("/Artist/155/Red-Hot-Chili-Peppers","Red Hot Chili Peppers"),
("/Artist/178854/%D0%94%D0%B6%D0%B8%D0%B3%D0%B0%D0%BD","Джиган"),
("/Artist/205/Papa-Roach","Papa Roach"),
("/Artist/158889/5Sta-Family","5sta Family"),
("/Artist/2/The-Offspring","The Offspring"),
("/Artist/39954/Stromae","Stromae"),
("/Artist/392/Fergie","Fergie"),
("/Artist/1467/U-D-O","U.D.O."),
("/Artist/1039/Electric-Light-Orchestra","Electric Light Orchestra"),
("/Artist/976/Kiss","Kiss"),
("/Artist/365109/Charlie-Puth","Charlie Puth"),
("/Artist/31/Bon-Jovi","Bon Jovi"),
("/Artist/111230/Mc-Zali","Mc Zali"),
("/Artist/25837/Swanky-Tunes","Swanky Tunes"),
("/Artist/172058/%D0%9C%D0%B0%D0%BA%D1%81-%D0%9A%D0%BE%D1%80%D0%B6","Макс Корж"),
("/Artist/89152/%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80-%D0%9A%D1%83%D0%B7%D1%8C%D0%BC%D0%B8%D0%BD","Владимир Кузьмин"),
("/Artist/76580/%D0%97%D0%B5%D0%BC%D1%84%D0%B8%D1%80%D0%B0","Земфира"),
("/Artist/1008/C-C-Catch","C.C. Catch"),
("/Artist/12159/Ramin-Djawadi","Ramin Djawadi"),
("/Artist/95246/Dj-Half","DJ Half"),
("/Artist/196785/%D0%9A%D0%B0%D1%81%D0%BF%D0%B8%D0%B8%D1%81%D0%BA%D0%B8%D0%B8-%D0%93%D1%80%D1%83%D0%B7","Каспийский Груз"),
("/Artist/342996/Feder","Feder"),
("/Artist/2156/Ennio-Morricone","Ennio Morricone"),
("/Artist/94826/%D0%AE%D0%BB%D0%B8%D0%B0%D0%BD%D0%BD%D0%B0-%D0%9A%D0%B0%D1%80%D0%B0%D1%83%D0%BB%D0%BE%D0%B2%D0%B0","Юлианна Караулова"),
("/Artist/310466/Raign","Raign"),
("/Artist/2223/Rainbow","Rainbow"),
("/Artist/197168/Leonora","Leonora"),
("/Artist/348508/Mband","MBAND"),
("/Artist/376331/Burito","Burito"),
("/Artist/13402/The-Script","The Script"),
("/Artist/238/Tokio-Hotel","Tokio Hotel"),
("/Artist/18129/Noize-Mc","Noize MC"),
("/Artist/357/Justin-Timberlake","Justin Timberlake"),
("/Artist/84698/%D0%91%D1%83%D1%82%D1%8B%D1%80%D0%BA%D0%B0","Бутырка"),
("/Artist/154/Smokie","Smokie"),
("/Artist/8020/Adele","Adele"),
("/Artist/345/Ludacris","Ludacris"),
("/Artist/478/Chris-Rea","Chris Rea"),
("/Artist/244/Boney-M","Boney M."),
("/Artist/83462/%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB-%D0%9A%D1%80%D1%83%D0%B3","Михаил Круг"),
("/Artist/193/T-I","T.I."),
("/Artist/123/Adriano-Celentano","Adriano Celentano"),
("/Artist/82773/Helena","Helena"),
("/Artist/23297/Inna","Inna"),
("/Artist/14/Green-Day","Green Day"),
("/Artist/2344/Bring-Me-The-Horizon","Bring Me The Horizon"),
("/Artist/1076/Helloween","Helloween"),
("/Artist/170/Roxette","Roxette"),
("/Artist/76596/%D0%9C%D1%83%D0%BC%D0%B8%D0%B8-%D0%A2%D1%80%D0%BE%D0%BB%D0%BB%D1%8C","Мумий Тролль"),
("/Artist/3294/Miley-Cyrus","Miley Cyrus"),
("/Artist/2520/Pet-Shop-Boys","Pet Shop Boys"),
("/Artist/1112/Dj-Bobo","DJ Bobo"),
("/Artist/261560/Borgeous","Borgeous"),
("/Artist/92445/%D0%91%D1%8C%D1%8F%D0%BD%D0%BA%D0%B0","Бьянка"),
("/Artist/367/Evanescence","Evanescence")
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



def getURL(url,Referer = 'https://myzuka.org/'):
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

def rt(x):
	L=[('&#39;','’'), ('&#145;','‘'), ('&#146;','’'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x


def Format(t):
	title =t
	return title

def Root():
				title="[COLOR F0E0E067][B][ Поиск ][/B][/COLOR]"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=title'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="[COLOR F0E0E067][B][ Жанры ][/B][/COLOR]"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=genres'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="[COLOR F0E0E067][B][ Исполнители ][/B][/COLOR]"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=artist'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				Serch_in_album("https://myzuka.org/Hits/Top100Monthly")
				
				xbmcplugin.endOfDirectory(pluginhandle)


def SerchTitle():
		q=inputbox().replace(" ","%20")
		url='https://myzuka.org/Search?searchText='+q
		Serch(url, Lt=[])
		xbmcplugin.endOfDirectory(pluginhandle)


def SrcArtist(q=""):
		if q=="": q=inputbox()
		Lt=[]
		url='http://kibergrad.com/search?q='+q.replace(" ","+")+"&p=artists"
		
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
				url="https://myzuka.org"+id
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
				for n in range (1,10):
					if n>1: url2=url+"/Page"+str(n)
					else: url2=url
					Album2(url2)
				xbmcplugin.endOfDirectory(pluginhandle)

def Album2(url):
		http=getURL(url)
		try:
			ss='ght="30">'
			es='<td hei'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
			try:
				i=i.replace('  ','')
				i=i.replace(chr(10),'').replace(chr(13),'')
				i=i.replace('ght="30"><a href="','https://myzuka.org')
				i=i.replace('</a></td><td><a href="','","https://myzuka.org')
				i=i.replace('</a></td><td>','","')
				i=i.replace('</td></tr><tr>','"')
				i=i.replace('">','","')
				i=i.replace('&amp;','&')
				i=i.replace(' class="img-rounded","",',',')
				i=i.replace('</td><td>','","')
				i=i.replace('</td><td><b>','","')
				i=i.replace('<img alt="','')
				i=i.replace('" src="','","')
				i=rt(i)
				i='["'+i+"]"
				#print i
				ie=eval(i)
				
				
				img		=ie[2]
				album	=ie[1]
				artist	=ie[4]
				title	=ie[1]
				url		=ie[0]
				urlart	=ie[3]
				title2 = artist+" - [B]"+title+"[/B]"
				
				uri = sys.argv[0] + '?mode=serchtracs'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)

				alb='[COLOR F07070F0][А] [/COLOR]'
				trk='[COLOR F050F050][T] [/COLOR]'
				item = xbmcgui.ListItem(alb+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist, "album":album})#222
				xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True,500)
				
			except:pass



def Artist(L=[]):
		if L==[]:
				title="[COLOR F0E0E067][B][ Поиск ][/B][/COLOR]"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=srcartist'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

		if L==[]:AL=ArtistList
		else: AL=L
			
		for i in AL:
				url, title=i
				url='https://myzuka.org'+url
				img=thumb
				#uri = sys.argv[0] + '?mode=serchartists'
				uri = sys.argv[0] + '?mode=serchalbums'
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
				uri += '&url='  + urllib.quote_plus(url)#+'?p=albums')
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				Lt=[]
				for n in range (1,20):
					if n>1: url2=url+"?page="+str(n)
					else: url2=url
					Lt=Serch(url2, Lt)
				xbmcplugin.endOfDirectory(pluginhandle)

def SerchAlbums(url):
				title="[COLOR F050F050][B][ Tреки ] [/B][/COLOR]"
				img=thumb
				uri = sys.argv[0] + '?mode=serchartists'
				uri += '&url='  + urllib.quote_plus(url)#+'?p=albums')
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)
				
				Lt=[]
				url2=url+'/Albums'
				Lt=Album(url2, Lt)
				xbmcplugin.endOfDirectory(pluginhandle)

def SerchTracs(url):
				if url.find("ttps://myzuka")<0: url='https://myzuka.org'+url
				#print url
				Lt=Serch_in_album(url)
				xbmcplugin.endOfDirectory(pluginhandle)

def Serch_in_album(url, Lt=[], S=0):
	if url.find("ttps://myzuka")<0: url='https://myzuka.org'+url
	#print url
	http=getURL(url)
	try:
		ss='itemprop="image" src="'
		es='<div class="share-block">'
		es='&amp;il=False&amp;msl=0"/'
		img=mfindal(http, ss, es)[0][len(ss):].replace(chr(10),'').replace(chr(13),'').replace('"/>        </div>','').replace('amp;','')+"&il=False&msl=0"
		#print img
	except:img=""
	try:
		ss='<h1>'
		es='</h1>'
		album2=mfindal(http, ss, es)[0][len(ss):-6].replace('amp;','')
		album2=rt(album2)
	except:album2=""
	try:
		ss='<h1>'
		es='</h1>'
		year=mfindal(http, ss, es)[0][-5:-1]
	except:year=""

	try:
		ss='data-url="/Song/Play/'
		es='><!---->'
		es='title="Слушать '
		L=mfindal(http, ss, es)
	except:
		L=[]
	tnb=0
	for i in L:
		try:
			if len (i)>10:
				i=i.replace('data-url=','{"url":')
				i=i.replace('data-position =',',"position":')
				i=i.replace('data-url=','{"url":')
				i=i.replace('amp;','')
				i=rt(i)
				i=i.replace('data-title=',',"artist":')
				#i=i.replace('title="Слушать ',',"artist2":')
				i=i.replace(' - ','", "title":"')
				i=i.replace('&#39;',"'")
				i=i+'}'
				#print i
				dict=eval(i)
			
				purl=dict["url"].replace("/Song/Play/","https://myzuka.org/Song/Download/")
				title=dict["title"]
				artist=dict["artist"]
				album=album2.replace(artist+' - ','')
				#img=""
				title2=artist+" - "+title
				#print title
				tnb+=1
				trk='[COLOR F050F050][T] [/COLOR]'
				item = xbmcgui.ListItem(trk+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist, "album":album, "year":year, "tracknumber":tnb})
				
				dict["dlurl"]=purl
				dict["album"]=album
				dict["year"]=year
				dict["cover"]=img
				info=repr(dict)
				
				uri = sys.argv[0] + '?mode=save'
				uri += '&info='  + urllib.quote_plus(info)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)
				
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.myzuka.org/'+uri+'")'),])
				if S>0: Save(dict, title,update=0)
				xbmcplugin.addDirectoryItem(pluginhandle, purl, item, False, len(L))
		except:pass
	if S>0:xbmc.executebuiltin('UpdateLibrary("music")')

def Serch(url, Lt=[]):
		http=getURL(url)
		n=http.find("<h1>Поиск по композициям</h1>")
		http=http[n:]
		try:
			ss='ght="30">'
			es='<td hei'
			L=mfindal(http, ss, es)
		except:
			L=[]
		for i in L:
			try:
				i=i.replace('  ','')
				i=i.replace(chr(10),'').replace(chr(13),'')
				i=i.replace('ght="30"><a href="','https://myzuka.org')
				i=i.replace('</a></td><td><a href="','","https://myzuka.org')
				i=i.replace('</a></td><td>','","')
				i=i.replace('</td></tr><tr>','"')
				i=i.replace('">','","')
				i=rt(i)
				i='["'+i+"]"
				#print i
				ie=eval(i)
				
				img=""
				#album	=ie["album"]
				artist	=ie[1]
				title	=ie[3]
				#img		=ie["cover"]
				url		=ie[2]
				dlurl	=ie[2]
				urlart	=ie[0]
				title2 = artist+" - [B]"+title+"[/B]"
				
				trk='[COLOR F050F050][T] [/COLOR]'
				item = xbmcgui.ListItem(trk+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist})#, "album":album
				
				dict={"dlurl":dlurl, "title":title, "artist":artist, "cover":"", "album":""}
				uri = sys.argv[0] + '?mode=save'
				uri += '&info='  + urllib.quote_plus(repr(dict))
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)
				
				if artist.find(" feat.")>0: artist1=artist[:artist.find(" feat.")]
				else: artist1=artist
				uri2 = sys.argv[0] + '?mode=serchalbums'
				uri2 += '&url='  + urllib.quote_plus(urlart)
				uri2 += '&name='  + urllib.quote_plus(artist1)
				uri2 += '&img='  + urllib.quote_plus(img)
				
				item.addContextMenuItems([('[COLOR F050F050] Сохранить [/COLOR]', 'Container.Update("plugin://plugin.audio.myzuka.org/'+uri+'")'),('[COLOR F050F050] Исполнитель [/COLOR]', 'Container.Update("plugin://plugin.audio.myzuka.org/'+uri2+'")')])
				
				uri = sys.argv[0] + '?mode=play'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title2)
				uri += '&img='  + urllib.quote_plus(img)

				if title2 not in Lt:
					xbmcplugin.addDirectoryItem(pluginhandle, uri, item, False,500)
					Lt.append(title2)
			except: pass
		return Lt

def Album(url, Lt=[]):
		#print url
		http=getURL(url)
		http=http.replace('  ','')
		http=http.replace(chr(10),'').replace(chr(13),'')
		try:
			ss='<div data-type="'
			es='</a></div></div>'
			L=mfindal(http, ss, es)
		except:
			L=[]
		#print L
		for i in L:
			try:
				#print i
				it=i.replace('<div data-type=' ,'{"type":')
				it=it.replace(' class="item "><div class="vis"><a href=',' ,"url":')
				it=it.replace('><img src=',' ,"cover":')
				it=it.replace('amp;','')
				it=rt(it)
				it=it.replace(' alt=',' ,"album":')
				it=it.replace(' data-qazy=true></a><div class="overlay"><ul><li>Аплоадер: <a href="/Profile/',' ,"uploader": ("')
				it=it.replace('</a> </li><li>Добавлен: ','") ,"load":"')
				it=it.replace('</li><li>Рейтинг: ','", "rat": "')
				it=it.replace('</li></ul></div></div><div class="info"><div class="title"><a href=','" ,"url2":(')
				it=it.replace('</a></div><div class="tags"><a href=','"), "genre":(')
				it=it.replace('</a></div><div class="tags">Год релиза: <a href=','"), "year": (')
				it=it.replace('">','","')
				it=it.replace('</a> / <a href="','","')
				it=it.replace(': <a href="', '"), "year": ("')
				it=it.replace('class="tags', '')
				it=it+'")}'
				
				it=it.strip()
				#print it
				dict=eval(it)
				
				ss='<title>'
				es=': скачать альбомы и сборники'
				artist=rt(mfindal(http, ss, es)[0][len(ss):])#.replace("&#039;","'")

				dict["artist"] = rt(artist)
				album	=dict["album"]#.replace("&#039;","'")
				img		=dict["cover"]
				url		=dict["url"]
				type	=dict["type"]
				year	=dict["year"][1]
				title=artist+" - "+album+" ("+year+")"
				
				alb='[COLOR F07070F0][А] [/COLOR]'
				item = xbmcgui.ListItem(alb+title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={ "artist":artist, "album":album, "year":year})#"title":album,
				
				uri = sys.argv[0] + '?mode=save_all'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				
				uri2 = sys.argv[0] + '?mode=srcartist_q'
				uri2 += '&name='  + urllib.quote_plus(artist)
				uri2 += '&img='  + urllib.quote_plus(img)
				
				item.addContextMenuItems([('[COLOR F050F050] Сохранить альбом [/COLOR]', 'Container.Update("plugin://plugin.audio.myzuka.org/'+uri+'")'),])#('[COLOR F050F050] Исполнитель [/COLOR]', 'Container.Update("plugin://plugin.audio.kibergrad.com/'+uri2+'")')
				
				uri = sys.argv[0] + '?mode=serchtracs'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)

				if title not in Lt and type=="2":
					xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True,len(L))
					Lt.append(title)
			except:pass
		return Lt

def Save(dict, name, update=1):
	target	=dict["dlurl"]
	#print target
	artist	=dict["artist"]
	title	=dict["title"]
	img		=dict["cover"]
	#print img
	album	=dict["album"].strip()

	Dldir = __settings__.getSetting("DownloadDirectory")
	if Dldir == "":Dldir = os.path.join( addon.getAddonInfo('path'), "mp3" )
	
	fp = os.path.join(ru(Dldir), ru(artist))
	fp = os.path.join(fp, ru(album))
	if os.path.exists(fp)== False: os.makedirs(fp)
	cp=os.path.join(fp, "cover.jpg")
	fp = os.path.join(fp, ru(title+".mp3"))
	#try:
	if 1==1:
			req = urllib2.Request(url = target, data = None)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			fl = open(fp, "wb")
			fl.write(resp.read())
			fl.close()
			if os.path.exists(cp)== False and img !="":
				req = urllib2.Request(url = img, data = None)
				req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
				resp = urllib2.urlopen(req)
				fl = open(cp, "wb")
				fl.write(resp.read())
				fl.close()
			
			retag(fp, dict)
			#print "Update"
			if update==1: xbmc.executebuiltin('UpdateLibrary("music")')
			
			return fp
	#except Exception, e:
	#		#xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
	#		return target
	#		print 'HTTP ERROR ' + str(e)


def Play(url):
	http=getURL(url)
	ss='data-url="/Song/Play/'
	es='" data-position = "'
	purl=mfindal(http, ss, es)[0].replace(ss,"https://myzuka.org/Song/Download/").replace('amp;','')
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(purl)


params = get_params()
url  =	'https://myzuka.org'
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
elif mode == 'save_all':	Serch_in_album(url, S=1)
elif mode == 'srcartist':	SrcArtist()
elif mode == 'srcartist_q':	SrcArtist(name)
elif mode == 'play':	Play(url)