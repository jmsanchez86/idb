#!/usr/bin/env python3
# pylint: disable=missing-docstring

import app
import config

FLASK_APP = app.create_app(config)

if __name__ == "__main__":
    FLASK_APP.run(host='127.0.0.1', port=8080, debug=True)
