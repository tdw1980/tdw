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
("Jazz", "[COLOR F0E0E067]Джаз[/COLOR]"),
("Hits", "[COLOR F050F050]Хиты[/COLOR]")
]

ArtistList=[
("http://kibergrad.com/578/2517", "25/17"),
("http://kibergrad.com/63/acdc", "AC/DC")
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
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				title="[COLOR F0E0E067][B][ Исполнители ][/B][/COLOR]"
				url=""
				img=thumb
				uri = sys.argv[0] + '?mode=artist'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)
				item = xbmcgui.ListItem(title, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"Title": title})
				#xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True)

				#Serch("http://kibergrad.com/popular-music")

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
				title="[COLOR F0E0E067][B][ Поиск ][/B][/COLOR]"
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
				print url
				Lt=Serch_in_album('https://myzuka.org'+url)
				xbmcplugin.endOfDirectory(pluginhandle)

def Serch_in_album(url, Lt=[]):
	http=getURL(url)
	try:
		ss='itemprop="image" src="'
		es='<div class="share-block">'
		img=mfindal(http, ss, es)[0][len(ss):].replace(chr(10),'').replace(chr(13),'').replace('"/>        </div>','').replace('amp;','')
	except:img=""
	try:
		ss='<h1>'
		es='</h1>'
		album2=mfindal(http, ss, es)[0][len(ss):-6].replace('amp;','')
	except:album2=""
	try:
		ss='<h1>'
		es='</h1>'
		year=mfindal(http, ss, es)[0][-5:-1]
	except:year=""

	try:
		ss='data-url="/Song/Play/'
		es='><!---->'
		L=mfindal(http, ss, es)
	except:
		L=[]
	tnb=0
	for i in L:
		try:
			if len (i)>10:
				i=i.replace('data-url=','{"url":')
				i=i.replace('amp;','')
				i=i.replace('title="Слушать ',',"artist":"')
				i=i.replace(' - ','", "title":"')
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
				
				xbmcplugin.addDirectoryItem(pluginhandle, purl, item, False, len(L))
		except:pass


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
				i='["'+i+"]"
				ie=eval(i)
				
				img=""
				#album	=ie["album"]
				artist	=ie[1]
				title	=ie[3]
				#img		=ie["cover"]
				url		=ie[2]
				urlart	=ie[0]
				title2 = artist+" - [B]"+title+"[/B]"
				
				trk='[COLOR F050F050][T] [/COLOR]'
				item = xbmcgui.ListItem(trk+title2, iconImage = img, thumbnailImage = img)
				item.setInfo(type="Music", infoLabels={"title":title, "artist":artist})#, "album":album
				
				
				uri = sys.argv[0] + '?mode=save'
				uri += '&info='  + urllib.quote_plus(i)
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
				artist=mfindal(http, ss, es)[0][len(ss):]#.replace("&#039;","'")

				dict["artist"] = artist
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
				
				item.addContextMenuItems([('[COLOR F050F050] Сохранить альбом [/COLOR]', 'Container.Update("plugin://plugin.audio.kibergrad.com/'+uri+'")'),('[COLOR F050F050] Исполнитель [/COLOR]', 'Container.Update("plugin://plugin.audio.kibergrad.com/'+uri2+'")')])
				
				uri = sys.argv[0] + '?mode=serchtracs'
				uri += '&url='  + urllib.quote_plus(url)
				uri += '&name='  + urllib.quote_plus(title)
				uri += '&img='  + urllib.quote_plus(img)

				if title not in Lt and type=="2":
					xbmcplugin.addDirectoryItem(pluginhandle, uri, item, True,len(L))
					Lt.append(title)
			except:pass
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
	print target
	artist	=dict["artist"]
	title	=dict["title"]
	img		=dict["cover"]
	print img
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
			
			return fp
	#except Exception, e:
	#		#xbmc.log( '[%s]: GET EXCEPT [%s]' % (addon_id, e), 4 )
	#		return target
	#		print 'HTTP ERROR ' + str(e)


def Play(url):
	http=getURL(url)
	ss='data-url="/Song/Play/'
	es='" title="Слушать'
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
elif mode == 'save_all':	SaveAll(url)
elif mode == 'srcartist':	SrcArtist()
elif mode == 'srcartist_q':	SrcArtist(name)
elif mode == 'play':	Play(url)