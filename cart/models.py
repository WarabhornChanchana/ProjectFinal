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

from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    # อื่นๆที่ต้องการเพิ่มเติมในรายการสั่งซื้อ

class AdminOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_orders')
    payment_slip = models.ImageField(upload_to='payment_slips/')
    # อื่นๆที่ต้องการเพิ่มเติมในรายการสั่งซื้อของแอดมิน


from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_time = models.TimeField(auto_now_add=True)  # เพิ่มฟิลด์เวลา

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} on {self.payment_date} at {self.payment_time}"
