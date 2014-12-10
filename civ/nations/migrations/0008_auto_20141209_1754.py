# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0007_auto_20141209_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='government',
            field=models.CharField(default=b'Democratic', max_length=30),
            preserve_default=True,
        ),
    ]
