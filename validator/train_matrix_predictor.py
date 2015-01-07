import os
import copy
import sys
from constant import COOKED_DATA_DIR
from constant import PICKLE_FILENAME
import cPickle as pickle
from matrix import Matrix

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: %s [width] [height]' % sys.argv[0]
        sys.exit(1)

    width = int(sys.argv[1])
    height = int(sys.argv[2])

    with open(PICKLE_FILENAME, 'r') as ff:
        all_data = pickle.load(ff)

    dataset_end = max(all_data.keys())
    dataset_begin = min(all_data.keys())

    training_dataset = os.path.join(COOKED_DATA_DIR, 'matrix_predictor_%d_%d' % (width, height))
    try:
        with open(training_dataset, 'r') as ff:
            training_data = pickle.load(ff)
    except IOError:
        training_data = dict()

    bitmap = list()
    for period in xrange(dataset_end, dataset_begin - 1, -1):
        bit = [False] * 80
        for num in all_data[period]['numbers']:
            bit[num - 1] = True
        bitmap.append(tuple(bit))
    bitmap = tuple(bitmap)

    for y in xrange(len(bitmap) - 1 - height + 1, -1, -1):
        period = dataset_end - y
        if period not in training_data:
            if period - 1 in training_data:
                training_data[period] = copy.deepcopy(training_data[period - 1])
            else:
                training_data[period] = dict()

            for x in xrange(80 - 1 - width + 1, -1, -1):
                m = Matrix.create_from_bitmap(width, height, bitmap, x, y)
                if m in training_data[period]:
                    training_data[period][m] += 1
                else:
                    training_data[period][m] = 1

    with open(training_dataset, 'w') as ff:
        pickle.dump(training_data, ff, pickle.HIGHEST_PROTOCOL)
