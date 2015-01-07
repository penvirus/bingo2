from predictor import Predictor

class DeltaPredictor(Predictor):
    def get_name(self):
        return 'Delta Predictor'

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1

        try:
            prev_numbers = self._all_data[target_period - 1]['numbers']
        except KeyError:
            return self.no_comment(target_period, debug)

        candidate = list()
        for num in prev_numbers:
            if num + 1 not in prev_numbers and num + 2 in prev_numbers:
                candidate.append(num + 1)

        if debug:
            output = list()
            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % candidate)
            output.append('')
        else:
            output = dict()
            output['period'] = target_period
            output['numbers'] = candidate
        return output

if __name__ == '__main__':
    p = DeltaPredictor()
    print '\n'.join(p.predict(debug=True))
