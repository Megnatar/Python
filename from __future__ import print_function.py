from __future__ import print_function
import sys
for i in range(10**6):
    perc = float(i) / 10**6 * 10
    print(">>> Download is {}% complete      ".format(perc), end='\r')
    sys.stdout.flush()
print("")
