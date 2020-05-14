# Generated by Django 2.2.10 on 2020-05-03 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_app.Category'),
        ),
        migrations.AddField(
            model_name='item',
            name='cuisine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu_app.Cuisine'),
        ),
        migrations.AddField(
            model_name='cuisine',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]