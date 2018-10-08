#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
from __future__ import print_function
import os
import sys

from .homedir import get_homedir

def make_shortcut(script, name, description=None, icon=None, terminal=False):
    """create linux .desktop file"""
    if description is None:
        description = name

    desktop = os.path.join(get_homedir(), 'Desktop')
    script = os.path.abspath(script)

    buff = ['[Desktop Entry]']
    buff.append('Name=%s' % name)
    buff.append('Type=Application')
    buff.append('Comment=%s' % description)
    if terminal:
        buff.append('Terminal=true')
    else:
        buff.append('Terminal=false')
    if icon:
        buff.append('Icon=%s' % icon)

    buff.append('Exec=%s' % script)
    buff.append('')

    with open(os.path.join(desktop, '%s.desktop' % name), 'w') as fout:
        fout.write("\n".join(buff))
