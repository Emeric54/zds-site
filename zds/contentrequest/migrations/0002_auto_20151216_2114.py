# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contentrequest', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'verbose_name': 'Request', 'verbose_name_plural': 'Requests'},
        ),
        migrations.AlterField(
            model_name='request',
            name='subtitle',
            field=models.CharField(max_length=120, verbose_name=b'Sous-titre de la demande', blank=True),
            preserve_default=True,
        ),
    ]
