#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
import xbmc, xbmcgui, xbmcplugin

sys.path.append(os.path.join(xbmc.translatePath("special://home/"),"addons","script.module.torrent2http","lib"))
from torrent2http import State, Engine, MediaType
from contextlib import closing
progressBar = xbmcgui.DialogProgress()

def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)


def list(uri):
  # Create instance of Engine 
  engine = Engine(uri)
  files = []
  # Ensure we'll close engine on exception 
  with closing(engine):
    # Start engine 
    engine.start()
    # Wait until files received 
    while not files and not xbmc.abortRequested:
        # Will list only video files in torrent
        files = engine.list(media_types=[MediaType.VIDEO])
        # Check if there is loading torrent error and raise exception 
        engine.check_torrent_error()
        xbmc.sleep(200)
  return files

def play(uri, handle, file_id=0, DDir=""):
  print DDir
  if DDir=="": DDir=os.path.join(xbmc.translatePath("special://home/"),"userdata")
  progressBar.create('Torrent2Http', 'Запуск')
  # XBMC addon handle
  # handle = ...
  # Playable list item
  # listitem = ...
  # We can know file_id of needed video file on this step, if no, we'll try to detect one.
  # file_id = None
  # Flag will set to True when engine is ready to resolve URL to XBMC
  ready = False
  # Set pre-buffer size to 15Mb. This is a size of file that need to be downloaded before we resolve URL to XMBC 
  pre_buffer_bytes = 15*1024*1024
  engine = Engine(uri, download_path=DDir)
  with closing(engine):
    # Start engine and instruct torrent2http to begin download first file, 
    # so it can start searching and connecting to peers  
    engine.start(file_id)
    progressBar.update(0, 'Torrent2Http', 'Загрузка торрента', "")
    while not xbmc.abortRequested and not ready:
        xbmc.sleep(500)
        status = engine.status()
        # Check if there is loading torrent error and raise exception 
        engine.check_torrent_error(status)
        # Trying to detect file_id
        if file_id is None:
            # Get torrent files list, filtered by video file type only
            files = engine.list(media_types=[MediaType.VIDEO])
            # If torrent metadata is not loaded yet then continue
            if files is None:
                continue
            # Torrent has no video files
            if not files:
                break
                progressBar.close()
            # Select first matching file                    
            file_id = files[0].index
            file_status = files[0]
        else:
            # If we've got file_id already, get file status
            file_status = engine.file_status(file_id)
            # If torrent metadata is not loaded yet then continue
            if not file_status:
                continue
        if status.state == State.DOWNLOADING:
            # Wait until minimum pre_buffer_bytes downloaded before we resolve URL to XBMC
            if file_status.download >= pre_buffer_bytes:
                ready = True
                break
            print file_status
            progressBar.update(100*file_status.download/pre_buffer_bytes, 'Torrent2Http', xt('Предварительная буферизация: '+str(file_status.download/1024/1024)+" MB"), "")
            
        elif status.state in [State.FINISHED, State.SEEDING]:
            #progressBar.update(0, 'T2Http', 'We have already downloaded file', "")
            # We have already downloaded file
            ready = True
            break
        
        if progressBar.iscanceled():
            progressBar.update(0)
            progressBar.close()
            break
        # Here you can update pre-buffer progress dialog, for example.
        # Note that State.CHECKING also need waiting until fully finished, so it better to use resume_file option
        # for engine to avoid CHECKING state if possible.
        # ...
    progressBar.update(0)
    progressBar.close()
    if ready:
        # Resolve URL to XBMC
        #listitem = xbmcgui.ListItem(path=file_status.url)
        #listitem.SetPath(file_status.url)
        #xbmcplugin.SetResolvedUrl(handle, True, listitem)
        xbmc.Player().play(file_status.url)
        #xbmc.executebuiltin('"PlayMedia('+file_status.url+',isdir,1)"')
        
        # Wait until playing finished or abort requested
        while not xbmc.abortRequested and xbmc.Player().isPlaying():
            xbmc.sleep(500)