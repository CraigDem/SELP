# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0005_userprofile_soldiers'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tanks',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
