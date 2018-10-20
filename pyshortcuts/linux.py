#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
from __future__ import print_function
import os
import sys

from .shortcut import Shortcut

def make_shortcut(script, name=None, description=None, terminal=True,
                  folder=None, icon=None):
    """create linux .desktop file

    Arguments
    ---------
    script      (str)  path to script to run.  This can include  command-line arguments
    name        (str or None) name to use for shortcut [defaults to script name]
    description (str or None) longer description of script [defaults to `name`]
    icon        (str or None) path to icon file [defaults to python icon]
    folder      (str or None) folder on Desktop to put shortcut [defaults to Desktop]
    terminal    (True or False) whether to run in a Terminal  [True]
    """
    if description is None:
        description = name

    scut = Shortcut(script, name=name, description=description, folder=folder, icon=icon)

    term = 'false'
    if terminal:
        term = 'true'

    with open(scut.target, 'w') as fout:
        fout.write("""[Desktop Entry]
Name={name:s}
Type=Application
Comment={desc:s}
Terminal={term:s}
Icon={icon:s}
Exec={exe:s} {script:s} {args:s}
""".format(name=scut.name, desc=description, exe=sys.executable,
           icon=scut.icon, script=scut.full_script, args=scut.args,
           term=term))


