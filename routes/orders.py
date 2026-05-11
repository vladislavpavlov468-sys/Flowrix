from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user, login_required

from services.order_service import (
    add_item_to_cart, checkout_cart, get_user_orders
)

orders_bp = Blueprint("orders", __name__, url_prefix="/orders")


@orders_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id: int):
    quantity = int(request.form.get("quantity", 1))
    add_item_to_cart(current_user, product_id, quantity)
    return redirect(url_for("products.detail", product_id=product_id))


@orders_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    if request.method == "POST":
        # Save cart total in session for payment page display
        cart = current_user.active_cart
        if cart:
            session["pending_total"] = "%.0f" % cart.cart_total

        success = checkout_cart(current_user)
        if success:
            return redirect(url_for("orders.payment"))
        return redirect(url_for("products.index"))
    if not current_user.active_cart or current_user.active_cart.items_count == 0:
        return redirect(url_for("products.index"))

    return render_template("orders/checkout.html", cart=current_user.active_cart)


@orders_bp.route("/payment")
@login_required
def payment():
    total = session.pop("pending_total", None)
    orders = get_user_orders(current_user)
    order_id = orders[0].id if orders else None
    return render_template("orders/payment.html", total=total, order_id=order_id)


@orders_bp.route("/history")
@login_required
def history():
    orders = get_user_orders(current_user)
    return render_template("orders/history.html", orders=orders)
