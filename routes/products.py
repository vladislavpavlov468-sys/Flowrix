from flask import Blueprint, render_template

products_bp = Blueprint("products", __name__)


@products_bp.route("/")
def index():
    return render_template("products/index.html", products=[])
