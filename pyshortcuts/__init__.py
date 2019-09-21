#!/usr/bin/env python

__version__ = '1.4'

import os
import sys
from optparse import OptionParser
from collections import namedtuple

UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))

platform = sys.platform
if os.name == "nt":
    platform = "win"
if platform == "linux2":
    platform = "linux"

from .linux import (make_shortcut, get_folders, get_homedir,
                    scut_ext, ico_ext)

if platform.startswith('win'):
    from .windows import (make_shortcut, get_folders, get_homedir,
                          scut_ext, ico_ext)

elif platform.startswith('darwin'):
    from .darwin import (make_shortcut, get_folders, get_homedir,
                         scut_ext, ico_ext)


try:
    import wx
    from .wxgui import ShortcutFrame
    HAS_WX = True
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
    usage = 'Usage: pyshortcut [options] scriptname'
    vers = 'pyshortcut %s' % (__version__)

    parser = OptionParser(usage=usage, prog='pyshortcut', version=vers)

    parser.add_option('-n', '--name', dest='name', metavar='link_name',
                      default=None, help='name for shortcut link')

    parser.add_option('-i', '--icon', dest='icon', metavar='icon_name',
                      default=None, help='name of icon file')

    parser.add_option('-f', '--folder', dest='folder', metavar='subfolder',
                      default=None, help='subfolder on desktop to put icon')

    parser.add_option('-e', '--executable', dest='exe', metavar='exe_name',
                      default=None, help='name of executable to use (python)')

    parser.add_option('-t', '--terminal', dest='terminal', action='store_true',
                      default=True, help='run in a Terminal [True]')

    parser.add_option('-g', '--gui', dest='gui', action='store_true',
                      default=False, help='run as GUI, with no Terminal [False]')

    parser.add_option('-d', '--desktop', dest='desktop', action='store_true',
                      default=True, help='create desktop shortcut [True]')

    parser.add_option('-s', '--startmenu', dest='startmenu', action='store_true',
                      default=True, help='create Start Menu shortcut [True]')

    parser.add_option('-w', '--wxgui', dest='wxgui', action='store_true',
                      default=False, help='run GUI version of pyshortcut')


    (options, args) = parser.parse_args()

    if HAS_WX and options.wxgui:
        app = wx.App()
        ShortcutFrame().Show(True)
        app.MainLoop()
        sys.exit()

    if options.gui:
        options.terminal = False

    if len(args) != 1:
        print("pyshortcut: must provide script.  try 'pyshortcuts -h'")
        sys.exit()

    desc = scriptname = args[0]
    print('creating %s shortcut for script %s' % (platform, scriptname))
    make_shortcut(scriptname, name=options.name, description=desc,
                  terminal=options.terminal, folder=options.folder,
                  icon=options.icon, desktop=options.desktop,
                  startmenu=options.startmenu, executable=options.exe)
