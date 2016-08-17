# coding: utf-8
# Module: server
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys
import xbmc, xbmcgui, xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.KinoPoisk.ru')

print('----- KinoPoisk.ru started -----')
start_trigger = False
xbmc.sleep(10000)
xbmc.executebuiltin('RunPlugin("plugin://plugin.video.KinoPoisk.ru/?mode=check")')

print('----- KinoPoisk.ru stopped -----')

