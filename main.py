import os
import shutil
from flask import Flask, render_template
from config import Config
from extensions import db, login_manager
from routes.auth import auth_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.admin import admin_bp
from routes.api import api_bp


def create_app(config_class: object = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    _register_error_handlers(app)
    _register_filters(app)

    @app.before_request
    def initialize_on_first_run():
        if not getattr(app, "_database_initialized", False):
            try:
                os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
                if os.environ.get("VERCEL") and not os.environ.get("DATABASE_URL"):
                    repo_db = os.path.join(Config.BASE_DIR, 'flowrix.db')
                    target_db = '/tmp/flowrix.db'
                    if os.path.exists(repo_db) and not os.path.exists(target_db):
                        shutil.copy2(repo_db, target_db)
                
                import models
                db.create_all()
                app._database_initialized = True
            except Exception as e:
                print(f"Lazy initialization error: {e}")

    @app.before_request
    def check_admin():
        _ensure_admin()

    return app



def _ensure_admin():
    from models import User
    try:
        first_user = User.query.order_by(User.id.asc()).first()
        if first_user and first_user.role != "admin":
            first_user.role = "admin"
            db.session.commit()
            print(f"User {first_user.username} promoted to Admin")
    except Exception as e:
        print(f"Admin promotion error: {e}")
        db.session.rollback()


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500


def _register_filters(app: Flask) -> None:
    @app.template_filter("nl2br")
    def nl2br_filter(s):
        if not s:
            return ""
        from markupsafe import Markup
        if "<br>" in s or "<p>" in s:
            return Markup(s)
        return Markup(s.replace("\n", "<br>\n"))


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
