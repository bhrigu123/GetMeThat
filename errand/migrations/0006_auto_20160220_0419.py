# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-19 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('errand', '0005_auto_20160220_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='errand.Role'),
        ),
    ]