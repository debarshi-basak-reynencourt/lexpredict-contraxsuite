# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-15 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_celery_task_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]