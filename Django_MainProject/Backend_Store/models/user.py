from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime

class User(AbstractUser):
    # 基础字段
    username = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.EmailField(max_length=120, unique=True, db_index=True)
    registered_on = models.DateTimeField(default=datetime.utcnow)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    
    # 密码字段（使用Django内置安全存储）
    password = models.CharField(max_length=128) 
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="backend_store_user_groups",  # 添加唯一related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="backend_store_user_permissions",  # 添加唯一related_name
        related_query_name="user",
    )

    # 保持原始方法签名但改进实现
    def set_password(self, raw_password):
        """改进：使用Django的安全密码哈希"""
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """改进：安全验证密码"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return f'<User {self.username}>'

    class Meta:
        db_table = 'user' 