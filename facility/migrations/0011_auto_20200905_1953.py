# Generated by Django 2.2.11 on 2020-09-05 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0010_auto_20200905_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]
