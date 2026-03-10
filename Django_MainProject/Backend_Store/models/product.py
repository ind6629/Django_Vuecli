from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    price = models.FloatField(null=False)
    image = models.CharField(max_length=1000, null=False)
    stock = models.IntegerField(null=False)
    description = models.TextField(null=False)
    category = models.CharField(max_length=50, null=False)
    type = models.CharField(max_length=50, null=False)
    
    user_id = models.IntegerField(null=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'stock': self.stock,
            'description': self.description,
            'type': self.type
        }

    def __repr__(self):
        return f'<Product {self.name}>'
    
    class Meta:
        db_table = 'product'