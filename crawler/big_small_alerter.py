"""
    Extract numbers either from file or a given line string.
"""

import sys
import time
import requests
from datetime import date
from datetime import timedelta
import cPickle as pickle
import xml.etree.ElementTree as ET
from cStringIO import StringIO
from subprocess import Popen, PIPE
import signal
import datetime

from common.constant import RAW_DATA_DIR, PICKLE_FILENAME, DATA_SOURCE

def extract_from_line(line, dest):
    root = ET.fromstring(line)

    period = int(root.find('./td').text.split('_')[0])
    time = root.find('./td').text.split('_')[1]
    numbers = [int(div.text) for div in root.iter('div')]
    special = [int(div.text) for div in root.iter('div') if 's' in div.attrib['class']][0]

    big = 0
    for n in numbers:
        if n >= 41:
            big += 1

    data = dict()
    data['period'] = period
    data['time'] = time
    data['numbers'] = numbers
    data['special'] = special
    if big >= 13:
        data['big_small'] = 'big'
    elif big > 7:
        data['big_small'] = 'even'
    else:
        data['big_small'] = 'small'

    dest[period] = data

def extract_from_file(fh, dest):
    for line in fh:
        if 'bingo_row' in line:
            line = line.replace('<br>', '')
            line = line.replace('<b>', '')
            line = line.replace('</b>', '_')
            extract_from_line(line, dest)

def get_max_period(all_data):
    return max(all_data.keys())

def get_min_period(all_data):
    return min(all_data.keys())

mail_list = 'thsu@varmour.com,newbug@varmour.com,alvion@varmour.com,slin@varmour.com,tshih@varmour.com'

def start_service():
    now = '%s' % datetime.datetime.now()
    msg = "Bingo Bingo Bot is now serving for you."
    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo Bingo Alert Service Up: %s' % now, '-t', mail_list], close_fds=True, stdin=PIPE)
    p.communicate(msg)

def stop_service(a, b):
    now = '%s' % datetime.datetime.now()
    msg = "Bingo Bingo Bot is stopped."
    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo Bingo Alert Service Down: %s' % now, '-t', mail_list], close_fds=True, stdin=PIPE)
    p.communicate(msg)
    sys.exit(0)

if __name__ == '__main__':
    today = date.today()
    url = '%s%s' % (DATA_SOURCE, 'list_%04d%02d%02d.html' % (today.year, today.month, today.day))
    saved_max_period = 0

    signal.signal(signal.SIGINT, stop_service)
    start_service()

    while True:
        print 'fetching %s...' % url,
        sys.stdout.flush()

        r = requests.get(url)
        if r.status_code == 200:
            fake_file = StringIO()
            fake_file.write(r.text.encode('UTF-8'))
            fake_file.seek(0)
            all_data = dict()
            extract_from_file(fake_file, all_data)
            fake_file.close()

            max_period = get_max_period(all_data)
            min_period = get_min_period(all_data)
            if max_period > saved_max_period:
                saved_max_period = max_period

                combo = 0
                for i in xrange(max_period, min_period, -1):
                    if all_data[i]['big_small'] == 'even':
                        combo += 1
                    else:
                        break

                if combo > 10:
                    msg = "Newest period: %d\nHas been even for %d round.\n" % (max_period, combo)
                    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo Bingo Alert Message For Next Period [%d]' % (max_period + 1), '-t', mail_list], close_fds=True, stdin=PIPE)
                    p.communicate(msg)
            print 'success'
        else:
            print 'failed'
        sys.stdout.flush()

        time.sleep(280)
