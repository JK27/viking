# Generated by Django 3.0.8 on 2020-08-08 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0011_auto_20200805_0835'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='stripe_plan_id',
            new_name='stripe_price_id',
        ),
    ]
