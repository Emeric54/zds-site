# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contentrequest', '0002_auto_20151216_2114'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['-pubdate'], 'verbose_name': 'Request', 'verbose_name_plural': 'Requests'},
        ),
        migrations.AddField(
            model_name='request',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 17, 19, 57, 57, 442482), auto_now_add=True, verbose_name='Date de cr\xe9ation', db_index=True),
            preserve_default=False,
        ),
    ]
