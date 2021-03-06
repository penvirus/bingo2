from crawler.num_extractor import load

class Predictor(object):
    def __init__(self):
        self._all_data = load()

    def get_max_period(self):
        return max(self._all_data.keys())

    def get_min_period(self):
        return min(self._all_data.keys())

    def is_configurable(self):
        return False

    def set_target(self, target):
        pass

    def no_comment(self, target_period, debug):
        if debug:
            output = list()
            output.append('period: %s' % target_period)
            output.append('candidate: no comment')
        else:
            output = dict()
            output['period'] = target_period
            output['numbers'] = list()
        return output

    def get_name(self):
        """
            This function should return a predictor name for displaying purpose.
        """
        raise NotImplementedError('Not Implemented')

    def predict(self, target_period=None, dataset_begin=None, dataset_end=None, debug=False):
        """
            If target_period is not None, it will be an integer to indicate the target period.
            Otherwise, it should try to predict the nearest future period.

            dataset_begin and dataset_end indicate a period interval for the training data.
            If dataset_begin is not set, it should find the minimum period.
            If dataset_end is not set, it should find the maximum period.
            If dataset_begin > dataset_end, it should raise a ValueError.
            Note: not all predictors reference the values. (i.e. some predictor may not need long-term training data)
            Note: target_period and the dataset interval are independent. (i.e. use relatively new training data to predict relatively old period is allowed)

            If debug flag is on, the function should return an array of verbose messages.
            Otherwise, the function should return a dictionary in a pre-defined manner.
        """
        raise NotImplementedError('Not Implemented')
