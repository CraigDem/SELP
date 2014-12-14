# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0013_nation_paid_bills'),
    ]

    operations = [
        migrations.AddField(
            model_name='nation',
            name='collect_taxes',
            field=models.DateField(default=datetime.datetime(2014, 12, 14, 1, 51, 8, 969030, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
