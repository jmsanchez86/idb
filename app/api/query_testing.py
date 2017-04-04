# pylint: disable=missing-docstring
from app.api.main import API_SERVICE
from app.api.models import *

ctx = API_SERVICE.app_context()
ctx.push()
