#!/usr/bin/env python

from pyshortcuts.version import version as __version__

import os
import sys

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .utils import (fix_filename, new_filename, fix_varname, isotime,
                    get_pyexe, bytes2str, str2bytes, get_homedir, get_cwd)
from .gformat import gformat
from .debugtimer import debugtimer


from .linux import make_shortcut, get_folders
platform = "linux"

if sys.platform.startswith('darwin'):
    platform = 'darwin'
    from .darwin import make_shortcut, get_folders

elif os.name.startswith('win'):
    platform = "win"
    from .windows import make_shortcut, get_folders

uname = platform

scut_ext = {'linux': 'desktop', 'darwin':'app', 'windows': 'lnk'}[platform]
ico_ext = {'linux': ('ico', 'png'),
           'darwin': ('icns',), 'windows': ('ico', )}[platform]

from .shortcut import shortcut, Shortcut

try:
    import wx
    from .wxgui import ShortcutFrame
except ImportError:
    ShortCutFrame = None


def get_cwd():
    """get current working directory
    Note: os.getcwd() can fail with permission error.

    when that happens, this changes to the users `HOME` directory
    and returns that directory so that it always returns an existing
    and readable directory.
    """
    try:
        return os.getcwd()
    except:
        home = get_homedir()
        os.chdir(home)
        return home


def shortcut_cli():
    '''
    command-line interface to creating desktop shortcuts
    '''
    desc = 'create desktop and start menu shortcuts'
    version_string = 'pyshortcuts %s' % (__version__)


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

    parser.add_argument('-x', '--no-executable', dest='noexe', action='store_true',
                        default=False, help='use no implied executable [False]')

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

    parser.add_argument('-b', '--bootstrap', dest='bootstrap', action='store_true',
                        default=False, help='make desktop shortcut to wxGUI')

    parser.add_argument('scriptname', nargs='?',
                        help='script name, including arguments')

    args = parser.parse_args()

    if args.version:
        print(f"pyshortcut {__version__}")

    if (args.wxgui or args.bootstrap) and ShortcutFrame is None:
        print("wxpython is required to run GUI")
        sys.exit()

    if args.bootstrap:
        bindir = 'bin'
        if platform.startswith('win'):
            bindir = 'Scripts'
        fpath = Path(__file__)
        here, this =fpath.parent, fpath.stem

        icon = Path(here, 'icons', f'ladder.{ico_ext[0]}').resolve().as_posix()
        script = Path(sys.prefix, bindir, 'pyshortcut').resolve().as_posix()
        make_shortcut(f"{script} --wxgui", name='PyShortcut',
                      terminal=False, icon=icon)

    elif args.wxgui:
        app = wx.App()
        ShortcutFrame().Show(True)
        app.MainLoop()

    else:
        if args.gui:
            args.terminal = False

        if args.scriptname is None:
            print("pyshortcut: must provide one script.  try 'pyshortcut -h'")
        else:
            make_shortcut(args.scriptname, name=args.name,
                          terminal=args.terminal, folder=args.folder,
                          icon=args.icon, desktop=args.desktop,
                          startmenu=args.startmenu, executable=args.exe,
                          noexe=args.noexe)
