# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, sys
import updatetc

PLUGIN_NAME   = 'torrent.checker'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.torrent.checker')
__settings__ = xbmcaddon.Addon(id='plugin.video.torrent.checker')

Pdir = addon.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

try:
	import tthp
except:
	print "Error import t2http"




def inputbox(t):
	skbd = xbmc.Keyboard(t, 'Название:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return t

#---------asengine----by-nuismons-----

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

def play_ace(url, ind):
    from ASCore import TSengine,_TSPlayer
    #print 'play'
    torr_link=url
        
    img=""
    title=""
    #showMessage('heading', torr_link, 10000)
    TSplayer=TSengine()
    out=TSplayer.load_torrent(torr_link,'TORRENT')
    if out=='Ok':
        lnk=TSplayer.get_link(ind,title, img, img)
        if lnk:
           
            item = xbmcgui.ListItem(path=lnk, thumbnailImage=img, iconImage=img)
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)  

            while not xbmc.Player().isPlaying:
                xbmc.sleep(300)
            while TSplayer.player.active and not TSplayer.local: 
                TSplayer.loop()
                xbmc.sleep(300)
                if xbmc.abortRequested:
                    TSplayer.log.out("XBMC is shutting down")
                    break
            if TSplayer.local and xbmc.Player().isPlaying: 
                try: time1=TSplayer.player.getTime()
                except: time1=0
                
                i = xbmcgui.ListItem("***%s"%title)
                i.setProperty('StartOffset', str(time1))
                xbmc.Player().play(TSplayer.filename.decode('utf-8'),i)

        else:
            item = xbmcgui.ListItem(path='')
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), False, item) 
    TSplayer.end()
    xbmc.Player().stop


def add_item (name, mode="", path = Pdir, ind="0", cover=None, funart=None):
	if cover==None:	listitem = xbmcgui.ListItem(name)
	else:			listitem = xbmcgui.ListItem(name, iconImage=cover)
	listitem.setProperty('fanart_image', funart)
	uri = sys.argv[0] + '?mode='+mode
	uri += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	uri += '&name='  + urllib.quote_plus(xt(name))
	uri += '&ind='  + urllib.quote_plus(ind)
	if cover!=None:uri += '&cover='  + urllib.quote_plus(cover)
	if funart!=None and funart!="":uri += '&funart='  + urllib.quote_plus(funart)
	
	
	urr = sys.argv[0] + '?mode=rem'
	urr += '&path='  + urllib.quote_plus(path.encode('utf-8'))
	urr += '&name='  + urllib.quote_plus(xt(name))
	urr += '&ind='  + urllib.quote_plus(ind)

	urr2 = sys.argv[0] + '?mode=rename'
	urr2 += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	urr2 += '&name='  + urllib.quote_plus(xt(name))
	urr2 += '&ind='  + urllib.quote_plus(ind)
	
	urr3 = sys.argv[0] + '?mode=rem_files'
	urr3 += '&url='  + urllib.quote_plus(path.encode('utf-8'))
	urr3 += '&name='  + urllib.quote_plus(xt(name))
	urr3 += '&ind='  + urllib.quote_plus(ind)

	if mode=="epd_lst":listitem.addContextMenuItems([('[COLOR F050F050] Удалить задание[/COLOR]', 'Container.Update("plugin://plugin.video.torrent.checker/'+urr+'")'),('[COLOR F050F050] Переименовать [/COLOR]', 'Container.Update("plugin://plugin.video.torrent.checker/'+urr2+'")'),('[COLOR F050F050] Обновить файлы [/COLOR]', 'Container.Update("plugin://plugin.video.torrent.checker/'+urr3+'")')])

	xbmcplugin.addDirectoryItem(handle, uri, listitem, True)


def root():
	L=updatetc.get_list()
	ind=0
	for i in L:
		name  = i[0]
		url   = i[1]
		add_item (name, 'epd_lst', url, str(ind))
		ind+=1
	xbmcplugin.endOfDirectory(handle)

def epd_lst(name, url, ind):
	f=updatetc.get_filtr(int(ind))
	L=tthp.list(url)#updatetc.file_list(name)
	
	add_item ('[B][ - ] Удалить правила переименования[/B] ', 'rem_filtr', url, str(ind))
	add_item ('[B][+] Добавить правило переименования: '+str(len(f))+'[/B]: ', 'add_filtr', L[0].name.replace('\\'," "), str(ind))
	
	for i in L:
		epd_name=i.name.replace('\\'," ")
		epd_name_f=""
		for j in f:
			opid=j[0]
			if opid=="t":epd_name_f+=j[1]
			else:epd_name_f+=epd_name[j[0]:j[1]+1]
		epd_name_f+=".strm"
		if f==[]:epd_name_f=epd_name+".strm"
		add_item (epd_name+chr(10)+epd_name_f, 'none', url, str(ind))
	xbmcplugin.endOfDirectory(handle)

def add_filtr(name, ind):
	sel = xbmcgui.Dialog()
	opl=["Текст", "Диапазон"]
	k = sel.select("Тип:", opl)
	if k==0:
		t=inputbox(name)
		if t<>"":updatetc.filtr_list(int(ind), ("t", t))
	elif k==1:
		s=name#updatetc.file_list(name)[0]
		n = sel.select("Начало диапазона:", list(s))
		k = sel.select("Конец диапазона:", list(s))
		updatetc.filtr_list(int(ind), (n, k))
	xbmc.executebuiltin("Container.Refresh")


def add(name, url):
	updatetc.add_list([name, url,[]])
	#xbmcplugin.endOfDirectory(handle)

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
if mode=="epd_lst"  : epd_lst(name, url, ind)
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

