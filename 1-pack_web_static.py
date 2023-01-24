#!/usr/bin/python3
# python file that archives files in web static folder

import os.path
from datetime import datetime
from fabric.api import local


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
