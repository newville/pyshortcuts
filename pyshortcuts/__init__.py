#!/usr/bin/env python

__version__ = '1.6'
__data__ = '26-Sept-2019'

import os
import sys
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import namedtuple

UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))

platform = sys.platform
if os.name == "nt":
    platform = "win"
if platform == "linux2":
    platform = "linux"

from .linux import (scut_ext, ico_ext, make_shortcut,
                    get_folders, get_homedir, get_desktop)

if platform.startswith('win'):
    from .windows import (scut_ext, ico_ext, make_shortcut,
                          get_folders, get_homedir, get_desktop)

elif platform.startswith('darwin'):
    from .darwin import (scut_ext, ico_ext, make_shortcut,
                         get_folders, get_homedir, get_desktop)

from .shortcut import shortcut, Shortcut, fix_filename

try:
    import wx
    HAS_WX = True
    from .wxgui import ShortcutFrame
except ImportError:
    HAS_WX = False


# for back-compat
from . import utils
utils.get_homedir = get_homedir
utils.get_folders = get_folders
utils.platform = platform


def shortcut_cli():
    '''
    command-line interface to creating desktop shortcuts
    '''
    desc = 'create desktop and start menu shortcuts'
    version_string = 'pyshortcut %s' % (__version__)


    parser = ArgumentParser(description=desc, # version=version_string,
                            formatter_class=RawDescriptionHelpFormatter)


    parser.add_argument('-v', '--version', dest='version', action='store_true',
                        default=False, help='show version')

    parser.add_argument('-n', '--name', dest='name', default=None,
                        help='name for shortcut link')

    parser.add_argument('-i', '--icon', dest='icon', default=None,
                        help='name of icon file')

    parser.add_argument('-f', '--folder', dest='folder', default=None,
                        help='subfolder on desktop to put shortcut')

    parser.add_argument('-e', '--executable', dest='exe', default=None,
                        help='name of executable to use (python)')

    parser.add_argument('-t', '--terminal', dest='terminal', action='store_true',
                        default=True, help='run script in a Terminal [True]')

    parser.add_argument('-g', '--gui', dest='gui', action='store_true',
                        default=False, help='run script as GUI, with no Terminal [False]')

    parser.add_argument('-d', '--desktop', dest='desktop', action='store_true',
                        default=True, help='create desktop shortcut [True]')

    parser.add_argument('-s', '--startmenu', dest='startmenu', action='store_true',
                        default=True, help='create Start Menu shortcut [True]')

    parser.add_argument('-w', '--wxgui', dest='wxgui', action='store_true',
                        default=False, help='run GUI version of pyshortcut [False]')

    parser.add_argument('scriptname', nargs='?',
                        help='script name, including arguments')

    args = parser.parse_args()

    if args.version:
        print("pyshortcuts {:s}".format(__version__))

    if HAS_WX and args.wxgui:
        app = wx.App()
        ShortcutFrame().Show(True)
        app.MainLoop()
        sys.exit()

    if args.gui:
        args.terminal = False

    if args.scriptname is None:
        print("pyshortcut: must provide one script.  try 'pyshortcuts -h'")
        sys.exit()

    desc = scriptname = args.scriptname
    make_shortcut(scriptname, name=args.name, description=desc,
                  terminal=args.terminal, folder=args.folder,
                  icon=args.icon, desktop=args.desktop,
                  startmenu=args.startmenu, executable=args.exe)
