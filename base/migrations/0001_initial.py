# Generated by Django 4.2.7 on 2025-02-17 07:17

import base.models.capture
import base.models.item
import base.models.order
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('slug', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
                ('order', models.IntegerField(default=32)),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('slug', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.CharField(default=base.models.order.custom_timestamp_id, editable=False, max_length=64, primary_key=True, serialize=False)),
                ('uid', models.CharField(editable=False, max_length=50)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('tax_included', models.PositiveIntegerField(default=0)),
                ('items', models.JSONField()),
                ('shipping', models.JSONField()),
                ('shipped_at', models.DateTimeField(blank=True, null=True)),
                ('canceled_at', models.DateTimeField(blank=True, null=True)),
                ('memo', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.CharField(default=base.models.item.create_id, editable=False, max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('price', models.PositiveIntegerField(default=0)),
                ('description', models.TextField(blank=True, default='')),
                ('sold_count', models.PositiveIntegerField(default=0)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, default='', upload_to=base.models.item.upload_image_to)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.category')),
                ('formats', models.ManyToManyField(to='base.format')),
                ('tags', models.ManyToManyField(to='base.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Capture',
            fields=[
                ('id', models.CharField(default=base.models.item.create_id, editable=False, max_length=32, primary_key=True, serialize=False)),
                ('data', models.FileField(upload_to=base.models.capture.upload_data_to)),
                ('format', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.format')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.item')),
            ],
        ),
    ]
