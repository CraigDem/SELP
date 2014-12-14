# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0011_auto_20141209_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nation',
            name='soldiers',
        ),
        migrations.RemoveField(
            model_name='nation',
            name='tanks',
        ),
    ]
