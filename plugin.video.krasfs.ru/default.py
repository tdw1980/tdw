#!/usr/bin/python
# -*- coding: utf-8 -*-
# *      Copyright (C) 2013 TDW



import string, xbmc, xbmcgui, xbmcplugin, os, xbmcaddon, time, codecs, urllib


siteUrl = 'www.krasfs.ru'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'plugin.video.krasfs.ru.cookies.sid')

PLUGIN_NAME   = 'krasfs'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.krasfs.ru')

icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
thumb = os.path.join( addon.getAddonInfo('path'), "icon.png" )
fanart = os.path.join( addon.getAddonInfo('path'), "fanart.jpg" )

__settings__ = xbmcaddon.Addon(id='plugin.video.krasfs.ru')

xbmcplugin.setContent(int(sys.argv[1]), 'movies')

def debug(s):
	fl = open(os.path.join( ru(addon.getAddonInfo('path')),"test.txt"), "w")
	fl.write(s)
	fl.close()
def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def inputbox():
	skbd = xbmc.Keyboard()
	skbd.setHeading('Поиск:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return ""

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)

#--------------- krasfs --------------
import krasfs
tft=krasfs.Tracker()

def stft(text):
	RL=tft.Search(text, 4)
	#if len(RL)>0:
	#	Title = "[COLOR F050F050]"+"[-------  Мультимедийный портал «KrasFS.ru»  ---------]"+"[/COLOR]"
	#	row_url = Title
	#	listitem = xbmcgui.ListItem(Title)
	#	listitem.setInfo(type = "Video", infoLabels = {"Title": Title} )
	#	purl = sys.argv[0] + '?mode=Search'\
	#		+ '&url=' + urllib.quote_plus(row_url)\
	#		+ '&title=' + urllib.quote_plus(Title)\
	#		+ '&text=' + urllib.quote_plus('0')
	#	xbmcplugin.addDirectoryItem(handle, purl, listitem, True)

	for itm in RL:
		n=0
		for i in ["PDF","pdf","FLAC","flac","FB2","fb2","MP3","mp3","PNG","png","ISO","iso","JPG","jpg","DJVU","djvu",".APE",".ape",".RTF",".rtf",".TXT",".txt",".DOC",".doc",".AC3",".ac3",".ZIP",".zip",".RAR",".rar",".EXE",".exe"]:
			filtr=itm[2].find(i)
			if filtr>0:n+=1
		if n==0:
				Title = itm[0]+"|"+itm[1]+"|  "+itm[2]
				row_url = itm[3]
				cover=""
				dict={}
				listitem = xbmcgui.ListItem(Title, thumbnailImage=cover, iconImage=cover)
				listitem.setProperty('fanart_image', cover)
				purl = sys.argv[0] + '?mode=play_url'\
					+ '&url=' + urllib.quote_plus(row_url)\
					+ '&title=' + urllib.quote_plus(Title)
				xbmcplugin.addDirectoryItem(handle, purl, listitem, True)


#---------tsengine----by-nuismons-----

from TSCore import TSengine as tsengine
prt_file= __settings__.getSetting('port_path')
aceport=62062
try:
	if prt_file: 
		gf = open(prt_file, 'r')
		aceport=int(gf.read())
		gf.close()
except: prt_file=None

if not prt_file:
	try:
		fpath= os.path.expanduser("~")
		pfile= os.path.join(fpath,'AppData\Roaming\TorrentStream\engine' ,'acestream.port')
		gf = open(pfile, 'r')
		aceport=int(gf.read())
		gf.close()
		__settings__.setSetting('port_path',pfile)
	except: aceport=62062

def play_url(params):
	torr_link=params['file']
	img=urllib.unquote_plus(params["img"])
	#showMessage('heading', torr_link, 10000)
	TSplayer=tsengine()
	out=TSplayer.load_torrent(torr_link,'TORRENT',port=aceport)
	if out=='Ok':
		for k,v in TSplayer.files.iteritems():
			li = xbmcgui.ListItem(urllib.unquote(k))
			uri = construct_request({
				'torr_url': torr_link,
				'title': k,
				'ind':v,
				'img':img,
				'mode': 'play_url2'
			})
			xbmcplugin.addDirectoryItem(handle, uri, li, False)
	xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.endOfDirectory(handle)
	TSplayer.end()
	
def play_url2(params):
	#torr_link=params['torr_url']
	torr_link=urllib.unquote_plus(params["torr_url"])
	img=urllib.unquote_plus(params["img"])
	title=urllib.unquote_plus(params["title"])
	#showMessage('heading', torr_link, 10000)
	TSplayer=tsengine()
	out=TSplayer.load_torrent(torr_link,'TORRENT',port=aceport)
	if out=='Ok':
		TSplayer.play_url_ind(int(params['ind']),title, icon, img)
	TSplayer.end()

#=======================================


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
mode     = None
url      = ''
title    = ''
ref      = ''
img      = ''
text     = '0'


try:
	mode  = urllib.unquote_plus(params["mode"])
except:
	pass

try:
	url  = urllib.unquote_plus(params["url"])
except:
	pass

try:
	title  = urllib.unquote_plus(params["title"])
except:
	pass

try:
	img  = urllib.unquote_plus(params["img"])
except:
	pass

try:
	text  = urllib.unquote_plus(params["text"])
except:
	pass



if mode == None:
	stft(inputbox())
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
if mode == 's':
	stft(text)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
elif mode == 'play_url':
	play_url({'file':url,'img':img})
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

elif mode == 'play_url2':
	play_url2(params)
