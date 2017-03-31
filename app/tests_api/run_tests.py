# pylint: disable=missing-docstring

import unittest
from unittest.runner import TextTestRunner
from io import StringIO

from app.tests import ModelTests
from app.tests_api.TestResultWithSuccess import TestResultWithSuccess

def run_tests():
    out_stream = StringIO()
    runner = TextTestRunner(resultclass=TestResultWithSuccess, stream=out_stream)
    result = runner.run(unittest.makeSuite(ModelTests))
    return (result, out_stream)
