#!/usr/bin/env python3
# pylint: disable=missing-docstring

import app
import config

FLASK_APP = app.create_app(config)
FLASK_APP.run(host='127.0.0.1', port=8090, debug=True)
