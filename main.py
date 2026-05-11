import os
import markupsafe
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

    try:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    except Exception:
        pass

    with app.app_context():
        import models
        try:
            db.create_all()
            _seed_db()
        except Exception:
            pass

    return app


def _seed_db():
    from models import Product
    if Product.query.first() is None:
        p = Product(
            name="Демонстрационный товар",
            description="Этот товар был создан автоматически для проверки работы базы данных на Vercel.",
            price=1500,
            category="Декор",
            is_available=True
        )
        db.session.add(p)
        db.session.commit()


def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500


def _register_filters(app: Flask) -> None:
    @app.template_filter('nl2br')
    def nl2br_filter(value):
        if not value:
            return ''
        escaped = markupsafe.escape(value)
        return markupsafe.Markup(str(escaped).replace('\n', '<br>\n'))


app = create_app()


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(debug=True)
