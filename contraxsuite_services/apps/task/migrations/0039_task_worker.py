# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-22 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0038_remove_task_own_date_work_start'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='worker',
            field=models.CharField(blank=True, db_index=True, max_length=1024, null=True),
        ),
    ]