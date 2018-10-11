import sys
from time import sleep, time
from datetime import datetime

from optparse import OptionParser

usage = "Usage: timer.py [options]"

parser = OptionParser(usage=usage, prog="timer", version="simple clock")

parser.add_option("-t", "--time", dest="maxtime", metavar='maxtime',
                      default=None, help="maximum run time (seconds)")
parser.add_option("-u", "--update", dest="update", metavar='update',
                      default=0.1, help="update time (seconds)")

(options, args) = parser.parse_args()

update = float(options.update)
maxtime = options.maxtime
if maxtime is not None:
    maxtime = float(maxtime)

t0 = time()

while True:
    sleep(update)
    print("%s : %.3f " % (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), time()-t0))
    sys.stdout.flush()
    if maxtime is not None and (time()-t0 > maxtime):
        break

print("done.")
sleep(0.5)
