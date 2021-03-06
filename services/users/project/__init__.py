# services/users/project/__init__.py
import os  # nuevo
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # nuevo
# instanciado la app
app = Flask(__name__)

# establecer configuraicon
app_settings = os.getenv('APP_SETTINGS')   # Nuevo
app.config.from_object(app_settings)       # Nuevo

# instanciando la db
db = SQLAlchemy(app)  # nuevo


def create_app(script_info=None):
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    db.init_app(app)
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
