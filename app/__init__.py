from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from app.configs.connection import DbConnectionHandler as dbc

app = Flask(__name__)

from app.controllers import default

