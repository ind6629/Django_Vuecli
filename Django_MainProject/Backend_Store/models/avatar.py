from django.db import models

class Avatar(models.Model):
    class Meta:
        db_table = 'avatar'  # 保持原表名

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    avatar =  models.CharField(max_length=200, null=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'avatar': self.avatar,
        }

    def __repr__(self):
        return f'<Cartresult_Sparkstream {self.id}>'