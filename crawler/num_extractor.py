"""
    Extract numbers either from file or a given line string.
"""

import os
from datetime import date
from datetime import timedelta
import cPickle as pickle
import xml.etree.ElementTree as ET
from constant import RAW_DATA_DIR, PICKLE_FILENAME

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

if __name__ == '__main__':
    tmp_pickle_filename = '%s.tmp' % PICKLE_FILENAME

    try:
        with open(PICKLE_FILENAME, 'r') as ff:
            all_data = pickle.load(ff)
    except IOError:
        all_data = dict()

    today = date.today()
    #begin = date(2013, 9, 1)
    begin = today - timedelta(days=1)
    d = timedelta(days=1)
    while begin < today:
        target_filename = 'list_%04d%02d%02d.html' % (begin.year, begin.month, begin.day)
        target_dest = os.path.join(RAW_DATA_DIR, target_filename)
        print 'extract %s...' % target_dest,
        try:
            with open(target_dest, 'r') as ff:
                extract_from_file(ff, all_data)
            print 'success'
        except IOError:
            print 'skip'
        begin += d

    with open(tmp_pickle_filename, 'w') as ff:
        pickle.dump(all_data, ff, pickle.HIGHEST_PROTOCOL)
    os.rename(tmp_pickle_filename, PICKLE_FILENAME)
