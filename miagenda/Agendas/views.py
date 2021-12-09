"""
Registra las vistas de la aplicación (arquitectura vista controlador)
"""
from core import app
from . import resources
  

app.route('/')(resources.index)

app.route('/login', methods=["POST", "GET"])(resources.login)

app.route('/signup', methods=["POST", "GET"])(resources.signup)

app.route('/logout')(resources.logout)

app.route('/acercade')(resources.about)

app.route('/guia')(resources.guide)

app.route('/miagenda')(resources.mi_agenda)

app.route('/creditos')(resources.credits)

app.route('/agenda/<id>')(resources.agenda)

app.route('/gestionar_agenda')(resources.gestionar_agenda)