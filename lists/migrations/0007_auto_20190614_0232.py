# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-14 02:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_auto_20190614_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='lists.List'),
        ),
    ]
