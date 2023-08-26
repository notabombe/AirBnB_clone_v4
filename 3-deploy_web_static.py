#!/usr/bin/python3
"""
    Fabric script that creates and distributes an archive
    on my web servers, using deploy function
"""
from fabric.api import *
from fabric.operations import run, put, sudo, local
from datetime import datetime
import os

env.hosts = ['66.70.184.249', '54.210.138.75']
created_path = None


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


def do_deploy(archive_path):
    """
        using fabric to distribute archive
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        put(f"{archive_path}", f"/tmp/{archive}")
        folder = archive.split(".")
        run(f"mkdir -p {path}/{folder[0]}/")
        new_archive = '.'.join(folder)
        run(f"tar -xzf /tmp/{new_archive} -C {path}/{folder[0]}/")
        run(f"rm /tmp/{archive}")
        run(f"mv {path}/{folder[0]}/web_static/* {path}/{folder[0]}/")
        run(f"rm -rf {path}/{folder[0]}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -sf {path}/{folder[0]} /data/web_static/current")
        return True
    except:
        return False


def deploy():
    """
        deploy function that creates/distributes an archive
    """
    global created_path
    if created_path is None:
        created_path = do_pack()
    return False if created_path is None else do_deploy(created_path)
