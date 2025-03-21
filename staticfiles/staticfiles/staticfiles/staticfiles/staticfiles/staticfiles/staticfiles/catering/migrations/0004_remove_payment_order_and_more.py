# Generated by Django 5.1.6 on 2025-02-17 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catering', '0003_eventbooking_menu_items_eventbooking_payment_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.RemoveField(
            model_name='eventbooking',
            name='payment_status',
        ),
        migrations.RemoveField(
            model_name='eventbooking',
            name='razorpay_order_id',
        ),
        migrations.AddField(
            model_name='eventbooking',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
