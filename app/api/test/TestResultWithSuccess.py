# pylint: disable=missing-docstring

import unittest


class TestResultWithSuccess(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super(TestResultWithSuccess, self).__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super(TestResultWithSuccess, self).addSuccess(test)
        self.successes.append(test)
