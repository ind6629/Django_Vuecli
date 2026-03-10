from django.db import models
from django.utils import timezone
from datetime import datetime

class TrackClick(models.Model):
    id = models.AutoField(primary_key=True)
    event_type = models.IntegerField(null=False)
    product_id = models.CharField(max_length=50, null=False)
    user_id = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'track_click'

class TrackCart(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, null=False)
    product_id = models.IntegerField(null=False)
    user_id = models.CharField(max_length=100, null=False)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'track_cart'

class Track(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.CharField(max_length=255, null=False)
    user_id = models.IntegerField(null=False)
    timestamp = models.DateTimeField(default=datetime.utcnow, db_index=True)

    def __repr__(self):
        return f'<Track {self.id}>'
    
    class Meta:
        db_table = 'track'

class TrackSearch(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(null=False)
    user_id = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'track_search'

class TrackOrder(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True, blank=True)
    product_id = models.IntegerField(null=False)
    category = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'track_order'