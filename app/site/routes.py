# pylint: disable=missing-docstring
from flask import Blueprint, render_template

SITE_BP = Blueprint('site', __name__)

@SITE_BP.route('/')
def index():
    return render_template('base.html')
