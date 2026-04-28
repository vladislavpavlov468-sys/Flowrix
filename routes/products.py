from flask import Blueprint, abort, render_template, request, send_from_directory, current_app
from models import Product
from services.product_service import get_all_categories, get_products_filtered

products_bp = Blueprint("products", __name__)


@products_bp.route("/")
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

    return render_template("products/detail.html", product=product)


@products_bp.route("/uploads/<path:filename>")
def uploaded_file(filename: str):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
