
class Error(Exception):
    TORRENT_ERROR = 12
    """ Error returned by libtorrent """
    CRASHED = 13
    """ torrent2http client has crashed abnormally """
    UNKNOWN_PLATFORM = 1
    """ Unknown/unsupported platform """
    XBMC_HOME_NOT_DEFINED = 2
    """ XBMC_HOME or KODI_HOME is not set """
    NOEXEC_FILESYSTEM = 3
    """ torrent2http binary is placed on noexec filesystem, so it can't be started """
    REQUEST_ERROR = 5
    """ Error occurred while sending request to torrent2http """
    INVALID_DOWNLOAD_PATH = 6
    """ Dowload path is invalid """
    BIND_ERROR = 7
    """ Bind error can occur on start, if it's impossible to find a port to bind torrent2http to """
    POPEN_ERROR = 8
    """ Can't start torrent2http client, path to binary doesn't exist or can't be executed """
    PROCESS_ERROR = 9
    """ torrent2http client started but exited abnormally, may be conflict in startup options """
    TIMEOUT = 10
    """ torrent2http not answered during specified timeout """
    INVALID_FILE_INDEX = 11
    """ Specified file index is invalid, no file with specified index found in torrent """

    def __init__(self, message, code=0, **kwargs):
        self.message = message
        self.code = code
        self.kwargs = kwargs

    def __str__(self):
        return self.message