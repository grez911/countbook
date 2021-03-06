# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 09:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_name', models.TextField()),
                ('show', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Records',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.Operations')),
            ],
        ),
    ]
