# -*- coding: utf-8 -*-
import json
import os
import socket
import stat
import subprocess
import sys
import time
import urllib2
import httplib
from os.path import dirname
from download import LibraryManager

import logpipe
import mimetypes
import xbmc
from error import Error
from platform import Platform
from . import SessionStatus, FileStatus, PeerInfo, MediaType, Encryption
from util import can_bind, find_free_port, ensure_fs_encoding


class Engine:
    """
    This is python binding class to torrent2http client.
    """
    SUBTITLES_FORMATS = ['.aqt', '.gsub', '.jss', '.sub', '.ttxt', '.pjs', '.psb', '.rt', '.smi', '.stl',
                         '.ssf', '.srt', '.ssa', '.ass', '.usf', '.idx']

    def _ensure_binary_executable(self, path):
        st = os.stat(path)
        if not st.st_mode & stat.S_IEXEC:
            try:
                self._log("%s is not executable, trying to change its mode..." % path)
                os.chmod(path, st.st_mode | stat.S_IEXEC)
            except Exception, e:
                self._log("Failed! Exception: %s" % str(e))
                return False
            st = os.stat(path)
            if st.st_mode & stat.S_IEXEC:
                self._log("Succeeded")
                return True
            else:
                self._log("Failed")
                return False
        return True
    
    def _log(self, message):
        if self.logger:
            self.logger(message)
        else:
            xbmc.log("[torrent2http] %s" % message)

    def _get_binary_path(self, binaries_path):
        """
        Detects platform and returns corresponding torrent2http binary path

        :param binaries_path:
        :return: torrent2http binary path
        """
        binary = "torrent2http" + (".exe" if self.platform.system == 'windows' else "")
        binary_dir = os.path.join(binaries_path, "%s_%s" % (self.platform.system, self.platform.arch))
        binary_path = os.path.join(binary_dir, binary)
        lm=LibraryManager(binary_dir, "%s_%s" % (self.platform.system, self.platform.arch))
        if not os.path.isfile(binary_path):
            success=lm.download()
            if not success:
                raise Error("Can't find torrent2http or download binary for %s" % self.platform,
                            Error.UNKNOWN_PLATFORM, platform=str(self.platform))
        #This is needed only if bin in folder that not deletes on update!
        #else: lm.update()

        if not self._ensure_binary_executable(binary_path):
            if self.platform.system == "android":
                self._log("Trying to copy torrent2http to ext4, since the sdcard is noexec...")
                xbmc_home = os.environ.get('XBMC_HOME') or os.environ.get('KODI_HOME')
                if not xbmc_home:
                    raise Error("Suppose we are running XBMC, but environment variable "
                                "XBMC_HOME or KODI_HOME is not found", Error.XBMC_HOME_NOT_DEFINED)
                base_xbmc_path = dirname(dirname(dirname(xbmc_home)))
                android_binary_dir = os.path.join(base_xbmc_path, "files")
                if not os.path.exists(android_binary_dir):
                    os.makedirs(android_binary_dir)
                android_binary_path = os.path.join(android_binary_dir, binary)
                if not os.path.exists(android_binary_path) or \
                        int(os.path.getmtime(android_binary_path)) < int(os.path.getmtime(binary_path)):
                    import shutil
                    shutil.copy2(binary_path, android_binary_path)
                    if not self._ensure_binary_executable(android_binary_path):
                        raise Error("Can't make %s executable" % android_binary_path, Error.NOEXEC_FILESYSTEM)
                binary_path = android_binary_path
            else:
                raise Error("Can't make %s executable, ensure it's placed on exec partition and "
                            "partition is in read/write mode" % binary_path, Error.NOEXEC_FILESYSTEM)
        self._log("Selected %s as torrent2http binary" % binary_path)
        return binary_path

    def __init__(self, uri=None, binaries_path=None, platform=None, download_path=".",
                 bind_host='127.0.0.1', bind_port=5001, connections_limit=None, download_kbps=None, upload_kbps=None,
                 enable_dht=True, enable_lsd=True, enable_natpmp=True, enable_upnp=True, enable_scrape=False,
                 log_stats=False, encryption=Encryption.ENABLED, keep_complete=False, keep_incomplete=False,
                 keep_files=False, log_files_progress=False, log_overall_progress=False, log_pieces_progress=False,
                 listen_port=6881, use_random_port=False, max_idle_timeout=None, no_sparse=False, resume_file=None,
                 user_agent=None, startup_timeout=5, state_file=None, enable_utp=True, enable_tcp=True,
                 debug_alerts=False, logger=None, torrent_connect_boost=50, connection_speed=50,
                 peer_connect_timeout=15, request_timeout=20, min_reconnect_time=60, max_failcount=3,
                 dht_routers=None, trackers=None):
        """
        Creates engine instance. It doesn't do anything except initializing object members. For starting engine use
        start() method.

        :param uri: Torrent URI (magnet://, file:// or http://)
        :param binaries_path: Path to torrent2http binaries
        :param platform: Object with two methods implemented: arch() and system()
        :param download_path: Torrent download path
        :param bind_host: Bind host of torrent2http
        :param bind_port: Bind port of torrent2http
        :param connections_limit: Set a global limit on the number of connections opened
        :param download_kbps: Max download rate (kB/s)
        :param upload_kbps: Max upload rate (kB/s)
        :param enable_dht: Enable DHT (Distributed Hash Table)
        :param enable_lsd: Enable LSD (Local Service Discovery)
        :param enable_natpmp: Enable NATPMP (NAT port-mapping)
        :param enable_upnp: Enable UPnP (UPnP port-mapping)
        :param enable_scrape: Enable sending scrape request to tracker (updates total peers/seeds count)
        :param log_stats: Log all stats (incl. log_overall_progress, log_files_progress, log_pieces_progress)
        :param encryption: Encryption: 0=forced 1=enabled (default) 2=disabled
        :param keep_complete: Keep complete files after exiting
        :param keep_incomplete: Keep incomplete files after exiting
        :param keep_files: Keep all files after exiting (incl. keep_complete and keep_incomplete)
        :param log_files_progress: Log files progress
        :param log_overall_progress: Log overall progress
        :param log_pieces_progress: Log pieces progress
        :param listen_port: Use specified port for incoming connections
        :param use_random_port: Use random listen port (49152-65535)
        :param max_idle_timeout: Automatically shutdown torrent2http if no connection are active after a timeout
        :param no_sparse: Do not use sparse file allocation
        :param resume_file: Use fast resume file
        :param user_agent: Set an user agent
        :param startup_timeout: torrent2http startup timeout
        :param state_file: Use file for saving/restoring session state
        :param enable_utp: Enable uTP protocol
        :param enable_tcp: Enable TCP protocol
        :param debug_alerts: Show debug alert notifications
        :param logger: Instance of logging.Logger
        :param torrent_connect_boost: The number of peers to try to connect to immediately when the first tracker
            response is received for a torrent
        :param connection_speed: The number of peer connection attempts that are made per second
        :param peer_connect_timeout: The number of seconds to wait after a connection attempt is initiated to a peer
        :param request_timeout: The number of seconds until the current front piece request will time out
        :param min_reconnect_time: The time to wait between peer connection attempts. If the peer fails, the time is
            multiplied by fail counter
        :param max_failcount: The maximum times we try to connect to a peer before stop connecting again
        :param dht_routers: List of additional DHT routers (host:port pairs)
        :param trackers: List of additional tracker URLs
        """
        self.dht_routers = dht_routers or []
        self.trackers = trackers or []
        self.max_failcount = max_failcount
        self.min_reconnect_time = min_reconnect_time
        self.request_timeout = request_timeout
        self.peer_connect_timeout = peer_connect_timeout
        self.connection_speed = connection_speed
        self.torrent_connect_boost = torrent_connect_boost
        self.platform = platform
        self.bind_host = bind_host
        self.bind_port = bind_port
        self.binaries_path = binaries_path or os.path.join(dirname(dirname(dirname(os.path.abspath(__file__)))), 'bin')
        self.download_path = download_path
        self.connections_limit = connections_limit
        self.download_kbps = download_kbps
        self.upload_kbps = upload_kbps
        self.enable_dht = enable_dht
        self.enable_lsd = enable_lsd
        self.enable_natpmp = enable_natpmp
        self.enable_upnp = enable_upnp
        self.enable_scrape = enable_scrape
        self.log_stats = log_stats
        self.encryption = encryption
        self.keep_complete = keep_complete
        self.keep_incomplete = keep_incomplete
        self.keep_files = keep_files
        self.log_files_progress = log_files_progress
        self.log_overall_progress = log_overall_progress
        self.log_pieces_progress = log_pieces_progress
        self.listen_port = listen_port
        self.use_random_port = use_random_port
        self.max_idle_timeout = max_idle_timeout
        self.no_sparse = no_sparse
        self.resume_file = resume_file
        self.user_agent = user_agent
        self.startup_timeout = startup_timeout
        self.state_file = state_file
        self.wait_on_close_timeout = None
        self.enable_utp = enable_utp
        self.enable_tcp = enable_tcp
        self.debug_alerts = debug_alerts
        self.logger = logger
        self.uri = uri
        self.logpipe = None
        self.process = None
        self.started = False

    @staticmethod
    def _validate_save_path(path):
        """
        Ensures download path can be accessed locally.

        :param path: Download path
        :return: Translated path
        """
        import xbmc
        path = xbmc.translatePath(path)
        if "://" in path:
            if sys.platform.startswith('win') and path.lower().startswith("smb://"):
                path = path.replace("smb:", "").replace("/", "\\")
            else:
                raise Error("Downloading to an unmounted network share is not supported", Error.INVALID_DOWNLOAD_PATH)
        if not os.path.isdir(ensure_fs_encoding(path)):
            raise Error("Download path doesn't exist (%s)" % path, Error.INVALID_DOWNLOAD_PATH)
        return path

    def start(self, start_index=None):
        """
        Starts torrent2http client with specified settings. If it can be started in startup_timeout seconds, exception
        will be raised.

        :param start_index: File index to start download instantly, if not specified, downloading will be paused, until
            any file requested
        """
        self.platform = self.platform or Platform()
        binary_path = self._get_binary_path(self.binaries_path)
        download_path = self._validate_save_path(self.download_path)
        if not can_bind(self.bind_host, self.bind_port):
            port = find_free_port(self.bind_host)
            if port is False:
                raise Error("Can't find port to bind torrent2http", Error.BIND_ERROR)
            self._log("Can't bind to %s:%s, so we found another port: %d" % (self.bind_host, self.bind_port, port))
            self.bind_port = port

        kwargs = {
            '--bind': "%s:%s" % (self.bind_host, self.bind_port),
            '--uri': self.uri,
            '--file-index': start_index,
            '--dl-path': download_path,
            '--connections-limit': self.connections_limit,
            '--dl-rate': self.download_kbps,
            '--ul-rate': self.upload_kbps,
            '--enable-dht': self.enable_dht,
            '--enable-lsd': self.enable_lsd,
            '--enable-natpmp': self.enable_natpmp,
            '--enable-upnp': self.enable_upnp,
            '--enable-scrape': self.enable_scrape,
            '--encryption': self.encryption,
            '--show-stats': self.log_stats,
            '--files-progress': self.log_files_progress,
            '--overall-progress': self.log_overall_progress,
            '--pieces-progress': self.log_pieces_progress,
            '--listen-port': self.listen_port,
            '--random-port': self.use_random_port,
            '--keep-complete': self.keep_complete,
            '--keep-incomplete': self.keep_incomplete,
            '--keep-files': self.keep_files,
            '--max-idle': self.max_idle_timeout,
            '--no-sparse': self.no_sparse,
            '--resume-file': self.resume_file,
            '--user-agent': self.user_agent,
            '--state-file': self.state_file,
            '--enable-utp': self.enable_utp,
            '--enable-tcp': self.enable_tcp,
            '--debug-alerts': self.debug_alerts,
            '--torrent-connect-boost': self.torrent_connect_boost,
            '--connection-speed': self.connection_speed,
            '--peer-connect-timeout': self.peer_connect_timeout,
            '--request-timeout': self.request_timeout,
            '--min-reconnect-time': self.min_reconnect_time,
            '--max-failcount': self.max_failcount,
            '--dht-routers': ",".join(self.dht_routers),
            '--trackers': ",".join(self.trackers),
        }

        args = [binary_path]
        for k, v in kwargs.iteritems():
            if v is not None:
                if isinstance(v, bool):
                    if v:
                        args.append(k)
                    else:
                        args.append("%s=false" % k)
                else:
                    args.append(k)
                    if isinstance(v, str) or isinstance(v, unicode):
                        v = ensure_fs_encoding(v)
                    else:
                        v = str(v)
                    args.append(v)

        self._log("Invoking %s" % " ".join(args))
        startupinfo = None
        if self.platform.system == "windows":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= 1
            startupinfo.wShowWindow = 0

        self.logpipe = logpipe.LogPipe(self._log)
        try:
            self.process = subprocess.Popen(args, stderr=self.logpipe, stdout=self.logpipe, startupinfo=startupinfo)
        except OSError, e:
            raise Error("Can't start torrent2http: %r" % e, Error.POPEN_ERROR)

        start = time.time()
        self.started = True
        initialized = False
        while (time.time() - start) < self.startup_timeout:
            time.sleep(0.1)
            if not self.is_alive():
                raise Error("Can't start torrent2http, see log for details", Error.PROCESS_ERROR)
            try:
                self.status(1)
                initialized = True
                break
            except Error:
                pass

        if not initialized:
            self.started = False
            raise Error("Can't start torrent2http, time is out", Error.TIMEOUT)
        self._log("torrent2http successfully started.")

    def check_torrent_error(self, status=None):
        """
        It is recommended to call this method periodically to check if any libtorrent errors occurred.
        Usually libtorrent sets error if it can't download or parse torrent file by specified URI.
        Note that torrent2http remains started after such error, so you need to shutdown it manually.

        :param status: Pass return of status() method if you don't want status() called twice
        """
        if not status:
            status = self.status()
        if status.error:
            raise Error("Torrent error: %s" % status.error, Error.TORRENT_ERROR, reason=status.error)

    def status(self, timeout=10):
        """
        Returns libtorrent session status. See SessionStatus named tuple.

        :rtype : SessionStatus
        :param timeout: torrent2http client request timeout
        """
        status = self._decode(self._request('status', timeout))
        status = SessionStatus(**status)
        return status

    def _detect_media_type(self, name):
        ext = os.path.splitext(name)[1]
        if ext in self.SUBTITLES_FORMATS:
            return MediaType.SUBTITLES
        else:
            mime_type = mimetypes.guess_type(name)[0]
            if not mime_type:
                return MediaType.UNKNOWN
            mime_type = mime_type.split("/")[0]
            if mime_type == 'audio':
                return MediaType.AUDIO
            elif mime_type == 'video':
                return MediaType.VIDEO
            else:
                return MediaType.UNKNOWN

    def list(self, media_types=None, timeout=10):
        """
        Returns list of files in the torrent (see FileStatus named tuple).
        Note that it will return None if torrent file is not loaded yet by torrent2http client, so you may need to call
        this method periodically until results are returned.

        :param media_types: List of media types (see MediaType constants)
        :param timeout: torrent2http client request timeout
        :rtype : list of FileStatus
        :return: List of files of specified media types or None if torrent is not loaded yet
        """
        files = self._decode(self._request('ls', timeout))['files']
        if files:
            res = [FileStatus(index=index, media_type=self._detect_media_type(f['name']), **f)
                   for index, f in enumerate(files)]
            if media_types is not None:
                res = filter(lambda fs: fs.media_type in media_types, res)
            return res

    def file_status(self, file_index, timeout=10):
        """
        Returns file in the torrent with specified index (see FileStatus named tuple)
        Note that it will return None if torrent file is not loaded yet by torrent2http client, so you may need to call
        this method periodically until results are returned.

        :param file_index: Requested file's index
        :param timeout: torrent2http client request timeout
        :return: File with specified index
        :rtype: FileStatus
        """
        res = self.list(timeout=timeout)
        if res:
            try:
                return next((f for f in res if f.index == file_index))
            except StopIteration:
                raise Error("Requested file index (%d) is invalid" % file_index, Error.INVALID_FILE_INDEX,
                            file_index=file_index)

    def peers(self, timeout=10):
        """
        Returns list of peers connected (see PeerInfo named tuple).

        :param timeout: torrent2http client request timeout
        :return: List of peers
        :rtype: list of PeerInfo
        """
        peers = self._decode(self._request('peers', timeout))['peers']
        if peers:
            return [PeerInfo(**p) for p in peers]

    def is_alive(self):
        return self.process and self.process.poll() is None

    @staticmethod
    def _decode(response):
        try:
            return json.loads(response)
        except (KeyError, ValueError), e:
            raise Error("Can't decode response from torrent2http: %r" % e, Error.REQUEST_ERROR)

    def _request(self, cmd, timeout=None):
        if not self.started:
            raise Error("torrent2http is not started", Error.REQUEST_ERROR)
        try:
            url = "http://%s:%s/%s" % (self.bind_host, self.bind_port, cmd)
            kwargs = {}
            if timeout is not None:
                kwargs['timeout'] = timeout
            return urllib2.urlopen(url, **kwargs).read()
        except (urllib2.URLError, httplib.HTTPException) as e:
            if isinstance(e, urllib2.URLError) and isinstance(e.reason, socket.timeout):
                raise Error("Timeout occurred while sending command '%s' to torrent2http" % cmd, Error.TIMEOUT)
            elif not self.is_alive() and self.started:
                raise Error("torrent2http has crashed.", Error.CRASHED)
            else:
                raise Error("Can't send command '%s' to torrent2http: %r" % (cmd, e), Error.REQUEST_ERROR)
        except socket.error as e:
            reason = e[1] if isinstance(e, tuple) else e
            raise Error("Can't read from torrent2http: %s" % reason, Error.REQUEST_ERROR)

    def wait_on_close(self, wait_timeout=10):
        """
        By default, close() method sends shutdown command to torrent2http, stops logging and returns immediately, not
        waiting while torrent2http exits. It can be handy to wait torrent2http to view log messages during shutdown.
        So call this method with reasonable timeout before calling close().

        :param wait_timeout: Time in seconds to wait until torrent2http client shut down
        """
        self.wait_on_close_timeout = wait_timeout

    def close(self):
        """
        Shuts down torrent2http and stops logging. If wait_on_close() was called earlier, it will wait until
        torrent2http successfully exits.
        """
        if self.logpipe and self.wait_on_close_timeout is None:
            self.logpipe.close()
        if self.is_alive():
            self._log("Shutting down torrent2http...")
            self._request('shutdown')
            finished = False
            if self.wait_on_close_timeout is not None:
                start = time.time()
                os.close(self.logpipe.write_fd)
                while (time.time() - start) < self.wait_on_close_timeout:
                    time.sleep(0.5)
                    if not self.is_alive():
                        finished = True
                        break
                if not finished:
                    self._log("Timeout occurred while shutting down torrent2http, killing it")
                    self.process.kill()
                else:
                    self._log("torrent2http successfully shut down.")
                self.wait_on_close_timeout = None
            self.process.wait()
        self.started = False
        self.logpipe = None
        self.process = None
