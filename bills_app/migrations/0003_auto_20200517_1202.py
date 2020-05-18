# Generated by Django 2.2.10 on 2020-05-17 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_app', '0002_auto_20200503_1318'),
        ('bills_app', '0002_auto_20200503_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bills',
            name='items',
        ),
        migrations.AddField(
            model_name='bills',
            name='items',
            field=models.ManyToManyField(null=True, to='menu_app.Item'),
        ),
    ]
