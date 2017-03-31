#!/usr/bin/env python3
# pylint: disable=missing-docstring

import config as cfg

from app.create_app import create_app
from app.api import routes
from app.api import test


API_SERVICE = create_app(cfg, [(routes.API_BP, {}),
                               (test.routes.TEST_BP, {"url_prefix": "/test"})])
if __name__ == "__main__":
    API_SERVICE.run(host='127.0.0.1', port=8080, debug=True)
