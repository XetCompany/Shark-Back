from app.models import ProductCompany, User, Order, OrderStatus, Cart, CartProduct


def user_can_comment_product(user: User, product: ProductCompany):
    if not user.is_authenticated:
        return False

    is_order = Order.objects.filter(
        user=user, status=OrderStatus.ADOPTED, products__product=product
    ).exists()
    is_commented = product.evaluations.filter(author=user).exists()
    return is_order and not is_commented


def user_can_add_product_to_cart(user: User, product: ProductCompany):
    if not user.is_authenticated:
        return False

    cart = Cart.objects.get_or_create(user=user)[0]
    return not cart.products.filter(product=product).exists()
