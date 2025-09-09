from flask import Flask
from .extensions import db, migrate, login_manager
from .config import Config
from .auth import auth_bp
from .main import main_bp

def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_object or Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # simple route
    @app.route("/health")
    def health():
        return {"status":"ok"}

    return app