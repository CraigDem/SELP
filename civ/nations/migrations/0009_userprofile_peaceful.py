# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nations', '0008_auto_20141209_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='peaceful',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
