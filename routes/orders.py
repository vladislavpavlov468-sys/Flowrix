from flask import Blueprint, redirect, url_for
from flask_login import login_required

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    return redirect(url_for("products.index"))


@orders_bp.route("/history")
@login_required
def history():
    return redirect(url_for("products.index"))
