from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from services.order_service import get_cart_data, remove_item_from_cart

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/cart", methods=["GET"])
@login_required
def get_cart():
    return jsonify(get_cart_data(current_user))

    return jsonify({"error": "Item not found"}), 404


@api_bp.route("/cart/<int:item_id>", methods=["PATCH"])
@login_required
def update_cart_item_quantity(item_id: int):
    from flask import request
    data = request.get_json()
    delta = data.get("delta", 0)

    from services.order_service import update_item_quantity
    success = update_item_quantity(current_user, item_id, delta)
    if success:
        return jsonify(get_cart_data(current_user))
    return jsonify({"error": "Item not found"}), 404


@api_bp.route("/cart", methods=["DELETE"])
@login_required
def clear_user_cart():
    from services.order_service import clear_cart
    clear_cart(current_user)
    return jsonify(get_cart_data(current_user))
