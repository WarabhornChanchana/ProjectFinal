from django.db import models
from authenticate.models import *
from products.models import Product
from django.utils.translation import gettext_lazy as _

class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('cart item')
        verbose_name_plural = _('cart items')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.account.user.username}"