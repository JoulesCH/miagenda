from flask import Flask
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
DATABASE_URL = os.getenv('DATABASE_URL')

if 'postgresql' not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace('postgres', 'postgresql')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

from Agendas import views
from . import database

