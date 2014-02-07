import os
from flask import Flask


# initialization
app = Flask(__name__)
app.config.update(
 DEBUG = True,
)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views