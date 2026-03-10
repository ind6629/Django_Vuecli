from django.db import models

class Orderesult_Sparkstream(models.Model):
    class Meta:
        db_table = 'orderesult_sparkstream'  # 保持原表名

    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100, null=False)
    times = models.IntegerField(null=False)
    date = models.CharField(max_length=100, null=False)

    def to_dict(self):
        return {
            'id': self.id,
            'category': self.category,
            'times': self.times,
            'date': self.date
        }

    def __repr__(self):
        return f'<Orderesult_Sparkstream {self.id}>'
    
    class Meta:
        db_table = 'orderesult_sparkstream'