# Generated by Django 4.2.9 on 2024-06-08 07:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0007_order_shipping_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='shipping_company',
        ),
    ]