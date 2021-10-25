from core import app, database
#from core.database import db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, database.db, directory='migrations_joules/')
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()