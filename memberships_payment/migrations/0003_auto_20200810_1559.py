# Generated by Django 3.0.8 on 2020-08-10 15:59

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('memberships_payment', '0002_subscription_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]