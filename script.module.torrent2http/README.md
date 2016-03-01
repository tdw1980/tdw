script.module.torrent2http
==========================

This add-on is binding to [torrent2http](https://github.com/anteo/torrent2http) client. 
It is bundled with torrent2http binaries for Android ARM, Linux x86/x64/ARM, Windows x86/x64 and Darwin/OSX x64 platforms.
You can download it from my [repository](http://bit.ly/184XKjm)

This add-on can be used to stream media files from torrents without need to download entire files.

Internally, it runs pre-compiled torrent2http client binary, which starts local HTTP server, presenting contents of torrent.
Next, request to HTTP server can be sent to receive list of files or to start streaming of needed file inside of torrent.

Usage
-----

### Get list of files inside torrent ###

Getting list of files inside torrent is straightforward:

```python
import xbmc 
from torrent2http import State, Engine, MediaType
from contextlib import closing

# Create instance of Engine 
engine = Engine(uri="...")
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
```

### Start streaming ###

```python
import xbmc 
from torrent2http import State, Engine, MediaType
from contextlib import closing

# XBMC addon handle
handle = ...
# Playable list item
listitem = ...
# We can know file_id of needed video file on this step, if no, we'll try to detect one.
file_id = None
# Flag will set to True when engine is ready to resolve URL to XBMC
ready = False
# Set pre-buffer size to 15Mb. This is a size of file that need to be downloaded before we resolve URL to XMBC 
pre_buffer_bytes = 15*1024*1024
engine = Engine(uri="...")
with closing(engine):
    # Start engine and instruct torrent2http to begin download first file, 
    # so it can start searching and connecting to peers  
    engine.start(file_id or 0)
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
        elif status.state in [State.FINISHED, State.SEEDING]:
            # We have already downloaded file
            ready = True
            break
        # Here you can update pre-buffer progress dialog, for example.
        # Note that State.CHECKING also need waiting until fully finished, so it better to use resume_file option
        # for engine to avoid CHECKING state if possible.
        # ...
    if ready:
        # Resolve URL to XBMC
        listitem.SetPath(file_status.url)
        xbmcplugin.SetResolvedUrl(handle, True, listitem)
        # Wait until playing finished or abort requested
        while not xbmc.abortRequested and xbmc.Player().isPlaying():
            xbmc.sleep(500)
```
        
### Fully working example ###

You can look into fully working [example](https://github.com/anteo/plugin.video.okino/blob/master/resources/lib/okino/torrent/stream/t2h_stream.py). This is
excerpt from my plugin using script.module.torrent2http. It rather complicated but it includes error handling, showing progress dialog and other features.
