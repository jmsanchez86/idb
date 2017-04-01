# pylint: disable=missing-docstring

import flask

from app.api.test.run_tests import run_tests

TEST_BP = flask.Blueprint('test', __name__)


@TEST_BP.route('/')
def get_test_results():
    result, out_stream = run_tests()
    successes = [t.id() for t in result.successes]
    failures = [{"id": t[0].id(), "err": t[1]} for t in result.failures]
    errors = [{"id": t[0].id(), "err": t[1]} for t in result.errors]
    return flask.json.jsonify(
        {
            "total_tests": result.testsRun,
            "successes": successes,
            "failures": failures,
            "errors": errors,
            "output": out_stream.getvalue()
        })
