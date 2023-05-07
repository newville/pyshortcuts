#!/usr/bin/env python
import sys
import os
from os.path import abspath, normpath, realpath
from os.path import (split as path_split, join as path_join,
                     exists as path_exists)
from collections import namedtuple

BAD_FILECHARS = ';~,`!%$@$&^?*#:"/|\'\\\t\r\n(){}[]<>'
GOOD_FILECHARS = '_'*len(BAD_FILECHARS)


def fix_filename(s, allow_multiple_dots=True):
    """
    fix string to be a 'good' filename, with very few special
    characters and (optionally) no more than 1 '.'.

    More restrictive than most OSes, but avoids nasty cases.
    """
    t = str(s).translate(str.maketrans(BAD_FILECHARS, GOOD_FILECHARS))
    if not allow_multiple_dots:
        if t.count('.') > 1:
            for i in range(t.count('.') - 1):
                idot = t.find('.')
                t = "%s_%s" % (t[:idot], t[idot+1:])
    return t

def get_pyexe():
    return realpath(normpath(sys.executable))

Shortcut = namedtuple("Shortcut", ('name', 'description', 'icon', 'target', 'working_dir',
                                   'script', 'full_script', 'arguments',
                                   'desktop_dir', 'startmenu_dir'))


def shortcut(script, userfolders, name=None, description=None, folder=None, working_dir=None,
             icon=None):
    """representation of a Shortcuts parameters.

    Arguments:
    ----------
    script        script to run, may include optional arguments
    userfolders   userfolders returned from the appropriate get_userfolders()
    name          name for shortcut (`None` to use name of script file)
    description   long description (`None` to use name of script file)
    folder        sub-folder of Desktop to place shortcut (`None` for on Desktop)
    working_dir   directory where to run the script in
    icon          full path to icon file for shortcut (`None` for default)

    Returns:
    --------
    Namedtuple with the following fields:

      name           name for shortcut
      description    long description of shortcut
      icon           full path of icon file
      target         name of the shortcut file (without folder name)
      working_dir    directory where to run the script in
      script         shortname of python script to be run (without arguments)
      full_script    full path of python script to be run (without arguments)
      arguments      command line arguments
      desktop_dir    full path of desktop folder (may need to be created)
      startmenu_dir  full path of startmenu folder (may need to be created)

    """
    from . import platform, scut_ext, ico_ext

    if not isinstance(script, str) or len(script) < 1:
        raise ValueError("`script` for shortcut must be a non-zero length string")

    words = script.strip().split(' ', 1)
    if len(words) < 2:
        words.append('')

    script, arguments = words[0], words[1]
    if script in ('_', '{}'):
        script = words[0] = get_pyexe()
        
    full_script = normpath(abspath(script))

    if name is None:
        name = script
    
    _path, name = path_split(name)
    name = fix_filename(name)
    if name.endswith('.py'):
        name = name[:-3]

    if description is None:
        description = name

    target = '%s.%s' % (name, scut_ext)

    if icon is not None and len(str(icon)) > 0:
        icon = normpath(abspath(icon))
        if not path_exists(icon):
            for ext in ico_ext:
                ticon = "{:s}.{:s}".format(icon, ext)
                if path_exists(ticon):
                    icon = ticon
                    break

    if icon is None or not path_exists(icon):
        _path, _fname = path_split(__file__)
        icon = normpath(path_join(abspath(_path), 'icons',
                                  'py.{:s}'.format(ico_ext[0])))

    desktop_dir = userfolders.desktop
    if folder is not None:
        if folder.startswith(desktop_dir):
            folder = folder[len(desktop_dir)+1:]
        desktop_dir = normpath(path_join(desktop_dir, folder))

    startmenu_dir = userfolders.startmenu
    if folder is not None and len(startmenu_dir) > 1:
        if folder.startswith(startmenu_dir):
            folder = folder[len(startmenu_dir)+1:]
        startmenu_dir = normpath(path_join(startmenu_dir, folder))

    return Shortcut(name, description, icon, target, working_dir,
                    script, full_script, arguments, desktop_dir,
                    startmenu_dir)
