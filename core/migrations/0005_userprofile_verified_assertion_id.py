# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-24 21:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_userprofile_declaration_of_interests'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verified_assertion_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
