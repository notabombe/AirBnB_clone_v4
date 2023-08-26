#!/usr/bin/python3
"""
    Fabric script that distributes an archive to my web servers
"""
from fabric.api import *
from fabric.operations import run, put, sudo
import os
env.hosts = ['66.70.184.249', '54.210.138.75']


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
