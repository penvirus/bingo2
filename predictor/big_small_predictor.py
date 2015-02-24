from predictor import Predictor
from collections import defaultdict
from operator import itemgetter

class BigSmallPredictor(Predictor):
    def get_name(self):
        return 'Big Small Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        min_period = self.get_min_period()
        max_period = self.get_max_period()

        even_frequency = defaultdict(int)
        combo = 0
        for i in xrange(min_period, max_period):
            if self._all_data[i]['big_small'] == 'even':
                combo += 1
            else:
                if combo:
                    even_frequency[combo] += 1
                    combo = 0

        if debug:
            output = list()

            output.append('min ==> %d' % min_period)
            output.append('max ==> %d' % max_period)

            matrix = sum(v for k, v in even_frequency.items())
            output.append('matrix ==> %d' % matrix)

            for k, v in even_frequency.items():
                output.append('%3d ==> %3d (%.12f %%)' % (k, v, float(v) * 100 / matrix))
        else:
            output = dict()

        return output

if __name__ == '__main__':
    p = BigSmallPredictor()
    print '\n'.join(p.predict(debug=True))
