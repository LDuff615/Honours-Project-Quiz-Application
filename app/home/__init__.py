# This file will be used to create and initialize the 'hpApp' blueprint
from flask import Blueprint

# hpApp - a blueprint object
hpApp = Blueprint('hpApp', __name__)

# Importing the views.py file from 'app' directory
from . import views