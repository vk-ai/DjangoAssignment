# Generated by Django 3.0.5 on 2020-04-27 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0003_auto_20200427_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingdetails',
            name='orderDetails',
            field=models.ManyToManyField(blank=True, null=True, to='shipments.OrderDetails'),
        ),
    ]
