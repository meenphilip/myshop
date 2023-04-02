from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    # Add an item to cart
    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    # save modified cart
    def save(self):
        """
        make the session as 'modified' to make sure it gets saved
        """
        self.session.modified = True

    # remove product from cart
    def remove(self, product):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # Iterate thru cart items & get related product
    def __iter__(self):
        """
        Iterate over the item in the cart and get the product from the database
        """
        product_ids = self.cart.keys()
        # get products object and add them to cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    # Get total number of items in cart
    def __len__(self):
        """
        Count all items in cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    # Calculate cart total
    def get_total(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    # Clear cart
    def clear(self):
        """
        Remove cart from the session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()