from django.db import models
from authenticate.models import Account
from products.models import Product
from django.utils.translation import gettext_lazy as _

class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('cart')
        verbose_name_plural = _('carts')

    def __str__(self):
        return f"Cart for {self.account.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart {self.cart.id}"
