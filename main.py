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
        
        # Vercel: copy existing DB from repo to /tmp if it's not there
        if os.environ.get("VERCEL"):
            import shutil
            repo_db = os.path.join(Config.BASE_DIR, 'flowrix.db')
            target_db = '/tmp/flowrix.db'
            if os.path.exists(repo_db) and not os.path.exists(target_db):
                try:
                    shutil.copy2(repo_db, target_db)
                except Exception:
                    pass

        try:
            db.create_all()
            _ensure_admin()
        except Exception:
            pass

    return app


def _ensure_admin():
    """Назначает роль администратора первому пользователю или по списку."""
    from models import User
    # Можно добавить ваш email здесь:
    admin_emails = ["admin@flowrix.ru", "vlad@example.com"] 
    
    # Делаем всех из списка админами
    users = User.query.filter(User.email.in_(admin_emails)).all()
    for u in users:
        u.role = "admin"
    
    # Или просто сделаем самого первого зарегистрированного пользователя админом
    first_user = User.query.first()
    if first_user:
        first_user.role = "admin"
        
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
