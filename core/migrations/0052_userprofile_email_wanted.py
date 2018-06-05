# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-22 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20180117_2240'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email_wanted',
            field=models.BooleanField(default=False, help_text='Whether to consent to receiving notifications via email.', verbose_name='Consent for sending email'),
        ),
    ]