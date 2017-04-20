# pylint: disable=missing-docstring

import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def get_path_to_file(*fileargs):
    return os.path.join(APP_ROOT, *fileargs)
