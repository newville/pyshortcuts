#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
from __future__ import print_function
import os
import sys

from .utils import get_homedir, get_paths

def make_shortcut(script, name, description=None, terminal=False,
                  icon_path=None, icon=None):
    """create windows shortcut"""
    from win32com.client import Dispatch

    if description is None:
        description = name

    homedir = get_homedir()
    desktop, sname, icon_path = get_paths(script, icon_path)

    pyexe = os.path.join(sys.prefix, 'pythonw.exe')
    if terminal:
        pyexe = os.path.join(sys.prefix, 'python.exe')

    # check for other valid ways to run each script, allowing
    # for Anaconda's automagic renaming and creation of exes.
    args = sname.split()
    sname = args.pop(0)
    if not os.path.exists(sname):
        for suffix in ('.exe', '-script.py'):
            tname = sname + suffix
            if os.path.exists(tname):
                sname = tname
    args.insert(0, sname)

    shortcut = Dispatch('WScript.Shell').CreateShortCut(
        os.path.join(desktop, name) +  '.lnk')

    shortcut.Targetpath =  '"%s"' % pyexe
    shortcut.Arguments = ' '.join(args)
    shortcut.WorkingDirectory = homedir
    shortcut.WindowStyle = 0
    shortcut.Description = description
    if icon is not None:
        shortcut.IconLocation = os.path.join(icon_path, icon + '.ico')
    shortcut.save()
