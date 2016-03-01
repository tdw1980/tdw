# -*- coding: utf-8 -*-

from collections import namedtuple


# noinspection PyClassHasNoInit
class State:
    QUEUED_FOR_CHECKING = 0
    CHECKING_FILES = 1
    DOWNLOADING_METADATA = 2
    DOWNLOADING = 3
    FINISHED = 4
    SEEDING = 5
    ALLOCATING = 6
    CHECKING_RESUME_DATA = 7


# noinspection PyClassHasNoInit
class MediaType:
    UNKNOWN = None
    AUDIO = 'audio'
    VIDEO = 'video'
    SUBTITLES = 'subtitles'


# noinspection PyClassHasNoInit
class Encryption:
    FORCED = 0
    ENABLED = 1
    DISABLED = 2


SessionStatus = namedtuple('SessionStatus', "name, state, state_str, error, progress, download_rate, upload_rate, "
                                            "total_download, total_upload, num_peers, num_seeds, total_seeds, "
                                            "total_peers")

FileStatus = namedtuple('FileStatus', "name, save_path, url, size, offset, download, progress, index, media_type")

PeerInfo = namedtuple('PeerInfo', "ip, flags, source, up_speed, down_speed, total_upload, total_download, "
                                  "country, client")

from engine import Engine
from platform import Platform
from error import Error
