from flask import (
    Blueprint, abort, current_app, render_template, request,
    send_from_directory
)

from models import Product
from services.product_service import get_all_categories, get_products_filtered

products_bp = Blueprint("products", __name__)


@products_bp.route("/")
def home():
    featured = Product.query.filter_by(is_available=True).order_by(
        Product.created_at.desc()
    ).limit(4).all()
    return render_template("home.html", featured=featured)


@products_bp.route("/catalog")
def index():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    products = get_products_filtered(search=search, category=category)
    categories = get_all_categories()

    return render_template(
        "products/index.html",
        products=products,
        categories=categories,
        search=search,
        active_category=category,
    )


@products_bp.route("/products/<int:product_id>")
def detail(product_id: int):
    product = Product.query.get_or_404(product_id)

    if not product.is_available:
        abort(404)

    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id,
        Product.is_available.is_(True),
    ).limit(3).all()

    return render_template("products/detail.html",
                           product=product, related=related)


@products_bp.route("/delivery")
def delivery():
    return render_template("pages/delivery.html")


@products_bp.route("/contacts")
def contacts():
    return render_template("pages/contacts.html")


@products_bp.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
