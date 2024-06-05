# Generated by Django 4.2.9 on 2024-05-29 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_tracking_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adminorder',
            name='tracking_number',
        ),
        migrations.AlterField(
            model_name='adminorder',
            name='shipping_details',
            field=models.CharField(blank=True, choices=[('EMS', 'EMS'), ('Kerry', 'Kerry'), ('DHL', 'DHL'), ('J&T Express', 'J&T Express'), ('Flash Express', 'Flash Express')], max_length=50),
        ),
    ]
