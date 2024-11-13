.. _utility_funcs:

Utility Functions
---------------------------

Pyshortcuts provides a number of utility functions, especially for working
with text files.  These may seem like an assorted mix of functions.  The author
found many of these useful in multiple projects, and rather than having
different versions in different packages, used this package to host those.  The
utilities here are small (adding no extra dependencies), but useful for many
projects.



:func:`isotime`: get time is ISO format
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`isotime` is a shorthand for::


    from datetime import datetime
    def isotime(dtime=None, timepec='seconds', sep=' '):
        """return ISO format of current timestamp:
              2024-04-27 17:31:12
        """
        if dtime is None:
            dtime = datetime.now()
        return datetime.isoformat(dtime, timespec=timespec, sep=sep)


There isn't more to it than that, it's just shorter.



:func:`get_homedir`: get home directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`get_homedir` is sort of shorthand for::


        pathlib.Path.home().resolve().as_posix()

except that it also checks for ``SUDO_USER`` on POSIX systems, and it always uses the
``win32com`` module on Windows.




:func:`get_cwd`: get current working directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:func:`get_cwd` is mostly shorthand for::

        pathlib.Path('.').resolve().as_posix()




:func:`fix_filename`: turn a string into a valid filename
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given a string, :func:`fix_filename` will return a "good" file name that
will work on any operating system.  Most of the disallowed or even
"inconvenient" characters will be converted to '_'.   The filename will not
have more than 1 '.' character.

:func:`new_filename`: make sure a filename is not in use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Given a string (perhaps first run through :func:`fix_filename`),
:func:`new_filename` will return a file name that is not in use in the
current working folder.  Generally, numbers will be incremented in order so
that an input of `file.001` might become `file.002` or `file.004` if the
interim files exist.   If a file named `foo.dat`  exists, the `001` will be
inserted before the dot: `foo_001.dat`.   The filenumbers are not limited to
1000.


:func:`gformat`: fixed formatting of floating point numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


:func:`gformat` converts a floating point number to a string with
exactly the specified length, and maximizing the displayed precision.  This is
very useful for creating tables of floating point numbers.

The  formatting will be similar to  '%g'-like format, expect that:

     a) the length of the output string will be of the requested length.
     b) positive numbers will have a leading blank.
     c) the precision will be as high as possible.
     d) trailing zeros will not be trimmed.

The precision will determined by the length of the string.

An example::

    >>>from pyshortcuts import gformat
    >>> gformat(1023/78, length=11)
    ' 13.1153846'
    >>> gformat(10.2, length=11)
    ' 10.2000000'
    >>> gformat(-102.e-8/78, length=11)
    '-1.30769e-8'

:func:`debugtimer`: debugging runtime of code in a function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Debugging run time in a function or section of code can be a painful process.
Using Python's `timeit` module is really good at timing a single statement, but
not good at answering "how long is each section of code taking to run".
Sometimes you just want to print out times to find where code is slow.  That
can somewhat challenging to track run times and gets cumbersome to manage.

The :func:`debugtimer` helps with this process by creating a DebugTimer object,
with methods :meth:`.add`, that marks time with a message, and the
:meth:`get_report`, and :meth:`.show()` methods to show a report of total and
incremental run times. An example usage would be::


    import time
    import numpy as np
    from pyshortcuts import debugtimer
    dtimer = debugtimer('test timer', precision=3)
    time.sleep(0.50)
    dtimer.add('slept for 0.500 seconds')
    nx = 10_000_000
    x = np.arange(nx, dtype='float64')/3.0
    dtimer.add(f'created numpy array len={nx}')
    s = np.sqrt(x)
    dtimer.add('took sqrt')
    dtimer.show()

which would print out a report like::

   # test timer                                      2024-10-11 14:07:27.868
   +----------------------------------+------------------+------------------+
   | Message                          |   Delta Time (s) |   Total Time (s) |
   +==================================+==================+==================+
   | start                            |            0.000 |            0.000 |
   | slept for 0.500 seconds          |            0.502 |            0.502 |
   | created numpy array len=10000000 |            0.073 |            0.575 |
   | took sqrt                        |            0.038 |            0.613 |
   +----------------------------------+------------------+------------------+
