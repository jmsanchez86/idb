#!/usr/bin/env python3
# pylint: disable=missing-docstring
# pylint: disable=invalid-sequence-index
# pylint: disable=fixme

import logging
from flask import Flask, Blueprint
from typing import List, Tuple, Any


# TODO: fix when mypy bug resolved and remove pylint message
# there is currently a mypy bug that won't let us use ModuleType here for
# config. https://github.com/python/mypy/issues/1498
def create_app(config: Any,
               route_blueprints: List[Tuple[Blueprint, dict]],
               debug: bool=False, testing: bool=False,
               config_overrides: Any=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(err):
        # pylint: disable=unused-variable
        return """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(err), 500

    for blueprint in route_blueprints:
        app.register_blueprint(blueprint[0], **blueprint[1])
    return app
