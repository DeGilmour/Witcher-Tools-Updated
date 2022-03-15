import os
from config_file import SECRET_KEY

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = SECRET_KEY

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'storage.db')