#!/usr/bin/env python3
# pylint: disable=missing-docstring


import config as cfg

from app.create_app import create_app
from app.site import routes

SITE_SERVICE = create_app(cfg, [(routes.SITE_BP, {})])
if __name__ == "__main__":
    SITE_SERVICE.run(host='127.0.0.1', port=8080, debug=True)
