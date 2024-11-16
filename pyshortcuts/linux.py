#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
import os
import sys
from pathlib import Path
from collections import namedtuple

from .utils import  get_pyexe, get_homedir

DESKTOP_FORM = """[Desktop Entry]
Name={name:s}
Type=Application
Path={workdir:s}
Comment={desc:s}
Terminal={term:s}
Icon={icon:s}
Exec={execstring:s}
"""

def get_desktop():
    "get desktop location"
    homedir = get_homedir()
    desktop = Path(homedir, 'Desktop').resolve().as_posix()

    if sys.platform.startswith('linux'):
        # search for .config/user-dirs.dirs in HOMEDIR
        ud_file = Path(homedir, '.config', 'user-dirs.dirs').resolve().as_posix()
        if Path(ud_file).exists():
            val = desktop
            with open(ud_file, 'r') as fh:
                text = fh.readlines()
            for line in text:
                if 'DESKTOP' in line:
                    line = line.replace('$HOME', homedir)[:-1]
                    _, val = line.split('=')
                    val = val.replace('"', '').replace("'", "")
            desktop = val
    return desktop

def get_startmenu():
    "get start menu location"
    homedir = get_homedir()
    return Path(homedir, '.local', 'share', 'applications').resolve().as_posix()


def get_folders():
    """get user-specific folders

    Returns:
    -------
    Named tuple with fields 'home', 'desktop', 'startmenu'

    Example:
    -------
    >>> from pyshortcuts import get_folders
    >>> folders = get_folders()
    >>> print("Home, Desktop, StartMenu ",
    ...       folders.home, folders.desktop, folders.startmenu)
    """
    UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def make_shortcut(script, name=None, description=None, icon=None, working_dir=None,
                  folder=None, terminal=True, desktop=True,
                  startmenu=True, executable=None, noexe=False):
    """create shortcut

    Arguments:
    ---------
    script      (str) path to script, may include command-line arguments
    name        (str, None) name to display for shortcut [name of script]
    description (str, None) longer description of script [`name`]
    icon        (str, None) path to icon file [python icon]
    working_dir (str, None) directory where to run the script in
    folder      (str, None) subfolder of Desktop for shortcut [None] (See Note 1)
    terminal    (bool) whether to run in a Terminal [True]
    desktop     (bool) whether to add shortcut to Desktop [True]
    startmenu   (bool) whether to add shortcut to Start Menu [True] (See Note 2)
    executable  (str, None) name of executable to use [this Python] (see Note 3)
    noexe       (bool) whether to use no executable (script is entire command) [False]

    Notes:
    ------
    1. `folder` will place shortcut in a subfolder of Desktop and/or Start Menu
    2. Start Menu does not exist for Darwin / MacOSX
    3. executable defaults to the Python executable used to make shortcut.
    """
    from .shortcut import shortcut

    userfolders = get_folders()
    if working_dir is None:
        working_dir = userfolders.home
    scut = shortcut(script, userfolders, name=name, description=description,
                    working_dir=working_dir, folder=folder, icon=icon)

    if noexe:
        full_script =scut.script
        executable = ''
    else:
        full_script =scut.full_script
        if executable is None:
            executable = get_pyexe()
        executable = Path(executable).resolve().as_posix()

        if Path(scut.full_script).resolve() == Path(executable).resolve():
            executable = ''

    execstring=f"{executable:s} {full_script:s} {scut.arguments:s}".strip()

    text = DESKTOP_FORM.format(name=scut.name, desc=scut.description,
                               workdir=scut.working_dir,
                               execstring=execstring,
                               icon=scut.icon,
                               term='true' if terminal else 'false')

    for (create, ofolder) in ((desktop, scut.desktop_dir),
                             (startmenu, scut.startmenu_dir)):
        if create:
            if not Path(ofolder).exists():
                os.makedirs(ofolder)
            dest = Path(ofolder, scut.target).resolve().as_posix()
            with open(dest, 'w') as fout:
                fout.write(text)
            os.chmod(dest, 493) ## = octal 755 / rwxr-xr-x
    return scut
