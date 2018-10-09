#!/usr/bin/env python
"""
Create desktop shortcuts for Linux
"""
from __future__ import print_function
import os
import sys

from .utils import get_paths

def make_shortcut(script, name, description=None, terminal=False,
                  icon_path=None, icon=None):
    """create linux .desktop file"""
    if description is None:
        description = name

    desktop, script, icon_path = get_paths(script, icon_path)

    buff = ['[Desktop Entry]']
    buff.append('Name=%s' % name)
    buff.append('Type=Application')
    buff.append('Comment=%s' % description)
    if terminal:
        buff.append('Terminal=true')
    else:
        buff.append('Terminal=false')
    if icon:
        buff.append('Icon=%s' % os.path.join(icon_path, '%s.ico' % icon))

    buff.append('Exec=%s %s' % (sys.executable, script))
    buff.append('')

    with open(os.path.join(desktop, '%s.desktop' % name), 'w') as fout:
        fout.write("\n".join(buff))
