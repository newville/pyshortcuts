#!/usr/bin/env python

__version__ = '1.1'

import os
import sys
from optparse import OptionParser

from .utils import platform

make_shortcut = None
if platform.startswith('win'):
    from .windows import make_shortcut

elif platform.startswith('darwin'):
    from .darwin import make_shortcut

elif platform.startswith('linux'):
    from .linux import make_shortcut

try:
    import wx
    from .wxgui import ShortcutFrame
    HAS_WX = True
except ImportError:
    HAS_WX = False

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

    parser.add_option('-t', '--terminal', dest='terminal', action='store_true',
                      default=True, help='run in a Terminal [True]')

    parser.add_option('-g', '--gui', dest='gui', action='store_true',
                      default=False, help='run as GUI, with no Terminal [False]')

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
                  icon=options.icon)
