"""
Se almacena la instancia de la base de datos
"""
##### Installed packages
from flask_sqlalchemy import SQLAlchemy
##### Local
from . import app

##### db config
db = SQLAlchemy(app)

from Agendas.models import *