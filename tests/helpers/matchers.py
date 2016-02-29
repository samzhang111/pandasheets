import numpy as np

class numpy_array_equal(object):
    def __init__(self, actual):
        self.actual = actual

    def _match(self, expected):
        try:
            np.testing.assert_array_equal(self.actual, expected)
            return True
        except AssertionError:
            return False

    def _description(self, expected):
        return "array {} to equal {}".format(expected, self.actual)