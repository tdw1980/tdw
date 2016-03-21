# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, sys, urllib2

PLUGIN_NAME   = 'newstudio.tv'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.newstudio.tv')
__settings__ = xbmcaddon.Addon(id='plugin.video.newstudio.tv')

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
	if cover==None:	listitem = xbmcgui.ListItem("[B]"+name+"[/B]")
	else:			listitem = xbmcgui.ListItem("[B]"+name+"[/B]", iconImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	uri += '&name='  + urllib.quote_plus(xt(name))
	uri += '&ind='  + urllib.quote_plus(ind)
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	if mode=="play": fld=False
	else: fld=True
	
	
	lf_name=name[name.find('/ ')+2:]
	lf_url='plugin://plugin.video.newstudio.tv/?mode=GetTC&name='+urllib.quote_plus(lf_name)

	listitem.addContextMenuItems([('[B]Отслеживать в ТС[/B]', 'Container.Update("plugin://plugin.video.torrent.checker/?mode=add&url='+urllib.quote_plus(lf_url)+'&name='+lf_name+'")'),])
	xbmcplugin.addDirectoryItem(handle, uri, listitem, fld)

def getURL(url,Referer = 'http://newstudio.tv/'):
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
	url='http://newstudio.tv/'
	rss=getURL(url)
	return rss

def pars_rss(rss):
	L=mfindal(rss, '<div class="torrent">', '</div>'+chr(10)+'</div>')
	L2=[]
	for i in L:
		try:
			title2=mfindal(i, ') / ', ' (20')[0][4:]
			title=mfindal(i, '<div class="tdesc">', ' (20')[0][25:].replace('&#039;','')
			#description=mfindal(i, '<description>', '</description>')[0][13:]
			try: cover='http://newstudio.tv'+mfindal(i, '/images/posters', '" alt="pic" class="img-tracker"')[0]
			except: cover=""
			#content=mfindal(i, '<div class="pull-right taright">', '<div class="ttitle">')[0]
			Lt=mfindal(i, '/download.php?id=', '</span></a>')
			n=0
			for t in Lt:
				n+=1
				try:
					url='http://newstudio.tv'+mfindal(t, '/download.php?id=', '"><span class=')[0]
					qual=t[t.find('link">Скачать '):]
					dict={'title':title, 'title2':title2, 'url':url, 'cover':cover, 'qual':qual}
					if n==1 or __settings__.getSetting("Qual")=="1":
						L2.append(dict)
				except: pass
		except: pass
	return L2

def GetTC(ntc):
	rss=get_rss()
	L=pars_rss(rss)
	for i in L:
		name  = i['title']
		url   = i['url']
		cover = i['cover']
		qual  = i['qual']
		if name.find(ntc)>0:
			s=name.find(" (")
			e=name.find(") ")
			nm=ntc+name[s:e]+".strm"
			nm=nm.replace(" (Сезон ",".s")
			nm=nm.replace(", Серия ","e")
			for n in range(1,10):
				nm=nm.replace("s"+str(n)+"e","s0"+str(n)+"e")
				nm=nm.replace("e"+str(n)+".","e0"+str(n)+".")
				
			sys.path.append(os.path.join(xbmc.translatePath("special://home/"),"addons","plugin.video.torrent.checker"))
			import updatetc
			LD=updatetc.file_list(ntc)
			if  nm not in LD:
				if __settings__.getSetting("Qual")=="1":
					if   qual.find("720p")>0: updatetc.save_strm(ntc, nm, url, 0)
				else:
					updatetc.save_strm(ntc, nm, url, 0)
	xbmc.executebuiltin('UpdateLibrary("video")')

def root():
	rss=get_rss()
	L=pars_rss(rss)
	ind=0
	for i in L:
		name  = i['title']
		url   = i['url']
		cover = i['cover']
		qual  = i['qual']
		
		if   qual.find("720p")>0: qual="[COLOR FFA900EF][ 720p ] [/COLOR]"
		elif qual.find("480p")>0: qual="[COLOR FFFF0090][ 480p ] [/COLOR]"
		elif qual.find("400p")>0: qual="[COLOR FFFF0090][ 400p ] [/COLOR]"
		elif qual.find("1080p")>0:qual="[COLOR FF50FF50][1080p] [/COLOR]"
		else: qual="[ "+qual+" ] "

		add_item (qual+name, 'play', url, str(0),cover)
		ind+=1
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
	
if mode=="GetTC": GetTC(name)
