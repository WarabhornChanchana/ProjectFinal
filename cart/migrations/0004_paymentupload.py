# Generated by Django 4.2.9 on 2024-04-27 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_order_adminorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transfer_time', models.DateTimeField()),
                ('payment_slip', models.FileField(upload_to='paymentslips/')),
            ],
        ),
    ]