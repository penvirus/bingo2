"""
    Extract numbers either from file or a given line string.
"""

import sys
import time
import requests
from datetime import date
import xml.etree.ElementTree as ET
from cStringIO import StringIO
from subprocess import Popen, PIPE
import signal
import datetime

from common.constant import DATA_SOURCE

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

mail_list = 'thsu@varmour.com,newbug@varmour.com,alvion@varmour.com,slin@varmour.com,marktseng@varmour.com,tshih@varmour.com'
threshold = 10

def start_service():
    now = '%s' % datetime.datetime.now()
    msg = "Bingo2 Bot is now serving for you.\n\nCurrent threshold is %d, that is, if the bingo result has been even for more than %d times, the Bingo2Bot will notify you.\n" % (threshold, threshold)
    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo2 Alert Service Up: %s, threshold is %d' % (now, threshold), '-t', mail_list], close_fds=True, stdin=PIPE)
    p.communicate(msg)

def stop_service(a, b):
    now = '%s' % datetime.datetime.now()
    msg = "Bingo2 Bot is stopped.\n"
    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo2 Alert Service Down: %s' % now, '-t', mail_list], close_fds=True, stdin=PIPE)
    p.communicate(msg)
    sys.exit(0)

def send_alert(max_period, combo):
    msgs = list()
    msgs.append('Newest period: %d' % max_period)
    msgs.append('Has been even for %d round.' % combo)
    msgs.append('')
    msgs.append('Please check the web page http://lotto.auzonet.com/bingobingo.php for further information.')
    msg = '\n'.join(msgs)
    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo2 Alert Message: target period is [%d], even for [%d] times' % (max_period + 1, combo), '-t', mail_list], close_fds=True, stdin=PIPE)
    p.communicate(msg)

def send_abort(max_period, big_small):
    msgs = list()
    msgs.append('Newest period: %d' % max_period)
    msgs.append('Has been "%s"' % big_small)
    msgs.append('')
    msgs.append('Please check the web page http://lotto.auzonet.com/bingobingo.php for further information.')
    msg = '\n'.join(msgs)
    p = Popen(['mail', '-a', 'From: Bingo2Bot <bingo2bot@varmour.com>', '-s', 'Bingo2 Alert Message: ABORT!!', '-t', mail_list], close_fds=True, stdin=PIPE)
    p.communicate(msg)

if __name__ == '__main__':
    saved_max_period = 0
    alerted = False

    signal.signal(signal.SIGINT, stop_service)
    start_service()

    while True:
        today = date.today()
        url = '%s%s' % (DATA_SOURCE, 'list_%04d%02d%02d.html' % (today.year, today.month, today.day))
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

                if combo >= threshold:
                    send_alert(max_period, combo)
                    alerted = True
                else:
                    if alerted:
                        send_abort(max_period, all_data[max_period]['big_small'])
                        alerted = False
            print 'success'
        else:
            print 'failed'
        sys.stdout.flush()

        time.sleep(30)
