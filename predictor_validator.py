import sys
import cPickle as pickle
from constant import PICKLE_FILENAME
from reward import reward_table

from heuristic_predictor import HeuristicPredictor
from pure_prob_predictor import PureProbPredictor
from gg_predictor import GGPredictor
from matrix_predictor import MatrixPredictor
from random_predictor import RandomPredictor
from markov_predictor import MarkovPredictor
from heuristic2_predictor import Heuristic2Predictor
from delta_predictor import DeltaPredictor
predictors = list()
predictors.append(HeuristicPredictor)
predictors.append(PureProbPredictor)
predictors.append(GGPredictor)
predictors.append(RandomPredictor)
predictors.append(MarkovPredictor)
#predictors.append(MatrixPredictor)
predictors.append(Heuristic2Predictor)
predictors.append(DeltaPredictor)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        debug = True
    else:
        debug = False

    with open(PICKLE_FILENAME, 'r') as ff:
        all_data = pickle.load(ff)

    min_period = min(all_data.keys())
    max_period = max(all_data.keys())
    dataset_begin = min_period + 10
    dataset_end = max_period
    if dataset_begin > dataset_end:
        print 'Not enough data for validation'
        sys.exit(1)

    for pred in predictors:
        p = pred()
        matrix = 0
        hit = 0
        spend = 0
        earned = 0
        earned_cash = 0
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
                if (h_num, m_num) in reward_table:
                    earned += 1
                    earned_cash += reward_table[(h_num, m_num)]
                    earned_set.append((h_num, m_num))

        print 'predictor: %s' % p.get_name()

        if matrix == 0:
            print 'hit rate: N/A'
        else:
            print 'hit rate: %.6f  (%d / %d)' % ((float(hit) / matrix), hit, matrix)

        if spend == 0:
            print 'C/P: N/A'
        else:
            print 'C/P: %.6f  (%d / %d)' % ((float(earned) / spend), earned, spend)
            print 'earned set: %s' % earned_set
            print 'spend: %d NTD' % (spend * 25)
            print 'earned cash: %d NTD' % earned_cash
        print
