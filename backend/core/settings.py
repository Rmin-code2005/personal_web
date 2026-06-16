from decouple import config
from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='localhost,127.0.0.1'
).split(',')

# =========================
# Apps
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'storages',
    'corsheaders',

    'portfolio',
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # باید قبل از CommonMiddleware باشه ✅
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = "core.wsgi.application"

# =========================
# Templates
# =========================
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

# =========================
# Database
# =========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='portfolio'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# =========================
# Static files
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# =========================
# S3 / Liara Object Storage
# =========================
AWS_ACCESS_KEY_ID = os.environ.get("LIARA_ACCESS_KEY", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("LIARA_SECRET_KEY", "")
AWS_STORAGE_BUCKET_NAME = os.environ.get("LIARA_BUCKET_NAME", "")
AWS_S3_ENDPOINT_URL = os.environ.get("LIARA_ENDPOINT", "")

# اگه endpoint بدون https بود، اضافه می‌کنیم
if AWS_S3_ENDPOINT_URL and not AWS_S3_ENDPOINT_URL.startswith("http"):
    AWS_S3_ENDPOINT_URL = "https://" + AWS_S3_ENDPOINT_URL

AWS_QUERYSTRING_AUTH = False          # URL های عمومی بدون signature
AWS_DEFAULT_ACL = "public-read"       # 🔥 FIX: عکس‌ها باید public باشن
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_SIGNATURE_VERSION = "s3v4"

# 🔥 FIX اصلی: تعریف custom domain برای URL درست عکس‌ها
# فرمت لیارا: storage.iran.liara.space/BUCKET_NAME
_endpoint_host = AWS_S3_ENDPOINT_URL.replace("https://", "").replace("http://", "") if AWS_S3_ENDPOINT_URL else ""
AWS_S3_CUSTOM_DOMAIN = f"{_endpoint_host}/{AWS_STORAGE_BUCKET_NAME}" if _endpoint_host and AWS_STORAGE_BUCKET_NAME else ""

# 🔥 FIX: MEDIA_URL باید به S3 اشاره کنه، نه /media/
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/" if AWS_S3_CUSTOM_DOMAIN else "/media/"

# =========================
# CORS
# =========================
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173"
).split(",")

# 🔥 FIX: اجازه دادن به مرورگر برای خوندن هدرهای S3
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# =========================
# DRF
# =========================
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Personal Portfolio API',
    'DESCRIPTION': 'API سایت شخصی',
    'VERSION': '1.0.0',
}

# =========================
# Security
# =========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# =========================
# STORAGE BACKENDS
# =========================
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =========================
# Prevent OOM (admin upload fix)
# =========================
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024   # 5MB

# =========================
# Prevent collectstatic crash on Liara
# =========================
if "collectstatic" in sys.argv:
    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    AWS_STORAGE_BUCKET_NAME = ""
    AWS_S3_ENDPOINT_URL = ""