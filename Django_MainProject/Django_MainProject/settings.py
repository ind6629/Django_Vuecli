"""
Django settings for Django_MainProject project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ================== 基础配置 ==================
SECRET_KEY = "django-insecure-jpqi(xbiv@shy)(*@9_juwf9t(fhldepga6d_j$kwf(p!dn)-o"
DEBUG = True
ALLOWED_HOSTS = ['*']  # 开发环境允许所有主机

# ================== 应用和中间件配置 ==================
INSTALLED_APPS = [
    'corsheaders',  # 必须放在前面
    'Backend_Store',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必须第一个
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ================== 跨域配置 ==================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True  # 允许携带凭证
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']  # 暴露自定义头

# ================== 会话和Cookie配置 ==================
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 86400  # 24小时
SESSION_COOKIE_SAMESITE = 'Lax'  # 跨站传递Cookie
SESSION_COOKIE_SECURE = False  # 开发环境可False
SESSION_COOKIE_HTTPONLY = True  # 防止XSS
SESSION_COOKIE_DOMAIN = None    # 开发环境保持None

CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False  # 允许JS读取
CSRF_COOKIE_DOMAIN = None     # 开发环境保持None
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS  # 同步跨域配置

# ================== 其他配置 ==================
ROOT_URLCONF = "Django_MainProject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'frontend/dist')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Django_MainProject.wsgi.application"

# ================== 数据库配置 ==================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_database',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}

# ================== 密码验证 ==================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
]

# ================== 国际化 ==================
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

# ================== 静态文件 ==================
STATIC_URL = "static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/dist/static"),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ================== 生产环境检查 ==================
if not DEBUG:
    # 生产环境必须启用HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_DOMAIN = '.yourdomain.com'  # 生产域名
    CSRF_COOKIE_DOMAIN = '.yourdomain.com'
    # 限制允许的主机
    ALLOWED_HOSTS = ['your-production-domain.com']
    # 更严格的CORS设置
    CORS_ALLOWED_ORIGINS = [
        "https://your-production-domain.com",
        "https://www.your-production-domain.com"
    ]