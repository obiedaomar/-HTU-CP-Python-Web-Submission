from mongoengine import *
from datetime import datetime


class Cart(Document):
    owner_id = StringField()