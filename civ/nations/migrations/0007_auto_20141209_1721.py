# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0006_userprofile_tanks'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='religion',
            field=models.CharField(default=b'None', max_length=30),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='government',
            field=models.CharField(default=b'Democracy', max_length=30),
            preserve_default=True,
        ),
    ]
