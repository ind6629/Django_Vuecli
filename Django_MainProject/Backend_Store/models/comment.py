from django.db import models
from django.utils import timezone

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    product_id = models.IntegerField()
    content = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(null=True, blank=True)

    user_id = models.IntegerField(null=False)
    product_id = models.IntegerField(null=False)

    def __repr__(self):
        return f'<Comment {self.content[:20]}...>'
    
    class Meta:
        db_table = 'comment'