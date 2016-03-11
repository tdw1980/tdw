# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmc
import updatetc
import time
import xbmcgui
icon=None

time.sleep(2.0)
print('----- Starting Torrent Checker -----')
start_trigger = True
n=0
while not xbmc.abortRequested:
		if start_trigger:
			print('----- Torrent Checker started -----')
			xbmcgui.Dialog().notification('Torrent Checker', 'Запущен', icon, 1000, False)
			start_trigger = False
			updatetc.update()
		# ---------------------------------
		time.sleep(1)
		n+=1
		upint=6*360
		if n>= upint:
			n=0
			updatetc.update()

print('----- Torrent Checker stopped -----')

