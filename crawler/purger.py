import os

from common.constant import RAW_DATA_DIR, PICKLE_FILENAME, DATA_SOURCE

if __name__ == '__main__':
    if os.path.exists(PICKLE_FILENAME):
        os.remove(PICKLE_FILENAME)
