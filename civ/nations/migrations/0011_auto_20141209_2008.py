# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0010_auto_20141209_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nation',
            name='infrastructure',
            field=models.DecimalField(default=1.0, max_digits=19, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nation',
            name='land',
            field=models.DecimalField(default=1.0, max_digits=19, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nation',
            name='technology',
            field=models.DecimalField(default=1.0, max_digits=19, decimal_places=2),
            preserve_default=True,
        ),
    ]
