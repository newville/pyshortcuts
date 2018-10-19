#!/usr/bin/env python
from __future__ import print_function
import os
import sys
from .utils import platform, get_homedir

import six

if six.PY3:
    maketrans = str.maketrans
else:
    from string import maketrans

BAD_FILECHARS = ';~,`!%$@$&^?*#:"/|\'\\\t\r\n(){}[]<>'
GOOD_FILECHARS = '_'*len(BAD_FILECHARS)

def fix_filename(s):
    """
    fix string to be a 'good' filename, with very few special
    characters and no more than 1 '.'.

    More restrictive than most OSes, but avoids nasty cases.
    """
    t = str(s).translate(maketrans(BAD_FILECHARS, GOOD_FILECHARS))
    if t.count('.') > 1:
        for i in range(t.count('.') - 1):
            idot = t.find('.')
            t = "%s_%s" % (t[:idot], t[idot+1:])
    return t

class Shortcut():
    """
    representation of a Shortcuts parameters.

    Arguments:
      script        script to run including optional arguments
      name          name for shortcut (`None` to use name of script file)
      description   shortcut long description (`None` to use name of script file)
      folder        folder under Desktop to place shortcut (`None` for on Desktop)
      icon          name of icon file (full path) for shortcut (`None` for default)

    Contains:
      name          name for shortcut
      script        name of python script to be run
      full_script   full name of python script to be run
      args          command line arguments
      target        full name of shortcut to create
      icon          full name of icon to use
    """
    def __init__(self, script, name=None, description=None,
                 folder=None, icon=None):

        words = script.split(' ', 1)
        if len(words) < 2:
            words.append('')
        self.script = words[0]
        self.args = words[1]
        self.full_script = os.path.abspath(self.script)

        if name is None:
            name = self.script

        _, name = os.path.split(name)
        name = fix_filename(name)
        if name.endswith('.py'):
            name = name[:-3]

        self.name = name
        self.description = description
        if self.description is None:
            self.description = name

        desktop = dest = os.path.join(get_homedir(), 'Desktop')
        if folder is not None:
            if folder.startswith(desktop):
                folder = folder[len(desktop)+1:]
            dest = os.path.join(desktop, folder)


        if not os.path.exists(dest):
            os.mkdir(dest)

        suffix = {'linux': 'desktop', 'darwin': 'app', 'win': 'lnk'}[platform]
        target = '%s.%s' % (name, suffix)
        self.folder = dest
        self.target = os.path.join(self.folder, target)
        self.folder = self.folder[len(desktop)+1:]

        self.icon = icon
        if self.icon is None:
            _path, _fname = os.path.split(__file__)
            _path = os.path.join(_path, 'icons')
            suffix = 'ico'
            if platform.startswith('darwin'):
                suffix = 'icns'
            self.icon = os.path.join(_path, 'py.%s' % (suffix))

        self.icon = os.path.abspath(self.icon)
