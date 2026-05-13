.. _utility_funcs:

.. module:: pyshortcuts.utils

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

.. autofunction:: isotime

This is shorthand for::

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

.. autofunction:: get_homedir

This sort of shorthand for::

        pathlib.Path.home().resolve().as_posix()

except that it also checks for ``SUDO_USER`` on POSIX systems, and it always uses the
``win32com`` module on Windows.



:func:`get_cwd`: get current working directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: get_cwd


This mostly shorthand for::

        pathlib.Path('.').resolve().as_posix()


:func:`fix_filename`: turn a string into a valid filename
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: fix_filename

Given a string, :func:`fix_filename` will return a "good" file name that
will work on any operating system.  Most of the disallowed or even
"inconvenient" characters will be converted to '_'.   The filename will not
have more than 1 '.' character.


:func:`new_filename`: make sure a filename is not in use
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: new_filename

Given a string (perhaps first run through :func:`fix_filename`),
:func:`new_filename` will return a file name that is not in use in the
current working folder.  Generally, numbers will be incremented in order so
that an input of `file.001` might become `file.002` or `file.004` if the
interim files exist.   If a file named `foo.dat`  exists, the `001` will be
inserted before the dot: `foo_001.dat`.   The filenumbers are not limited to
1000.


:func:`read_textfile`: read a text file to string
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: read_textfile

Given a filename or file-like object (`io.IOBase` instance), this returns a
'\\n'-delimited string from the file. This handles the possibility of different
unicode encodings by reading the file contents as bytes, and then using
``str(charset_normalizer.from_bytest(data).best())`` to convert to a string.
Line endings of `\\r` and `\\r\\n` are replaced by `\\n`.


:func:`gformat`: fixed formatting of floating point numbers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: pyshortcuts.gformat

.. autofunction:: gformat

:func:`gformat` converts a floating point number to a string with a
specified length, and maximizing the displayed precision for that
length.  This is very useful for creating tables of floating point
numbers.

The formatting will be similar to  '%g'-like format, expect that:

     a) the length of the output string will be of the requested length.
     b) positive numbers will have a leading blank.
     c) the precision will be as high as possible.
     d) trailing zeros will not be trimmed.

The precision displayed will be determined by the length of the string.

An example::

    >>>from pyshortcuts import gformat
    >>> gformat(1023/78, length=11)
    ' 13.1153846'
    >>> gformat(10.2, length=11)
    ' 10.2000000'
    >>> gformat(-1/732023, length=11))
    '-1.36608e-6'
    >>> gformat(-1/732023, length=15)
    '-0.000001366077'
    >>> gformat(6/80030, length=7)
    ' 7.5e-5'


:func:`sleep`: a higher-precision sleep
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Python's `time.sleep` function can be somewhat inaccurate, often
sleeping 10 or more milliseconds more than requested. Some
applications may want a higher-precision precision `sleep`.  The
version provided here is just::

    def sleep(duration):
        "more accurate sleep()"
        end = perf_counter() + duration
        while perf_counter() < end:
            pass


:func:`debugtimer`: debugging runtime of code in a function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. module:: pyshortcuts.debugtimer

Debugging the run time for a function or section of code is a common
need, and can be a painful process.  Using Python's `timeit` module is
really good at timing a single statement, but not good at answering
"how long is each section of code taking to run".  Sometimes you just
want to print out times to find where code is slow.  That gets
cumbersome to manage.

The :func:`debugtimer` helps with this process by creating a
DebugTimer object, with a method :meth:`.add` to mark the time with a
message, and methods :meth:`get_report` and :meth:`.show()` methods to
show a report of total and incremental run times for a section of
code. An example usage would be::


    import numpy as np
    from pyshortcuts import debugtimer, sleep

    SHOW_TIMING = True
    dtimer = debugtimer('test timer', precision=4)
    sleep(0.502)
    dtimer.add('slept for 0.500 seconds')
    nx = 10_000_000
    x = np.arange(nx, dtype='float64')/3.0
    dtimer.add(f'created numpy array len={nx}')
    s = np.sqrt(x)
    dtimer.add('took sqrt')
    if SHOW_TIMING:
        dtimer.show()

which would print out a report like::

   +----------------------------------+--------------+--------------+
   | Message                          |   Delta Time |   Total Time |
   +==================================+==============+==============+
   | test timer: 2026-05-13 10:30:54  |       0.0000 |       0.0000 |
   | slept for 0.500 seconds          |       0.5020 |       0.5020 |
   | created numpy array len=10000000 |       0.4010 |       0.9030 |
   | took sqrt                        |       0.4349 |       1.3379 |
   +----------------------------------+--------------+--------------+


Note that setting `SHOW_TIMING` to `False` would suppess the printing
of the timing report. This approach can be helpful during development
(or even in production code), as the creation of the `dtimer` object
and the `dtimer.add()` calls add very little runtime cost.

The timing data stored uses Python's `time.perf_counter()` function, so should
be a high-precision time measurement.

The `debugtimer function` also stores the number of imported modules (from
`len(sys.modules)`)at each event, which can be displayed with the optional
`use_mod_count` option either when createing the `debugtimer` or when getting
the output.

.. autofunction:: debugtimer

The returned `debgugTimer` object will have several methods:

.. autoclass:: DebugTimer

.. automethod:: DebugTimer.clear

.. automethod:: DebugTimer.add

.. automethod:: DebugTimer.get_report

.. automethod:: DebugTimer.show
