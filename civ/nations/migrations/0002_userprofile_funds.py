# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='funds',
            field=models.IntegerField(default=10000),
            preserve_default=True,
        ),
    ]
