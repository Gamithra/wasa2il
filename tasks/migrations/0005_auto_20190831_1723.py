# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-31 17:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_auto_20190831_1623'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='description',
            new_name='detailed_description',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='objectives',
            new_name='short_description',
        ),
    ]
