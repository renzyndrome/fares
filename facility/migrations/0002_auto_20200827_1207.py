# Generated by Django 2.2.11 on 2020-08-27 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
