from predictor import Predictor
from operator import itemgetter

class Heuristic2Predictor(Predictor):
    def __init__(self):
        super(Heuristic2Predictor, self).__init__()

        self._height = 20

    def get_name(self):
        return 'Heuristic2 Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1
            
        try:
            self._all_data[target_period - 1 - self._height -1]
        except KeyError:
            return {'numbers': []}

        count = [0] * 80
        for i in xrange(self._height):
            for num in self._all_data[target_period - 1 - i]['numbers']:
                count[num - 1] += 1

        result = sorted(enumerate(count), key=itemgetter(1), reverse=True)[:6]
        candidate = [num[0] + 1 for num in result]

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
    p = Heuristic2Predictor()
    print '\n'.join(p.predict(debug=True))
