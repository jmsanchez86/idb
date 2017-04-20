# pylint: disable=missing-docstring

import unittest
from unittest.runner import TextTestRunner
from io import StringIO

from app.api.test.tests import DatabaseIntegrityTests, ModelTests, RouteTests,\
                               RouteUtilityTests, SearchTests,\
                               SearchResultClassTests
from app.api.test.TestResultWithSuccess import TestResultWithSuccess


def run_tests():
    out_stream = StringIO()
    runner = TextTestRunner(
        resultclass=TestResultWithSuccess, stream=out_stream)
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(DatabaseIntegrityTests))
    suite.addTest(unittest.makeSuite(ModelTests))
    suite.addTest(unittest.makeSuite(RouteTests))
    suite.addTest(unittest.makeSuite(RouteUtilityTests))
    suite.addTest(unittest.makeSuite(SearchTests))
    suite.addTest(unittest.makeSuite(SearchResultClassTests))
    result = runner.run(suite)
    return (result, out_stream)
