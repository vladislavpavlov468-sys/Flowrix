from extensions import db
from models import Order, OrderItem, Product, User


def get_or_create_cart(user: User) -> Order:
    cart = Order.query.filter_by(user_id=user.id, status="new").first()
    if not cart:
        cart = Order(user_id=user.id, status="new")
        db.session.add(cart)
        db.session.commit()
    return cart


def add_item_to_cart(user: User, product_id: int, quantity: int = 1) -> None:
    cart = get_or_create_cart(user)
    product = Product.query.get(product_id)

    if not product or not product.is_available:
        return

    existing_item = OrderItem.query.filter_by(
        order_id=cart.id, product_id=product_id
    ).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = OrderItem(
            order_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price_at_purchase=product.price
        )
        db.session.add(new_item)

    db.session.commit()


def remove_item_from_cart(user: User, item_id: int) -> bool:
    cart = get_or_create_cart(user)
    item = OrderItem.query.filter_by(id=item_id, order_id=cart.id).first()

    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False


def clear_cart(user: User) -> bool:
    cart = get_or_create_cart(user)
    if cart.items:
        OrderItem.query.filter_by(order_id=cart.id).delete()
        db.session.commit()
        return True
    return False


def checkout_cart(user: User) -> bool:
    cart = get_or_create_cart(user)

    if not cart.items:
        return False

    cart.status = "in_progress"
    db.session.commit()
    return True


def get_user_orders(user: User) -> list[Order]:
    return Order.query.filter(
        Order.user_id == user.id,
        Order.status != "new"
    ).order_by(Order.created_at.desc()).all()


def get_cart_data(user: User) -> dict:
    cart = get_or_create_cart(user)

    items_data = []
    for item in cart.items:
        if item.product:
            items_data.append({
                "id": item.id,
                "product_id": item.product.id,
                "product_name": item.product.name,
                "price": float(item.price_at_purchase),
                "quantity": item.quantity,
                "subtotal": item.subtotal
            })

    return {
        "id": cart.id,
        "total": cart.cart_total,
        "items_count": cart.items_count,
        "items": items_data
    }
