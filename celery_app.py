from celery import Celery
from flask import Flask
from flask_migrate import Migrate

from env_vars import PG_DB_USERNAME, PG_DB_PASSWORD, PG_DB_NAME, PG_DB_HOSTNAME
from persistance.models import db

app = Flask(__name__)

# Configure postgres db
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_DB_USERNAME}:{PG_DB_PASSWORD}@{PG_DB_HOSTNAME}/{PG_DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(
    app.name,  # Replace with your Flask app name
    broker=app.config['CELERY_BROKER_URL'],  # Use Redis as the message broker
    include=['jobs.tasks']
)
celery.conf.update(app.config)