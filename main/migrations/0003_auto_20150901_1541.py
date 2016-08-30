# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20150901_1539'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='MessageSetting',
        ),
    ]
