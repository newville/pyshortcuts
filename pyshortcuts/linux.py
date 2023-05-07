#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
import os
import sys

HAS_PWD = False
try:
    import pwd
    HAS_PWD = True
except ImportError:
    pass

from .shortcut import shortcut, get_pyexe
from . import UserFolders

scut_ext = 'desktop'
ico_ext = ('ico', 'svg', 'png')

DESKTOP_FORM = """[Desktop Entry]
Name={name:s}
Type=Application
Path={workdir:s}
Comment={desc:s}
Terminal={term:s}
Icon={icon:s}
Exec={execstring:s}
"""

_HOME = None
def get_homedir():
    "determine home directory of current user"
    global _HOME
    if _HOME is None:
        home = None
        susername = os.environ.get("SUDO_USER", None)
        if susername is not None:
            try:
                from pwd import getpwnam
                home = getpwnam(susername).pw_dir
            except ImportError:
                pass
        if home is None:
            try:
                from pathlib import Path
                home = str(Path.home())
            except:
                pass
        if home is None:
            home = os.path.expanduser("~")
        if home is None:
            home = os.environ.get("HOME", os.path.abspath("."))
        _HOME = os.path.normpath(home)
    return _HOME

def get_desktop():
    "get desktop location"
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
    return desktop

def get_startmenu():
    "get start menu location"
    homedir = get_homedir()
    return os.path.join(homedir, '.local', 'share', 'applications')

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
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def make_shortcut(script, name=None, description=None, icon=None, working_dir=None,
                  folder=None, terminal=True, desktop=True,
                  startmenu=True, executable=None):
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

    Notes:
    ------
    1. `folder` will place shortcut in a subfolder of Desktop and/or Start Menu
    2. Start Menu does not exist for Darwin / MacOSX
    3. executable defaults to the Python executable used to make shortcut.
    """
    userfolders = get_folders()
    if working_dir is None:
        working_dir = userfolders.home
    scut = shortcut(script, userfolders, name=name, description=description,
                    working_dir=working_dir, folder=folder, icon=icon)

    if executable is None:
        executable = get_pyexe()

    executable = os.path.normpath(executable)
    if os.path.realpath(scut.full_script) == os.path.realpath(executable):
        executable = ''

    execstring=f"{executable:s} {scut.full_script:s} {scut.arguments:s}".strip()

    text = DESKTOP_FORM.format(name=scut.name, desc=scut.description,
                               workdir=scut.working_dir,
                               execstring=execstring,
                               icon=scut.icon,
                               term='true' if terminal else 'false')

    for (create, folder) in ((desktop, scut.desktop_dir),
                             (startmenu, scut.startmenu_dir)):
        if create:
            if not os.path.exists(folder):
                os.makedirs(folder)
            dest = os.path.join(folder, scut.target)
            with open(dest, 'w') as fout:
                fout.write(text)
            os.chmod(dest, 493) ## = octal 755 / rwxr-xr-x
    return scut
