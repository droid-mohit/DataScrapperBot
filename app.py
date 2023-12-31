from flask import Flask
from flask_migrate import Migrate

from env_vars import PG_DB_USERNAME, PG_DB_PASSWORD, PG_DB_NAME, PG_DB_HOSTNAME, FLAKS_APP_SECRET_KEY
from persistance.models import db
from routes.app_router import app_blueprint
from routes.google_router import google_blueprint
from routes.slack_router import slack_blueprint

app = Flask(__name__)
app.secret_key = FLAKS_APP_SECRET_KEY

# Configure all the blueprints
app.register_blueprint(app_blueprint, url_prefix='/app')
app.register_blueprint(slack_blueprint, url_prefix='/slack')
app.register_blueprint(google_blueprint, url_prefix='/google')

# Configure postgres db
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{PG_DB_USERNAME}:{PG_DB_PASSWORD}@{PG_DB_HOSTNAME}/{PG_DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
