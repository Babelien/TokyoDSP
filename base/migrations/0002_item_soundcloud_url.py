# Generated by Django 4.2.7 on 2025-02-17 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='soundcloud_url',
            field=models.URLField(blank=True),
        ),
    ]
