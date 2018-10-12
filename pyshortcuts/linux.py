#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
from __future__ import print_function
import os
import sys

from .shortcut import Shortcut

def make_shortcut(script, name, description=None, terminal=True,
                  folder=None, icon=None):
    """create linux .desktop file"""
    if description is None:
        description = name

    scut = Shortcut(script, name=name, description=description, folder=folder, icon=icon)

    buff = ['[Desktop Entry]']
    buff.append('Name=%s' % scut.name)
    buff.append('Type=Application')
    buff.append('Comment=%s' % description)
    if terminal:
        buff.append('Terminal=true')
    else:
        buff.append('Terminal=false')

    buff.append('Icon=%s' % scut.icon)

    buff.append('Exec=%s %s %s' % (sys.executable, scut.full_script, scut.args))
    buff.append('')

    with open(scut.target, 'w') as fout:
        fout.write("\n".join(buff))
