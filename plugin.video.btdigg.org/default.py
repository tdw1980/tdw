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


def btd(text):
	import btdigg
	digg=btdigg.Tracker()
	RL=digg.Search(text)
	for itm in RL:
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


if mode == None:
	btd(inputbox())
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	xbmc.executebuiltin("Container.SetViewMode(51)")
	
if mode == 's':
	btd(inputbox())
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
	xbmc.executebuiltin("Container.SetViewMode(51)")
