# Generated by Django 4.1.7 on 2023-11-07 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware_store', '0002_cart_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(max_length=300, verbose_name='Product image'),
        ),
    ]