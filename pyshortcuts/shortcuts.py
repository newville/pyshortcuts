#!/usr/bin/env python
from __future__ import print_function
import os
import sys
from optparse import OptionParser

make_shortcut = None

if sys.platform.startswith('win') or os.name == 'nt':

    from .windows import make_shortcut

elif sys.platform == 'darwin':
    from .darwin import make_shortcut

elif sys.platform == 'linux':
    from .linux import make_shortcut


usage = "Usage: pyshortcuts [options] scriptname"

def shortcut_cli():
    """
    command-line interface to creating desktop shortcuts
    """

    parser = OptionParser(usage=usage, prog="pyshortcuts",
                          version="pyshortcuts command-line version 1")

    parser.add_option("-n", "--name", dest="name", metavar='link_name',
                      default=None, help="name for shortcut link")

    parser.add_option("-i", "--icon", dest="icon", metavar='icon_name',
                      default=None, help="name of icon file")

    parser.add_option("-p", "--path", dest="icon_path", metavar='icon_path',
                      default=None, help="path to icon resource folder")

    parser.add_option("-t", "--terminal", dest="terminal", action="store_true",
                      default=False, help="run in a Terminal")

    (options, args) = parser.parse_args()



    if len(args) != 1:
        print("pyshortcuts: must provide script.  try 'pyshortcuts -h'")
        sys.exit()

    name = desc = scriptname = args[0]

    if options.name  is not None:
        name = desc = options.name

    _, osname = make_shortcut.__module__.split('.')

    print("creating %s shortcut for script %s" % (osname, scriptname))

    make_shortcut(scriptname, name, terminal=options.terminal,
                  icon_path=options.icon_path, icon=options.icon)
