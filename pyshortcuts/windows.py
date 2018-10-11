#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
from __future__ import print_function
import os
import sys

from .utils import get_homedir
from .shortcut import Shortcut

def make_shortcut(script, name, description=None, terminal=False,
                  folder=None, icon=None):
    """create windows shortcut"""
    from win32com.client import Dispatch

    scut = Shortcut(script, name=name, description=description,
                    folder=folder, icon=icon)

    homedir = get_homedir()

    pyexe = os.path.join(sys.prefix, 'pythonw.exe')
    if terminal:
        pyexe = os.path.join(sys.prefix, 'python.exe')

    # check for other valid ways to run each script, allowing
    # for Anaconda's automagic renaming and creation of exes.
    if not os.path.exists(scut.full_script):
        for suffix in ('.exe', '-script.py'):
            tname = scut.full_script + suffix
            if os.path.exists(tname):
                scut.full_script = tname

    wscript = Dispatch('WScript.Shell').CreateShortCut(scut.target)
    wscript.Targetpath = '"%s"' % pyexe
    wscript.Arguments = '%s %s' % (scut.full_script, scut.args)
    wscript.WorkingDirectory = homedir
    wscript.WindowStyle = 0
    wscript.Description = scut.description
    wscript.IconLocation = scut.icon
    wscript.save()
