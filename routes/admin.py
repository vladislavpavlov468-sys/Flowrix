from functools import wraps
from flask import (
    Blueprint, abort, flash, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from models import Order, Product, ContactMessage
from services.admin_service import (
    create_product,
    get_all_orders,
    get_all_products,
    get_dashboard_stats,
    toggle_product_availability,
    update_order_status,
    update_product,
    delete_product
)
from services.product_service import delete_product_image, save_product_image

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    stats = get_dashboard_stats()
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route("/products")
@login_required
@admin_required
def products():
    items = get_all_products()
    return render_template("admin/products.html", products=items)


@admin_bp.route("/products/new", methods=["GET", "POST"])
@login_required
@admin_required
def product_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0").strip()
        category = request.form.get("category", "").strip()
        image_file = request.files.get("image")

        if not name or not price:
            flash("Название и цена обязательны.", "danger")
            return render_template("admin/product_form.html", product=None)

        image_filename = save_product_image(image_file) if image_file else None
        extra_images = request.files.getlist("extra_images")
        extra_filenames = [save_product_image(img) for img in extra_images if img]
        
        create_product(
            name,
            description,
            float(price),
            category,
            image_filename,
            extra_filenames)
        flash(f"Товар «{name}» добавлен.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=None)


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def product_edit(product_id: int):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "0").strip()
        category = request.form.get("category", "").strip()
        image_file = request.files.get("image")

        if not name or not price:
            flash("Название и цена обязательны.", "danger")
            return render_template("admin/product_form.html", product=product)

        new_image = None
        if image_file and image_file.filename:
            if product.image_filename:
                delete_product_image(product.image_filename)
            new_image = save_product_image(image_file)

        update_product(
            product,
            name,
            description,
            float(price),
            category,
            new_image)
        
    
        extra_images = request.files.getlist("extra_images")
        from models import ProductImage
        from extensions import db
        for img in extra_images:
            if img:
                fname = save_product_image(img)
                new_img_obj = ProductImage(product_id=product.id, filename=fname)
                db.session.add(new_img_obj)
        db.session.commit()
        flash(f"Товар «{name}» обновлён.", "success")
        return redirect(url_for("admin.products"))

    return render_template("admin/product_form.html", product=product)


@admin_bp.route("/products/<int:product_id>/toggle", methods=["POST"])
@login_required
@admin_required
def product_toggle(product_id: int):
    product = Product.query.get_or_404(product_id)
    toggle_product_availability(product)
    state = "включён" if product.is_available else "скрыт"
    flash(f"Товар «{product.name}» {state}.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
@admin_required
def product_delete(product_id: int):
    product = Product.query.get_or_404(product_id)
    name = product.name
    delete_product(product)
    flash(f"Товар «{name}» удалён.", "success")
    return redirect(url_for("admin.products"))


@admin_bp.route("/orders")
@login_required
@admin_required
def orders():
    all_orders = get_all_orders()
    return render_template("admin/orders.html", orders=all_orders)


@admin_bp.route("/orders/<int:order_id>/status", methods=["POST"])
@login_required
@admin_required
def order_status(order_id: int):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get("status", "")
    if update_order_status(order, new_status):
        flash("Статус заказа обновлён.", "success")
    else:
        flash("Недопустимый статус.", "danger")
    return redirect(url_for("admin.orders"))


@admin_bp.route("/messages")
@login_required
@admin_required
def messages():
    all_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template("admin/messages.html", messages=all_messages)


@admin_bp.route("/messages/<int:message_id>/read", methods=["POST"])
@login_required
@admin_required
def message_read(message_id: int):
    from extensions import db
    msg = ContactMessage.query.get_or_404(message_id)
    msg.status = "read"
    db.session.commit()
    flash("Сообщение помечено как прочитанное.", "success")
    return redirect(url_for("admin.messages"))
