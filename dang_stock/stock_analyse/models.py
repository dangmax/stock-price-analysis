# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Stock(models.Model):
    stock_id = models.CharField(max_length=6)
    open = models.FloatField(null=True)
    close = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    vol = models.BigIntegerField(null=True)
    amount = models.FloatField(null=True)
    pub_date = models.CharField(max_length=10)
    tor = models.FloatField(null=True,default=0)
    vr  = models.FloatField(null=True,default=0)
    ma5 = models.FloatField(null=True,default=0)
    ma10 = models.FloatField(null=True,default=0)
    ma20 = models.FloatField(null=True,default=0)

    class Meta:
        unique_together = ("stock_id","pub_date")