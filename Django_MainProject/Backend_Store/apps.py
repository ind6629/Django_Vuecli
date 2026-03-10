from django.apps import AppConfig


class BackendStoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Backend_Store"

    def ready(self):
        # 确保模型被加载
        from . import models  # 关键！