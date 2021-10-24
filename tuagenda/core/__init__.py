from flask import Flask
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

from Agendas import views
from . import database

