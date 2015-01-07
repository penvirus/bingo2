from operator import itemgetter

from predictor import Predictor

def my_pprint(it, dest):
    i = 1
    buf = list()
    for num,prob in it:
        buf.append('%02d: %.6f' % (num, prob))
        i += 1

        if i == 5:
            dest.append(''.join(buf))
            i = 1
            buf = list()
        else:
            buf.append('%8s' % ' ')

    if buf:
        dest.append(''.join(buf))

class PureProbPredictor(Predictor):
    def get_name(self):
        return 'Pure Probability Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1
        if dataset_begin is None:
            dataset_begin = self.get_min_period()
        if dataset_end is None:
            dataset_end = self.get_max_period()
        if dataset_begin > dataset_end:
            raise ValueError()

        matrix = 0
        counts = dict()
        for num in xrange(1, 81):
            counts[num] = 0

        for period in xrange(dataset_begin, dataset_end + 1):
            if period in self._all_data:
                matrix += 1
                for num in self._all_data[period]['numbers']:
                    counts[num] += 1

        prob = dict()
        for num in xrange(1, 81):
            prob[num] = float(counts[num]) / matrix

        result = sorted(prob.items(), key=itemgetter(1), reverse=True)

        top8 = result[:8]
        mid8 = result[36:44]
        bot8 = result[-8:]

        if debug:
            output = list()

            output.append('raw prob:')
            my_pprint(result, output)
            output.append('')

            output.append('top 8:')
            my_pprint(top8, output)
            output.append('')

            output.append('mid 8:')
            my_pprint(mid8, output)
            output.append('')

            output.append('bot 8:')
            my_pprint(bot8, output)
            output.append('')

            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % sorted([num for num,_ in bot8]))
            output.append('')
        else:
            output = dict()
            output['period'] = '%d' % target_period
            output['numbers'] = sorted([num for num,_ in bot8])
            output['raw_prob'] = dict()
            for num,prob in result:
                output['raw_prob'][num] = prob

        return output

if __name__ == '__main__':
    p = PureProbPredictor()
    print '\n'.join(p.predict(debug=True))
