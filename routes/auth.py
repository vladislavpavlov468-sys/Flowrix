from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def _validate_registration(
    username: str, email: str, password: str, confirm: str
) -> list[str]:
    errors = []

    if not all([username, email, password, confirm]):
        errors.append("Все поля обязательны для заполнения.")
        return errors

    if len(username) < 3:
        errors.append("Имя пользователя должно содержать минимум 3 символа.")

    if len(password) < 6:
        errors.append("Пароль должен содержать минимум 6 символов.")

    if password != confirm:
        errors.append("Пароли не совпадают.")

    if not errors:
        if User.query.filter_by(username=username).first():
            errors.append(f"Имя пользователя «{username}» уже занято.")
        if User.query.filter_by(email=email).first():
            errors.append("Этот email уже зарегистрирован.")

    return errors


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("products.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        errors = _validate_registration(username, email, password, confirm)

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template(
                "auth/register.html",
                username=username,
                email=email,
            )

        new_user = User(username=username, email=email, role="client")
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash("Ошибка при создании аккаунта. Попробуйте позже.", "danger")
            return render_template("auth/register.html")

        login_user(new_user)
        flash(f"Добро пожаловать, {new_user.username}!", "success")
        return redirect(url_for("products.index"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("products.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = request.form.get("remember") == "on"

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Неверный email или пароль.", "danger")
            return render_template("auth/login.html", email=email)

        login_user(user, remember=remember)
        flash(f"С возвращением, {user.username}!", "success")

        next_page = request.args.get("next")
        return redirect(next_page or url_for("products.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for("auth.login"))
