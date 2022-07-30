from django.db import models

import datetime
from django.db.models.deletion import CASCADE


class Regions(models.Model):
    region     = models.CharField(null=False,max_length=1000)
    
    
class Datasources(models.Model):
    datasource = models.CharField(null=False,max_length=1000)
    
    
class Trips(models.Model):
    region                       = models.ForeignKey(Regions, related_name="regions_trips",on_delete=CASCADE)
    origin_coord_longitud        = models.CharField(null=False,max_length=1000)
    origin_longitud_round        = models.FloatField(null=False,db_index=True) 
    origin_coord_latitud         = models.CharField(null=False,max_length=1000)
    origin_latitud_round         = models.FloatField(null=False,db_index=True)
    destination_coord_longitud   = models.CharField(null=False,max_length=1000)
    destination_longitud_round   = models.FloatField(null=False,db_index=True)
    destination_coord_latitud    = models.CharField(null=False,max_length=1000)
    destination_latitud_round    = models.FloatField(null=False,db_index=True)
    datetime                     = models.DateTimeField()
    datasource                   = models.ForeignKey(Datasources, related_name="dataSource_trips", on_delete=CASCADE)


    
    