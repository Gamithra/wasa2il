# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-08-05 15:56
from __future__ import unicode_literals

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
            name='EmailConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40)),
                ('timing_created', models.DateTimeField(auto_now=True)),
                ('action', models.CharField(choices=[('email_change', 'Email change')], max_length=30)),
                ('data', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_confirmations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]