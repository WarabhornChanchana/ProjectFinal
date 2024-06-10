# Generated by Django 4.2.9 on 2024-06-08 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_cart_delivery_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_company',
            field=models.CharField(choices=[('EMS', 'EMS'), ('Kerry', 'Kerry'), ('DHL', 'DHL'), ('J&T Express', 'J&T Express'), ('Flash Express', 'Flash Express')], default='EMS', max_length=20),
        ),
    ]
