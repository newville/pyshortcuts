#!/usr/bin/env python
"""
utilities for pyshortcuts
"""
import os, sys
from pathlib import Path
from datetime import datetime
from string import ascii_letters


def isotime(dtime=None, timepec='seconds'):
    """return ISO format of current timestamp:
          2024-04-27 17:31:12
    """
    if dtime is None:
        dtime = datetime.now()
    return datetime.isoformat(dtime, sep=' ', timespec=timespec)

BAD_FILECHARS = ';~,`!%$@$&^?*#:"/|\'\\\t\r\n(){}[]<>'
GOOD_FILECHARS = '_'*len(BAD_FILECHARS)
TRANS_FILE = str.maketrans(BAD_FILECHARS, GOOD_FILECHARS)

def fix_filename(filename):
    """
    fix string to be a 'good' filename, with very few special
    characters and (optionally) no more than 1 '.'.

    More restrictive than most OSes, but avoids hard-to-deal with filenames
    """
    fname = str(filename).translate(TRANS_FILE)
    if fname.count('.') > 1:
        words = fname.split('.')
        ext = words.pop()
        fname = f"{'_'.join(words)}.{ext}"
    return fname

def fix_varname(varname):
    """fix string to be a 'good' variable name."""
    vname = fix_filename(varname)
    if vname[0] not in (ascii_letters+'_'):
        vname = f'_{vname}'
    for c in '=+-.':
        vname = vname.replace(c, '_')
    while vname.endswith('_'):
        vname = vname[:-1]
    while '__' in vname:
        vname = vname.replace('__', '_')
    return vname

def get_pyexe():
    return Path(sys.executable).resolve().as_posix()

def new_filename(filename):
    """
    increment filename to be an unused filename
    """
    fpath = Path(filename)
    if fpath.exists():
        fstem = fpath.stem
        fsuffix = fpath.suffix
        if fsuffix.startswith('.'):
            fsuffix = fsuffix[1:]
        if len(fsuffix) == 0:
            fsuffix = 'txt'
        int_suffix = True
        fsint = 0
        try:
            fsint = int(fsuffix)
        except (ValueError, TypeError):
            int_suffix = False
        while fpath.exists():
            fsint += 1
            if int_suffix:
                fpath = Path(f"{fstem}.{fsint:03d}")
            else:
                if '_' in fstem:
                    w = fstem.split('_')
                    try:
                        fsint = int(w[-1])
                        fstem = '_'.join(w[:-1])
                    except (ValueError, TypeError):
                        pass
                fpath = Path(f"{fstem}_{fsint:03d}.{fsuffix}")

    return fpath.as_posix()

def bytes2str(s):
    'byte to string conversion'
    if isinstance(s, str):
        return s
    elif isinstance(s, bytes):
        return s.decode(sys.stdout.encoding)
    return str(s, sys.stdout.encoding)

def str2bytes(s):
    'string to byte conversion'
    if isinstance(s, bytes):
        return s
    return bytes(s, sys.stdout.encoding)
