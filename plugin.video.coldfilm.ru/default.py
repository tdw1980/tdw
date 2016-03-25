# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, sys, urllib2

PLUGIN_NAME   = 'coldfilm.ru'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.coldfilm.ru')
__settings__ = xbmcaddon.Addon(id='plugin.video.coldfilm.ru')

Pdir = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

try:
	import tthp
except:
	print "Error import t2http"


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



def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t


def play(url, id=0):
	print url
	engine=__settings__.getSetting("Engine")
	if engine=="0":
		play_ace(url, id)
		
	if engine=="1":
		item = xbmcgui.ListItem()#path=url
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
		tthp.play(url, handle, id, __settings__.getSetting("DownloadDirectory"))
		
	if engine=="2":
		purl ="plugin://plugin.video.yatp/?action=play&torrent="+ urllib.quote_plus(url)+"&file_index="+str(id)
		item = xbmcgui.ListItem()#path=purl
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
		xbmc.Player().play(purl)


def play_ace(torr_link, ind):
	from TSCore import TSengine as tsengine
	aceport=62062
	img=""
	title="title"
	TSplayer=tsengine()
	out=TSplayer.load_torrent(torr_link,'TORRENT',port=aceport)
	if out=='Ok':
		TSplayer.play_url_ind(int(ind),title, icon, img)
	TSplayer.end()


def add_item (name, mode="", path = Pdir, ind="0", cover=None, funart=None):
	#print name
	#print path
	if   path.find("720p")>0: qual="[COLOR FFA900EF][ 720p ] [/COLOR]"
	elif path.find("480p")>0: qual="[COLOR FFFF0090][ 480p ] [/COLOR]"
	elif path.find("400p")>0: qual="[COLOR FF70F020][ 400p ] [/COLOR]"
	elif path.find("1080p")>0:qual="[COLOR FF50FF50][1080p] [/COLOR]"
	else: qual="[ ???? ] "
	if cover==None:	listitem = xbmcgui.ListItem(qual+"[B]"+name+"[/B]")
	else:			listitem = xbmcgui.ListItem(qual+"[B]"+name+"[/B]", iconImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	uri += '&name='  + urllib.quote_plus(xt(name))
	uri += '&ind='  + urllib.quote_plus(ind)
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	if mode=="play": fld=False
	else: fld=True

	xbmcplugin.addDirectoryItem(handle, uri, listitem, fld)

def getURL(url,Referer = 'http://coldfilm.ru/'):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
	req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
	req.add_header('Accept-Language', 'ru,en;q=0.9')
	req.add_header('Referer', Referer)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def get_rss():
	url='http://coldfilm.ru/news/rss'
	rss=getURL(url)
	return rss

def pars_rss(rss):
	L=mfindal(rss, '<item>', '</item>')
	L2=[]
	for i in L:
		title=mfindal(i, '<title>', '</title>')[0][7:]
		description=mfindal(i, '<description>', '</description>')[0][13:]
		try: cover=mfindal(i, 'src=&quot;', '&quot; title=&quot;')[0][10:]
		except: cover=""
		content=mfindal(i, '<content:encoded>', '</content:encoded>')[0][17:]
		Lt=mfindal(i, 'http://coldfilm.ru/torrent', '.torrent')
		for t in Lt:
			dict={'title':title.replace('[Смотреть Онлайн]',''), 'url':t+'.torrent', 'cover':cover}
			L2.append(dict)
		Lm=mfindal(i, 'http://videoapi.my.mail.ru', '&quot; webkitallowfullscreen')
		#for m in Lm:
		#	urm=m.replace('embed/','').replace('.html','.json')
		#	dict={'title':title.replace('[Смотреть Онлайн]',''), 'url':urm, 'cover':cover}
		#	L2.append(dict)
	return L2

def get_mv(url):
	#'http://videoapi.my.mail.ru/videos/embed/mail/dim_kalchenko/_myvideo/1015.html'
	#'http://videoapi.my.mail.ru/videos/mail/dim_kalchenko/_myvideo/1015.json'
	
	j=getURL(url,url).replace('true','True').replace('false','False')
	jsn=eval(j)
	L=jsn["videos"]
	for i in L:
		key=i['key']
		url=i['url']
	return url

def root():
	rss=get_rss()
	L=pars_rss(rss)
	for i in L:
		name  = i['title']
		url   = i['url']
		cover = i['cover']
		if url.find("400p")<0 or __settings__.getSetting("Qual")=="1":
			add_item (name, 'play', url, str(0),cover)
	xbmcplugin.endOfDirectory(handle)

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

params = get_params()

try:mode = urllib.unquote_plus(params["mode"])
except:mode =""
try:name = urllib.unquote_plus(params["name"])
except:name =""
try:url = urllib.unquote_plus(params["url"])
except:url =""
try:ind = urllib.unquote_plus(params["ind"])
except:ind ="0"


if mode==""         : root()
if mode=="add"      : add(name, url)
if mode=="play"     : play(url, int(ind))#updatetc.play(url, int(ind))
if mode=="rename"   : updatetc.rename_list(int(ind))
if mode=="epd_lst"  : 
	if url[:4]!='plug':epd_lst(name, url, ind)
if mode=="add_filtr": add_filtr(url, ind)
if mode=="rem_filtr": 
	updatetc.rem_filtr(int(ind))
	xbmc.executebuiltin("Container.Refresh")
if mode=="rem_files": 
	updatetc.rem(name)
	updatetc.update()
if mode=="rem": 
	updatetc.rem_list(int(ind))
	xbmc.executebuiltin("Container.Refresh")

