# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-13 03:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analyse', '0002_auto_20171212_1516'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together=set([('stock_id', 'pub_date')]),
        ),
    ]
