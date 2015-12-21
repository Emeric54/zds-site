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
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=80, verbose_name=b'Titre de la demande')),
                ('slug', models.SlugField(max_length=80)),
                ('subtitle', models.CharField(max_length=120, verbose_name=b'Sous-titre de la demande')),
                ('comment', models.TextField(verbose_name=b'Commentaire du demandeur')),
                ('user', models.ForeignKey(verbose_name='Membre', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
