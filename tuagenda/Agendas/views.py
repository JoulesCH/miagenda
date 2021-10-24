from core import app
from . import resources

app.route('/')(resources.index)