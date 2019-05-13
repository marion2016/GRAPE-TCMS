from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from celery import Celery

from hobbit_core.flask_hobbit import HobbitManager

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
celery = Celery()
hobbit = HobbitManager()
