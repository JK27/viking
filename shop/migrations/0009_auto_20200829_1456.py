# Generated by Django 3.0.8 on 2020-08-29 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_product_master_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='base_colour',
        ),
        migrations.RemoveField(
            model_name='product',
            name='brand_logo_url',
        ),
        migrations.AlterField(
            model_name='category',
            name='friendly_name',
            field=models.CharField(blank=True, default='', max_length=254),
            preserve_default=False,
        ),
    ]
