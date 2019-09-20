#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
from __future__ import print_function
import os
import sys
from collections import namedtuple


from .shortcut import Shortcut
from .utils import get_homedir

DESKTOP_FORM = """[Desktop Entry]
Name={name:s}
Type=Application
Comment={desc:s}
Terminal={term:s}
Icon={icon:s}
Exec={exe:s} {script:s} {args:s}
"""

def get_folders():
    """Return named tuple of Home, Desktop and Startmenu paths.

        folders = get_folders()
        print("Home, Desktop, StartMenu ",
            folders.home, folders.desktop, folders.startmenu)
    """
    homedir = get_homedir()
    desktop = os.path.join(homedir, 'Desktop')

    # search for .config/user-dirs.dirs in HOMEDIR
    ud_file = os.path.join(homedir, '.config', 'user-dirs.dirs')
    if os.path.exists(ud_file):
        val = desktop
        with open(ud_file, 'r') as fh:
            text = fh.readlines()
        for line in text:
            if 'DESKTOP' in line:
                line = line.replace('$HOME', homedir)[:-1]
                key, val = line.split('=')
                val = val.replace('"', '').replace("'", "")
        desktop = val

    nt = namedtuple("folders", "home desktop startmenu")
    folders = nt(
        homedir,
        desktop,
        None
    )
    return folders


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

    scut = Shortcut(script, name=name, description=description, folder=folder, icon=icon)

    term = 'false'
    if terminal:
        term = 'true'

    text = DESKTOP_FORM.format(name=scut.name, desc=scut.description,
                               exe=sys.executable, icon=scut.icon,
                               script=scut.full_script, args=scut.args,
                               term=term)
    # Desktop
    desktop = os.path.join(get_homedir(), 'Desktop') # todo: use folders.desktop
    if os.path.exists(desktop):
        with open(scut.target, 'w') as fout:
            fout.write(text)

    # Local Applications
    appfolder = os.path.join(get_homedir(), '.local', 'share', 'applications')
    if os.path.exists(appfolder):
        _, target = os.path.split(scut.target)
        apptarget = os.path.join(appfolder, target)
        with open(apptarget, 'w') as fout:
            fout.write(text)

    return scut
