# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-11-23 11:45
from __future__ import unicode_literals
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    # Moved to separate migration to exclude this errors:
    # django.db.utils.OperationalError: cannot DROP TABLE "document_documenttypefield" because it has pending trigger events
    dependencies = [
        ('document', '0107_data_document_type_fields_to_1_n'),
    ]
    operations = [
        migrations.RemoveField(
            model_name='documenttype',
            name='fields',
        ),
        migrations.DeleteModel(
            name='DocumentTypeField',
        ),
        migrations.RemoveField(
            model_name='documentfielddetector',
            name='document_type',
        ),
        migrations.AlterModelOptions(
            name='documentfield',
            options={'ordering': ('long_code',)},
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='long_code',
            field=models.CharField(default=None, max_length=150, unique=True),
        ),
        migrations.RemoveField(
            model_name='classifiermodel',
            name='document_type',
        ),
        migrations.RemoveField(
            model_name='externalfieldvalue',
            name='type_id',
        ),
        migrations.RenameModel(
            old_name='DocumentTypeFieldCategory',
            new_name='DocumentFieldCategory',
        ),
        migrations.AlterModelOptions(
            name='documentfieldcategory',
            options={'ordering': ('order', 'name'), 'verbose_name_plural': 'Document Field Categories'},
        ),
        migrations.AlterField(
            model_name='classifiermodel',
            name='document_field',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE,
                                    to='document.DocumentField'),
        ),
    ]