# Generated by Django 3.0.8 on 2020-07-28 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0002_auto_20200727_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('friendly_name', models.CharField(blank=True, max_length=20, null=True)),
                ('slug', models.SlugField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
        migrations.AddField(
            model_name='membership',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='memberships.Category'),
        ),
    ]
