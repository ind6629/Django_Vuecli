from django.db import models

class Cart(models.Model):
    # 主键（Django会自动创建，此处显式声明以保持与Flask一致）
    id = models.AutoField(primary_key=True)
    
    # 数量字段
    quantity = models.IntegerField(null=False)
    
    # 用户关系
    user_id = models.IntegerField(null=False)
    
    # 商品关系
    product_id = models.IntegerField(null=False)

    def __repr__(self):
        return f'<Cart {self.id}>'
    
    class Meta:
        db_table = 'cart'
        
    def to_dict(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'user_id': self.user_id,
            'product_id': self.product_id,
        }
    
    