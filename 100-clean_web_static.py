#!/usr/bin/python3
# fabric script that deletes out-of-date archives

import os
from fabric.api import *


env.hosts = ["52.91.132.254", "100.25.203.14"]


def do_clean(number=0):
    """
    python function that implements fabric to remove
    any out-of-date files in a directory.

    """

    num = 1 if int(number) == 0 else int(number)
    archive_files = sorted(os.listdir("versions"))
    [archive_files.pop() for a in range(num)]

    with lcd("versions"):
        [local("rm ./{}".format(files)) for files in archive_files]
    with cd("/etc/web_static/releases"):
        archive_files = run("ls -tr").split()
        archive_files = [files for files in archive_files
                         if "web_static_" in files]
        [archive_files.pop() for i in range(number)]
        [run("rm -rf ./{}".format(files)) for files in archive_files]
