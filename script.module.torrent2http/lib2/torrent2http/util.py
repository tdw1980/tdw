import sys
import socket


def can_bind(host, port):
    """
    Checks we can bind to specified host and port

    :param host: Host
    :param port: Port
    :return: True if bind succeed
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.close()
    except socket.error:
        return False
    return True


def find_free_port(host):
    """
    Finds free TCP port that can be used for binding

    :param host: Host
    :return: Free port
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, 0))
        port = s.getsockname()[1]
        s.close()
    except socket.error:
        return False
    return port


def ensure_fs_encoding(string):
    if isinstance(string, str):
        string = string.decode('utf-8')
    return string.encode(sys.getfilesystemencoding() or 'utf-8')
