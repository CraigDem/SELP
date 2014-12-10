# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0004_userprofile_government'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='soldiers',
            field=models.IntegerField(default=10),
            preserve_default=True,
        ),
    ]
