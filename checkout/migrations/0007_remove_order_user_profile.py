# Generated by Django 3.0.8 on 2020-08-21 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0006_order_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user_profile',
        ),
    ]
