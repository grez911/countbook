# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-08 17:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_auto_20171008_1824'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='operation_name',
            new_name='name',
        ),
    ]