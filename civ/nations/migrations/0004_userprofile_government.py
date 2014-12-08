# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0003_auto_20141208_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='government',
            field=models.CharField(default='Democracy', max_length=200),
            preserve_default=False,
        ),
    ]
