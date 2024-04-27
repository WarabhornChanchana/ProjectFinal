from django import forms
from .models import PaymentUpload

from django import forms
from django.forms import DateTimeInput
from .models import PaymentUpload

class PaymentUploadForm(forms.ModelForm):
    class Meta:
        model = PaymentUpload
        fields = ['name', 'phone', 'amount', 'transfer_time', 'payment_slip']
        widgets = {
            'transfer_time': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


