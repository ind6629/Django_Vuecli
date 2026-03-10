from django.db import models
from django.utils import timezone
from datetime import datetime

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    quantity = models.IntegerField(null=False)
    total_price = models.FloatField(null=False)
    timestamp = models.DateTimeField(default=timezone.now)
    user_id = models.IntegerField(null=False)
    product_id = models.IntegerField(null=False)

    def __repr__(self):
        return f'<Order {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'total_price': self.total_price
        }
        
    class Meta:
        db_table = 'order'