from django import forms
from django.forms import DateTimeInput
from .models import PaymentUpload
from django import forms
from .models import Order
from django import forms
from .models import Order, AdminOrder

class PaymentUploadForm(forms.ModelForm):
    class Meta:
        model = PaymentUpload
        fields = ['name', 'phone', 'amount', 'transfer_time', 'payment_slip', 'order']
        widgets = {
            'transfer_time': DateTimeInput(attrs={'type': 'datetime-local'}),
            'order': forms.HiddenInput(),  # Hide order field in the form
            'amount': forms.HiddenInput(),  # Hide amount field in the form
        }


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_status', 'tracking_number', 'delivery_method']
        widgets = {
            'order_status': forms.Select(choices=Order.order_status_choices),
            'tracking_number': forms.TextInput(),
            'delivery_method': forms.Select(choices=Order.delivery_method_choices),
        }

class AdminOrderForm(forms.ModelForm):
    class Meta:
        model = AdminOrder
        fields = ['shipping_details']
        widgets = {
            'shipping_details': forms.Select(choices=Order.SHIPPING_CHOICES),
        }

