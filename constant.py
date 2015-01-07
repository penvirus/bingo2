import os

RAW_DATA_DIR = 'raw_data'
if not os.path.exists(RAW_DATA_DIR):
    os.mkdir(RAW_DATA_DIR)

COOKED_DATA_DIR = 'cooked_data'
if not os.path.exists(COOKED_DATA_DIR):
    os.mkdir(COOKED_DATA_DIR)

DATA_SOURCE = 'http://lotto.auzonet.com/bingobingo/'
PICKLE_FILENAME = os.path.join(COOKED_DATA_DIR, 'all_data')
