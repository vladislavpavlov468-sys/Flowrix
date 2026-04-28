import os
import uuid

from PIL import Image
from flask import current_app
from sqlalchemy import or_

from models import Product


THUMBNAIL_SIZE = (800, 800)


def get_products_filtered(search: str = "", category: str = "") -> list:
    query = Product.query.filter_by(is_available=True)

    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Product.name.ilike(pattern),
                Product.description.ilike(pattern),
            )
        )

    if category:
        query = query.filter_by(category=category)

    return query.order_by(Product.created_at.desc()).all()


def get_all_categories() -> list[str]:
    rows = (
        Product.query
        .filter(Product.is_available.is_(True), Product.category.isnot(None))
        .with_entities(Product.category)
        .distinct()
        .all()
    )
    return sorted(row[0] for row in rows if row[0])


def save_product_image(file) -> str | None:
    if not file or not file.filename:
        return None

    extension = file.filename.rsplit(".", 1)[-1].lower()
    allowed = current_app.config.get("ALLOWED_EXTENSIONS", set())

    if extension not in allowed:
        return None

    filename = f"{uuid.uuid4().hex}.{extension}"
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)

    try:
        image = Image.open(file)
        image.thumbnail(THUMBNAIL_SIZE)
        image.save(filepath)
    except Exception:
        return None

    return filename


def delete_product_image(filename: str) -> None:
    if not filename:
        return

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    filepath = os.path.join(upload_folder, filename)

    if os.path.exists(filepath):
        os.remove(filepath)
