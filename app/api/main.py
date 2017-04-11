#!/usr/bin/env python3
# pylint: disable=missing-docstring

# pylint can't find flask_cors for some reason
# pylint: disable=import-error

import config as cfg

from app.api.models import init_db
from app.create_app import create_app
from app.api import routes
from app.api.test import routes as test_routes
from flask_cors import CORS


API_SERVICE = create_app(cfg, [(routes.API_BP, {}),
                               (test_routes.TEST_BP, {"url_prefix": "/test"})])
CORS(API_SERVICE)
init_db(API_SERVICE)
if __name__ == "__main__":
    API_SERVICE.run(host='127.0.0.1', port=8080, debug=True)
