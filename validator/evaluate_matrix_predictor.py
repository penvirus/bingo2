import sys
import cPickle as pickle
from constant import PICKLE_FILENAME
from math import ceil

from matrix_predictor import MatrixPredictor

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: %s [width] [height]' % sys.argv[0]
        sys.exit(1)

    with open(PICKLE_FILENAME, 'r') as ff:
        all_data = pickle.load(ff)

    min_period = min(all_data.keys())
    max_period = max(all_data.keys())
    dataset_begin = min_period + 10
    dataset_end = max_period
    if dataset_begin > dataset_end:
        print 'Not enough data for validation'
        sys.exit(1)

    width = int(sys.argv[1])
    height = int(sys.argv[2])

    p = MatrixPredictor()
    p.set_dimension(width, height)
    #p.set_target(6)

    matrix = 0
    hit = 0
    spend = 0
    earned = 0
    earned_set = list()

    for target_period in xrange(dataset_begin, dataset_end + 1):
        begin = min_period
        end = target_period - 1

        result = p.predict(target_period=target_period, dataset_begin=begin, dataset_end=end)

        actual_numbers = set(all_data[target_period]['numbers'])
        predicted_numbers = set(result['numbers'])
        hit_numbers = actual_numbers & predicted_numbers

        m_num = len(predicted_numbers)
        h_num = len(hit_numbers)
        matrix += m_num
        hit += h_num

        if m_num > 0 and m_num <= 10:
            spend += 1
            if (float(h_num) / m_num) >= 0.5:
                earned += 1
                earned_set.append((h_num, m_num))

    print 'predictor: %s' % p.get_name()

    if matrix == 0:
        print 'hit rate: N/A'
    else:
        print 'hit rate: %.6f  (%d / %d)' % ((float(hit) / matrix), hit, matrix)

    if spend == 0:
        print 'C/P: N/A'
    else:
        cp = float(earned) / spend
        if cp >= 0.2:
            print 'C/P: %.6f  (%d / %d)' % (cp, earned, spend)
            print 'earned set: %s' % earned_set
        else:
            print 'C/P: too low! %.6f' % cp
    print
    sys.stdout.flush()
