#!/usr/bin/env python
"""
utilities for pyshortcuts
  get_homedir()  get home directory
  get_paths()

"""
import os
import sys


platform = sys.platform
if os.name == 'nt':
    platform = 'win'


def unixpath(d):
    "unix path"
    return d.replace('\\', '/')

def winpath(d):
    "ensure path uses windows delimiters"
    if d.startswith('//'):
        d = d[1:]
    d = d.replace('/', '\\')
    return d

nativepath = unixpath
if platform == 'win':
    nativepath = winpath

HAS_PWD = True
try:
    import pwd
except ImportError:
    HAS_PWD = False

def get_homedir():
    "determine home directory of current user"
    home = None
    def check(method, s):
        "check that os.path.expanduser / expandvars gives a useful result"
        try:
            if method(s) not in (None, s):
                return method(s)
        except:
            pass
        return None

    # for Unixes, allow for sudo case
    susername = os.environ.get("SUDO_USER", None)
    if HAS_PWD and susername is not None and home is None:
        home = pwd.getpwnam(susername).pw_dir

    # try expanding '~' -- should work on most Unixes
    if home is None:
        home = check(os.path.expanduser, '~')

    # try the common environmental variables
    if home is  None:
        for var in ('$HOME', '$HOMEPATH', '$USERPROFILE', '$ALLUSERSPROFILE'):
            home = check(os.path.expandvars, var)
            if home is not None:
                break

    # For Windows, ask for parent of Roaming 'Application Data' directory
    if home is None and os.name == 'nt':
        try:
            from win32com.shell import shellcon, shell
            home = shell.SHGetFolderPath(0, shellcon.CSIDL_APPDATA, 0, 0)
        except ImportError:
            pass

    # finally, use current folder
    if home is None:
        home = os.path.abspath('.')
    return nativepath(home)


def fix_paths(script, folder=None, icon_path=None, icon=None):
    """get absolute paths to

    1.  script
    2.  desktop folder or subfolder (creating if needed)
    3.  icon

    """
    scriptname = os.path.abspath(script)

    dest = os.path.join(get_homedir(), 'Desktop')
    if folder is not None:
        dest = os.path.join(dest, folder)
        if not os.path.exists(dest):
            os.mkdir(dest)

    if icon_path is None:
        _path, _fname = os.path.split(__file__)
        icon_path = os.path.join(_path, 'icons')
    if icon is None:
        icon = 'py'
    ext = '.ico'
    if platform.startswith('darwin'):
        ext = '.icns'
    iconfile = os.path.abspath(os.path.join(icon_path, icon + ext))

    return scriptname, dest, iconfile
