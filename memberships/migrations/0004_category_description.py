# Generated by Django 3.0.8 on 2020-07-28 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0003_auto_20200728_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
