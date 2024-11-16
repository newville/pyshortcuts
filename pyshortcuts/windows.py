#!/usr/bin/env python
"""
Create desktop shortcuts for Windows
"""
import os
import sys
import time
from pathlib import Path
from collections import namedtuple
import win32com.client
from win32com.shell import shell, shellcon

from .utils import get_pyexe, get_homedir

def get_conda_active_env():
    '''Return name of active conda environment or empty string'''
    c_env = None
    try:
        c_env = os.environ['CONDA_DEFAULT_ENV']
    except KeyError:
        print("No conda env active, defaulting to base")
        c_env = "base"
    return c_env

# batch file to activate the environment
# for Anaconda Python before running command.
conda_env = get_conda_active_env()
ENVRUNNER = r"""
@ECHO OFF
if exist "%~dp0..\Scripts\activate.bat" (
  call "%~dp0..\Scripts\activate.bat" {0}
) else (
   if exist "%~dp0..\condabin\conda.bat" (
      call "%~dp0..\condabin\conda.bat" activate {0}
   )
)
echo # run in conda environment "%CONDA_DEFAULT_ENV%":
echo # %*
%*
""".format(conda_env)


def get_desktop():
    '''Return user Desktop folder'''
    return shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0)

def get_startmenu():
    '''Return user Start Menu Programs folder
    note that we return CSIDL_PROGRAMS not CSIDL_COMMON_PROGRAMS
    '''
    return shell.SHGetFolderPath(0, shellcon.CSIDL_PROGRAMS, None, 0)

def get_folders():
    """get user-specific folders

    Returns:
    -------
    Named tuple with fields 'home', 'desktop', 'startmenu'

    Example:
    -------
    >>> from pyshortcuts import get_folders
    >>> folders = get_folders()
    >>> print("Home, Desktop, StartMenu ",
    ...       folders.home, folders.desktop, folders.startmenu)
    """
    UserFolders = namedtuple("UserFolders", ("home", "desktop", "startmenu"))
    return UserFolders(get_homedir(), get_desktop(), get_startmenu())


def make_shortcut(script, name=None, working_dir=None, description=None, icon=None,
                  folder=None, terminal=True, desktop=True,
                  startmenu=True, executable=None, noexe=False):
    """create shortcut

    Arguments:
    ---------
    script      (str) path to script, may include command-line arguments
    name        (str, None) name to display for shortcut [name of script]
    working_dir (str, None) directory where to run the script in
    description (str, None) longer description of script [`name`]
    icon        (str, None) path to icon file [python icon]
    folder      (str, None) subfolder of Desktop for shortcut [None] (See Note 1)
    terminal    (bool) whether to run in a Terminal [True]
    desktop     (bool) whether to add shortcut to Desktop [True]
    startmenu   (bool) whether to add shortcut to Start Menu [True] (See Note 2)
    executable  (str, None) name of executable to use [this Python] (see Note 3)
    noexe       (bool) whether to use no executable (script is entire command) [False]

    Notes:
    ------
    1. `folder` will place shortcut in a subfolder of Desktop and/or Start Menu
    2. Start Menu does not exist for Darwin / MacOSX
    3. executable defaults to the Python executable used to make shortcut.
    """
    from .shortcut import shortcut
    userfolders = get_folders()

    scut = shortcut(script, userfolders, name=name, description=description,
                    working_dir=working_dir, folder=folder, icon=icon)

    if noexe:
        full_script =scut.script
        executable = ''
    else:
        full_script =scut.full_script
        if executable is None:
            executable = get_pyexe()
        executable = Path(executable).resolve().as_posix()

        if Path(scut.full_script).resolve() == Path(executable).resolve():
            executable = ''

    # Check for other valid ways to run the script
    # try appending .exe if script itself not found
    if not Path(full_script).exists():
        tname = full_script + '.exe'
        if Path(tname).exists():
            executable = tname
            full_script = ''

    # If script is already executable use it directly instead of via pyexe
    ext = os.path.splitext(full_script)[1].lower()
    known_exes = [e.lower() for e in os.environ['PATHEXT'].split(os.pathsep)]
    if ext != '.py' and ext in known_exes:
        executable = full_script
        full_script = ''
    full_script = ' '.join((full_script, scut.arguments))

    # If we're on Anaconda Python, we need to wrap this
    # script in a batch file that activates an environment
    if Path(sys.prefix, 'conda-meta').exists():
        runnerbat = f'envrunner-{conda_env}.bat'
        runner = Path(sys.prefix, 'Scripts', runnerbat).resolve().as_posix()
        with open(runner, 'w') as fh:
            fh.write(ENVRUNNER)
        time.sleep(0.05)
        full_script = f"{executable} {full_script}".strip()
        executable = runner

    for (create, ofolder) in ((desktop, scut.desktop_dir),
                             (startmenu, scut.startmenu_dir)):
        if create:
            if not Path(ofolder).exists():
                os.makedirs(ofolder)
            dest = Path(ofolder, scut.target).resolve().as_posix()

            _WSHELL = win32com.client.Dispatch("Wscript.Shell")
            wscript = _WSHELL.CreateShortCut(dest)
            wscript.Targetpath = f'"{executable}"'
            wscript.Arguments = full_script
            wscript.WorkingDirectory = scut.working_dir or userfolders.home
            wscript.WindowStyle = 0
            wscript.Description = scut.description
            wscript.IconLocation = scut.icon
            wscript.save()

    return scut
