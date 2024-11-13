#!/usr/bin/env python
"""
debug timer: measure run times of code, display results
"""
import time
from datetime import datetime

def isotime(dtime=None, sep=' '):
    "return datetime isoformat"
    if dtime is None:
        dtime = datetime.now()
    return datetime.isoformat(dtime, sep=sep)

class DebugTimer():
    '''
    Measure run times for lines of code and summarize results
    '''
    def __init__(self, title=None, verbose=False, precision=4):
        self.verbose = verbose
        if title is None:
            title = "DebugTimer"
        self.title = title
        self.precision = precision
        self.clear(title=title)

    def clear(self, title=None):
        """clear debugtimer"""
        self.data = []
        if title is None:
            title = self.title
        self.add('start')
        tparts = isotime().split('.')
        self.start_time = tparts[0] + '.' + tparts[1][:self.precision]

    def add(self, msg):
        "add message point to debugtimer"
        self.data.append((msg, time.perf_counter()))
        if self.verbose:
            print(msg)

    def get_report(self, precision=None):
        "get report text"
        if precision is None:
            precision = self.precision

        cols = [("Message", "Delta Time (s)", "Total Time (s)")]
        w0, w1, w2 = max(len(self.title), 32), 17, 17
        tlast = tstart = self.data[0][1]
        for msg, t in self.data:
            tt = f"{t-tstart:.{precision}f}"
            dt = f"{t-tlast:.{precision}f}"
            tlast = t
            cols.append((msg, dt, tt))
            w0 = max(len(msg)+1, w0)
            w1 = max(len(dt)+1,  w1)
            w2 = max(len(tt)+1,  w2)

        tline = f"+-{'-'*w0}+{'-'*w1}-+{'-'*w2}-+"
        out = [f"# {self.title:{w0}s}    {self.start_time:>{w1+w2}s}", tline]

        for i, col in enumerate(cols):
            out.append(f"| {col[0]:{w0}s}|{col[1]:>{w1}s} |{col[2]:>{w2}s} |")
            if i == 0:
                out.append(tline.replace('-', '='))
        out.append(tline)
        out.append('')

        return "\n".join(out)


    def show(self, precision=None, clear=True):
        "print report text"
        print(self.get_report(precision=precision))
        if clear:
            self.clear(title=self.title)


def debugtimer(title=None, precision=4, verbose=False):
    '''return a DebugTimer object to measure the run time of
    portions of code, and write a simple report.

    Arguments
    ------------
    title:      str, optional initial message ['DebugTimer']
    precision:  int, precision for timing results [4]
    verbose:    bool, whether to print() each message when entered [False]

    Returns
    --------
    DebugTimer object, with methods:

      clear(title=None)  : reset Timer
      add(message)       : record an event, saving message and time
      get_report()       : return text of report
      show()             : print out text of report and optionally clear

    Example:
    -------
      timer = debugtimer('timer testing', precision=4)
      result = foo(x=100)
      timer.add('ran function foo')
      bar(result)
      timer.add('ran bar')
      timer.show()
    '''
    return DebugTimer(title=title, precision=precision, verbose=verbose)



if __name__ == '__main__':
    import numpy as np
    dtimer = debugtimer('test timer')
    time.sleep(1.1010)
    dtimer.add('slept for 1.101 seconds')
    nx = 10_000_000
    x = np.arange(nx, dtype='float64')/3.0
    dtimer.add(f'created numpy array len={nx}')
    s = np.sqrt(x)
    dtimer.add('took sqrt')
    dtimer.show(precision=4)
