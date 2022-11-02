from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.configs.connection import DbConnectionHandler as dbc
from flask_migrate import Migrate
from app.configs.base import Base as db

app = Flask(__name__)
from app.controllers import default
