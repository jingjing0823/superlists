# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-06-26 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0007_auto_20190614_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(),
        ),
    ]
