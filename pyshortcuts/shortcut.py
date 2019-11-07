#!/usr/bin/env python
from __future__ import print_function
import os
import sys
from collections import namedtuple

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

Shortcut = namedtuple("Shortcut", ('name', 'description', 'icon', 'target',
                                   'script', 'full_script', 'arguments',
                                   'desktop_dir', 'startmenu_dir'))

def shortcut(script, userfolders, name=None, description=None, folder=None,categories=None,
             icon=None):
    """representation of a Shortcuts parameters.

    Arguments:
    ----------
    script        script to run, may include optional arguments
    userfolders   userfolders returned from the approprieate get_userfolders()
    name          name for shortcut (`None` to use name of script file)
    description   long description (`None` to use name of script file)
    folder        sub-folder of Desktop to place shortcut (`None` for on Desktop)
    icon          full path to icon file for shortcut (`None` for default)

    Returns:
    --------
    Namedtuple with the following fields:

      name           name for shortcut
      description    long description of shortcut
      icon           full path of icon file
      target         name of the shortcut file (without folder name)
      script         shortname of python script to be run (without arguments)
      full_script    full path of python script to be run (without arguments)
      arguments      command line arguments
      desktop_dir    full path of desktop folder (may need to be created)
      startmenu_dir  full path of startmenu folder (may need to be created)

    """
    from . import platform, scut_ext, ico_ext

    if not isinstance(script, str) or len(script) < 1:
        raise ValueError("`script` for shortcut must be a non-zero length string")

    words = script.split(' ', 1)
    if len(words) < 2:
        words.append('')

    script, arguments = words[0], words[1]

    full_script = os.path.abspath(script)

    if name is None:
        name = script

    _path, name = os.path.split(name)
    name = fix_filename(name)
    if name.endswith('.py'):
        name = name[:-3]

    if description is None:
        description = name

    target = '%s.%s' % (name, scut_ext)

    if icon is None:
        _path, _fname = os.path.split(__file__)
        icon = os.path.join(_path, 'icons', 'py.{:s}'.format(ico_ext))
    icon = os.path.abspath(icon)
    if not icon.endswith(ico_ext):
        icon = "{:s}.{:s}".format(icon, ico_ext)

    desktop_dir = userfolders.desktop
    if folder is not None:
        if folder.startswith(desktop_dir):
            folder = folder[len(desktop_dir)+1:]
        desktop_dir = os.path.join(desktop_dir, folder)

    startmenu_dir = userfolders.startmenu
    if folder is not None and len(startmenu_dir) > 1:
        if folder.startswith(startmenu_dir):
            folder = folder[len(startmenu_dir)+1:]
        startmenu_dir = os.path.join(startmenu_dir, folder)
    categories = categories

    return Shortcut(name, description, icon, target, script, full_script,
                    arguments, desktop_dir, startmenu_dir, categories)
