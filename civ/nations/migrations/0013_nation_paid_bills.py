# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0012_auto_20141214_0038'),
    ]

    operations = [
        migrations.AddField(
            model_name='nation',
            name='paid_bills',
            field=models.DateField(default=datetime.datetime(2014, 12, 14, 1, 40, 54, 887192, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
