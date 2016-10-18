from flask import Flask

app = Flask(__name__, static_folder = 'static', static_url_path='')
app.config.from_object('config')

from app import index
from app import inventory
from app import sale
from app import transaction
from app import category
from app import supplier