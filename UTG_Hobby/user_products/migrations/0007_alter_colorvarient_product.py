# Generated by Django 4.2.8 on 2023-12-21 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_products', '0006_remove_image_varient_image_variant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colorvarient',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colorvarient', to='user_products.products'),
        ),
    ]
