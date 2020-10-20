"""Flask Application"""

# load libaries
from flask import Flask, jsonify
from mongoengine import connect
import sys

# load modules
from src.endpoints.cart import cart_blueprint
from src.endpoints.product import product_blueprint
from src.endpoints.user import user_blueprint
from src.models import *

# init Flask app
app = Flask(__name__)

# connect to the DB
connect('mysouq', host='localhost', port=27017, username='root',
        password='example', authentication_source='admin')

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(cart_blueprint, url_prefix="/api/v1/cart")
app.register_blueprint(product_blueprint, url_prefix="/api/v1/product")
app.register_blueprint(user_blueprint, url_prefix="/api/v1/user")

# app.register_blueprint(tasklist, url_prefix="/api/v1/tasklist")
# app.register_blueprint(task, url_prefix="/api/v1/task")
# app.register_blueprint(user, url_prefix="/api/v1/user")
