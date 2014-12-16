# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0016_auto_20141215_0436'),
    ]

    operations = [
        migrations.AddField(
            model_name='nation',
            name='citizens',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nation',
            name='tax_rate',
            field=models.IntegerField(default=20),
            preserve_default=True,
        ),
    ]
