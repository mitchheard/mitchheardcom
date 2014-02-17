import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate

# initialization
app = Flask(__name__)
app.config.update(
 DEBUG = True,
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mheard:12345@localhost/mitchheardcom'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config.from_object('config')

db = SQLAlchemy()
db.app = app
db.init_app(app)

migrate = Migrate(app, db)
manager = Manager(app)

from app import views
from app import models