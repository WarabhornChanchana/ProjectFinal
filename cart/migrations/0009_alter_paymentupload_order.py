# Generated by Django 4.2.9 on 2024-05-16 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_alter_adminorder_order_alter_paymentupload_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentupload',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='cart.order'),
        ),
    ]
