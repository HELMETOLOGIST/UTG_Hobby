# Generated by Django 4.2.8 on 2024-02-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_products', '0009_remove_colorvarient_category_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorvarient',
            name='category_offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]