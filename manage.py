from app import app, manager
from flask.ext.migrate import MigrateCommand

manager.add_command('db', MigrateCommand)

app.debug = True
manager.run()