from django.db import models
from authenticate.models import Account
from products.models import Product
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(default=timezone.now)
    order_status_choices = [
        ('PENDING', 'รอดำเนินการ'),
        ('PROCESSING', 'กำลังดำเนินการ'),
        ('PREPARED', 'เตรียมของเสร็จแล้ว'),
        ('SHIPPED', 'จัดส่งแล้ว'),
        ('DELIVERED', 'จัดส่งสำเร็จ'),
        ('RECEIVED', 'รับสินค้าแล้ว'),
        ('CANCELLED', 'ยกเลิก'),
    ]

    order_status = models.CharField(max_length=20, choices=order_status_choices, default='PENDING')
    tracking_number = models.CharField(max_length=50, blank=True, null=True)
    SHIPPING_CHOICES = [
        ('EMS', 'EMS'),
        ('Kerry', 'Kerry'),
        ('DHL', 'DHL'),
        ('J&T Express', 'J&T Express'),
        ('Flash Express', 'Flash Express'),
    ]
    delivery_method_choices = [
        ('pickup', 'รับที่ร้าน'),
        ('delivery', 'จัดส่ง'),
    ]
    delivery_method = models.CharField(max_length=20, choices=delivery_method_choices)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delivery_method = models.CharField(max_length=20, choices=Order.delivery_method_choices, default='pickup')

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


class AdminOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_orders')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_slip = models.ImageField(upload_to='payment_slips/')
    shipping_details = models.CharField(max_length=50, choices=Order.SHIPPING_CHOICES, blank=True)


   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class PaymentUpload(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transfer_time = models.DateTimeField()
    payment_slip = models.FileField(upload_to='paymentslips/')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments', null=True, blank=True)



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])  # Ratings from 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for Order {self.order.id}"


