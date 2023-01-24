#!/usr/bin/python3
# fabric script that uploads an archived file to a remote server

import os.path
from fabric.api import env
from fabric.api import run
from fabric.api import put

env.hosts = ["52.91.132.254", "100.25.203.14"]

def do_deploy(archive_path):
    """function that uploads an archive file to a web server"""

    if os.path.isfile("archive_path") is False:
        return False
    fpath = archive_path.split("/")[-1]
    fname = fpath.split(".")[0]

    if put(archive_path, "/tmp/fpath").failed is True:
        return False
    if run("rm -rf /data/web_static/releases/fname").failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/fname").failed is True:
        return False
    if run("tar -xzf /tmp/fpath -C /data/web_static/releases/fname").failed is True:
        return False
    if run("rm -rf /tmp/fpath").failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/fname /data/web_static/current").failed is True:
        return False
    return True
