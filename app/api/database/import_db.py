"""
Import the json data into our real postgres database
"""

import os
from app.project_root import APP_ROOT
from app.api import models
from app.api.main import API_SERVICE
from app.scraping.importer import Importer

def run_import():
    """
    imports the json data into real postgres database
    """
    with API_SERVICE.app_context():
        imp = Importer(os.path.join(APP_ROOT, "scraping", "data"), models.db)
        imp.run()


if __name__ == "__main__":
    run_import()
