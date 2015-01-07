import random
import time

from predictor import Predictor

class RandomPredictor(Predictor):
    def get_name(self):
        return 'Random Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1

        candidate = random.sample(xrange(1, 81), 8)
        candidate = sorted(candidate)

        if debug:
            output = list()
            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % candidate)
            output.append('')
        else:
            output = dict()
            output['period'] = '%d' % target_period
            output['numbers'] = candidate

        return output

if __name__ == '__main__':
    p = RandomPredictor()
    print '\n'.join(p.predict(debug=True))
