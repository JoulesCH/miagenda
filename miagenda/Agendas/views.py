from core import app
from . import resources

app.route('/')(resources.index)

app.route('/login')(resources.login)

app.route('/signup')(resources.signup)

app.route('/acercade')(resources.about)

app.route('/guia')(resources.guide)

app.route('/creditos')(resources.credits)