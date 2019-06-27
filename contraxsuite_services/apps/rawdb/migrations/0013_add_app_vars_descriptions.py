# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-12-29 17:14
from __future__ import unicode_literals

from django.db import migrations


def do_migrate(apps, schema_editor):
    AppVar = apps.get_model('common', 'AppVar')
    from apps.rawdb.constants import APP_VAR_DISABLE_RAW_DB_CACHING_NAME
    description = 'Disables automatic caching of documents into raw db tables when document type / document field ' \
                  'structures are changed via the admin app or when a document is loaded / changed. ' \
                  'Values: true / false (json)'

    v, created = AppVar.objects.get_or_create(name=APP_VAR_DISABLE_RAW_DB_CACHING_NAME, defaults={
        'name': APP_VAR_DISABLE_RAW_DB_CACHING_NAME,
        'value': False,
        'description': description
    })

    if not created:
        v.description = description
        v.save()


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0014_appvar_description'),
        ('rawdb', '0012_add_postgres_index_extension')
    ]

    operations = [
        migrations.RunPython(do_migrate, reverse_code=migrations.RunPython.noop),
    ]