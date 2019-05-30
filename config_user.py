import os

DEBUG = False

SECRET_KEY = os.urandom(24)


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:roots@localhost/new_translate?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False