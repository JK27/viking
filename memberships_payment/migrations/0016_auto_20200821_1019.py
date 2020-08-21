# Generated by Django 3.0.8 on 2020-08-21 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20200812_1432'),
        ('memberships_payment', '0015_subscription_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='user_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subscriptions', to='profiles.UserProfile'),
        ),
    ]
