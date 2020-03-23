# Generated by Django 2.2.11 on 2020-03-23 06:36

from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('facility', '0010_facility_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facility',
            name='image',
            field=stdimage.models.StdImageField(blank=True, default='court.png', upload_to='facility'),
        ),
    ]
