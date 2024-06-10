from cProfile import Profile
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Address

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='อีเมล')
    role_choices = [('admin', 'ผู้ดูแลระบบ'), ('customer', 'ลูกค้า'), ('employee', 'พนักงาน')]
    role = forms.ChoiceField(choices=role_choices, required=True, label='บทบาท')
    first_name = forms.CharField(max_length=100, required=True, label='ชื่อจริง')
    last_name = forms.CharField(max_length=100, required=True, label='นามสกุล')
    phone_number = forms.CharField(max_length=20, required=True, label='เบอร์โทรศัพท์')
    password1 = forms.CharField(label='รหัสผ่าน', widget=forms.PasswordInput)
    password2 = forms.CharField(label='ยืนยันรหัสผ่าน', widget=forms.PasswordInput)
    admin_code = forms.CharField(required=False, label='โค้ดสำหรับผู้ดูแลระบบ')

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "role", "phone_number", "admin_code"]
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')
        admin_code = cleaned_data.get('admin_code')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "รหัสผ่านต้องตรงกัน")
        if role == 'admin' and admin_code != '513875':
            self.add_error('admin_code', "โค้ดสำหรับผู้ดูแลระบบไม่ถูกต้อง")
        return cleaned_data




class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150, widget=forms.TextInput)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'district', 'city', 'postal_code']
        labels = {
            'street': 'ที่อยู่/ถนน',
            'district': 'เขต/อำเภอ',
            'city': 'จังหวัด',
            'postal_code': 'รหัสไปรษณีย์',
        }


# from django import forms
# from .models import Profile

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'email', 'phone_number', 'street', 'district', 'city', 'postal_code']

class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, required=False, label='ชื่อจริง')
    last_name = forms.CharField(max_length=100, required=False, label='นามสกุล')
    username = forms.CharField(label='ชื่อผู้ใช้', max_length=150, widget=forms.TextInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id
        if User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("อีเมลนี้มีผู้ใช้งานอยู่แล้ว")
        return email

class AddressEditForm(forms.ModelForm):
    street = forms.CharField(max_length=255, required=False, label='ที่อยู่/ถนน')
    district = forms.CharField(max_length=255, required=False, label='เขต/อำเภอ')
    city = forms.CharField(max_length=255, required=False, label='จังหวัด')
    postal_code = forms.CharField(max_length=10, required=False, label='รหัสไปรษณีย์')

    class Meta:
        model = Address
        fields = ["street", "district", "city", "postal_code"]
