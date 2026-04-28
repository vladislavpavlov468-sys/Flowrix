from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from services.order_service import add_item_to_cart, checkout_cart, get_user_orders

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id: int):
    quantity = int(request.form.get("quantity", 1))
    add_item_to_cart(current_user, product_id, quantity)
    return redirect(url_for("products.detail", product_id=product_id))


@orders_bp.route("/checkout", methods=["POST"])
@login_required
def checkout():
    success = checkout_cart(current_user)
    if success:
        return redirect(url_for("orders.history"))
    return redirect(url_for("products.index"))


@orders_bp.route("/history")
@login_required
def history():
    orders = get_user_orders(current_user)
    return render_template("orders/history.html", orders=orders)
