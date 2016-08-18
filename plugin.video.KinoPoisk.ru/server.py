# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmc, xbmcgui, xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.KinoPoisk.ru')

print('----- KinoPoisk.ru started -----')
start_trigger = False
xbmc.sleep(10000)

while not xbmc.abortRequested:
		xbmc.executebuiltin('RunPlugin("plugin://plugin.video.KinoPoisk.ru/?mode=check")')
		for i in range(0, 6000):
				xbmc.sleep(3000)
				if xbmc.abortRequested: break
				xbmc.sleep(3000)
				if xbmc.abortRequested: break

print('----- KinoPoisk.ru stopped -----')

