# Generated by Django 3.0.8 on 2020-08-04 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0006_auto_20200804_1547'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category_description',
            new_name='full_description',
        ),
        migrations.AddField(
            model_name='category',
            name='short_description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]