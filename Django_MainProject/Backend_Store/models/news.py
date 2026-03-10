from django.db import models
from datetime import datetime

class News(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=datetime.utcnow)
    headline = models.CharField(max_length=100, null=False)
    excerpt = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)

    def __repr__(self):
        return str({
            'id': self.id,
            'date': self.date,
            'headline': self.headline,
            'excerpt': self.excerpt,
            'content': self.content,
        })
        
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date,
            'headline': self.headline,
            'excerpt': self.excerpt,
            'content': self.content,
        }
        
    class Meta:
        db_table = 'news'