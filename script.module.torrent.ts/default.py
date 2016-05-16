# -*- coding: utf-8 -*-

import sys
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='script.module.torrent.ts')
__plugin__ = __settings__.getAddonInfo('name')
__root__ = __settings__.getAddonInfo('path')

if __name__ == "__main__":
    __settings__.openSettings()
