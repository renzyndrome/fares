# Generated by Django 2.2.11 on 2020-08-27 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cart_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
