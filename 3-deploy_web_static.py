#!/usr/bin/python3
# python file that archives files in web static folder

import os.path
from datetime import datetime
from fabric.api import local
from fabric.api import env
from fabric.api import run
from fabric.api import put


def do_pack():
    """python function that implements archives files
    in a directory using the fabric api"""

    date = datetime.utcnow()
    tarFile = "versions/web_static_{}{}{}{}{}{}.tgz".format(
                                                          date.year,
                                                          date.month,
                                                          date.day,
                                                          date.hour,
                                                          date.minute,
                                                          date.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(tarFile)).failed is True:
        return None
    return tarFile


env.hosts = ["52.91.132.254", "100.25.203.14"]


def do_deploy(archive_path):
    """function that uploads an archive file to a web server"""

    if os.path.isfile(archive_path) is False:
        return False
    fpath = archive_path.split("/")[-1]
    fname = fpath.split(".")[0]

    if put(archive_path, "/tmp/{}".format(fpath)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".format(
           fname)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".format(
           fname)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
           fpath, fname)).failed is True:
        return False
    if run("rm /tmp/{}".format(fpath)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(fname, fname)
           ).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static"
           .format(fname)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(fname)).failed is True:
        return False
    return True


def deploy():
    """function that deploys web_static using python functions"""

    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
