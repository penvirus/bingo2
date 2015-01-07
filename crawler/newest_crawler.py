"""
    Fetch newest numbers from http://lotto.auzonet.com/bingobingo.php.
"""

import os
import sys
import time
import requests
from datetime import date
import cPickle as pickle
from cStringIO import StringIO
from num_extractor import extract_from_file
from constant import PICKLE_FILENAME

if __name__ == '__main__':
    tmp_pickle_filename = '%s.tmp' % PICKLE_FILENAME
    today = date.today()
    url = 'http://lotto.auzonet.com/bingobingo/list_%04d%02d%02d.html' % (today.year, today.month, today.day)

    try:
        with open(PICKLE_FILENAME, 'r') as ff:
            all_data = pickle.load(ff)
    except IOError:
        all_data = dict()

    while True:
        print 'fetching %s...' % url,
        sys.stdout.flush()
        r = requests.get(url)
        if r.status_code == 200:
            fake_file = StringIO()
            fake_file.write(r.text.encode('UTF-8'))
            fake_file.seek(0)
            extract_from_file(fake_file, all_data)
            fake_file.close()
            print 'success'
        else:
            print 'failed'

        with open(tmp_pickle_filename, 'w') as ff:
            pickle.dump(all_data, ff, pickle.HIGHEST_PROTOCOL)
        os.rename(tmp_pickle_filename, PICKLE_FILENAME)

        print 'sleep 60 seconds..'
        time.sleep(60)
