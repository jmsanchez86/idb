# pylint: disable=missing-docstring

import logging

from flask import Flask, render_template

def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Add a default root route.
    @app.route("/")
    def index():
        # pylint: disable=unused-variable
        return render_template('base.html')

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

    return app
