from __future__ import absolute_import
from platform import uname
from .error import Error
import sys
import os


class Platform:
    def __init__(self):
        self.arch = self.arch()
        self.system = self.system()

    def __str__(self):
        return "%s/%s" % (self.system, self.arch)

    @staticmethod
    def arch():
        if sys.platform.lower().startswith('linux') and (uname()[4].lower().startswith('arm') or
                                                         uname()[4].lower().startswith('aarch')):
            if uname()[4].lower().startswith('armv6'):
                return "armv6"
            return 'arm'
        elif sys.maxsize > 2**32:
            return 'x64'
        else:
            return 'x86'

    @staticmethod
    def system():
        if sys.platform.startswith('linux'):
            if 'ANDROID_DATA' in os.environ:
                return 'android'
            else:
                return 'linux'
        elif sys.platform.startswith('win'):
            return 'windows'
        elif sys.platform.startswith('darwin'):
            return 'darwin'
        else:
            raise Error("Platform %s is unknown" % sys.platform, Error.UNKNOWN_PLATFORM,
                        platform=sys.platform)
