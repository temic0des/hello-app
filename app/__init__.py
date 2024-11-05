from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_uuid import FlaskUUID

load_dotenv()

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config.from_object(Config)
db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)
migrate.init_app(app, db)

flask_uuid = FlaskUUID()
flask_uuid.init_app(app=app)

from app import routes, models