from extensions import db
from models import Order, Product, User, ContactMessage, OrderItem


def get_dashboard_stats() -> dict:
    total_products = Product.query.filter_by(is_available=True).count()
    total_orders = Order.query.filter(Order.status != "new").count()
    total_users = User.query.filter_by(role="client").count()
    pending_orders = Order.query.filter_by(status="in_progress").count()
    new_messages = ContactMessage.query.filter_by(status="new").count()

    return {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_users": total_users,
        "pending_orders": pending_orders,
        "new_messages": new_messages,
    }


def get_all_orders() -> list[Order]:
    return (
        Order.query
        .filter(Order.status != "new")
        .order_by(Order.created_at.desc())
        .all()
    )


def get_all_products() -> list[Product]:
    return Product.query.order_by(Product.created_at.desc()).all()


def create_product(name: str, description: str, price: float,
                   category: str, image_filename: str | None,
                   extra_filenames: list[str] | None = None) -> Product:
    from models import ProductImage
    product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        image_filename=image_filename,
        is_available=True,
    )
    db.session.add(product)
    db.session.flush() 

    if extra_filenames:
        for fname in extra_filenames:
            img_obj = ProductImage(product_id=product.id, filename=fname)
            db.session.add(img_obj)

    db.session.commit()
    return product


def update_product(product: Product, name: str, description: str,
                   price: float, category: str,
                   image_filename: str | None) -> None:
    product.name = name
    product.description = description
    product.price = price
    product.category = category
    if image_filename:
        product.image_filename = image_filename
    db.session.commit()


def toggle_product_availability(product: Product) -> None:
    product.is_available = not product.is_available
    db.session.commit()


def delete_product(product: Product) -> None:
    from services.product_service import delete_product_image
    if product.image_filename:
        delete_product_image(product.image_filename)

    OrderItem.query.filter_by(product_id=product.id).delete()

    db.session.delete(product)
    db.session.commit()


def update_order_status(order: Order, status: str) -> bool:
    allowed = {"in_progress", "shipped", "delivered", "cancelled"}
    if status not in allowed:
        return False
    order.status = status
    db.session.commit()
    return True
