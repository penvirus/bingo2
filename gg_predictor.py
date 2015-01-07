from predictor import Predictor
from heuristic_predictor import HeuristicPredictor
from pure_prob_predictor import PureProbPredictor
from random_predictor import RandomPredictor

class GGPredictor(Predictor):
    def __init__(self):
        super(GGPredictor, self).__init__()

        self._p1 = HeuristicPredictor()
        self._p2 = PureProbPredictor()

    def get_name(self):
        return 'GG Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1

        r1 = self._p1.predict(target_period=target_period, dataset_begin=dataset_begin, dataset_end=dataset_end, debug=False)
        r2 = self._p2.predict(target_period=target_period, dataset_begin=dataset_begin, dataset_end=dataset_end, debug=False)

        candidate = set(r1['numbers'])
        candidate &= set(r2['numbers'])
        candidate = sorted(candidate)

        if debug:
            output = list()
            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % candidate)
        else:
            output = dict()
            output['period'] = '%d' % target_period
            output['numbers'] = candidate

        return output

if __name__ == '__main__':
    p = GGPredictor()
    print '\n'.join(p.predict(debug=True))
