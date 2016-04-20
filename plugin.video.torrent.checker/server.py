# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmc, xbmcgui, xbmcaddon
import updatetc
import time
import xbmcgui
__settings__ = xbmcaddon.Addon(id='plugin.video.torrent.checker')
icon=None

time.sleep(2.0)
print('----- Starting Torrent Checker -----')
start_trigger = True
#n=0
while not xbmc.abortRequested:
		if start_trigger:
			print('----- Torrent Checker started -----')
			#xbmcgui.Dialog().notification('Torrent Checker', 'Запущен', icon, 1000, False)
			start_trigger = False
			updatetc.update()
		# ---------------------------------
		time.sleep(1)
		#n+=1
		iv = 2*int(__settings__.getSetting("Interval"))
		if iv==0: iv=1
		upint=iv*3600
		try:
			lu=eval(__settings__.getSetting("LU"))
		except:
			__settings__.setSetting("LU", repr(time.time()))
			lu=time.time()
		n=time.time()-lu
		if n>= upint:
			n=0
			updatetc.update()
			__settings__.setSetting("LU", repr(time.time()))

print('----- Torrent Checker stopped -----')

