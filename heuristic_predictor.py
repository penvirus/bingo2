from predictor import Predictor

class HeuristicPredictor(Predictor):
    def __init__(self):
        super(HeuristicPredictor, self).__init__()

        self._depth = 5

    def get_name(self):
        return 'Heuristic Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1

        history = list()
        for p in xrange(target_period - 1, target_period - 1 - self._depth, -1):
            history.append(self._all_data[p]['numbers'])

        dup = list()
        dup.append(history[0])
        for i in xrange(len(history) - 1):
            d = list()
            for num in dup[i]:
                if num in history[i + 1]:
                    d.append(num)
            dup.append(d)

        try:
            cont_seq = []
            i = 0
            while i < len(history[0]):
                num = history[0][i]

                if history[0][i + 1] == num + 1:
                    seq = [num]

                    while history[0][i + 1] == num + 1:
                        seq.append(num + 1)
                        i += 1

                    cont_seq.append(seq)

                i += 1
        except IndexError:
            pass

        candidate = set(history[0])
        for i in xrange(1, len(dup)):
            candidate -= set(dup[i])
        for cont in cont_seq:
            candidate -= set(cont)
        candidate = sorted(candidate)

        if debug:
            output = list()
            output.append('candidate: %s' % history[0])
            output.append('')

            for i in xrange(1, len(history)):
                output.append('history[%d]: %s' % (i, history[i]))
            output.append('')

            for i in xrange(1, len(dup)):
                output.append('dup[%d]: %s' % (i, dup[i]))
            output.append('')

            output.append('cont_seq: %s' % cont_seq)
            output.append('')

            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % candidate)
            output.append('')
        else:
            output = dict()
            output['period'] = '%d' % target_period
            output['numbers'] = candidate

        return output

if __name__ == '__main__':
    p = HeuristicPredictor()
    print '\n'.join(p.predict(debug=True))
