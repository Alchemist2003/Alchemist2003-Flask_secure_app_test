from flask import Flask, redirect
from app.config import Config
from app.extensions import db, migrate, jwt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ============================
    # ROOT ROUTE (redirect to login)
    # ============================
    @app.route("/")
    def index():
        return redirect("/login")

    # ============================
    # API BLUEPRINTS (JSON APIs)
    # ============================
    from app.auth.routes import auth_bp
    from app.notes.routes import notes_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    # ============================
    # FRONTEND BLUEPRINTS (HTML)
    # ============================
    from app.auth.views import auth_views
    from app.notes.views import notes_views

    app.register_blueprint(auth_views)
    app.register_blueprint(notes_views)

    return app
