from operator import itemgetter

from predictor import Predictor

class MarkovPredictor(Predictor):
    def __init__(self):
        super(MarkovPredictor, self).__init__()

        self._target = 2

    def get_name(self):
        return 'Markov Predictor  (t%d)' % self._target

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1

        try:
            self._all_data[target_period - 1]
        except KeyError:
            output = dict()
            output['period'] = target_period
            output['numbers'] = []
            return output

        prev_period = self._all_data[target_period - 1]['numbers']

        # initialize
        all_prob = list()
        prob = [0.0] * 80
        space = prev_period[1] - 1
        for num in xrange(1, prev_period[1]):
            prob[num - 1] = float(1) / space
        all_prob.append(prob)

        for i in xrange(1, 19):
            prob = [0.0] * 80
            for pos,p in enumerate(all_prob[i - 1]):
                if p == 0:
                    continue

                space = prev_period[i + 1] - (pos + 1 + 1)
                for num in xrange(pos + 1 + 1, prev_period[i + 1]):
                    prob[num - 1] += (float(1) / space) * p
            all_prob.append(prob)

        # last one
        prob = [0.0] * 80
        for pos,p in enumerate(all_prob[18]):
            if p == 0:
                continue

            space = 81 - (pos + 1 + 1)
            for num in xrange(pos + 1 + 1, 81):
                prob[num - 1] += (float(1) / space) * p
        all_prob.append(prob)

        total_prob = map(sum, zip(*all_prob))
        sorted_prob = sorted(enumerate(total_prob), key=itemgetter(1), reverse=True)
        candidate = list()
        for i in xrange(self._target):
            candidate.append(sorted_prob[i][0] + 1)

        big = 0
        for i in xrange(20):
            if sorted_prob[i][0] + 1 > 40:
                big += 1
        if big >= 13:
            big_small = 'big'
        elif big > 7:
            big_small = 'even'
        else:
            big_small = 'small'

        if debug:
            output = list()

            output.append('probability:')
            for i in xrange(self._target):
                output.append('%d: %.6f' % (sorted_prob[i][0] + 1, sorted_prob[i][1]))
            output.append('')

            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % candidate)

            output.append('big_small: %s' % big_small)
        else:
            output = dict()
            output['period'] = '%d' % target_period
            output['numbers'] = candidate

        return output


if __name__ == '__main__':
    p = MarkovPredictor()

    p._target = 2
    print '\n'.join(p.predict(debug=True))
    print

    p._target = 4
    print '\n'.join(p.predict(debug=True))
    print

    p._target = 1
    print '\n'.join(p.predict(debug=True))
    print

    p._target = 7
    print '\n'.join(p.predict(debug=True))
    print
