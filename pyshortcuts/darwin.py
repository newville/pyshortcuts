#!/usr/bin/env python
"""
Create desktop shortcuts for Darwin / MacOS
"""
import os
import sys
import shutil

from .shortcut import shortcut, get_pyexe
from .linux import get_homedir, get_desktop
from . import UserFolders

scut_ext = 'app'
ico_ext = ('icns',)


def get_startmenu():
    "get start menu location"
    return ''


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
    if not desktop:
        return

    userfolders = get_folders()
    if working_dir is None:
        working_dir = ''

    scut = shortcut(script, userfolders, name=name, description=description,
                    working_dir=working_dir, folder=folder, icon=icon)

    osascript = '%s %s' % (scut.full_script, scut.arguments)
    osascript = osascript.replace(' ', '\\ ')
    prefix = os.path.normpath(sys.prefix)
    if executable is None:
        executable = get_pyexe()

    executable = os.path.normpath(executable)
    if os.path.realpath(scut.full_script) == os.path.realpath(executable):
        executable = ''

    if not os.path.exists(scut.desktop_dir):
        os.makedirs(scut.desktop_dir)

    dest = os.path.join(scut.desktop_dir, scut.target)

    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.mkdir(dest)
    os.mkdir(os.path.join(dest, 'Contents'))
    os.mkdir(os.path.join(dest, 'Contents', 'MacOS'))
    os.mkdir(os.path.join(dest, 'Contents', 'Resources'))

    opts = dict(name=scut.name,
                desc=scut.description,
                script=scut.full_script,
                workdir=scut.working_dir,
                args=scut.arguments,
                prefix=prefix,
                exe=executable,
                osascript=osascript)

    info = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
  <key>CFBundleGetInfoString</key> <string>{desc:s}</string>
  <key>CFBundleName</key> <string>{name:s}</string>
  <key>CFBundleExecutable</key> <string>{name:s}</string>
  <key>CFBundleIconFile</key> <string>{name:s}</string>
  <key>CFBundlePackageType</key> <string>APPL</string>
  </dict>
</plist>
"""

    text = ['#!/bin/bash',
            "export EXE={exe:s}",
            "export SCRIPT={script:s}",
            "export ARGS='{args:s}'"]

    if scut.working_dir not in (None, ''):
        text.append("cd {workdir:s}")

    if terminal:
        text.append("""osascript -e 'tell application "Terminal"
   do script "'${{EXE}}\ {osascript:s}'"
end tell
'
""")
    else:
        text.append("$EXE $SCRIPT $ARGS")

    text.append('\n')
    text = '\n'.join(text)

    with open(os.path.join(dest, 'Contents', 'Info.plist'), 'w') as fout:
        fout.write(info.format(**opts))

    ascript_name = os.path.join(dest, 'Contents', 'MacOS', scut.name)
    with open(ascript_name, 'w') as fout:
        fout.write(text.format(**opts))

    os.chmod(ascript_name, 493)  # = octal 755 / rwxr-xr-x
    icon_dest = os.path.join(dest, 'Contents', 'Resources', scut.name + '.icns')
    shutil.copy(scut.icon, icon_dest)
    return scut
