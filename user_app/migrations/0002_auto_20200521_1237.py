# Generated by Django 2.2.10 on 2020-05-21 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restraunt',
            name='address',
        ),
        migrations.RemoveField(
            model_name='restraunt',
            name='manager_name',
        ),
        migrations.AddField(
            model_name='profile',
            name='add_tax',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=150, null=True, verbose_name='address'),
        ),
        migrations.AddField(
            model_name='profile',
            name='centre_gst',
            field=models.IntegerField(null=True, verbose_name='CGST'),
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', null=True, upload_to='', verbose_name='Profile Pics'),
        ),
        migrations.AddField(
            model_name='profile',
            name='manager_name',
            field=models.CharField(max_length=50, null=True, verbose_name='manager'),
        ),
        migrations.AddField(
            model_name='profile',
            name='state_gst',
            field=models.IntegerField(null=True, verbose_name='SGST'),
        ),
    ]