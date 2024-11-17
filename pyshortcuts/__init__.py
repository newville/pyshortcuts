#!/usr/bin/env python
"""
pyshortcuts
"""
import os
import sys
from pathlib import Path
from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .version import version as __version__
from .utils import (fix_filename, new_filename, fix_varname, isotime,
                    get_pyexe, bytes2str, str2bytes, get_homedir, get_cwd,
                    uname, scut_ext, ico_ext)

from .gformat import gformat
from .debugtimer import debugtimer

make_shortcut =  get_folders = None
if uname.startswith('lin'):
    from .linux import make_shortcut, get_folders
elif uname.startswith('darwin'):
    from .darwin import make_shortcut, get_folders
elif uname.startswith('win'):
    from .windows import make_shortcut, get_folders

# back compat
platform = uname

from .shortcut import shortcut, Shortcut

try:
    import wx
    from .wxgui import ShortcutFrame
except ImportError:
    ShortCutFrame = None


def get_desktop():
    "for back compatibility"
    return get_folders().desktop

def shortcut_cli():
    '''
    command-line interface to creating desktop shortcuts
    '''
    desc = 'create desktop and start menu shortcuts'

    parser = ArgumentParser(description=desc,
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
        if uname.startswith('win'):
            bindir = 'Scripts'
        fpath = Path(__file__)
        icon = Path(fpath.parent, 'icons', f'ladder.{ico_ext[0]}'
                        ).resolve().as_posix()
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
            p_icon = Path(args.icon).resolve()
            if p_icon.exists():
                icon = p_icon.resolve().as_posix()
            else:
                parent = p_icon.parent
                stem  = p_icon.stem
                for ext in ico_ext:
                    x = Path(parent, f"{stem}.{ext}").absolute()
                    if x.exists():
                        icon = x.resolve().as_posix()
            make_shortcut(args.scriptname, name=args.name,
                          terminal=args.terminal, folder=args.folder,
                          icon=icon, desktop=args.desktop,
                          startmenu=args.startmenu, executable=args.exe,
                          noexe=args.noexe)
