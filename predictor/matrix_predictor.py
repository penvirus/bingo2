import os
import copy
import cPickle as pickle
from operator import itemgetter
from matrix import Matrix

from predictor import Predictor
from common.constant import COOKED_DATA_DIR

def print_bitmap(bitmap):
    for i in bitmap:
        for k in i:
            if k:
                print '1',
            else:
                print '0',
        print

class MatrixPredictor(Predictor):
    def __init__(self):
        super(MatrixPredictor, self).__init__()

        self._height = 3
        self._width = 3
        self._target = 3

    def set_dimension(self, width, height):
        self._width = width
        self._height = height

    def set_target(self, target):
        self._target = target

    def get_name(self):
        return 'Matrix Predictor  (w%d x h%d)' % (self._width, self._height)

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        if target_period is None:
            target_period = self.get_max_period() + 1
        if dataset_begin is None:
            dataset_begin = self.get_min_period()
        if dataset_end is None:
            dataset_end = self.get_max_period()
        if dataset_begin > dataset_end:
            raise ValueError()

        training_dataset = os.path.join(COOKED_DATA_DIR, 'matrix_predictor_%d_%d' % (self._width, self._height))
        try:
            with open(training_dataset, 'r') as ff:
                training_data = pickle.load(ff)
        except IOError:
            training_data = dict()

        if target_period - 1 not in training_data:
            bitmap = list()
            for period in xrange(dataset_end, dataset_begin - 1, -1):
                bit = [False] * 80
                for num in self._all_data[period]['numbers']:
                    bit[num - 1] = True
                bitmap.append(tuple(bit))
            bitmap = tuple(bitmap)

            for y in xrange(len(bitmap) - 1 - self._height + 1, -1, -1):
                period = dataset_end - y
                if period not in training_data:
                    if period - 1 in training_data:
                        training_data[period] = copy.deepcopy(training_data[period - 1])
                    else:
                        training_data[period] = dict()

                    for x in xrange(80 - 1 - self._width + 1, -1, -1):
                        m = Matrix.create_from_bitmap(self._width, self._height, bitmap, x, y)
                        if m in training_data[period]:
                            training_data[period][m] += 1
                        else:
                            training_data[period][m] = 1

            with open(training_dataset, 'w') as ff:
                pickle.dump(training_data, ff, pickle.HIGHEST_PROTOCOL)

        sorted_matrices = sorted(training_data[target_period - 1].items(), key=itemgetter(1), reverse=True)

        latest_bitmap = list()
        for period in xrange(target_period - 1, target_period - 1 - self._height - 1, -1):
            bm = [False] * 80
            for num in self._all_data[period]['numbers']:
                bm[num - 1] = True
            latest_bitmap.append(tuple(bm))
        latest_bitmap = tuple(latest_bitmap)

        candidate = list()
        adopted_matrix = list()
        adopted_sub_matrix = set()
        for m,f in sorted_matrices:
            sub_matrix = Matrix.create_sub_matrix(m)
            if m.is_qualified() and sub_matrix not in adopted_sub_matrix:
                candidate += m.findall(latest_bitmap)
                candidate = list(set(candidate))
                adopted_matrix.append(m)
                adopted_sub_matrix.add(sub_matrix)
            if len(candidate) >= self._target:
                break

        if debug:
            output = list()
            #rank = 1
            #for m in sorted_matrices:
            #    if m['matrix'].is_qualified():
            #        output.append('top %d: ' % rank)
            #        output.append(str(m['matrix']))
            #        output.append('')
            #        rank += 1

            #        if rank == 10:
            #            break

            output.append('adopted matrice:')
            for m in adopted_matrix:
                output.append(str(m))
                output.append('')
            output.append('predicted period: %d' % target_period)
            output.append('prediction: %s' % sorted(candidate))
        else:
            output = dict()
            output['period'] = '%d' % target_period
            output['numbers'] = sorted(candidate)

        return output

if __name__ == '__main__':
    p = MatrixPredictor()
    print '\n'.join(p.predict(debug=True))
