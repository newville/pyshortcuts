#!/usr/bin/env python
"""
shortcut function
"""
from pathlib import Path
from collections import namedtuple

from .utils import get_pyexe, fix_filename, scut_ext, ico_ext

Shortcut = namedtuple("Shortcut", ('name', 'description', 'icon', 'target',
                      'working_dir', 'script', 'full_script', 'arguments',
                      'desktop_dir', 'startmenu_dir'))


def shortcut(script, userfolders, name=None, description=None,
             folder=None, working_dir=None, icon=None):
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
      icon           path for icon file
      target         name of the shortcut file (without folder name)
      working_dir    directory where to run the script in
      script         shortname of python script to be run (without arguments)
      full_script    full path of python script to be run (without arguments)
      arguments      command line arguments
      desktop_dir    full path of desktop folder (may need to be created)
      startmenu_dir  full path of startmenu folder (may need to be created)

    """
    if not isinstance(script, str) or len(script) < 1:
        raise ValueError("`script` for shortcut must be a non-zero length string")

    words = script.strip().split(' ', 1)
    if len(words) < 2:
        words.append('')

    script, arguments = words[0], words[1]
    if script in ('_', '{}'):
        script = words[0] = get_pyexe()

    full_script = Path(script).resolve().as_posix()

    if name is None:
        name = script

    name = fix_filename(Path(name).stem)
    if name.endswith('.py'):
        name = name[:-3]

    if description is None:
        description = name

    target = f'{name}.{scut_ext}'
    if icon is not None and len(str(icon)) > 0:
        picon = Path(icon).resolve()
        if not picon.exists():
            for ext in ico_ext:
                ticon = Path(f"{icon:s}.{ext:s}").resolve()
                if ticon.exists():
                    picon = ticon
                    break

    if icon is None or not Path(icon).exists():
        _parent = Path(__file__).parent
        icon = f'py.{ico_ext[0]:s}'
        icon = Path(_parent, 'icons', icon).resolve().as_posix()

    desktop_dir = userfolders.desktop
    if folder is not None:
        if folder.startswith(desktop_dir):
            folder = folder[len(desktop_dir)+1:]
        desktop_dir = Path(desktop_dir, folder).resolve().as_posix()

    startmenu_dir = userfolders.startmenu
    if folder is not None and len(startmenu_dir) > 1:
        if folder.startswith(startmenu_dir):
            folder = folder[len(startmenu_dir)+1:]
        startmenu_dir = Path(startmenu_dir, folder).resolve().as_posix()

    return Shortcut(name, description, icon, target, working_dir,
                    script, full_script, arguments, desktop_dir,
                    startmenu_dir)
