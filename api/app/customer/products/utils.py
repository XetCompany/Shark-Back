from app.models import ProductCompany, User, Order, OrderStatus


def user_can_comment_product(user: User, product: ProductCompany):
    if not user.is_authenticated:
        return False

    is_order = Order.objects.filter(
        user=user, status=OrderStatus.ADOPTED, products__product=product
    ).exists()
    is_commented = product.evaluations.filter(author=user).exists()
    return is_order and not is_commented
