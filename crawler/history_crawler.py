"""
    Put historic HTML (started from 2013/09/01) to RAW_DATA_DIR.
"""

import os
import sys
import requests
from datetime import date
from datetime import timedelta

from common.constant import RAW_DATA_DIR, DATA_SOURCE

if __name__ == '__main__':
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        begin = date(year, month, day)
    except IndexError:
        begin = date(2013, 9, 1)
    end = date.today()

    d = timedelta(days=1)
    while begin < end:
        target_filename = 'list_%04d%02d%02d.html' % (begin.year, begin.month, begin.day)
        target_dest = os.path.join(RAW_DATA_DIR, target_filename)
        if not os.path.exists(target_dest):
            url = '%s%s' % (DATA_SOURCE, target_filename)

            print 'fetching %s...' % url,
            sys.stdout.flush()

            r = requests.get(url)
            if r.status_code == 200:
                with open(target_dest, 'w') as ff:
                    ff.write(r.text.encode('UTF-8'))
                print 'success'
            else:
                print 'failed'
            sys.stdout.flush()

        begin += d
