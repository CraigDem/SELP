# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0015_auto_20141215_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='funds',
            field=models.DecimalField(default=10000.0, max_digits=19, decimal_places=2),
            preserve_default=True,
        ),
    ]
