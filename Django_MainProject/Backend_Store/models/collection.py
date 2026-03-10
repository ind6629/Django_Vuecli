from django.db import models

class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    # user_id = models.IntegerField()
    # product_id = models.IntegerField()

    user_id = models.IntegerField(null=False)

    product_id = models.IntegerField(null=False)

    def __repr__(self):
        return str({
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id
        })
        
    class Meta:
        db_table = 'collection'