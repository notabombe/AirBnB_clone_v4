#!/usr/bin/python3
"""
    Fabric script that generates tgz archive from contents of web_static
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
        generates a .tgz archine from contents of web_static
    """
    time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    file_name = f"versions/web_static_{time}.tgz"
    try:
        local("mkdir -p ./versions")
        local(f"tar --create --verbose -z --file={file_name} ./web_static")
        return file_name
    except:
        return None
