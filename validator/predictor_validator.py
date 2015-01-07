import sys

from crawler.num_extractor import load
from common.constant import PICKLE_FILENAME
from common.reward import reward_table

from collections import defaultdict
from ascii_graph import Pyasciigraph

from predictor.alvion_heuristic_predictor import AlvionHeuristicPredictor
from predictor.pure_prob_predictor import PureProbPredictor
from predictor.matrix_predictor import MatrixPredictor
from predictor.random_predictor import RandomPredictor
from predictor.markov_predictor import MarkovPredictor
from predictor.delta_predictor import DeltaPredictor
predictors = list()
predictors.append(AlvionHeuristicPredictor)
predictors.append(PureProbPredictor)
predictors.append(RandomPredictor)
predictors.append(MarkovPredictor)
#predictors.append(MatrixPredictor)
predictors.append(DeltaPredictor)

def validate(pred, min_period, max_period):
    graph = Pyasciigraph()

    num_count = 0
    hit_count = 0
    spend_count = 0
    earned_count = 0
    earned_cash = 0
    earned_set = list()
    graph_data = defaultdict(int)

    for target_period in xrange(min_period, max_period + 1):
        dataset_begin = min_period
        dataset_end = target_period - 1

        if dataset_begin > dataset_end:
            continue

        result = p.predict(target_period=target_period, dataset_begin=dataset_begin, dataset_end=dataset_end)

        actual_numbers = set(all_data[target_period]['numbers'])
        predicted_numbers = set(result['numbers'])
        hit_numbers = actual_numbers & predicted_numbers

        m_count = len(predicted_numbers)
        h_count = len(hit_numbers)
        num_count += m_count
        hit_count += h_count

        if m_count > 0 and m_count <= 10:
            spend_count += 1
            if (h_count, m_count) in reward_table:
                earned_count += 1
                earned_cash += reward_table[(h_count, m_count)]
                earned_set.append((h_count, m_count))
                hour = '%s:00' % all_data[target_period]['time'].split(':')[0]
                graph_data[hour] += 1

    print 'predictor: %s' % p.get_name()

    for line in graph.graph('', graph_data.items(), sort=2):
        print line.encode('UTF-8')

    if num_count == 0:
        print 'hit rate: N/A'
    else:
        print 'hit rate: %.6f  (%d / %d)' % ((float(hit_count) / num_count), hit_count, num_count)

    if spend_count == 0:
        print 'C/P: N/A'
    else:
        print 'C/P: %.6f  (%d / %d)' % ((float(earned_count) / spend_count), earned_count, spend_count)
        print 'earned set: %s' % earned_set
        print 'spend: %d NTD' % (spend_count * 25)
        print 'earned cash: %d NTD' % earned_cash
    print

if __name__ == '__main__':
    all_data = load()

    min_period = min(all_data.keys())
    max_period = max(all_data.keys())
    if min_period > max_period:
        print 'Not enough data for validation'
        sys.exit(1)

    for pred in predictors:
        p = pred()

        if p.is_configurable():
            for target in xrange(1, 11):
                p.set_target(target)
                validate(p, min_period, max_period)
        else:
            validate(p, min_period, max_period)
