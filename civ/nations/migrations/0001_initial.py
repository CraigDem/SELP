# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Nation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infrastructure', models.IntegerField(default=1)),
                ('technology', models.IntegerField(default=1)),
                ('land', models.IntegerField(default=1)),
                ('resource_1', models.CharField(max_length=200)),
                ('resource_2', models.CharField(max_length=200)),
                ('ruler', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('initiator', models.ForeignKey(related_name='+', to='nations.Nation')),
                ('reciever', models.ForeignKey(related_name='+', to='nations.Nation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='War',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(auto_now_add=True)),
                ('attacker', models.ForeignKey(related_name='+', to='nations.Nation')),
                ('defender', models.ForeignKey(related_name='+', to='nations.Nation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
