# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageSent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sender', models.CharField(max_length=30)),
                ('receiver', models.CharField(max_length=30)),
                ('message', models.TextField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='password',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='message',
            name='username',
            field=models.CharField(max_length=30),
        ),
    ]
