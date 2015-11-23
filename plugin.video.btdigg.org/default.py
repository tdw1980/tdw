#!/usr/bin/python
# -*- coding: utf-8 -*-
# *      Copyright (C) 2015 TDW

import string, xbmc, xbmcgui, xbmcplugin, os, xbmcaddon, time, codecs, urllib

siteUrl = 'www.btdigg.org'
httpSiteUrl = 'http://' + siteUrl
sid_file = os.path.join(xbmc.translatePath('special://temp/'), 'plugin.video.btdigg.org.cookies.sid')

PLUGIN_NAME   = 'btdigg.org'
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.btdigg.org')

icon = xbmc.translatePath(os.path.join(addon.getAddonInfo('path'), 'icon.png'))
thumb = os.path.join( addon.getAddonInfo('path'), "icon.png" )
fanart = os.path.join( addon.getAddonInfo('path'), "fanart.jpg" )

__settings__ = xbmcaddon.Addon(id='plugin.video.btdigg.org')

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


def rulower(str):
	str=str.strip()
	str=xt(str).lower()
	str=str.replace('Й','й')
	str=str.replace('Ц','ц')
	str=str.replace('У','у')
	str=str.replace('К','к')
	str=str.replace('Е','е')
	str=str.replace('Н','н')
	str=str.replace('Г','г')
	str=str.replace('Ш','ш')
	str=str.replace('Щ','щ')
	str=str.replace('З','з')
	str=str.replace('Х','х')
	str=str.replace('Ъ','ъ')
	str=str.replace('Ф','ф')
	str=str.replace('Ы','ы')
	str=str.replace('В','в')
	str=str.replace('А','а')
	str=str.replace('П','п')
	str=str.replace('Р','р')
	str=str.replace('О','о')
	str=str.replace('Л','л')
	str=str.replace('Д','д')
	str=str.replace('Ж','ж')
	str=str.replace('Э','э')
	str=str.replace('Я','я')
	str=str.replace('Ч','ч')
	str=str.replace('С','с')
	str=str.replace('М','м')
	str=str.replace('И','и')
	str=str.replace('Т','т')
	str=str.replace('Ь','ь')
	str=str.replace('Б','б')
	str=str.replace('Ю','ю')
	return str

def btd(text):
	
	listitem = xbmcgui.ListItem("[COLOR FF0FFF0F] НОВЫЙ ПОИСК[/COLOR]")
	url = 'plugin://plugin.video.btdigg.org/?mode=s'
	xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True)
	
	
	import btdigg
	digg=btdigg.Tracker()
	RL=digg.Search(text)
	L1=[]
	L2=[]
	
	for y in range (1970, 2018):
		sy=" "+str(y)
		text=text.replace(sy,"")
	
	for itm in RL:
		if rulower(xt(itm[2])).find(rulower(text))<0:	L2.append(itm)
		else:					L1.append(itm)
	
	for itm in L1:
				Title = "[COLOR FFFFFFFF]"+itm[0]+"|"+itm[1]+"|  "+itm[2]+"[/COLOR]"
				row_url = itm[3]
				cover=""
				listitem = xbmcgui.ListItem(Title, thumbnailImage=cover, iconImage=cover)
				#listitem.setProperty('fanart_image', cover)
				url = 'plugin://plugin.video.yatp/?action=list_files&torrent='+ urllib.quote_plus(row_url)
				xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True)
	
	for itm in L2:
				Title = itm[0]+"|"+itm[1]+"|  "+itm[2]
				row_url = itm[3]
				cover=""
				listitem = xbmcgui.ListItem(Title, thumbnailImage=cover, iconImage=cover)
				#listitem.setProperty('fanart_image', cover)
				url = 'plugin://plugin.video.yatp/?action=list_files&torrent='+ urllib.quote_plus(row_url)
				xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, isFolder=True)


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


if mode == None :
	btd(inputbox())
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	xbmc.sleep(300)
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
if mode == 's':
	btd(inputbox())
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle, True, True)
	xbmc.sleep(300)
	xbmc.executebuiltin("Container.SetViewMode(51)")
