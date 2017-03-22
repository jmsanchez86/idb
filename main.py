#!/usr/bin/env python3
# pylint: disable=missing-docstring

import app
import config


# This is only used when running locally. When running live, gunicorn runs
# the application.
def main():
    flask_app = app.create_app(config)
    flask_app.run(host='127.0.0.1', port=8090, debug=True)

if __name__ == '__main__':
    main()
