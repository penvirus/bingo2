"""
    Put historic HTML (started from 2013/09/01) to RAW_DATA_DIR.
"""

import os
import requests
from datetime import date
from datetime import timedelta
from constant import RAW_DATA_DIR, DATA_SOURCE

if __name__ == '__main__':
    if not os.path.exists(RAW_DATA_DIR):
        os.mkdir('raw_data')

    today = date.today()
    begin = date(2013, 9, 1)
    d = timedelta(days=1)
    while begin < today:
        target_filename = 'list_%04d%02d%02d.html' % (begin.year, begin.month, begin.day)
        target_dest = os.path.join(RAW_DATA_DIR, target_filename)
        if not os.path.exists(target_dest):
            url = '%s%s' % (DATA_SOURCE, target_filename)
            print 'fetching %s...' % url,
            r = requests.get(url)
            if r.status_code == 200:
                with open(target_dest, 'w') as ff:
                    ff.write(r.text.encode('UTF-8'))
                print 'success'
            else:
                print 'failed'
        begin += d
