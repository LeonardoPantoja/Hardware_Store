# Generated by Django 4.1.7 on 2023-11-24 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware_store', '0006_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
