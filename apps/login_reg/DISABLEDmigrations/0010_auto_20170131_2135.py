# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-31 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0009_auto_20170131_2008'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quote',
            old_name='posted_by',
            new_name='poster_id',
        ),
        migrations.AddField(
            model_name='quote',
            name='poster_alias',
            field=models.CharField(default='', max_length=45),
            preserve_default=False,
        ),
    ]
