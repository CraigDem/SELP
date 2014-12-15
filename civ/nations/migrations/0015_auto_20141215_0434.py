# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0014_nation_collect_taxes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='funds',
            field=models.FloatField(default=10000.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nation',
            name='infrastructure',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nation',
            name='land',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nation',
            name='technology',
            field=models.FloatField(default=1.0),
            preserve_default=True,
        ),
    ]
