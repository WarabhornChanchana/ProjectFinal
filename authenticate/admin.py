from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import *
# Register your models here.

@admin.register(Address)
class Address(admin.ModelAdmin):
    list_display = ('account','street', 'district', 'city' , 'postal_code')

class AccountInline(admin.StackedInline): #แสดงและแก้ไขข้อมูลของโมเดลที่มีความสัมพันธ์แบบ foreign key หรือ one-to-one โดยตรงจากหน้า admin
    model = Account 
    can_delete = False # ตั้งค่าให้ไม่สามารถลบข้อมูลโมเดลที่เชื่อมโยงกันออกได้
    verbose_name_plural = "Account" # กำหนดชื่อที่แสดงในหน้า admin

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline,)
admin.site.unregister(User,)
admin.site.register(User, CustomizedUserAdmin)




@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'role' , 'created_at' , 'updated_at')

