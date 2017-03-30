# pylint: disable=missing-docstring

import flask

TEST_BP = flask.Blueprint('test', __name__)

@TEST_BP.route('/')
def run_tests():
    return flask.json.jsonify({"result": "success"})
