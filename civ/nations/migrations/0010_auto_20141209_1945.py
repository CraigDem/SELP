# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nations', '0009_userprofile_peaceful'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nation_name', models.CharField(max_length=30)),
                ('funds', models.DecimalField(default=10000.0, max_digits=19, decimal_places=2)),
                ('government', models.CharField(default=b'Democratic', max_length=30)),
                ('religion', models.CharField(default=b'None', max_length=30)),
                ('infrastructure', models.IntegerField(default=1)),
                ('technology', models.IntegerField(default=1)),
                ('land', models.IntegerField(default=1)),
                ('resource1', models.CharField(max_length=200)),
                ('resource2', models.CharField(max_length=200)),
                ('soldiers', models.IntegerField(default=10)),
                ('tanks', models.IntegerField(default=1)),
                ('peaceful', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
