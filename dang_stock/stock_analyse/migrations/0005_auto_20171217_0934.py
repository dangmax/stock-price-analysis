# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-17 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock_analyse', '0004_auto_20171217_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='ma10',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ma20',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ma5',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='tor',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='vr',
            field=models.FloatField(default=0, null=True),
        ),
    ]